# Les photos d'atelier — ce qu'elles montrent, et ce qu'elles valent

**Ce document est versionné ; les photos ne le sont pas.** Le dépôt est
public, et ni les portraits de Sandra ni les fichiers clients n'ont à y
être. Conséquence éprouvée le 22 octobre : le conteneur de travail a été
recyclé et `reseaux/visuels/sources/` est parti avec. Le code était
intact, les images non. Ce fichier existe pour que la prochaine fois on
sache **quoi redemander, et ce qui avait déjà été corrigé**.

## Où elles vont

| Fichier | Publication | Planche |
|---|---|---|
| `01-recadre-4x5.png` | n° 1, pédagogie couleur | 7, clôture |
| `07-recadre-4x5.png` | n° 13, Solaire 66 | 8, clôture |
| `06-recadre-4x5.png` | n° 24, reel bilan | écran 6 |
| `04-recadre-4x5.png` | — | en réserve |

Le registre qui les relie aux gabarits est `PHOTOS` dans `visuels.py`,
et nulle part ailleurs : un chemin recopié dans un gabarit se périme en
silence le jour où le fichier change de nom.

## Les sept, et ce qu'on y a trouvé

Chaque texte a été agrandi avant publication. C'est la règle, et c'est
elle qui a attrapé tout ce qui suit.

| Fichier | Sujet | État |
|---|---|---|
| `01-nuancier-pull-rouge.jpg` | pull rouge, nuancier Pantone | **bon.** Pseudo correct, logo mural fidèle |
| `04-carte-voeux-dorure.jpg` | carte de vœux en main | **la carte ne peut pas être montrée de près** — elle porte « Graautte de voeuwr ». Utilisable en plan large, où elle redevient du décor |
| `06-ecran-solaire66.jpg` | de profil, devant l'écran | **bon.** L'affiche murale « Solaire 66 / Grafycom » est fidèle |
| `07-bureau-solaire66.jpg` | au bureau, Solaire 66 à l'écran | **corrigée** : le vrai logo est incrusté en perspective à l'écran, coins mesurés et inscrits dans `ECRANS`. Le croquis « devanfture » est hors du recadrage 4:5 |
| `03-portrait-nuancier-4x5.jpg` | portrait vertical, nuancier | **à corriger** : le pseudo y est `@grafycom graphiste`, **sans le point**. `retouche_atelier.py` sait le refaire |
| `08-croquis-denim.jpg` | veste en jean, carnet de croquis | reçue en aperçu seulement, pas en fichier |
| `05-profil-ecran-solaire66.jpg` | de profil, écran | perdue avec le conteneur, non renvoyée |

## Ce qui manque encore

- **Plus rien.** Le panneau de chantier est arrivé le 23 octobre —
  2000 × 1337 px, rapport 1,496, soit les 120 × 80 cm annoncés. La n° 13
  est complète, et avec elle tout le cycle.

  Les **cartes recto/verso sont arrivées le 23 octobre**, en vectoriel —
  `CARTES_DE_VISITE.pdf`, deux pages de 89 × 59 mm, soit 85 × 55 mm plus
  2 mm de fond perdu. Rendues à **300 dpi**, ce qui donne 1052 px pour
  89 mm : exactement la constante `MM` du gabarit. Le fond perdu est rogné
  par `poser(rogner_mm=2)`, pas à la main — un rognage manuel se périme
  le jour où le fichier est réexporté.

## Ce que les scripts refont tout seuls

`retouche_atelier.py` n'a pas besoin d'être réécrit, seulement
réalimenté :

- `pseudo()` — remet le point du pseudo sur le liège, par seuil local ;
- `logo_mural()` — projette `assets/img/logo-grafycom.jpg` dans le
  quadrilatère de l'affiche, en perspective, l'encre posée en
  multiplication ;
- `carte_voeux()` — recadre la carte au lieu de la retoucher, et dit
  pourquoi la retouche échoue ;
- `logo_ecran()` — projette le logo d'un client dans le plan de travail
  affiché à l'écran. Les coins y sont **mesurés** par ajustement des
  quatre bords puis intersection, et non estimés : le premier relevé,
  fait à l'œil, avait lu un rectangle là où l'écran est tourné, et le
  logo se posait à plat sur un plan incliné.

