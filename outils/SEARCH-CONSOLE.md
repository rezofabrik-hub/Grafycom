# Search Console — ce qui est prêt, et les cinq minutes qui restent

Objectif : savoir ce que Google fait du site, et pouvoir lui soumettre le
sitemap. Sans cet outil on référence à l'aveugle.

## Ce que je ne peux pas faire d'ici, et pourquoi

Créer la propriété demande d'être connecté au compte Google qui la
possédera. Je n'ai pas d'accès à la Search Console depuis cette session, et
la validation par DNS est hors de portée : le domaine est chez Gandi et sa
zone est déléguée à Route 53, tenue par le webmaster.

Donc la création reste manuelle. En revanche **tout le reste est prêt** : il
n'y a qu'un jeton à me rapporter, et je m'occupe de la suite.

## Le choix de la méthode

| Méthode | Ce qu'elle couvre | Qui doit agir |
|---|---|---|
| **Préfixe d'URL + balise HTML** | `https://grafycom.fr/` seulement | toi seul, 5 min |
| Propriété de domaine (TXT) | `www`, l'apex, http et https | le webmaster |

**À faire d'abord : le préfixe d'URL avec la balise HTML.** C'est la seule
voie qui ne dépend de personne d'autre, et elle couvre `grafycom.fr`,
c'est-à-dire le site tel qu'il est servi aujourd'hui.

La propriété de domaine viendra en second, quand le webmaster touchera à la
zone pour les enregistrements de l'apex : autant lui demander les deux dans
le même message, l'enregistrement TXT ne coûte rien de plus.

## Les cinq minutes, étape par étape

1. Ouvrir <https://search.google.com/search-console> en étant connecté au
   compte Google qui doit posséder la propriété. **Choisir ce compte avec
   soin** : c'est lui qui recevra les alertes et qui pourra donner les accès.
   Le compte de Sandra est le bon choix si le site est le sien ; sinon le
   tien, en lui donnant ensuite un accès « propriétaire délégué ».
2. « Ajouter une propriété » → colonne de **droite**, « Préfixe de l'URL ».
3. Saisir exactement : `https://grafycom.fr/`
4. Dans la liste des méthodes de validation, déplier **« Balise HTML »**.
   Google affiche une ligne de ce genre :

   ```html
   <meta name="google-site-verification" content="AbC123dEf456..." />
   ```

5. **Me rapporter la valeur du `content`** — uniquement la chaîne entre les
   guillemets, pas la balise entière. Ce n'est pas un secret : elle est
   destinée à être lue par tout le monde dans le code de la page. Tu peux la
   coller ici sans crainte.
6. Je la place dans `generateurs/gen.py`, je régénère les 27 pages, je pousse,
   et je te dis quand c'est en ligne. Il te reste à cliquer « Valider ».

### Si tu préfères te passer de moi

Dans `generateurs/gen.py`, la constante existe déjà :

```python
GOOGLE_VERIF = ""
```

Y coller le jeton entre les guillemets, puis régénérer :

```bash
cd generateurs
for p in p_index p_prestations p_methode p_apropos p_contact p_merci \
         p_legal p_cgv p_realisations p_cibles zone \
         villes villes2 villes3 villes4 villes5 villes6 p_construction; do
  python3 "$p.py"
done
cd .. && bash build.sh
git add -A && git commit -m "Jeton de validation Search Console" && git push
```

La balise part alors sur toutes les pages d'un coup, et elle y restera :
Google revérifie la propriété régulièrement et la révoque si la balise
disparaît.

## ⚠️ Le fichier à ne jamais supprimer

`googled06dc63854d9f4a5.html`, à la racine du dépôt, est la preuve de
propriété. Il ne contient qu'une ligne :

```
google-site-verification: googled06dc63854d9f4a5.html
```

Google revérifie la propriété régulièrement. **Si ce fichier disparaît,
l'accès à la Search Console est révoqué** — et avec lui l'historique des
performances. Il reste donc en place pour toujours, même après la
validation. Ce n'est pas un fichier de travail, c'est une serrure.

La constante `GOOGLE_VERIF` de `generateurs/gen.py` reste disponible pour
la méthode par balise, en second moyen de validation si besoin.

## À faire dès maintenant, sans attendre le 16

Un `noindex` sur la page ne gêne pas la validation : Google lit la page, il
se contente de ne pas l'indexer. Ce qui aurait gêné, c'est l'ancien
`robots.txt` du site, qui portait `Disallow: /` et interdisait toute lecture.
La documentation de Google ne dit pas noir sur blanc si la validation
respecte `robots.txt` — je ne l'affirmerai donc pas — mais la question ne se
pose plus : **le `robots.txt` de chantier autorise maintenant l'exploration**,
et les 29 pages gardent leur `noindex`.

Ce changement n'est pas qu'un confort, il corrige une erreur. `Disallow: /`
combiné à `noindex` est un contresens connu : en interdisant l'exploration
on empêche Google de *lire* le `noindex`, et une adresse citée sur un autre
site peut alors être indexée sans que la consigne ait jamais été vue. En
laissant entrer, les robots lisent la consigne et n'indexent rien. La
protection est meilleure, pas moindre.

Donc :

- valider la propriété **avant** le 16, c'est possible dès aujourd'hui ;
- le 16, dès que `ouvrir-le-site.sh` est poussé, le sitemap est soumis et
  l'exploration démarre le jour même.

Faire l'inverse — ouvrir le site puis créer la propriété une semaine plus
tard — c'est une semaine perdue sur chaque page.

## Le 16, dans la Search Console

1. **Sitemaps** → ajouter `sitemap.xml`. Les 23 adresses indexables y sont
   déjà, `realisations.html` comprise.
2. **Inspection de l'URL** → pour chacune des six pages qui comptent,
   « Demander une indexation ». Le quota est d'une dizaine par jour, donc
   dans cet ordre :
   `/` · `/prestations.html` · `/infographiste-perpignan.html` ·
   `/enseigne-perpignan.html` · `/graphiste-restaurant-perpignan.html` ·
   `/realisations.html`
3. **Pages** (ex-Couverture) → revenir au bout d'une semaine. Les deux
   diagnostics à surveiller : « Explorée, actuellement non indexée » (contenu
   jugé faible, il faudra étoffer) et « Bloquée par robots.txt » (il ne doit
   plus rien y avoir, à part `/merci.html`).
4. **Expérience / Signaux web essentiels** → le site est en HTML statique
   sans JavaScript de suivi, ça devrait être vert d'emblée.

## Bing, Yandex, Qwant, Ecosia : déjà automatisé

Pas besoin de Search Console pour eux, et c'est fait :

```bash
python3 outils/indexnow.py           # soumet les 23 adresses du sitemap
python3 outils/indexnow.py --essai   # montre sans envoyer
```

La clé publique est le fichier `a6219de595ef8c82f49d9b389ab001a1.txt` à la
racine du dépôt ; `build.sh` la publie. Le script **refuse de s'exécuter**
tant que `robots.txt` interdit le site : il n'y a rien à gagner à soumettre
des pages fermées, et ça se retient contre le domaine. Il se lance donc
le 16, après `ouvrir-le-site.sh`.

Côté Google il n'y a pas d'équivalent : l'ancien `ping?sitemap=` a été
supprimé en 2023, le sitemap dans la Search Console est la seule voie.

Un compte **Bing Webmaster Tools** reste utile ensuite — il sait importer la
propriété depuis la Search Console en un clic, et Bing alimente aussi les
réponses de ChatGPT et de Copilot, ce qui commence à compter.
