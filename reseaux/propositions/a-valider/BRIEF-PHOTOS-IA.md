# Brief — les visuels réalistes à générer

Pour commander à une IA générative des images qui tiennent dans ce
cycle, et qui le modernisent au lieu de le diluer.

---

## 1. Le diagnostic, d'abord

Les planches actuelles sont **dessinées** : des objets vectoriels posés
sur un aplat crème, avec une ombre de contact, une rampe de lumière à
138° et un grain fin. C'est propre, c'est cohérent, et ça lit
**« illustration éditoriale »** — une esthétique de magazine imprimé.

Ce n'est pas la même chose que *moderne*. Ce qui lit moderne sur
Instagram en 2026, pour un studio de création, c'est :

| Ce qu'on a | Ce qu'il faut |
|---|---|
| objet entier, centré, détouré | **cadrage serré**, le sujet déborde du cadre |
| lumière calculée, douce partout | **lumière directionnelle**, une ombre nette quelque part |
| profondeur simulée par une ombre | **profondeur de champ réelle**, l'arrière-plan décroche |
| surfaces lisses, aplats | **matière** : fibre du papier, morsure de l'encre, grain du béton |
| pas de main | **une main en geste**, souvent coupée au poignet |
| composition symétrique | **décentrée**, de l'air d'un côté |
| couleurs de charte pleines | **neutres désaturés + un seul accent** |

Un détail qui change tout : **l'imperfection**. Un rendu parfait lit
« synthèse ». Une poussière, un reflet mal placé, un bord de papier qui
gondole, c'est ce qui fait croire à l'objet.

---

## 2. La ligne à ne pas franchir

Elle n'est pas négociable, et elle n'interdit presque rien.

### ✅ Ce qui se génère sans problème

Tout ce qui est **décor, matière, ambiance, geste**. Ces images ne
prétendent rien : elles habillent un propos.

- un plan de travail, des outils, du papier, un nuancier
- une main qui tient, plie, pose, découpe
- une texture : kraft, lin, béton ciré, chêne clair, plâtre brut
- une devanture **anonyme**, sans enseigne lisible
- un fond abstrait, un dégradé de lumière sur un mur

### ⛔ Ce qui ne se génère jamais

Tout ce qui **ferait preuve**. Une image qui atteste d'un fait doit être
vraie, sinon elle est un faux.

- une devanture présentée comme un chantier de Grafycom
- un logo inventé présenté comme une réalisation
- un visage présenté comme Sandra
- un imprimé présenté comme sorti de chez son imprimeur
- un plat, un produit, une boutique d'un client réel

> **La règle en une phrase.** Générer le *décor* est permis. Générer la
> *preuve* est un faux. Les quatre réalisations — Solaire 66, BIG FOOD,
> KRUSTY, SWEET DREAM — ne reçoivent **aucune image générée**, jamais :
> ce sont les seules publications dont tout l'intérêt est d'être vraies.

---

## 3. La charte — ce qui ne varie jamais

Quinze images générées séparément ne feront une série que si tout ce
qui suit reste **identique d'une image à l'autre**. Ce n'est pas une
liste d'inspirations : c'est une liste de contraintes. Ce qui n'y
figure pas est interdit.

### 3.1 — Les sept constantes optiques

| Paramètre | Valeur imposée | Pourquoi |
|---|---|---|
| **Focale** | 50 mm équivalent | pas de grand-angle : la déformation trahit la synthèse |
| **Ouverture** | f/2.2 | l'arrière-plan décroche franchement |
| **Mise au point** | premier tiers du cadre | jamais tout net |
| **Source** | une seule, fenêtre | deux ombres divergentes = image de synthèse |
| **Direction** | 45° depuis la gauche caméra | identique partout, c'est ce qui fait la série |
| **Température** | 4800 K, fin d'après-midi | chaud, jamais neutre ni bleuté |
| **Grain** | argentique fin, visible à 100 % | pas de bruit numérique |

### 3.2 — La grille de composition

**C'est la contrainte que personne n'anticipe, et c'est la plus
importante.** Ces images ne sont pas des photos : ce sont des **fonds
sur lesquels on écrit**. Le moteur pose un voile dégradé qui monte du
bas sur 56 à 62 % de la hauteur, puis le titre par-dessus.

