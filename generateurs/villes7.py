# -*- coding: utf-8 -*-
"""La couronne de Perpignan, la Salanque, et Fitou.

Pourquoi ces sept pages, alors que p_locales.py et pays.py posent la règle
inverse — décliner la même page sur chaque village produit des pages
satellites, que Google sanctionne.

Parce que la règle vise la DUPLICATION, pas le nombre. Saint-Estève compte
11 630 habitants, plus qu'Argelès (10 616), Elne (9 511) ou Thuir (8 243),
qui ont toutes leur page ; Le Soler en compte 7 942, plus que Céret, Prades
ou Le Barcarès. Les ignorer n'était pas de la prudence, c'était un trou.

Pour les quatre petites — Claira, Salses, Baho, Peyrestortes — la règle
tiendrait, et la prudence aurait été de les traiter en page de secteur.
Laurent les a demandées nommément : ce sont ses communes de prospection. La
réponse n'est donc pas de refuser, elle est d'écrire sept pages réellement
différentes. Chacune part d'une activité qu'on ne trouve pas sur les six
autres : la zone d'activités et le véhicule d'artisan à Saint-Estève, la
vente au bord de la RN116 au Soler, le maraîchage face à la zone
commerciale à Claira, le flux de la forteresse à Salses, l'entreprise sans
vitrine à Baho, le petit domaine au caveau à Peyrestortes, l'appellation à
Fitou.

Fitou n'est pas dans les Pyrénées-Orientales : la commune est dans l'Aude,
code postal 11510, à quelques kilomètres au nord de Salses. Elle est traitée
ici parce qu'elle est voisine et que la limite départementale n'a aucun sens
commercial — mais son code postal est le vrai, pas un 66 arrangeant, et
areaServed dira Fitou et non le département.
"""
from p_locales import locale, carte

# ------------------------------------------------------------- SAINT-ESTÈVE
locale(
 "graphiste-saint-esteve.html", "Saint-Estève", "66240",
 "Saint-Estève · 66240",
 "Graphiste", "à Saint-Estève",
 "Identité visuelle, marquage de véhicule et supports pour les artisans, les entreprises de zone d'activités et les commerces de Saint-Estève.",
 """<p>Saint-Estève touche Perpignan sans en faire partie. On passe de l'une à l'autre sans voir la limite, et c'est précisément ce qui complique la communication des entreprises installées ici&nbsp;: elles travaillent à l'échelle de l'agglomération, mais elles ont une adresse que leurs clients ne situent pas toujours.</p>
    <h3>Le véhicule est la première vitrine d'un artisan</h3>
    <p>La commune compte beaucoup d'entreprises du bâtiment et de services qui n'ont pas de boutique&nbsp;: plombiers, électriciens, menuisiers, paysagistes. Leur enseigne, c'est leur camionnette, et elle est vue chaque jour par des centaines de personnes sur la rocade et dans les lotissements où ils interviennent.</p>
    <p>Un marquage de véhicule obéit à des règles qu'une affiche ignore&nbsp;: on lit de loin, de biais, souvent en mouvement. Trois informations suffisent — le métier, le nom, le téléphone — et tout le reste nuit. J'ai vu des flancs de camionnette où le numéro était écrit plus petit que le slogan&nbsp;: c'est de la peinture perdue.</p>
    <h3>Les zones d'activités ne se visitent pas, elles se cherchent</h3>
    <p>Une entreprise installée dans une zone est trouvée par son nom, pas par la vitrine. Ce qui compte alors, c'est que le nom soit le même partout — sur la façade, sur le devis, sur la fiche en ligne, sur le véhicule. Une entreprise qui s'appelle «&nbsp;SARL Martin&nbsp;» sur ses papiers et «&nbsp;Martin Rénovation&nbsp;» sur sa camionnette se divise en deux aux yeux d'un client qui cherche à la rappeler.</p>
    <h3>Se distinguer de Perpignan sans s'en couper</h3>
    <p>Beaucoup d'entreprises stéphanoises hésitent&nbsp;: afficher Saint-Estève, ou afficher Perpignan pour paraître plus central&nbsp;? Mon avis est de ne pas mentir sur l'adresse, parce que ça se voit, et de jouer la proximité&nbsp;: un artisan de Saint-Estève intervient chez un client de Perpignan en quinze minutes, et c'est un argument plus solide qu'une adresse empruntée.</p>""",
 [carte("p-bleu", "fa-truck", "Marquage de véhicule", "Lisible de loin et en mouvement. Le métier, le nom, le numéro — et rien qui vienne les concurrencer."),
  carte("p-violet", "fa-id-card", "Identité d'artisan", "Un nom, un logo et des documents qui concordent, du devis à la facture en passant par la camionnette."),
  carte("p-turq", "fa-sign-hanging", "Signalétique de zone", "Totem, façade, numéro de lot : être trouvé par quelqu'un qui cherche votre nom, pas votre vitrine.")],
 "à Saint-Estève",
 "Saint-Estève est à dix minutes de Perpignan. Pour un marquage de véhicule, je me déplace systématiquement&nbsp;: les surfaces utiles d'une camionnette ne se devinent pas sur une photo, et un montant de porte mal relevé fait rater une pose.",
 "Baho, Peyrestortes, Pia, Villeneuve-de-la-Rivière, Le Soler, Rivesaltes&nbsp;— toute la couronne nord-ouest de Perpignan.",
 "Graphiste à Saint-Estève — Grafycom",
 "Graphiste à Saint-Estève (66240) : marquage de véhicule, identité d'artisan et signalétique de zone d'activités. Devis gratuit.")

