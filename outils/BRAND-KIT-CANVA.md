# Le Brand Kit Canva — ce qu'il faut y entrer

## Pourquoi ce document existe, et ce qu'il n'est pas

Le Brand Kit **ne peut pas être rempli depuis ici.** Le connecteur Canva
expose de quoi *lire* les Brand Kits, créer un design, publier un modèle
— mais aucun outil pour créer un Brand Kit ni pour y écrire une couleur,
une police ou un logo. Vérifié le 23 octobre : l'appel de liste répond
`{"items": []}`, et il n'existe aucune fonction d'écriture en regard.

C'est donc une saisie manuelle, dans l'interface Canva, et ce document
est fait pour la rendre mécanique. Tout y est dans l'ordre où Canva le
demande, et rien n'est à aller chercher ailleurs.

> ⚠️ **Le Brand Kit est une fonction payante** (Canva Pro ou Teams). Sur
> un compte gratuit, l'onglet existe mais n'enregistre ni les polices ni
> les logos. À vérifier avant de commencer, pour ne pas saisir deux fois.

> 🛑 **Ce Brand Kit ne sert pas le cycle.** Les 210 visuels sont produits
> par `reseaux/visuels.py`, qui refuse en dur toute couleur absente de
> `assets/style.css` — c'est ce qui garantit qu'aucune planche ne sort de
> la charte. Canva n'a pas ce garde-fou : il **propose** la charte, il ne
> l'**impose** pas. Il est là pour les pièces ponctuelles de Sandra, pas
> pour les publications.

## 1 · Les couleurs — 18, dans cet ordre

L'ordre compte : Canva affiche les premières en tête de palette, et ce
sont celles qu'on prend sans réfléchir. Les accents d'abord, les fonds
ensuite, l'encre en dernier.

### Les accents — la gamme aquarelle

Ils ne servent **jamais de fond**. Un seul accent par planche.

| # | Nom | Hex |
|---|---|---|
| 1 | Corail | `#f2585c` |
| 2 | Violet | `#a86cd0` |
| 3 | Bleu | `#2f7fc4` |
| 4 | Turquoise | `#3ec2b3` |
| 5 | Magenta | `#e33d82` |
| 6 | Rose | `#e75ba6` |
| 7 | Orange | `#f5883c` |
| 8 | Jaune | `#f9c33f` |
| 9 | Bleu vif | `#35a9dd` |

### Les fonds — la base chaude

| # | Nom | Hex |
|---|---|---|
| 10 | Crème | `#f7f1ef` |
| 11 | Crème rosé | `#f3eae9` |
| 12 | Sable | `#efe4dd` |
| 13 | Sable foncé | `#e4d5cc` |
| 14 | Blanc | `#ffffff` |

### Les textes

| # | Nom | Hex | Emploi |
|---|---|---|---|
| 15 | Encre | `#2f2723` | les titres, et les fonds sombres |
| 16 | Brun | `#6d5a50` | le texte courant |
| 17 | Brun clair | `#8a7469` | le texte secondaire |
| 18 | Taupe | `#a2897c` | les surtitres, les légendes |

## 2 · Les polices

Canva demande une police de titre et une police de texte. Les deux sont
sur Google Fonts, donc disponibles dans Canva sans import.

| Rôle | Police | Graisses utilisées |
|---|---|---|
| **Titres** | Playfair Display | 500, 700, 800 |
| **Texte courant** | Inter | 400, 600, 800 |
| **Accent manuscrit** | Caveat | 600 |

**Playfair en 500 pour les titres**, pas en 700 : c'est le réglage du
site et des planches. Le 700 et le 800 sont réservés aux chiffres et aux
repères.

Le site utilise aussi **Courier Prime** pour quelques étiquettes
techniques. Ce n'est pas une police de marque : ne pas la mettre au
Brand Kit, elle n'a de sens que dans le code du site.

## 3 · Les logos

| Fichier | Usage |
|---|---|
| `assets/img/logo-grafycom.webp` | la version longue, par défaut |
| `assets/img/logo-grafycom-carre.webp` | la version carrée, pour les avatars |

Canva accepte le WebP. Les `.jpg` du même dossier sont les versions de
repli du site : ils ont un fond blanc cuit dans l'image, donc **ne pas
les charger dans le Brand Kit**.

## 4 · Ce qu'il faut écrire dans les notes du Brand Kit

Canva permet une note libre. Trois lignes suffisent, et ce sont les trois
règles qui se perdent en premier :

```
Un seul accent par visuel. Les accents ne servent jamais de fond.
Les fonds sont crème, sable ou blanc — jamais une couleur vive.
Le pseudo s'écrit @grafycom.graphiste, avec le point.
```

## 5 · Après la saisie

Rien à faire côté dépôt : le Brand Kit vit dans Canva et n'est lu par
aucun programme d'ici. Si la charte du site change un jour, c'est
`assets/style.css` qui fait foi, et ce document qu'il faut refaire —
`python3 -c "import reseaux.visuels as v; print(v.C)"` en donne la
liste à jour en une ligne.
