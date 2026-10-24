# Blog — les articles à valider

Les textes complets sont dans `reseaux/blog/`, un fichier par article.
Ce document est l'index : il dit ce qui existe, à quelle date, et ce qu'il
reste à faire.

## Comment un article paraît

Il y a **deux verrous indépendants**, et c'est voulu.

1. L'en-tête doit porter **`statut: validé`**, le mot en toutes lettres.
   « rédigé », « à relire » ou « prêt » ne suffisent pas : ils décrivent
   l'état du texte, pas ton accord.
2. **La date de l'en-tête doit être arrivée.** Un article du 4 décembre ne
   sort pas le 13, même validé.

Tu peux donc **tout valider d'un coup** sans que tout sorte le même jour.
Chaque article paraîtra à sa date, tout seul.

## Les articles

| Date | Titre | Mots | Images | Statut |
|---|---|---|---|---|
| vendredi 30 octobre | Enseigne de commerce : comment obtenir l'autorisation préalab | 801 | 3 | ✅ validé |
| vendredi 6 novembre | Pourquoi vos couleurs imprimées ne ressemblent jamais à votre | 647 | 3 | ✅ validé |
| jeudi 12 novembre | Habiller sa vitrine : dépoli, microperforé ou lettres découpé | 925 | 3 | ✅ validé |
| vendredi 13 novembre | Qui possède votre logo ? | 687 | 3 | ✅ validé |
| vendredi 20 novembre | Cartes de vœux : il est trop tard pour Noël, et c'est une bon | 1026 | 3 | ✅ validé |
| vendredi 27 novembre | Vitrine de fin d'année : ce qui se lit vraiment depuis le tro | 854 | 3 | ✅ validé |
| vendredi 4 décembre | Faut-il refaire son logo pour la nouvelle année ? Trois quest | 792 | 3 | ✅ validé |
| vendredi 11 décembre | Écouter, c'est déjà dessiner | 996 | 3 | ✅ validé |

**Les huit articles sont validés le 24 octobre.** Il n'y a plus rien à
relire.

> ✅ **Le passage automatique du matin existe depuis le 24 octobre.**
> Ce document et le calendrier l'annonçaient depuis le premier jour, et
> il n'existait pas : le dépôt ne portait qu'un workflow, qui vérifie
> le certificat du domaine. Sans lui, l'article du 30 octobre serait
> resté dans le dépôt.
>
> Il s'appelle `.github/workflows/parution-blog.yml`, il tourne tous
> les matins à **8 h 07**, et il ne fait qu'une chose : relancer
> `generateurs/p_blog.py`, vérifier que les pages produites tiennent
> debout, et pousser si quelque chose a changé. GitHub Pages sert la
> racine du dépôt — pousser, c'est publier.
>
> Il ne lance pas `build.sh` : celui-ci assemble `dist/` à partir des
> fichiers déjà écrits, il n'exécute aucun générateur. C'est une chose
> que j'ai apprise en refaisant les CGV, et elle aurait coûté cher un
> 30 octobre au matin.
>
> **À vérifier une fois, et une seule :** lancer le workflow à la main
> depuis l'onglet Actions, et regarder qu'il finit en vert.

Pour en
valider un : ouvrir son fichier dans `reseaux/blog/`, remplacer la ligne
`statut:` par `statut: validé`, et le pousser. Le reste est automatique.

## Les illustrations — faites le 24 octobre

**Vingt-quatre, trois par article** : une en tête, qui sert aussi de
vignette quand le lien est partagé, et deux posées dans le texte à
l'endroit où l'argument se pose.

Aucune ne décore. Chacune porte un point que l'article développe — les
deux Cerfa côte à côte, le même quadri sur quatre papiers, la bande de
trente centimètres réellement lue d'une vitrine, le même monogramme
réduit à dix-huit pixels puis réagrandi. Elles se fabriquent toutes avec
`python3 reseaux/illustrations.py`, qui ne connaît aucune couleur hors
charte et refuse de démarrer s'il en rencontre une.

**Ce qu'elles ne sont pas : des photographies.** Une devanture réelle, un
imprimé posé à côté de l'écran, un nuancier ouvert — ça se
photographie, c'est le métier de Sandra, et la liste est donnée par
`python3 reseaux/illustrations.py --photos`. Un schéma ne les remplace
pas ; il tient la place en attendant, et il tient honnêtement, parce
qu'il ne prétend pas être une preuve.

## Comment un article est mis en page

Trois marques s'écrivent dans le Markdown, et le site comme le PDF de
relecture les comprennent de la même façon — c'est le même convertisseur,
`generateurs/md_article.py` :

| Marque | Effet |
|---|---|
| `[figure: fichier.png \| légende \| description]` | une image pleine largeur, légendée. Les trois champs sont obligatoires : sans description, l'image n'existe pas pour qui ne voit pas. |
| `[exergue: la phrase]` | une phrase sortie du flux, en gros, entre deux filets |
| `> ⚠️ ...` | un encadré d'avertissement, qui ne se confond plus avec une citation |

Le PDF `reseaux/pdf/articles.pdf` montre le résultat : les sept textes
complets, composés sur deux colonnes, dans l'ordre de parution. C'est là
qu'on relit, pas dans le Markdown.
