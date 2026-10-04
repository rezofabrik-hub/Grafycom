# -*- coding: utf-8 -*-
from gen import page, appel

BLOC = """<section class="{fond}" id="{ancre}">
  <div class="conteneur grille g2" style="align-items:start; gap:clamp(30px,5vw,60px)">
    <div>
      <div class="picto {picto}"><i class="fa-solid {icone}" aria-hidden="true"></i></div>
      <h2>{titre}</h2>
      <div class="trait"></div>
      <p>{intro}</p>
      <p style="margin-top:14px">{suite}</p>
{visuel}
    </div>
    <div class="carte" style="background:#fff">
      <h3 style="margin-bottom:16px">{soustitre}</h3>
      <ul class="liste-check" style="margin-top:0">{items}</ul>
    </div>
  </div>
</section>

"""

# Quatre rubriques montrent désormais de vraies réalisations de Grafycom,
# tirées du portfolio de Sandra. Les deux dernières gardent une photo
# d'illustration libre de droits, créditée dans les mentions légales.
#
# Le troisième champ dit laquelle est laquelle : le commentaire posé dans
# le HTML en dépend, et c'est une distinction qui compte — présenter une
# photo d'illustration comme un travail de Grafycom serait faux, et
# l'inverse priverait Sandra du crédit de son travail.
#
# Pour ajouter une photo là où il n'y en a pas : déposer le fichier dans
# assets/img/prestations/, remplacer None par son nom, écrire le texte
# alternatif, régénérer.
PHOTOS = {
 "identite":     ("presta-identite.webp", "grafycom",
                  "Logo Crazy Frenchy, lettrage doré et tour Eiffel, appliqué en grand sur le mur d'un hall d'entreprise"),
 "menus":        ("presta-menus.webp", "grafycom",
                  "Menu de la pizzeria Pizza Fry ouvert à plat, carte des pizzas et carte des boissons sur fond ardoise"),
 "print":        ("presta-print.webp", "grafycom",
                  "Dépliant trois volets de Cap Loisirs, déplié, fond violet et plan d'accès"),
 "signaletique": ("presta-signaletique.webp", "grafycom",
                  "Enseigne lumineuse du restaurant Le Cayrou, allumée sur une façade à la tombée du jour"),
 "digital":      ("presta-digital.jpg", "illustration",
                  "Main tenant un téléphone qui photographie un ciel au coucher du soleil"),
 "projet":       ("presta-projet.jpg", "illustration",
                  "Bureau vu de dessus : clavier, carnet, appareil photo, téléphone et tasse de café"),
}

REALISATION = """      <!-- Réalisation de Grafycom, tirée du portfolio de Sandra. -->
      <figure class="presta-photo"><img src="assets/img/prestations/%s" alt="%s" loading="lazy"></figure>"""

ILLUSTRATION = """      <!-- Photographie d'illustration (Wikimedia Commons, créditée dans les
           mentions légales). Ce n'est pas une réalisation de Grafycom. -->
      <figure class="presta-photo"><img src="assets/img/prestations/%s" alt="%s" loading="lazy"></figure>"""

ATTENTE = """      <!-- Emplacement en attente de la photo de Grafycom. -->
      <div class="presta-attente" role="img" aria-label="Emplacement réservé : %s">
        <i class="fa-solid fa-camera" aria-hidden="true"></i>
        <strong>Photo à venir</strong>
        <span>%s</span>
      </div>"""

def bloc(ancre, picto, icone, titre, intro, suite, soustitre, items, fond=""):
    fichier, origine, texte = PHOTOS[ancre]
    if not fichier:
        visuel = ATTENTE % (texte, texte)
    else:
        gabarit = REALISATION if origine == "grafycom" else ILLUSTRATION
        visuel = gabarit % (fichier, texte)
    return BLOC.format(ancre=ancre, picto=picto, icone=icone, titre=titre, intro=intro,
                       suite=suite, soustitre=soustitre, fond=fond, visuel=visuel,
                       items="".join("<li>%s</li>" % i for i in items))

BODY = """
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">Prestations</span>
    <h1>Tout ce qui porte votre nom,<br><span class="texte-degrade">conçu au même endroit</span></h1>
    <div class="trait"></div>
    <p class="chapeau">Du logo à l'enseigne, du menu au visuel Instagram&nbsp;: des solutions 360° pensées ensemble, pour que chaque support renforce le précédent au lieu de le contredire.</p>
    <div class="groupe-btn" style="margin-top:30px">
      <a href="contact.html" class="btn btn-couleur">Demander un devis <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
    </div>
  </div>
</section>

"""

