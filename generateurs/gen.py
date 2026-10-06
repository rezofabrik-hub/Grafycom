# -*- coding: utf-8 -*-
"""Assemble les pages du site Grafycom (en-tete/pied communs + contenu par page)."""
import os, io, pathlib

SITE = "https://www.grafycom.fr"

# Mode chantier : passer à False pour ouvrir le site au public et aux moteurs.
CONSTRUCTION = False

# Le formulaire est traité par le Worker Cloudflare (src/index.js), qui envoie
# le message via Resend. Ni clé ni adresse ici : ce sont des secrets Cloudflare.
#
# False tant que le site est servi par GitHub Pages, qui ne sait pas exécuter
# de code : le formulaire garde alors son repli par courriel. Passer à True le
# jour où Cloudflare sert le site.
FORMULAIRE_ACTIF = False
ENVOI_FORMULAIRE = "/api/contact"

# Jeton de validation de la Google Search Console, methode « balise HTML ».
# Vide = aucune balise emise. Le jeton n'est pas un secret : c'est une chaine
# publique que Google lit dans la page pour confirmer qu'on tient le site. Il
# s'obtient dans la Search Console (voir outils/SEARCH-CONSOLE.md) et se colle
# ici tel quel, sans les chevrons ni le reste de la balise.
GOOGLE_VERIF = ""
# La racine du dépôt : le dossier qui contient celui-ci.
OUT = str(pathlib.Path(__file__).resolve().parent.parent)
MAIL = "sandra.grafycom@gmail.com"
TEL = "07 82 92 19 81"
TEL_URI = "+33782921981"

# Pendant les travaux, la racine sert la page de chantier et le vrai site
# vit dans accueil.html. À l'ouverture, la page d'accueil reprend sa place
# à la racine. Une seule constante gouverne les deux cas : la navigation,
# le logo et le lien de la page « merci » suivent sans qu'on y pense.
ACCUEIL = "accueil.html" if CONSTRUCTION else "index.html"

NAV = [
    (ACCUEIL, "Accueil"),
    ("prestations.html", "Prestations"),
    ("realisations.html", "Réalisations"),
    ("blog.html", "Blog"),
    ("methode.html", "Méthode"),
    ("a-propos.html", "À propos"),
    ("contact.html", "Contact"),
]

HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}/{slug}">
<meta name="robots" content="{robots}">
<meta name="author" content="Grafycom">
{verif}
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Grafycom">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}/{slug}">
<meta property="og:image" content="{site}/assets/img/logo-grafycom-carre.jpg">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="assets/img/logo-grafycom-carre.jpg">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; form-action 'self' mailto:; frame-ancestors 'none'; base-uri 'self'; object-src 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="assets/fa/css/all.min.css">
<link rel="stylesheet" href="assets/style.css">
{jsonld}</head>
<body>

<div class="bandeau">Studio de communication visuelle à Perpignan — <a href="contact.html">premier échange gratuit</a></div>

<header>
  <div class="entete">
    <a class="logo" href="{accueil}" aria-label="Grafycom, accueil">
      <img src="assets/img/logo-grafycom.webp" alt="Grafycom — L'image qui vous ressemble" width="960" height="384">
    </a>
    <nav class="principal" id="menu">
{nav}
    </nav>
    <a href="contact.html" class="btn btn-primaire">Parlons de votre projet</a>
    <button class="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu"><i class="fa-solid fa-bars" aria-hidden="true"></i></button>
  </div>
</header>

<main>
"""

FOOT = """</main>

