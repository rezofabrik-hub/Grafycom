#!/bin/sh
# Bascule le site de grafycom.fr vers l'apex grafycom.fr.
#
# POURQUOI
# Le 6 octobre 2026, le site était injoignable. Cause : « grafycom.fr »
# n'a aucun enregistrement DNS, alors que le fichier CNAME demandait à
# GitHub Pages de servir ce nom-là. Résultat : l'apex répondait bien, mais
# renvoyait un 301 vers un nom d'hôte inexistant.
#
#   grafycom.fr      -> 185.199.108-111.153   (GitHub Pages)  resout
#   grafycom.fr  -> rien                                  ne resout pas
#
# L'apex, lui, est correctement configuré. Servir l'apex remet donc le site
# en ligne sans toucher au DNS — donc sans dépendre du webmaster.
#
# APRÈS COUP
# Si le webmaster ajoute un jour « www CNAME rezofabrik-hub.github.io »,
# GitHub redirigera www vers l'apex tout seul. Rien à défaire ici.

set -e
cd "$(dirname "$0")"

ANCIEN="grafycom.fr"
NOUVEAU="grafycom.fr"

echo "Bascule de $ANCIEN vers $NOUVEAU"

# dist/ est reconstruit par build.sh : inutile d'y toucher.
fichiers=$(grep -rl "$ANCIEN" . \
  --include='*.html' --include='*.xml' --include='*.txt' \
  --include='*.md' --include='*.py' --include='*.sh' \
  2>/dev/null | grep -v '^\./dist/' | grep -v '^\./\.git/' || true)

if [ -n "$fichiers" ]; then
  # On remplace « grafycom.fr » par « grafycom.fr ». Le motif est
  # ancré sur le www. : aucune occurrence déjà à l'apex n'est touchée.
  echo "$fichiers" | xargs sed -i "s#$ANCIEN#$NOUVEAU#g"
fi

# GitHub Pages lit ce fichier pour savoir quel domaine servir.
echo "$NOUVEAU" > CNAME

restant=$(grep -rl "$ANCIEN" . --include='*.html' --include='*.xml' \
  --include='*.txt' --include='*.md' 2>/dev/null \
  | grep -v '^\./dist/' | wc -l | tr -d ' ')

echo
echo "CNAME                      : $(cat CNAME)"
echo "fichiers modifies          : $(echo "$fichiers" | grep -c . || echo 0)"
echo "occurrences www restantes  : $restant"
[ "$restant" = "0" ] || { echo "ERREUR : il reste des URL en www" >&2; exit 1; }
echo
echo "Reste a faire :"
echo "  1. git add -A && git commit && git push origin main"
echo "  2. GitHub > Settings > Pages : le domaine suit le fichier CNAME"
echo "  3. attendre le certificat (jusqu'a 1 h), puis cocher Enforce HTTPS"
echo "  4. Search Console : ajouter la propriete grafycom.fr"