Sur un cadre de 1080 × 1350 :

```
  0 ┌─────────────────────────┐
    │                         │
    │   LE SUJET VIT ICI      │   0 → 594 px   (44 %)
    │   net, contrasté        │
594 ├─────────────────────────┤
    │   zone voilée           │   594 → 830    le dégradé monte
830 ├─────────────────────────┤
    │   LE TEXTE S'ÉCRIT ICI  │   830 → 1250   (31 %)
    │   doit être CALME       │
1250└─────────────────────────┘
```

**Deux règles qui en découlent :**

1. **Le sujet tient entièrement dans les 44 % du haut.** S'il descend
   plus bas, le voile le mange.
2. **Le bas du cadre est calme** — une surface, une ombre, un dégradé.
   Aucun détail fin, aucun contraste fort, aucun bord net dans le tiers
   inférieur. Sinon le titre se bat avec l'image, et ça ne se voit
   qu'une fois publié.

Un prompt qui le dit : `subject positioned in the upper third, lower
third is empty surface with soft shadow falloff, clean negative space
at the bottom for text overlay`.

### 3.3 — Le format

| Usage | Cadre | À générer au minimum |
|---|---|---|
| Carrousel | 4:5 — 1080 × 1350 | **2160 × 2700** |
| Reel, story | 9:16 — 1080 × 1920 | **2160 × 3840** |

> **Ce minimum est un confort, pas une barrière** — vérifié le 23
> octobre sur l'image B, que le moteur a rendue en **940 × 1672**, soit
> sa taille native et non une copie réduite. Il manquait 15 %.
>
> Mesuré plutôt que redouté : agrandie en Lanczos à 1080, la zone de
> fibre garde **85 %** de son énergie de contours, et à 100 % sur la
> planche la tranche et la fibre se lisent toujours. Un agrandissement
> de 1,15 sur une **photographie** n'est pas celui de 1,18 sur un
> **logo** — un trait net révèle l'interpolation, une matière
> l'absorbe. Le plafond de 356 px de la deux lignes de BIG FOOD était
> un vrai plafond ; 940 px sur une photo n'en est pas un.
>
> Le minimum reste demandé : il laisse de la marge au recadrage. Mais
> une image en dessous se juge sur la planche, pas sur le principe.

Générer **exactement au bon rapport**. Le moteur recadre en
« couvrir », centré horizontalement : une image 16:9 perdra ses deux
bords, et c'est souvent là qu'est le sujet.

### 3.4 — La palette : neutres imposés, un seul accent

**Les neutres** portent toute l'image. Ce sont ceux de la charte
Grafycom, et ils doivent dominer à au moins 85 % de la surface.

| Nom | Valeur | Rôle dans l'image |
|---|---|---|
| crème | `#f7f1ef` | murs, papier, lumière |
| sable | `#efe4dd` | surfaces claires, plâtre |
| sable foncé | `#e4d5cc` | demi-teintes |
| taupe | `#a2897c` | bois clair, ombres moyennes |
| brun | `#6d5a50` | bois foncé, ombres profondes |
| encre | `#2f2723` | les noirs, jamais du pur noir |

**L'accent** : **un seul par image**, sur **moins de 10 % de la
surface**. Pris dans cette liste, et nulle part ailleurs.

| Nom | Valeur | Quand l'employer |
|---|---|---|
| corail | `#f2585c` | urgence, alerte, erreur à éviter |
| violet | `#a86cd0` | fêtes, fin d'année |
| bleu | `#2f7fc4` | technique, réglementation, administratif |
| orange | `#f5883c` | matière, impression, chaleur |
| turquoise | `#3ec2b3` | nouveauté, vitrine, extérieur |
| jaune | `#f9c33f` | lumière, signalétique |

**Interdits :** le vert végétal, le rouge sang, le bleu ciel saturé, le
rose bonbon, tout métallisé or ou argent. Et **jamais deux accents dans
la même image** — c'est la faute qui fait « banque d'images ».

### 3.5 — Le vocabulaire fermé

Une charte tient parce qu'elle restreint. Ces quatre listes sont
closes : si ce n'est pas dedans, ça n'entre pas dans l'image.

**Surfaces** — chêne clair · plâtre brut · béton ciré gris chaud · lin
froissé · kraft · marbre blanc veiné gris