## Les logos clients

| Fichier | Client | État |
|---|---|---|
| `sources/solaire-66-logo.png` | Solaire 66 | détouré, les trois monochromes en découlent |
| `sources/clients/big-food.png` | BIG FOOD | **fichier vectoriel reçu** (`LOGO_OK.ai`, PDF 1.6), rendu à 3600 px. **Accord du client donné** le 22 octobre |
| `sources/clients/big-food-2lignes.png` | BIG FOOD, composition deux lignes | **capture d'écran, 356 px** — pas de vectoriel. Posée à sa taille native, jamais agrandie. Le `.ai` reste demandé |
| `sources/clients/krusty.png` | KRUSTY | **fichier vectoriel reçu** (`LOGO.pdf`), rendu à 3593 px, fond transparent. ✅ **Accord client acquis** le 22 octobre |
| `sources/clients/krusty-depliant.png` | KRUSTY, dépliant | mock-up fourni, recadré à 1168 px. Extrait du transcript, faute de dépôt sur le disque |
| `sources/clients/sweet-dream.png` | SWEET DREAM, une ligne | **vectoriel reçu** (`LOGO.pdf`), 3123 px, fond transparent. ✅ **Accord acquis** le 22 octobre |
| `sources/clients/sweet-dream-2lignes.png` | SWEET DREAM, deux lignes | **du même fichier vectoriel**, 1463 px. Contrairement à BIG FOOD, les deux compositions sont dans le même plan de travail |
| `sources/clients/sweet-dream-depliant.png` | SWEET DREAM, dépliant | **mock-up calculé** par `reseaux/mockup.py` à partir des deux faces fournies. Rien de téléchargé, aucun droit à vérifier |

### BIG FOOD — ce que le fichier dit, et ce qu'il ne dit pas

Relevé dans le fichier :

- rapport **4:1** exactement ;
- trois couleurs, mesurées sur l'aplat : violet `#4b165f` (59 % de la
  surface), blanc `#ffffff` (14 %), orange `#f39200` (4 %). Le reste
  est l'illustration des deux burgers ;
- le « B » est le seul caractère orange ; les deux « O » de FOOD sont
  remplacés par des burgers ;
- **un seul plan de travail**, donc une seule composition : la ligne.
  La version deux lignes existe, Sandra l'a envoyée — mais en capture
  d'écran de 356 px, pas dans ce fichier.

Ces trois valeurs sont **les couleurs du client, pas celles de la
charte Grafycom** — elles n'ont donc rien à faire dans `style.css` ni
dans `charte.py`, exactement comme le bleu et le jaune de Solaire 66.

### La composition deux lignes

Reçue le 22 octobre, en capture d'écran : **356 × 222 px**, rapport
1,6:1. Les couleurs sont fidèles — orange et blanc identiques au
vectoriel, violet à une unité près (`#4c1660` au lieu de `#4b165f`,
l'arrondi d'une capture), réaligné à l'enregistrement.

Elle est posée **à 356 px, sa taille native**, et non aux 420 px
prévus. Une planche qui explique qu'un logo doit rester net ne peut
pas montrer une image agrandie : on verrait le défaut dont elle parle.

Elle n'a pas été reconstruite à partir du vectoriel non plus, alors
que les lettres y sont. Dans la deux lignes, le « B » orange est
surdimensionné et chevauche le « F » de la ligne du dessous : c'est un
arbitrage de Sandra, pas une mise en page qu'on redevine. Recomposer,
ce serait redessiner le logo d'un client à sa place.

**Ce qui manque encore :** le `.ai` de cette composition, pour tout
usage au-delà de 356 px.

### SWEET DREAM — et le mock-up calculé

Logo vectoriel reçu le 22 octobre avec le JPEG recto-verso du
dépliant. Accord client acquis.

Relevé dans le fichier : **un seul plan de travail**, qui contient
**les deux compositions** — une ligne et deux lignes. C'est la
différence avec BIG FOOD, dont le `.ai` n'en portait qu'une. Deux
encres seulement : rose clair `#f5a3c7` pour les lettres, magenta
`#ec008b` pour l'ombre décalée. Pas de troisième couleur, pas de
dégradé.

