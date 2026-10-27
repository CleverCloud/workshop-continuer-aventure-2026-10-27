# Lab — Workshop développeurs Clever Cloud

*À suivre en direct ou à refaire après. Remplacez `<prenom>` par votre prénom (minuscules, sans espace). Chaque étape indique l'équivalent dans la Console.*

| | |
|---|---|
| Console | <https://console.clever-cloud.com> |
| Fichiers des démos | <https://github.com/CleverCloud/workshop-continuer-aventure-2026-10-27> |
| Zone utilisée | `par` (Paris) |
| Crédits du workshop | le code est donné en direct dans le chat du webinar (il n’est pas dans ce repo) |

> Les commandes Clever Tools qui gèrent une application s'exécutent **dans le dossier de l'app** : il est relié à l'application par le fichier `.clever.json` créé par `clever create`.

---

## Étape 0 — Compte et CLI (5 min)

1. Créez votre compte sur <https://console.clever-cloud.com> (ou connectez-vous).
2. Dans un terminal :

```bash
clever login          # ouvre le navigateur
clever profile        # votre compte
git clone https://github.com/CleverCloud/workshop-continuer-aventure-2026-10-27.git ~/cc-workshop-src
export LAB=~/cc-workshop-src            # le dossier qui contient lab.md et demos/
ls $LAB/demos
```

> Nouveau terminal ? Relancez la ligne `export LAB=…`.

---

## Partie 1 — Déployer une app Python (25 min)

### 1.1 Récupérer l'app et en faire un repo Git

```bash
cp -r $LAB/demos/1-app-python ~/cc-workshop-<prenom>
cd ~/cc-workshop-<prenom>
git init && git add . && git commit -m "v1"
```

Regardez les fichiers : `app.py` (une petite app Flask), `requirements.txt` (ses dépendances). Pas de Dockerfile, pas de configuration serveur, pas de script de build.

### 1.2 Créer l'application

```bash
clever create --type python --region par app-<prenom>
cat .clever.json
clever status
```

👉 Console : ouvrez l'application et faites le tour — **Information**, **Environment variables**, **Scalability**, **Domain names**, **Logs**, **Metrics**, **Activity**.

*Sans CLI : Console → **Create** → **an application** → depuis votre fork GitHub → Python.*

### 1.3 Dire à la plateforme quoi lancer