**Objets autorisés** — papier, carton, échantillons de matière,
nuancier, crayon de bois, stylo noir, règle en acier, cutter, pinceau,
tampon encreur, caractères en plomb, carnet, café noir dans une tasse
blanche unie

**Objets interdits** — écran allumé, ordinateur portable, téléphone,
plante verte, fleurs, lunettes posées, souris, clavier, post-it de
couleur, mug à motif. Ce sont les clichés de la photo de bureau, et ils
datent une image en six mois.

**Humain** — mains et avant-bras seulement, toujours coupés avant le
coude. Peau neutre, aucun bijou, aucun vernis, aucune montre. **Jamais
de visage, jamais de buste, jamais de regard caméra.**

**Lettres — la règle qu'on découvre trop tard.** Le négatif interdit
`text, letters, numbers`, et c'est facile tant que le sujet n'en porte
pas. Mais plusieurs sujets de cette liste en portent par nature : des
caractères en plomb, un tampon encreur, un nuancier annoté. Un moteur à
qui on demande une lettre rend **un glyphe inventé** — empattements qui
ne se referment pas, formes qui n'existent dans aucune fonte. Sur le
compte d'une graphiste, c'est la faute la plus chère possible.

La parade n'est pas de flouter : c'est de **changer l'angle**. Un
caractère en plomb vu de profil est une tige de métal avec un cran et un
épaulement — aucune lettre, et la matière devient le sujet au lieu
d'être un prétexte. Vérifié sur l'image C : à 100 %, les formes qui
ressemblent à des lettres au format vignette sont des profils flous, pas
des glyphes. Rien n'y est transcriptible.

Le prompt le dit en toutes lettres — `seen strictly FROM THE SIDE`,
`every printing face turned away`, `no letterform anywhere in the
frame` — et le négatif ajoute `letterforms, glyphs, typefaces, printed
characters, engraved text, mirror writing, type faces pointing at
camera`.

**Matières — la même règle, un cran plus loin.** Ce n'est pas seulement
la lettre qu'un moteur invente : c'est **toute affirmation technique**.
Un dibond, ce sont deux peaux d'aluminium sur une âme noire en
polyéthylène. Un moteur en rend une approximation, et une approximation
de la structure d'un matériau qu'on vend est aussi fausse qu'un glyphe
qui n'existe pas — avec cette aggravation qu'un client peut la citer.

Donc : **ne jamais nommer une matière dans un prompt.** Demander des
échantillons de feuille quelconques, d'épaisseurs et de finitions
différentes, sans coupe, sans âme visible, sans étiquette. L'image dit
« des supports » ; elle ne dit pas lequel. Le négatif porte
`layered composite core, visible core layer, honeycomb, sandwich panel
cross-section, technical cutaway`.

### 3.6 — Le bloc à copier tel quel

Une seule ligne change d'une image à l'autre : la première.

```
[SUJET ET GESTE — la seule ligne variable]

on [SURFACE de la liste 3.5], shot on 50mm at f/2.2, single warm
window light from camera left at 45 degrees, 4800K late afternoon,
soft shadows with defined edges, shallow depth of field with
background falling off, warm neutral palette of cream #f7f1ef, sand
#efe4dd, taupe #a2897c and brown #6d5a50, exactly one accent of
[COULEUR + HEX] covering less than 10 percent of the frame, fine film
grain, slight natural imperfection, editorial still life photography,
vertical 4:5 framing, subject entirely in the upper third, lower third
is calm empty surface with soft shadow falloff for text overlay

NEGATIVE: faces, people, eyes, text, letters, numbers, logos,
watermarks, brand names, readable signage, symmetry, flat lighting,
pure white background, 3D render, CGI, plastic sheen, oversaturation,
two accent colours, green plants, flowers, screens, laptops, phones,
gold, silver, metallic
```

### 3.7 — Le test de la série

Quand les quinze images sont générées, les poser **en planche
contact**, six par rangée, et regarder de loin en plissant les yeux.

Si la planche lit comme **une seule famille**, la charte a tenu. Si une
image saute aux yeux, c'est qu'elle a un accent de trop, une lumière
qui vient d'ailleurs, ou un fond plus froid. **La régénérer, ne pas la
retoucher** : une correction colorimétrique après coup se voit toujours
à côté des autres.

