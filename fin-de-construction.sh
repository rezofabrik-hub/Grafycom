#!/bin/sh
# Ouvre le site au public : retire la page de chantier et rend les pages
# indexables. À lancer depuis la racine du dépôt quand tout est prêt.
#
#   ./fin-de-construction.sh
#   git add -A && git commit -m "Ouverture du site" && git push

set -e

GEN="Le dossier des générateurs n'est pas dans le dépôt : régénérez les pages
avec CONSTRUCTION = False dans gen.py, ou appliquez les changements à la main."

echo "Ouverture du site au public"

# 1. La page d'accueil reprend sa place à la racine.
if [ ! -f accueil.html ]; then
  echo "accueil.html introuvable — le site est peut-être déjà ouvert." >&2
  exit 1
fi
mv accueil.html index.html

# 2. Les liens internes repointent vers index.html.
grep -rl 'accueil\.html' . --include='*.html' \
  | xargs sed -i 's#href="accueil\.html"#href="index.html"#g'

# 3. Le lien d'aperçu du pied de la page de chantier n'a plus lieu d'être.
sed -i '/Aperçu du site en préparation/d' index.html 2>/dev/null || true

# 4. Les pages redeviennent indexables.
grep -rl 'content="noindex, nofollow"' . --include='*.html' \
  | xargs sed -i 's#content="noindex, nofollow"#content="index, follow"#g'

# 5. robots.txt rouvre le site aux moteurs.
cat > robots.txt <<'ROBOTS'
User-agent: *
Allow: /
Disallow: /mentions-legales.html
Disallow: /confidentialite.html

Sitemap: https://www.grafycom.fr/sitemap.xml
ROBOTS

echo
echo "Fait. Vérifications :"
echo "  - pages en noindex restantes : $(grep -rl 'noindex, nofollow' . --include='*.html' 2>/dev/null | wc -l)"
echo "  - liens vers accueil.html restants : $(grep -rl 'href=\"accueil.html\"' . --include='*.html' 2>/dev/null | wc -l)"
echo
echo "$GEN"
echo
echo "Puis : git add -A && git commit -m 'Ouverture du site' && git push"
echo "Et : soumettre le sitemap dans Google Search Console."
