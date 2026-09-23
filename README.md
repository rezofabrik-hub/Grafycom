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

## ⚠ Le site est en mode chantier

La racine `https://www.grafycom.fr/` affiche une **page d'attente** : logo,
promesse en une phrase, téléphone et courriel. L'activité ne s'arrête pas — un
visiteur qui arrive peut appeler ou écrire.

Le site complet reste **accessible et fonctionnel** à `accueil.html` et aux
autres adresses, mais :

- toutes les pages portent `noindex, nofollow` ;
- `robots.txt` interdit l'exploration ;
- un lien discret « Aperçu du site en préparation » figure en bas de la page
  d'attente, pour vous et vos relecteurs.

### Ouvrir le site au public

Quand tout est prêt&nbsp;:

```bash
./fin-de-construction.sh
git add -A && git commit -m "Ouverture du site" && git push
```

Le script remet `accueil.html` à la racine sous le nom `index.html`, repointe
les liens internes, retire le lien d'aperçu, rend les pages indexables et
rétablit le `robots.txt` normal.

Si vous régénérez les pages depuis les scripts de génération, pensez à passer
`CONSTRUCTION = False` dans `gen.py`.

### Avant d'ouvrir — la liste

1. Les six photos du portfolio, et la page Réalisations remise dans le menu
2. Les mentions légales complètes : raison sociale, statut, SIRET, TVA, hébergeur
3. Le formulaire de contact branché sur un service d'envoi
4. Le domaine nu `grafycom.fr` qui redirige vers `www`
5. HTTPS forcé dans les réglages GitHub Pages

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
| `MENTIONS-DEVIS.md` | Textes prêts à coller dans les devis (hors site) |
| `cgv.html` | Conditions générales de vente — professionnels et particuliers |
| `mentions-legales.html` | Obligatoires — complètes |
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

### 2. Informations légales — fait

Les mentions légales sont renseignées d'après le registre national des
entreprises&nbsp;: Grafycom, nom commercial de **Sandra Martinez Gala**,
entrepreneur individuel, SIREN 999 556 301, SIRET 999 556 301 00011, TVA non
applicable (art. 293 B du CGI). L'hébergeur (GitHub,&nbsp;Inc.) et la date de
mise à jour y figurent également.

Les **conditions générales de vente** sont rédigées (`cgv.html`), avec les
régimes distincts pour les clients professionnels et pour les consommateurs&nbsp;:
devis, acomptes, allers-retours, bon à tirer, cession de droits au sens de
l'article L131-3 du CPI, droit de rétractation et formulaire type.

Les mentions à faire figurer sur les devis — dont la renonciation au droit de
rétractation — sont rassemblées dans `MENTIONS-DEVIS.md`, à la racine du dépôt.

⚠ **Ces textes doivent être relus par un juriste avant usage.**

### Le choix du tout-professionnel

Grafycom ne contracte **qu'avec des clients professionnels** — entreprises,
commerçants, artisans, professions libérales, associations, collectivités. Ce
n'est pas un détail de rédaction&nbsp;: c'est ce qui dispense de deux obligations
qui ne s'appliquent qu'aux consommateurs.

- **L'adhésion à un médiateur de la consommation** (article L612-1), qui est un
  abonnement annuel payant.
- **Le droit de rétractation de quatorze jours** sur les contrats conclus à
  distance, qui permet à un client de tout annuler après deux semaines de
  travail.

Les mentions légales et les CGV sont rédigées en conséquence, et la mention de
qualité à faire signer sur chaque devis figure dans `MENTIONS-DEVIS.md`.

⚠ **Ce positionnement ne vaut que s'il est tenu.** Accepter un seul particulier
fait renaître les deux obligations pour ce contrat. Si Grafycom décide un jour
d'ouvrir aux particuliers, il faudra adhérer à un médiateur et rétablir les
sections retirées — l'historique git les conserve.

**L'adresse du siège n'est pas publiée**, à la demande de l'éditrice. Elle est
pourtant publique au registre national des entreprises, et
l'article 6-III de la LCEN l'exige. Voir «&nbsp;Ce qui reste à trancher&nbsp;».

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

### 4. Nom de domaine — fait

Le site est publié sur **https://www.grafycom.fr**. Les balises canoniques, le
`sitemap.xml`, le `robots.txt` et les chemins de la page 404 pointent vers cette
adresse, et le fichier `CNAME` la déclare à GitHub Pages.

L'ancienne adresse `rezofabrik-hub.github.io/Grafycom/` est redirigée
automatiquement par GitHub.

