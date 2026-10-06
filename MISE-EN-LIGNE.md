# Mise en ligne du site Grafycom — note au webmaster

Document de passation. Tout ce qu'il faut pour brancher le site sur son nom de
domaine définitif.

---

## 1. Ce qu'est ce site

Un site **statique** : vingt-cinq pages HTML, une feuille de style, un fichier
JavaScript, des polices, des icônes et des images. **Aucune base de données,
aucun PHP, aucun CMS.** Il fonctionne en le déposant tel quel sur n'importe
quel serveur web.

- **Dépôt** : <https://github.com/rezofabrik-hub/Grafycom>
- **Branche de production** : `main`
- **Racine du site** : la racine du dépôt
- **Adresse actuelle** : <https://grafycom.fr/>

**Le site est en mode chantier jusqu'au 16 octobre 2026.** La racine sert une
page d'attente ; le vrai site vit dans `accueil.html` et toutes les pages
portent un `noindex`. Le script `./ouvrir-le-site.sh` fait la bascule : la page
d'accueil reprend sa place à la racine, les moteurs sont autorisés, et il
refuse de rendre la main si quelque chose ne va pas.

**Les pages HTML sont générées.** Les scripts qui les produisent sont dans
`generateurs/`, avec un LISEZ-MOI. Modifier un fichier HTML à la main marche
jusqu'à la prochaine régénération, qui écrase la correction sans prévenir. Tout
passe par les générateurs.

**Deux fichiers ne sont pas publiés en l'état** : `build.sh` construit `dist/`,
qui contient le site public et rien d'autre — ni documentation, ni scripts, ni
générateurs. C'est `dist/` qui part en ligne chez Cloudflare. Sur GitHub Pages,
c'est la racine du dépôt qui est servie.

---

## 2. Option A — GitHub Pages (hébergement actuel)

C'est la configuration en place. Hébergement gratuit, HTTPS automatique,
mise à jour par simple `git push`. Il n'y a qu'à brancher le domaine.

### 2.1 Enregistrements DNS à créer

Chez le bureau d'enregistrement du domaine (OVH, Gandi, Infomaniak…) :

**Pour le sous-domaine `www` — un enregistrement CNAME :**

| Type | Nom | Valeur | TTL |
|---|---|---|---|
| `CNAME` | `www` | `rezofabrik-hub.github.io.` | 3600 |

**Pour le domaine nu (`grafycom.fr` sans `www`) — quatre A et quatre AAAA :**

| Type | Nom | Valeur | TTL |
|---|---|---|---|
| `A` | `@` | `185.199.108.153` | 3600 |
| `A` | `@` | `185.199.109.153` | 3600 |
| `A` | `@` | `185.199.110.153` | 3600 |
| `A` | `@` | `185.199.111.153` | 3600 |
| `AAAA` | `@` | `2606:50c0:8000::153` | 3600 |
| `AAAA` | `@` | `2606:50c0:8001::153` | 3600 |
| `AAAA` | `@` | `2606:50c0:8002::153` | 3600 |
| `AAAA` | `@` | `2606:50c0:8003::153` | 3600 |

> Ces adresses sont celles publiées par GitHub. Elles changent très rarement,
> mais **à vérifier au moment de la configuration** sur la page officielle :
> <https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site>

Les enregistrements AAAA sont facultatifs ; ils servent aux visiteurs en IPv6.

### 2.1 bis — Marche à suivre sur AWS Route 53

Le DNS du domaine est géré par Route 53. Voici le détail, console AWS ouverte.

> **Attention, piège AWS.** Route 53 ne permet pas de créer un `CNAME` sur le
> domaine nu, et son type **Alias ne fonctionne qu'avec des ressources AWS**
> (CloudFront, S3, ELB) — **pas avec GitHub Pages**. Pour le domaine nu, il faut
> donc obligatoirement des enregistrements **A**, pas un Alias.

**Étape 1 — ouvrir la zone hébergée**

Console AWS → **Route 53** → **Hosted zones** → cliquer sur le domaine.

**Étape 2 — le domaine nu (`grafycom.fr`)**

Bouton **Create record** :

| Champ | Valeur |
|---|---|
| Record name | *laisser vide* |
| Record type | `A` |
| Alias | **désactivé** |
| Value | les quatre IP, **une par ligne** :<br>`185.199.108.153`<br>`185.199.109.153`<br>`185.199.110.153`<br>`185.199.111.153` |
| TTL | `300` |
| Routing policy | Simple routing |

**Étape 3 — le sous-domaine `www`**

De nouveau **Create record** :

| Champ | Valeur |
|---|---|
| Record name | `www` |
| Record type | `CNAME` |
| Alias | désactivé |
| Value | `rezofabrik-hub.github.io` |
| TTL | `300` |

**Étape 4 — IPv6 (facultatif)**

