# Scénario 3.2 — « Ça marche, puis ça plante »

> *« Depuis la mise en prod de ce matin, `/db` marche quelques fois, puis ne renvoie que des erreurs. Un redémarrage règle le problème… pendant une minute. La base est cassée ? »*

```bash
cd ~/cc-workshop-<prenom>
cp -R $LAB/demos/3-connexions/files/. .
git add -A && git commit -m "v3"
clever deploy
for i in $(seq 1 10); do curl -s -o /dev/null -w "%{http_code}\n" https://<domaine-de-votre-app>/db; done
```

Questions dans [`../../lab.md`](../../lab.md), Partie 3.2.
