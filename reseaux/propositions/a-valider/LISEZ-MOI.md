# À valider — du 26 octobre au 5 décembre 2026

Tout ce qui est écrit et pas encore publié, classé par canal.

| Document | Ce qu'il contient |
|---|---|
| **`PRET-A-VALIDER.md`** | **ce qui est terminé et ce qui ne l'est pas** — à lire en premier |
| **`calendrier.md`** | les 101 éléments datés, tous canaux, dans l'ordre |
| **`instagram-facebook.md`** | les 27 publications |
| **`fiche-google.md`** | les 23 textes de fiche |
| **`stories.md`** | les 6 séquences hebdomadaires, 40 écrans |
| **`blog.md`** | l'index des 7 articles — les textes sont dans `reseaux/blog/` |
| **`messages-prives.md`** | le message d'accueil et 4 réponses types |
| **`photos-a-prendre.md`** | **plus rien à photographier** — la réserve de prises de vue, et pourquoi les douze publications concernées sont dessinées |
| **`visuels-a-produire.md`** | le récapitulatif de ce qui a été produit |
| **`acquisition.md`** | **l'objectif : des abonnés, puis des clients** — ce que le plan fait pour ça, mesuré |
| **`checklist-enseigne.md`** | le document à **donner** en message privé — quatre pages, à relire avant usage |
| **`arbitrages.md`** | **ce qui demande ta décision** — à lire en premier |

## Dans quel ordre les traiter

L'ordre n'est pas indifférent, et ce n'est pas celui du tableau
ci-dessus. **Une décision prise en haut de cette liste déplace ce qui
est en dessous** : refuser une publication, c'est aussi refaire son
texte de fiche, sa story, sa ligne de calendrier et quatre compteurs.
Lire le calendrier en premier, c'est relire une conséquence avant sa
cause.

**D'abord ce qui peut encore bouger** — 15 minutes, et ça conditionne
tout le reste.

1. **`arbitrages.md`** — ce qui attend encore ta décision. Tout ce qui
   s'y tranche change des documents plus bas. *(Ce fichier date du
   12 octobre : là où il parle de visuels restant à dessiner, c'est
   périmé — ils le sont tous.)*
2. **`PRET-A-VALIDER.md`** — l'état exact, et surtout les **deux
   réserves réglementaires** encore ouvertes, n° 14 et n° 22. Une
   troisième, la n° 18, a déjà fait sortir sa publication du
   calendrier : c'est ce qui arrive quand la réserve n'est pas levée.

**Ensuite la substance, de la plus lourde à la plus légère.** C'est là
que se passe la vraie validation, et c'est le gros du temps.

3. **`instagram-facebook.md`** — le document le plus long de loin, et
   celui dont tout le reste dérive. Rien n'est encore publié :
   **27 publications attendent ton accord**.
4. **`fiche-google.md`** — 23 textes, un par publication, **avec ses
   cases à cocher**. Si une publication change au point 3, son texte
   change ici.
5. **`stories.md`** — 40 écrans, **avec ses cases à cocher**. Ils
   annoncent les publications : ils bougent avec elles.
6. **`blog.md`** — l'index seul. Les sept textes ne sont pas dans les
   PDF : ils s'ouvrent dans `reseaux/blog/`, et se valident en y
   écrivant `statut: validé`.

**Puis ce qui ne se valide pas, mais se vérifie** — une relecture de
cohérence, rapide, une fois que les décisions sont prises.

7. **`calendrier.md`** — l'ensemble d'un coup d'œil, et la somme de
   tout ce qui précède.
8. **`A-FOURNIR.md`** — ce qui manque encore de ton côté.

**Enfin les annexes**, qui ne bloquent rien et se lisent quand tu veux :
`photos-a-prendre`, `visuels-a-produire`, `acquisition`,
`messages-prives`, `checklist-enseigne`, `BRIEF-PHOTOS-IA`.

**Ce qu'on peut sauter.** Les points 7 et 8 sont tenus par
`reseaux/audit.py`, qui relit à chaque passage les quatre tableaux de
dates du dossier et tous les compteurs. S'il ne signale rien, le
calendrier est d'accord avec le reste — inutile de le vérifier à la
main.

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
python3 reseaux/pdf.py            # les quinze
python3 reseaux/pdf.py calendrier  # un seul
```

## Ce qui n'est pas ici

Les textes complets des articles, qui vivent dans `reseaux/blog/`, un
fichier par article. Et les visuels produits, dans `reseaux/visuels/` —
un dossier par publication, nommé à **la date réelle de parution**.

Pour les relire sans ouvrir 210 fichiers un par un :

```bash
python3 reseaux/planche-contact.py          # une page A4 par publication
python3 reseaux/planche-contact.py 2026-11  # un seul mois
```

Et les six reels se montent tout seuls, à partir des écrans et du
découpage écrit — aucune durée n'est recopiée, elles sont lues dans le
cahier des charges :

```bash
python3 reseaux/reels.py --liste
python3 reseaux/reels.py --tout         # six MP4 muets, aux bons chronos
python3 reseaux/reels.py --tout --voix  # avec la voix de synthèse
```
