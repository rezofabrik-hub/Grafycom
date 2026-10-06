# Prospection des nouvelles entreprises du 66

Deux mouvements différents, qu'il vaut mieux ne pas confondre :

- le **référencement** fait venir à Sandra les gens qui cherchent déjà un
  graphiste à Perpignan ;
- la **prospection** va chercher ceux qui ne savent pas encore qu'ils en
  ont besoin.

Ce dossier concerne le second. Une entreprise qui vient de s'immatriculer a
besoin d'un logo, d'une carte, d'une enseigne, d'un menu — et elle ne le
sait souvent qu'au moment où quelqu'un le lui dit. C'est le seul moment où
le budget communication n'est pas encore dépensé ailleurs.

## L'outil

```bash
python3 outils/veille-entreprises.py                  # les 7 derniers jours
python3 outils/veille-entreprises.py --jours 30
python3 outils/veille-entreprises.py --depuis 2026-09-01
python3 outils/veille-entreprises.py --jours 7 --adresses   # + adresse postale
python3 outils/veille-entreprises.py --tout           # sans filtre d'intérêt
```

Pour l'envoi automatique du matin à Sandra, voir `VEILLE-QUOTIDIENNE.md` :

```bash
python3 outils/veille-entreprises.py --quotidien --adresses \
        --envoyer sandra.grafycom@gmail.com
```

Deux fichiers sortent dans `outils/prospects/` : un `.csv` à ouvrir dans un
tableur, et un `.md` à lire tel quel.

## D'où viennent les données

Du **BODACC**, le Bulletin officiel des annonces civiles et commerciales.
Toute immatriculation au registre du commerce y est publiée — c'est la
raison d'être du bulletin, et les données sont ouvertes. Aucune clé d'API,
aucun abonnement, aucun achat de fichier.

