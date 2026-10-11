# -*- coding: utf-8 -*-
"""Gabarit des pages locales. Ne produit aucune page à lui seul.

Les douze communes sont réparties dans villes.py à villes6.py, qui
appellent locale() d'ici. Douze, et pas les 226 du département : des pages
quasi identiques déclinées partout sont traitées par Google comme des
« pages satellites » et peuvent faire déclasser le site entier. Mieux vaut
peu de pages qui disent chacune quelque chose de vrai sur le territoire
qu'elles visent — zone-intervention.html couvre le reste en une page.
"""
from gen import page, appel, TEL, TEL_URI, MAIL

GABARIT = """
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1a}<br><span class="texte-degrade">{h1b}</span></h1>
    <div class="trait"></div>
    <p class="chapeau">{chapeau}</p>
    <div class="groupe-btn" style="margin-top:30px">
      <a href="contact.html" class="btn btn-couleur">Demander un devis <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
      <a href="tel:{tel_uri}" class="btn btn-secondaire"><i class="fa-solid fa-phone" aria-hidden="true"></i> {tel}</a>
    </div>
  </div>
</section>

<section>
  <div class="conteneur prose">
    <h2 style="margin-top:0">Ce que {ville} a de particulier</h2>
    {particularites}
  </div>
</section>

<section class="fond-creme">
  <div class="conteneur centre">
    <span class="eyebrow">Sur place</span>
    <h2>Ce que je fais le plus {a_ville}</h2>
    <div class="trait"></div>
  </div>
  <div class="conteneur grille g3" style="margin-top:44px">
    {cartes}
  </div>
</section>

<section>
  <div class="conteneur prose">
    <h2 style="margin-top:0">Se déplacer, ou pas</h2>
    <p>{deplacement}</p>
    <div class="encart">
      <strong>Concrètement&nbsp;:</strong> un premier échange par téléphone ou en visio suffit presque toujours à cadrer un projet et à établir un devis. Le déplacement se justifie quand il faut relever des cotes — une devanture, une vitrine, un véhicule — ou quand vous préférez simplement qu'on se voie.
    </div>
    <h2>Les communes voisines</h2>
    <p>{voisines}</p>
    <h2>Selon votre situation</h2>
    <p>Trois pages répondent plus précisément que celle-ci selon le moment où vous me lisez&nbsp;: <a href="ouverture-commerce-66.html">vous ouvrez un commerce</a> et vous cherchez l'ordre dans lequel préparer vos supports&nbsp;; <a href="refaire-son-image.html">votre entreprise a des années</a> et son image ne la raconte plus&nbsp;; ou vous avez <a href="enseigne-perpignan.html">une façade à habiller</a>. Les restaurateurs trouveront le détail de ce qui les concerne sur la page <a href="graphiste-restaurant-perpignan.html">graphiste pour restaurant</a>.</p>

    <p>Et partout ailleurs en visio&nbsp;: une partie de mes clients ne m'a jamais rencontrée en personne, ce qui n'a rien changé au résultat. La liste complète des communes du département est sur la page <a href="zone-intervention.html">zone d'intervention</a>.</p>
  </div>
</section>
{secteur}
"""