**Reste à vérifier :** le domaine nu `grafycom.fr` (sans `www`) ne résolvait pas
au moment de la bascule. Pour qu'il redirige lui aussi, il faut quatre
enregistrements `A` sur `@` dans Route 53 — voir `MISE-EN-LIGNE.md`.

### 5. Brancher le formulaire de contact

Le formulaire est **entièrement câblé**, il ne lui manque que trois secrets
Cloudflare. Il n'utilise aucun service de formulaire tiers&nbsp;: le message part
du Worker (`src/index.js`) vers **Resend**, sur votre propre domaine.

En attendant, `FORMULAIRE_ACTIF = False` dans les scripts de génération&nbsp;:
le formulaire ouvre la messagerie du visiteur avec un message prérempli, comme
avant. GitHub Pages ne sait pas exécuter de code, donc l'activer maintenant
casserait l'envoi.

#### Ce qu'il reste à faire, une fois le site sur Cloudflare

1. **Créer une clé d'API Resend** — [resend.com](https://resend.com) →
   API Keys → Create.
2. **Déclarer trois secrets** dans Cloudflare → Workers &amp; Pages → le projet →
   Settings → Variables and Secrets&nbsp;:

   | Secret | Contenu |
   |---|---|
   | `RESEND_API_KEY` | la clé créée à l'étape 1 |
   | `CONTACT_TO` | l'adresse qui reçoit les demandes |
   | `CONTACT_FROM` | l'expéditeur, par exemple `Grafycom <contact@grafycom.fr>` — le domaine doit être vérifié chez Resend. Sans ce secret, l'expéditeur est `onboarding@resend.dev`, qui ne délivre qu'au titulaire du compte Resend&nbsp;: pratique pour tester, insuffisant en production. |

3. **Passer `FORMULAIRE_ACTIF = True`** et régénérer les pages, ou ajouter à la
   main `action="/api/contact" method="POST"` sur la balise `<form>` de
   `contact.html`.

#### Changer l'adresse de réception

C'est le secret `CONTACT_TO`, **pas le code**. Modifier la valeur dans
l'interface Cloudflare suffit — rien à redéployer, rien à recommiter. C'est ce
qui permet de recevoir les demandes sur une adresse pendant la mise au point,
puis de basculer sur celle de Sandra en trente secondes.

L'adresse affichée sur le site reste indépendante&nbsp;: c'est `MAIL` dans les
scripts de génération.

#### Ce que fait le Worker

Il vérifie le pot de miel, contrôle que le nom, le courriel et le message sont
présents et plausibles, limite leur longueur, puis appelle Resend en plaçant
l'adresse du visiteur en `reply_to` — un simple « Répondre » suffit.

En cas de succès il redirige vers `merci.html`&nbsp;; en cas d'échec vers
`contact.html?erreur=…`, et la page affiche alors un message qui distingue le
champ manquant de la panne d'envoi.


### 6. Renseigner les réseaux sociaux

Les trois icônes du pied de page pointent vers les accueils de Facebook,
Instagram et LinkedIn. Remplacer par les vraies adresses, ou supprimer les
lignes inutiles (commentaire `À REMPLACER` dans chaque page).

## Référencement local

**Douze pages de commune**, chacune visant une requête précise, plus une page
**Zone d'intervention** qui liste les 226 communes du département.

| Page | Angle |
|---|---|
| `infographiste-perpignan.html` | Secteur protégé, autorisations d'enseigne, clientèle catalane |
| `graphiste-canet-en-roussillon.html` | Double saison, sel et tramontane |
| `graphiste-saint-cyprien.html` | Port de plaisance, résidences de tourisme |
| `graphiste-argeles-sur-mer.html` | Signalétique de camping, multilingue |
| `graphiste-le-barcares.html` | Camping, événementiel, calendrier de saison |
| `graphiste-elne.html` | Producteurs de la plaine, centre ancien |
| `graphiste-rivesaltes.html` | Étiquettes de vin, artisans de la zone d'activité |
| `graphiste-thuir.html` | Gammes de cuvées, accueil au caveau |
| `graphiste-collioure.html` | Site protégé, appellations, galeries |
| `graphiste-ceret.html` | Étiquettes de producteur, vie associative |
| `graphiste-prades.html` | Affiches de festival, montagne |
| `graphiste-font-romeu.html` | Saison inversée, sport de haut niveau |
| `zone-intervention.html` | Les 12 pages + les 226 communes |

