# Ce qu'il me manque, par ordre de priorité

Relevé le 22 octobre, **vérifié fichier par fichier** et non de mémoire :
chaque manque ci-dessous a été constaté par `reseaux/audit.py` ou par le
rapport du moteur, pas recopié d'une note.

Trois niveaux, et ils ne se valent pas.

| Niveau | Ce que ça veut dire |
|---|---|
| 🔴 **Bloquant** | une publication sort avec un trou visible |
| 🟠 **Décision** | rien n'est cassé, mais j'attends ton arbitrage |
| 🟡 **Confort** | la publication tient sans, ce serait mieux avec |

---

## 🔴 Bloquant — trois fichiers, une seule publication

### 1. Les cartes de visite Solaire 66, recto et verso

**Où ça manque :** n° 13, lundi 16 novembre, planche **4**.
**Noms attendus :** `solaire-66-carte-recto.png`, `solaire-66-carte-verso.png`
**Où les déposer :** `reseaux/visuels/sources/`

La planche sort avec son emplacement vide et le signale. Le reste de la
publication — huit planches — est complet.

### 2. Le panneau de chantier Solaire 66

**Où ça manque :** n° 13, planche **5**.
**Nom attendu :** `solaire-66-panneau.png`

La planche 5 pose la carte et le panneau **à l'échelle exacte**, d'après
les dimensions que tu as données : panneau 120 × 80 cm, carte 8,5 × 5,5 cm.
C'est la planche qui démontre qu'un logo doit tenir aux deux tailles. Sans
les deux fichiers, elle ne démontre rien.

> **Ce sont les deux seuls trous de tout le cycle.** 210 visuels produits,
> deux planches incomplètes.

---

## 🟠 Décision — quatre arbitrages qui n'attendent qu'un mot

### 3. KRUSTY le 14 et Solaire 66 le 16

Deux réalisations à deux jours d'intervalle. C'est la seule imperfection
de l'intercalage, et elle vient de Solaire 66, fixée au créneau n° 13.

La corriger veut dire la sortir du rythme — ce qui rouvre l'arbitrage
n° 6 et demande d'écrire une publication de remplacement pour le 16.

**Trois réponses possibles :** on laisse · on sort Solaire 66 · on décale
KRUSTY au 11 (mercredi, comme SWEET DREAM — mais c'est l'Armistice, donc
plutôt le 18).

### 4. La semaine du 23 novembre porte six publications

n° 17, 18, 27, 19, 20 et 16. C'est une de plus que partout ailleurs, et
c'est la conséquence directe d'avoir ramené SWEET DREAM au 25.

C'est écrit comme **dérogation motivée** dans `reseaux/audit.py`, pas
toléré en silence. Si tu préfères revenir à cinq, SWEET DREAM repart au
2 décembre et le trou de seize jours revient avec elle.

### 5. Solaire 66 : réalisation en plus, ou à la place ?

L'arbitrage n° 6 disait « en plus du rythme, pas à la place ». BIG FOOD,
KRUSTY et SWEET DREAM le sont. **Solaire 66 ne l'est pas** : elle occupe
le créneau n° 13.

Je ne l'ai pas déplacée, pour une raison que je te soumets plutôt que de
trancher seul : le créneau qu'elle occupe ne portait pas une leçon, il
portait **un exercice fictif**. Le cycle n'a donc rien perdu. La sortir
obligerait à écrire une 30ᵉ publication.

### 6. Trois projets clients sans accord écrit

**Alliance Peintures, Cap Loisirs, Pano Perpignan** — relevés dans
`acquisition.md`. Soit tu obtiens l'accord, soit on les retire de la page
réalisations. Aucune publication du cycle ne les montre, donc rien n'est
bloqué : c'est le site qui attend.

---

## 🟡 Confort — ce qui améliorerait sans débloquer

### 7. Le logo Social Miroir, à redemander

Reçu le 13 octobre avec trois déclinaisons vectorielles, puis **perdu** :
`reseaux/visuels/sources/` n'est pas versionné — le dépôt est public — et
le conteneur a été reconstruit depuis. Aucune publication ne l'utilise
aujourd'hui, mais la page réalisations le cite.

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

### 11. Le `.ai` de la composition deux lignes de BIG FOOD

La capture reçue fait 356 px. Elle est posée **à cette taille exacte**,
donc nette. Mais 356 px est un plafond : le jour où cette composition
part à l'impression, il faudra le vectoriel.

### 12. Les textes des deux avis Google

**Social Miroir** et **Solaire 66** ont laissé un avis le 13 octobre. Les
textes ne sont pas lisibles depuis ici. Me les recopier permet d'écrire
les réponses — un avis sans réponse vaut la moitié d'un avis.

### 13. L'adresse de partage de la fiche Google

Une adresse courte en `g.page/…`, ou un lien Maps. Elle se récupère dans
le profil d'établissement, bouton **« Partager »**.

C'est la dernière entrée manquante du bloc `sameAs` : celle qui permet à
Google de rapprocher le site, la fiche et les réseaux sans le deviner.

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
| La date de SWEET DREAM | ✅ mercredi 25 novembre |
| Le mock-up du dépliant KRUSTY | ✅ posé, planche 4 |
| Le mock-up du dépliant SWEET DREAM | ✅ calculé, planche 7 |
| Les photos des publications | ✅ plus aucune publication n'attend d'image |
| Les gabarits de visuels | ✅ 30 gabarits, 210 planches |

---

## Comment me répondre

Le plus simple : reprends les numéros.

> « 1 et 2 : je t'envoie les fichiers demain. 3 : on laisse. 5 : sors-la.
> 12 : voici les textes… »

Je n'ai besoin de rien d'autre. Chaque point de cette liste a été vérifié
contre les fichiers le 22 octobre ; si l'un d'eux est déjà réglé de ton
côté, dis-le et je corrige la liste plutôt que de te la redemander.
