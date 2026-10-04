# -*- coding: utf-8 -*-
from gen import page, appel

def reaz(cat, titre, desc, fichier):
    return """    <article class="reaz">
      <div class="reaz-vignette"><img src="assets/img/realisations/%s" alt="%s" data-attente="Visuel à venir" loading="lazy"></div>
      <div class="reaz-texte"><span>%s</span><h3>%s</h3><p>%s</p></div>
    </article>
""" % (fichier, titre, cat, titre, desc)

GALERIE = "".join([
    reaz("Identité visuelle", "Création de logo", "Recherche, esquisses, déclinaisons et charte d'usage.", "logo-01.jpg"),
    reaz("Restauration", "Carte de restaurant", "Mise en page, hiérarchie des prix, déclinaison saisonnière.", "carte-01.jpg"),
    reaz("Signalétique", "Enseigne de façade", "Du fichier à la pose, en lien avec l'imprimeur et le poseur.", "enseigne-01.jpg"),
    reaz("Print", "Cartes de visite", "Papier, finition et façonnage choisis avec le client.", "print-01.jpg"),
    reaz("Véhicule", "Marquage de flotte", "Un gabarit décliné sur plusieurs véhicules.", "vehicule-01.jpg"),
    reaz("Événement", "Affiche &amp; programme", "Une saison culturelle déclinée sur tous ses supports.", "evenement-01.jpg"),
])

BODY = """
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">Réalisations</span>
    <h1>Des projets, <span class="texte-degrade">pas des maquettes</span></h1>
    <div class="trait"></div>
    <p class="chapeau">Chaque projet part d'une page blanche et d'une conversation. Voici une sélection de travaux et, pour chacun, ce qu'il fallait résoudre.</p>
  </div>
</section>

<section>
  <!-- À DÉPOSER : les photos de cette galerie vont dans assets/img/realisations/
       (noms attendus : logo-01.jpg, carte-01.jpg, enseigne-01.jpg, print-01.jpg,
       vehicule-01.jpg, evenement-01.jpg). Tant qu'un fichier manque, un cadre
       explicite s'affiche à la place. Voir le README. -->
  <div class="conteneur galerie">
""" + GALERIE + """  </div>
</section>

<section class="fond-creme">
  <div class="conteneur centre">
    <span class="eyebrow">Ce que disent mes clients</span>
    <h2>Les avis, bientôt ici</h2>
    <div class="trait"></div>
    <p class="chapeau">Cet espace est volontairement vide&nbsp;: il accueillera de vrais témoignages, signés, et non des phrases inventées pour faire joli. Si nous avons travaillé ensemble et que le résultat vous a plu, votre avis a toute sa place ici.</p>
    <div class="groupe-btn" style="margin-top:28px">
      <a href="contact.html" class="btn btn-secondaire">Laisser un avis</a>
    </div>
  </div>
</section>

<section>
  <div class="conteneur centre">
    <span class="eyebrow">Confidentialité</span>
    <h2>Un projet qui n'apparaît pas ici&nbsp;?</h2>
    <div class="trait"></div>
    <p class="chapeau">Certains travaux — packagings en cours de lancement, refontes pas encore annoncées, dossiers internes — ne sont pas publiables. Je peux vous les montrer lors d'un rendez-vous, avec l'accord du client concerné.</p>
  </div>
</section>

""" + appel(
    "Votre projet a sa place ici",
    "Racontez-moi ce que vous avez en tête. Le premier échange est gratuit, et je vous dis franchement si je suis la bonne personne pour le faire.",
    fond="fond-creme")

page("realisations.html",
     "Réalisations — Grafycom Perpignan",
     "Une sélection de réalisations Grafycom : logos, cartes de restaurant, enseignes et supports imprimés dans les Pyrénées-Orientales.",
     BODY,
     ogtitle="Les réalisations Grafycom",
     robots="noindex, follow")
