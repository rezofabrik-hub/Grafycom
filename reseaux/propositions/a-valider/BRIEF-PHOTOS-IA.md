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
| Illustration d'article | 1,9:1 — 1200 × 630 | **2400 × 1260** |

L'illustration d'article sert deux fois : en tête de l'article, et en
vignette quand le lien est partagé. Aucun moteur ne propose 1,9:1 —
demander du **16:9**, le plus proche, et rogner le haut et le bas. Le
sujet se place donc au centre, pas dans le tiers supérieur : c'est la
seule ligne du § 3.6 qui change pour ce format.

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

**Humain** — par défaut : mains et avant-bras seulement, coupés avant
le coude. Peau neutre, aucun bijou, aucun vernis, aucune montre.
**Aucun visage inventé, jamais.** Un visage généré est une personne qui
n'existe pas, présentée comme si elle existait.

**Une exception, et une seule : Sandra.** Accordée par elle le
23 octobre. Son visage, son buste et son regard sont autorisés, parce
qu'une graphiste indépendante se vend d'abord sur une personne et que
son visage n'apparaissait sur **aucun** des trente carreaux de la
grille — les trois photos existantes sont toutes sur une planche de
clôture, qu'il faut faire glisser pour atteindre.

L'exception porte sur **elle**, pas sur ce qui l'entoure. Tout le reste
du cadre reste soumis aux deux règles dures : **rien de lisible**, et
**aucun logo approximé**. C'est précisément là que la première série a
échoué — voir ci-dessous.

#### Ce que la première série de portraits a raté, et ce qu'on en tire

Cinq images reçues le 23 octobre. Mesuré à pleine résolution :

