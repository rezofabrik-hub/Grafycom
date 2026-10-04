# L'envoi du matin — comment ça marche, et ce qu'il reste à brancher

Chaque matin ouvré, Sandra reçoit la liste des entreprises qui viennent de
se créer dans les Pyrénées-Orientales, triées par intérêt pour son métier.

```bash
python3 outils/veille-entreprises.py --quotidien --adresses \
        --envoyer sandra.grafycom@gmail.com --copie rezofabrik@gmail.com
```

---

## Pourquoi pas Infogreffe

C'est la question de départ, et la réponse est nette : **Infogreffe serait
un recul.**

| | BODACC (utilisé) | Infogreffe |
|---|---|---|
| Source | publication officielle des immatriculations | les mêmes greffes |
| Accès | API ouverte, sans clé | API sur contrat, payante |
| Tarif | gratuit | à l'acte ou à l'abonnement |
| Connecteur disponible ici | — | aucun |
| Adresses e-mail | aucune | **aucune non plus** |

Les deux regardent le même registre. Le BODACC *est* le canal par lequel
les greffes publient les immatriculations : c'est la source, pas une copie.
Infogreffe revend l'accès à ces mêmes données avec des extraits
certifiés — utile pour un K-bis, inutile pour de la prospection.

Donc : rien à brancher, rien à payer, et c'est déjà en place.

## Pourquoi il n'y aura pas d'adresses e-mail

Il faut le dire franchement : **aucune de ces sources ne publie d'adresse
e-mail**, et ce n'est pas un défaut de l'outil. Ni le BODACC, ni
Infogreffe, ni le répertoire Sirene de l'INSEE, ni l'Annuaire des
Entreprises de l'État ne collectent les courriels des entreprises. Ils n'en
ont pas.

Les services qui prétendent en fournir les ont aspirés ailleurs — sur les
sites, les réseaux, les annuaires. Acheter ces listes pose deux problèmes :
la qualité (adresses mortes, mauvais interlocuteur) et le droit. La
prospection B2B par courriel est permise sans accord préalable si le message
concerne l'activité professionnelle du destinataire et comporte un moyen de
refus — mais ça suppose une adresse obtenue loyalement, ce que n'est pas une
liste aspirée.

**Ce que l'outil donne à la place**, et qui marche :

- le nom et la forme de l'entreprise ;
- la ville et le code postal ;
- l'activité déclarée, en clair ;
- l'adresse postale, vérifiée auprès de l'INSEE ;
- le nom du dirigeant, pour adresser le courrier ;
- le SIREN et la date de début d'activité.

Donc : courrier, téléphone après recherche du numéro, ou passage. Pour un
commerce qui vient d'ouvrir à Perpignan, passer la porte avec un carton
d'exemples vaut mieux qu'un courriel de masse — et c'est d'ailleurs ce que
les agences du département ne font pas.

Le modèle de courrier et le cadre légal sont dans `PROSPECTION.md`.

---

## Ce que fait le mode `--quotidien`

1. **Fenêtre de sept jours, pas d'un seul.** Le BODACC publie avec deux à
   cinq jours de décalage et ne publie pas le week-end. Une fenêtre d'un
   jour raterait des créations, et toutes celles du samedi et du dimanche.
2. **Mémoire des SIREN déjà signalés**, dans
   `outils/prospects/deja-signales.txt`. C'est ce qui évite de répéter sept
   fois la même entreprise. Sans elle, la fenêtre de sept jours serait
   insupportable.
3. **Tri par secteur**, de l'intérêt le plus fort au plus faible :
   restauration, commerce de détail, artisanat, beauté, loisirs… Une SCI ou
   un holding ne sort pas de la liste.
4. **Vérification des adresses** avec `--adresses` : un appel par
   entreprise auprès de l'INSEE. Les entreprises marquées
   `[NON-DIFFUSIBLE]` sont **retirées** — leur dirigeant s'est opposé à la
   diffusion de ses données, ou bien c'est le réglage par défaut des
   entrepreneurs individuels depuis 2023. Dans les deux cas il n'y a pas
   d'adresse exploitable.
