# Les générateurs du site

**Les pages HTML à la racine du dépôt sont produites par ces scripts. Elles
ne se modifient pas à la main** : la prochaine régénération écraserait la
correction sans prévenir.

Ces fichiers ont vécu plusieurs semaines dans un dossier temporaire, hors
du dépôt. Un site entier dont la source n'existait que dans `/tmp`, c'est
une perte à un redémarrage près. Ils sont ici désormais.

## Comment ça s'articule

`gen.py` porte tout ce qui est commun : l'en-tête HTML, la navigation, le
pied de page, les coordonnées, l'adresse du site, et la fonction `page()`
qui assemble et écrit un fichier.

Trois constantes de réglage en haut de `gen.py` :

| Constante | Effet |
|---|---|
| `CONSTRUCTION` | `True` : toutes les pages en `noindex`, l'accueil vit dans `accueil.html` et la racine sert la page de chantier. `False` : le site est ouvert, l'accueil est `index.html`. |
| `FORMULAIRE_ACTIF` | `False` : le formulaire de contact ouvre le logiciel de messagerie. `True` : il poste vers `/api/contact`, ce qui suppose que Cloudflare sert le site. |
| `GOOGLE_VERIF` | Jeton de validation de la Search Console. Vide : aucune balise. Rempli : la balise `google-site-verification` part sur toutes les pages. Voir `../outils/SEARCH-CONSOLE.md`. |

Ne pas basculer `CONSTRUCTION` à la main : `../ouvrir-le-site.sh` s'en
charge, régénère tout et vérifie le résultat avant de laisser publier.

Un script par page, sauf trois cas :

- `p_locales.py` n'est qu'un gabarit. Les douze pages de communes sont
  déclarées dans `villes.py` à `villes6.py`, deux par fichier.
- `p_cibles.py` produit les quatre pages « par situation » d'un seul coup.
  Il a été oublié dans les listes de régénération pendant un temps, et les
  quatre pages seraient restées en `noindex` le jour de l'ouverture.
- `p_blog.py` est le seul générateur qui ne contient pas son texte. Les
  articles vivent en Markdown dans `reseaux/blog/`, un fichier par
  article avec un en-tête de métadonnées ; le script les lit, les
  convertit, produit `blog.html` et une page par article, puis met à jour
  le bloc du blog dans `sitemap.xml` entre ses deux marqueurs. Ajouter un
  article, c'est déposer un `.md` et relancer le script — rien d'autre,
  et surtout pas d'édition manuelle du sitemap, qu'on oublierait.
- `pays.py` produit les trois pages de pays de montagne — Cerdagne,
  Capcir, Conflent. Des pays et non des communes : la haute montagne
  compte des dizaines de villages de quelques centaines d'habitants, et
  une page par village serait exactement la page satellite que la règle
  de `p_locales.py` cherche à éviter.
- `p_construction.py` produit la page d'attente. Il n'est pas rejoué à
  l'ouverture, et pour cause.

`404.html` n'est pas généré : il est autonome, avec des chemins absolus,
parce qu'il doit s'afficher correctement depuis n'importe quelle adresse.

## Tout régénérer

```bash
cd generateurs
for f in p_index p_prestations p_methode p_apropos p_contact p_merci \
         p_legal p_cgv p_realisations p_cibles p_blog zone pays villes villes2 villes3 \
         villes4 villes5 villes6; do python3 $f.py; done
python3 p_construction.py        # seulement si CONSTRUCTION = True
```

Puis `git diff` : si le site n'a pas changé, le diff est vide. C'est le
test qui prouve que les générateurs décrivent bien le site livré, et il
vaut la peine d'être lancé après toute modification.

## Une règle apprise à la dure

`p_cgv.py` prenait autrefois la date d'entrée en vigueur des conditions
sur l'horloge du jour. Chaque reconstruction du site annonçait donc de
nouvelles conditions générales alors que pas une ligne n'avait bougé. La
date est maintenant écrite en dur, et ne change que lorsque les conditions
changent.

Un document contractuel ne change pas de date parce qu'on a reconstruit
une page.
