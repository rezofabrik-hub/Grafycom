# Ce qu'il me manque, par ordre de priorité

Relevé le 23 octobre, **vérifié fichier par fichier** et non de mémoire :
chaque manque ci-dessous a été constaté par `reseaux/audit.py` ou par le
rapport du moteur, pas recopié d'une note.

Trois niveaux, et ils ne se valent pas.

| Niveau | Ce que ça veut dire |
|---|---|
| 🔴 **Bloquant** | une publication sort avec un trou visible |
| 🟠 **Décision** | rien n'est cassé, mais j'attends ton arbitrage |
| 🟡 **Confort** | la publication tient sans, ce serait mieux avec |

---

## 🟢 Plus aucun bloquant

**Le cycle est complet.** 217 visuels, aucune planche avec un trou.

Les deux derniers manques sont arrivés le 23 octobre :

| Reçu | Ce que ça débloque |
|---|---|
| Les cartes Solaire 66, recto et verso | planche **4** de la n° 13 |
| Le panneau de chantier Solaire 66 | planche **5** de la n° 13 |

Les cartes étaient en vectoriel, 89 × 59 mm — 85 × 55 plus 2 mm de fond
perdu — rendues à 300 dpi, fond perdu rogné par `poser()`. Le panneau
fait 2000 × 1337 px, rapport 1,496 : les 120 × 80 cm annoncés, à trois
millièmes près.

La planche 5 démontre enfin ce qu'elle annonce. Le panneau occupe 860 px,
la carte 61 — **7 % de la largeur**, à l'échelle exacte. Sans le panneau,
la carte était seule au milieu d'un vide.

---

## 🟠 Décision — plus rien en attente

Les quatre arbitrages ont été tranchés les 22 et 23 octobre. Ils restent
écrits ici, parce qu'un arbitrage qu'on efface se re-pose trois semaines
plus tard.

### 3. ~~KRUSTY et Solaire 66 à deux jours~~ — tranché le 23 octobre

**KRUSTY passe au mercredi 18 novembre**, 18 h 30, après Solaire 66 et
non avant. Le mercredi devient le créneau des réalisations intercalées.

L'ordre se défend mieux ainsi : la n° 13 du 16 montre une identité
complète — enseigne, cartes, panneau — et la n° 26 revient deux jours
après sur le seul logo et sur ce qui le fait tenir. L'une ouvre, l'autre
resserre.

### 4. ~~La semaine du 23 novembre porte six publications~~ — tranché le 23 octobre

SWEET DREAM est **repartie au 2 décembre**, comme tu l'as demandé. La
semaine du 23 reste pourtant à six — n° 17, 18, 19, 20, 16 et Solaire 66
le 25 — parce que Solaire 66 a été ajoutée **en plus**, pas à la place.

C'est écrit comme **dérogation motivée** dans `reseaux/audit.py`, avec sa
raison et sa date, pas toléré en silence. Le contrôle du plafond de cinq
publications par semaine passe donc pour la bonne raison, et il échouera
de nouveau si une sixième arrive sans motif écrit.

### 5. ~~Solaire 66 : réalisation en plus, ou à la place ?~~ — tranché le 23 octobre

**En plus.** Elle est publiée le 25 novembre et le créneau n° 13 garde
son exercice. Le cycle passe de 29 à 30 publications.

### 6. ~~Trois projets clients sans accord écrit~~ — tranché le 23 octobre

**Alliance Peintures, Cap Loisirs et Pano Perpignan sont retirés** de la
page réalisations, faute d'accord confirmé. Leurs fichiers sont
supprimés et non seulement déréférencés : une image qu'on retire d'une
page reste servie à son adresse.

À leur place, les projets dont l'accord est acquis : **Solaire 66, Sweet
Dream, Krusty, Big Food** et, depuis le 23 octobre, **Social Miroir**.

---

## 🟡 Confort — ce qui améliorerait sans débloquer

### 7. ~~Les visuels IA~~ — les six sont faites

| | Publication | Place | Ce que l'image a dû contourner |
|---|---|---|---|
| **A** | n° 1 · Couleur | ouverture | — |
| **C** | n° 5 · Typographie | ouverture | des lettres : vues de profil |
| **D** | n° 9 · Logo en petit | **clôture** | une semelle gravée, une feuille imprimée |
| **E** | n° 15 bis · Quatre supports | ouverture | une matière nommée |
| **B** | n° 20 · Matières | ouverture | — |
| **F** | n° 21 · Vitrine | ouverture | une enseigne, un ciel, un reflet qui parle |

