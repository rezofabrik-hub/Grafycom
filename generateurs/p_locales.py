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
    <p>Et partout ailleurs en visio&nbsp;: une partie de mes clients ne m'a jamais rencontrée en personne, ce qui n'a rien changé au résultat. La liste complète des communes du département est sur la page <a href="zone-intervention.html">zone d'intervention</a>.</p>
  </div>
</section>

"""

def carte(picto, icone, titre, texte):
    return ('<article class="carte carte-creme"><div class="picto %s"><i class="fa-solid %s" aria-hidden="true"></i></div>'
            '<h3>%s</h3><p>%s</p></article>' % (picto, icone, titre, texte))

def jsonld(ville, cp, slug):
    return """{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Grafycom — infographiste à %s",
  "description": "Création de logo, identité visuelle et supports de communication à %s (%s).",
  "url": "https://www.grafycom.fr/%s",
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
        tel=TEL, tel_uri=TEL_URI)
    corps += appel(
        "Un projet %s&nbsp;?" % a_ville,
        "Le premier échange est gratuit et sans engagement. Décrivez-moi votre activité et ce qui vous gêne dans votre image&nbsp;: je vous réponds sous 48&nbsp;heures ouvrées.",
        fond="fond-creme")
    page(slug, title, desc, corps, ogtitle=title.split(" | ")[0], jsonld=jsonld(ville, cp, slug))
