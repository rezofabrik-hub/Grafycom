# Ligne éditoriale — Instagram & Facebook

Ce document n'est pas une note d'intention, c'est le cerveau de l'assistant.
Tout ce qui est produit chaque mois en découle : s'il est juste, les
publications le sont ; s'il dérive, elles dérivent avec lui.

## Le principe

Le compte Instagram d'un graphiste **est** son portfolio. C'est la preuve
qu'il sait faire, avant tout argument. Deux conséquences qui tiennent lieu
de règles :

1. **Aucun visuel n'est généré automatiquement.** La création reste celle
   de Sandra. Un compte de graphiste qui publie des images fabriquées par
   une machine détruit exactement ce qu'il vend.
2. **Aucune publication ne part sans relecture.** L'assistant prépare :
   sujets, textes, hashtags, intentions visuelles, dates. Sandra tranche et
   programme depuis Meta Business Suite, qui le fait gratuitement.

Ce qui est automatisé, c'est donc le travail ingrat : trouver quoi
raconter, écrire, décliner, tenir le rythme. Pas le métier.

## La voix

La même que le site, et ce n'est pas un hasard : un compte qui parle
autrement que le site donne l'impression de deux entreprises.

- **Concrète avant d'être élégante.** « La camionnette d'un artisan
  irréprochable avec un lettrage fait à la va-vite » vaut mieux que
  « valoriser votre image de marque ».
- **Une idée par publication.** Pas trois conseils, pas une liste de dix
  astuces. Une.
- **Un peu à contre-courant.** Dire qu'un logo ne suffit pas, qu'un devis
  doit être lisible, qu'un besoin ne relève pas de son métier : c'est ce
  qui distingue d'un compte de prestataire interchangeable.
- **Sans jargon, ou alors expliqué.** Personne ne doit se sentir bête de ne
  pas connaître la différence entre RVB et CMJN.
- **Tutoiement : non.** Le vouvoiement, comme sur le site. Clientèle de
  professionnels.
- **Pas d'emoji en rafale.** Un, parfois, jamais trois.

Interdits de vocabulaire : « boostez », « votre partenaire de confiance »,
« n'hésitez pas à », « dans l'ADN de », « game changer », « 🚀 ».

## Les cinq piliers

| Pilier | Ce que ça prouve | Fréquence |
|---|---|---|
| **Le regard** | Qu'elle voit ce que les autres ne voient pas | 1 sur 3 |
| **Les coulisses** | Que le travail est réel, et qu'il a des étapes | 1 sur 4 |
| **Le territoire** | Qu'elle est d'ici, et que ça compte | 1 sur 5 |
| **Les réalisations** | Qu'elle sait faire. Le plus fort, le plus rare | dès que possible |
| **La personne** | Qu'on travaillera avec quelqu'un, pas avec un studio | 1 sur 6 |

**Le regard** — pourquoi un détail compte : la hiérarchie d'une carte de
restaurant, un logo qui doit tenir brodé sur un polo et sur un panneau de
trois mètres, pourquoi le menu en Word se lit mal. Format carrousel.

**Les coulisses** — les crayonnés, les pistes écartées, un bon à tirer
annoté, la pose d'une enseigne, la préparation d'un fichier grand format.
Format reel court ou carrousel. C'est ce qui marche le mieux et c'est ce
qu'on oublie de photographier : prendre l'habitude de filmer dix secondes.

**Le territoire** — une devanture à Collioure, une carte bilingue, un
commerce de Perpignan. Ancrage local, et les gens d'ici se reconnaissent.

**Les réalisations** — avant/après, projet livré, mot du client.
**Toujours demander l'accord du client avant de publier son projet**, même
si le contrat cède les droits. Un client surpris de se voir sur Instagram
est un client perdu.

**La personne** — le colibri, pourquoi ce métier, une règle de travail
assumée. Une fois par mois suffit : ce compte parle du client, pas d'elle.

## Le rythme

**Deux publications par semaine, mardi et vendredi.** Plus serait tenu
trois semaines puis abandonné — et un compte qui s'arrête fait plus de mal
qu'un compte lent. Deux ou trois stories par semaine en plus, prises sur le
vif, sans préparation.

Mardi : contenu qui apprend quelque chose (regard, territoire).
Vendredi : contenu qui montre (coulisses, réalisation).

## Les hashtags

Huit à douze, jamais trente. Trois jeux à alterner pour ne pas déclencher
les filtres de répétition.

**Jeu A — local**
`#graphistePerpignan #Perpignan #PyreneesOrientales #PaysCatalan #CommerceLocal66 #ArtisanDuRoussillon #Occitanie #IdentiteVisuelle`

**Jeu B — métier**
`#identitevisuelle #creationlogo #designgraphique #charteGraphique #directionArtistique #graphismeFrance #brandingLocal #printdesign`

**Jeu C — secteur**
`#carteDeRestaurant #menuDesign #enseigne #signaletique #commercantsPerpignan #restaurateur66 #ouvertureCommerce #nouvelleEntreprise`

## Les règles qui ne se discutent pas

- **Texte alternatif sur chaque image.** C'est de l'accessibilité, et pour
  une graphiste c'est aussi une démonstration de sérieux. Instagram le
  permet dans les paramètres avancés.
- **Jamais une maquette présentée comme un projet client.** Si c'est un
  exercice, le dire.
- **Jamais une image dont les droits ne sont pas clairs.** Ni photo
  trouvée, ni visuel de banque sans licence commerciale.
- **Répondre aux commentaires sous 24 h.** L'algorithme le récompense, et
  c'est surtout la moitié de l'intérêt d'être là.
- **Les liens dans la bio, pas dans les légendes** : Instagram ne les rend
  pas cliquables.

## Relancer l'assistant chaque mois

Le calendrier d'un mois se régénère en une demande. Le texte à me donner :

> Prépare le calendrier éditorial Grafycom du mois de [MOIS]. Suis
> `reseaux/LIGNE-EDITORIALE.md`. Projets livrés ce mois-ci et publiables :
> [liste, ou « aucun »]. Événements à caler : [salon, fermeture, promotion,
> ou « rien »].

Sans projet publiable, l'assistant bascule sur les piliers « regard » et
« territoire », qui ne dépendent de personne.

Le squelette de dates se produit à part, sans moi :

```bash
python3 reseaux/calendrier.py --mois 2026-11
```
