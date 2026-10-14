# Photos à prendre — du 2 novembre au 28 novembre 2026

> **Aucune publication du mois n'attend plus d'image.** Les huit qui en
> demandaient une sont redessinées — le détail est plus bas, dans « Les
> photos spécifiques au mois ». Ce document reste, et il garde tout son
> sens : il n'est plus une liste de courses, c'est **la réserve dans
> laquelle on puise** quand une occasion se présente, et le mode d'emploi
> pour que la photo prise ce jour-là soit utilisable.

Ce que `visuels.py` ne sait pas faire, et ne doit pas faire : les
photographies. Une devanture, une matière, un plan de travail se
photographient. Une image inventée sur le compte d'une graphiste se
retourne contre elle. Ce que `visuels.py` sait faire, en revanche, c'est
**dessiner** — et sur un schéma, une coupe ou une comparaison, le dessin
vaut mieux que la photo. C'est la ligne de partage, et elle est nette :
on dessine ce qui s'explique, on photographie ce qui se prouve.

Quand une photo se prend, elle se prend **par lots**, à l'avance, plutôt
qu'une image à la fois la veille d'une publication. Une séance d'une
heure remplit la réserve pour longtemps.

---

## La règle qui gouverne tout le reste

**Jamais une image dont les droits ne sont pas clairs.** Ni photo trouvée,
ni visuel de banque sans licence commerciale. Et pour tout projet client :
**son accord avant publication**, même si le contrat cède les droits. Un
client surpris de se voir sur Instagram est un client perdu.

---

## Comment photographier pour que ça serve partout

Il y a trois formats de sortie, et `recadrer.py` les fabrique à partir
d'une seule source. Sandra n'a donc **pas** à penser au cadrage final.

| Format | Taille | Usage |
|---|---|---|
| article | 1200 × 630 | aperçu quand on partage un lien |
| post | 1080 × 1350 | carrousel et post Instagram ou Facebook |
| story | 1080 × 1920 | story et reel |

```bash
python3 reseaux/recadrer.py photo.jpg vitrine --tous
python3 reseaux/recadrer.py photo.jpg enseigne 0.35   # viser plus haut
```

**Six habitudes qui font la différence entre une photo utilisable et une
photo à refaire :**

1. **Photographier en grand, dans le format natif du téléphone.** On
   recadre après. Cadrer serré à la prise, c'est s'interdire les deux
   autres formats.
2. **Prendre la même scène en vertical ET en horizontal.** Le vertical
   donne la story, l'horizontal donne l'aperçu de lien. Deux déclenchements,
   dix secondes.
3. **Laisser du vide.** Un ciel, un mur, une table nue : c'est là que le
   texte se posera. Une photo pleine jusqu'aux bords ne supporte aucune
   légende incrustée.
4. **Éviter les lumières mélangées.** Néon de boutique plus lumière du
   jour par la vitrine, et les blancs virent — vert d'un côté, bleu de
   l'autre. Soit on éteint, soit on sort. C'est le défaut qu'un œil de
   graphiste repère et que personne ne sait rattraper proprement.
5. **Filmer dix secondes à chaque fois.** Les coulisses sont ce qui marche
   le mieux et ce qu'on oublie systématiquement de capter. Un plan fixe de
   dix secondes suffit à faire un reel.
6. **Photographier l'avant AVANT de toucher à quoi que ce soit.** Un
   avant/après ne se reconstitue pas. C'est la photo qu'on regrette le
   plus souvent de ne pas avoir prise.

---

## Les prises de vue permanentes

À constituer une fois, puis à compléter au fil des chantiers. C'est le
stock dans lequel on puise quand une publication demande une image.

### Coulisses — le pilier qui marche le mieux

- Les **crayonnés** sur papier, avec le crayon encore dans le cadre.
- Les **pistes écartées**, posées côte à côte. Montrer ce qu'on n'a pas
  retenu vaut mieux que montrer le résultat seul : ça prouve qu'il y a eu
  un choix.
- Un **bon à tirer annoté** au stylo rouge.
- L'**écran** avec le tracé vectoriel ouvert, points d'ancrage visibles.
- Le **nuancier** Pantone ouvert en éventail, en lumière du jour.
- Le **plan de travail** en plan large, en début de journée.

### Matières — le détail qui ne se voit qu'en lumière rasante

