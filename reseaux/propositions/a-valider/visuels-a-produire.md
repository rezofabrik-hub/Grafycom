# Visuels à produire — du 9 novembre au 5 décembre 2026

Ce que `reseaux/visuels.py` doit dessiner, et ce qui demande une vraie
photo (voir `photos-a-prendre.md`).

> **L'outil est `visuels.py`, pas Canva.** Le cahier des charges disait
> l'inverse jusqu'au 12 octobre ; la correction est expliquée dans
> `arbitrages.md`. `visuels.py` dessine avec Pillow et la police Inter du
> site : accents français garantis par la police, format imposé en dur,
> pseudo `@grafycom.graphiste` en constante du code. Les trois défauts
> mesurés de Canva — format qui part en 9:16, point du pseudo avalé,
> polices sans accents — ne peuvent pas s'y produire.
>
> ```bash
> python3 reseaux/visuels.py --liste    # les gabarits existants
> ```
>
> **À jour au 24 octobre : 28 publications, 160 planches.** Tout le
> cycle du 26 octobre au 5 décembre est produit, les 41 écrans de
> stories compris.
> Les huit publications qui attendaient une photographie ont été
> redessinées — voir `photos-a-prendre.md`, section « Les photos
> spécifiques au mois ». Les récapitulatifs ci-dessous décrivent donc ce
> qui **a été** produit, et non ce qui reste à faire ; les deux lignes
> les lignes « Photos » et « Tournages » ne valent plus du tout : **les six
> reels du cycle sont dessinés**, et plus aucune publication n'attend
> d'image.

> **Les dossiers de `reseaux/visuels/` portent désormais la vraie date de
> publication.** Ils étaient restés aux dates d'avant le décalage du
> calendrier au 26 octobre : le carrousel du lundi 19 était rangé dans
> `2026-10-12-couleurs`, le reel du 27 novembre dans `2026-11-20-…`. Les
> vingt-cinq dossiers sont renommés, et chaque gabarit porte maintenant
> son numéro de publication dans son commentaire.

---

## L'état mesuré au 24 octobre

Ce tableau n'est pas saisi à la main : les quatre premières lignes sont
ce que `python3 reseaux/audit.py` relève à chaque passage, en comptant
les fichiers.

| Ce qui est produit | Compte |
|---|---|
| Publications, toutes avec leur dossier de planches | **28** |
| Planches de publication | **160** |
| Écrans de story | **41** |
| Illustrations d'articles | **24** — trois par article |
| Reels montés, chronos et voix off compris | **6** |

**Rien de ce que `visuels.py` sait dessiner n'attend d'être dessiné.**
Les trois gabarits absents de la liste — `emballage-tri`, 
`francais-devanture`, `sticker-enseigne` — ne manquent pas : ils sont
mis en commentaire avec leur raison, parce que les publications n° 14,
18 et 22 sont sorties du calendrier faute de vérification
réglementaire. Les rétablir, c'est décommenter trois clés.

## Ce qui reste, et qui ne se dessine pas

Deux choses, et aucune des deux n'est un dessin.

**1. Quatre images réalistes** — G, I, J, K du brief
`BRIEF-PHOTOS-IA.md`, § 5, priorité moyenne. Elles gagnent du réalisme
sur quatre planches qui fonctionnent déjà sans. Tenté de les générer
d'ici le 24 octobre : refusé deux fois, la résolution 2K n'étant pas
ouverte par la formule en cours, puis les crédits étant épuisés. Les
quatre prompts sont écrits mot pour mot dans le brief, prêts à coller
dans n'importe quel moteur.

**2. Les photographies.** Elles ne s'inventent pas, et une photo
inventée sur le compte d'une graphiste se retourne contre elle.

| Où | Combien | La liste |
|---|---|---|
| Le cycle social | **0** | `photos-a-prendre.md` — les douze publications concernées ont été redessinées |
| Les articles du blog | **4** | `python3 reseaux/illustrations.py --photos` |

Les quatre du blog : une devanture réelle du centre ancien, un bon à
tirer posé à côté de l'écran qui affiche le même visuel, un nuancier
Pantone ouvert en lumière du jour, un jeu de fichiers sources ouvert
avec ses calques. Les schémas tiennent la place en attendant, et ils
la tiennent honnêtement : ils n'ont jamais prétendu être des preuves.

---

## Ce que disaient les quinzaines — conservé, et périmé

> Les deux récapitulatifs qui suivaient ici annonçaient du travail à
> faire qui a été fait depuis, et des compteurs qui ont bougé trois
> fois. Ils sont retirés plutôt que corrigés : un document qui dit
> « à produire » et qui liste du produit se relit de travers, et
> `arbitrages.md` garde déjà la trace de ce qui a changé et quand.
>
> Ce qui les remplace est au-dessus, et il est mesuré.
