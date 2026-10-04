#!/usr/bin/env bash
# Construit dist/ : le site public, et rien d'autre.
#
# Cloudflare Pages publie le contenu du dossier de sortie. Comme le depot
# contient aussi des fichiers de travail (documentation, scripts, outils),
# on ne deploie pas la racine telle quelle.
#
# Le principe est volontairement inverse d'une liste blanche : on recopie
# tout, puis on retire ce qui n'a rien a faire en ligne. Une liste blanche
# finit toujours par oublier un fichier public ; ici, un nouveau fichier
# public part tout seul, et un nouveau fichier interne est arrete par le
# garde-fou en fin de script.
#
# Reglages Cloudflare Pages correspondants :
#   Build command      : bash build.sh
#   Build output       : dist
set -euo pipefail
cd "$(dirname "$0")"

rm -rf dist
mkdir -p dist

tar --exclude=./.git --exclude=./dist -cf - . | tar -xf - -C dist

# Outils, sources et automatisations : pas du site.
rm -rf dist/.github

# Le code du Worker n'est pas un fichier statique : il ne doit pas etre servi.
rm -rf dist/src

# Les outils internes et, surtout, les listes de prospects qu'ils produisent :
# des noms et des adresses de personnes physiques. Jamais en ligne.
rm -rf dist/outils

# Calendriers editoriaux et ligne editoriale : documents de travail.
rm -rf dist/reseaux

# Les generateurs du site. Leurs .py sont deja retires plus bas, mais pas
# communes66.json : le garde-fou le laisse passer, .json etant une
# extension legitime pour un site. Une liste blanche d'extensions ne
# remplace pas l'exclusion d'un dossier entier.
rm -rf dist/generateurs

# Artefacts propres a GitHub Pages, inutiles chez Cloudflare.
rm -f dist/CNAME dist/.nojekyll dist/.gitignore dist/wrangler.toml

# Documentation, scripts, pages enregistrees : jamais en ligne.
find dist \( -name '*.md' -o -name '*.sh' -o -name '*.py' -o -name '*.mhtml' -o -name '*.toml' \) -delete
find dist -type d \( -name '_*' -o -name '__pycache__' \) -prune -exec rm -rf {} +

# Garde-fou. Il ne repete pas la liste noire ci-dessus : il verifie
# l'inverse. Tout ce qui part en ligne doit porter une extension connue
# d'un site statique, ou etre un fichier de configuration attendu. Une
# liste noire oublie toujours un cas — elle a deja laisse passer des
# fichiers .csv de prospection. Une liste blanche de verification, elle,
# refuse ce qu'elle ne connait pas, et c'est exactement ce qu'on veut
# d'un dernier controle.
autorises='html|css|js|mjs|json|webmanifest|xml|txt|svg|ico|png|jpg|jpeg|webp|avif|gif|woff2|woff|ttf|eot|pdf|map'
attendus='_headers|_redirects|_routes.json|.nojekyll'

inconnus=$(find dist -type f -printf '%P\n' | while read -r f; do
  base=${f##*/}
  if printf '%s\n' "$attendus" | tr '|' '\n' | grep -qxF "$base"; then
    continue
  fi
  ext=${base##*.}
  if [ "$ext" = "$base" ] || ! printf '%s\n' "$autorises" | tr '|' '\n' | grep -qxF "$ext"; then
    echo "$f"
  fi
done)

if [ -n "$inconnus" ]; then
  echo "ERREUR : fichier non publiable dans dist/, publication annulee." >&2
  echo "Ajoutez son extension a la liste si elle est legitime :" >&2
  echo "$inconnus" >&2
  exit 1
fi

echo "dist/ construit : $(find dist -type f | wc -l | tr -d ' ') fichiers."