Ces finitions sont invisibles en lumière frontale. Il faut une lumière qui
arrive **par le côté**, presque parallèle à la surface, et on les voit
apparaître.

- Un **papier texturé** en lumière rasante, le grain visible.
- Une **dorure à chaud** ou un **vernis sélectif** : incliner le support
  jusqu'à ce que la lumière accroche.
- Un **gaufrage**, de trois-quarts, l'ombre dans le creux.
- Une **pile de papiers** de grammages différents, vue sur la tranche.
- Un **échantillon d'adhésif** ou de Dibond, coin relevé.

### Réalisations — avec accord du client

- Le support **en situation**, pas à plat : un menu sur une table dressée,
  une carte de visite dans une main, une étiquette sur la bouteille.
- L'**enseigne sur la façade**, prise d'en face et de biais, à l'heure où
  elle est éclairée comme un passant la voit.
- Un **véhicule marqué**, de trois-quarts avant, en entier dans le cadre.
- Un **avant/après**, même cadrage, même heure, même distance.

### Territoire — l'ancrage local

- Une **devanture de Perpignan**, centre ancien.
- Un **marché**, une **rue commerçante**, un **port**.
- Une **carte ou une signalétique bilingue** catalan-français.
- Un **commerce de village** dans une des communes couvertes par le site.

### La personne — une fois par mois, pas plus

- Sandra **au travail**, de trois-quarts ou de dos, pas de portrait posé.
- Les **mains** en train de dessiner, de trier des échantillons.
- Le **bureau** en fin de journée.

---

## Les photos spécifiques au mois — il n'y en a plus

**Les huit publications qui attendaient une image sont redessinées.** Tu as
dit que les prises de vue étaient très compliquées pour toi ; huit trous
dans le calendrier auraient été pires. Les visuels sont faits, ils sont
dans `reseaux/visuels/`, et il n'y a rien à photographier pour les sortir.

| # | Date | Ce qui était demandé | Ce qui est livré |
|---|---|---|---|
| 4 | 23 oct | cinq plans à filmer, dont deux animations | **cinq écrans finis** : écran contre papier, synthèse RVB et synthèse CMJN **calculées**, le même bleu sur mat et sur couché |
| 8 | 30 oct | quatre plans à filmer, dont une séquence sans issue propre | **cinq écrans finis** : citrouille, contraste orange/noir, quatre pictogrammes d'alerte, deux devantures comparées |
| 10 | 3 nov | une rue commerçante au crépuscule | une rue dessinée, six façades, enseignes allumées avec leur halo — plus un schéma de formulaire à la place de la capture du Cerfa |
| 12 | 6 nov | quatre plans à filmer | **cinq écrans finis** : vitrine nue cotée, dépoli, microperforé vu des deux côtés, lettres contre pavé blanc, vitrine de nuit |
| 14 | 10 nov | une devanture floutée | une devanture fictive, slogan anglais **lisible**, puis la même avec la ligne française ajoutée |
| 15 | 12 nov | quatre macrophotographies | quatre matières **dessinées en coupe** |
| 16 | 14 nov | cinq plans à filmer, dont des mains | **cinq écrans finis** : calendrier de six semaines, cartes gaufrées, paquet kraft, rétroplanning, table vue de dessus |
| 20 | 20 nov | cinq plans à filmer | **cinq écrans finis** : gaufrage, deux grammages sur la tranche, gaufrage de côté **et** de face, dorure allumée **et** éteinte |
| 24 | 28 nov | cinq plans à filmer | **cinq écrans finis** : deux pages de calendrier, deux versions du logo, trois questions, le logo sur trois supports |
| 18 | 17 nov | un sachet à photographier | un sachet dessiné, puis **le même** au trait avec sa zone réservée |
| 21 | 23 nov | une vitrine de nuit du trottoir d'en face | la scène dessinée — **et une septième planche** : la même devanture à 2, 8 et 25 m |
| 22 | 24 nov | une vitrine avec adhésifs de fêtes | une vitrine dessinée portant les deux adhésifs |

### Pourquoi un dessin, et pas une image générée

C'est la question qui se pose, et elle mérite une réponse nette.

1. **Un dessin ne prétend pas être une photo.** Une image générée, si — et
   elle se trahit sur les enseignes, en pseudo-lettres. C'est exactement ce
   qui s'est passé le 13 octobre, plus bas dans ce document. Une façade
   dessinée de loin porte des barres : personne ne lit un texte qui n'est
   pas écrit. Et quand un lettrage doit se lire — « SUNSET COFFEE », le
   numéro de Cerfa — il est composé en Inter, accents compris.