Un enregistrement `AAAA` sur le domaine nu, avec les quatre adresses
`2606:50c0:8000::153` à `2606:50c0:8003::153`, une par ligne.

**À ne pas toucher**

- Les enregistrements **NS** et **SOA** de la zone : ils sont gérés par AWS.
- Les enregistrements **MX**, **TXT/SPF**, **DKIM** s'il y a une messagerie sur
  le domaine — les supprimer couperait les courriels.
- S'il existe déjà un `A`, un `CNAME` ou un Alias sur `@` ou `www` (page
  parking, ancien site), **le supprimer d'abord** : deux enregistrements du même
  type sur le même nom sont en conflit.

**Si le domaine est enregistré ailleurs que chez AWS**

Vérifier que les serveurs de noms déclarés chez le bureau d'enregistrement
correspondent bien aux quatre `NS` affichés en haut de la zone hébergée Route 53.
Sinon, la zone ne sert à rien : c'est l'autre DNS qui répond.

**Délai**

Avec un TTL de 300 secondes, la propagation prend quelques minutes. Contrôle en
ligne de commande :

```bash
dig +short grafycom.fr A
dig +short grafycom.fr CNAME
```

> Note : une zone hébergée Route 53 est facturée environ 0,50 $ par mois. Le DNS
> inclus chez la plupart des bureaux d'enregistrement ferait le même travail
> gratuitement — sans urgence, mais bon à savoir.

### 2.2 Côté GitHub

Dans **Settings → Pages → Custom domain**, saisir le domaine retenu
(`grafycom.fr` recommandé) et valider. GitHub vérifie le DNS, puis émet un
certificat Let's Encrypt — comptez de quelques minutes à quelques heures.

Une fois le certificat émis, **cocher « Enforce HTTPS »**.

GitHub redirige automatiquement l'autre forme du domaine (nu ↔ `www`) ainsi que
l'ancienne adresse `grafycom.fr/` vers le domaine
configuré. Rien à faire de plus côté redirections.

### 2.3 Côté dépôt — une commande

Le site est actuellement servi dans un **sous-dossier** (`/Grafycom/`). Sur un
domaine propre, il passe à la racine : les URL canoniques, le sitemap et les
chemins absolus de la page 404 doivent suivre. Un script s'en charge :

```bash
git clone https://github.com/rezofabrik-hub/Grafycom.git
cd Grafycom
./basculer-domaine.sh grafycom.fr
git add -A
git commit -m "Bascule sur grafycom.fr"
git push
```

Le script modifie les URL du site, corrige `404.html` et crée le fichier
`CNAME` attendu par GitHub Pages.

---

## 2 bis. Passer sur Cloudflare et rendre le dépôt privé

**Pourquoi.** GitHub Pages sur un dépôt privé exige un abonnement payant, et
n'autorise aucun en-tête HTTP personnalisé. Cloudflare sert un dépôt privé sur
son offre gratuite, lit le fichier `_headers` — c'est ce qui permet
`Strict-Transport-Security`, `X-Frame-Options` et la CSP en vrai en-tête — et
exécute le code du formulaire de contact, ce que GitHub Pages ne sait pas faire.

**Workers, pas Pages.** Le dépôt contient `wrangler.toml` et `src/index.js` : le
site part en **Worker avec fichiers statiques**. Le Worker sert `dist/` tel quel
et ne s'exécute que sur `/api/contact`, la route du formulaire. Un projet Pages
ne servirait que les fichiers ; le formulaire resterait mort.

**L'ordre compte.** Rendre le dépôt privé avant que Cloudflare ne serve le site
met celui-ci hors ligne immédiatement. Suivre la séquence.

### 1. Créer le projet

Tableau de bord Cloudflare → **Workers & Pages** → **Create** → **Workers** →
**Import a repository** → autoriser GitHub → choisir `rezofabrik-hub/Grafycom`.

| Champ | Valeur |
|---|---|
| Build command | `bash build.sh` |
| Deploy command | `npx wrangler deploy` |
| Production branch | `main` |

Tout le reste — nom du service, dossier publié, page 404, route du formulaire —
est déjà écrit dans `wrangler.toml`, que Cloudflare lit.

Le premier déploiement donne une adresse en `grafycom.<compte>.workers.dev`.
**Vérifier le site dessus avant d'aller plus loin** : pages, polices, icônes,
page 404.

En ligne de commande, depuis le dépôt, avec un jeton d'API Cloudflare
(`CLOUDFLARE_API_TOKEN`, droits *Workers Scripts: Edit*) :

```bash
bash build.sh
npx wrangler deploy
```

### 2. Les trois secrets du formulaire

Projet → **Settings → Variables and Secrets** → **Add**, type **Secret** :