## 4. Pourquoi l'anglais, et pourquoi le négatif

Les moteurs d'images travaillent mieux en anglais : leurs légendes
d'entraînement le sont. Un prompt français passe, mais il perd en
précision sur les termes optiques — *shallow depth of field* est
compris, « faible profondeur de champ » beaucoup moins.

Le **négatif** du bloc 3.6 compte autant que le positif. Deux entrées y
sont vitales :

- **`text, letters, numbers`** — un texte généré est toujours faux :
  lettres déformées, mots inventés. Sur le compte d'une graphiste, une
  image portant un mot qui n'existe pas est fatale.
- **`logos, brand names`** — un logo généré ressemble toujours à une
  marque existante sans l'être. C'est le plus sûr moyen de se retrouver
  à publier la contrefaçon de quelqu'un.

## 5. La liste de prises, publication par publication

Classée par ce que ça rapporte. Les publications absentes de cette liste
n'ont rien à gagner à une photo — leur planche fonctionne comme elle est.

### Priorité haute — six images qui changent le feed

> **Quatre sont faites.** **A** ouvre la n° 1 depuis le 23 octobre.
> **B** est arrivée le 23 au soir, en 9:16 exact, et elle ouvre la
> **n° 20** — pas la n° 4 comme annoncé ici. La raison tient en une
> ligne, et c'est la règle du § 2 : les deux écrans « matière » de la
> n° 4 portent des **démonstrations calculées** — l'écran vif contre
> l'imprimé terne, le mat contre le couché. On ne remplace pas une
> preuve par un décor. L'écran d'ouverture de la n° 20, lui, ne
> démontre rien : il affirme qu'on touche une carte avant de la lire.
> C'est exactement la place d'un décor, et la docstring de ce gabarit
> l'avait écrit avant que l'image existe.
>
> **C** ouvre la n° 5 — planche 01, la seule des six qui ne démontre
> rien. Les planches 02, 04 et 05 portent les devantures à deux graisses
> et le même mot à trois corps : elles restent dessinées.
>
> **E a changé de publication, et c'est une erreur de ce brief.** Elle
> était annoncée sur la n° 15 — le **quiz**, dont les cinq planches
> demandent d'identifier une matière. Le document le dit lui-même :
> « l'épaisseur des échantillons est volontairement exagérée, trois
> millimètres d'alu sur un panneau d'un mètre ne feraient pas un
> pixel ». C'est le cas rare où le dessin est **supérieur** à la
> photographie : une vraie photo ne montrerait rien à cette échelle, et
> une photo générée rendrait le quiz injouable. E ouvre donc la
> **n° 15 bis**, dont la planche 01 énonce au lieu de démontrer.

| # | Publication | L'image à générer |
|---|---|---|
| ~~**A**~~ | n° 1 · Pédagogie couleur | ✅ **intégrée le 23 octobre.** Nuancier Pantone en éventail, main qui écarte deux teintes, accent **corail**. Ouvre le cycle. |
| ~~**B**~~ | **n° 20** · Ce qu'on sent avant de lire | ✅ **reçue le 23 octobre.** Macro d'une pile de papiers vus **sur la tranche**, lumière rasante qui révèle l'épaisseur et la fibre. Accent **orange** sur un seul, 9:16 exact, zone de texte calme. Déposée en `B-papiers-tranche.png`. |
| ~~**C**~~ | n° 5 · Typographie | ✅ **reçue le 23 octobre.** Caractères en plomb dans un composteur en laiton, vus **de profil** — crans et épaulements face caméra, faces tournées. Accent **bleu** sur un seul sort. Déposée en `C-caracteres-plomb.jpg`. |
| **D** | n° 9 · Un logo tient-il en petit | Un stylo-bille posé en biais sur du papier blanc, et un tampon encreur à côté — l'échelle se lit toute seule. Accent **turquoise** sur le capuchon. |
| ~~**E**~~ | **n° 15 bis** · Un visuel, quatre supports | ✅ **reçue le 23 octobre.** Quatre échantillons de feuille **quelconques** debout sur un établi en chêne, coupés par le haut du cadre, épaisseurs et finitions différentes. Accent **violet** sur un translucide. Déposée en `E-echantillons-debout.jpg`. |
| **F** | n° 21 · Vitrine vue du trottoir | Une devanture **anonyme** photographiée depuis le trottoir d'en face, de nuit, reflets de rue dans le verre. Aucune enseigne lisible, aucun nom. |

