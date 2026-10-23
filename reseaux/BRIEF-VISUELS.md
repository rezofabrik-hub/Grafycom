# Brief visuels Grafycom — cycle du 26 octobre au 5 décembre 2026

Document destiné à un prestataire ou à un outil de génération d'images et
de vidéos. Il décrit **le rendu attendu**, planche par planche, pour les
177 visuels du cycle : 133 planches de publications, 44 écrans de stories,
plus les 7 illustrations d'articles de blog.

---

## 0. À lire avant tout : ces visuels existent déjà

Les 177 planches sont **produites**, en PNG, par un script Python
(`reseaux/visuels.py`, bibliothèque Pillow). Elles sont livrées avec ce
brief. Ce document n'est donc pas une commande à partir de rien : c'est la
spécification de ce qui existe, pour trois usages possibles.

**Usage 1 — animer les planches existantes (recommandé pour les reels).**
Les six reels sont aujourd'hui des suites d'écrans fixes. Les monter avec
la voix off fonctionne, mais reste statique. Un modèle vidéo qui prend une
image en entrée (image-to-video) et lui ajoute un mouvement discret —
parallaxe, apparition progressive d'un élément, travelling lent — produit
le vrai gain, **sans rien réinventer** : le contenu reste exactement celui
qui a été validé. C'est l'usage où un outil génératif apporte le plus et
risque le moins.

**Usage 2 — refaire une planche en mieux.** Certaines sont volontairement
schématiques. Les redessiner avec plus de métier est légitime, à condition
de respecter la charte et les règles de la section 1.

**Usage 3 — produire ce que le script ne sait pas faire.** Les matières en
lumière rasante (dorure, gaufrage, vernis sélectif) sont le point faible
reconnu du dessin : elles se *sentent*, et un tracé vectoriel n'en rend
rien. Voir la publication n° 20.

> **Les planches existantes sont la référence visuelle.** En cas de doute
> entre ce document et l'image livrée, c'est **l'image** qui fait foi.

---

## 1. Les règles non négociables

Ces règles viennent de la ligne éditoriale du compte. Un visuel qui en
viole une ne se publie pas, quelle que soit sa qualité.

### 1.1 Les droits doivent être clairs

Aucune photo trouvée, aucune banque d'images sans licence commerciale
explicite, aucun élément de marque appartenant à un tiers.

### 1.2 Aucun texte inventé, nulle part

C'est la règle la plus importante, et celle qu'un modèle génératif viole
le plus souvent. **Le 13 octobre 2026, deux images proposées comme des
photographies portaient sur leurs devantures « S A.CKS », « Tïvllts »,
« nmcces » et, sur un auvent, une suite de signes illisibles.** Un modèle
dessine la *forme* d'un texte sans savoir l'écrire.

Conséquences pratiques :

- **Tout texte lisible doit être composé, pas généré.** Si le visuel passe
  par un modèle d'image, le texte est ajouté ensuite, en vectoriel, dans
  les polices de la charte.
- **Une enseigne vue de loin ne porte pas de lettres : elle porte des
  barres abstraites.** C'est un choix, pas un pis-aller — à vingt mètres
  l'œil ne lit pas un nom, il voit un rythme. Des barres disent cela sans
  prétendre écrire quoi que ce soit.
- **Vérification systématique :** agrandir chaque enseigne, affiche,
  étiquette du visuel livré. Un seul caractère approximatif = visuel
  refusé.

Le compte est tenu par une graphiste. Une enseigne au texte illisible sur
une publication qui parle de lisibilité d'enseigne est le genre de détail
qu'un confrère repère, et qu'il montre.

### 1.3 Aucun commerce réel identifiable

Quatre publications du cycle parlent de **non-conformité** (n° 10, 14, 18,
22). Elles ne peuvent pas illustrer leur sujet avec la vitrine de
quelqu'un, même floutée. Toutes les devantures sont fictives. Le nom
générique utilisé est **« MAISON BERNAT »** ou **« VOTRE NOM »** ; la
marque fictive des démonstrations de logo s'appelle **« ATELIER DU
PONT »**, et pour la publication sur la loi Toubon, **« SUNSET COFFEE »**.

### 1.3 bis Le travail d'un client se montre avec SON fichier

Quand un visuel montre le travail livré à un client — un logo à l'écran,
une carte imprimée, une enseigne posée — c'est **le fichier réel** qui est
incrusté, jamais une reconstitution.

Le cas s'est présenté le 18 octobre : deux photos d'atelier montraient le
logo Solaire 66 ouvert sur un écran. Le rendu était proche, et faux — le
dessin des montagnes, la spirale du soleil dans le O et les lettres
différaient de l'original. Publier une approximation du logo d'un client
sur le compte de la graphiste qui l'a dessiné, c'est le seul endroit où
une erreur de ce genre se voit immédiatement, et par la personne la plus
mal placée pour ne pas la voir.

Les fichiers clients disponibles sont dans
`reseaux/visuels/sources/clients/` — Solaire 66 (logo couleur, trois
monochromes, carte recto-verso, panneau), Big Food (vectoriel, les deux
compositions), Krusty (logo et dépliant), Sweet Dream (logo, deux lignes,
dépliant), Social Miroir (rond, carré, en long), SR Coiffure. Ce dossier
n'est **pas versionné** : le dépôt est public, et il a déjà été vidé deux
fois par une reconstruction du conteneur. Ce qui ne se relève pas dans un
fichier — le violet de Big Food, par exemple — vit dans
`reseaux/couleurs-clients.json`, qui l'est.

### 1.4 Ni visage inventé, ni main dessinée

Dans les **planches dessinées** : aucune personne, et **pas de mains** : un plan de
mains dessiné est soit maladroit, soit une illustration de banque d'images
déguisée. Là où le découpage d'origine prévoyait des mains (une table de
famille, un doigt sur un calendrier), elles ont été retirées et remplacées
par ce que le plan devait montrer.

**Les photographies de Sandra font exception**, évidemment : elle est la
graphiste, c'est son compte, et les portraits d'atelier validés le
18 octobre la montrent de face et au travail. La règle vise les figurants
inventés dans un visuel pédagogique, pas la personne qui tient le
studio.

### 1.5 La typographie française

Espace **insécable** avant `? ! ; :` et à l'intérieur des guillemets
français `« »`. Les heures s'écrivent `17 h 30` avec des insécables, les
dates `mardi 10 novembre` de même — un `?` seul en début de ligne ou un
`8 h` coupé en deux sont des défauts rédhibitoires.

### 1.6 Le pseudo et les mentions exactes

- Le pseudo est **`@grafycom.graphiste`**, avec le point. Jamais
  « @grafycom graphiste », jamais sans le point.
- Le formulaire d'enseigne est le **Cerfa n° 16308\*01**. L'astérisque
  fait partie du numéro et doit sortir entière. L'ancien **14798\*01** est
  périmé depuis le 1er juillet 2026 et n'apparaît que dans la publication
  qui dit justement qu'il est périmé.
- Un document administratif n'est **jamais reproduit** : la publication
  n° 10 montre un *schéma* de formulaire, portant la mention « schéma »,
  sans emblème ni mise en page officielle.

---

## 2. La charte graphique

Valeurs exactes, lues dans la feuille de style du site `grafycom.fr`.
**Aucune autre couleur ne doit apparaître**, à une exception documentée
(section 2.4).

### 2.1 L'aquarelle — accents, jamais les fonds

| Nom | Hex | Usage |
|---|---|---|
| bleu | `#2f7fc4` | chiffres, encadrés d'information, fond plein de carton |
| bleu vif | `#35a9dd` | second bleu, dégradés |
| turquoise | `#3ec2b3` | accents, matières |
| violet | `#a86cd0` | bandeaux d'accroche, fond plein de carton final |
| rose | `#e75ba6` | rare |
| magenta | `#e33d82` | dégradés |
| corail | `#f2585c` | **l'accent principal** : pastilles, flèches, soulignements |
| orange | `#f5883c` | saison, matières chaudes |
| jaune | `#f9c33f` | lumière, vitrines éclairées |

### 2.2 La base chaude — fonds et texte

| Nom | Hex | Usage |
|---|---|---|
| crème | `#f7f1ef` | **le fond par défaut** |
| crème rosé | `#f3eae9` | fond alternatif |
| sable | `#efe4dd` | surfaces |
| sable foncé | `#e4d5cc` | filets, séparateurs |
| taupe | `#a2897c` | surtitres, légendes secondaires |
| brun | `#6d5a50` | **le texte courant** |
| brun clair | `#8a7469` | variante |
| encre | `#2f2723` | **les titres**, et le fond des planches sombres |
| blanc | `#ffffff` | fond alternatif, texte sur fond sombre |