| Nom | Valeur |
|---|---|
| `RESEND_API_KEY` | clé d'API Resend (`re_…`) |
| `CONTACT_TO` | adresse qui reçoit les demandes |
| `CONTACT_FROM` | expéditeur sur un domaine vérifié chez Resend (facultatif) |

Tant qu'ils manquent, `/api/contact` renvoie une erreur. C'est pourquoi le
formulaire du site reste pour l'instant en mode « ouvre le logiciel de
messagerie » : il ne sera basculé sur `/api/contact` qu'une fois les secrets en
place et un envoi réel vérifié.

### 3. Rattacher le domaine

Un domaine personnalisé sur un Worker exige que **la zone `grafycom.fr` soit
gérée par Cloudflare** : contrairement à Pages, un Worker ne peut pas être
atteint par un simple `CNAME` depuis un DNS extérieur. Aujourd'hui la zone est
sur AWS Route 53. Deux chemins.

**Chemin recommandé — déplacer la zone chez Cloudflare.**

Le domaine est enregistré chez **Gandi** ; seule la zone DNS est déléguée à
Route 53. Changer de DNS se fait donc chez Gandi, pas chez AWS.

L'ordre ci-dessous ne coupe le site à aucun moment : les enregistrements sont
créés chez Cloudflare **avant** la bascule, à l'identique. Pendant la
propagation, les visiteurs sont servis par l'une ou l'autre zone, et les deux
disent la même chose.

1. Cloudflare → **Add a domain** → `grafycom.fr` → offre **Free**. Cloudflare
   recopie les enregistrements existants.
2. **Vérifier la liste importée.** Elle doit contenir quatre `A` sur `www` vers
   `185.199.108.153`, `.109.153`, `.110.153`, `.111.153`, et rien d'autre : la
   zone ne porte ni `MX`, ni `TXT`, ni `CAA` — aucune messagerie ne dépend de
   ce domaine. Si quelque chose d'autre apparaît, l'examiner avant de
   continuer.
3. **Ajouter le domaine nu**, absent aujourd'hui : quatre `A` sur `@` vers les
   mêmes adresses GitHub, et quatre `AAAA` sur `@` vers `2606:50c0:8000::153`
   à `2606:50c0:8003::153`.
4. **Mettre tous ces enregistrements sur « DNS only »** (nuage gris), pas sur
   « Proxied ». GitHub Pages gère lui-même le certificat du domaine, et un
   enregistrement proxifié l'empêche de le valider. Le nuage orange redeviendra
   utile le jour où c'est Cloudflare qui sert le site.
5. Relever les **deux serveurs de noms** que Cloudflare attribue.
6. **Chez Gandi** → le domaine → *Serveurs de noms* → remplacer les quatre
   serveurs AWS par les deux de Cloudflare. Propagation : quelques heures,
   parfois jusqu'à 48 h.
7. Attendre que Cloudflare affiche la zone **Active**, puis vérifier que
   `grafycom.fr` et `grafycom.fr` répondent tous les deux.
8. **Supprimer alors la zone hébergée Route 53**, facturée au mois, et dont
   plus personne ne se sert.

Une fois le site servi par un Worker plutôt que par GitHub Pages, les
enregistrements de l'étape 3 sont remplacés par un *Custom domain* sur le
Worker (**Settings → Domains & Routes → Add → Custom domain**), et le domaine
nu se traite par un `A` sur `@` vers `192.0.2.0` **proxifié** — une adresse
réservée, jamais joignable — accompagné d'une *Redirect Rule* `grafycom.fr/*`
→ `https://grafycom.fr/$1` en 301.

**Chemin sans toucher aux serveurs de noms.** Rester sur Route 53 et créer à la
place un projet **Pages**, qui accepte un `CNAME` depuis un DNS extérieur. Le
formulaire doit alors être réécrit en *Pages Function* (`functions/api/contact.js`
au lieu de `src/index.js`) — une modification courte, mais une modification.

Dans les deux cas, attendre que `https://grafycom.fr` soit servi par
Cloudflare : la réponse porte alors un `cf-ray` au lieu de `server: GitHub.com`.

```bash
curl -sI https://grafycom.fr/ | grep -iE 'server|cf-ray'
```

### 4. Débrancher GitHub Pages

Une fois Cloudflare confirmé : dépôt → **Settings → Pages** → source **None**.
Supprimer aussi le fichier `CNAME` à la racine, qui ne sert qu'à GitHub Pages,
et les anciens enregistrements `A` vers GitHub s'ils subsistent.

### 5. Rendre le dépôt privé

**Settings → General → Danger Zone → Change repository visibility → Private.**

À vérifier ensuite : que le déploiement Cloudflare fonctionne toujours
(l'autorisation GitHub accordée à l'étape 1 survit au passage en privé), et que
`https://grafycom.fr` répond.

