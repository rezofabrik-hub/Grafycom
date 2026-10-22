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
| `07-bureau-solaire66.jpg` | au bureau, Solaire 66 à l'écran | **corrigée** : le vrai logo est incrusté en perspective à l'écran. Le croquis « devanfture » est hors du recadrage 4:5 |
| `03-portrait-nuancier-4x5.jpg` | portrait vertical, nuancier | **à corriger** : le pseudo y est `@grafycom graphiste`, **sans le point**. `retouche_atelier.py` sait le refaire |
| `08-croquis-denim.jpg` | veste en jean, carnet de croquis | reçue en aperçu seulement, pas en fichier |
| `05-profil-ecran-solaire66.jpg` | de profil, écran | perdue avec le conteneur, non renvoyée |

## Ce qui manque encore

- **Les cartes Solaire 66**, recto et verso, et **le panneau de chantier.**
  Deux planches de la n° 13 sortent avec un trou nommé : `04.png` et
  `05.png`. Le reste de la publication est complet.

## Ce que les scripts refont tout seuls

`retouche_atelier.py` n'a pas besoin d'être réécrit, seulement
réalimenté :

- `pseudo()` — remet le point du pseudo sur le liège, par seuil local ;
- `logo_mural()` — projette `assets/img/logo-grafycom.jpg` dans le
  quadrilatère de l'affiche, en perspective, l'encre posée en
  multiplication ;
- `carte_voeux()` — recadre la carte au lieu de la retoucher, et dit
  pourquoi la retouche échoue.

Les trois versions monochromes du logo Solaire 66 se **déduisent** du
fichier couleur : même forme, une seule encre. Les redessiner serait
l'occasion d'une divergence.