# ----------------------------------------------------------------- LE SOLER
locale(
 "graphiste-le-soler.html", "Le Soler", "66270",
 "Le Soler · 66270",
 "Graphiste", "au Soler",
 "Supports de vente directe, signalétique de bord de route et identité visuelle pour les producteurs, artisans et commerces du Soler et de la vallée de la Têt.",
 """<p>Le Soler est sur la RN116, la route qui monte vers Prades, le Conflent et l'Espagne. C'est une commune où l'on habite et une commune devant laquelle on passe — et ces deux réalités ne demandent pas les mêmes supports.</p>
    <h3>Vendre à quelqu'un qui roule</h3>
    <p>La plaine de la Têt est arboricole&nbsp;: abricots, pêches, nectarines. Une part de la récolte se vend en direct, au bord de la route, pendant quelques semaines. Le panneau qui annonce le stand a une fraction de seconde pour être lu par un conducteur qui ne s'était pas levé en pensant acheter des abricots.</p>
    <p>Cela veut dire un mot, pas une phrase. Un prix, parce qu'un prix affiché fait s'arrêter et un prix absent fait douter. Et une flèche, parce qu'un automobiliste qui a compris trop tard ne fait pas demi-tour. Un panneau de vente directe bien conçu, c'est trois éléments et beaucoup de vide&nbsp;; un mauvais, c'est une liste de fruits que personne n'a le temps de lire.</p>
    <h3>La saison ne se rattrape pas</h3>
    <p>Un verger produit pendant six semaines. Les supports doivent être prêts avant, résister au soleil et à la tramontane, et pouvoir resservir l'année suivante. Je conçois les panneaux saisonniers avec des éléments interchangeables&nbsp;: la structure et le nom restent, le fruit et le prix se remplacent. C'est moins cher à la deuxième saison, et c'est surtout plus rapide quand la récolte arrive en avance.</p>
    <h3>Les commerces du centre ne jouent pas le même jeu</h3>
    <p>Le village a aussi ses commerces de proximité, qui vivent d'habitués et non de passage. Pour eux l'enjeu est inverse&nbsp;: on ne cherche pas à être vu de loin, mais à être reconnu de près et à tenir dans la durée. Une devanture sobre, une vitrine lisible, une présence en ligne à jour — et surtout pas une communication qui change tous les six mois.</p>""",
 [carte("p-orange", "fa-road", "Panneaux de bord de route", "Un mot, un prix, une flèche. Conçus pour être lus à cinquante à l'heure, pas pour être admirés de près."),
  carte("p-jaune", "fa-seedling", "Vente directe et marchés", "Étals, ardoises, étiquettes de cagette : des supports qui tiennent le soleil et resservent la saison suivante."),
  carte("p-violet", "fa-store", "Commerce de village", "Devanture et vitrine pour une clientèle d'habitués, pensées pour durer plutôt que pour surprendre.")],
 "au Soler",
 "Le Soler est à un quart d'heure de Perpignan par la RN116. Pour une signalétique de bord de route, le déplacement est indispensable&nbsp;: il faut voir d'où arrive le véhicule, à quelle vitesse, et où le regard se pose réellement.",
 "Baho, Pézilla-la-Rivière, Villeneuve-de-la-Rivière, Toulouges, Saint-Féliu-d'Avall, Canohès&nbsp;— la vallée de la Têt et le Ribéral.",
 "Graphiste au Soler — Grafycom",
 "Graphiste au Soler (66270) : panneaux de vente directe, supports de marché et identité de commerce. Devis gratuit.")

