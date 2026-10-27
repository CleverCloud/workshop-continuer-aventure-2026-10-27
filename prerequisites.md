# Prérequis

**Rien n'est obligatoire pour assister** : vous pouvez regarder la démo et refaire le [lab](lab.md) après, à votre rythme. Pour suivre en même temps que l'intervenant, préparez ceci avant le début (10 minutes).

## Pour suivre en direct

| # | Quoi | Vérifier |
|---|------|----------|
| 1 | Un **compte Clever Cloud** — on le crée ensemble au début si besoin : <https://console.clever-cloud.com> | vous accédez à la Console |
| 2 | **Git**, avec `user.name` et `user.email` configurés | `git --version` · `git config user.email` |
| 3 | **Clever Tools** (le CLI), version récente | `clever version` |
| 4 | Clever Tools **connecté** à votre compte | `clever login` puis `clever profile` |
| 5 | Un terminal, `curl`, un éditeur de code | `curl --version` |
| 6 | Les fichiers des démos : <https://github.com/CleverCloud/workshop-continuer-aventure-2026-10-27> | `git clone https://github.com/CleverCloud/workshop-continuer-aventure-2026-10-27.git` |

Installer Clever Tools : <https://www.clever.cloud/developers/doc/manage/cli/install> — binaires Linux / macOS / Windows, paquets (Homebrew, etc.), ou `npm install -g clever-tools`.

`clever login` ouvre votre navigateur pour vous connecter, puis enregistre le jeton localement.

## Sans CLI ?

C'est possible : la Console permet de créer une application **depuis un repo GitHub** (forkez <https://github.com/CleverCloud/workshop-continuer-aventure-2026-10-27>), de gérer ses variables d'environnement, ses add-ons et de lire les logs. Le lab indique l'équivalent Console à chaque étape. Le CLI reste plus rapide pour suivre en direct.

## Derrière un proxy d'entreprise ?

Exportez `https_proxy` / `http_proxy` dans votre terminal ; Git suit `git config --global http.proxy`. Si un certificat d'entreprise est nécessaire : `NODE_EXTRA_CA_CERTS=/chemin/ca.pem` pour le CLI, `git config --global http.sslCAInfo /chemin/ca.pem` pour Git. Ne désactivez jamais la vérification TLS. Si ça bloque : regardez, et refaites le lab depuis un autre réseau.
