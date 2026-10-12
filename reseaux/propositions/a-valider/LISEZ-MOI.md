# À valider — du 19 octobre au 28 novembre 2026

Tout ce qui est écrit et pas encore publié, classé par canal.

| Document | Ce qu'il contient |
|---|---|
| **`PRET-A-VALIDER.md`** | **ce qui est terminé et ce qui ne l'est pas** — à lire en premier |
| **`calendrier.md`** | les 96 éléments datés, tous canaux, dans l'ordre |
| **`instagram-facebook.md`** | les 24 publications |
| **`fiche-google.md`** | les 24 textes de fiche |
| **`stories.md`** | les 6 séquences hebdomadaires, 41 écrans |
| **`blog.md`** | l'index des 7 articles — les textes sont dans `reseaux/blog/` |
| **`messages-prives.md`** | le message d'accueil et 4 réponses types |
| **`photos-a-prendre.md`** | la liste de prises de vue pour Sandra |
| **`visuels-a-produire.md`** | ce qu'il reste à dessiner |
| **`acquisition.md`** | **l'objectif : des abonnés, puis des clients** — ce que le plan fait pour ça, mesuré |
| **`arbitrages.md`** | **ce qui demande ta décision** — à lire en premier |

## Par où commencer

1. **`PRET-A-VALIDER.md`** : l'état exact. 57 éléments sont complets et
   peuvent partir ; le reste attend un visuel, une photo ou une
   vérification. Trois points y demandent une réponse de ta part.
2. **`arbitrages.md`**, section 1 : la question du rythme. Rien n'est
   publié, 24 publications attendent, et 14 visuels restent à dessiner.
3. **`calendrier.md`** pour voir l'ensemble d'un coup d'œil.
4. Puis canal par canal, dans l'ordre qui t'arrange.

## Comment valider

- **Les publications, stories et textes de fiche** : dis-moi lesquels sont
  bons, ou ce qu'il faut changer. Rien ne part sans ton accord explicite.
- **Les articles de blog** : ouvre le fichier dans `reseaux/blog/`, remplace
  `statut: à relire` par `statut: validé`. L'article paraîtra **à sa date**,
  tout seul — les deux verrous sont indépendants, tu peux donc tout valider
  d'un coup sans que tout sorte le même jour.

## Les PDF

Les mêmes documents, paginés et prêts à annoter, sont fabriqués par
`reseaux/pdf.py` dans `reseaux/pdf/`. Ils ne sont pas versionnés —
ce sont des dérivés, la source reste le markdown.

```bash
python3 reseaux/pdf.py            # les douze
python3 reseaux/pdf.py calendrier  # un seul
```

## Ce qui n'est pas ici

Les textes complets des articles, qui vivent dans `reseaux/blog/`, un
fichier par article. Et les visuels produits, dans `reseaux/visuels/`.
