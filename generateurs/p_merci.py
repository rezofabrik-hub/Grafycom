# -*- coding: utf-8 -*-
"""Page de confirmation, affichée après l'envoi réussi du formulaire."""
from gen import page, TEL, TEL_URI, MAIL, ACCUEIL

BODY = """
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">Message envoyé</span>
    <h1>Merci,<br><span class="texte-degrade">c'est bien parti</span></h1>
    <div class="trait"></div>
    <p class="chapeau">Votre demande est arrivée. Je vous réponds sous 48&nbsp;heures ouvrées, avec un avis honnête sur ce dont vous avez besoin — et un devis détaillé si le projet s'y prête.</p>
    <div class="groupe-btn" style="margin-top:32px">
      <a href="%(accueil)s" class="btn btn-couleur">Retour à l'accueil <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
      <a href="tel:%(tel_uri)s" class="btn btn-secondaire"><i class="fa-solid fa-phone" aria-hidden="true"></i> %(tel)s</a>
    </div>
  </div>
</section>

<section>
  <div class="conteneur centre">
    <h2>En attendant</h2>
    <div class="trait"></div>
    <p class="chapeau">Si votre projet est urgent, le téléphone reste le plus rapide. Sinon, vous pouvez parcourir le détail des prestations ou la méthode de travail.</p>
  </div>
  <div class="conteneur grille g3" style="margin-top:44px">
    <a class="carte carte-creme" href="prestations.html" style="text-decoration:none">
      <div class="picto p-bleu"><i class="fa-solid fa-feather-pointed" aria-hidden="true"></i></div>
      <h3>Les prestations</h3><p>Logo, identité visuelle, menus, supports imprimés, signalétique, réseaux.</p></a>
    <a class="carte carte-creme" href="methode.html" style="text-decoration:none">
      <div class="picto p-violet"><i class="fa-solid fa-route" aria-hidden="true"></i></div>
      <h3>La méthode</h3><p>Les six étapes d'un projet, et ce qui est attendu de vous.</p></a>
    <a class="carte carte-creme" href="a-propos.html" style="text-decoration:none">
      <div class="picto p-corail"><i class="fa-solid fa-heart" aria-hidden="true"></i></div>
      <h3>À propos</h3><p>Qui est derrière Grafycom, et comment je travaille.</p></a>
  </div>
</section>
""" % {"tel": TEL, "tel_uri": TEL_URI, "accueil": ACCUEIL}

page("merci.html", "Message envoyé — Grafycom",
     "Votre demande a bien été envoyée à Grafycom. Réponse sous 48 heures ouvrées.",
     BODY, ogtitle="Message envoyé — Grafycom", robots="noindex, nofollow")