# ------------------------------------------------------------------- CLAIRA
locale(
 "graphiste-claira.html", "Claira", "66530",
 "Claira · 66530",
 "Graphiste", "à Claira",
 "Étiquettes de maraîcher, supports de vente directe et signalétique commerciale pour les producteurs et les entreprises de Claira et de la Salanque.",
 """<p>Claira a deux économies qui se tournent le dos. D'un côté les terres maraîchères de la Salanque, où l'on produit des artichauts, des salades et des légumes de plein champ depuis des générations. De l'autre une zone commerciale qui attire tout le nord de l'agglomération. Même commune, deux clientèles qui ne se croisent jamais.</p>
    <h3>Le maraîcher vend un produit qu'on ne distingue pas</h3>
    <p>Un artichaut ressemble à un artichaut. Sur un étal ou dans un rayon, ce qui différencie celui d'un producteur de Claira de celui qui vient d'Espagne, ce n'est pas le légume&nbsp;: c'est ce qui est écrit à côté. L'origine, le nom de l'exploitation, parfois le visage du producteur.</p>
    <p>C'est pour ça qu'une identité visuelle de maraîcher n'est pas un luxe. Elle sert à transformer un produit indifférencié en produit identifié — sur une cagette, une ardoise de marché, un sachet, un panneau de stand. Et elle doit tenir dans des conditions que peu de supports supportent&nbsp;: l'humidité, la terre, le froid des chambres.</p>
    <h3>La vente en circuit court change ce qu'il faut imprimer</h3>
    <p>Un producteur qui vend en direct, en AMAP ou en panier n'a pas besoin des mêmes supports qu'un producteur qui livre une centrale d'achat. Il lui faut de quoi se faire connaître localement et de quoi rassurer sur la régularité&nbsp;: un nom, une étiquette, une fiche d'exploitation, et de quoi exister sur les réseaux sans y passer ses soirées. L'investissement utile est faible, mais il doit être juste.</p>
    <h3>La zone commerciale, c'est un autre métier</h3>
    <p>Une enseigne en zone est vue depuis un parking, souvent de loin, souvent entre deux autres enseignes plus grosses. La lisibilité y prime sur l'originalité, et les contraintes techniques — hauteur, éclairage, autorisation d'urbanisme — se règlent avant la création, pas après. Je travaille dans les deux mondes, mais je ne prétends pas que ce soit le même travail.</p>""",
 [carte("p-jaune", "fa-carrot", "Identité de maraîcher", "Transformer un légume indifférencié en produit identifié : nom, origine, visage. Sur cagette, sachet et ardoise."),
  carte("p-turq", "fa-basket-shopping", "Circuit court et paniers", "Fiche d'exploitation, étiquettes, visuels pour les réseaux. De quoi exister localement sans y passer ses soirées."),
  carte("p-corail", "fa-store", "Enseigne de zone", "Lisible depuis un parking, entre deux voisines plus grandes. Contraintes d'urbanisme réglées avant la création.")],
 "à Claira",
 "Claira est à un quart d'heure de Perpignan. Pour une exploitation, la visite vaut le déplacement&nbsp;: voir les cultures, le local de conditionnement et la façon dont les produits partent donne de meilleures idées qu'une conversation téléphonique.",
 "Saint-Laurent-de-la-Salanque, Torreilles, Pia, Bompas, Le Barcarès, Rivesaltes&nbsp;— toute la Salanque.",
 "Graphiste à Claira — Grafycom",
 "Graphiste à Claira (66530) : identité de maraîcher, supports de circuit court et enseignes de zone commerciale. Devis gratuit.")