### 2.3 Les deux dégradés

**Le fond « sable chaud »** — c'est le dégradé du site, utilisé comme fond
de planche. Linéaire, **angle 150°** (convention CSS), trois arrêts :
`#f7f1ef` à 0 %, `#f1e6e1` à 55 %, `#e9dcd5` à 100 %. Très doux, presque
imperceptible : il ne doit jamais se remarquer comme un effet.

**Le filet dégradé** — la signature graphique du compte. Une barre
horizontale aux coins arrondis, **180 px de large sur 10 px de haut**,
posée au-dessus d'un titre. Dégradé de gauche à droite sur huit arrêts :

`#2f7fc4` 0 % → `#35a9dd` 18 % → `#3ec2b3` 33 % → `#a86cd0` 52 % →
`#e33d82` 70 % → `#f2585c` 84 % → `#f5883c` 94 % → `#f9c33f` 100 %

> **Le site ne pose jamais un aplat bleu ou violet sur toute une page.**
> Il pose ce filet de quelques pixels sur un fond crème. Les planches font
> pareil. C'est ce qui empêche le feed de crier.

### 2.4 L'unique exception à la charte

Les schémas **RVB et CMJN** de la publication n° 4 utilisent les primaires
physiques : rouge `(255,0,0)`, vert `(0,255,0)`, bleu `(0,0,255)` pour la
lumière ; cyan `(0,174,239)`, magenta `(236,0,140)`, jaune `(255,241,0)`,
noir `(35,31,32)` pour l'encre. Ce ne sont pas des couleurs choisies, ce
sont les valeurs dont la publication parle : les remplacer par des
couleurs de la charte rendrait les schémas faux. **Nulle part ailleurs.**

### 2.5 Les polices

| Rôle | Police | Graisses | Usage |
|---|---|---|---|
| Titrage | **Playfair Display** | 500, 700, 800 | tous les titres, les grands chiffres |
| Texte | **Inter** | 400, 600, 800 | texte courant, légendes, surtitres, pastilles |
| Manuscrit | **Caveat** | — | notes manuscrites, mots écrits à la main sur une carte |
| Mono | Courier Prime | — | mentions techniques (rare) |

Playfair est une serif à empattements : elle demande un **interligne de
1,16** minimum, sinon les hampes touchent les accents de la ligne du
dessous. Inter en texte courant : interligne **1,38**.

Attention : **Inter ne contient ni `→` ni `≠` ni `←`.** Ces caractères
sortent en carré vide. Toute flèche doit être **tracée** (un trait plus un
triangle), jamais écrite.

---

## 3. Formats et grille

| Format | Dimensions | Usage |
|---|---|---|
| Post | **1080 × 1350** (4:5) | carrousels, dilemmes A/B, quiz |
| Story / Reel | **1080 × 1920** (9:16) | écrans de stories et de reels |
| Aperçu de lien | 1200 × 630 | illustrations d'articles de blog |

**Marge : 86 px** sur les quatre côtés, pour tous les formats. Le texte ne
la franchit jamais.

**La ligne de signature** est à `hauteur − 86 − 26` px, soit **y = 1238**
en 4:5 et **y = 1808** en 9:16. Aucun bloc de texte ne descend sous cette
ligne.

---

## 4. Le vocabulaire de mise en page

Dix éléments reviennent dans toutes les planches. Les respecter est ce qui
fait tenir le feed ensemble.

**Le surtitre.** Un petit label en capitales, Inter 800, **26 px**, avec
un interlettrage d'environ 3 px, en taupe `#a2897c`. Posé au-dessus du
titre. Exemples : « IDENTITÉ VISUELLE », « RÉGLEMENTATION », « QUIZ »,
« REEL · 0-3 S ». Il situe la publication avant qu'on lise le titre.

**Le filet.** Décrit en 2.3. Posé juste au-dessus du titre, 34 px de blanc
en dessous. Il n'apparaît pas sur toutes les planches : c'est un accent,
réservé aux planches d'ouverture, de respiration et de conclusion.

**Le titre.** Playfair, de **62 à 116 px** selon la longueur, couleur
encre `#2f2723` sur fond clair, blanc sur fond sombre. Interligne 1,16.
Les retours à la ligne sont **voulus** et font partie du rythme : les
respecter.

**Le texte courant.** Inter 400 ou 600, **34 à 46 px**, brun `#6d5a50`.
Interligne 1,38. Posé à la marge gauche, jamais justifié, jamais centré
sauf mention contraire.

**La pastille.** Un rectangle à coins très arrondis (rayon = demi-hauteur)
contenant un mot court en Inter 800 blanc. Fond corail le plus souvent.
Sert aux numéros, aux étiquettes « QUIZ », « VRAI », « FAUX », « A », « B ».

**Les puces numérotées.** Un disque plein de 44 px de diamètre, fond
corail ou violet, chiffre en Inter 800 blanc au centre, texte à 62 px à
droite du disque. Interligne entre items : 1,5 à 1,7.

**Le grand chiffre.** Inter 800, **150 à 260 px**, en bleu `#2f7fc4` ou
corail. Pour une heure, un prix, une mesure. Seul sur la planche, avec son
explication en dessous.

**La flèche.** Tracée : un trait horizontal et un triangle plein, corail,
environ 68 px de long. Marque l'appel à l'action.

**La signature.** `@grafycom.graphiste`, Inter 600, **26 px**, en bas à
gauche à la marge. Brun sur fond clair, sable `#efe4dd` sur fond sombre.

**Le numéro de planche.** `3/6`, Inter 600, 24 px, en haut à droite, en
taupe. Sur les carrousels de plus de quatre planches.

**La relance d'abonnement.** « Abonnez-vous : un conseil par semaine. »,
Inter 600, 30 px, sable, posée **48 px au-dessus** de la signature.
**Uniquement sur le dernier écran des reels** — ce sont eux qui touchent
les gens qui ne suivent pas encore le compte. Une demande répétée sur
chaque planche ne se remarque plus.

---

## 5. Les objets dessinés récurrents

Sept objets reviennent d'une publication à l'autre. **Le même objet doit
être rigoureusement le même d'une planche à l'autre** : c'est ce qui rend
les comparaisons honnêtes, et c'est non négociable sur les démonstrations.

### 5.1 La devanture

Vue de face, en élévation, jamais en perspective. De bas en haut : un
soubassement de 5,5 % de la hauteur, un vitrage, un bandeau d'enseigne de
17 % de la hauteur en haut. Le vitrage est divisé par deux meneaux
verticaux ; la porte occupe les 28 % de droite, avec une poignée ronde.
Encadrement en encre, épaisseur = largeur ÷ 52.

La devanture a une **échelle réelle : 3,20 m de haut**. C'est ce qui
permet de placer la bande de hauteur des yeux entre **1,40 m et 1,70 m**
du sol sans la deviner.

Déclinaisons : éclairée (dégradé jaune → orange derrière la vitre),
éteinte de nuit (verre bleu très sombre + reflet de la rue d'en face +
traînées de lumière en transparence), au trait (contours bruns sur blanc),
avec décor de fêtes (bande translucide portant des motifs), avec adhésifs
promotionnels (pastilles de couleur), avec lettrage adhésif à hauteur des
yeux.

### 5.2 La rue au crépuscule

Six façades de largeurs et de hauteurs différentes — un centre ancien
n'est jamais régulier. Ciel en dégradé vertical : bleu `#2f7fc4` en haut →
violet `#a86cd0` à 42 % → corail `#f2585c` à 78 % → jaune `#f9c33f` à
l'horizon. Chaque façade a un ou deux étages de fenêtres, dont certaines
éclairées, une vitrine de rez-de-chaussée et un bandeau d'enseigne. Les
enseignes allumées portent un **halo flou**. Au premier plan : trottoir,
bordure, chaussée.

**Les enseignes portent des barres, pas des mots.** Voir 1.2.

### 5.3 Les quatre matières, en coupe

