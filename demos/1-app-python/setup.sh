#!/usr/bin/env bash
# Intervenant : déploie l'app Python de zéro (app de secours pendant le workshop).
# Usage : ./setup.sh <nom-app> [--with-db] [--org <org>]
set -euo pipefail
NAME="${1:?nom de l'app requis}"; shift
WITH_DB=false; ORG_ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --with-db) WITH_DB=true ;;
    --org) shift; ORG_ARGS=(--org "$1") ;;
  esac; shift
done
SRC="$(cd "$(dirname "$0")" && pwd)"
WORK="$HOME/cc-workshop/$NAME"
mkdir -p "$WORK"
cp -n "$SRC/app.py" "$SRC/requirements.txt" "$SRC/.gitignore" "$WORK/"
cd "$WORK"
[ -d .git ] || { git init -q && git add . && git commit -qm "v1"; }
[ -f .clever.json ] || clever create --type python --region par "${ORG_ARGS[@]}" "$NAME"
clever env set CC_PYTHON_MODULE app:app
clever env set CC_PYTHON_VERSION 3.13
clever env set CC_HEALTH_CHECK_PATH /health
if $WITH_DB; then
  clever addon create postgresql-addon "$NAME-pg" --plan dev --region par "${ORG_ARGS[@]}" || echo "(add-on déjà existant ?)"
  clever service link-addon "$NAME-pg" || echo "(déjà lié ?)"
fi
clever deploy --same-commit-policy restart
clever domain
echo "OK. Dossier : $WORK"