Deux choses que le brief n'avait pas prévues, et qui se sont vérifiées
à chaque fois :

**La bonne place n'est presque jamais celle qui était annoncée.** Trois
des six ont changé de publication ou de planche, parce que la planche
visée démontrait quelque chose. La règle décor/preuve n'est pas une
précaution théorique : elle a déplacé la moitié de la série.

**Le piège est toujours dans le sujet, jamais dans la lumière.** Les
constantes optiques ont tenu du premier coup à chaque fois. Ce qui a
demandé du travail, c'est d'empêcher le moteur d'affirmer quelque
chose — une lettre, une structure de matériau, un nom sur une vitre.

Restent les neuf images de priorité moyenne et basse du brief — **G**
à **O**. Aucune n'est attendue par une planche : elles élargiraient le
choix, c'est tout.

### 8. La photo `03-portrait-nuancier-4x5.jpg` — « la grande version »

**La question était : c'est quoi, la grande version ?** Voici la
réponse exacte, parce que ma formulation précédente était vague.

Sur cette photo, le pseudo est écrit à la main sur du liège :
**« @grafycom graphiste », sans le point**. `retouche_atelier.py`
sait le réparer — il efface l'encre sombre, reconstruit le liège par
flou local, et réécrit « @grafycom.graphiste » incliné de 3 degrés pour
suivre la ligne de base.

Mais la fonction travaille sur **des coordonnées en pixels, relevées
une fois à la main** : la boîte du pseudo est à `(1120, 588)-(1570, 696)`.
Cela suppose une image d'au moins **1570 px de large**. Le script porte
aussi un second jeu de coordonnées, `(318, 470)-(700, 516)`, pour une
copie **3,5 fois plus petite** — c'est celle-là qui avait circulé.

Sur la petite, la retouche se voit : le liège reconstruit est plus lisse
que le vrai, et le raccord apparaît dès qu'on agrandit.

**Et depuis, le fichier a disparu.** `sources/atelier/` contient
aujourd'hui 01, 04, 06 et 07 — pas de 03. Il est parti avec le
conteneur, comme la photo n° 05. Ce qu'il faut donc, c'est **le fichier
d'origine tel qu'il sort de l'appareil**, pas un envoi par messagerie
qui le redimensionne.

### 9. De vraies photographies de Sandra

**Les deux contournements ont échoué.** La génération d'abord — cinq
images, texte inventé, logos redessinés. Puis la photo du site
détourée et posée sur la planche 01 du blog : techniquement propre,
refusée au rendu.

Il n'y a donc pas de raccourci. Trois poses couvriraient tout le
cycle :

- **elle écrit** — le blog, les publications de conseil ;
- **elle tend un dossier** — la livraison, la propriété des fichiers ;
- **de dos devant un mur d'échantillons** — les clôtures.

Fond neutre, haut **crème ou sable** — ni rouge ni bleu marine, ils
dépassent les 10 % d'accent de la charte. C'est le seul manque de cette
liste que je ne sais pas contourner.

En attendant, les trois photos existantes restent sur leurs clôtures et
son visage n'est sur aucun carreau de la grille.

### 10. Deux photos d'atelier

- `08-croquis-denim.jpg` — reçue en aperçu seulement, jamais en fichier.
- `05-profil-ecran-solaire66.jpg` — perdue avec le conteneur, non renvoyée.

Aucune planche ne les attend : elles élargiraient le choix, c'est tout.

### 11. Les textes des avis Google — un reçu, deux manquants

**L'avis de Laurent est arrivé le 23 octobre**, texte intégral, avec sa
réponse déjà publiée. Il est consigné dans `outils/FICHE-GOOGLE.md`.
Deux questions l'accompagnent, et elles sont pour toi : sous quel nom
le reprendre sur le site, et faut-il y rendre lisible le lien entre
REZOFABRIK et Grafycom.

Et une coquille à corriger depuis la fiche : la réponse publiée dit
« dompter **le flues** de vos idées ».

**Restent ceux de Social Miroir et Solaire 66**, du 13 octobre. Les
textes ne sont pas lisibles depuis ici. Me les recopier permet d'écrire
les réponses — un avis sans réponse vaut la moitié d'un avis.

### 12. L'adresse de partage de la fiche Google

Une adresse courte en `g.page/…`, ou un lien Maps. Elle se récupère dans
le profil d'établissement, bouton **« Partager »**.

