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

### 8. Le logo SR Coiffure

La forme est vectorisée depuis ta capture, **le filet doré manque**. À
demander au salon.

### 9. La photo `03-portrait-nuancier-4x5.jpg`

Le pseudo y est écrit **« @grafycom graphiste », sans le point**.
`retouche_atelier.py` sait le corriger, mais il lui faut le fichier
d'origine — celui en main est trop petit pour que la correction tienne à
l'agrandissement.

### 10. Deux photos d'atelier

- `08-croquis-denim.jpg` — reçue en aperçu seulement, jamais en fichier.
- `05-profil-ecran-solaire66.jpg` — perdue avec le conteneur, non renvoyée.

Aucune planche ne les attend : elles élargiraient le choix, c'est tout.

### 11. Les textes des deux avis Google

**Social Miroir** et **Solaire 66** ont laissé un avis le 13 octobre. Les
textes ne sont pas lisibles depuis ici. Me les recopier permet d'écrire
les réponses — un avis sans réponse vaut la moitié d'un avis.

### 12. L'adresse de partage de la fiche Google

Une adresse courte en `g.page/…`, ou un lien Maps. Elle se récupère dans
le profil d'établissement, bouton **« Partager »**.

C'est la dernière entrée manquante du bloc `sameAs` : celle qui permet à
Google de rapprocher le site, la fiche et les réseaux sans le deviner.

### 13. Une réserve, pas un manque : le violet de BIG FOOD

Le vectoriel reçu le 23 octobre ne porte **que le logo**, sur fond
transparent. La capture qu'il remplace montrait ce logo sur une bande
violette, et c'est là que la planche 2 de la n° 25 prenait son fond.

Le violet `#4b175f` est conservé dans `reseaux/couleurs-clients.json`,
versionné, avec sa provenance. **À confirmer auprès du client :** si
Big Food n'a pas de violet de marque, l'entrée se retire et la planche
tombe sur l'encre de la charte. L'orange et le blanc, eux, se relèvent
toujours dans le fichier — `#f39200` et `#ffffff`, exacts.

### 14. La confirmation des délais d'impression

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