# -------------------------------------------------------- SALSES-LE-CHÂTEAU
locale(
 "graphiste-salses-le-chateau.html", "Salses-le-Château", "66600",
 "Salses-le-Château · 66600",
 "Graphiste", "à Salses-le-Château",
 "Étiquettes de vin, supports de caveau et signalétique touristique pour les domaines et commerces de Salses-le-Château, porte nord du département.",
 """<p>Salses est la première commune des Pyrénées-Orientales quand on descend du nord, et la forteresse en est le repère. Un monument national, visible depuis l'autoroute, qui amène chaque année un flux de visiteurs dont une partie seulement s'arrête ailleurs qu'au parking du château. Capter cette part, c'est l'enjeu commercial de la commune.</p>
    <h3>Un visiteur de passage décide en quelques secondes</h3>
    <p>Quelqu'un qui vient de visiter la forteresse a du temps, de la curiosité, et aucune intention précise. Il s'arrêtera dans un caveau s'il comprend en un regard ce qu'il y trouvera. Un panneau qui dit «&nbsp;dégustation&nbsp;» sans dire quoi, ou un caveau dont on ne devine pas s'il est ouvert, perd ce visiteur sans jamais savoir qu'il est passé.</p>
    <p>Les supports qui marchent ici sont simples&nbsp;: une signalétique d'accès lisible depuis la route, une indication d'horaires qu'on n'a pas à deviner, et de quoi repartir avec une trace — une carte, une étiquette qu'on retrouve chez soi et qui permet de recommander.</p>
    <h3>L'étiquette doit porter l'appellation sans s'y réduire</h3>
    <p>Les Rivesaltes et les Muscats de Rivesaltes produits ici partagent leur appellation avec des dizaines de domaines. L'étiquette est donc ce qui distingue, à l'intérieur d'un nom commun. Elle doit porter les mentions obligatoires — appellation, degré, volume, allergènes, numéro de lot — sans que ces obligations écrasent le peu de place qui reste pour dire qui vous êtes.</p>
    <p>C'est un exercice de hiérarchie plus que de décoration&nbsp;: décider ce qu'on lit en premier à trois mètres, puis à trente centimètres, puis le verre à la main.</p>
    <h3>Les abords d'un monument historique sont réglementés</h3>
    <p>Une enseigne située dans le périmètre de protection de la forteresse passe par l'avis de l'Architecte des Bâtiments de France. Ce n'est pas un obstacle insurmontable, mais ça se prépare&nbsp;: matériaux, dimensions, éclairage et teintes se discutent avant le dessin, pas après un refus.</p>""",
 [carte("p-rose", "fa-wine-bottle", "Étiquettes d'appellation", "Les mentions obligatoires intégrées à la composition, pas plaquées dessus. Se distinguer à l'intérieur d'un nom commun."),
  carte("p-turq", "fa-signs-post", "Signalétique d'accès", "Être vu depuis la route, dire ce qu'on trouve et quand c'est ouvert. Le visiteur de passage ne cherche pas deux fois."),
  carte("p-violet", "fa-landmark", "Enseigne en secteur protégé", "Périmètre de la forteresse : matériaux, teintes et dimensions calés avec l'ABF avant le dessin.")],
 "à Salses-le-Château",
 "Salses est à vingt minutes de Perpignan par l'A9 ou la D900. Pour un caveau ou une signalétique d'accès, la visite est utile&nbsp;: il faut voir par où arrivent les visiteurs, et à quel moment ils décident de s'arrêter ou de continuer.",
 "Opoul-Périllos, Saint-Hippolyte, Rivesaltes, Claira, Espira-de-l'Agly, Fitou&nbsp;— la porte nord du département et les premières Corbières.",
 "Graphiste à Salses-le-Château — Grafycom",
 "Graphiste à Salses-le-Château (66600) : étiquettes de vin, supports de caveau et enseignes en secteur protégé. Devis gratuit.")

