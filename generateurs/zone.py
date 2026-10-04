# -*- coding: utf-8 -*-
"""Page « zone d'intervention » : les 12 pages locales, puis les 226 communes.

Une seule page pour tout le reste du département. C'est le bon endroit pour
nommer les petites communes : une page par village de 40 habitants serait une
page satellite, une liste sur une page utile n'en est pas une.
"""
import json, pathlib, html
from gen import page, appel, TEL, TEL_URI

com = json.load(open(pathlib.Path(__file__).resolve().parent / "communes66.json", encoding="utf-8"))
com = sorted([c["nom"] for c in com])

VEDETTES = [
 ("infographiste-perpignan.html", "Perpignan", "Enseignes en secteur protégé, cartes, identité"),
 ("graphiste-canet-en-roussillon.html", "Canet-en-Roussillon", "Cartes de saison, devantures de front de mer"),
 ("graphiste-saint-cyprien.html", "Saint-Cyprien", "Commerces de port, signalétique de résidence"),
 ("graphiste-argeles-sur-mer.html", "Argelès-sur-Mer", "Signalétique de camping, supports multilingues"),
 ("graphiste-le-barcares.html", "Le Barcarès", "Camping, événementiel, multilingue"),
 ("graphiste-elne.html", "Elne", "Producteurs, vente directe, centre ancien"),
 ("graphiste-rivesaltes.html", "Rivesaltes", "Étiquettes de vin, artisans, véhicules"),
 ("graphiste-thuir.html", "Thuir", "Étiquettes et gammes, accueil au caveau"),
 ("graphiste-collioure.html", "Collioure", "Site protégé, appellations, galeries"),
 ("graphiste-ceret.html", "Céret", "Étiquettes de producteur, affiches, associations"),
 ("graphiste-prades.html", "Prades", "Affiches, programmes, producteurs de montagne"),
 ("graphiste-font-romeu.html", "Font-Romeu", "Montagne, saison inversée, clubs sportifs"),
]

cartes = "\n    ".join(
  '<a class="carte carte-creme" href="%s" style="text-decoration:none">'
  '<h3 style="margin-bottom:6px">%s</h3><p>%s</p>'
  '<p style="margin-top:12px;color:var(--violet);font-weight:600;font-size:14px">Voir la page '
  '<i class="fa-solid fa-arrow-right" aria-hidden="true"></i></p></a>' % (s, v, d)
  for s, v, d in VEDETTES)

liste = "".join("<li>%s</li>" % html.escape(n) for n in com)

BODY = """
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">Pyrénées-Orientales</span>
    <h1>Où je travaille<br><span class="texte-degrade">dans le 66</span></h1>
    <div class="trait"></div>
    <p class="chapeau">Installée à Perpignan, je me déplace dans tout le département — et je travaille en visio pour le reste. Ci-dessous, les communes où j'interviens le plus souvent, puis la liste complète des %d communes des Pyrénées-Orientales.</p>
    <div class="groupe-btn" style="margin-top:30px">
      <a href="contact.html" class="btn btn-couleur">Demander un devis <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
      <a href="tel:%s" class="btn btn-secondaire"><i class="fa-solid fa-phone" aria-hidden="true"></i> %s</a>
    </div>
  </div>
</section>

<section>
  <div class="conteneur centre">
    <span class="eyebrow">Douze communes</span>
    <h2>Là où j'interviens le plus</h2>
    <div class="trait"></div>
    <p class="chapeau">Chaque page dit ce qui change vraiment d'une commune à l'autre&nbsp;: les règles d'enseigne, la saisonnalité, le type d'activité dominante.</p>
  </div>
  <div class="conteneur grille g3" style="margin-top:44px">
    %s
  </div>
</section>

<section class="fond-creme">
  <div class="conteneur">
    <div class="centre">
      <span class="eyebrow">Le département entier</span>
      <h2>Les %d communes du 66</h2>
      <div class="trait"></div>
      <p class="chapeau">Votre commune n'a pas sa page&nbsp;? Cela ne change rien&nbsp;: le devis est gratuit partout, et le premier échange se fait au téléphone ou en visio de toute façon.</p>
    </div>
    <ul class="communes">%s</ul>
    <p class="centre" style="margin-top:30px;font-size:14px;color:var(--taupe)">Liste établie d'après le répertoire officiel des communes (geo.api.gouv.fr).</p>
  </div>
</section>

<section>
  <div class="conteneur prose">
    <h2 style="margin-top:0">Se déplacer, ou travailler à distance</h2>
    <p>La distance n'est pas le sujet. Un premier échange par téléphone ou en visio suffit presque toujours à cadrer un projet et à établir un devis, et l'essentiel du travail se fait par échange de fichiers.</p>
    <p>Le déplacement devient utile dans trois cas&nbsp;: relever les cotes d'une devanture, d'une vitrine ou d'un véhicule&nbsp;; voir un produit, un atelier ou un lieu qu'on ne peut pas décrire au téléphone&nbsp;; ou tout simplement parce que vous préférez qu'on se rencontre. Dans le premier cercle autour de Perpignan, le rendez-vous ne coûte rien de plus.</p>
    <div class="encart">
      <strong>Et au-delà du département&nbsp;?</strong> Une partie de mes clients ne m'a jamais rencontrée en personne, et cela n'a rien changé au résultat. Aude, Ariège, Haute-Garonne, Catalogne espagnole&nbsp;: l'accompagnement se fait aussi bien à distance, en français comme en espagnol.
    </div>
  </div>
</section>

""" % (len(com), TEL_URI, TEL, cartes, len(com), liste)

BODY += appel("Votre commune, votre projet",
  "Le premier échange est gratuit et sans engagement, où que vous soyez dans le département.",
  fond="fond-creme")

JSONLD = """{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Grafycom",
  "description": "Infographiste à Perpignan intervenant dans tout le département des Pyrénées-Orientales.",
  "url": "https://www.grafycom.fr/zone-intervention.html",
  "telephone": "+33782921981",
  "address": { "@type": "PostalAddress", "addressLocality": "Perpignan", "postalCode": "66000", "addressCountry": "FR" },
  "areaServed": { "@type": "AdministrativeArea", "name": "Pyrénées-Orientales" },
  "knowsLanguage": [ "fr", "es" ]
}"""

page("zone-intervention.html",
     "Zone d'intervention — Grafycom dans les Pyrénées-Orientales",
     "Graphiste à Perpignan intervenant dans les %d communes des Pyrénées-Orientales. Douze pages locales et la liste complète du département." % len(com),
     BODY, ogtitle="Où je travaille dans le 66 — Grafycom", jsonld=JSONLD)