- **Du texte inventé dans quatre des cinq.** « devanfture » pour
  devanture, « MALLES HOLTCARBER » sur l'affiche Halloween,
  « Graautte de voeux » sur la carte tenue en main, l'enseigne du
  croquis brouillée, « (rofycom » sur l'esquisse.
- **Le logo Grafycom redessiné, et différemment dans chaque photo.**
  Comparé à `assets/img/logo-grafycom.webp` : la structure y est —
  l'aile sur le « a », le « com » en script, la ligne de signature —
  mais la tache aquarelle, l'espacement et la position du « com »
  changent d'une image à l'autre. Son propre logo, approximé.
- **Le logo Solaire 66 faux.** Deux sommets au lieu de trois, l'éclair
  au centre au lieu d'être à droite du sommet central, le soleil à côté
  du S au lieu d'être la spirale DANS le O, le « 66 » qui chevauche le
  R et le E. C'est l'erreur du 18 octobre, à l'identique.

**Une seule chose était juste : le pseudo portait son point.**

La parade tient en une ligne de prompt — **rien de net et de lisible
derrière elle** — et en un réflexe : le tableau de liège hors de la
profondeur de champ, aucune affiche nette, l'écran éteint ou tourné.
Les logos qui doivent apparaître ne se demandent pas au moteur : ils
s'**incrustent** depuis le vrai fichier, et `retouche_atelier.py` sait
déjà le faire — `logo_ecran()` et `logo_mural()`, avec les quatre coins
mesurés et non estimés.

#### Et ce qu'elle porte compte

Dans la première série, un pull rouge et un blazer bleu marine. Le
rouge couvre bien plus que les 10 % d'accent autorisés, et le bleu
marine n'est dans aucune des deux listes de la charte.

Sur une photo de Sandra, **elle porte un neutre** — crème, sable,
taupe, écru. Pas par austérité : parce que l'accent de la planche doit
rester le seul, et qu'un vêtement occupe un quart du cadre.

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

**Les symboles réglementés — le piège le plus grave, et il était dans
ce brief.** La ligne H demandait « un paquet kraft fermé d'un bandeau
imprimé et d'une pastille ». C'est exactement ce qu'il ne fallait pas
générer : la publication n° 18 parle de **la mention de tri**, et le
Triman est un symbole réglementé. Un bandeau imprimé sur ce sachet se
serait lu comme cette mention, et un pictogramme inventé est une
affirmation réglementaire fausse — pire qu'une lettre inventée, parce
qu'un client peut s'en prévaloir. D'autant que le texte de cette
publication porte déjà l'avertissement « contenu au conditionnel,
vérification à faire ».

Le sachet reçu est donc **rigoureusement vierge** : ni bandeau, ni
étiquette, ni pastille, ni pictogramme. Négatif correspondant :
`printed band, printed label, sticker, pictogram, recycling symbol,
triman, sorting symbol, eco label, certification mark, barcode, QR
code, stamp`.

**Et les mains sont sorties.** H les demandait, « coupées au poignet ».
Les sept images à sujet les ont toutes évitées et aucune n'en a
souffert. Compter les doigts reste le défaut le plus fréquent des
moteurs, et aucune de ces publications n'avait besoin d'un geste.

**L'extérieur — la seule image qui ne tient pas les sept constantes.**
F est un extérieur : il n'a ni établi, ni fenêtre à 45° à gauche. Trois
entorses, assumées et nommées plutôt que subies — la surface sort de la
liste fermée (bitume gris chaud, le plus proche du béton ciré), la
source est la vitrine elle-même face caméra, et l'image ne porte aucun
accent parce que le bandeau violet de la planche est déjà le sien. Ce
qui tient quand même, et c'est ce qui fait la famille : **une seule
source**, chaude, et la même palette de neutres.

La quatrième décision est la plus importante : **ni fronton, ni ciel,
ni nom dans le cadre.** Une devanture porte une enseigne, une enseigne
générée est un faux logo, et un faux logo sur le compte d'une graphiste
est la faute dont on ne se relève pas. Le cadre commence sous le
bandeau d'enseigne. Une vitre chaude au-dessus d'un bitume mouillé se
lit comme une devanture sans qu'aucun nom existe.

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

> **Les six sont faites.** **A** ouvre la n° 1 depuis le 23 octobre.
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
| ~~**D**~~ | n° 9 · Un logo tient-il en petit | ✅ **reçue le 23 octobre.** Stylo-bille en biais sur une feuille **vierge**, tampon sur le flanc, **semelle sans gravure**. Accent **turquoise** sur le capuchon, 0,18 % de la surface. Sur la planche **06**, la clôture — les cinq autres démontrent. Déposée en `D-stylo-tampon.jpg`. |
| ~~**E**~~ | **n° 15 bis** · Un visuel, quatre supports | ✅ **reçue le 23 octobre.** Quatre échantillons de feuille **quelconques** debout sur un établi en chêne, coupés par le haut du cadre, épaisseurs et finitions différentes. Accent **violet** sur un translucide. Déposée en `E-echantillons-debout.jpg`. |
| ~~**F**~~ | n° 21 · Vitrine vue du trottoir | ✅ **reçue le 23 octobre.** Le bas d'une vitrine éclairée, **fronton hors cadre**, bordure et chaussée mouillée. Ni enseigne, ni ciel, ni vitrine garnie, ni reflet lisible. **Aucun accent** : le bandeau violet de la planche est le sien. Déposée en `F-vitrine-trottoir.png`. |

### Priorité moyenne — cinq images qui gagnent du réalisme

| # | Publication | L'image |
|---|---|---|
| **G** | n° 17 · Rétroplanning vœux | Une main qui pose une carte imprimée sur une table, pile de cartes à côté, gaufrage visible en lumière rasante. Accent **violet**. |
| ~~**H**~~ → **P** | n° 18 · Emballage de fête | ✅ **reçue le 23 octobre**, mais **rien de ce qui était décrit ici**. Un sachet kraft **rigoureusement vierge** sur du plâtre pâle, sans mains. Sur la planche **07**, la clôture. Déposée en `P-sachet-kraft.jpg`. |
| **I** | n° 15 bis · Un visuel, quatre supports | Les quatre supports réels **côte à côte** sur un plan de travail : étiquette, sachet, carte, adhésif. Vue de dessus, léger désordre. |
| **J** | n° 20 · Matières et fabrication | Une découpe en cours : lame, règle en acier, chute d'adhésif qui s'enroule. Geste arrêté. |
| **K** | n° 23 · Impressions de fin d'année | Une sortie d'imprimante en train de tomber dans le réceptacle, légèrement floue par le mouvement. |

#### Les quatre prompts, prêts à coller — écrits le 24 octobre

Tentés depuis ici le 24 octobre : **le générateur a refusé deux fois**,
d'abord la résolution 2K que la formule en cours n'ouvre pas, puis la
génération elle-même, faute de crédits. Les prompts sont donc écrits
ici plutôt que produits, et ils fonctionnent avec n'importe quel moteur.

Chacun suit le bloc du § 3.6 : seule la première ligne change. Les
surfaces viennent de la liste close du § 3.5, et chaque image ne porte
qu'un seul accent.

> ⚠️ **Le format.** Demander du **4:5** si le moteur le propose. S'il
> n'offre que du 3:4, le prendre : le recadrage « couvrir » rognera le
> haut et le bas plutôt que les côtés, et le sujet est dans les deux
> tiers supérieurs. Ne jamais prendre du 16:9, qui perd les bords —
> c'est souvent là qu'est le sujet.

> ⚠️ **Viser 2160 px sur le grand côté.** En dessous, l'image se juge
> sur la planche et pas sur le principe (voir § 3.3) — mais un
> agrandissement de 1,3 sur une photographie commence à se voir.

**G — n° 17, rétroplanning vœux.** Accent violet, surface chêne clair.

```
A hand and forearm, cut off before the elbow, setting a thick blank
greeting card down flat on a table, a small stack of identical blank
cards beside it, blind embossing catching the raking light across the
card face, the card surface carrying no text and no mark of any kind

on light oak, shot on 50mm at f/2.2, single warm window light from
camera left at 45 degrees, 4800K late afternoon, soft shadows with
defined edges, shallow depth of field with background falling off,
warm neutral palette of cream #f7f1ef, sand #efe4dd, taupe #a2897c and
brown #6d5a50, exactly one accent of violet #a86cd0 covering less than
10 percent of the frame, fine film grain, slight natural imperfection,
editorial still life photography, vertical 4:5 framing, subject
entirely in the upper third, lower third is calm empty surface with
soft shadow falloff for text overlay

NEGATIVE: faces, people, eyes, text, letters, numbers, logos,
watermarks, brand names, readable signage, printed words, symmetry,
flat lighting, pure white background, 3D render, CGI, plastic sheen,
oversaturation, two accent colours, green plants, flowers, screens,
laptops, phones, gold, silver, metallic, jewellery, watches, nail
polish
```

**I — n° 15 bis, un visuel sur quatre supports.** Accent orange,
surface béton ciré gris chaud, vue de dessus.

```
Four blank printed pieces laid side by side in slight disorder, seen
from directly above — a gummed label, a flat kraft paper bag, a thick
business card and a cut sheet of matte vinyl — every surface
completely unmarked, no text and no image on any of them

on warm grey polished concrete, shot on 50mm at f/2.2, single warm
window light from camera left at 45 degrees, 4800K late afternoon,
soft shadows with defined edges, shallow depth of field with
background falling off, warm neutral palette of cream #f7f1ef, sand
#efe4dd, taupe #a2897c and brown #6d5a50, exactly one accent of orange
#f5883c covering less than 10 percent of the frame, fine film grain,
slight natural imperfection, editorial still life photography,
vertical 4:5 framing, subject entirely in the upper third, lower third
is calm empty surface with soft shadow falloff for text overlay

NEGATIVE: faces, people, eyes, text, letters, numbers, logos,
watermarks, brand names, readable signage, printed words, symmetry,
flat lighting, pure white background, 3D render, CGI, plastic sheen,
oversaturation, two accent colours, green plants, flowers, screens,
laptops, phones, gold, silver, metallic
```

**J — n° 20, matières et fabrication.** Accent turquoise, surface
chêne clair.

```
A cut in progress, the gesture stopped mid-motion — a scalpel blade
pressed along a steel ruler, a thin curl of offcut vinyl lifting away
from the sheet, one hand and forearm only, cut off before the elbow,
the vinyl entirely plain with nothing printed on it

on light oak, shot on 50mm at f/2.2, single warm window light from
camera left at 45 degrees, 4800K late afternoon, soft shadows with
defined edges, shallow depth of field with background falling off,
warm neutral palette of cream #f7f1ef, sand #efe4dd, taupe #a2897c and
brown #6d5a50, exactly one accent of turquoise #3ec2b3 covering less
than 10 percent of the frame, fine film grain, slight natural
imperfection, editorial still life photography, vertical 4:5 framing,
subject entirely in the upper third, lower third is calm empty surface
with soft shadow falloff for text overlay

NEGATIVE: faces, people, eyes, text, letters, numbers, logos,
watermarks, brand names, readable signage, printed words, symmetry,
flat lighting, pure white background, 3D render, CGI, plastic sheen,
oversaturation, two accent colours, green plants, flowers, screens,
laptops, phones, gold, silver, metallic, jewellery, watches, nail
polish
```

**K — n° 23, impressions de fin d'année.** Accent orange, surface
béton ciré gris chaud.

```
A freshly printed sheet dropping into the output tray of a press,
caught slightly blurred by its own motion, a small stack already
landed beneath it, every sheet carrying only soft abstract blocks of
colour and nothing legible

on warm grey polished concrete, shot on 50mm at f/2.2, single warm
window light from camera left at 45 degrees, 4800K late afternoon,
soft shadows with defined edges, shallow depth of field with
background falling off, warm neutral palette of cream #f7f1ef, sand
#efe4dd, taupe #a2897c and brown #6d5a50, exactly one accent of orange
#f5883c covering less than 10 percent of the frame, fine film grain,
slight natural imperfection, editorial still life photography,
vertical 4:5 framing, subject entirely in the upper third, lower third
is calm empty surface with soft shadow falloff for text overlay

NEGATIVE: faces, people, eyes, text, letters, numbers, logos,
watermarks, brand names, readable signage, printed words, symmetry,
flat lighting, pure white background, 3D render, CGI, plastic sheen,
oversaturation, two accent colours, green plants, flowers, screens,
laptops, phones, gold, silver, metallic
```

**Une fois reçues**, les déposer dans
`reseaux/visuels/sources/ambiances/` sous `G-…`, `I-…`, `J-…`, `K-…`
— le § 7 dit comment les nommer — et me le dire : `photo()` les pose
sur la planche avec le voile de lisibilité, sans que les textes
bougent.

### ~~Priorité basse~~ — les quatre textures, faites le 23 octobre

Elles étaient rangées en réserve. Elles se sont révélées la réponse la
moins chère au vrai défaut du feed : **douze carreaux d'affilée sans
photographie**, des positions 13 à 24 de la grille. Quatre images pour
quatre planches, et la plus longue suite tombe de 12 à 6.

| | Texture | Planche | État |
|---|---|---|---|
| **L** | plâtre brut | n° 6 · 4 idées reçues sur l'impression | ✅ `L-platre-brut.jpg` |
| **M** | chêne clair | n° 17 · Rétroplanning vœux | ✅ `M-chene-clair.jpg` |
| **N** | lin froissé | n° 24 · Quiz fin d'année | ✅ `N-lin-froisse.jpg` |
| **O** | béton ciré | n° 8 · Enseigne, autorisation | ✅ `O-beton-cire.jpg` |

**Ce qu'une texture change par rapport aux six images à sujet.** Elle
n'a pas de sujet, donc la grille de composition ne s'applique pas : ce
qui la remplace est le **plan de netteté**. La lumière rasante et le
grain dans le tiers haut, le premier plan qui part dans le flou vers le
bas — c'est physiquement ce que fait un 50 mm à f/2.2 près d'une
surface, et ça donne la zone calme sans qu'on ait à la fabriquer.

Et **aucun accent** : les quatre planches portent déjà le leur. La
pastille QUIZ corail de la n° 6 est restée en place sur la photo.

**Deux ouvertures restent volontairement en typographie pleine page** —
la n° 7 « Qui possède votre logo ? » et la n° 5 bis « Le blog ». C'est
l'écart entre les deux traitements qui fait ressortir les photos ; six
fonds photographiques d'affilée les annuleraient.

#### Le test du motif recopié, et comment le rater

Sur une texture, c'est **le** contrôle. Mais il se mesure mal, et la
première mesure a donné un faux positif.

Corrélation croisée d'un carré de 220 px contre tout le reste de
l'image, en excluant son voisinage. Sans passe-haut préalable, le
**dégradé lent** de la lumière suffit à faire monter le score à 0,99
sur n'importe quelle surface lisse : on mesure la lumière, pas la
matière.

Après passe-haut : plâtre **0,37**, lin **0,54**, chêne **0,72**, béton
**0,92**. Les deux derniers restent hauts, et ce ne sont pas des
copies : le chêne a un fil droit qui se ressemble d'un bout à l'autre,
et le béton porte **une arête d'ombre** qui traverse le cadre. Sorti
les deux carrés les plus corrélés du béton et regardé : c'est deux fois
la même ligne d'ombre, une seule vraie structure.

**La leçon vaut plus que le chiffre : un score élevé se regarde avant
de se croire.** Sortir les deux carrés, les poser côte à côte. Un motif
recopié se voit en une seconde ; une structure continue aussi.

---

## 5 ter. Les quatre photographies du blog — passées à la règle

`python3 reseaux/illustrations.py --photos` en liste quatre. Laurent a
demandé le 24 octobre des prompts pour les faire générer. **Deux
peuvent l'être, deux ne peuvent pas**, et la frontière est celle du
§ 2, pas une préférence.

| # | Ce qu'il faut | Article | Verdict |
|---|---|---|---|
| **α** | Une devanture du centre ancien, enseigne comprise | Autorisation d'enseigne | ⚠️ générable en **décor anonyme** seulement |
| **β** | Un bon à tirer posé à côté de l'écran qui affiche le même visuel | Couleurs écran / impression | ⛔ **non** |
| **γ** | Un nuancier ouvert, en lumière du jour | Couleurs écran / impression | ✅ oui |
| **δ** | Les fichiers sources ouverts, avec leurs calques | Qui possède votre logo | ⛔ **non** |

### Pourquoi β et δ ne se génèrent pas

Ce ne sont pas des décors, ce sont des **démonstrations**.

**β** existe pour qu'on voie l'écart entre un écran et un imprimé. Une
image générée fabriquerait cet écart au lieu de le constater : elle
montrerait exactement la différence qu'on lui aurait demandé de
montrer. C'est la définition d'un faux, et c'est déjà la raison pour
laquelle l'image **B** n'a pas pris la planche de la n° 4.

**δ** existe pour montrer ce qu'un client reçoit vraiment. Une
arborescence de calques inventée est une preuve inventée. Et elle
franchit en plus la liste close du § 3.5, qui interdit l'**écran
allumé** — parce qu'un écran généré porte du faux texte, toujours.

**Les deux se photographient en dix minutes**, sans matériel : un
imprimé posé devant l'écran qui affiche le même fichier, le logiciel
ouvert sur un vrai projet. Ce sont les deux seules de la liste qui
n'ont besoin d'aucun déplacement. En attendant, les schémas tiennent
la place, et ils la tiennent honnêtement : `cmjn.png` explique le
procédé, `droits.png` explique le droit, aucun des deux ne prétend
être une photographie.

### α — la devanture, et sa condition

Générable, mais **jamais présentée comme une rue de Perpignan**. Une
façade générée qu'on légende « centre ancien de Perpignan » est un
faux, même si elle est jolie. Elle sert de décor, le texte alternatif
et la légende doivent le dire, et elle ne porte aucune enseigne
lisible.

Si l'article doit montrer une vraie devanture du 66 — et il gagnerait
à le faire — c'est une photographie, prise par Sandra, et rien d'autre.

```
A shop front seen straight on, early morning, the fascia board
completely blank with no sign and no lettering of any kind, shutters
half up, worn stone surround and an old painted door frame

on warm grey polished concrete pavement, shot on 50mm at f/2.8, single
warm window light from camera left at 45 degrees, 4800K late afternoon,
soft shadows with defined edges, shallow depth of field with background
falling off, warm neutral palette of cream #f7f1ef, sand #efe4dd, taupe
#a2897c and brown #6d5a50, exactly one accent of blue #2f7fc4 covering
less than 10 percent of the frame, fine film grain, slight natural
imperfection, editorial architectural photography, horizontal 16:9
framing, subject centred, calm empty surface on the left for text
overlay

NEGATIVE: faces, people, eyes, text, letters, numbers, logos,
watermarks, brand names, readable signage, shop names, house numbers,
street signs, posters, menus, price lists, symmetry, flat lighting,
pure white background, 3D render, CGI, plastic sheen, oversaturation,
two accent colours, green plants, flowers, screens, cars, gold, silver,
metallic
```

> ⚠️ **À vérifier à pleine résolution avant de l'accepter.** Les
> moteurs posent du faux texte sur les façades — c'est exactement ce
> qu'a raté la première série de portraits, § 3.5. Une seule lettre
> inventée sur le bandeau, et l'image part.

Elle se déposerait en `assets/img/blog/devanture.png`, et elle
**n'évince pas** `enseigne.png` : le schéma des deux façades porte
l'argument de l'article — le lieu décide, pas la taille — et une photo
ne le dit pas. Elle viendrait en seconde figure, pas en tête.

### γ — le nuancier

Le cas simple. C'est de la matière, ça ne démontre rien, et ça
remplace avantageusement un aplat.

```
An open fan-deck of printing colour swatches spread in an arc on a
table, each blade a solid flat colour with no printed reference,
numbers or text anywhere, the metal rivet and the worn edges visible

on light oak, shot on 50mm at f/2.2, single warm window light from
camera left at 45 degrees, 4800K late afternoon, soft shadows with
defined edges, shallow depth of field with background falling off,
warm neutral palette of cream #f7f1ef, sand #efe4dd, taupe #a2897c and
brown #6d5a50, exactly one accent of orange #f5883c covering less than
10 percent of the frame, fine film grain, slight natural imperfection,
editorial still life photography, horizontal 16:9 framing, subject
centred, calm empty surface on the right for text overlay

NEGATIVE: faces, people, eyes, text, letters, numbers, codes, logos,
watermarks, brand names, Pantone, readable references, symmetry, flat
lighting, pure white background, 3D render, CGI, plastic sheen,
oversaturation, two accent colours, green plants, flowers, screens,
laptops, phones, gold, silver, metallic
```

> ⚠️ **« Pantone » est un nom de marque**, et il est dans le négatif
> pour cette raison. Un éventail générique dit la même chose à un
> lecteur, et n'emprunte le nom de personne.

Elle se déposerait en `assets/img/blog/nuancier.png`, en seconde
figure de l'article sur les couleurs, à côté de `cmjn-papiers.png` qui
montre l'autre moitié du sujet — l'encre et le papier.

### Une fois reçues

Les déposer dans `assets/img/blog/`, me le dire, et j'écris la ligne
`[figure: …]` à sa place dans l'article, légende et description
alternative comprises. Le reste du dispositif ne bouge pas.

---

## 5 bis. Ce qui ne recevra pas de photographie, et pourquoi

Vérifié publication par publication le 23 octobre. **Ce n'est pas une
liste d'attente : c'est une liste de refus motivés.** Elle existe pour
que la question ne se repose pas dans trois semaines.

### Les quatre réalisations — règle absolue

Solaire 66, Sweet Dream, Krusty, Big Food. Aucune image générée
n'approche le travail d'un client, jamais, à aucune place du carrousel.

### Les démonstrations calculées

| Publication | Ce qu'elle démontre | Pourquoi le dessin gagne |
|---|---|---|
| n° 4 · RVB/CMJN | les deux synthèses | les recouvrements sont **calculés**, pas choisis |
| n° 11 · slogan anglais | une devanture qui porte un slogan | l'enseigne **est** la question |
| n° 12 · vitrophanie | voir ci-dessous | les cinq écrans |
| n° 13 · fichier vectoriel | la marque témoin réduite | c'est le même objet d'un écran à l'autre |
| n° 15 · quiz matières | quatre coupes | l'épaisseur est **volontairement exagérée** : 3 mm d'alu sur un panneau d'un mètre ne feraient pas un pixel |
| n° 18 · emballage, planches 01-02 | la zone à réserver | c'est le **même** sachet sur les deux planches |
| n° 22 · sticker | une vitrine et ses stickers | les stickers **sont** la question |
| les dilemmes | A contre B | la comparaison exige deux objets identiques à un détail près |

### La n° 12, vérifiée écran par écran

C'était la dernière candidate du creux du feed. Elle est fermée deux
fois.

**Les quatre premiers écrans démontrent**, et le plus décisif est le
premier, de façon subtile : il porte **une cote**. Une ligne de mesure
tracée comme sur un plan, qui annonce 6 m² sur la largeur exacte de la
vitrine dessinée. Sur une vitrine générée, cette cote mesurerait
quelque chose dont personne ne connaît la taille — on affirmerait une
surface qui n'est pas celle de l'objet montré. C'est la faute du
dibond, transposée à une dimension.

**Le cinquième ne démontre rien, et il est fermé quand même.** Le
document le dit déjà : « une vitrine inventée sur le compte d'une
graphiste qui habille des vitrines est précisément l'image qui se
retourne contre elle ». Et c'est le cas le plus exposé : il montre une
vitrine **habillée**, décor adhésif et enseigne. Exactement ce que
Sandra vend.

C'est ce qui le sépare de **F**, pourtant une devanture elle aussi : F
ne montre que du vitrage nu, une bordure et du bitume. Aucun habillage,
aucune enseigne, rien qui ressemble à une commande. Elle ne prétend à
rien.

### Conséquence : le creux du feed est structurel

Positions 13 à 18 de la grille — quiz matières, Krusty, slogan anglais,
fichier vectoriel, vitrophanie, dilemme carte. Six carreaux sans
photographie, et les six sont exclus pour une raison écrite.

**Ce n'est pas un oubli à rattraper.** C'est la zone du cycle où les
publications démontrent le plus, donc où le dessin fait un travail que
la photographie ne peut pas faire. Le feed y est plus uniforme parce
que le contenu y est plus technique. Aller plus loin obligerait à
casser une démonstration, et la première personne à s'en apercevoir
serait le public de Sandra.

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