### Ce que le passage en privé change vraiment

Le code d'un site vitrine n'a rien de confidentiel : c'est exactement ce que le
navigateur de chaque visiteur télécharge. Ce que le dépôt privé protège, c'est
le reste — `README.md`, `MISE-EN-LIGNE.md`, `MENTIONS-DEVIS.md`, les scripts, et
l'historique des commits, jusqu'ici lisibles et indexés par les moteurs.

`build.sh` écarte déjà ces fichiers du site publié. Le dépôt privé ferme la
seconde porte.

## 3. Option B — héberger ailleurs

Si vous préférez un hébergement mutualisé classique, c'est possible sans rien
changer au code. **Mais n'envoyez pas le dépôt tel quel** : il contient des
scripts, des générateurs, de la documentation interne et des listes de
prospection comportant des noms et des adresses de personnes. Tout cela serait
servi publiquement.

```bash
bash build.sh        # construit dist/ : le site public, et rien d'autre
```

C'est le **contenu de `dist/`** qu'on dépose à la racine web (`www/`,
`public_html/`…), par FTP ou rsync. Le script refuse de construire s'il
rencontre un fichier qui n'a rien à faire en ligne, ce qui évite la mauvaise
surprise.

Dans ce cas :

- pointez le domaine vers le serveur selon les indications de l'hébergeur
  (souvent un `A` vers son IP) ;
- **activez HTTPS** (Let's Encrypt est gratuit chez tous les hébergeurs) ;
- reportez les en-têtes de `_headers` dans la configuration du serveur
  (`.htaccess` chez Apache, un bloc `add_header` chez nginx) : un hébergement
  mutualisé ne lit pas ce fichier ;
- le formulaire de contact restera en repli par courriel, sauf à porter
  `src/index.js` vers le langage du serveur ;
- les mises à jour se feront par un nouvel envoi de fichiers, pas par
  `git push`.

---

## 4. Points d'attention

**Le domaine nu ne résout pas.** Seul `grafycom.fr` répond ; `grafycom.fr`
sans `www` renvoie une erreur. Il manque les enregistrements `A` et `AAAA` sur
l'apex de la zone Route 53 — ils sont détaillés en 2.1. C'est la seule chose à
faire avant l'ouverture du 16 octobre.

**Le formulaire de contact ouvre le logiciel de messagerie du visiteur.** C'est
un repli volontaire : GitHub Pages n'exécute aucun code. La vraie solution est
déjà écrite — `src/index.js` est un Worker Cloudflare qui reçoit le formulaire
sur `/api/contact` et envoie le message via Resend. Elle s'active le jour où
Cloudflare sert le site : définir les trois secrets (section 2 bis), puis
passer `FORMULAIRE_ACTIF` à `True` dans `generateurs/gen.py` et régénérer.
Ne pas brancher un service tiers du type Formspree : le travail est fait.

**Aucune ressource tierce n'est chargée.** Les polices et les icônes sont
servies depuis `assets/`, pas depuis Google Fonts ni un CDN. Aucun cookie,
aucun traceur, aucune adresse IP de visiteur transmise à qui que ce soit. C'est
un choix, et il ne faut pas le défaire en ajoutant une police distante : la
page de confidentialité affirme le contraire au visiteur.

**Les en-têtes de sécurité sont dans `_headers`** — HSTS, CSP, X-Frame-Options,
Referrer-Policy, et les durées de cache. GitHub Pages ignore ce fichier ;
Cloudflare le lit. C'est l'une des raisons du passage à Cloudflare.

**Les mentions légales sont complètes**, de même que les CGV, écrites pour une
clientèle exclusivement professionnelle. Elles n'ont pas été relues par un
juriste : la recommandation tient toujours.

**La page `realisations.html` est volontairement hors ligne** : elle existe mais
n'est liée nulle part et porte un `noindex`, en attendant de vraies photos. La
marche à suivre pour la remettre en circulation est en tête du `README.md`.

**Après l'ouverture**, déclarer le site dans Google Search Console et y
soumettre `https://grafycom.fr/sitemap.xml`.

---

## 5. Récapitulatif des valeurs

| | |
|---|---|
| Dépôt | `https://github.com/rezofabrik-hub/Grafycom` |
| Branche | `main` |
| Dossier publié | racine (`/`) |
| Cible CNAME | `rezofabrik-hub.github.io.` |
| A (IPv4) | `185.199.108.153`, `.109.153`, `.110.153`, `.111.153` |
| AAAA (IPv6) | `2606:50c0:8000::153` à `2606:50c0:8003::153` |
| État | Mode chantier jusqu'au 16 octobre 2026 |
| À faire en priorité | Les `A` et `AAAA` sur l'apex, dans Route 53 |
| Contact | Sandra — 07 82 92 19 81 — sandra.grafycom@gmail.com |