# --------------------------------------------------------------------- BAHO
locale(
 "graphiste-baho.html", "Baho", "66540",
 "Baho · 66540",
 "Graphiste", "à Baho",
 "Identité visuelle, cartes de visite et présence en ligne pour les entreprises sans vitrine, artisans et indépendants de Baho et du Ribéral.",
 """<p>Baho est une petite commune de la plaine, entre Perpignan et Le Soler. Ce qui s'y passe commercialement ne se voit pas depuis la rue&nbsp;: beaucoup d'activités s'exercent à domicile, dans un petit local ou chez le client. Pas de vitrine, pas d'enseigne, pas de passage.</p>
    <h3>Quand il n'y a pas de vitrine, la carte de visite en tient lieu</h3>
    <p>Une entreprise sans devanture est recommandée de bouche à oreille. Le moment décisif n'est pas la découverte, c'est la transmission&nbsp;: quelqu'un parle de vous à quelqu'un d'autre, et il faut que cette personne puisse vous retrouver. La carte de visite, le devis, la signature de mail et la fiche en ligne portent à eux seuls tout ce qu'une vitrine ferait ailleurs.</p>
    <p>Cela change ce qu'il faut y mettre. Une carte de visite d'entreprise sans local doit dire le métier explicitement — pas un nom poétique seul — et porter un numéro qu'on peut composer sans loupe. C'est banal à écrire et pourtant la moitié des cartes que je vois échouent sur l'un des deux.</p>
    <h3>La cohérence remplace la répétition</h3>
    <p>Un commerce de centre-ville est vu cent fois par an par le même passant&nbsp;: la répétition fait le travail. Une activité sans vitrine n'a pas cette chance, et chaque contact doit donc ressembler aux précédents. Même logo, mêmes couleurs, même façon d'écrire son nom, du premier devis jusqu'à la facture. C'est ce qui donne à une petite structure l'air d'être solide.</p>
    <h3>Une petite commune ne veut pas dire un petit périmètre</h3>
    <p>La plupart des indépendants installés à Baho travaillent sur toute l'agglomération. Leur communication doit donc dire d'où ils viennent sans se limiter à leur village&nbsp;: mentionner la commune pour la proximité, et l'agglomération pour la zone d'intervention. Les deux, pas l'un ou l'autre.</p>""",
 [carte("p-bleu", "fa-id-card", "Carte de visite et papeterie", "Quand il n'y a pas de vitrine, c'est la carte qui en tient lieu. Le métier dit clairement, un numéro lisible."),
  carte("p-violet", "fa-palette", "Identité d'indépendant", "Logo, couleurs et typographies tenus d'un support à l'autre. C'est la cohérence qui fait sérieux, pas la taille."),
  carte("p-turq", "fa-file-signature", "Devis, factures, signature", "Les documents que vos clients lisent vraiment. Au même niveau de soin que le reste.")],
 "à Baho",
 "Baho est à dix minutes de Perpignan. Pour une activité sans local, le déplacement est rarement nécessaire&nbsp;: un échange en visio suffit à cadrer le projet, et les épreuves se valident en ligne.",
 "Le Soler, Saint-Estève, Villeneuve-de-la-Rivière, Pézilla-la-Rivière, Peyrestortes&nbsp;— le Ribéral et la couronne ouest de Perpignan.",
 "Graphiste à Baho — Grafycom",
 "Graphiste à Baho (66540) : identité visuelle, cartes de visite et papeterie pour indépendants et entreprises sans vitrine.")

