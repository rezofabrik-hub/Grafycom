# -*- coding: utf-8 -*-
from gen import page, appel

def reaz(cat, titre, desc, fichier):
    return """    <article class="reaz">
      <div class="reaz-vignette"><img src="assets/img/realisations/%s" alt="%s" data-attente="Visuel à venir" loading="lazy"></div>
      <div class="reaz-texte"><span>%s</span><h3>%s</h3><p>%s</p></div>
    </article>
""" % (fichier, titre, cat, titre, desc)

GALERIE = "".join([
    reaz("Identité visuelle", "Casa Aldo",
         "Création du logo d'un restaurant italien. L'enseigne a été réalisée par Alinea.",
         "casa-aldo.webp"),
    reaz("Signalétique", "Ô Fait Maison",
         "Enseigne de devanture d'un salon de thé, et la décoration intérieure qui lui répond.",
         "o-fait-maison.webp"),
    reaz("Véhicule", "Alliance Peintures",
         "Une identité déclinée sur la flotte, du hayon aux portes latérales.",
         "alliance-vehicule.webp"),
    reaz("Édition", "Mia Beauty",
         "Livret de formation : couverture, mise en page et gabarit des pages intérieures.",
         "mia-beauty.webp"),
    reaz("Affichage", "Cap Loisirs",
         "Affiche tarifaire des prestations proposées, lisible de loin à l'entrée.",
         "cap-loisirs.webp"),
    reaz("Réseaux sociaux", "Pano Perpignan",
         "Gabarits de publication et visuels de campagne, déclinables semaine après semaine.",
         "pano-perpignan.webp"),
])
BODY = """
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">Réalisations</span>
    <h1>Quelques projets,<br><span class="texte-degrade">et ce qu'ils demandaient</span></h1>
    <div class="trait"></div>
    <p class="chapeau">Chaque projet part d'une page blanche et d'une conversation. Voici une sélection de travaux et, pour chacun, ce qu'il fallait résoudre.</p>
  </div>
</section>

<section>
  <!-- Réalisations de Grafycom, tirées du portfolio de Sandra. Pour en
       ajouter une : déposer le fichier dans assets/img/realisations/ et
       ajouter un appel à reaz() ci-dessus. -->
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
     robots="index, follow")
