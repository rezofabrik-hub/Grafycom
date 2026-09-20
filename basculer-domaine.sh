#!/bin/sh
# Bascule le site de l'adresse GitHub Pages vers un vrai nom de domaine.
#
#   ./basculer-domaine.sh www.grafycom.fr
#
# À lancer le jour où le domaine est acheté, depuis la racine du dépôt.
# Ensuite : git add -A && git commit && git push, puis renseigner le domaine
# dans Settings > Pages sur GitHub, et faire pointer le DNS
# (enregistrement CNAME de « www » vers rezofabrik-hub.github.io).

set -e

if [ -z "$1" ]; then
  echo "Usage : $0 www.example.fr" >&2
  exit 1
fi
DOMAINE="$1"
ANCIEN="rezofabrik-hub.github.io/Grafycom"

echo "Bascule de $ANCIEN vers $DOMAINE"

# 1. Toutes les URL du site : canoniques, og:url, sitemap, robots, README
grep -rl "$ANCIEN" . --include='*.html' --include='*.xml' --include='*.txt' --include='*.md' \
  | xargs sed -i "s#$ANCIEN#$DOMAINE#g"

# 2. La page 404 utilise des chemins absolus préfixés par le nom du dépôt.
#    À la racine d'un domaine, ce préfixe disparaît.
sed -i 's#"/Grafycom/#"/#g' 404.html

# 3. GitHub Pages lit ce fichier pour servir le domaine personnalisé.
echo "$DOMAINE" > CNAME

echo
echo "Fait. Vérifications :"
echo "  - occurrences restantes de l'ancienne adresse : $(grep -rl "$ANCIEN" . --include='*.html' --include='*.xml' --include='*.txt' 2>/dev/null | wc -l)"
echo "  - CNAME : $(cat CNAME)"
echo
echo "Reste à faire, hors de ce script :"
echo "  1. git add -A && git commit -m 'Bascule sur $DOMAINE' && git push"
echo "  2. GitHub > Settings > Pages > Custom domain : $DOMAINE"
echo "  3. Chez le bureau d'enregistrement : CNAME 'www' -> rezofabrik-hub.github.io"
echo "  4. Une fois le certificat émis, cocher « Enforce HTTPS »"