# ------------------------------------------------------------- PEYRESTORTES
locale(
 "graphiste-peyrestortes.html", "Peyrestortes", "66600",
 "Peyrestortes · 66600",
 "Graphiste", "à Peyrestortes",
 "Étiquettes, supports de caveau et identité visuelle pour les petits domaines viticoles et les artisans de Peyrestortes.",
 """<p>Peyrestortes est un village de vignes, à quelques kilomètres de Rivesaltes, dans l'aire des Rivesaltes et des Muscats. Moins de deux mille habitants, quelques domaines, des artisans. On n'y vend presque rien par la grande distribution&nbsp;: on y vend au caveau, sur les salons, et à des clients qui reviennent.</p>
    <h3>Un domaine qui vend au caveau n'a pas les mêmes besoins</h3>
    <p>Quand la vente se fait en rayon, l'étiquette doit gagner une bataille d'attention contre quarante concurrentes. Quand elle se fait au caveau, la bataille est déjà gagnée&nbsp;: le client est là, il goûte, il parle au vigneron. L'étiquette ne sert plus à convaincre — elle sert à ce qu'on se souvienne, et à ce qu'on puisse recommander.</p>
    <p>Cela change tout. On peut être plus sobre, plus personnel, moins démonstratif. Ce qui compte, c'est que le nom se retienne et que la bouteille, posée sur une table deux mois plus tard, rappelle la visite à quelqu'un qui n'y était pas.</p>
    <h3>Une gamme réduite se conçoit comme un ensemble</h3>
    <p>Un petit domaine sort souvent trois ou quatre cuvées. Dessinées séparément, elles donnent quatre étiquettes sans rapport entre elles. Dessinées ensemble, elles forment une gamme&nbsp;: la même structure, la même typographie, une variation de couleur ou de détail d'une cuvée à l'autre. On gagne en reconnaissance, et on gagne aussi en coût — la deuxième étiquette d'une gamme demande moins de travail que la première.</p>
    <h3>Le budget d'un petit domaine est un vrai sujet</h3>
    <p>Je préfère le dire franchement&nbsp;: une identité complète n'est pas toujours le bon premier achat. Pour un domaine qui démarre, une gamme d'étiquettes propre et un panneau de caveau lisible font plus pour les ventes qu'un logo retravaillé. On peut commencer par là et compléter plus tard&nbsp;; l'inverse est un ordre coûteux.</p>""",
 [carte("p-rose", "fa-wine-bottle", "Gamme d'étiquettes", "Trois ou quatre cuvées conçues ensemble, pas séparément. Plus reconnaissables, et moins chères à la deuxième."),
  carte("p-jaune", "fa-door-open", "Supports de caveau", "Panneau d'accès, horaires, fiches de dégustation. De quoi faire s'arrêter, et de quoi faire revenir."),
  carte("p-violet", "fa-pen-nib", "Identité de domaine", "Un nom qui se retient et se recommande. Sobre plutôt que démonstratif, quand la vente se fait en direct.")],
 "à Peyrestortes",
 "Peyrestortes est à un quart d'heure de Perpignan. Pour un domaine, la visite vaut le déplacement&nbsp;: voir les vignes, le chai et le caveau donne une matière que personne ne décrit bien au téléphone.",
 "Rivesaltes, Pia, Baixas, Villeneuve-de-la-Raho, Saint-Estève, Espira-de-l'Agly&nbsp;— les villages viticoles du nord de Perpignan.",
 "Graphiste à Peyrestortes — Grafycom",
 "Graphiste à Peyrestortes (66600) : étiquettes de vin, gammes de cuvées et supports de caveau pour petits domaines.")

