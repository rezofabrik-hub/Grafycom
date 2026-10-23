# -*- coding: utf-8 -*-
from gen import page, appel

# `avant=True` marque un projet mene AVANT Grafycom, au sein d'une
# precedente structure. La mention se pose alors SUR LA FICHE, et non en
# chapeau de page : depuis que la galerie melange des commandes recues
# par Grafycom (Solaire 66, Sweet Dream, Krusty, Big Food, Social Miroir)
# et des travaux anterieurs, une phrase globale en haut de page devient
# fausse pour la moitie des fiches. Le texte est celui qu'autorise
# l'accord, mot pour mot — voir assets/img/realisations/LISEZ-MOI.md.
PROVENANCE = ("\n      <p style=\"margin-top:10px;font-size:12.5px;"
              "color:var(--taupe)\">Création de Sandra, fondatrice de "
              "Grafycom — projet réalisé au sein d'une précédente "
              "structure.</p>")


def reaz(cat, titre, desc, fichier, alt=None, avant=False):
    return """    <article class="reaz">
      <div class="reaz-vignette"><img src="assets/img/realisations/%s" alt="%s" data-attente="Visuel à venir" loading="lazy"></div>
      <div class="reaz-texte"><span>%s</span><h3>%s</h3><p>%s</p>%s</div>
    </article>
""" % (fichier, alt or titre, cat, titre, desc, PROVENANCE if avant else "")

# Casa Aldo est retire definitivement : Laurent n'a plus le logo
# vectoriel, et la seule source restante est la photo de l'enseigne ou il
# mesure 205 px. Ne pas rouvrir le sujet sans un nouveau fichier.
# Historique : L'accord porte sur
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
# Alliance Peintures et Pano Perpignan ont ete retires le 12 octobre,
# Cap Loisirs le 23 — accord jamais confirme dans les trois cas. Leurs
# fichiers sont SUPPRIMES, pas seulement dereferences : une image
# seulement retiree de la page reste servie a son adresse. Avant d'en
# ajouter une, lire assets/img/realisations/LISEZ-MOI.md : l'accord du
# client y est note projet par projet.
#
# Cette note vit ici et non dans un commentaire HTML : build.sh recopie
# le fichier tel quel, et un commentaire nommant des clients retires
# serait lisible dans la source de la page publique.
GALERIE = "".join([
    reaz("Identité", "Solaire 66",
         "Logo, cartes de visite et panneau de chantier. Le même dessin "
         "tient des 8,5 cm de la carte aux 120 cm du panneau — c'est ce "
         "qui se vérifie avant de livrer, pas après.",
         "solaire-66.webp", alt="Panneau de chantier Solaire 66"),
    reaz("Identité &amp; édition", "Sweet Dream",
         "Logo et dépliant de menu pour un salon de desserts. Le relief "
         "des lettres ne vient pas d'un dégradé mais d'une ombre "
         "décalée : deux encres suffisent, et ça passe partout.",
         "sweet-dream.webp", alt="Dépliant de menu Sweet Dream"),
    reaz("Logo &amp; édition", "Krusty",
         "Logo et dépliant de menu. Les lettres sont creuses, blanches "
         "cernées de violet — c'est ce qui les laisse vivre sur un fond "
         "chargé de photos comme sur un fond clair.",
         "krusty.webp", alt="Dépliant de menu Krusty"),
    reaz("Logo", "Big Food",
         "Logo seul, décliné sur une ligne et sur deux. Les deux O du "
         "mot sont des burgers : l'objet remplace la lettre au lieu de "
         "s'ajouter à côté.",
         "big-food.webp", alt="Logo Big Food"),
    reaz("Identité", "Social Miroir",
         "Logo décliné en trois versions : ronde, carrée, en long. La "
         "ronde n'est pas la carrée recadrée — la bande du nom y est "
         "allongée de trois centimètres pour rejoindre le cercle, sinon "
         "l'avatar laisse deux vides sur les côtés.",
         "social-miroir.webp", alt="Logo Social Miroir"),
    reaz("Signalétique", "Ô Fait Maison",
         "Enseigne de devanture d'un salon de thé, et la décoration intérieure qui lui répond.",
         "o-fait-maison.webp", avant=True),
    reaz("Édition", "Mia Beauty",
         "Livret de formation : couverture, mise en page et gabarit des pages intérieures.",
         "mia-beauty.webp", avant=True),
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
  <div class="conteneur galerie">
""" + GALERIE + """  </div>
</section>

<section class="fond-creme">
  <div class="conteneur">
    <div class="centre">
      <span class="eyebrow">Ce que disent mes clients</span>
      <h2>Trois avis, signés</h2>
      <div class="trait" style="margin-left:auto;margin-right:auto"></div>
      <p class="chapeau">De vrais témoignages, laissés par des clientes avec qui le contact est resté. Pas de phrases inventées pour faire joli&nbsp;: s'il n'y en a que trois, c'est qu'il n'y en a que trois.</p>
    </div>
    <div class="grille g3" style="margin-top:34px;text-align:left">
      <article class="carte">
        <p style="font-size:16px;line-height:1.66;font-style:italic;color:var(--brun)">J'ai adoré l'accueil, l'écoute et le professionnalisme. Sandra comprend tout de suite ce que vous voulez. Je la recommande vivement : mon coffee shop a été mis en avant avec sa créativité, et maintenant mes bougies artisanales aussi.</p>
        <p style="margin-top:16px;font-size:15px"><strong>Sarah Otman</strong><br><span style="color:var(--taupe)">Ô Fait Maison</span></p>
      </article>
      <article class="carte">
        <p style="font-size:16px;line-height:1.66;font-style:italic;color:var(--brun)">Sandra et son équipe mettent la notion de «&nbsp;service client&nbsp;» au cœur de leurs prestations : des conseils avisés, des délais tenus, et un travail de qualité à la hauteur de vos attentes. Je vous recommande vivement de leur confier la communication de votre entreprise.</p>
        <p style="margin-top:16px;font-size:15px"><strong>Ludivine Le Blay</strong><br><span style="color:var(--taupe)">La Casquette Bleue</span></p>
      </article>
      <article class="carte">
        <p style="font-size:16px;line-height:1.66;font-style:italic;color:var(--brun)">Je travaille avec Sandra depuis plus de cinq ans. Je suis ravie de leurs prestations : rapidité, efficacité, tarifs abordables. J'ai toujours une mission à leur confier. Je recommande les yeux fermés&nbsp;!</p>
        <p style="margin-top:16px;font-size:15px"><strong>Jade Lopez</strong><br><span style="color:var(--taupe)">Mia Beauty</span></p>
      </article>
    </div>
    <p class="chapeau" style="font-size:.95rem;opacity:.72;margin-top:26px;text-align:center">Ces avis ont été laissés à l'époque de la structure précédente, et sont repris ici avec l'accord de leurs autrices.</p>
    <div class="groupe-btn" style="margin-top:22px;justify-content:center">
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
