# -*- coding: utf-8 -*-
"""Les trois pays de montagne : Cerdagne, Capcir, Conflent.

Pourquoi des pages de PAYS et non de communes. La règle posée dans
p_locales.py vaut ici aussi : décliner la même page sur chaque village
produit des pages satellites, que Google sanctionne. Or la haute montagne
du 66 compte des dizaines de communes de quelques centaines d'habitants —
une page par commune serait exactement l'erreur à ne pas faire.

Un pays, en revanche, est une vraie unité : on y vit du même rythme, on y
subit le même climat, on y relève des mêmes contraintes d'urbanisme. Trois
pages, trois territoires qui n'ont pas les mêmes problèmes, et qui ne
racontent donc pas la même chose. Font-Romeu et Prades gardent par
ailleurs leur page de commune : ces pages-ci les complètent et pointent
vers elles.

Tous les faits cités ont été vérifiés le 6 octobre 2026 :
  - Villefranche-de-Conflent, Fort Libéria et Mont-Louis sont inscrits au
    patrimoine mondial de l'UNESCO depuis 2008, au titre des
    fortifications de Vauban ;
  - le Train jaune (ligne de Cerdagne) relie Villefranche-de-Conflent à
    Latour-de-Carol, 63 km, jusqu'à 1 600 m d'altitude ;
  - Puyvalador n'est plus en exploitation : la station n'est pas citée
    comme active. Les Angles et Formiguères le sont.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen import page, appel, TEL, TEL_URI, MAIL          # noqa: E402
from p_locales import GABARIT, carte                     # noqa: E402


def jsonld_pays(nom, slug, communes):
    lieux = ",\n    ".join(
        '{ "@type": "Place", "name": "%s" }' % c for c in communes)
    return """{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Grafycom — graphiste en %s",
  "description": "Logo, identité visuelle, enseignes et supports de communication pour les commerces et hébergements de %s.",
  "url": "https://grafycom.fr/%s",
  "telephone": "+33782921981",
  "email": "%s",
  "slogan": "L'image qui vous ressemble",
  "address": { "@type": "PostalAddress", "addressLocality": "Perpignan", "postalCode": "66000", "addressRegion": "Pyrénées-Orientales", "addressCountry": "FR" },
  "areaServed": {
    "@type": "AdministrativeArea",
    "name": "%s",
    "containedInPlace": { "@type": "AdministrativeArea", "name": "Pyrénées-Orientales" },
    "containsPlace": [
    %s
    ]
  },
  "knowsLanguage": [ "fr", "es", "ca" ]
}""" % (nom, nom, slug, MAIL, nom, lieux)


def pays(slug, nom, avec_article, communes, eyebrow, h1a, h1b, chapeau,
         particularites, cartes, au_pays, deplacement, voisines, title, desc):
    """avec_article : « le Capcir », « la Cerdagne ».

    Le gabarit écrit « Ce que {ville} a de particulier ». Pour une commune,
    le nom nu convient. Pour un pays, il faut l'article, sans quoi on lit
    « Ce que Capcir a de particulier ».
    """
    corps = GABARIT.format(
        eyebrow=eyebrow, h1a=h1a, h1b=h1b, chapeau=chapeau, ville=avec_article,
        particularites=particularites, cartes="\n    ".join(cartes),
        a_ville=au_pays, deplacement=deplacement, voisines=voisines,
        tel=TEL, tel_uri=TEL_URI)
    corps += appel(
        "Un projet %s&nbsp;?" % au_pays,
        "Le premier échange est gratuit et sans engagement. Décrivez-moi "
        "votre activité et ce qui vous gêne dans votre image&nbsp;: je vous "
        "réponds sous 48&nbsp;heures ouvrées.",
        fond="fond-creme")
    page(slug, title, desc, corps, ogtitle=title.split(" | ")[0],
         jsonld=jsonld_pays(nom, slug, communes))


# ------------------------------------------------------------------ CERDAGNE

pays(
 "graphiste-cerdagne.html", "Cerdagne", "la Cerdagne",
 ["Font-Romeu-Odeillo-Via", "Bolquère", "Saillagouse", "Err", "Osséja",
  "Bourg-Madame", "Latour-de-Carol", "Targasonne"],
 "Cerdagne · Pyrénées-Orientales",
 "Graphiste", "en Cerdagne",
 "Logo, enseignes, cartes et supports de saison pour les commerces, hôtels "
 "et restaurants de Cerdagne. Une conception qui tient compte de l'altitude, "
 "de la frontière et des deux saisons.",
 """<p>La Cerdagne n'est pas une vallée de montagne comme les autres&nbsp;: c'est un plateau large et ouvert, à plus de 1&nbsp;200&nbsp;mètres, où le soleil tape une bonne partie de l'année. Cela a trois conséquences très concrètes pour vos supports.</p>
    <h3>L'altitude abîme ce qu'on y expose</h3>
    <p>À 1&nbsp;500&nbsp;mètres, le rayonnement ultraviolet est nettement plus intense qu'en plaine. Une enseigne, un panneau ou un adhésif de vitrine qui tiendrait cinq ans à Perpignan peut passer en deux hivers ici&nbsp;— les rouges et les bleus partent en premier. S'ajoutent le gel, la neige qui s'accumule sur les faces horizontales, et les écarts de température qui travaillent les collages.</p>
    <p>Ce n'est pas une fatalité&nbsp;: cela se joue au choix du support et de l'encre, et se décide avant la commande, avec le poseur. Un laminat anti-UV ou un dibond plutôt qu'un PVC change la durée de vie du simple au triple.</p>
    <h3>Deux saisons, deux clientèles</h3>
    <p>L'hiver amène les skieurs des Neiges Catalanes, l'été les randonneurs, les cyclistes et les stages d'altitude. Entre les deux, la fréquentation retombe et la clientèle redevient locale et frontalière. Une carte de restaurant ou une devanture qui ne parle qu'à l'une des trois ne travaille qu'un tiers de l'année.</p>
    <p>La réponse n'est pas de tout refaire trois fois&nbsp;: c'est de construire un gabarit solide et de le décliner. Même identité, même maison, contenus différents.</p>
    <h3>La frontière, à quelques minutes</h3>
    <p>Bourg-Madame touche Puigcerdà, et l'enclave espagnole de Llívia est posée en plein territoire français. La clientèle catalane et espagnole fait partie du quotidien, pas de l'exception. Une carte, une signalétique ou une plaquette gagnent presque toujours à exister en plusieurs langues&nbsp;— le piège étant de traduire après la mise en page&nbsp;: le texte catalan et espagnol gonfle, et la maquette casse. On le prévoit dès le départ.</p>
    <p>L'accompagnement se fait en français comme en espagnol.</p>
    <h3>Une commune, une page</h3>
    <p>Si votre activité est à Font-Romeu même, la page <a href="graphiste-font-romeu.html">graphiste à Font-Romeu</a> entre davantage dans le détail de la station.</p>""",
 [carte("p-bleu", "fa-snowflake", "Supports qui tiennent l'hiver",
        "Choix des matériaux et des encres pour l'altitude&nbsp;: anti-UV, résistance au gel, fixations prévues pour la neige."),
  carte("p-turq", "fa-utensils", "Cartes de saison",
        "Une carte d'hiver, une carte d'été, la même identité. Gabarits que vous déclinez vous-même ensuite."),
  carte("p-violet", "fa-language", "Supports multilingues",
        "Français, espagnol, catalan prévus dès la maquette&nbsp;— pas rajoutés après coup, ce qui se voit toujours.")],
 "en Cerdagne",
 "La Cerdagne est à une heure et demie de Perpignan par la vallée de la Têt. "
 "Je monte pour un relevé de cotes ou un point avec le poseur&nbsp;; le reste "
 "se traite très bien à distance.",
 "Font-Romeu, Bolquère, Saillagouse, Err, Osséja, Bourg-Madame, "
 "Latour-de-Carol, Targasonne&nbsp;— et le Capcir voisin.",
 "Graphiste en Cerdagne — logo, enseignes, cartes | Grafycom",
 "Graphiste en Cerdagne (66) : logo, enseignes et cartes pour commerces, "
 "hôtels et restaurants. Supports conçus pour l'altitude. Devis gratuit.")


# -------------------------------------------------------------------- CAPCIR

pays(
 "graphiste-capcir.html", "Capcir", "le Capcir",
 ["Les Angles", "Matemale", "Formiguères", "Puyvalador", "Réal",
  "La Llagonne", "Fontrabiouse"],
 "Capcir · Pyrénées-Orientales",
 "Graphiste", "au Capcir",
 "Enseignes, cartes et identité visuelle pour les commerces, locations et "
 "restaurants du Capcir. Pensés pour une activité qui se joue sur quelques "
 "mois.",
 """<p>Le Capcir est le plus haut et le plus petit des trois pays de montagne du département&nbsp;: un plateau entre 1&nbsp;500 et 1&nbsp;700&nbsp;mètres, des forêts de pins, des lacs, et une poignée de communes de quelques centaines d'habitants. On l'appelle parfois le petit Canada, et ce n'est pas qu'une image&nbsp;: l'enneigement y est le plus durable du massif.</p>
    <h3>Une économie qui se joue sur quelques mois</h3>
    <p>Les Angles et Formiguères font vivre le territoire l'hiver&nbsp;; l'été ramène les lacs, le VTT et la randonnée. Mais la saison haute reste courte, et un commerce doit y faire l'essentiel de son chiffre. Cela change complètement la façon de concevoir&nbsp;: un support qui met trois semaines à être compris a déjà coûté une partie de la saison.</p>
    <p>Concrètement, ça veut dire des messages courts, une hiérarchie lisible à distance, et une devanture qui dit en trois secondes ce qu'on vend. Le raffinement discret fonctionne très bien en centre-ville&nbsp;; sur un front de neige, il passe inaperçu.</p>
    <h3>Le froid est un paramètre, pas un détail</h3>
    <p>Ici, le gel est la règle plusieurs mois par an. Les adhésifs décollent sur un support froid, les colles ne prennent pas en dessous d'une certaine température, la neige s'accumule sur toute surface horizontale et charge les fixations. Un panneau conçu pour la plaine ne passe pas l'hiver.</p>
    <p>Ces contraintes se traitent au moment du choix du matériau et du façonnage. C'est une conversation à avoir avec le poseur avant de commander&nbsp;— pas au printemps, devant les dégâts.</p>
    <h3>Une clientèle qui vient de loin</h3>
    <p>Le Capcir ne vit pas de sa population&nbsp;: il vit des Perpignanais, des Toulousains, des Catalans du sud et des familles venues passer la semaine. Des gens qui ne connaissent pas les lieux, qui choisissent vite, souvent depuis leur téléphone avant même d'arriver. La cohérence entre ce qu'ils voient en ligne et ce qu'ils trouvent sur place compte donc autant que l'enseigne elle-même.</p>
    <h3>De petites structures, un interlocuteur unique</h3>
    <p>Loueurs, restaurants d'altitude, gîtes, écoles de ski, commerces de village&nbsp;: des structures où le dirigeant décide seul, avec un budget réel et aucun service communication. C'est précisément le type de projet que j'accompagne — un devis clair, pas de jargon, et des fichiers qui vous appartiennent.</p>""",
 [carte("p-corail", "fa-mountain-sun", "Devantures de front de neige",
        "Lisibilité à distance, par mauvais temps et en pleine lumière sur neige. Matériaux choisis pour le gel."),
  carte("p-orange", "fa-house-chimney", "Locations &amp; hébergements",
        "Identité, signalétique intérieure, livret d'accueil et visuels cohérents avec vos annonces en ligne."),
  carte("p-jaune", "fa-bolt", "Supports prêts pour la saison",
        "On travaille en amont pour que tout soit posé à l'ouverture&nbsp;— pas livré trois semaines après.")],
 "au Capcir",
 "Le Capcir est à environ une heure trente de Perpignan. Je monte pour un "
 "relevé ou un rendez-vous&nbsp;; le suivi se fait ensuite à distance, ce qui "
 "évite de multiplier les allers-retours.",
 "Les Angles, Matemale, Formiguères, Puyvalador, Réal, La Llagonne, "
 "Fontrabiouse&nbsp;— et la Cerdagne toute proche.",
 "Graphiste au Capcir — Les Angles, Formiguères | Grafycom",
 "Graphiste au Capcir (66) : enseignes, cartes et identité visuelle pour "
 "les commerces des Angles, de Formiguères et de Matemale. Devis gratuit.")