2. **Les droits sont clairs.** Le tracé sort de `reseaux/visuels.py`.
3. **Aucun commerce réel n'est reconnaissable.** Quatre de ces huit
   publications parlent de non-conformité. Aucune ne peut illustrer son
   sujet avec la vitrine de quelqu'un, même floutée.
4. **Sur deux sujets le dessin montre mieux.** La coupe d'un alu composite
   fait voir l'âme noire entre les deux peaux, qu'aucune macro ne donne
   aussi nettement. Et la même vitrine redessinée à trois distances fait
   une démonstration qu'aucun cadrage unique ne rend.

### Ce que le dessin ne remplace pas

Deux familles, et les listes plus haut restent entières pour elles :

- **Les matières en lumière rasante** — une dorure, un gaufrage, un vernis
  sélectif. Le dessin les suggère, il ne les rend pas. Le reel n° 20 est
  désormais dessiné lui aussi, mais c'est **le seul visuel du cycle que je
  referais en priorité** le jour où les échantillons seront sous la main :
  une macro en lumière rasante garde quelque chose qu'un tracé n'a pas. Les
  écrans se remplacent un par un.

**Plus aucune publication du cycle ne demande de filmer.** Les six reels
sont dessinés. Les fiches de tournage ont disparu de `visuels.py` avec
elles — une fonction sans appelant ne casse pas, elle pourrit ; l'historique
git les conserve si le besoin revient.
- **Les réalisations en situation.** Un support en situation photographié,
  c'est une preuve ; dessiné, c'est une maquette. La distinction compte
  pour le pilier « réalisations », pas pour les publications pédagogiques.

Ces deux familles se photographient le jour où ce sera possible, et les
planches dessinées tiennent d'ici là. Le remplacement se fait case par
case, sans toucher au reste du carrousel.

---

## Ce qui rend une photo inutilisable

- **Le flash direct.** Il écrase les matières, et les matières sont
  précisément ce qu'on veut montrer.
- **Les lumières mélangées** (voir plus haut).
- **Un cadrage déjà serré** : plus aucune marge pour les trois formats.
- **Une marque tierce lisible** qui n'a rien à faire là — une bouteille,
  un logo de fournisseur, une enseigne voisine au second plan.
- **Un visage reconnaissable** sans accord de la personne.
- **Un projet client non livré ou non validé.** Même flouté, même de loin.
- **Une image générée.** Voir ci-dessous — c'est arrivé le 13 octobre.

## Une image générée n'est pas une photo

Deux images ont été proposées le 13 octobre comme étant les deux prises de
vue demandées. Elles ne l'étaient pas : c'étaient des images générées.

**Comment ça se voit, en dix secondes.** Il suffit d'agrandir une
enseigne, une affiche, une étiquette. Sur les deux images, **tous** les
textes étaient des pseudo-lettres : « S A.CKS », « Tïvllts », « nmcces »,
et sur l'auvent du commerce une suite de signes illisibles. Un modèle
génératif dessine la forme d'un texte sans savoir l'écrire. Aucune des
deux n'avait non plus de données EXIF — ni appareil, ni objectif, ni date
de prise de vue. Un téléphone en laisse toujours.

**Pourquoi c'est disqualifiant ici**, au-delà de la règle de
`LIGNE-EDITORIALE.md` :

1. **Ce n'est pas Perpignan.** Les deux scènes montrent des rues qui
   n'existent pas. Tout l'intérêt d'une photo locale est d'être locale ;
   un commerçant de Saint-Estève reconnaît sa rue, ou ne reconnaît rien.
2. **Une graphiste qui publie une enseigne au texte illisible pour parler
   de lisibilité d'enseigne se contredit dans la même image.** C'est le
   genre de détail qu'un confrère repère, et qu'il montre.
3. **Les droits ne sont pas clairs**, et c'est exactement ce que la règle
   interdit : ni photo trouvée, ni visuel de banque sans licence.

**Ce qui reste vrai :** les deux sorties décrites plus haut prennent une
heure, au téléphone, et débloquent six publications. Il n'y a pas de
raccourci — c'est la raison d'être de ce document.

