# -*- coding: utf-8 -*-
"""Page Boutique : en attente d'ouverture (demande de Laurent, 18/11/2026).

La boutique en ligne de Sandra n'existe pas encore. La rubrique est dans
le menu, et la page dit simplement qu'elle arrive. Aucun produit, aucun
prix, aucun paiement : tant que rien n'est en vente, la page n'annonce rien
qu'on ne pourrait pas tenir.

noindex : une page « bientôt disponible » n'a rien a faire dans les
resultats de recherche. Elle n'est pas non plus dans sitemap.xml. A
l'ouverture de la vraie boutique, repasser en « index, follow » et
l'ajouter au sitemap.
"""
from gen import page, TEL, TEL_URI

BODY = """
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">Boutique</span>
    <h1>Bientôt<br><span class="texte-degrade">disponible</span></h1>
    <div class="trait"></div>
    <p class="chapeau">La boutique Grafycom ouvre bientôt. En attendant, contactez-moi pour toute demande&nbsp;: je vous réponds avec plaisir.</p>
    <div class="groupe-btn" style="margin-top:32px">
      <a href="contact.html" class="btn btn-couleur">Me contacter <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
      <a href="tel:%(tel_uri)s" class="btn btn-secondaire"><i class="fa-solid fa-phone" aria-hidden="true"></i> %(tel)s</a>
    </div>
  </div>
</section>

<section>
  <div class="conteneur centre">
    <h2>En attendant l'ouverture</h2>
    <div class="trait"></div>
    <p class="chapeau">Découvrez ce que le studio réalise déjà pour les entreprises, commerces et associations des Pyrénées-Orientales.</p>
  </div>
  <div class="conteneur grille g3" style="margin-top:44px">
    <a class="carte carte-creme" href="prestations.html" style="text-decoration:none">
      <div class="picto p-bleu"><i class="fa-solid fa-feather-pointed" aria-hidden="true"></i></div>
      <h3>Les prestations</h3><p>Logo, identité visuelle, menus, supports imprimés, signalétique, réseaux.</p></a>
    <a class="carte carte-creme" href="realisations.html" style="text-decoration:none">
      <div class="picto p-violet"><i class="fa-solid fa-images" aria-hidden="true"></i></div>
      <h3>Les réalisations</h3><p>Quelques projets menés pour des clients du département.</p></a>
    <a class="carte carte-creme" href="contact.html" style="text-decoration:none">
      <div class="picto p-corail"><i class="fa-solid fa-envelope" aria-hidden="true"></i></div>
      <h3>Contact</h3><p>Une question, un projet&nbsp;? Écrivez-moi ou appelez-moi.</p></a>
  </div>
</section>
""" % {"tel": TEL, "tel_uri": TEL_URI}

page("boutique.html", "Boutique — bientôt disponible | Grafycom",
     "La boutique en ligne Grafycom ouvre bientôt. En attendant, contactez le studio pour toute demande.",
     BODY, ogtitle="Boutique Grafycom — bientôt disponible", robots="noindex, follow")