**Le mock-up du dépliant n'a pas été téléchargé.** Il est calculé par
`reseaux/mockup.py`, à partir des deux faces du JPEG : perspective
résolue à la main, ombre portée dérivée de la silhouette transformée,
creux de pli en dégradé. C'est le même principe que partout ailleurs
ici — ce qui peut se calculer ne se télécharge pas, et ce qui ne se
télécharge pas n'a pas de licence à vérifier.

> Le dépliant porte, comme celui de KRUSTY, la mention « Réalisation
> REZOFABRIK » et les coordonnées du client. À l'échelle du mock-up
> les deux sont illisibles. Même arbitrage que pour KRUSTY si la pièce
> est un jour montrée plus grande.

### KRUSTY — reçu, pas utilisable pour l'instant

Logo vectoriel reçu le 22 octobre, avec un dépliant de menu en
visualisation. Relevé dans le fichier : trois couleurs sur fond
transparent — violet `#7b4c9f`, orange `#fcb141`, jaune `#fbce45`,
plus le blanc des lettres. Rapport 1,25:1. Le burger est posé sur le
« Y » et le « K » est la seule lettre orange.

**Accord acquis le 22 octobre.** Le logo a été commandé à Grafycom
par REZOFABRIK, et le client KRUSTY est au courant de la
sous-traitance. La publication n° 26 est écrite, mercredi 18 novembre.

**Le dépliant est de Grafycom lui aussi.** Son fichier d'impression
fait 68 Mo et n'est pas ici — mais il n'a pas eu à l'être. La planche
S4 de la n° 26 **dessine sa grille** : trois volets, la trame
violette, le vrai logo posé dedans, des blocs neutres à la place des
plats. Ce qui démontre le propos, c'est la grille, et une grille se
dessine.

> ⚠️ **Trois points à régler le jour où le dépliant réel serait
> montré.** Un JPEG de 1500 px suffirait ; le fichier d'impression
> n'est pas nécessaire.
>
> **Les photographies de plats sont générées par IA**, Laurent l'a
> dit le 22 octobre. Les droits ne posent donc pas de problème. Le
> reste si : sur un compte dont tout le cycle argumente sur le dessin
> et la netteté, une photo générée affaiblit l'argument plus qu'elle
> ne sert la réalisation. Et pour le restaurant, montrer un plat qui
> ne ressemble pas à celui qu'on sert est un risque commercial — dit
> comme un risque, pas comme une règle de droit, faute de l'avoir
> vérifiée. **Mon avis : ne pas les montrer sur ce compte.**
>
> Le dépliant porte en pied de volet la mention **« Réalisation
> REZOFABRIK »**. Sur une publication signée `@grafycom.graphiste`
> elle se contredit avec la signature. Deux issues honnêtes : la
> retirer **du fichier source**, ou l'assumer d'une ligne de légende
> qui dit la sous-traitance. **Jamais l'effacer sur l'image** :
> maquiller un crédit sur une pièce imprimée est autre chose que
> corriger un fichier.
>
> Il porte aussi le **téléphone, l'adresse et les réseaux du client**.
> Publics, mais sans raison d'être relayés : le cadrage devra les
> exclure.

> ⚠️ **Ce que le fichier NE dit PAS, et que j'avais écrit à tort.**
>
> Le plan de travail mesure 7937 × 1984 points, soit 2 800 × 700 mm.
> J'en avais déduit « c'est une enseigne de 2,80 m », et c'est faux :
> **Sandra n'a fait que le logo.** La taille d'un plan de travail dit
> comment un fichier a été réglé, pas ce qui a été produit, ni ce qui a
> été posé sur une façade.
>
> La règle 3 interdit d'inventer une référence client. Déduire un
> livrable d'une propriété de fichier en est une, et elle est d'autant
> plus dangereuse qu'elle a l'air vérifiée. **Ce qu'un fichier prouve,
> c'est ce qu'il contient — jamais ce qu'on en a fait.**

Les trois versions monochromes du logo Solaire 66 se **déduisent** du
fichier couleur : même forme, une seule encre. Les redessiner serait
l'occasion d'une divergence.