# ------------------------------------------------------------------- CONFLENT

pays(
 "graphiste-conflent.html", "Conflent", "le Conflent",
 ["Prades", "Villefranche-de-Conflent", "Vernet-les-Bains", "Molitg-les-Bains",
  "Ille-sur-Têt", "Olette", "Mont-Louis", "Vinça"],
 "Conflent · Pyrénées-Orientales",
 "Graphiste", "en Conflent",
 "Enseignes en secteur protégé, identité visuelle et supports pour les "
 "commerces, hébergements et établissements thermaux du Conflent, au pied "
 "du Canigó.",
 """<p>Le Conflent remonte la vallée de la Têt, de la plaine jusqu'à la haute montagne, au pied du Canigó. C'est le pays le plus patrimonial des trois&nbsp;— et c'est ce qui en fait la particularité pour quiconque veut poser une enseigne.</p>
    <h3>Du patrimoine classé, donc des règles</h3>
    <p>Villefranche-de-Conflent, le fort Libéria et la citadelle de Mont-Louis sont inscrits au patrimoine mondial de l'UNESCO depuis 2008, au titre des fortifications de Vauban. Villefranche, bâtie en marbre rose, figure parmi les plus beaux villages de France.</p>
    <p>Dans ces périmètres, une enseigne ne s'improvise pas. Elle relève d'une autorisation préalable, déposée en mairie, et l'avis de l'architecte des Bâtiments de France encadre les matériaux, les couleurs, l'éclairage et jusqu'au mode de fixation. Un lettrage peint ou découpé passe là où un caisson lumineux sera refusé.</p>
    <p>Ce n'est pas un obstacle&nbsp;: c'est un paramètre de conception. Je dessine en tenant compte de ce qui est acceptable dans votre rue, et je vous dis ce qu'il faut déposer. L'ordre compte&nbsp;: vérifier d'abord, dessiner ensuite, fabriquer en dernier. L'inverse coûte une enseigne.</p>
    <h3>Un tourisme de patrimoine et de thermalisme</h3>
    <p>Vernet-les-Bains et Molitg-les-Bains vivent du thermalisme, avec une clientèle qui séjourne plusieurs semaines&nbsp;— un rythme très différent du tourisme de passage de la côte. Le Train jaune, qui part de Villefranche-de-Conflent pour rejoindre Latour-de-Carol sur 63&nbsp;kilomètres et jusqu'à 1&nbsp;600&nbsp;mètres, amène toute l'année des visiteurs dans des villages qui n'en auraient pas autrement.</p>
    <p>Pour un commerce, cela signifie une clientèle qui a le temps de regarder, de revenir, de comparer. Une image soignée se remarque ici davantage qu'ailleurs.</p>
    <h3>Prades et la plaine du Conflent</h3>
    <p>Prades concentre les commerces et les services du secteur. Les contraintes patrimoniales y sont moins serrées qu'à Villefranche, mais le centre ancien reste encadré. Si votre activité est à Prades même, la page <a href="graphiste-prades.html">graphiste à Prades</a> y est consacrée.</p>""",
 [carte("p-violet", "fa-landmark", "Enseignes en secteur protégé",
        "Conception compatible avec l'avis des Bâtiments de France, relevé sur place, et le dossier à déposer en mairie."),
  carte("p-bleu", "fa-spa", "Thermalisme &amp; hébergement",
        "Supports pour une clientèle qui séjourne&nbsp;: livret d'accueil, signalétique, documents de séjour cohérents."),
  carte("p-turq", "fa-feather-pointed", "Logo &amp; identité",
        "Charte complète, déclinaisons et fichiers sources vectoriels. De quoi tenir dix ans, quel que soit le prestataire.")],
 "en Conflent",
 "Le Conflent commence à trente minutes de Perpignan et Prades est à "
 "quarante. Un rendez-vous sur place, un relevé de cotes ou un point avec le "
 "poseur ne posent aucune difficulté.",
 "Prades, Villefranche-de-Conflent, Vernet-les-Bains, Molitg-les-Bains, "
 "Ille-sur-Têt, Vinça, Olette, Mont-Louis&nbsp;— et la Cerdagne en remontant "
 "la vallée.",
 "Graphiste en Conflent — enseignes en secteur protégé | Grafycom",
 "Graphiste en Conflent (66) : enseignes en secteur protégé, identité "
 "visuelle et supports pour Prades, Villefranche-de-Conflent et Vernet. "
 "Devis gratuit.")

print("pays : 3 pages produites")