BODY += bloc(
    "identite", "p-bleu", "fa-feather-pointed",
    "Identité visuelle &amp; création de logo",
    "Un logo n'est pas un dessin joli&nbsp;: c'est un outil qui doit fonctionner sur une carte de visite de 8&nbsp;cm comme sur un panneau de 3&nbsp;mètres, en couleur comme en noir et blanc, brodé sur un polo comme affiché sur un écran.",
    "Je pars de votre activité, de vos clients et de ce qui vous distingue réellement de la concurrence. Vous repartez avec un logo, ses déclinaisons et une charte graphique qui dit comment l'utiliser — pour que votre image reste la même dans dix ans, quel que soit le prestataire.",
    "Ce que comprend la prestation",
    ["Atelier de cadrage : activité, clientèle, positionnement, concurrence",
     "Pistes créatives argumentées, présentées en situation",
     "Déclinaisons : couleur, monochrome, fond sombre, format carré réseaux",
     "Palette de couleurs, avec ses déclinaisons",
     "Typographies de titre et de texte, et leurs règles d'emploi",
     "Charte graphique PDF, remise avec les fichiers sources vectoriels"],
    fond="")

BODY += bloc(
    "menus", "p-turq", "fa-utensils",
    "Menus, cartes &amp; supports de table",
    "Une carte de restaurant est un outil de vente avant d'être un document. La hiérarchie, la place des prix, le choix des plats mis en avant : tout cela se décide, et cela se voit sur le ticket moyen.",
    "Je conçois des cartes lisibles en terrasse comme en salle tamisée, déclinables à la saison, et faciles à remettre à jour quand un plat change. Format papier, plastifié, ardoise, set de table ou QR code&nbsp;: on choisit ensemble ce qui tient à l'usage.",
    "Exemples de supports",
    ["Carte principale et carte des boissons",
     "Menu du jour et ardoise, remise à jour facile",
     "Sets de table, chevalets, porte-menus de devanture",
     "Carte numérique accessible par QR code",
     "Déclinaisons saisonnières et cartes événementielles",
     "Version bilingue français / espagnol ou anglais"],
    fond="fond-creme")

BODY += bloc(
    "print", "p-violet", "fa-print",
    "Supports imprimés",
    "Un fichier mal préparé, c'est un tirage raté et une facture pour rien. Fonds perdus, repères de coupe, résolution, profils colorimétriques, polices vectorisées&nbsp;: la partie technique fait partie du travail.",
    "Je livre des fichiers directement exploitables par votre imprimeur, ou je gère l'impression avec des partenaires de la région et je vérifie les bons à tirer avant lancement.",
    "Supports courants",
    ["Cartes de visite, cartes de fidélité, chèques cadeaux",
     "Flyers, dépliants, brochures, catalogues",
     "Affiches et programmes d'événement",
     "Packaging, étiquettes, stickers",
     "Kakémonos, roll-ups, stands de salon"],
    fond="")

BODY += bloc(
    "signaletique", "p-rose", "fa-store",
    "Signalétique, enseignes &amp; véhicules",
    "Votre devanture travaille pour vous vingt-quatre heures sur vingt-quatre. C'est souvent le premier support à reprendre, et le plus rentable.",
    "Conception adaptée au grand format, en lien direct avec le poseur&nbsp;: dimensions relevées, contraintes de support prises en compte, fichiers fournis à ses normes. Pour les enseignes en centre-ville, je vous signale les démarches d'autorisation à prévoir auprès de la mairie.",
    "Interventions",
    ["Enseignes de façade et enseignes drapeau",
     "Vitrophanie : adhésifs, dépolis, lettrages de vitrine",
     "Panneaux de chantier et de signalisation",
     "Marquage de véhicule : voiture, camionnette, flotte",
     "Habillage de stand et de terrasse",
     "Relevé de cotes et coordination avec le poseur"],
    fond="fond-creme")

