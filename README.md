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
| `realisations.html` | Portfolio — **à remplir**, voir `assets/img/realisations/LISEZ-MOI.md` |
| `methode.html` | Le déroulé d'un projet en 6 étapes, et ce qui est attendu du client |
| `a-propos.html` | Sandra, le colibri, la double casquette, le bilinguisme |
| `contact.html` | Formulaire de devis détaillé + coordonnées + zone d'intervention |
| `mentions-legales.html` | Obligatoires — **à compléter avant mise en ligne** |
| `confidentialite.html` | RGPD — **à compléter avant mise en ligne** |
| `assets/style.css` | Feuille de style commune |
| `assets/site.js` | Menu mobile, année du copyright, visuels manquants, formulaire |
| `robots.txt`, `sitemap.xml` | Référencement |

L'en-tête et le pied de page sont recopiés dans chaque fichier : pour modifier
le menu ou une mention du pied, il faut passer sur les huit pages.

## À faire avant la mise en ligne

Par ordre d'importance.

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

### 4. Confirmer le nom de domaine

Les balises canoniques, le `sitemap.xml` et `robots.txt` pointent vers
`https://www.grafycom.fr`. Ce domaine est une hypothèse : le vérifier auprès
d'un bureau d'enregistrement. Pour un autre nom :

```bash
grep -rl 'www.grafycom.fr' . | xargs sed -i 's#www\.grafycom\.fr#le-vrai-domaine.fr#g'
```

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

## Hébergement

Un site statique tient sur n'importe quel hébergement mutualisé, et gratuitement
sur Netlify, Cloudflare Pages ou GitHub Pages. Trois points à vérifier :

- **HTTPS activé** (gratuit et automatique chez tous les hébergeurs cités)
- Redirection de `grafycom.fr` vers `www.grafycom.fr`, ou l'inverse — une seule
  des deux versions doit répondre, pour ne pas diviser le référencement
- Une fois en ligne, déclarer le site dans Google Search Console et y soumettre
  `sitemap.xml`

## Confidentialité et polices externes

Les polices (Google Fonts) et les icônes (Font Awesome via cdnjs) sont chargées
depuis des serveurs tiers. Aucun cookie n'est déposé, mais ces services voient
l'adresse IP des visiteurs. Pour une conformité RGPD maximale, télécharger les
fichiers et les servir depuis `assets/` — la politique de confidentialité
mentionne déjà ce point.

Si vous ajoutez un outil de statistiques, un pixel Meta ou une carte Google
Maps, `confidentialite.html` doit être mis à jour et un bandeau de consentement
devient obligatoire.
