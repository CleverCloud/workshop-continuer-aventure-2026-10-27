# Démos

| Dossier | Partie | Quoi |
|---|---|---|
| [`1-app-python/`](1-app-python/) | 1–2 | Une app Flask (runtime Python classique) : `/`, `/health`, `/db` (PostgreSQL), `/files` |
| [`2-build-echoue/`](2-build-echoue/) | 3.1 | Version « v2 » : « ma nouvelle version n'est pas en ligne » |
| [`3-connexions/`](3-connexions/) | 3.2 | Version « v3 » : « ça marche, puis ça plante » |
| [`4-django-uv/`](4-django-uv/) | 4 | Django + uv + PostgreSQL (copie de [CleverCloud/django-todo-list-example](https://github.com/CleverCloud/django-todo-list-example)) |
| [`5-k8s/`](5-k8s/) | 5 | Manifests Kubernetes pour la démo CKE |

**Appliquer une version** (depuis le dossier de votre app) :

```bash
cp -R $LAB/demos/<scenario>/files/. .
git add -A && git commit -m "<scenario>"
clever deploy
```
