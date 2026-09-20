# Mise en ligne du site Grafycom — note au webmaster

Document de passation. Tout ce qu'il faut pour brancher le site sur son nom de
domaine définitif.

---

## 1. Ce qu'est ce site

Un site **statique** : neuf pages HTML, une feuille de style, un fichier
JavaScript, des images. **Aucune base de données, aucun PHP, aucun CMS, aucune
étape de build.** Il fonctionne en le déposant tel quel sur n'importe quel
serveur web.

- **Dépôt** : <https://github.com/rezofabrik-hub/Grafycom>
- **Branche de production** : `main`
- **Racine du site** : la racine du dépôt (`index.html` est à la racine)
- **Adresse provisoire actuelle** : <https://www.grafycom.fr/>

---

## 2. Option A — rester sur GitHub Pages (recommandé)

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
dig +short www.grafycom.fr CNAME
```

> Note : une zone hébergée Route 53 est facturée environ 0,50 $ par mois. Le DNS
> inclus chez la plupart des bureaux d'enregistrement ferait le même travail
> gratuitement — sans urgence, mais bon à savoir.

### 2.2 Côté GitHub

Dans **Settings → Pages → Custom domain**, saisir le domaine retenu
(`www.grafycom.fr` recommandé) et valider. GitHub vérifie le DNS, puis émet un
certificat Let's Encrypt — comptez de quelques minutes à quelques heures.

Une fois le certificat émis, **cocher « Enforce HTTPS »**.

GitHub redirige automatiquement l'autre forme du domaine (nu ↔ `www`) ainsi que
l'ancienne adresse `www.grafycom.fr/` vers le domaine
configuré. Rien à faire de plus côté redirections.

### 2.3 Côté dépôt — une commande

Le site est actuellement servi dans un **sous-dossier** (`/Grafycom/`). Sur un
domaine propre, il passe à la racine : les URL canoniques, le sitemap et les
chemins absolus de la page 404 doivent suivre. Un script s'en charge :

```bash
git clone https://github.com/rezofabrik-hub/Grafycom.git
cd Grafycom
./basculer-domaine.sh www.grafycom.fr
git add -A
git commit -m "Bascule sur www.grafycom.fr"
git push
```

Le script modifie les URL du site, corrige `404.html` et crée le fichier
`CNAME` attendu par GitHub Pages.

---

## 3. Option B — héberger ailleurs

Si vous préférez un hébergement mutualisé classique, c'est possible sans rien
changer au code : **déposez le contenu du dépôt à la racine web** (`www/`,
`public_html/`…) par FTP ou rsync, en excluant `.git/`, `README.md`,
`MISE-EN-LIGNE.md` et `basculer-domaine.sh`.

Dans ce cas :

- pointez le domaine vers le serveur selon les indications de l'hébergeur
  (souvent un `A` vers son IP) ;
- **activez HTTPS** (Let's Encrypt est gratuit chez tous les hébergeurs) ;
- lancez tout de même `./basculer-domaine.sh votre-domaine.fr` avant l'envoi,
  pour que les URL internes soient correctes ;
- les mises à jour ne se feront plus par `git push` mais par un nouvel envoi de
  fichiers.

---

## 4. Points d'attention

**Le formulaire de contact n'envoie rien.** Un site statique n'a pas de serveur
pour traiter un envoi : au clic, le formulaire ouvre le logiciel de messagerie
du visiteur avec un message prérempli. Pour un vrai envoi, ajouter un attribut
`action` à la balise `<form>` de `contact.html` (Formspree, Web3Forms, Basin,
ou le formulaire intégré de Netlify) — dès que cet attribut est présent, le
repli par courriel se désactive tout seul.

**Polices et icônes sont chargées depuis des CDN** (Google Fonts, cdnjs). Aucun
cookie n'est déposé, mais ces services voient l'IP des visiteurs. Pour une
conformité RGPD maximale, les télécharger et les servir depuis `assets/`.

**Les mentions légales sont incomplètes.** Raison sociale, statut juridique,
SIRET, TVA et coordonnées de l'hébergeur restent à renseigner — les passages
concernés sont surlignés en jaune dans `mentions-legales.html`. À compléter
avant toute communication publique.

**La page `realisations.html` est volontairement hors ligne** : elle existe mais
n'est liée nulle part et porte un `noindex`, en attendant de vraies photos. La
marche à suivre pour la remettre en circulation est en tête du `README.md`.

**Après la bascule**, déclarer le site dans Google Search Console avec la
nouvelle adresse et y soumettre `sitemap.xml`.

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
| Contact | Sandra — 07 82 92 19 81 — sandra.grafycom@gmail.com |
