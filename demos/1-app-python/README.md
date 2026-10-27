# App Python — Workshop Clever Cloud

Une petite app Flask déployée avec le **runtime Python classique** : un `requirements.txt`, pas d'étape de build, pas de uv. La plateforme installe les dépendances et sert l'app (uWSGI derrière Nginx).

| Endpoint | Ce qu'il montre |
|---|---|
| `GET /` | version, numéro et id d'instance, commit |
| `GET /health` | cible du health check |
| `GET /db` | enregistre une visite dans PostgreSQL (nécessite un add-on PostgreSQL lié) |
| `GET /files` · `POST /files` | liste / écrit des fichiers sur le disque local (bonus : ils disparaissent au redéploiement — pourquoi ?) |

Obligatoire sur Clever Cloud : `CC_PYTHON_MODULE=app:app` (module `app.py`, objet Flask `app`).

`setup.sh` est un script pour l'intervenant (app de secours) : en lab, faites les étapes à la main.