Vues de trois quarts, tranche tournée vers le spectateur, **épaisseur
volontairement exagérée** (un dessin technique grossit ce qu'il explique).

- **Alu composite** : deux peaux claires et une **âme noire** entre elles,
  visible sur la tranche. Mention « 3 mm ».
- **Plexiglas** : masse translucide turquoise très pâle, **tranche polie**
  saturée et lumineuse, avec un halo — c'est elle qui conduit la lumière.
- **Adhésif dépoli** : une vitre avec un rayonnage derrière. Au-dessus de
  la ligne, les formes sont **nettes** ; en dessous, **floutées et
  éclaircies**. Les mêmes formes traversent la ligne : c'est le même objet
  net puis brouillé, sinon la démonstration ne démontre rien.
- **Papier gaufré** : un motif rendu par **deux traits décalés** — un
  blanc décalé vers le haut-gauche, un taupe vers le bas-droite. Pas de
  couleur : un gaufrage n'a qu'une ombre et une lumière.

### 5.4 Le logo fictif « ATELIER DU PONT »

Trois disques concentriques : bleu `#2f7fc4`, bleu vif `#35a9dd` à 72 %,
crème à 44 %. Plus, en version détaillée, dix arcs fins blancs sur le bord
et le nom en Inter 600 sous le symbole. Les arcs fins et le nom sont
**les premiers à disparaître quand on réduit** — c'est le sujet de la
publication n° 9.

### 5.5 Le sachet cadeau

Élévation : corps rectangulaire, pli horizontal à 12 % de la hauteur,
soufflet latéral à 17 % de la largeur, deux anses en arc au-dessus, un
bandeau imprimé violet à flocons à mi-hauteur, une pastille ronde corail
au logo. Version au trait pour la seconde planche : **le même sachet**.

### 5.6 La carte imprimée

Posée à plat, légèrement tournée (±7 à 14°), avec une **ombre portée qui
suit la rotation** — l'ombre est la silhouette tournée de l'objet, pas un
rectangle flou posé dessous. Gaufrage rendu comme en 5.3. Les mots
manuscrits sont en Caveat.

### 5.7 Le schéma de formulaire

Une feuille blanche avec ombre portée, un bandeau d'en-tête bleu très
pâle portant le numéro de Cerfa en Inter 800 bleu, un titre, puis cinq à
sept lignes de champs (une case à cocher vide + un trait). En bas à
gauche, en taupe, la mention **« schéma »**. Ni emblème, ni logo
administratif, ni mise en page officielle.

---

## 6. Les 30 publications, planche par planche

Les textes exacts (accroche, légende, texte alternatif, hashtags) sont
dans `instagram-facebook.md`. Ce qui suit décrit **le rendu**.

Notation : `fond` / `surtitre` / **titre** / corps / éléments dessinés.

---

### n° 1 · lundi 26 octobre · Carrousel 7 planches · Pédagogie couleur

1. `sable chaud` · surtitre « IDENTITÉ VISUELLE » · filet · **« Votre
   couleur dit déjà ce que vous vendez. »** (104 px) · signature.
2. `blanc` · **« Avant même de lire votre nom… »** (62 px) · trois disques
   pleins de 230 px — turquoise, bleu, rose — alignés sur une ligne ·
   sous eux : « Le client a déjà deviné votre secteur. » (42 px, encre).
3. `blanc` · les **mêmes trois disques**, légendés en dessous sur deux
   lignes centrées : « BIO / SANTÉ », « BANQUE / CONSEIL », « SOIN /
   ENFANCE » · en bas : **« Ce ne sont pas des règles. / Ce sont des
   réflexes. »**
4. `sable chaud` · bloc centré optiquement · filet · **« Les suivre vous
   rend crédible. / Les casser vous rend mémorable. »** (78 px) · « Le
   problème, c'est de le faire sans le savoir. »
5. `crème` · **« Le même prix. Deux fonds. »** · deux rectangles de
   390 × 470 côte à côte, l'un jaune `#f9c33f` l'autre bleu `#2f7fc4`,
   portant **tous deux « 12 € » en blanc**, Inter 800 118 px — c'est tout
   l'intérêt : la même couleur de texte sur les deux, sinon la
   démonstration ne vaut rien · en bas : **« Le contraste se vérifie. / Il
   ne se devine pas. »**
6. `blanc` · **« Votre secteur en commentaire. »** (86 px) · texte · flèche
   corail · signature.

**Planche 7 — photographie.** La seule du carrousel. Sandra à son poste,
un nuancier Pantone déployé, le liège et le logo derrière elle. Recadrée
en 4:5. Un voile encre monte du bas sur 56 % de la hauteur, en rampe
puis plateau — sans le plateau, un titre posé aux deux tiers reste sur
une zone claire. Titre blanc, trois lignes : « Je choisis les couleurs
d'après votre métier, pas d'après la mode. » Puis « Sandra, Grafycom —
Perpignan. » en crème, et la signature.

### n° 2 · mardi 10 novembre · Carrousel 7 planches · Réglementation enseigne

1. `sable chaud` · surtitre « RÉGLEMENTATION » · filet · **« Votre enseigne
   a besoin / d'une autorisation. / Pas d'une déclaration. »** (74 px).
2. `blanc` · **« La confusion / la plus répandue »** · un trait corail
   horizontal de 620 px · « Déclaration préalable » (54 px, brun 600) puis
   « Autorisation préalable » (54 px, **violet 800**) — le contraste de
   graisse et de couleur porte l'opposition.
3. `crème` · bloc centré · **« Cerfa n° 16308\*01 »** en Playfair 92 px ·
   « À déposer en mairie, / en trois exemplaires. »
4. `blanc` · **« Au-delà de trois / dispositifs ? »** · « Le formulaire se
   remplit une seconde fois. » · en corail 600 : « Enseigne en bandeau ·
   caisson en drapeau · lettrage de vitrine · adhésif de porte. Ça fait
   déjà quatre. »
5. `crème` · **« Ce qui change / selon la commune »** · trois pastilles
   corail numérotées 1-2-3, texte à droite en Inter 600 40 px : « Le
   Règlement Local de Publicité », « Le Plan Local d'Urbanisme », « Le
   secteur patrimonial protégé ».
6. `sable chaud` · filet · **« À Perpignan, le centre ancien / est en
   secteur protégé. »** (68 px) · paragraphe sur l'avis des ABF.
7. `encre` · filet · **« Une enseigne se pense / en amont. »** (86 px,
   blanc) · « Pas après le logo. » (crème) · signature sable.

### n° 3 · jeudi 29 octobre · Dilemme A/B · 2 images

**La démonstration la plus stricte du cycle.** Deux images **rigoureusement
identiques**, la seconde étant la première **floutée par le programme**.

1. `crème` · **« Laquelle se lit / depuis le trottoir d'en face ? »**
   (72 px) · deux façades schématiques de 420 × 430, écartées de 60 px,
   portant **le même mot « MAISON »** au même corps (62 px) — à gauche en
   **Inter 400**, à droite en **Inter 800**. Sous chaque façade, un repère
   « A » / « B » en corail.
2. La **même image**, floutée d'un **flou gaussien de rayon 8 px** — ni
   plus ni moins : à 16 px les deux mots disparaissent et on ne prouve
   rien ; à 8 px le lettrage fin se dissout et le gras tient, ce qui est
   exactement le propos. Les lettres A et B sont retracées **après** le
   flou, nettes : ce sont des repères de lecture, pas des éléments de la
   scène. Titres ajoutés par-dessus : **« À vingt mètres, / ce n'est plus
   une typo. »** en haut, **« C'est une silhouette. »** en corail en bas.

### n° 4 · vendredi 6 novembre · REEL 24 s · 5 écrans 9:16 · RVB / CMJN

**La publication où le dessin bat le tournage le plus nettement.** Une
synthèse additive et une synthèse soustractive sont des schémas, pas des
scènes.

1. `sable chaud` · surtitre « REEL · 0-3 S » · **« Pourquoi ce n'est /
   jamais la même couleur. »** (98 px) · un **moniteur** dessiné
   (rectangle à coins arrondis encre, pied et socle) affichant un aplat
   bleu vif `#35a9dd`, légendé « à l'écran » ; en dessous une **feuille
   blanche posée à plat**, légèrement tournée, portant le **même bleu
   rendu terne**, légendée « imprimé ».
2. `crème` · **« RVB : de la lumière. »** (100 px) · un carré de 800 px,
   **fond noir**, trois disques rouge, vert, bleu purs, disposés en
   triangle, qui se recouvrent. **Les recouvrements sont calculés par
   addition de calques**, pas dessinés : jaune, cyan, magenta aux
   intersections deux à deux, **blanc pur au centre**. Lettres R, V, B en
   blanc sur chaque disque.
3. `crème` · **« CMJN : de l'encre. »** · le même carré, **fond blanc**,
   trois disques cyan, magenta, jaune, recouvrements calculés par
   **multiplication** : rouge, vert, bleu aux intersections,
   **presque-noir au centre**. Lettres C, M, J en encre.
4. `crème` · **« Le papier / change tout. »** · deux carrés de 420 px
   portant **la même valeur d'encre**. À gauche « mat » : couleur rabattue
   d'environ 26 % vers un gris clair, et un **grain** de petits points
   clairs et sombres. À droite « couché brillant » : couleur pleine, plus
   une **bande de lumière diagonale floue** en blanc translucide.
5. `encre` · le moniteur et la feuille à nouveau, en petit · filet ·
   **« Demandez un BAT. / Toujours. »** (98 px, blanc) · relance
   d'abonnement · signature sable.

> Le bleu « imprimé » n'est **pas** une conversion colorimétrique : pas de
> profil ICC. C'est une approximation assumée qui reproduit ce qu'on
> constate en quadri — **la couleur perd son éclat avant de perdre sa
> teinte**. Ne pas la présenter autrement.

### n° 4 bis · samedi 31 octobre · Carrousel 4 planches · Annonce du blog

1. `sable chaud` · surtitre « LE BLOG » · filet · **« Un nouvel article /
   chaque vendredi matin. »** (84 px) · « Sur grafycom.fr/blog. Gratuit,
   sans inscription. » · numéro 1/4.
2. `crème` · **« Ce qu'on y traite »** (80 px) · quatre puces corail :
   réglementation des enseignes et vitrines ; impression (couleurs,
   matières, fichiers) ; droits, propriété, fichiers sources ; coups de
   main saisonniers · « Des sujets vérifiés, pas des avis. » · 2/4.
3. `blanc` · **« Les quatre prochains »** · quatre puces violettes listant
   les **titres et dates réels** des quatre prochains articles, lus dans
   le dossier du blog et non recopiés · 3/4.
4. `encre` · filet · **« grafycom.fr/blog »** (86 px, blanc) · « Le lien
   est en bio. Activez les notifications pour ne rien rater. » · 4/4.

### n° 5 · lundi 2 novembre · Carrousel 6 planches · Typographie

1. `blanc` · surtitre « TYPOGRAPHIE » · bloc centré · **« Cette police est
   magnifique. »** (92 px) · « Et elle va vous coûter des clients. »
   (44 px, **corail 600**).
2. `crème` · **« Lisible sur une carte. / Illisible sur une bâche. »** ·
   « La même police, quatre supports, quatre résultats. » · deux façades
   schématiques de 400 × 380 portant « MAISON », l'une en Inter 400 40 px,
   l'autre en Inter 800 48 px.
3. `sable chaud` · bloc centré · filet · **« Trois questions / avant de
   choisir / une police. »** (86 px).
4. `blanc` · **« 1. À quelle distance / sera-t-elle lue ? »** · quatre
   lignes : carte de visite à bout de bras, menu à table le soir, enseigne
   à vingt mètres, puis « Ce ne sont pas les mêmes polices. »
5. `crème` · deux questions sur une seule planche : **« 2. Tient-elle / en
   tout petit ? »** en haut, **« 3. Avez-vous le droit / de l'utiliser ? »**
   à mi-hauteur, chacune avec son paragraphe.
6. `encre` · filet · **« Une identité, / c'est deux polices. »** (88 px,
   blanc) · « Une pour les titres, une pour le texte. Pas cinq. »

