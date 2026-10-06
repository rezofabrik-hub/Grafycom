#!/usr/bin/env bash
# Ouvre le site au public : la page d'accueil reprend sa place à la racine
# et les moteurs sont autorisés à indexer.
#
#   ./ouvrir-le-site.sh
#   git add -A && git commit -m "Ouverture du site" && git push
#
# Ce script ne bricole pas le HTML : il bascule l'interrupteur dans les
# générateurs et reconstruit les pages. C'est la seule façon de garantir
# que le site livré est bien celui que les générateurs décrivent — une
# version précédente modifiait le HTML au sed, et les générateurs se
# retrouvaient à décrire un site qui n'existait plus.
set -euo pipefail
cd "$(dirname "$0")"

GEN=generateurs

if [ ! -f "$GEN/gen.py" ]; then
  echo "ERREUR : $GEN/gen.py introuvable." >&2
  exit 1
fi

if grep -q '^CONSTRUCTION = False' "$GEN/gen.py"; then
  echo "Le site est déjà ouvert (CONSTRUCTION = False)." >&2
  exit 1
fi

echo "Ouverture du site au public."
echo

# 1. L'interrupteur. Tout en découle : robots, navigation, nom du fichier
#    d'accueil, lien du logo.
sed -i 's/^CONSTRUCTION = True$/CONSTRUCTION = False/' "$GEN/gen.py"
grep -q '^CONSTRUCTION = False' "$GEN/gen.py" || { echo "bascule ratée" >&2; exit 1; }

# 2. Reconstruction de toutes les pages. p_construction.py est volontairement
#    absent : la page de chantier n'a plus lieu d'être, et index.html est
#    désormais produit par p_index.py.
# p_locales.py n'est qu'un gabarit : ce sont villes.py à villes6.py qui
# produisent les douze pages locales, deux par fichier.
for p in p_index p_prestations p_methode p_apropos p_contact p_merci \
         p_legal p_cgv p_realisations p_cibles p_blog zone \
         villes villes2 villes3 villes4 villes5 villes6; do
  ( cd "$GEN" && python3 "$p.py" >/dev/null )
done
echo "Pages reconstruites."

# 3. accueil.html n'existe plus : son contenu est à la racine.
rm -f accueil.html

# 4. Les moteurs peuvent entrer.
cat > robots.txt <<'ROBOTS'
User-agent: *
Allow: /
Disallow: /merci.html

Sitemap: https://grafycom.fr/sitemap.xml
ROBOTS

# 5. Vérifications. Mieux vaut échouer ici qu'en ligne.
erreurs=0

# dist/ est la sortie du build precedent, encore en mode chantier a cet
# instant : build.sh la reconstruit plus bas. L'inclure dans la verification
# faisait echouer l'ouverture sur toute machine ou build.sh avait deja tourne.
restant=$(grep -rl 'noindex, nofollow' . --include='*.html' --exclude-dir=dist 2>/dev/null \
          | grep -v -E 'merci\.html' || true)
if [ -n "$restant" ]; then
  echo "ERREUR : pages encore en noindex :" >&2; echo "$restant" >&2; erreurs=1
fi

liens=$(grep -rl 'href="accueil\.html"' . --include='*.html' --exclude-dir=dist 2>/dev/null || true)
if [ -n "$liens" ]; then
  echo "ERREUR : liens vers accueil.html :" >&2; echo "$liens" >&2; erreurs=1
fi

[ -f index.html ] || { echo "ERREUR : index.html manquant." >&2; erreurs=1; }
if ! grep -q 'Infographiste' index.html 2>/dev/null; then
  echo "ERREUR : index.html ne ressemble pas à la page d'accueil." >&2; erreurs=1
fi
[ -f accueil.html ] && { echo "ERREUR : accueil.html subsiste." >&2; erreurs=1; }

bash build.sh >/dev/null || { echo "ERREUR : build.sh échoue." >&2; erreurs=1; }

if [ "$erreurs" -ne 0 ]; then
  echo >&2
  echo "Ouverture incomplète. Rien n'est publié : corrigez avant de pousser." >&2
  exit 1
fi

echo
echo "Site ouvert. Vérifié : aucune page en noindex, aucun lien orphelin,"
echo "index.html en place, construction du site réussie."
echo
echo "Reste à faire, dans cet ordre :"
echo "  1. git add -A && git commit -m 'Ouverture du site' && git push"
echo "  2. python3 outils/indexnow.py       (Bing, Yandex, Qwant, Ecosia)"
echo "  3. soumettre sitemap.xml dans la Search Console, puis demander"
echo "     l'indexation des six pages listées dans outils/SEARCH-CONSOLE.md"