# ---------------------------------------------------------------- SECTEUR
# Maillage interne entre pages locales.
#
# Le constat qui l'a motive : quatorze pages de villes sur seize ne
# recevaient qu'UN seul lien editorial. Elles existaient, bien ecrites, et
# ne recevaient presque aucune autorite du reste du site. Le gabarit liait
# deja les pages thematiques - d'ou leurs quinze a dix-huit liens - mais
# jamais une ville vers sa voisine.
#
# Les voisinages sont poses a la main : communes66.json ne porte ni
# coordonnees ni limites, seulement un nom, une population et un code. On
# ne peut donc pas calculer une distance, et inventer une mitoyennete
# serait pire que de s'abstenir. D'ou la formule « dans le meme secteur »,
# qui dit un voisinage de zone et n'affirme aucune limite commune.
#
# Trois voisines par page, pas davantage : au-dela on ecrit une liste de
# liens, et une liste de liens ne se lit pas - elle se saute, et elle
# ressemble a ce qu'elle ne doit pas etre.
VOISINS = {
    # Littoral, du nord au sud
    "graphiste-le-barcares.html":        ["graphiste-canet-en-roussillon.html", "graphiste-claira.html", "graphiste-fitou.html"],
    "graphiste-canet-en-roussillon.html":["graphiste-saint-cyprien.html", "graphiste-le-barcares.html", "graphiste-claira.html"],
    "graphiste-saint-cyprien.html":      ["graphiste-canet-en-roussillon.html", "graphiste-elne.html", "graphiste-collioure.html"],
    "graphiste-argeles-sur-mer.html":    ["graphiste-collioure.html", "graphiste-elne.html", "graphiste-ceret.html"],
    "graphiste-collioure.html":          ["graphiste-argeles-sur-mer.html", "graphiste-elne.html", "graphiste-saint-cyprien.html"],
    # Plaine sud et Aspres
    "graphiste-elne.html":               ["graphiste-argeles-sur-mer.html", "graphiste-saint-cyprien.html", "graphiste-thuir.html"],
    "graphiste-thuir.html":              ["graphiste-elne.html", "graphiste-ceret.html", "graphiste-le-soler.html"],
    # Vallespir
    "graphiste-ceret.html":              ["graphiste-thuir.html", "graphiste-elne.html", "graphiste-argeles-sur-mer.html"],
    # Couronne nord-ouest de Perpignan et Ribéral
    "graphiste-saint-esteve.html":       ["graphiste-baho.html", "graphiste-peyrestortes.html", "graphiste-le-soler.html"],
    "graphiste-le-soler.html":           ["graphiste-baho.html", "graphiste-saint-esteve.html", "graphiste-thuir.html"],
    "graphiste-baho.html":               ["graphiste-le-soler.html", "graphiste-saint-esteve.html", "graphiste-peyrestortes.html"],
    "graphiste-peyrestortes.html":       ["graphiste-rivesaltes.html", "graphiste-saint-esteve.html", "graphiste-baho.html"],
    # Salanque et porte nord
    "graphiste-rivesaltes.html":         ["graphiste-peyrestortes.html", "graphiste-salses-le-chateau.html", "graphiste-claira.html"],
    "graphiste-claira.html":             ["graphiste-rivesaltes.html", "graphiste-le-barcares.html", "graphiste-salses-le-chateau.html"],
    "graphiste-salses-le-chateau.html":  ["graphiste-rivesaltes.html", "graphiste-claira.html", "graphiste-fitou.html"],
    "graphiste-fitou.html":              ["graphiste-salses-le-chateau.html", "graphiste-claira.html", "graphiste-rivesaltes.html"],
    # Conflent et haute montagne
    "graphiste-prades.html":             ["graphiste-conflent.html", "graphiste-cerdagne.html", "graphiste-thuir.html"],
    "graphiste-conflent.html":           ["graphiste-prades.html", "graphiste-capcir.html", "graphiste-cerdagne.html"],
    "graphiste-cerdagne.html":           ["graphiste-font-romeu.html", "graphiste-capcir.html", "graphiste-conflent.html"],
    "graphiste-capcir.html":             ["graphiste-cerdagne.html", "graphiste-font-romeu.html", "graphiste-conflent.html"],
    "graphiste-font-romeu.html":         ["graphiste-cerdagne.html", "graphiste-capcir.html", "graphiste-prades.html"],
    # Perpignan, qui est le centre et non une voisine comme les autres
    "infographiste-perpignan.html":      ["graphiste-saint-esteve.html", "graphiste-rivesaltes.html", "graphiste-canet-en-roussillon.html"],
}

