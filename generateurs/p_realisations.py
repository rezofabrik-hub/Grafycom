# -*- coding: utf-8 -*-
from gen import page, appel

def reaz(cat, titre, desc, fichier):
    return """    <article class="reaz">
      <div class="reaz-vignette"><img src="assets/img/realisations/%s" alt="%s" data-attente="Visuel à venir" loading="lazy"></div>
      <div class="reaz-texte"><span>%s</span><h3>%s</h3><p>%s</p></div>
    </article>
""" % (fichier, titre, cat, titre, desc)

# Casa Aldo est retire en attendant son logo source. L'accord porte sur
# le LOGO seul, et casa-aldo.webp montre l'enseigne ronde fabriquee :
# le visuel depassait donc l'accord. Reconstruire le logo depuis cette
# photo ne marche pas — il y mesure 205 px, de biais et compresse ; un
# logo flou dans le portfolio d'une graphiste dessert plus qu'il ne sert.
# Des que le fichier vectoriel arrive, remettre l'entree :
#     reaz("Identite visuelle", "Casa Aldo",
#          "Creation du logo d'un restaurant italien, dessine pour tenir "
#          "dans un cercle lumineux.", "casa-aldo-logo.webp"),
#
# Portfolio de Sandra. Ces projets ont ete menes avant Grafycom, au sein
# d'une precedente structure aujourd'hui fermee : la ligne d'attribution
# sous le chapeau le dit, et elle n'est pas facultative.
#
# Trois projets ont ete retires le 12 octobre faute d'accord confirme, et
# leurs fichiers supprimes — une image seulement dereferencee reste servie
# a son adresse. Avant d'en ajouter une, lire
# assets/img/realisations/LISEZ-MOI.md : l'accord du client y est note
# projet par projet.
#
# Cette note vit ici et non dans un commentaire HTML : build.sh recopie
# le fichier tel quel, et un commentaire nommant des clients retires
# serait lisible dans la source de la page publique.
GALERIE = "".join([
    reaz("Signalétique", "Ô Fait Maison",
         "Enseigne de devanture d'un salon de thé, et la décoration intérieure qui lui répond.",
         "o-fait-maison.webp"),
    reaz("Édition", "Mia Beauty",
         "Livret de formation : couverture, mise en page et gabarit des pages intérieures.",
         "mia-beauty.webp"),
])
BODY = """
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">Réalisations</span>
    <h1>Quelques projets,<br><span class="texte-degrade">et ce qu'ils demandaient</span></h1>
    <div class="trait"></div>
    <p class="chapeau">Chaque projet part d'une page blanche et d'une conversation. Voici une sélection de travaux et, pour chacun, ce qu'il fallait résoudre.</p>
    <p class="chapeau" style="font-size:1rem;opacity:.78;margin-top:14px">Ces projets ont été réalisés par Sandra avant la création de Grafycom, au sein d'une autre structure aujourd'hui fermée, et sont publiés avec l'accord des clients concernés.</p>
  </div>
</section>

<section>
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