### n° 6 · mardi 3 novembre · Carrousel 6 planches · Droits et propriété

1. `crème` · surtitre « DROITS & PROPRIÉTÉ » · **« Qui possède / votre
   logo ? »** (110 px) · « La réponse surprend la plupart des chefs
   d'entreprise. »
2. `sable chaud` · filet · **« Vous l'avez payé. / Vous ne le possédez /
   pas forcément. »** (80 px) · paragraphe sur le transfert écrit.
3. `blanc` · **« Ce qui se cède, / et ce qui ne se cède pas »** · « Les
   droits patrimoniaux se cèdent : exploiter, reproduire, adapter. »
   (encre 600) puis « Le droit moral, jamais. Il reste à l'auteur, à
   vie. » (**corail 600**).
4. `crème` · **« Une cession se précise »** · trois pastilles **violettes**
   numérotées : « Pour quels supports. », « Sur quel territoire. », « Pour
   combien de temps. »
5. `blanc` · **« Pourquoi ça compte / un jour »** · trois lignes : vendre
   l'entreprise, déposer la marque, changer de prestataire.
6. `encre` · filet · **« Demandez votre / contrat de cession. »** (88 px) ·
   « S'il n'existe pas, c'est le moment de le faire. »

### n° 7 · jeudi 5 novembre · Quiz vrai/faux · 5 planches

1. `sable chaud` · pastille « QUIZ » corail · filet · **« 4 idées reçues /
   sur l'impression / et les enseignes. »** (84 px) · « Combien allez-vous
   rater ? »
2-5. Une affirmation par planche, fond alterné `blanc` / `crème`.
   Structure identique : l'affirmation entre guillemets français en
   Playfair 64 px en haut ; deux pastilles côte à côte, « VRAI » en bleu
   et « FAUX » en corail ; puis le verdict en Playfair 92 px — **violet
   si VRAI, corail si FAUX** — et l'explication en dessous.

   | | Affirmation | Verdict | Explication |
   |---|---|---|---|
   | 2 | « Une enseigne se déclare en mairie. » | FAUX | Elle s'autorise. Cerfa 16308\*01. |
   | 3 | « Un logo doit rester lisible en noir et blanc. » | VRAI | Sinon il échoue sur un tampon, une gravure, une broderie. |
   | 4 | « 300 DPI convient à toutes les bâches. » | FAUX | La résolution se calcule à la distance de lecture. |
   | 5 | « Une police gratuite est libre pour un usage commercial. » | FAUX | Presque jamais vérifié, et c'est celui qui coûte. |

### n° 8 · vendredi 30 octobre · REEL 22 s · 5 écrans 9:16 · Halloween

1. `encre` · surtitre « REEL · 0-3 S » en **orange** · **« Pourquoi
   Halloween / est orange / et noir. »** (96 px, blanc) · une
   **citrouille** dessinée au centre : cinq ellipses orange de largeurs
   décroissantes pour les quartiers, contour plus sombre, queue brune.
2. `crème` · **« Le contraste / maximal. »** (110 px) · deux bandeaux
   empilés de 900 × 290 portant **le même mot « ATTENTION »** en Inter 800
   92 px : fond encre / texte orange, puis fond orange / texte encre.