Le runtime Python sert une app WSGI. Il doit savoir laquelle : module `app` (le fichier `app.py`), objet `app` (l'instance Flask).

```bash
clever env set CC_PYTHON_MODULE app:app
clever env set CC_PYTHON_VERSION 3.13
clever env set CC_HEALTH_CHECK_PATH /health
clever env
```

### 1.4 Déployer et lire le log de déploiement

```bash
clever deploy
```

Pendant que ça tourne, repérez dans le log :

- [ ] le commit déployé
- [ ] la version de Python choisie
- [ ] l'installation des dépendances depuis `requirements.txt`
- [ ] le cache de build
- [ ] la vérification que quelque chose écoute sur le port 8080
- [ ] le succès du déploiement

*Console : **Logs** (pendant le déploiement) ou **Activity** → le déploiement → ses logs.*

### 1.5 Tester et observer

```bash
clever domain                    # le domaine de l'app
curl https://<domaine-de-votre-app>/
clever open                      # ouvre l'app dans le navigateur
clever activity                  # historique des déploiements
clever logs --since 10m          # logs de l'application (Ctrl+C pour arrêter)
clever accesslogs --since 10m    # logs d'accès HTTP
```

### 1.6 Une nouvelle version, sans coupure

Dans un **deuxième terminal**, interrogez l'app chaque seconde :

```bash
while true; do curl -s https://<domaine-de-votre-app>/ | grep -o '"version":"[^"]*"'; sleep 1; done
```

Dans `app.py`, passez `VERSION = "v1"` à `"v1.1"`, puis :

```bash
git commit -am "v1.1"
clever deploy
```

La boucle échoue-t-elle à un moment ? Quand la version change-t-elle ? Pourquoi ?

---

## Partie 2 — Add-ons (15 min)

### 2.1 Le catalogue

```bash
clever addon providers
clever addon providers show postgresql-addon      # plans et zones
```

👉 Console : **Create** → **an add-on** : parcourez le catalogue.

### 2.2 Avant le lien

```bash
curl https://<domaine-de-votre-app>/db
```

Que répond l'app ? Pourquoi ?

### 2.3 Créer et lier une base PostgreSQL

```bash
clever addon create postgresql-addon pg-<prenom> --plan dev --region par
clever service link-addon pg-<prenom>
```

*Console : créez l'add-on, puis dans l'app → **Service dependencies** → liez-le.*

### 2.4 Qu'est-ce que le lien a changé ?

```bash
clever addon list
clever addon env <addon-id>          # les variables de l'add-on
curl https://<domaine-de-votre-app>/db    # toujours une erreur ?
```

Les variables de l'add-on (`POSTGRESQL_ADDON_HOST`, `…_USER`, `…_PASSWORD`…) sont **injectées dans l'environnement de l'application à son démarrage**. Une instance déjà lancée ne les voit pas.

```bash
clever restart
curl https://<domaine-de-votre-app>/db    # appelez-la deux ou trois fois
```

👉 Console : ouvrez l'add-on — informations de connexion, **Backups**, **Metrics**, et le tableau des plans (gardez-le en tête pour la Partie 3).

---

## Partie 3 — Quand ça casse (20 min)

Chaque scénario est une **nouvelle version de votre app** envoyée par « un collègue » : vous copiez ses fichiers sur votre app, vous committez, vous déployez… et le problème arrive. Partez toujours **du symptôme et des logs**, pas du diff : dans la vraie vie, on a rarement le diff.

### 3.1 « Ma nouvelle version n'est pas en ligne »

> *« J'ai poussé la v2 il y a une heure et l'app affiche toujours la v1 ! La plateforme est en panne ? »*

```bash
cd ~/cc-workshop-<prenom>
cp -R $LAB/demos/2-build-echoue/files/. .
git add -A && git commit -m "v2"
clever deploy
```

1. La plateforme est-elle en panne ? L'app est-elle en panne ? Que répond `curl https://<domaine-de-votre-app>/` ?
2. Où est l'explication ? (`clever activity`, le log du déploiement dans la Console)
3. Pourquoi l'app répond-elle encore ?
4. Corrigez et redéployez.

### 3.2 « Ça marche, puis ça plante »

> *« Depuis la mise en prod de ce matin, `/db` marche quelques fois, puis ne renvoie que des erreurs. Un redémarrage règle le problème… pendant une minute. La base est cassée ? »*

```bash
cp -R $LAB/demos/3-connexions/files/. .
git add -A && git commit -m "v3"
clever deploy
for i in $(seq 1 10); do curl -s -o /dev/null -w "%{http_code}\n" https://<domaine-de-votre-app>/db; done
```

1. Le déploiement a-t-il réussi ? Le log de déploiement aide-t-il cette fois ?
2. Où est l'erreur ? (`clever logs --since 10m`, les logs dans la Console)
3. Que dit exactement l'erreur, **jusqu'au bout** ? Qui parle : l'app ou la base ?
4. Quel est le plan de l'add-on, et quelles sont ses limites ?
5. Pourquoi un redémarrage « répare » pendant une minute ?
6. Quels correctifs possibles, côté app et côté add-on ? Lequel recommanderiez-vous ?

---

## Partie 4 — Une app moderne : Django + uv (démo, 10 min)

L'intervenant déploie l'[exemple Django todo-list](https://github.com/CleverCloud/django-todo-list-example) (uv + PostgreSQL ; copie dans `demos/4-django-uv/`). Regardez et répondez :

1. Quel fichier dit à la plateforme d'utiliser **uv** plutôt que le mode classique ? Quelle variable d'environnement est aussi nécessaire ?
2. `CC_PYTHON_MODULE` n'est pas défini. Pourquoi n'est-il pas nécessaire ici ?
3. D'où viennent les identifiants de la base ? Comparez avec la Partie 2.
4. Les migrations tournent dans `CC_PRE_RUN_HOOK`. Que peut-il se passer avec 3 instances ?
5. « Mon app uv se déploie mais répond *Bad Request (400)* » : que vérifiez-vous ?

Pour la refaire chez vous, suivez le `README.md` de `demos/4-django-uv/`.

---

## Partie 5 — Aller plus loin (démo, 10 min)

| Sujet | Où | Doc |
|---|---|---|
| Taille et nombre d'instances, auto-scaling | `clever scale --flavor S --instances 2` · Console → **Scalability** | [Scalabilité](https://www.clever.cloud/developers/doc/administrate/scalability/) |
| Votre propre domaine, TLS automatique | `clever domain add <domaine>` · Console → **Domain names** | [Domaines](https://www.clever.cloud/developers/doc/administrate/domain-names/) |
| Autres langages | Node.js, Java, PHP, Go, Rust, Ruby, .NET, Docker… | [Applications](https://www.clever.cloud/developers/doc/deploy/applications/) |
| Kubernetes managé (CKE, bêta) | `clever features enable k8s` · `clever k8s create …` | [CKE](https://www.clever.cloud/developers/doc/deploy/kubernetes/) |

---

## Partie 6 — Nettoyer (2 min)

Pour ne pas consommer vos crédits avec les apps du workshop :

```bash
cd ~/cc-workshop-<prenom>
clever service unlink-addon pg-<prenom>
clever addon delete pg-<prenom>
clever delete
```

---

## Aide-mémoire

| Je veux… | Commande | Console |
|---|---|---|
| créer une app | `clever create --type python <nom>` | Create → an application |
| relier un dossier à une app existante | `clever link <app-id\|nom>` | — |
| déployer | `clever deploy` | — |
| état / historique | `clever status` / `clever activity` | Overview / Activity |
| logs / logs d'accès | `clever logs [--since 1h] [--search txt]` / `clever accesslogs` | Logs |
| variables | `clever env`, `clever env set K V`, `clever env rm K` | Environment variables |
| redémarrer / rebuild | `clever restart [--without-cache]` | Overview |
| scaler | `clever scale --flavor S --instances 2` | Scalability |
| catalogue d'add-ons | `clever addon providers [show <provider>]` | Create → an add-on |
| créer / lier un add-on | `clever addon create …` / `clever service link-addon …` | Service dependencies |
| variables d'un add-on | `clever addon env <addon-id>` | Add-on → Information |
| infos pour le support | `clever diag` | — |

Doc : <https://www.clever.cloud/developers/doc/> · CLI : <https://www.clever.cloud/developers/doc/cli-reference/>
