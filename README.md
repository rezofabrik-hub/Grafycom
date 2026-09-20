# Grafycom — site vitrine

> Studio de communication visuelle de Sandra, à Perpignan (66).
> « L'image qui vous ressemble ».

Site **vitrine, sans boutique ni paiement en ligne** : il présente les
prestations et amène le visiteur vers une demande de devis.

Statique, sans dépendance ni étape de build. On ouvre `index.html` dans un
navigateur, on le dépose sur n'importe quel hébergement, et c'est en ligne.

## Voir le site en local

Double-cliquer sur `index.html` suffit pour la plupart des vérifications. Pour
un aperçu strictement identique à la mise en ligne (chemins absolus, polices),
lancer un petit serveur depuis le dossier :

```bash
python3 -m http.server 8000
```

puis ouvrir <http://localhost:8000>.

## Les pages

| Fichier | Rôle |
|---|---|
| `index.html` | Accueil : promesse, bénéfices d'une identité cohérente, les 6 prestations, présentation de Sandra, méthode en 4 étapes, secteurs, aperçu des réalisations, FAQ |
| `prestations.html` | Le détail des 6 familles de prestations, et la question du budget |
| `realisations.html` | Portfolio — **retirée du menu** tant qu'elle est vide, voir ci-dessous |
| `methode.html` | Le déroulé d'un projet en 6 étapes, et ce qui est attendu du client |
| `a-propos.html` | Sandra, le colibri, la double casquette, le bilinguisme |
| `contact.html` | Formulaire de devis détaillé + coordonnées + zone d'intervention |
| `infographiste-perpignan.html` | Page locale — Perpignan |
| `graphiste-canet-en-roussillon.html` | Page locale — Canet-en-Roussillon |
| `graphiste-argeles-sur-mer.html` | Page locale — Argelès-sur-Mer |
| `graphiste-ceret.html` | Page locale — Céret |
| `basculer-domaine.sh` | Script de bascule vers un vrai nom de domaine |
| `mentions-legales.html` | Obligatoires — **à compléter avant mise en ligne** |
| `confidentialite.html` | RGPD — **à compléter avant mise en ligne** |
| `assets/style.css` | Feuille de style commune |
| `assets/site.js` | Menu mobile, année du copyright, visuels manquants, formulaire |
| `robots.txt`, `sitemap.xml` | Référencement |

L'en-tête et le pied de page sont recopiés dans chaque fichier : pour modifier
le menu ou une mention du pied, il faut passer sur les huit pages.

## À faire avant la mise en ligne

Par ordre d'importance.

### 0. Remettre la page Réalisations en ligne

Cette page existe et fonctionne, mais elle **n'est liée nulle part** : ni dans
le menu, ni dans le pied de page, ni dans le sitemap, et elle porte une balise
`noindex`. Un portfolio vide dessert plus qu'il ne sert — mieux vaut pas de
page qu'une page avec six cadres vides.

Pour la remettre en circulation une fois les photos déposées :

1. Déposer les six images dans `assets/img/realisations/` (noms attendus dans
   le `LISEZ-MOI.md` du dossier)
2. Remettre `<a href="realisations.html">Réalisations</a>` dans le menu et le
   pied de page des neuf pages
3. Retirer `noindex` de `realisations.html` et remettre son entrée dans
   `sitemap.xml`
4. Sur l'accueil, la section « Un aperçu du travail » a été supprimée : la
   reprendre depuis l'historique git si vous la voulez de nouveau

### 1. Déposer les visuels manquants

Trois visuels de la marque ne sont pas encore dans le dossier :

| À déposer sous ce nom | Ce que c'est | Utilisé par |
|---|---|---|
| `assets/img/sandra-grafycom.jpg` | Le visuel « hello, moi c'est Sandra » | `index.html`, `a-propos.html` |
| `assets/img/realisations/*.jpg` | Les six photos du portfolio | `realisations.html` |

