#!/usr/bin/env bash
# Trainer helper for the Lab 3 demo: Django todo-list with uv + PostgreSQL.
# Source: https://github.com/CleverCloud/django-todo-list-example (snapshot in this folder).
#
# Usage: ./setup.sh <org> [app-name] [zone] [--deploy]
#   Copies the app to ~/cc-training/<app-name>, makes it a Git repo, creates the
#   Clever Cloud app and a PostgreSQL add-on, links them and sets all variables.
#   Without --deploy, it stops before deploying: run `clever deploy` in the app
#   folder at the start of Lab 2, so the app is ready for the demo at 1:10.
set -euo pipefail

ORG="${1:?org required}"; NAME="${2:-django-todo-demo}"; ZONE="${3:-par}"
DEPLOY=false; for a in "$@"; do [[ "$a" == "--deploy" ]] && DEPLOY=true; done
[[ "$NAME" == "--deploy" ]] && NAME=django-todo-demo
[[ "$ZONE" == "--deploy" ]] && ZONE=par

SRC="$(cd "$(dirname "$0")" && pwd)"
WORK="$HOME/cc-training/$NAME"
mkdir -p "$WORK"
( cd "$SRC" && tar cf - --exclude=./setup.sh . ) | ( cd "$WORK" && tar xf - )
cd "$WORK"

if [[ ! -d .git ]]; then
  git init -q && git add . && git commit -qm "Initial commit"
fi
if [[ ! -f .clever.json ]]; then
  clever create --type python --org "$ORG" --region "$ZONE" "$NAME"
fi

clever addon create postgresql-addon "$NAME-pg" --plan dev --region "$ZONE" --org "$ORG" || echo "(add-on may already exist)"
clever service link-addon "$NAME-pg" || echo "(add-on may already be linked)"

# Domain: first hostname printed by `clever domain`. Override with DOMAIN=... if needed.
DOMAIN="${DOMAIN:-$(clever domain | grep -Eo '[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+' | head -1)}"
echo "Using ALLOWED_HOSTS=$DOMAIN"

clever env set SECRET_KEY "$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')"
clever env set ALLOWED_HOSTS "$DOMAIN"
clever env set CC_PYTHON_UV_SYNC_FLAGS "--frozen"
clever env set CC_PYTHON_UV_RUN_COMMAND ".venv/bin/uvicorn config.asgi:application --host 0.0.0.0 --port 8080"
clever env set CC_PRE_RUN_HOOK "uv run python manage.py migrate --noinput && uv run python manage.py collectstatic --noinput"

if $DEPLOY; then
  clever deploy --same-commit-policy restart
  echo "Deployed: https://$DOMAIN/"
else
  echo "Ready. To deploy: cd $WORK && clever deploy"
fi