LIBELLES = {
    "graphiste-argeles-sur-mer.html": "Argelès-sur-Mer",
    "graphiste-canet-en-roussillon.html": "Canet-en-Roussillon",
    "graphiste-capcir.html": "le Capcir",
    "graphiste-cerdagne.html": "la Cerdagne",
    "graphiste-ceret.html": "Céret",
    "graphiste-collioure.html": "Collioure",
    "graphiste-conflent.html": "le Conflent",
    "graphiste-elne.html": "Elne",
    "graphiste-font-romeu.html": "Font-Romeu",
    "graphiste-le-barcares.html": "Le Barcarès",
    "graphiste-prades.html": "Prades",
    "graphiste-baho.html": "Baho",
    "graphiste-claira.html": "Claira",
    "graphiste-fitou.html": "Fitou",
    "graphiste-le-soler.html": "Le Soler",
    "graphiste-peyrestortes.html": "Peyrestortes",
    "graphiste-rivesaltes.html": "Rivesaltes",
    "graphiste-saint-esteve.html": "Saint-Estève",
    "graphiste-salses-le-chateau.html": "Salses-le-Château",
    "graphiste-saint-cyprien.html": "Saint-Cyprien",
    "graphiste-thuir.html": "Thuir",
    "infographiste-perpignan.html": "Perpignan",
}


def bloc_secteur(slug):
    """Les trois voisines, plus Perpignan, en fin de page.

    Perpignan est ajoutee partout sauf sur sa propre page : c'est le
    centre economique du departement, et la page vers laquelle un
    visiteur qui elargit sa recherche doit pouvoir aller d'un clic.
    """
    voisins = list(VOISINS.get(slug, []))
    if not voisins:
        return ""
    liens = ", ".join(
        '<a href="%s">%s</a>' % (v, LIBELLES[v]) for v in voisins)
    centre = ""
    if slug != "infographiste-perpignan.html":
        centre = (' Et <a href="infographiste-perpignan.html">Perpignan</a>'
                  ' pour le reste du département.')
    # Pas de fond-creme : l'appel a l'action qui suit en porte un, et deux
    # sections de la meme couleur se fondent l'une dans l'autre. Mesure
    # faite au rendu, pas devinee - les deux sortaient en rgb(247,241,239).
    return """
<section style="padding-top:0">
  <div class="conteneur" style="max-width:760px">
    <p class="encart" style="margin:0"><strong>Dans le même secteur&nbsp;:</strong> %s.%s</p>
  </div>
</section>
""" % (liens, centre)

def carte(picto, icone, titre, texte):
    return ('<article class="carte carte-creme"><div class="picto %s"><i class="fa-solid %s" aria-hidden="true"></i></div>'
            '<h3>%s</h3><p>%s</p></article>' % (picto, icone, titre, texte))

def jsonld(ville, cp, slug):
    return """{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Grafycom — infographiste à %s",
  "description": "Création de logo, identité visuelle et supports de communication à %s (%s).",
  "url": "https://grafycom.fr/%s",
  "telephone": "+33782921981",
  "email": "%s",
  "slogan": "L'image qui vous ressemble",
  "address": { "@type": "PostalAddress", "addressLocality": "Perpignan", "postalCode": "66000", "addressRegion": "Pyrénées-Orientales", "addressCountry": "FR" },
  "areaServed": { "@type": "City", "name": "%s", "postalCode": "%s" },
  "knowsLanguage": [ "fr", "es" ]
}""" % (ville, ville, cp, slug, MAIL, ville, cp)

def locale(slug, ville, cp, eyebrow, h1a, h1b, chapeau, particularites, cartes,
           a_ville, deplacement, voisines, title, desc):
    corps = GABARIT.format(
        eyebrow=eyebrow, h1a=h1a, h1b=h1b, chapeau=chapeau, ville=ville,
        particularites=particularites, cartes="\n    ".join(cartes),
        a_ville=a_ville, deplacement=deplacement, voisines=voisines,
        tel=TEL, tel_uri=TEL_URI, secteur=bloc_secteur(slug))
    corps += appel(
        "Un projet %s&nbsp;?" % a_ville,
        "Le premier échange est gratuit et sans engagement. Décrivez-moi votre activité et ce qui vous gêne dans votre image&nbsp;: je vous réponds sous 48&nbsp;heures ouvrées.",
        fond="fond-creme")
    page(slug, title, desc, corps, ogtitle=title.split(" | ")[0], jsonld=jsonld(ville, cp, slug))
