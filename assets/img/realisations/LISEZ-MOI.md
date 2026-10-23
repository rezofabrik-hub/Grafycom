# Les réalisations du portfolio

Deux visuels, tirés du portfolio de Sandra, au format **4/3** et en WebP.

| Fichier | Projet | Ce qu'il montre |
|---|---|---|
| `o-fait-maison.webp` | Ô Fait Maison | Enseigne de devanture d'un salon de thé |
| `mia-beauty.webp` | Mia Beauty | Livret de formation ouvert |

## En ajouter une

1. Déposer le fichier ici, recadré en 4/3, en WebP, 900 px de large environ.
2. Ajouter un appel à `reaz()` dans `generateurs/p_realisations.py`, avec sa
   catégorie, le nom du projet et une phrase sur ce qu'il fallait résoudre.
3. Régénérer la page.

## Une précaution qui n'est pas une formalité

Ces projets appartiennent à des clients identifiables. Les montrer suppose
leur accord — le contrat cède les droits sur la création, il ne donne pas
celui de s'en servir de vitrine. Un message suffit, et c'est rarement
refusé ; mais un client qui se découvre en ligne sans avoir été prévenu est
un client perdu.

## Provenance — précisé le 12 octobre, revu le 23

**La galerie mélange désormais deux provenances**, et c'est ce qui a
changé le 23 octobre.

| Provenance | Projets |
|---|---|
| Commandes reçues par **Grafycom** | Solaire 66, Sweet Dream, Krusty, Big Food, Social Miroir |
| Menés **au sein d'une structure précédente** | Ô Fait Maison, Mia Beauty |

La mention de provenance se pose donc **sur la fiche** et non en chapeau
de page. Elle y était, en une phrase sous le titre : depuis que cinq
fiches sur sept sont des commandes Grafycom, cette phrase affirmait le
contraire de la vérité pour la majorité de la page. `reaz(..., avant=True)`
la rend fiche par fiche dans `generateurs/p_realisations.py`.

Les projets ci-dessous sont ceux de la structure précédente. L'accord
obtenu porte sur le fait de dire que Sandra a créé les visuels, et il ne
couvre pas tout :

| Projet | Accord | Réserve |
|---|---|---|
| Ô Fait Maison | oui | l'entreprise a fermé |
| Mia Beauty | oui | — |
| ~~Casa Aldo~~ | **retiré le 12 octobre** | l'accord porte sur le logo, l'image montrait l'enseigne |
| ~~Alliance Peintures~~ | **retirés le 12 octobre**, faute d'accord confirmé | |
| ~~Cap Loisirs~~ | **retiré le 23 octobre**, accord jamais confirmé. Fichier supprimé, pas seulement déréférencé | |
| ~~Pano Perpignan~~ | une image déréférencée reste servie à son adresse | |

**Un travail mené pour le compte d'une autre structure ne se présente pas
comme une commande reçue par Grafycom.** La formule à employer, et la
seule que l'accord autorise :

> Création de Sandra, fondatrice de Grafycom — projet réalisé au sein
> d'une précédente structure.

C'est une précaution de fond, pas de forme : un prospect qui découvre que
« ce client » était celui d'un ancien employeur perd confiance d'un coup,
et ça se sait vite dans un département.

## Casa Aldo — classé le 12 octobre, ne pas rouvrir

**Le logo vectoriel n'est plus en possession de Laurent.** La seule source
restante était la photo de l'enseigne, où le logo mesure 205 × 235 px, de
biais et compressé. Il n'y a donc aucun moyen d'en faire un visuel propre,
et Casa Aldo ne revient pas sur le site.

Ce qui suit est conservé pour mémoire : si le fichier réapparaissait un
jour — chez l'ancien employeur, chez le client, dans une sauvegarde —
voici ce qui serait utilisable.

### Ce qu'il aurait fallu

L'accord porte sur le **logo seul**, et `casa-aldo.webp` montrait
l'enseigne ronde fabriquée : le visuel dépassait l'accord. Il a été retiré
et son fichier supprimé.

**Le reconstruire depuis cette photo ne marche pas.** Mesure faite : le
logo y occupait **205 × 235 px**, vu de biais, dans une image déjà
compressée. Trois tentatives de détourage l'ont confirmé — le cadrage se
règle, pas la résolution. Agrandi pour une publication de 1080 px, le
rouge part en taches et les contours se délitent.

**Ce qu'il faut :** le logo source, dans l'un de ces formats, par ordre de
préférence —

1. un **PDF vectoriel** ou un `.ai` / `.eps` — comme pour Solaire 66 ;
2. un **PNG à fond transparent**, 2000 px de large au minimum ;
3. à défaut, un JPEG du logo seul, le plus grand disponible.

Avec le vectoriel, le mock-up se fait à n'importe quelle taille, en
monochrome aussi, et il tient en impression.

> Le logo contient le **visage du restaurateur**, dessiné d'après sa
> photo. C'est le logo public du commerce, donc son usage en portfolio
> suit l'accord déjà obtenu — mais c'est une raison de plus pour ne jamais
> le publier recadré ou retouché.

## Toutes les images qui montrent un travail client

Relevé complet du 12 octobre, pour que la question ne se repose pas. Les
visuels ne sont pas tous dans ce dossier : il y en a aussi dans
`assets/img/secteurs/` et `assets/img/prestations/`.