**Douze, et pas 226.** Le département compte 226 communes, dont 138 de moins de
mille habitants. Une page par commune serait un cas d'école de ce que Google
appelle des pages satellites&nbsp;: la sanction ne frappe pas seulement ces
pages, elle frappe le domaine entier. Et personne ne cherche «&nbsp;graphiste à
Campoussy&nbsp;», 28 habitants.

Chaque page dit donc quelque chose de vrai et de distinct sur son territoire.
La page Zone d'intervention capte le reste&nbsp;: nommer 226 communes sur une
page utile n'est pas une page satellite, c'est une information.

La liste des communes vient du répertoire officiel (`geo.api.gouv.fr`).

### Pour ajouter une commune

Copier un bloc dans `villes.py` à `villes6.py` — et n'écrire la page que si vous
avez réellement quelque chose de spécifique à dire. Sinon, s'abstenir&nbsp;: la
mention dans la page Zone d'intervention suffit.

### Titres et descriptions

Tous les titres tiennent en 60 caractères, toutes les descriptions en 155&nbsp;:
au-delà, Google tronque. Contrôle&nbsp;:

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

## Ce qui reste à trancher

### L'adresse du siège

Le nom complet de l'éditrice est désormais publié, comme la loi l'exige.
L'adresse du siège, elle, ne l'est pas&nbsp;: la page indique «&nbsp;Perpignan
(66000) — adresse postale communiquée sur demande&nbsp;».

L'article 6-III de la LCEN impose l'adresse de l'établissement. La page n'y
répond donc pas entièrement. À noter&nbsp;: cette adresse est **déjà publique**
au registre national des entreprises, consultable par quiconque tape
«&nbsp;Grafycom&nbsp;» sur `annuaire-entreprises.data.gouv.fr`. La taire sur le
site ne protège donc rien&nbsp;; c'est un choix d'affichage, pas de
confidentialité.

Trois façons de régler ça&nbsp;:

1. **Publier l'adresse du siège**, puisqu'elle est déjà accessible.
2. **Une société de domiciliation** — une adresse commerciale à Perpignan pour
   quelques dizaines d'euros par mois, à déclarer au registre comme sur le site.
3. **Un espace de coworking** proposant la domiciliation.

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

## Sécurité et confidentialité

**Aucune ressource externe.** Polices (`assets/fonts/`) et icônes
(`assets/fa/`) sont servies depuis le site. Le navigateur d'un visiteur ne
contacte aucun serveur tiers&nbsp;: ni Google, ni cdnjs. Personne d'autre que
l'hébergeur ne voit son adresse IP.

Ce n'est pas qu'une question de sécurité&nbsp;: un site qui charge ses polices
chez Google transmet l'IP de chacun de ses visiteurs à Google. Plusieurs
décisions européennes ont jugé cette pratique contraire au RGPD.

**Politique de sécurité de contenu.** Chaque page porte une balise
`Content-Security-Policy` qui interdit&nbsp;:

- tout script qui ne vient pas du site (`script-src 'self'`) — la protection
  principale contre l'injection de code&nbsp;;
- toute ressource, police ou image extérieure&nbsp;;
- l'affichage du site dans un cadre tiers (`frame-ancestors 'none'`), ce qui
  bloque le détournement de clic&nbsp;;
- les greffons et objets embarqués (`object-src 'none'`).

Un `Referrer-Policy` limite par ailleurs ce qui est transmis aux sites que vos
visiteurs atteignent depuis le vôtre.

**Aucun cookie**, aucun traceur, aucune mesure d'audience. Pas de bandeau de
consentement à afficher, puisqu'il n'y a rien à consentir.

**HTTPS** est actif, avec redirection automatique depuis HTTP.

### La limite de GitHub Pages

GitHub Pages ne permet pas de définir d'en-têtes HTTP. Trois protections
restent donc hors de portée&nbsp;: `Strict-Transport-Security` (HSTS),
`X-Frame-Options` et `X-Content-Type-Options`. La balise CSP couvre l'essentiel
de ce que ferait `X-Frame-Options`, mais pas les deux autres.

Un hébergeur permettant les en-têtes personnalisés — Cloudflare&nbsp;Pages ou
Netlify, gratuits tous les deux — les rendrait possibles via un fichier
`_headers`. C'est aussi la condition pour garder le dépôt privé.

### Si vous ajoutez quelque chose

Tout outil externe (statistiques, pixel publicitaire, carte, service de
formulaire) sera **bloqué par la CSP** tant que son domaine n'y est pas ajouté.
C'est voulu&nbsp;: cela oblige à un choix conscient. Le cas échéant, modifier la
directive concernée dans `gen.py`, et mettre à jour `confidentialite.html`.