Tant qu'un fichier manque, la page affiche un cadre pointillé nommant le visuel
attendu, au lieu d'une icône d'image cassée. Rien n'est cassé, mais rien n'est
vendeur non plus : c'est le premier point à traiter.

Les deux logos, eux, sont bien en place :
`assets/img/logo-grafycom.jpg` (bandeau, en-tête et pied) et
`assets/img/logo-grafycom-carre.jpg` (héros, favicon, aperçu de partage).

### 2. Compléter les informations légales

Les passages surlignés en jaune dans `mentions-legales.html` et
`confidentialite.html` sont des trous à remplir : raison sociale, statut
juridique, SIRET, TVA, coordonnées de l'hébergeur, médiateur de la
consommation. Rien n'a été inventé — ces mentions sont obligatoires
(art. 6-III de la LCEN) et leur absence est sanctionnée.

L'adresse postale et le nom de famille ont été retirés à la demande de
l'éditrice : voir « Ce qui reste à trancher » plus bas.

### 3. Coordonnées — fait

Téléphone et courriel sont en place partout :

| | |
|---|---|
| **07 82 92 19 81** | pied de page des huit pages, page contact, mentions légales, données structurées. Cliquable sur mobile (`tel:+33782921981`) |
| **sandra.grafycom@gmail.com** | pied de page, page contact, mentions légales, politique de confidentialité, et destinataire du formulaire |

Le jour où une adresse au nom de domaine existe (`contact@grafycom.fr` ou
équivalent), elle inspirera plus confiance qu'une adresse Gmail sur un site
professionnel. La plupart des hébergeurs en fournissent une avec le domaine.
Pour basculer :

```bash
grep -rl 'sandra.grafycom@gmail.com' . | xargs sed -i 's/sandra\.grafycom@gmail\.com/contact@grafycom.fr/g'
```

### 4. Nom de domaine — provisoire

Le site est publié sur **GitHub Pages**, à l'adresse
<https://rezofabrik-hub.github.io/Grafycom/>. Les balises canoniques, le
`sitemap.xml` et le `robots.txt` pointent vers cette adresse.

⚠️ **La majuscule de `Grafycom` compte.** Le dépôt s'appelle `Grafycom`, et
GitHub Pages respecte la casse dans l'URL : `…github.io/grafycom/` renvoie une
erreur 404, `…github.io/Grafycom/` fonctionne. C'est une raison de plus de
basculer vers un vrai nom de domaine, où le problème disparaît.

Le jour où un vrai nom de domaine existe (`grafycom.fr` par exemple), trois
choses à faire :

```bash
# 1. basculer toutes les URL du site
grep -rl 'rezofabrik-hub.github.io/Grafycom' . \
  | xargs sed -i 's#rezofabrik-hub\.github\.io/grafycom#www.grafycom.fr#g'

# 2. déclarer le domaine à GitHub Pages
echo 'www.grafycom.fr' > CNAME

# 3. retirer le préfixe /grafycom/ de la page 404, qui devient inutile
sed -i 's#"/Grafycom/#"/#g' 404.html
```

Puis, chez le bureau d'enregistrement, faire pointer le domaine vers GitHub
Pages (un enregistrement `CNAME` de `www` vers `rezofabrik-hub.github.io`), et
cocher « Enforce HTTPS » dans les réglages Pages une fois le certificat émis.

### 5. Brancher le formulaire de contact

En l'état, le formulaire de `contact.html` **n'envoie rien tout seul** : un site
statique n'a pas de serveur pour traiter un envoi. Au clic sur « Envoyer », il
ouvre le logiciel de messagerie du visiteur avec un message prérempli. Ça
fonctionne, mais une partie des visiteurs abandonnera à cette étape.

Pour un vrai envoi, il suffit d'ajouter un attribut `action` à la balise
`<form>` — dès qu'il est présent, le repli par courriel se désactive tout seul :

```html
<form class="devis" action="https://formspree.io/f/VOTRE-ID" method="POST" data-mailto="sandra.grafycom@gmail.com">
```