# -------------------------------------------------------------------- FITOU
# Commune de l'AUDE, pas des Pyrenees-Orientales. Code postal 11510, et non
# un 66 arrangeant : ecrire un faux code postal sur une page locale est le
# genre de detail qu'un client verifie, et qui coute la confiance.
locale(
 "graphiste-fitou.html", "Fitou", "11510",
 "Fitou · 11510 · Aude",
 "Graphiste", "à Fitou",
 "Étiquettes d'appellation, supports de caveau et identité visuelle pour les domaines de Fitou, à vingt minutes de Salses et de Rivesaltes.",
 """<p>Fitou est dans l'Aude, pas dans les Pyrénées-Orientales. La limite départementale passe entre Salses et Fitou, et elle ne veut rien dire pour un vigneron&nbsp;: les mêmes Corbières, le même étang, les mêmes clients de passage sur l'A9. Je travaille des deux côtés, et je le dis plutôt que de faire semblant que Fitou est dans le 66.</p>
    <h3>Une appellation ancienne est un capital, et une contrainte</h3>
    <p>Fitou est l'une des plus anciennes appellations en rouge du Languedoc. C'est un atout considérable&nbsp;: le nom est connu, il porte une histoire, il se vend hors de la région. C'est aussi une contrainte&nbsp;: l'étiquette doit respecter le cahier des charges et les mentions réglementaires, et le nom de l'appellation occupe une place que vous ne choisissez pas entièrement.</p>
    <p>Le travail consiste donc à faire exister le domaine à l'intérieur d'un nom collectif. Ce qui distingue, ce n'est pas la taille du mot Fitou&nbsp;: c'est tout ce qu'on met autour — la typographie du nom de domaine, le traitement de la cuvée, la matière du papier.</p>
    <h3>Deux publics très différents sur quelques kilomètres</h3>
    <p>Un domaine de Fitou vend à des visiteurs qui sortent de l'autoroute et à des cavistes qui ne verront jamais le caveau. Les premiers achètent une rencontre, les seconds achètent une fiche technique et une étiquette qui tiendra dans un rayon. Il faut les deux jeux de supports, et ils n'ont pas le même ton.</p>
    <h3>L'étang et les Corbières ne racontent pas la même chose</h3>
    <p>La commune est partagée entre un bord d'étang et un arrière-pays de garrigue. Beaucoup de domaines s'appuient sur le paysage pour leur image, et le choix de celui qu'on montre n'est pas anodin&nbsp;: l'étang évoque la lumière et le tourisme, les Corbières évoquent la rudesse et le caractère du vin. Les deux sont vrais. Il faut en choisir un et s'y tenir.</p>""",
 [carte("p-rose", "fa-wine-bottle", "Étiquettes AOC Fitou", "Exister à l'intérieur d'un nom collectif. Le cahier des charges respecté sans que l'étiquette s'y résume."),
  carte("p-turq", "fa-file-lines", "Supports pour cavistes", "Fiches techniques, argumentaires, visuels de gamme. Pour un acheteur qui ne verra jamais le caveau."),
  carte("p-orange", "fa-door-open", "Accueil au caveau", "Signalétique depuis la sortie d'autoroute, horaires lisibles, de quoi repartir avec une trace.")],
 "à Fitou",
 "Fitou est à une demi-heure de Perpignan par l'A9, et à une vingtaine de minutes de Salses. Le fait d'être dans un autre département ne change rien aux délais ni aux tarifs&nbsp;: c'est plus près de chez moi que Font-Romeu.",
 "Leucate, Treilles, Caves, Salses-le-Château, Opoul-Périllos&nbsp;— la limite entre l'Aude et les Pyrénées-Orientales, de part et d'autre.",
 "Graphiste à Fitou — Étiquettes de domaine | Grafycom",
 "Graphiste à Fitou (11510) : étiquettes AOC, supports de caveau et pour cavistes. À vingt minutes de Salses et Rivesaltes.")
