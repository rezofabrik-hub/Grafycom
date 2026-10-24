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

### 8. ~~Les trois photos d'atelier manquantes~~ — retirées de la liste

`03-portrait-nuancier-4x5.jpg`, `08-croquis-denim.jpg`,
`05-profil-ecran-solaire66.jpg`. Elles y figuraient depuis le début.
Elles en sortent le 23 octobre, pour deux raisons qui se suffisent
chacune.

**On ne peut pas les générer.** Ce sont des photos de Sandra dans son
atelier, et c'est exactement ce qui a échoué cinq fois : texte inventé
sur les murs, logo Grafycom redessiné, logo Solaire 66 faux. Le sujet
est clos, dans les trois directions — voir `PHOTOS-ATELIER.md`.

**Et aucune planche ne les attend.** Vérifié : les trois sont
référencées nulle part dans `visuels.py`. Le registre `PHOTOS` n'en
connaît que quatre — 01, 04, 06, 07 — et elles sont toutes en place.
Ces trois-là élargissaient le choix, rien de plus.

Un manque qu'on ne peut pas combler et que personne n'attend n'est pas
un manque. Il encombre la liste, et il fait douter du reste.

### 9. ~~Les textes des avis Google~~ — les deux sont arrivés

**Solaire 66** le matin du 23 octobre, **Social Miroir** le soir. Les
deux textes sont dans `outils/FICHE-GOOGLE.md`, les deux réponses sont
publiées, et aucune n'a de coquille — celle de Solaire 66 en avait une,
corrigée depuis la fiche.

✅ **Les deux sont en ligne sur la page réalisations**, dans un groupe
« Projets menés par Grafycom » placé devant les trois anciens.

Le bloc portait une mention globale, « ces avis ont été laissés à
l'époque de la structure précédente ». Vraie à trois avis, fausse pour
un quart du bloc à quatre, pour deux cinquièmes à cinq. **Une mention
globale fausse est pire que pas de mention : elle fait douter du
reste.** À cinq, ce n'est plus une phrase qui peut le dire, c'est la
structure — deux groupes, deux intertitres, et la page se lit sans note
de bas de bloc.

### 10. L'adresse de partage de la fiche Google

Une adresse courte en `g.page/…`, ou un lien Maps. Elle se récupère dans
le profil d'établissement, bouton **« Partager »**.

C'est la dernière entrée manquante du bloc `sameAs` : celle qui permet à
Google de rapprocher le site, la fiche et les réseaux sans le deviner.

### 11. ~~Le violet de BIG FOOD~~ — tranché le 23 octobre

**Il n'est pas une couleur de marque.** L'entrée est retirée de
`reseaux/couleurs-clients.json`, et la planche 2 de la n° 25 tombe sur
l'encre de la charte — exactement ce que le repli prévoyait. Le fichier
de registre reste en place, vide : il a servi une fois, il resservira.

L'orange et le blanc continuent de se relever dans le vectoriel :
`#f39200` et `#ffffff`, exacts.

### 12. Le logo rond de Social Miroir — rien ne l'attend non plus

**Le site n'est pas concerné.** La vignette de la page réalisations est
faite à partir de la version **en long**, qui n'a pas le défaut. Le
fichier rond ne sert nulle part : ni sur le site, ni dans une
publication, ni dans un visuel. Il n'y a donc **rien à enlever**, et
rien qui bloque.

La reprise ne devient utile que le jour où la version ronde doit servir
d'**avatar** — c'est son usage, et c'est là que le défaut se verrait :
Instagram et Facebook recadrent l'avatar en cercle, et ce qui touche le
bord se fait rogner.

Les mesures restent ici pour ce jour-là, et la correction est plus
simple qu'elle n'en a l'air :

| | Aujourd'hui | Cible |
|---|---|---|
| Marge à gauche | 26,1 mm | inchangée |
| Marge à droite | **1,9 mm** | 26,1 mm |
| Décentrage du bloc | +12,1 mm | 0 |
| Largeur du bloc | 172,0 mm | **147,9 mm** |

**La largeur visée est exactement celle de la version carrée** —
147,7 mm mesurés contre 147,9. Il ne s'agit pas de redessiner, mais de
rendre à la bande la longueur qu'elle a déjà dans les deux autres
déclinaisons, et de recentrer.

### 13. ~~La n° 18~~ — sortie du calendrier le 23 octobre

Elle devait partir le mardi 24 novembre à 8 h 00. **Elle ne part pas**,
et elle n'a plus de date tant que la signalétique de tri n'est pas
confirmée sur une source officielle.

Ce qui part avec elle : le texte de fiche Google n° 18 et les deux
stories S5-B qui la teasaient. Tout est conservé, rien n'est supprimé.

Le cycle passe de **30 à 29 publications**, de 173 à 166 planches. Et
une conséquence inattendue, mesurée par l'audit : la semaine du 23
novembre portait six publications et vivait sous dérogation écrite.
Avec la n° 18 en moins elle retombe à **cinq**. **La dérogation est
retirée de `audit.py` : le plafond tient désormais tout seul, sans
exception.**

Pour la remettre un jour : une ligne dans `visuels.py`,
`GABARITS["emballage-tri"] = pub18_emballage_tri`, et les sept planches
reviennent — sachet kraft compris.

### 14. ~~La confirmation des délais d'impression~~ — donnée le 23 octobre

**Création sur la première quinzaine de novembre**, parce qu'en
décembre les livraisons deviennent risquées à cause de Noël. La chaîne
complète : création du 1er au 15 novembre → bon à tirer fin novembre →
livraison début décembre.

Elle a coûté un déplacement, et il était nécessaire. **Le reel n° 16
remonte du samedi 28 au lundi 9 novembre.** Il annonçait « création fin
novembre, livraison mi-décembre » — un calendrier que l'imprimeur ne
tient pas. Et surtout : une publication qui donne une date limite doit
précéder sa date limite. Le 28, elle arrivait deux semaines après la
fermeture de la fenêtre, et quelqu'un qui l'aurait suivie aurait
commandé des cartes qui ne seraient pas arrivées.

La **n° 9** glisse du lundi 9 au samedi 14 pour libérer le créneau :
c'est la seule publication de cette semaine dont le contenu ne dépend
d'aucune date.

**Aucune dérogation n'a été nécessaire.** La semaine du 9 portait
quatre publications, elle en porte cinq ; celle du 23 en portait cinq,
elle en porte quatre. Densités : 5 · 5 · 5 · 5 · 4 · 5.

L'écran 1 du reel porte maintenant **deux marques** au lieu d'une : le
15 novembre en corail, le 24 décembre en encre. « Six jours pour
décider. Six semaines pour livrer. » Une seule marque sur Noël laissait
croire qu'on avait six semaines devant soi.

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
| Les gabarits de visuels | ✅ 28 publications, 160 planches, 41 stories |
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