C'est la dernière entrée manquante du bloc `sameAs` : celle qui permet à
Google de rapprocher le site, la fiche et les réseaux sans le deviner.

### 13. ~~Le violet de BIG FOOD~~ — tranché le 23 octobre

**Il n'est pas une couleur de marque.** L'entrée est retirée de
`reseaux/couleurs-clients.json`, et la planche 2 de la n° 25 tombe sur
l'encre de la charte — exactement ce que le repli prévoyait. Le fichier
de registre reste en place, vide : il a servi une fois, il resservira.

L'orange et le blanc continuent de se relever dans le vectoriel :
`#f39200` et `#ffffff`, exacts.

### 14. Le logo rond de Social Miroir, à reprendre par Sandra

Ce n'est pas un fichier à me fournir : c'est une correction à faire
dans Illustrator, et elle ne se fait pas sur un PNG. Voici les mesures,
pour qu'elle n'ait pas à les relever.

| | Aujourd'hui | Cible |
|---|---|---|
| Marge à gauche | **26,1 mm** | inchangée |
| Marge à droite | **1,9 mm** | 26,1 mm |
| Décentrage du bloc | **+12,1 mm** vers la droite | 0 |
| Largeur du bloc | 172,0 mm | **147,9 mm** |

**Et la correction est plus simple qu'elle n'en a l'air : la largeur
visée est exactement celle de la version carrée.** La bande y mesure
147,7 mm contre 147,9 ici — à deux dixièmes près, la même. Il ne s'agit
donc pas de redessiner quoi que ce soit, mais de **rendre à la bande la
longueur qu'elle a déjà dans les deux autres déclinaisons**, et de
recentrer le bloc.

Tant que ce n'est pas fait, `social-miroir-rond.png` **ne sert nulle
part** : la vignette du portfolio utilise la version en long, qui n'a
pas le défaut.

### 15. La n° 18 attend ta relecture

Le carrousel sur la mention de tri porte toujours son avertissement :
**« contenu au conditionnel, vérification à faire avant publication »**.
Les règles de signalétique n'ont pas pu être confirmées sur une source
officielle — seulement des guides d'éco-organismes et de cabinets, ce
qui est exactement le piège qui a déjà fonctionné avec le Cerfa
14798\*01.

Le sachet vierge de la planche 07 règle l'**image**. Il ne règle pas le
**texte**. Rien ne part avant ta relecture.

### 16. La confirmation des délais d'impression

La n° 16 annonce **création fin novembre, bon à tirer début décembre,
livraison mi-décembre**. À faire confirmer par l'imprimeur partenaire
avant publication. S'ils sont plus serrés, le reel se décale d'une
semaine **en avant**, pas en arrière.

---

## Ce qui n'est plus en attente

Pour que la liste soit honnête dans les deux sens.

| Point | État |
|---|---|
| L'accord KRUSTY | ✅ donné le 22 octobre |
| L'accord SWEET DREAM | ✅ donné le 22 octobre |
| L'accord BIG FOOD | ✅ donné le 22 octobre |
| La date de SWEET DREAM | ✅ mercredi 2 décembre |
| Le mock-up du dépliant KRUSTY | ✅ posé, planche 4 |
| Le mock-up du dépliant SWEET DREAM | ✅ calculé, planche 7 |
| Les photos des publications | ✅ plus aucune publication n'attend d'image |
| Les cartes Solaire 66 | ✅ reçues le 23 octobre, planche 4 complète |
| Les gabarits de visuels | ✅ 30 publications, 173 planches, 44 stories |
| Le logo Social Miroir | ✅ reçu le 23 octobre, trois déclinaisons vectorielles |
| Le premier visuel IA | ✅ A, le nuancier, intégré à la n° 1 |
| Le deuxième visuel IA | ✅ B, les papiers sur la tranche, reçu le 23 octobre |
| Les trois projets sans accord | ✅ retirés, fichiers supprimés |
| Le `.ai` deux lignes de BIG FOOD | ✅ reçu le 23 octobre, les deux compositions, 3200 px |

---

## Comment me répondre

Le plus simple : reprends les numéros.

> « 1 et 2 : je t'envoie les fichiers demain. 3 : on laisse. 5 : sors-la.
> 12 : voici les textes… »

Je n'ai besoin de rien d'autre. Chaque point de cette liste a été vérifié
contre les fichiers le 22 octobre ; si l'un d'eux est déjà réglé de ton
côté, dis-le et je corrige la liste plutôt que de te la redemander.