### Priorité moyenne — cinq images qui gagnent du réalisme

| # | Publication | L'image |
|---|---|---|
| **G** | n° 17 · Rétroplanning vœux | Une main qui pose une carte imprimée sur une table, pile de cartes à côté, gaufrage visible en lumière rasante. Accent **violet**. |
| **H** | n° 18 · Emballage de fête | Un paquet kraft fermé d'un bandeau imprimé et d'une pastille, en cours de fermeture, mains coupées au poignet. |
| **I** | n° 15 bis · Un visuel, quatre supports | Les quatre supports réels **côte à côte** sur un plan de travail : étiquette, sachet, carte, adhésif. Vue de dessus, léger désordre. |
| **J** | n° 20 · Matières et fabrication | Une découpe en cours : lame, règle en acier, chute d'adhésif qui s'enroule. Geste arrêté. |
| **K** | n° 23 · Impressions de fin d'année | Une sortie d'imprimante en train de tomber dans le réceptacle, légèrement floue par le mouvement. |

### Priorité basse — les fonds d'ambiance, réutilisables partout

Quatre textures neutres, à garder en réserve pour les planches de
titre et de clôture. Elles servent plusieurs fois.

- **L** — plâtre brut, lumière rasante, nuances de crème
- **M** — chêne clair, veines marquées, vue de dessus
- **N** — lin froissé, plis doux, ombre longue
- **O** — béton ciré gris chaud, une seule ombre nette en diagonale

---

## 6. Comment juger une image avant de l'accepter

Six tests. Si l'un échoue, régénérer plutôt que retoucher.

1. **Les mains.** Compter les doigts. C'est encore le défaut le plus
   fréquent, et le plus visible.
2. **Le texte.** Il ne doit y en avoir aucun. S'il en reste, même flou,
   régénérer — un mot inventé dans une image de graphiste est fatal.
3. **La lumière.** Une seule source. Deux ombres qui partent dans deux
   directions, c'est une image de synthèse.
4. **Les reflets.** Dans un verre, dans du métal, ils doivent montrer
   quelque chose de cohérent avec la scène.
5. **La répétition.** Les moteurs recopient un motif à l'identique :
   deux poussières jumelles, deux veines de bois superposables.
6. **Le test du recadrage.** Zoomer à 100 % sur un bord. Si la matière
   devient molle ou se répète, l'image ne tiendra pas en grand.

---

## 7. Où les déposer, et comment les nommer

**Dossier :** `reseaux/visuels/sources/ambiances/`

**Nommage :** la lettre du brief, puis le sujet, en minuscules.
`A-nuancier-eventail.png`, `B-papiers-tranche.png`, et ainsi de suite.

**Format :** PNG ou JPEG qualité maximale. Minimum 2160 px sur le grand
côté.

> ⚠️ **Ce dossier n'est pas versionné** — le dépôt est public. Les
> fichiers vivent sur le disque du projet, et ils disparaissent si le
> conteneur est reconstruit. C'est déjà arrivé deux fois. **Garder
> l'original ailleurs.**

Une fois déposées, je les intègre aux planches avec `photo()`, qui pose
le voile de lisibilité et gère le recadrage — les textes de la planche
restent lisibles par-dessus sans qu'on ait à les déplacer.

---

## 8. Ce que je recommande de ne pas faire

**Ne pas tout remplacer.** Une alternance photo / dessin vaut mieux que
trente photos. Le dessin reste le bon outil quand il faut *démontrer*
— une échelle, une coupe, un avant/après. La photo est le bon outil
quand il faut *faire désirer*.

Mon dosage : **une image générée par publication au maximum**, en
ouverture ou en clôture, le reste dessiné.

**Ne pas générer de visage.** Jamais. Pour « la personne », il n'y a que
les vraies photos de Sandra — il y en a sept, dont quatre déjà
utilisées.

**Ne pas générer ce qu'on peut photographier.** Un nuancier, un papier,
un stylo : Sandra les a sur son bureau. Une photo au téléphone, en
lumière de fenêtre, battra une génération — parce qu'elle sera vraie, et
que ça se voit.