BODY += bloc(
    "digital", "p-corail", "fa-mobile-screen",
    "Réseaux sociaux &amp; supports numériques",
    "Publier régulièrement est déjà difficile&nbsp;; publier régulièrement <em>et</em> avec une image cohérente l'est encore plus. La solution n'est pas de tout me déléguer&nbsp;: c'est d'avoir de bons gabarits.",
    "Je crée des modèles à votre image, que vous remplissez vous-même semaine après semaine — dans un outil que vous savez utiliser. Votre fil reste reconnaissable sans que vous ayez à repartir d'une page blanche à chaque publication.",
    "Livrables",
    ["Photos de profil et bannières, tous réseaux",
     "Gabarits de publication et de story, réutilisables",
     "Carrousels et visuels de campagne",
     "Signature de courriel et fond de visioconférence",
     "Visuels pour site web, bandeaux et vignettes"],
    fond="")

BODY += bloc(
    "projet", "p-orange", "fa-diagram-project",
    "Gestion de projet &amp; direction artistique",
    "Chef de projet autant qu'infographiste&nbsp;: sur les opérations qui font intervenir plusieurs corps de métier, quelqu'un doit tenir le fil. Sinon l'imprimeur attend le poseur, qui attend le fichier, qui attend une validation.",
    "Je peux prendre ce rôle&nbsp;: planning, coordination des prestataires, vérification des bons à tirer, contrôle de conformité à la livraison. Vous avez un seul interlocuteur et une seule facture à suivre.",
    "Ce que cela couvre",
    ["Rétroplanning et suivi des échéances",
     "Consultation et coordination des imprimeurs et poseurs",
     "Vérification des bons à tirer avant lancement",
     "Contrôle de conformité à la réception",
     "Direction artistique d'une campagne ou d'une saison",
     "Refonte progressive d'une communication existante"],
    fond="fond-creme")

BODY += """<section>
  <div class="conteneur centre">
    <span class="eyebrow">Budget</span>
    <h2>Combien ça coûte&nbsp;?</h2>
    <div class="trait"></div>
    <p class="chapeau">Aucun tarif affiché ici, et c'est volontaire&nbsp;: un logo pour une association de quartier et une identité complète pour un restaurant de bord de mer n'ont ni le même périmètre, ni le même prix. Annoncer «&nbsp;logo à partir de 290&nbsp;€&nbsp;» reviendrait à vous vendre quelque chose avant de savoir ce dont vous avez besoin.</p>
    <p class="chapeau" style="margin-top:16px">Ce que je peux promettre&nbsp;: un devis détaillé ligne par ligne après notre premier échange, un périmètre écrit noir sur blanc, un nombre d'allers-retours fixé à l'avance, et aucun surcoût qui apparaît en cours de route.</p>
    <div class="groupe-btn" style="margin-top:32px">
      <a href="contact.html" class="btn btn-couleur">Obtenir un devis gratuit <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
      <a href="methode.html" class="btn btn-secondaire">Voir comment se déroule un projet</a>
    </div>
  </div>
</section>

<section class="fond-sable">
  <div class="conteneur centre">
    <span class="eyebrow">Je ne travaille pas seule</span>
    <h2>Et pour le reste, des partenaires</h2>
    <div class="trait"></div>
    <p class="chapeau">Concevoir est mon métier&nbsp;; imprimer, poser une enseigne, photographier un plat ou développer un site n'en sont pas. Je m'appuie sur des imprimeurs, des enseignistes et poseurs, des photographes et des développeurs de la région — vous n'avez qu'un interlocuteur, mais vous bénéficiez de plusieurs métiers. Et si vous avez déjà vos prestataires, les fichiers sont préparés pour qu'ils puissent travailler avec.</p>
  </div>
  <div class="conteneur centre" style="margin-top:34px">
    <a href="a-propos.html" class="btn btn-secondaire">Comment je travaille <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
  </div>
</section>

""" + appel(
    "Pas sûr de ce dont vous avez besoin&nbsp;?",
    "C'est le cas de la plupart des personnes qui me contactent. Décrivez-moi simplement votre activité et ce qui vous gêne dans votre image actuelle&nbsp;: je vous dirai par quoi commencer, même si ce n'est pas par moi.",
    fond="fond-creme")

page("prestations.html",
     "Création de logo et supports — Grafycom Perpignan",
     "Logo et identité visuelle, menus, supports imprimés, signalétique et réseaux sociaux. Grafycom, infographiste à Perpignan.",
     BODY,
     ogtitle="Les prestations Grafycom — Perpignan")