5. **Un corps de courriel** en HTML et en texte, dans
   `outils/prospects/courriel-AAAAMMJJ.html`.
6. **Envoi** avec `--envoyer`, en SMTP, par le script lui-même.

Le jour où il n'y a rien de neuf, le courriel part quand même et le dit en
une phrase. C'est volontaire : un envoi qui s'arrête sans prévenir ne se
distingue pas d'une panne.

### La garantie qui compte

**Si l'envoi échoue, la mémoire n'est pas touchée.** Les entreprises du jour
reviennent au prochain essai. Sans cette précaution, une panne de messagerie
les marquerait comme signalées et elles ne reparaîtraient plus jamais —
perdues sans que personne ne s'en aperçoive. C'est vérifié par un essai.

---

## Ce qu'il reste à brancher — une seule chose

L'envoi a besoin d'une adresse expéditrice et d'un mot de passe. Il n'y a
pas de connecteur de messagerie disponible pour les tâches programmées :
l'automatisation du matin a été créée, mais elle tourne **sans connecteur**,
donc sans Gmail. Le script envoie donc lui-même, en SMTP, et il lui faut
deux variables d'environnement :

| Variable | Valeur |
|---|---|
| `GRAFYCOM_SMTP_UTILISATEUR` | l'adresse Gmail expéditrice |
| `GRAFYCOM_SMTP_MOTDEPASSE` | un **mot de passe d'application** Google |

Elles se renseignent dans les réglages de l'environnement d'exécution — le
menu de l'environnement dans la barre de titre de la session, puis
« Edit » — en variables d'environnement. Une nouvelle session les reprend.

> Un mot de passe d'application n'est pas le mot de passe du compte. Il se
> crée dans les réglages de sécurité du compte Google, à la rubrique
> « Mots de passe des applications » (la validation en deux étapes doit être
> active). Il ne donne que le droit d'envoyer, et se révoque sans toucher au
> compte. **Ne jamais le coller dans une conversation** : il va dans les
> réglages de l'environnement, directement.

Tant que ces deux variables sont absentes, le script produit le courriel,
refuse d'envoyer, l'explique, et ne touche pas à la mémoire.

### Pourquoi pas Resend, puisqu'il est prévu pour le formulaire

Resend exige un domaine d'expédition vérifié. `grafycom.fr` n'y est pas
encore, et ça dépend de la bascule vers Cloudflare, qui n'est pas faite.
Le jour où ce sera fait, l'envoi pourra passer par là — mais il ne faut pas
que la veille attende ce chantier.

---

## L'automatisation

Créée, active, **mais encore muette** : elle tourne du lundi au vendredi à
7 h 56 (heure de Paris) et se bornera à produire la liste tant que les deux
variables ne sont pas renseignées.

Pourquoi 7 h 56 et pas 8 h : les tâches programmées à l'heure juste
s'entassent et se font attendre. Pourquoi du lundi au vendredi : le BODACC
ne publie pas le week-end, deux envois « rien de neuf » par semaine ne sont
que du bruit.

Ce qu'elle fait chaque matin : récupérer le dépôt, lancer la veille avec
vérification des adresses, envoyer le courriel, puis pousser la mémoire mise
à jour pour que le lendemain ne répète pas la même liste.

> La mémoire est le seul fichier du dossier `outils/prospects/` qui entre
> dans le dépôt, et il n'y entre que des SIREN. Les fichiers `.csv` et `.md`
> contiennent des noms et des adresses de personnes physiques : ils sont
> exclus par `.gitignore` et doivent le rester. Un dépôt n'oublie jamais.

## Retirer quelqu'un des envois

Ajouter son SIREN ou son nom dans `outils/ne-pas-contacter.txt`, une entrée
par ligne. Le script l'écarte dès le lendemain. C'est aussi là que doit
aller toute personne qui demande à ne plus être sollicitée — et cette
demande doit être respectée sans discussion ni délai.