L'adresse postale complète, elle, vient de l'annuaire des entreprises
(même source que le site de l'État), interrogé par numéro SIREN.

**Ce que ces sources ne donnent pas : ni e-mail, ni téléphone.** Aucune des
deux n'en publie. Ce n'est pas une limite de l'outil, c'est le droit
français : une base publique d'adresses e-mail d'entrepreneurs
n'existerait pas longtemps. La prise de contact se fait donc par courrier,
en passant, ou au téléphone après avoir trouvé le numéro.

## Comment la liste est triée

Chaque création reçoit une priorité de 0 à 3, d'après l'activité déclarée :

| Priorité | Ce que ça veut dire | Exemples |
|---|---|---|
| **3** | Besoin immédiat et visible | restaurant, boutique, salon de coiffure |
| **2** | Besoin réel d'identité | artisan, gîte, boutique en ligne, événementiel |
| **1** | À qualifier au téléphone | conseil, courtage, activité non publiée |
| **0** | Rien à proposer — écarté | SCI, holding, coursier de plateforme |

Les priorités 0 méritent un mot : une société civile immobilière n'a pas de
vitrine, et un livreur à vélo travaille sous l'enseigne d'un autre. Les
appeler, c'est leur faire perdre leur temps et user le sien.

Le classement par secteur est une aide au tri, pas un verdict. L'activité
déclarée au BODACC est un texte libre, souvent long, qui mélange l'activité
principale et cinq activités accessoires. L'outil retient le secteur le
mieux représenté dans le texte — ce qui se trompe parfois. L'activité
complète figure toujours à côté du nom : c'est elle qui tranche.

## Ce que dit le droit

La prospection d'entreprise à entreprise est permise, à des conditions
précises. Dans l'ordre d'importance :

**Par courrier et en personne** — rien à demander à l'avance. La personne
doit pouvoir s'opposer à être recontactée, et cette opposition doit être
respectée.

**Par e-mail** — l'article L34-5 du code des postes et des communications
électroniques interdit la prospection par courriel sans accord préalable.
La doctrine de la CNIL en écarte la prospection entre professionnels à
trois conditions cumulatives : l'adresse est professionnelle, le message
porte sur l'activité professionnelle de la personne, et le refus est
possible d'un seul geste dès le premier message. Un restaurateur qui reçoit
une proposition de carte imprimée est dans ce cadre. Le même message envoyé
à une adresse personnelle n'y est pas.

**Par téléphone** — la prospection entre professionnels échappe aux règles
du démarchage des consommateurs. La frontière est mince quand
l'entrepreneur individuel n'a qu'une ligne, la sienne. Dans le doute,
préférer le courrier.

**Les données des entrepreneurs individuels sont des données
personnelles.** Quand l'entreprise est une personne physique — plus de la
moitié de la liste — son nom est celui de quelqu'un. Le RGPD s'applique :
l'intérêt légitime (article 6.1.f) autorise la prospection
professionnelle, mais impose d'indiquer d'où vient l'information dès le
premier contact (article 14) et de respecter l'opposition sans discuter
(article 21).

**Plus de la moitié des créations n'a pas d'adresse exploitable.**
L'INSEE marque « non diffusible » les entreprises dont les données ne sont
pas rendues publiques dans sa base. Sur une semaine de test :
**42 sur 78**. Il faut être précis sur ce que cela veut dire, parce que
c'est contre-intuitif.

Pour une société, c'est un choix : quelqu'un a demandé la non-diffusion.
Pour un entrepreneur individuel — la moitié de la liste — c'est devenu le
réglage par défaut : ses données ne sont plus publiées sauf s'il le
demande. Ce n'est donc pas toujours un refus exprimé.

Mais la conséquence pratique est la même : **l'adresse postale n'existe
pas dans les données ouvertes**, donc il n'y a rien à quoi envoyer un
courrier. L'outil les retire pour cette raison — pas au nom d'une
interdiction légale, qui serait une affirmation plus large que ce que je
peux garantir. Leur nom et leur commune, eux, restent publics par le
BODACC, dont la publication est obligatoire : rien n'interdit de passer
dans une boutique ou d'appeler un numéro trouvé par ailleurs.

Si une campagne de courrier devient un axe sérieux, c'est le point à faire
vérifier par un juriste avant d'aller plus loin — pas le modèle de lettre.

**Quand l'annuaire ne répond pas, la fiche est marquée « diffusion non
vérifiée ».** Un appel réseau qui échoue ressemblait au départ à un appel
qui réussit et ne trouve rien ; c'est ainsi qu'une entreprise non
diffusible s'est glissée dans une première liste. L'outil distingue
désormais les deux et refuse de garantir ce qu'il n'a pas vérifié. Ne rien
envoyer à ces fiches sans relancer la commande.

**Toute opposition s'inscrit le jour même dans
`outils/ne-pas-contacter.txt`.** Une ligne, le SIREN ou le nom. L'outil ne
la fera plus remonter. Ce n'est pas une politesse : c'est une obligation, et
c'est aussi la différence entre une démarche qu'on recommande et une qu'on
signale.

## Le courrier

C'est le canal qui convient le mieux ici, et pas seulement pour des raisons
juridiques : un graphiste qui envoie un courrier mal composé s'est
disqualifié avant d'être lu. Le support est l'argument.

Texte de départ, à réécrire avec ses mots :

> **Objet : félicitations pour votre immatriculation**
>
> Bonjour,
>
> J'ai vu la création de votre entreprise dans les annonces du BODACC, le
> bulletin où sont publiées toutes les immatriculations. Je me permets donc
> ce mot, en voisine.
>
> Je suis infographiste et chef de projet à Perpignan. Depuis sept ans, je
> construis l'identité visuelle des entreprises du département : le logo,
> la carte de visite, l'enseigne, la carte d'un restaurant, le marquage
> d'un véhicule. Tout ce qui fait qu'on vous reconnaît avant de vous
> connaître.
>
> Les premières semaines sont le bon moment pour y penser : une identité
> posée au départ coûte moins cher qu'une identité refaite deux ans plus
> tard, quand les flyers sont imprimés et l'enseigne vissée.
>
> Si le sujet vous intéresse, je vous offre un premier échange, sans
> engagement — trente minutes pour comprendre votre métier et vous dire ce
> qui me semble utile, ou inutile.
>
> Sandra — Grafycom
> 07 82 92 19 81 · sandra.grafycom@gmail.com · grafycom.fr
>
> *Vous recevez ce courrier parce que votre immatriculation a été publiée
> au BODACC. Dites-le-moi d'un mot et je retire votre entreprise de ma
> liste définitivement.*

Le dernier paragraphe n'est pas une formalité : c'est lui qui rend la
démarche propre, et c'est le seul qui soit juridiquement obligatoire.

## Le rythme

Une vingtaine d'envois par semaine, choisis dans les priorités 3, vaut
mieux que deux cents d'un coup. Trois raisons : on peut personnaliser, on
peut relancer, et on peut encaisser le travail si ça répond.

Le département produit environ **350 immatriculations par mois**, dont à peu
près **80 en priorité 3**. Il n'y a pas de pénurie de prospects. Il y a une
limite au nombre de clients qu'une personne seule peut servir.