| Image | Projet | Statut |
|---|---|---|
| `realisations/o-fait-maison.webp` | Ô Fait Maison | accord — entreprise fermée |
| `realisations/mia-beauty.webp` | Mia Beauty | accord |
| `secteurs/secteur-restauration.webp` | Ô Fait Maison | accord |
| `secteurs/secteur-liberales.webp` | Mia Beauty | accord |
| `prestations/presta-identite.webp` | Crazy Frenchy | **logo créé par Laurent pour un projet de site web à lui.** Pas un client. Se montre librement, jamais comme une commande |
| `prestations/presta-menus.webp` | Pizza Fry | **accord confirmé le 13 octobre** |
| `prestations/presta-signaletique.webp` | Le Cayrou | entreprise fermée |
| `prestations/presta-digital.jpg`, `presta-projet.jpg` | — | illustrations, aucun client |

### Retirées le 12 octobre

Alliance Peintures, Cap Loisirs, Pano Perpignan et Casa Aldo. Fichiers
supprimés, pas seulement déréférencés : une image déréférencée reste
servie à son adresse.

### Deux nuances qui ne sont pas des blocages

**Une entreprise fermée ne cède pas ses droits en fermant.** Ils passent à
son ancien dirigeant. En pratique, plus personne ne s'y oppose et le
risque est faible — mais ce n'est pas la même chose qu'un accord, et il
vaut mieux le savoir que le croire.

**Un projet personnel ne se présente pas comme une commande.**
`presta-identite.webp` est le logo que Laurent a créé pour un projet de
site web à lui — vérifié le 12 octobre. Il illustre la prestation « logo »
sur la page prestations, ce qui est honnête : c'est un travail, montré
comme un travail. Mais il n'a rien à faire sur la page réalisations sous
la ligne d'attribution de la page réalisations, et son texte alternatif
ne parle plus d'un « hall d'entreprise » — le mur est une présentation,
pas un lieu réel.

## La galerie au 23 octobre

Cap Loisirs est retiré, faute d'accord confirmé — comme Alliance
Peintures et Pano Perpignan l'avaient été le 12 octobre. **La page ne
montre plus que des projets dont l'accord est acquis.**

Quatre réalisations récentes les remplacent, toutes avec accord écrit
donné le 22 octobre :

| Projet | Vignette | Ce qui est montré |
|---|---|---|
| **Solaire 66** | `solaire-66.webp` | le panneau de chantier |
| **Sweet Dream** | `sweet-dream.webp` | le dépliant en situation |
| **Krusty** | `krusty.webp` | le dépliant en situation |
| **Big Food** | `big-food.webp` | le logo seul |
| **Social Miroir** | `social-miroir.webp` | le logo, version en long |

> **Les deux mises en situation sont calculées**, pas photographiées :
> `reseaux/mockup.py` les monte à partir des faces fournies. C'est dit
> ici parce qu'une maquette présentée comme une photo d'imprimé serait
> un mensonge de plus dans une page qui vient d'en retirer trois.

> **Big Food, c'est le logo et rien d'autre.** Ni enseigne, ni
> dépliant. La taille d'un plan de travail dans un fichier ne dit pas
> ce qui a été produit — l'erreur a été faite une fois, elle est
> documentée dans `reseaux/PHOTOS-ATELIER.md`.

## Statuts précisés le 13 octobre

| Projet | Publiable en réalisation | Note |
|---|---|---|
| ~~**SR Coiffure**~~ | **retiré le 23 octobre** | la forme était vectorisée depuis une capture et le filet doré manquait. Plutôt que de courir après le fichier, Laurent préfère la sortir du portfolio. Ne pas rouvrir |
| **B.F Plomberie** | oui | **non récupérable** depuis la capture : nom en blanc sur beige, dégradé, texture |
| **Social Miroir** | oui | ✅ **logo reçu le 23 octobre**, trois déclinaisons — ronde, carrée, en long. La vignette utilise **la version en long**. ⚠️ La **ronde est à reprendre** : la bande arrive à 1,9 mm du cercle contre 26,1 mm à gauche, voir `A-FOURNIR.md` n° 13. **Client actuel de Grafycom** — pas de mention de structure précédente |
| **La Casquette Bleue** | **non** | Sandra n'a pas créé son identité : impression de cartes de visite uniquement |

### La Casquette Bleue : cliente, pas réalisation

La distinction compte, et elle est facile à perdre de vue. Ludivine Le
Blay est une **cliente réelle** dont l'avis figure sur la page
réalisations — c'est légitime, elle parle du service rendu. Mais son
identité visuelle n'est pas une création de Sandra : **son logo et ses
visuels n'ont rien à faire dans le portfolio**, ni sur le site ni sur les
réseaux.

Un avis client et une référence de création sont deux choses séparées.
Confondre les deux, c'est s'attribuer un travail qu'on n'a pas fait — la
faute la plus coûteuse du métier.

### Les logos à récupérer — il n'en reste qu'un, et il est perdu

SR Coiffure, B.F Plomberie et Social Miroir apparaissaient dans la
publication Instagram du 19 janvier. Il fallait leurs **fichiers
sources**, pas une capture du carrousel.

**Social Miroir est arrivé le 23 octobre** — trois `.ai` de 200 × 200 mm
et 300 × 100 mm, déposés dans `reseaux/visuels/sources/clients/` et
rendus à 300 dpi à côté. Le projet est en ligne.

**SR Coiffure est retiré le 23 octobre.** Le filet doré manquait, et
plutôt que de courir après le fichier, Laurent préfère le sortir du
portfolio. Classé.

**Reste B.F Plomberie**, non récupérable depuis la capture — nom en
blanc sur beige, dégradé, texture. Même situation que Casa Aldo : sans
un fichier qui réapparaît, il ne revient pas.