3. `crème` · **« La nature / l'utilise déjà. »** (104 px) · quatre
   pictogrammes légendés : un **ruban de chantier** (bandes à 45°, orange
   et encre), un **panneau de danger** (triangle orange, bord encre, point
   d'exclamation **tracé** et non écrit), une **guêpe** vue de dessus
   (tête et thorax encre, abdomen rayé orange/encre, ailes translucides,
   antennes), une **salamandre** (corps encre allongé, taches orange,
   pattes, queue pointue).
4. `crème` · **« Et pour / votre commerce ? »** (100 px) · **deux
   devantures identiques** empilées : la première neutre, légendée « toute
   l'année » ; la seconde avec un bandeau orange opaque portant des
   **silhouettes de citrouilles en encre**, légendée « en octobre ».
5. `violet` plein · filet · **« Une couleur / n'est jamais / neutre. »**
   (112 px, blanc) · relance d'abonnement · signature crème.

### n° 9 · lundi 9 novembre · Carrousel 6 planches · Un logo en petit

1. `crème` · surtitre « CONSEIL » · **« Votre logo tient-il / sur un
   stylo ? »** (96 px) · le logo fictif à **210 px de rayon**, et le même
   à **26 px** juste à côté, légendé « même logo, 8 mm » · mention en
   taupe : « Exercice de style — logo non commandé. »
2. `blanc` · **« On réduit, et on regarde. »** · le même logo à trois
   tailles décroissantes (rayons 180, 86, 44) alignés sur une ligne.
3. `sable chaud` · filet · **« Ce qui disparaît / en premier. »** (92 px) ·
   quatre puces corail : les dégradés, les ombres portées, les contours
   fins, le texte placé sous le symbole.
4. `crème` · **« Un logo doit exister / en une seule couleur. »** · le logo
   couleur à gauche, et à droite **le même en deux tons encre/crème**.
5. `crème` · **« Le même, cinq fois, / sans retouche. »** · le logo à 72 px
   posé cinq fois, légendé en violet : « carte de visite », « polo
   brodé », « flanc de camionnette », « panneau », « favicon ».
6. `encre` · filet · **« Faites le test / ce soir. »** (104 px, blanc) ·
   flèche corail.

### n° 10 · mardi 27 octobre · Carrousel 7 planches · L'enseigne à 17 h

1. `sable chaud` · la **rue au crépuscule** (section 5.2) occupant le haut
   jusqu'à y≈880 · un **bandeau violet plein en travers** à y=170, texte
   blanc Inter 800 54 px : **« Depuis dimanche, votre enseigne s'allume une
   heure plus tôt. »** · en dessous de la scène, une ligne de texte.
2. `crème` · surtitre « ENSEIGNE » · le chiffre **« 17 h »** en Inter 800
   **230 px bleu** · « C'est l'heure à laquelle votre devanture devient
   votre seul support de communication. » puis « Jusqu'en mars. »
3. `blanc` · **« Trois questions, / dans cet ordre. »** · trois puces
   corail numérotées : lisible, éclairée, autorisée.
4. `crème` · **« Éclairer une enseigne, / c'est la modifier. »** · un
   **encadré** crème rosé à filet **violet** sur le bord gauche, portant
   le conditionnel · en dessous, en taupe : « Le conditionnel est
   volontaire : ce point n'est pas vérifié à la source. »
5. `blanc` · **« Une autorisation, / pas une déclaration. »** · le
   **schéma de formulaire** (5.7) portant « Cerfa n° 16308\*01 » ·
   « Une déclaration, on la dépose. Une autorisation, on l'attend. »
6. `sable chaud` · une **horloge** tracée en corail (cercle, douze index,
   aiguilles) marquant **21 h 30** · filet · paragraphe sur l'extinction
   nocturne et le RLP.
7. `violet` plein · filet · **« Votre rue / en commentaire. »** (96 px,
   blanc) · flèche corail.

### n° 11 · jeudi 12 novembre · Dilemme A/B · 2 images · La place du prix

Deux cartes de restaurant **rigoureusement identiques** : mêmes six plats,
mêmes prix, même police, même corps, mêmes marges. **Le seul écart est la
place du prix.** Ajouter une couleur ou un cadre à l'une des deux la
ferait gagner pour une autre raison, et le post ne prouverait plus rien.

Structure commune : fond `crème`, « NOS PLATS » en Inter 800 26 px taupe
en haut, un filet sable foncé, puis six entrées espacées de 148 px — nom
du plat en Inter 600 40 px encre, description en Inter 400 30 px brun.

- **A** : le prix est **noyé dans la description**, à la suite du texte,
  séparé par un tiret. Pastille « A » bleue en haut à droite.
- **B** : le prix est **aligné à droite**, relié au nom par une **ligne de
  points** (petits disques sable foncé tous les 12 px). Pastille « B »
  corail.

Les six plats : Velouté de potimarron 9 € · Œuf parfait 12 € · Encornets
à la plancha 16 € · Épaule d'agneau confite 24 € · Rouget de roche 26 € ·
Tarte fine aux pommes 9 €.

### n° 12 · vendredi 13 novembre · REEL 23 s · 5 écrans 9:16 · Vitrophanie

1. `sable chaud` · surtitre « REEL · 0-3 S » · **« Vous avez un panneau /
   de 6 m². / Il est vide. »** (94 px) · une **devanture au trait**, vide ·
   sous elle, une **cote de plan** : un trait horizontal corail terminé par
   deux traits verticaux, légendé « 6 m² de verre, et rien dessus ».
2. `crème` · **« Dépoli : / on cache, on garde / la lumière. »** (86 px) ·
   la démonstration du dépoli (5.3) en grand : un rayonnage net au-dessus
   de la ligne, flouté et éclairci en dessous, légendes « verre nu » et
   « dépoli » incrustées.
3. `crème` · **« Microperforé : / plein dehors, / transparent dedans. »** ·
   une image **coupée en deux par un trait blanc**. À gauche, un dégradé
   violet → magenta → corail portant « SOLDES » en Inter 800 blanc,
   légendé « de la rue ». À droite, la **même surface vue de l'intérieur** :
   la rue en silhouettes claires, recouverte d'une **trame régulière de
   points** violet/magenta d'environ 7 px de pas, légendée « de
   l'intérieur ». Les deux légendes sont dans des pastilles encre.
4. `crème` · **« Lettres découpées : / sobre, et ça dure. »** · deux
   panneaux côte à côte montrant **le même texte « MAISON / BERNAT »** sur
   le même fond de vitrine. À gauche, le texte est posé sur un **pavé blanc
   opaque** (légende « pavé blanc ») ; à droite, les **lettres seules**,
   sans fond (légende « lettres découpées »).
5. `encre` · une devanture **éclairée** avec un bandeau d'adhésif violet ·
   filet · **« Et ça se décolle. »** (92 px, blanc) · relance
   d'abonnement.

### n° 13 · lundi 16 novembre · Carrousel 8 planches · Solaire 66

**La seule publication qui montre un vrai client, avec son accord.** Elle
utilise les couleurs de la marque Solaire 66 (`#10638b` et `#f5b32d`),
qui ne sont pas celles de Grafycom : c'est normal et voulu.

1. `blanc` · surtitre « RÉALISATION » centré · le logo Solaire 66 ·
   « Solaire 66 — identité livrée » en taupe.
2. `crème` · **« Ces deux couleurs / ne sont pas un goût. »** (92 px) ·
   leur origine, Canet-en-Roussillon.
3. `blanc` · **« Regardez le O. »** (110 px) · le détail du O-soleil.
4. `crème` · **« Une carte de visite / fait 85 millimètres. »** (88 px).
5. `crème` · **« À l'échelle exacte. »** (96 px) · la carte occupe 7 % de
   la largeur du panneau — **le rapport doit être exact**, c'est le sujet.
6. `crème` · **« En une seule couleur. »** (80 px) · le logo en
   monochrome.
7. `sable chaud` · **« Dessiné en grand. / Vérifié en petit. »** (92 px).

**Planche 8 — photographie.** Sandra de profil devant son écran, le mur
de liège et les nuanciers derrière. Recadrée en 4:5, voile encre sur
54 %. Titre blanc : « Trois semaines, et un logo qui tient sur un
stylo. » C'est la planche qui relie le travail livré à la personne qui
l'a livré — la seule publication du cycle qui montre un vrai client.

### n° 14 · mardi 17 novembre · Carrousel 6 planches · Loi Toubon

1. `sable chaud` · une **devanture éclairée** portant sur son bandeau
   principal **« SUNSET COFFEE »** et, sur un second bandeau juste en
   dessous, **« Best coffee in town — open all day »** en crème sur fond
   encre violacé — les deux doivent être **parfaitement lisibles**, c'est
   la condition pour que la publication fonctionne · bandeau **bleu** en
   travers : **« Votre slogan en anglais / est-il légal ? »** avec le
   sous-titre « La réponse est oui. Avec une condition. »
2. `crème` · surtitre « LA RÈGLE, EN UNE PHRASE » · **« Ce qui informe le
   client / doit être compréhensible / en français. »** (72 px) · filet ·
   « Ce qui vous nomme ne serait pas concerné de la même façon. »
3. `blanc` · **« Nommer, ou informer. »** · deux cartes à coins arrondis
   côte à côte, fond très pâle. À gauche, pastille **turquoise**
   « NOMMER », trois puces (nom de marque, dénomination, enseigne), et en
   bas « Ce serait votre identité. ». À droite, pastille **corail**
   « INFORMER », quatre puces (slogan, descriptif, promotion, mention de
   service), et « Là, le français serait attendu. » · mention en taupe sur
   le conditionnel.
4. `crème` · **« On ne retire rien. / On ajoute une ligne. »** · **la même
   devanture qu'en planche 1**, au pixel près, avec une seule chose
   changée : le second bandeau porte maintenant « Le meilleur café de la
   ville — ouvert toute la journée ». La démonstration est littéralement
   « on n'a rien retiré ».
5. `sable chaud` · filet · **« Et le catalan ? »** (100 px) · la réponse.
6. `blanc` · **« Vous avez un slogan / en anglais ? »** (86 px) · flèche.

### n° 15 · jeudi 19 novembre · Quiz 4 choix · 5 planches · Les matières

1. `sable chaud` · surtitre « QUIZ » · **« Quatre supports. / Vous en
   reconnaissez / combien ? »** (72 px) · les **quatre matières en coupe**
   (5.3) en grille 2 × 2, carrés de 290 px, chacune portant une petite
   pastille corail numérotée de 1 à 4.
2-4. `crème` · une matière en plein cadre (520 px, centrée), pastille
   « N° 1 / 2 / 3 » en haut à gauche, et **quatre réponses possibles** dans
   des bandeaux blancs à coins arrondis empilés :
   - n° 1, l'alu : alu composite · plexi · PVC expansé · inox brossé
   - n° 2, le plexi : plexi coulé · verre · polycarbonate · résine
   - n° 3, le dépoli : verre sablé · adhésif dépoli · film solaire · peinture
5. `sable chaud` · filet · **« Les quatre réponses. »** (78 px) · les
   quatre matières en vignettes de 150 px alignées verticalement, chacune
   avec son nom en Inter 600 40 px et son usage en 32 px brun · flèche
   corail et « Votre score en commentaire. »

### n° 16 · samedi 21 novembre · REEL 25 s · 5 écrans 9:16 · Fin d'année

1. `crème` · surtitre « REEL · 0-3 S » · **« Pour Noël, / vous êtes déjà /
   en retard. »** (100 px) · un **calendrier en bande continue** du
   21 novembre au 31 décembre — pas deux mois côte à côte, **une seule
   grille de six semaines**, sept colonnes, cases à coins arrondis. Les
   jours hors période sont en contour seul ; le **24 décembre est en encre
   plein, chiffre blanc**. Le premier de chaque mois porte son abréviation.
   · « Six semaines. C'est tout ce qui reste. »
2. `sable chaud` · **« Une carte imprimée / se garde. / Un mail se
   ferme. »** (86 px) · deux cartes posées à plat, légèrement tournées
   (+9° et −7°), avec gaufrage ; **celle qui porte le texte manuscrit
   « Bonne année » en Caveat est dessinée par-dessus l'autre**.
3. `crème` · **« Un bandeau suffit. / Pas un packaging / entier. »** · un
   **paquet kraft** en léger trois-quarts : face avant, face du dessus en
   biais, face latérale plus sombre, deux plis verticaux, un **bandeau
   violet à flocons** en travers et une **pastille ronde corail** au logo.
4. `blanc` · **« Création · BAT · / Livraison »** (92 px) · trois jalons
   verticaux reliés par un trait : disque violet « création / mi-novembre »,
   disque bleu « bon à tirer / fin novembre », disque corail « livraison /
   début décembre ».
5. `encre` · une **table vue de dessus** : un plateau brun foncé rayé de
   lignes de bois, deux cartes et le paquet posés dessus · filet ·
   **« Décembre se décide / en novembre. »** (78 px) · relance
   d'abonnement.

### n° 17 · lundi 23 novembre · Carrousel 6 planches · Rétroplanning

1. `sable chaud` · surtitre « FIN D'ANNÉE » · filet · **« Vos cartes de
   vœux / de Noël se décident / cette semaine. »** (86 px) · « Pas en
   décembre. Voici pourquoi. » · flèche · 1/6.
2. `blanc` · **« On compte à rebours. »** · **une frise qui se lit de
   DROITE à GAUCHE** : quatre disques corail de 92 px numérotés 4, 3, 2, 1
   placés aux abscisses 880, 640, 400, 160, reliés par des **flèches
   pointant vers la gauche**. Sous chaque disque, l'étape et son délai :
   « Réception / 24 déc. », « Impression / 8 jours », « Bon à tirer /
   4 jours », « Création / 10 jours ». Au-dessus, deux repères en taupe :
   « aujourd'hui » à gauche, « la boîte aux lettres » à droite.
   **Le sens de lecture est tout le propos** : une frise dessinée dans
   l'autre sens dirait le contraire du texte. · 2/6.
3. `crème` · **« Les trois étapes / qu'on oublie de compter »** · trois
   lignes précédées d'un **tiret violet épais** : « Le texte à écrire. »,
   « Le fichier à préparer. », « Les adresses à réunir. » · 3/6.
4. `sable chaud` · filet · **« Le bon à tirer n'est / pas une
   formalité. »** (82 px) · 4/6.
5. `blanc` · **« Tout part chez le même / imprimeur, au même moment. »** ·
   quatre **pictogrammes au trait violet**, épaisseur 5 px, alignés et
   légendés : une carte (rectangle + deux traits), une étiquette (pentagone
   avec œillet), un sachet (rectangle + anse en arc), une vitrine
   (rectangle + deux diagonales) · deux phrases opposées, l'une en encre
   l'autre en corail · 5/6.
6. `crème` · filet · **« Dites-moi ce que vous / voulez imprimer / pour les
   fêtes. »** (80 px) · flèche · 6/6.

### n° 18 · mardi 24 novembre · Carrousel 7 planches · Signalétique de tri

1. `crème` · le **sachet cadeau** complet (5.5) · bandeau **violet** en
   travers : **« Votre bel emballage de fête / a une mention à porter. »**
2. `blanc` · **« Il lui faut cette place. »** (72 px) · **le même sachet,
   au trait** — contours bruns sur blanc, bandeau remplacé par un aplat
   violet très pâle — avec un **rectangle vide cerné de corail** posé en
   bas à droite, légendé « cette place » juste en dessous.
3. `blanc` · surtitre « LE PRINCIPE » · **« Un emballage destiné / au grand
   public devrait / porter une signalétique / de tri. »** (64 px) · en bas,
   en **bleu 30 px** : « Cadre généralement cité : loi AGEC de 2020. À
   confirmer auprès de votre éco-organisme. »
4. `crème` · **« Dans quel ordre ? »** · deux cartes à coins arrondis. À
   gauche, sans contour, le texte « On dessine, puis on cherche où la
   mettre. » **barré ligne par ligne** d'un trait corail — un seul trait au
   milieu du bloc ne barrerait que la ligne du milieu. À droite, **contour
   violet**, « On réserve la zone, puis on dessine autour. »
5. `sable chaud` · filet · **« Un emballage dessiné / sans cette place /
   se refait. »** (84 px).
6. `blanc` · **« Trois interlocuteurs, / dans cet ordre. »** · trois puces
   corail numérotées : éco-organisme, imprimeur, graphiste.
7. `encre` · filet · **« Vous préparez / un emballage / pour les fêtes ? »**
   (92 px, blanc) · flèche.

### n° 19 · jeudi 26 novembre · Dilemme A/B · 2 images · Cartes de vœux

Deux cartes **au même format, sur le même fond, avec la même marque**
(le logo fictif). Le seul écart est **le texte et la place du logo**.

Structure commune : fond `crème`, une carte blanche de 700 × 500 posée à
plat à partir de (190, 300), avec une **ombre portée floue** ; sous la
carte, « Laquelle vous donne envie d'y retourner ? » en Inter 600 40 px.

- **A** (pastille bleue) : le logo **en grand au centre haut** (rayon
  86 px), et en dessous la formule type « Joyeuses fêtes et bonne année »
  en Inter 600 38 px.
- **B** (pastille violette) : un **mot manuscrit en Caveat 54 px**,
  centré, sur plusieurs lignes — « Merci d'avoir poussé notre porte cette
  année. On rouvre le 4 janvier, et on vous garde la table du fond. » — et
  le logo **petit, en bas** (rayon 40 px).

### n° 20 · vendredi 27 novembre · REEL 24 s · 5 écrans 9:16 · Les matières

> **C'est ici que le dessin perd le plus.** Une dorure, un gaufrage, un
> papier qui ondule se *sentent*. Si un seul visuel du cycle mérite une
> vraie photographie en lumière rasante, ou un rendu 3D soigné, c'est
> celui-ci. Les écrans se remplacent **un par un**.

1. `sable chaud` · surtitre « REEL · 0-3 S » · **« Ce que vos clients /
   sentent / avant de lire. »** (100 px) · un **gaufrage** en grand
   (720 px) : un motif circulaire rendu par deux contours décalés, un
   blanc vers le haut-gauche, un taupe vers le bas-droite.
2. `crème` · **« 120 g / 350 g »** (110 px) · deux feuilles **vues sur la
   tranche**, pincées à gauche par un mors taupe et s'étendant vers la
   droite. La première **s'affaisse en courbe** sur 300 px, étiquetée
   « 120 g » en corail ; la seconde reste **droite**, étiquetée « 350 g »
   en bleu.
3. `crème` · **« Le gaufrage : / du relief, / pas de l'encre. »** (92 px) ·
   **deux carrés de 420 px issus du même tracé**, un seul paramètre
   changé : à gauche « lumière de côté », décalage de 3 % et ombre
   marquée ; à droite « lumière de face », **décalage nul et ombre
   quasi nulle** — le motif doit presque disparaître. Ne pas tricher en
   en laissant un peu « pour qu'on voie ».
4. `crème` · **« La dorure : / une feuille, / pas du jaune. »** · deux
   cartes crème portant un **filet horizontal**. À gauche « sous un
   angle » : le filet est un dégradé brun → orange → jaune → **blanc** →
   jaune → brun, avec un halo lumineux. À droite « sous un autre » : le
   même filet en **brun sombre uni**, plus sombre que le papier.
5. `encre` · les trois matières en vignettes de 280 px — gaufrage, dorure,
   et une **carte épaisse vue de trois quarts** montrant sa tranche,
   légendée « 350 g » · filet · **« Choisissez la matière / avant le
   dessin. »** (84 px, blanc) · relance d'abonnement.

### n° 21 · lundi 30 novembre · Carrousel 7 planches · La vitrine du trottoir

1. `crème` · une **devanture éclairée vue de nuit depuis le trottoir d'en
   face** : ciel en dégradé encre → bleu → violet sur le tiers haut, le
   trottoir opposé, la devanture au centre sur 78 % de la largeur avec son
   enseigne « MAISON BERNAT », un **halo jaune** autour, puis la chaussée
   au premier plan avec sa bordure, ses **bandes blanches** et le **reflet
   de la vitrine sur le bitume** · bandeau **violet** : **« Votre vitrine
   de Noël est faite / pour celui qui passe. Pas pour / celui qui est
   dedans. »**
2. `blanc` · **« La hauteur des yeux. »** (76 px) · la devanture **au
   trait**, avec une **échelle en mètres** tracée à gauche (graduations 0,
   1, 2, 3 m) et une **bande corail translucide entre 1,40 m et 1,70 m**
   bordée de deux traits corail qui débordent du cadre.
3. `crème` · **« Couvrir, ou laisser voir. »** (70 px) · deux devantures de
   430 px côte à côte, **toutes deux éclairées** : à gauche le verre
   couvert à 96 % par un décor **corail opaque** à sapins, légendée « le
   verre couvert » ; à droite un simple **bandeau** de décor et du verre
   libre, légendée « un bandeau, du verre libre ».
4. `sable chaud` · filet · **« À 17 h en décembre, / il fait nuit. »**
   (88 px) · une devanture **éteinte** : verre bleu très sombre, silhouettes
   de la rue reflétées, traînées de lumière diagonales en transparence, un
   lampadaire reflété.
5. `blanc` · **« Un texte sur verre se lit / contre ce qu'il y a
   derrière. »** (58 px) · deux panneaux portant **exactement le même
   texte** « OUVERT / le dimanche » en blanc. À gauche, devant un
   **rayonnage encombré** de boîtes colorées : illisible. À droite, devant
   un **panneau uni sombre** : parfaitement lisible.
6. `crème` · **« La même vitrine, / trois reculs. »** (74 px) · la **même
   devanture au trait, redessinée à trois échelles** (44 %, 27 %, 15 % de
   la largeur utile), **alignées sur le sol** et non sur leur milieu,
   légendées « 2 m », « 8 m », « 25 m » en corail. Chacune porte le même
   lettrage « MAISON BERNAT / 9 h – 19 h ». Aucune photographie ne peut
   faire cela en une image : il faudrait trois prises de vue au même
   instant.
7. `crème` · **« Photographiez votre vitrine / depuis le trottoir d'en
   face. »** (60 px) · flèche.

### n° 22 · mardi 1er décembre · Carrousel 6 planches · Enseigne ou publicité

1. `crème` · une **devanture éclairée** portant **deux adhésifs** : une
   pastille **violette « Joyeuses fêtes »** en haut à gauche du vitrage, et
   une pastille **bleue « -30 % »** plus bas à droite · bandeau violet :
   **« Un sticker de Noël sur votre vitrine : / enseigne, publicité, ou
   rien du tout ? »**
2. `crème rosé` · **« Ce n'est pas / du vocabulaire. »** (76 px) · deux
   cartes blanches à **contour de 5 px**, l'une **violette** l'autre
   **bleue**. Violette : « Enseigne » en 52 px, « elle dit qui vous êtes et
   où. », puis en bas « On l'autorise. ». Bleue : « Publicité », « elle dit
   ce que vous vendez à quel prix. », « On la déclare. »
3. `crème` · **« L'un décore. / L'autre vend. »** (86 px) · deux **bulles**
   à coins très arrondis empilées : « Joyeuses fêtes » sur fond violet,
   « -30 % jusqu'au 24 » sur fond bleu, texte blanc Inter 800 54 px.
4. `bleu` plein · filet · **« C'est votre commune / qui tranche. »**
   (88 px, blanc) · le RLP, le PLU, et « À trois kilomètres de distance, la
   réponse change. »
5. `blanc` · **« Et surtout : / pas le 14798\*01. »** (72 px) · le **schéma
   de formulaire** portant « Cerfa n° 16308\*01 » · en dessous, un
   **encadré à filet corail** : le 14798\*01 est périmé depuis le
   1er juillet 2026, un dossier déposé avec est considéré comme incomplet,
   et il remonte encore dans les recherches.
6. `violet` plein · filet · **« Dites-moi votre commune / en
   commentaire. »** (72 px, blanc) · flèche.

### n° 23 · jeudi 3 décembre · Quiz · 6 planches · Impressions de fin d'année

1. `sable chaud` · surtitre « QUIZ » · filet · **« 4 idées reçues / sur vos
   impressions / de fin d'année. »** (86 px) · « Vous en avez combien de
   justes ? » · flèche · 1/6.
2. `crème` · **« Vrai ou faux ? »** · les quatre affirmations en puces
   **bleues numérotées**, texte bleu 36 px · « Répondez en commentaire
   avant de swiper. » en corail · 2/6.
3-6. `blanc` · une réponse par planche. Le libellé court en taupe en haut
   (« 1. La dorure », « 2. La signalétique de tri », « 3. Les fonds
   perdus », « 4. Mi-novembre »), puis le verdict en Playfair **150 px**
   (ou 96 px s'il est long), **corail pour FAUX, violet pour
   « VRAI… mais »**, puis l'explication en 44 px encre. La planche 6 porte
   en plus la flèche et « Votre score en commentaire. »

### n° 24 · samedi 5 décembre · REEL 30 s · 6 écrans 9:16 · Refaire son logo

1. `sable chaud` · surtitre « REEL · 0-3 S » · **« Non, / pas en
   janvier. »** (116 px) · **deux pages de calendrier mural** côte à côte,
   400 × 520, rigoureusement identiques sauf le nom du mois : « DÉCEMBRE
   2026 » sur bandeau **bleu**, « JANVIER 2027 » sur bandeau **violet**.
   Chacune a sa **spirale** (six anneaux en haut) et sa grille de jours
   réelle · flèche corail entre les deux.
2. `crème` · **« Changer par calendrier, / ce n'est pas changer / par
   besoin. »** (80 px) · **le même logo fictif, deux fois**, à 190 px de
   rayon, avec un écart **minuscule** sur l'épaisseur des anneaux (environ
   4 %). Légendés « version actuelle » et « « nouvelle » version ». S'ils
   étaient rigoureusement identiques on croirait à une erreur de montage ;
   s'ils différaient vraiment, la démonstration tomberait.
3. `blanc` · **« Trois questions, / avant de redessiner. »** (88 px) ·
   trois cartes crème à coins arrondis, chacune avec une pastille corail
   numérotée et une question **manuscrite en Caveat 62 px** : « Lisible
   partout ? », « Fichiers en main ? », « Dit-il ce que vous vendez
   aujourd'hui ? »
4. `crème` · **« Deux « oui », / un « non » : / on ajuste. »** (96 px) ·
   **trois supports alignés** portant le même logo : une carte de visite
   (rectangle crème), un panneau (rectangle sable sur deux pieds), un polo
   (silhouette bleue avec manches et col en V). Sur le polo, le logo est
   **réellement dégradé** : rendu net puis flouté et **réduit en paliers**,
   comme une aiguille qui ne sait pas rendre un contour fin. Il ne doit pas
   être « dessiné flou » — on doit voir disparaître ce qui disparaît en
   broderie.
5. `encre` · les **trois mêmes supports**, logo net partout, légendes en
   sable · filet · **« Un bilan, / pas une résolution. »** (92 px, blanc) ·
   relance d'abonnement.

---

## 7. Les six reels : montage et vidéo

Les six reels sont livrés en **écrans finis** 1080 × 1920, pas en rushes.
Le montage par défaut consiste à les enchaîner sur la voix off, au rythme
indiqué par le surtitre de chaque écran.

| N° | Date | Durée | Écrans | Découpage |
|---|---|---|---|---|
| 4 | ven 30 oct | 24 s | 5 | 0-3 · 3-9 · 9-15 · 15-20 · 20-24 |
| 8 | ven 6 nov | 22 s | 5 | 0-3 · 3-9 · 9-15 · 15-19 · 19-22 |
| 12 | ven 13 nov | 23 s | 5 | 0-3 · 3-8 · 8-13 · 13-18 · 18-23 |
| 16 | sam 21 nov | 25 s | 5 | 0-3 · 3-9 · 9-15 · 15-21 · 21-25 |
| 20 | ven 27 nov | 24 s | 5 | 0-3 · 3-8 · 8-14 · 14-19 · 19-24 |
| 24 | sam 5 déc | 26 s | 5 | 0-3 · 3-9 · 9-15 · 15-21 · 21-26 |

**Les six MP4 sont livrés montés**, en 1080 × 1920, H.264, 30 i/s, avec
un fondu enchaîné de 0,35 s entre les écrans et la durée exacte du
découpage. Ils sont produits par `reseaux/reels.py`, qui lit les chronos
et le texte de la voix dans le cahier des charges — rien n'y est recopié.
Ils sortent **muets** tant qu'aucune clé de synthèse vocale n'est posée,
et le script de la voix accompagne chaque fichier en `.txt`.

**La voix off** est écrite intégralement dans `instagram-facebook.md`,
colonne « Script voix off » ou « Voix off » de chaque découpage. Voix
féminine française, calme et professionnelle, articulation nette, **pas
d'intonation commerciale** : le texte est un conseil, pas une offre. Deux
exceptions de ton, notées dans le document : le n° 16 se permet d'être
affectif sans devenir publicitaire, le n° 24 est plus grave et plus lent
— c'est un reel d'avis, pas de pédagogie.

**Ce qu'un modèle vidéo peut apporter, par ordre de rendement :**

1. **Les transitions entre écrans.** Un fondu enchaîné ou un glissement
   latéral de 0,3 s vaut mieux qu'une coupe franche.
2. **L'apparition progressive des éléments** à l'intérieur d'un écran :
   les trois jalons du n° 16 qui s'allument un par un, les quatre
   pictogrammes du n° 8 qui entrent en cascade, les cases du calendrier
   qui se remplissent.
3. **Les quatre animations qui ont un vrai sens pédagogique**, et que le
   fixe rend mal :
   - **n° 4, écrans 2 et 3** : les trois disques RVB qui **arrivent un par
     un et se superposent** jusqu'au blanc central, puis les trois disques
     CMJ jusqu'au presque-noir. C'est l'animation la plus utile du cycle.
   - **n° 3** : le passage **net → flou** sur la même image, en 1,5 s. Le
     flou est déjà la démonstration ; le voir arriver la rend évidente.
   - **n° 20, écran 3** : la lumière qui **bascule de rasante à frontale**
     sur le gaufrage, et le relief qui s'efface.
   - **n° 21, écran 6** : la devanture qui **recule** de 2 m à 25 m, les
     horaires disparaissant avant le nom.
4. **Un mouvement d'ambiance très discret** sur les écrans d'ouverture :
   une lente respiration sur la rue au crépuscule, les enseignes dont le
   halo pulse imperceptiblement.

**Ce qu'il ne faut pas demander à un modèle vidéo :** régénérer la scène.
Un modèle qui « réinterprète » la rue au crépuscule produira des enseignes
en pseudo-lettres (règle 1.2) et une rue qui n'est pas Perpignan. Partir
de l'image, toujours.

---

## 8. Les 44 écrans de stories

Format 9:16. Ils sont **tous typographiques**, volontairement : un écran
propre vaut mieux qu'un écran qui attend une photo.

**Le gabarit est unique**, ce qui fait leur cohérence :

1. Fond `sable chaud`, `crème` ou `encre`.
2. **Surtitre** à y = 300, en taupe (ou sable sur fond encre).
3. **Filet dégradé** juste en dessous.
4. **Titre** en Playfair **76 px**, encre (ou blanc sur fond encre).
5. Puis, selon l'écran, l'un ou l'autre :
   - un **cartouche « sticker »** à y = 1160 : un rectangle blanc à coins
     arrondis (rayon 28), portant en haut un libellé en Inter 600 24 px
     capitales brun — « SONDAGE », « QUIZ », « BOÎTE À QUESTIONS »,
     « LIEN », « CURSEUR EMOJI », « MENTION DU POST » — puis une à cinq
     lignes en Inter 600 30 px encre, espacées de 44 px. **C'est une
     imitation de sticker Instagram : le vrai sticker interactif se pose
     par-dessus dans l'application au moment de publier.**
   - ou simplement un **paragraphe** en Inter 400 42 px.
6. **Signature** en bas à gauche.

Les 44 codes, dans l'ordre de publication :

`S1-A` `S1-B1` `S1-B2` `S1-C` `S1-D1` `S1-D2` `S1-E` · `S2-A` `S2-B`
`S2-C` `S2-D1` `S2-D2` `S2-E` `S2-F` · `S3-A` `S3-B1` `S3-B2` `S3-C`
`S3-D1` `S3-D2` `S3-E1` `S3-E2` · `S4-A` `S4-B1` `S4-B2` `S4-C` `S4-D1`
`S4-D2` `S4-E` `S4-F` · `S5-A` `S5-B1` `S5-B2` `S5-C1` `S5-C2` `S5-D`
`S5-E` · `S6-A` `S6-B1` `S6-B2` `S6-C1` `S6-C2` `S6-D` `S6-E`

Le suffixe `1` / `2` marque une **paire question / réponse** : l'écran
posant un sondage ou un quiz, puis celui qui donne la réponse quelques
heures plus tard. Les deux doivent se ressembler assez pour qu'on fasse le
lien, et différer assez pour qu'on voie que c'est la suite — le surtitre
du second est « La réponse ».

Le texte exact de chacun est dans `stories.md`, écran par écran, avec le
type de sticker à poser dans l'application.

---

## 9. Les sept illustrations d'articles

Format **1200 × 630**, pour l'aperçu quand on partage le lien. Ce sont des
**compositions géométriques dans la charte**, pas des photographies et pas
des pictogrammes : des formes larges, peu nombreuses, lisibles en
vignette. Aucun texte — le titre de l'article s'affiche à côté.

| Article | Composition |
|---|---|
| L'autorisation d'enseigne | une façade schématique et son bandeau |
| Couleurs imprimées / écran | les disques de synthèse, décalés |
| Qui possède votre logo | des formes qui se recouvrent partiellement |
| Habiller sa vitrine | un vitrage et ses trois familles d'habillage |
| Le rétroplanning | une frise de jalons |
| La vitrine du trottoir | une devanture vue de loin, de nuit |
| Refaire son logo | deux marques presque identiques |

---

## 10. Recette : ce qu'il faut vérifier à la livraison

À passer sur **chaque** visuel reçu, dans cet ordre. Les trois premiers
points sont éliminatoires.

1. **Agrandir chaque texte visible dans l'image** — enseigne, affiche,
   étiquette, formulaire. Un seul caractère approximatif, une seule
   pseudo-lettre : refusé. Voir 1.2.
2. **Vérifier le pseudo** : `@grafycom.graphiste`, avec le point.
3. **Vérifier qu'aucun commerce réel n'est identifiable**, et qu'aucun
   visage ni aucune main n'apparaît.
4. Prélever les couleurs à la pipette et les comparer aux hex de la
   section 2. Une teinte approchante n'est pas la teinte.
5. Vérifier les **espaces insécables** : aucun `?`, `!`, `;`, `:` seul en
   début de ligne, aucun `17 h 30` coupé en deux.
6. Vérifier qu'aucun bloc de texte ne descend **sous la ligne de
   signature** (y = 1238 en 4:5, y = 1808 en 9:16).
7. Sur les **démonstrations par paires** — n° 3, 4, 11, 14, 19, 20, 21,
   24 — vérifier que **le seul écart entre les deux images est celui qu'on
   démontre**. C'est la vérification la plus importante après la n° 1 :
   une paire dont les deux membres diffèrent par autre chose ne prouve
   rien, et une démonstration fausse sur un compte de graphiste coûte plus
   cher qu'une image moyenne.
8. Vérifier le **sens de lecture** de la frise du n° 17 : de droite à
   gauche. Dans l'autre sens elle dit le contraire du texte.
9. Vérifier que l'**astérisque du Cerfa** sort entière : `16308*01`.
10. Relire le visuel à **la taille d'une vignette de feed** (environ
    320 px de large). Si le titre ne se lit plus, le corps est trop petit.

---

## 11. Où sont les fichiers

| Quoi | Où |
|---|---|
| Les 133 planches de publications | `reseaux/visuels/AAAA-MM-JJ-sujet/` — **un dossier par publication, nommé à la date réelle de parution** |
| Les 44 écrans de stories | `reseaux/visuels/stories/` — nommés par leur code |
| Les textes exacts des publications | `reseaux/propositions/a-valider/instagram-facebook.md` |
| Les textes exacts des stories | `reseaux/propositions/a-valider/stories.md` |
| Une planche-contact A4 de tout | `python3 reseaux/planche-contact.py` |
| Le script qui produit tout | `reseaux/visuels.py` — `--liste`, `--tout` |

---

*Brief rédigé le 18 octobre 2026. En cas de contradiction entre ce
document et une planche livrée, c'est la planche qui fait foi.*

**Écran 6 — photographie.** Format 9:16. Sandra de face, souriante,
nuancier en main. Voile encre sur 46 %. Titre blanc, deux lignes : « Si
votre logo vous gêne, parlons-en. » Relance d'abonnement et signature en
pied. C'est la boucle du cycle : la première publication s'ouvrait sur
la même personne, un nuancier à la main.