<footer>
  <div class="conteneur">
    <div class="pied-grille">
      <div>
        <div class="pied-logo"><img src="assets/img/logo-grafycom.webp" alt="Grafycom" width="960" height="384"></div>
        <p>Infographiste et chef de projet à Perpignan. Solutions 360° et sur mesure pour les entreprises, commerces et associations des Pyrénées-Orientales.</p>
        <!-- Réseaux sociaux : bloc retiré tant que les adresses réelles ne sont
             pas connues. Pointer vers l'accueil de Facebook ou d'Instagram est
             pire que ne rien afficher. Pour le rétablir, remplacer les # par les
             vraies URL et décommenter.
        <div class="pied-social">
          <a href="#" aria-label="Facebook" rel="noopener"><i class="fa-brands fa-facebook-f" aria-hidden="true"></i></a>
          <a href="#" aria-label="Instagram" rel="noopener"><i class="fa-brands fa-instagram" aria-hidden="true"></i></a>
        </div>
        -->
      </div>
      <div>
        <h4>Prestations</h4>
        <ul>
          <li><a href="prestations.html#identite">Identité visuelle</a></li>
          <li><a href="prestations.html#menus">Menus &amp; cartes</a></li>
          <li><a href="prestations.html#print">Supports imprimés</a></li>
          <li><a href="prestations.html#signaletique">Signalétique</a></li>
          <li><a href="prestations.html#digital">Réseaux &amp; web</a></li>
        </ul>
      </div>
      <div>
        <h4>Le studio</h4>
        <ul>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="a-propos.html">À propos</a></li>
          <li><a href="methode.html">Méthode</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Par situation</h4>
        <ul>
          <li><a href="ouverture-commerce-66.html">J'ouvre un commerce</a></li>
          <li><a href="refaire-son-image.html">Mon image a vieilli</a></li>
          <li><a href="graphiste-restaurant-perpignan.html">Je tiens un restaurant</a></li>
          <li><a href="enseigne-perpignan.html">J'ai une façade à habiller</a></li>
        </ul>
      </div>
      <div>
        <h4>Zone d'intervention</h4>
        <ul>
          <li><a href="infographiste-perpignan.html">Perpignan</a></li>
          <li><a href="graphiste-canet-en-roussillon.html">Canet-en-Roussillon</a></li>
          <li><a href="graphiste-argeles-sur-mer.html">Argelès-sur-Mer</a></li>
          <li><a href="graphiste-saint-cyprien.html">Saint-Cyprien</a></li>
          <li><a href="graphiste-collioure.html">Collioure</a></li>
          <li><a href="zone-intervention.html"><strong>Tout le 66 &rarr;</strong></a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:{tel_uri}">{tel}</a></li>
          <li><a href="mailto:{mail}">{mail}</a></li>
          <li>Perpignan · Pyrénées-Orientales</li>
          <li><a href="cgv.html">CGV</a></li>
          <li><a href="mentions-legales.html">Mentions légales</a></li>
          <li><a href="confidentialite.html">Confidentialité</a></li>
        </ul>
      </div>
    </div>
    <div class="pied-bas">
      <span>© <span data-annee>2026</span> Grafycom — L'image qui vous ressemble</span>
      <span class="mono">Perpignan · 66</span>
    </div>
  </div>
</footer>

<script src="assets/site.js"></script>
</body>
</html>
"""

APPEL = """<section class="{fond}">
  <div class="conteneur">
    <div class="appel">
      <h2>{titre}</h2>
      <p>{texte}</p>
      <div class="groupe-btn"><a href="contact.html" class="btn btn-clair">Demander un devis <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></div>
    </div>
  </div>
</section>

"""

def appel(titre, texte, fond=""):
    return APPEL.format(titre=titre, texte=texte, fond=fond)

def page(slug, title, desc, body, ogtitle=None, jsonld="", robots="index, follow"):
    if CONSTRUCTION:
        robots = "noindex, nofollow"
    nav = "\n".join(
        '      <a href="%s"%s>%s</a>' % (h, ' class="actif"' if h == slug else "", l)
        for h, l in NAV
    )
    jl = ('<script type="application/ld+json">\n%s\n</script>\n' % jsonld) if jsonld else ""
    verif = ('<meta name="google-site-verification" content="%s">\n' % GOOGLE_VERIF) if GOOGLE_VERIF else ""
    html = HEAD.format(title=title, desc=desc, site=SITE, accueil=ACCUEIL,
                       slug="" if slug in ("accueil.html", "index.html") else slug,
                       ogtitle=ogtitle or title, nav=nav, jsonld=jl, robots=robots,
                       verif=verif)
    html += body
    html += FOOT.format(mail=MAIL, tel=TEL, tel_uri=TEL_URI)
    with io.open(os.path.join(OUT, slug), "w", encoding="utf-8") as f:
        f.write(html)
    print("%-24s %6d octets" % (slug, len(html.encode("utf-8"))))