Services courants et gratuits pour ce volume : Formspree, Web3Forms, Basin, ou
le formulaire intégré si le site est hébergé chez Netlify.

### 6. Renseigner les réseaux sociaux

Les trois icônes du pied de page pointent vers les accueils de Facebook,
Instagram et LinkedIn. Remplacer par les vraies adresses, ou supprimer les
lignes inutiles (commentaire `À REMPLACER` dans chaque page).

## Référencement local

Quatre pages visent chacune une commune et une requête&nbsp;: «&nbsp;infographiste
Perpignan&nbsp;», «&nbsp;graphiste Canet-en-Roussillon&nbsp;», «&nbsp;graphiste
Argelès-sur-Mer&nbsp;», «&nbsp;graphiste Céret&nbsp;». Elles sont liées depuis le
pied de page de toutes les pages et déclarées dans le `sitemap.xml`.

**Quatre, et pas onze.** Décliner la même page sur tout le département produit
ce que Google appelle des pages satellites, et les déclasse. Chaque page dit ici
quelque chose de vrai et de différent sur son territoire&nbsp;: le secteur
patrimonial protégé à Perpignan, la double saison à Canet, la signalétique de
camping à Argelès, les étiquettes de producteur à Céret. C'est ce qui fait la
différence entre une page utile et une page de remplissage.

Pour en ajouter une&nbsp: copier un bloc de `villes.py`, et n'écrire la page que
si vous avez réellement quelque chose de spécifique à dire sur la commune. Sinon,
mieux vaut s'abstenir.

### Titres et descriptions

Tous les titres tiennent en 60 caractères et les descriptions en 155&nbsp;: au-delà,
Google tronque. Un contrôle&nbsp;:

```bash
python3 - <<'EOF'
import re, glob
for p in sorted(glob.glob('*.html')):
    s = open(p, encoding='utf-8').read()
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    d = re.search(r'name="description" content="(.*?)"', s, re.S)
    if t and len(t.group(1)) > 60: print('titre long :', p)
    if d and len(d.group(1)) > 155: print('description longue :', p)
EOF
```

### Ce qui reste à faire pour le référencement

1. **Acheter le nom de domaine** — voir `basculer-domaine.sh`
2. **Créer la fiche Google Business Profile** — gratuite, et pour une activité
   locale elle pèse souvent plus lourd que le site lui-même. Le mode «&nbsp;zone de
   chalandise&nbsp;» permet de ne pas afficher d'adresse publiquement.
3. **Déclarer le site dans Google Search Console** et y soumettre le sitemap
4. **Remettre la page Réalisations** avec de vraies photos&nbsp;: c'est le contenu
   qui manque le plus

## Ce qui reste à trancher

### L'adresse et le nom de famille

La page de mentions légales publie aujourd'hui : Grafycom, Sandra, le
téléphone, le courriel et « Perpignan (66) — adresse postale communiquée sur
demande ». Ni adresse complète, ni nom de famille, conformément à la demande.

Il faut le savoir : l'article 6-III de la LCEN impose, pour un site
professionnel, **l'adresse du siège et le nom complet du responsable de la
publication**. En l'état, la page n'y répond pas entièrement. Le risque est
faible en pratique pour une petite structure, mais il existe, et il se
matérialise surtout en cas de litige avec un client ou de signalement.

Trois façons de régler ça sans publier une adresse personnelle :

1. **Une société de domiciliation** — une adresse commerciale à Perpignan pour
   quelques dizaines d'euros par mois, utilisable au registre comme sur le site.
2. **Un espace de coworking** qui propose la domiciliation dans son offre.
3. **Publier l'adresse professionnelle déclarée au registre**, qui est de toute
   façon déjà consultable publiquement sur l'annuaire des entreprises de
   l'INSEE dès lors que l'entreprise est immatriculée — ce point vaut la peine
   d'être vérifié avant de chercher une solution à un problème qui n'existe
   peut-être plus.

Pour le nom de famille, la mention « Directrice de la publication : Sandra »
reste incomplète au regard du texte. À arbitrer en connaissance de cause.

Un rappel de tout ceci est laissé en commentaire HTML dans
`mentions-legales.html`, pour la personne qui reprendra le fichier.

## Direction artistique

Reprise des visuels de la marque, pas inventée :

| | |
|---|---|
| **Fond** | Beige nude chaud (`--creme` `#f7f1ef`, `--sable` `#efe4dd`), comme les publications Instagram |
| **Texte** | Brun chaud (`--brun` `#6d5a50`) sur titres presque noirs (`--encre` `#2f2723`) |
| **Accent** | Le dégradé aquarelle du logo, du bleu au jaune — réservé aux titres clés, aux boutons d'action et aux pictogrammes |
| **Titres** | Playfair Display, le serif des visuels |
| **Texte courant** | Inter |
| **Accents manuscrits** | Caveat, pour les « hello, moi c'est… » |
| **Petites capitales** | Courier Prime, la machine à écrire de la signature du logo |

Toutes les couleurs sont des variables CSS en haut de `assets/style.css` :
changer une teinte se fait à un seul endroit.

## Ce qui n'a pas été inventé

Trois choix délibérés, à assumer ou à corriger :

- **Aucun tarif affiché.** La page `prestations.html` explique pourquoi et
  renvoie au devis. Si vous voulez afficher des prix d'appel, la section
  « Combien ça coûte ? » est prête à les accueillir.
- **Aucun faux témoignage.** Le bloc d'avis de `realisations.html` est
  volontairement vide, avec une invitation à en déposer de vrais. Publier des
  avis inventés est une pratique commerciale trompeuse (art. L121-2 du code de
  la consommation), sanctionnée par la DGCCRF.
- **Aucun chiffre non vérifiable** (nombre de clients, de projets, taux de
  satisfaction). Seul « +7 ans d'expertise » apparaît, repris de vos visuels.

## Hébergement — GitHub Pages

Le site est servi directement depuis la branche `main` de ce dépôt, sans
workflow ni étape de construction. Un `git push` met le site à jour ; la
publication prend une à deux minutes.

**Réglage (à faire une fois, dans Settings → Pages) :** source « Deploy from a
branch », branche `main`, dossier `/ (root)`.

À savoir :

- GitHub Pages sur un **dépôt privé** demande un abonnement payant (Pro ou
  plus). Sur un compte gratuit, le dépôt doit être **public**. Le code d'un
  site vitrine n'a rien de confidentiel — c'est exactement ce que le navigateur
  de chaque visiteur télécharge — mais le dépôt public rend aussi visibles le
  README et l'historique des commits.
- Le fichier `.nojekyll` désactive le traitement Jekyll : les fichiers sont
  servis tels quels.
- `404.html` s'affiche pour toute adresse inconnue. Ses chemins sont absolus
  (`/grafycom/…`) car elle peut être servie depuis n'importe quel niveau
  d'URL, où des chemins relatifs casseraient.
- HTTPS est automatique et gratuit.
- `robots.txt` n'est **pas** lu sur une page de projet : les robots ne le
  consultent qu'à la racine du domaine, qui n'appartient pas à ce dépôt. Les
  pages légales restent exclues de l'indexation par leur balise
  `<meta name="robots" content="noindex">`.

Une fois en ligne, déclarer le site dans Google Search Console et y soumettre
`sitemap.xml`.

## Confidentialité et polices externes

Les polices (Google Fonts) et les icônes (Font Awesome via cdnjs) sont chargées
depuis des serveurs tiers. Aucun cookie n'est déposé, mais ces services voient
l'adresse IP des visiteurs. Pour une conformité RGPD maximale, télécharger les
fichiers et les servir depuis `assets/` — la politique de confidentialité
mentionne déjà ce point.

Si vous ajoutez un outil de statistiques, un pixel Meta ou une carte Google
Maps, `confidentialite.html` doit être mis à jour et un bandeau de consentement
devient obligatoire.
