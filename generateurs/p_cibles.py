# -*- coding: utf-8 -*-
"""Pages de référencement par situation, et non par commune.

Le site compte déjà douze pages de communes. En empiler d'autres ferait
basculer l'ensemble du côté des « pages satellites » que Google déclasse.
Ce qui manquait, c'est de la profondeur par intention de recherche : les
requêtes qui convertissent ne sont pas « graphiste + ville », ce sont
« j'ouvre un commerce, que dois-je prévoir » et « mon enseigne a quinze
ans ». Deux situations, plus deux pages sectorielles adossées à de vraies
références du portfolio.
"""
import json
from gen import page, appel, demarches, TEL, TEL_URI, SITE


def carte(picto, icone, titre, texte):
    return ('<article class="carte"><div class="picto %s">'
            '<i class="fa-solid %s" aria-hidden="true"></i></div>'
            '<h3>%s</h3><p>%s</p></article>' % (picto, icone, titre, texte))


def faq_html(paires):
    out = ['<div class="faq" style="margin-top:40px">']
    for n, (q, r) in enumerate(paires):
        out.append('<details%s><summary>%s</summary><p>%s</p></details>'
                   % (" open" if n == 0 else "", q, r))
    out.append('</div>')
    return "\n".join(out)


def faq_jsonld(paires, titre, slug, desc):
    sansnbsp = lambda t: t.replace("&nbsp;", " ").replace("&amp;", "&")
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": sansnbsp(q),
                 "acceptedAnswer": {"@type": "Answer", "text": sansnbsp(r)}}
                for q, r in paires]},
            {"@type": "WebPage", "name": sansnbsp(titre),
             "url": "%s/%s" % (SITE, slug), "description": sansnbsp(desc),
             "about": {"@type": "ProfessionalService", "name": "Grafycom",
                       "areaServed": {"@type": "AdministrativeArea",
                                      "name": "Pyrénées-Orientales"}}},
        ],
    }, ensure_ascii=False, indent=1)


GABARIT = """
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1a}<br><span class="texte-degrade">{h1b}</span></h1>
    <div class="trait"></div>
    <p class="chapeau">{chapeau}</p>
    <div class="groupe-btn" style="margin-top:30px">
      <a href="contact.html" class="btn btn-couleur">Parlons de votre projet <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
      <a href="tel:{tel_uri}" class="btn btn-secondaire"><i class="fa-solid fa-phone" aria-hidden="true"></i> {tel}</a>
    </div>
  </div>
</section>

<section>
  <div class="conteneur prose">
{corps1}
  </div>
</section>

<section class="fond-creme">
  <div class="conteneur centre">
    <span class="eyebrow">{eyebrow2}</span>
    <h2>{titre2}</h2>
    <div class="trait"></div>
  </div>
  <div class="conteneur grille g3" style="margin-top:44px">
    {cartes}
  </div>
</section>

<section>
  <div class="conteneur prose">
{corps2}
  </div>
</section>

<section class="fond-sable">
  <div class="conteneur centre">
    <span class="eyebrow">Questions fréquentes</span>
    <h2>{titre_faq}</h2>
    <div class="trait"></div>
  </div>
  <div class="conteneur">
{faq}
  </div>
</section>

"""


def cible(slug, title, desc, eyebrow, h1a, h1b, chapeau, corps1,
          eyebrow2, titre2, cartes, corps2, titre_faq, faq, appel_titre,
          appel_texte):
    corps = GABARIT.format(
        eyebrow=eyebrow, h1a=h1a, h1b=h1b, chapeau=chapeau, corps1=corps1,
        eyebrow2=eyebrow2, titre2=titre2, cartes="\n    ".join(cartes),
        corps2=corps2, titre_faq=titre_faq, faq=faq_html(faq),
        tel=TEL, tel_uri=TEL_URI)
    corps += appel(appel_titre, appel_texte, fond="")
    page(slug, title, desc, corps, ogtitle=title.split(" —")[0],
         jsonld=faq_jsonld(faq, title, slug, desc))


# ─────────────────────────── 1. Les ouvertures ───────────────────────────

cible(
 "ouverture-commerce-66.html",
 "Ouvrir un commerce dans le 66 : les supports à prévoir",
 "Vous ouvrez dans les Pyrénées-Orientales ? L'ordre dans lequel préparer logo, enseigne, vitrine et cartes, et les délais à anticiper avant le jour J.",
 "Vous ouvrez bientôt",
 "Ouvrir un commerce",
 "dans les Pyrénées-Orientales",
 "Entre la signature du bail et le jour J, il y a une liste de supports à préparer — et un ordre qui évite de payer deux fois. Le voici, avec les délais réels.",
 """    <h2 style="margin-top:0">Par quoi commencer, et dans quel ordre</h2>
    <p>L'erreur la plus fréquente n'est pas d'oublier un support. C'est de les traiter dans le désordre, et de découvrir trois semaines avant l'ouverture que l'enseigne ne sera pas posée à temps — ou qu'il faut refaire le logo parce qu'il ne tient pas en lettres découpées.</p>
    <ol>
      <li><strong>Le logo.</strong> Tout le reste en découle : l'enseigne, la vitrine, la carte, le sachet. Comptez deux à trois semaines, allers-retours compris.</li>
      <li><strong>L'enseigne.</strong> C'est la plus longue, et la seule qui dépende d'un fabricant, d'un poseur et parfois d'une mairie. Six semaines n'ont rien d'exceptionnel.</li>
      <li><strong>La vitrine.</strong> Adhésifs, horaires, ce qu'on lit depuis le trottoir. Rapide à produire, mais à concevoir en même temps que l'enseigne pour que les deux se répondent.</li>
      <li><strong>Le quotidien.</strong> Carte de visite, carte ou menu, étiquettes, sacs. Une à deux semaines selon l'imprimeur.</li>
      <li><strong>Le numérique.</strong> Fiche Google, réseaux, site. Après le reste — parce qu'il faut les photos de votre local fini.</li>
    </ol>
    <div class="encart">
      <strong>La règle à retenir&nbsp;:</strong> commencez par ce qui a le plus long délai et le moins de marge de rattrapage. Une carte de visite se réimprime en trois jours ; une enseigne mal dimensionnée se refabrique en six semaines et se repaie intégralement.
    </div>""",
 "Les trois délais qui surprennent",
 "Ce qui prend plus de temps qu'on ne croit",
 [carte("p-corail", "fa-sign-hanging", "La fabrication de l'enseigne",
        "Entre la validation du fichier et la pose, comptez quatre à six semaines. Les lettres découpées et les caissons lumineux sont fabriqués à la commande."),
  carte("p-orange", "fa-stamp", "L'autorisation d'urbanisme",
        "Une autorisation préalable d'enseigne en mairie se compte en semaines, pas en jours. Dans les secteurs protégés, l'avis de l'architecte des Bâtiments de France s'y ajoute."),
  carte("p-bleu", "fa-print", "Le bon à tirer",
        "L'impression elle-même est rapide. Ce qui prend du temps, c'est la relecture, la correction et la validation — et c'est précisément là qu'il ne faut pas se presser.")],
 """    <h2 style="margin-top:0">L'autorisation d'enseigne, le point que tout le monde découvre trop tard</h2>
    <p>Poser une enseigne n'est pas libre. Dans bien des cas, il faut déposer une <strong>demande d'autorisation préalable</strong> (formulaire Cerfa n°&nbsp;16308*01) en mairie, avec un plan coté et une insertion sur photo de la façade. Les communes dotées d'un règlement local de publicité y ajoutent leurs propres règles : surface maximale, nombre d'enseignes par façade, matériaux, éclairage et horaires d'extinction.</p>
    """ + demarches() + """
    <p>À Perpignan, une bonne partie du centre est en secteur patrimonial protégé : l'avis de l'architecte des Bâtiments de France s'ajoute au dossier, et il porte sur les couleurs, les matières et le mode d'éclairage. Sur la côte, plusieurs communes encadrent l'affichage saisonnier. Ce sont des règles locales : <strong>vérifiez auprès de votre mairie avant de faire fabriquer quoi que ce soit.</strong></p>
    <p>Concrètement, cela change l'ordre des choses : le dossier se prépare pendant la conception, pas après. Un visuel conçu sans connaître la surface autorisée est un visuel à refaire.</p>

    <h2>Ce que ça donne, en vrai</h2>
    <p>Pour <strong>Ô Fait Maison</strong>, coffee shop et salon de thé, l'enseigne de devanture et la décoration intérieure ont été pensées ensemble : les mêmes formes végétales se retrouvent sur la façade et sur le mur du fond, et le client qui pousse la porte reconnaît ce qu'il a vu de la rue.</p>
    <p>Pour <strong>Casa Aldo</strong>, restaurant italien, le logo a été dessiné d'emblée pour tenir en enseigne ronde — un format qui pardonne peu les détails fins. Savoir dès le crayonné sur quoi le logo finira évite de le refaire au moment de la fabrication.</p>
    <p>Les deux sont visibles sur la page <a href="realisations.html">réalisations</a>. Le détail de chaque prestation est sur la page <a href="prestations.html">prestations</a>, et si vous ouvrez hors de Perpignan, la <a href="zone-intervention.html">zone d'intervention</a> couvre tout le département.</p>""",
 "Ouvrir sans mauvaise surprise",
 [("Combien de temps avant l'ouverture faut-il s'y prendre&nbsp;?",
   "Trois mois est confortable, deux mois est tenable, un mois oblige à faire des choix. Le facteur limitant est presque toujours l'enseigne : fabrication et pose, plus l'autorisation quand elle est nécessaire."),
  ("Faut-il vraiment une autorisation pour une enseigne&nbsp;?",
   "Dans bien des cas, oui : une autorisation préalable en mairie, à demander avec le formulaire Cerfa n°&nbsp;16308*01. Attention au vocabulaire : on « déclare » une publicité, on « autorise » une enseigne, et la procédure n'est pas la même. Les règles varient d'une commune à l'autre et se durcissent en secteur protégé. C'est à vérifier auprès de votre mairie, et à anticiper dès la conception."),
  ("Peut-on étaler la dépense&nbsp;?",
   "Oui, et c'est souvent la bonne approche. Le logo et l'enseigne d'abord, parce qu'ils conditionnent tout le reste et qu'ils sont les plus visibles. Les supports du quotidien peuvent suivre un mois plus tard, une fois les premières semaines passées."),
  ("Je n'ai pas encore de nom définitif. On peut commencer&nbsp;?",
   "Pas le logo, non — il dépend du nom, de sa longueur, de sa sonorité. En revanche, le premier échange sert justement à ça : poser les questions qui aident à trancher. Et il est gratuit."),
  ("Je reprends un commerce existant. Est-ce la même chose&nbsp;?",
   "Non, c'est plus délicat : il y a une clientèle en place à ne pas perdre. On regarde ce qui mérite d'être gardé avant de décider ce qui change. Le sujet est traité sur la page consacrée à la refonte d'image.")],
 "Vous ouvrez dans le département&nbsp;?",
 "Le premier échange est gratuit et sert surtout à savoir par quoi commencer — même si la réponse est «&nbsp;pas par moi&nbsp;». Trente minutes suffisent à dégrossir un calendrier.")


# ──────────────── 2. Les entreprises installées depuis longtemps ────────────────

cible(
 "refaire-son-image.html",
 "Refaire l'image d'une entreprise qui a dix ans",
 "Votre logo, votre enseigne et vos cartes datent ? Les signes qu'une identité a vieilli, et comment la reprendre sans tout jeter ni perdre vos clients.",
 "Vous existez depuis des années",
 "Votre image a vieilli",
 "sans que vous l'ayez vue vieillir",
 "Une entreprise qui tourne depuis dix ans a une réputation. Le problème n'est presque jamais la qualité du travail — c'est que l'image ne la raconte plus.",
 """    <h2 style="margin-top:0">Les signes qui ne trompent pas</h2>
    <p>Personne ne se réveille un matin en trouvant son logo démodé. Ça se voit de l'extérieur, et par petits indices :</p>
    <ul class="liste-check">
      <li>Vous n'avez pas de version vectorielle de votre logo — seulement un JPEG retrouvé dans un vieux mail, qui pixellise dès qu'on l'agrandit.</li>
      <li>Votre enseigne a pris le soleil : les rouges ont viré au rose, et l'adhésif se décolle aux angles.</li>
      <li>Vos trois derniers supports ont trois typographies différentes, parce que chacun a été fait par quelqu'un d'autre.</li>
      <li>Votre carte ou votre tarif a été rafistolé sous Word, puis photocopié, puis re-rafistolé.</li>
      <li>On vous confond avec le concurrent d'en face, et vous ne savez pas bien dire pourquoi.</li>
      <li>Vous évitez de donner votre carte de visite.</li>
    </ul>
    <p>Ce dernier point est le plus parlant. Quand on n'ose plus montrer ses propres supports, c'est qu'ils ne disent plus ce qu'on est devenu.</p>
    <div class="encart">
      <strong>Ce qui change, après dix ans&nbsp;:</strong> vous n'avez plus à vous faire connaître, vous avez à vous faire reconnaître. Ce n'est pas le même travail. Une entreprise jeune construit une image ; une entreprise installée en a déjà une, répartie dans la tête de ses clients. Il s'agit de la remettre au net, pas de la remplacer.
    </div>""",
 "Trois situations courantes",
 "Où en êtes-vous&nbsp;?",
 [carte("p-turq", "fa-rotate", "Le logo tient, le reste a dérivé",
        "Le plus fréquent, et le moins coûteux. On garde le logo, on le remet au propre en vectoriel, et on réaligne tous les supports dessus."),
  carte("p-violet", "fa-pen-nib", "Le logo ne tient plus",
        "Il ne fonctionne ni en petit, ni en une couleur, ni sur un écran. On le redessine en gardant ce que vos clients reconnaissent — souvent une couleur, une forme, un détail."),
  carte("p-corail", "fa-store", "L'activité a changé, pas l'image",
        "Vous faisiez un métier, vous en faites trois. L'image parle encore du premier. C'est le cas où la refonte rapporte le plus vite.")],
 """    <h2 style="margin-top:0">On ne jette pas tout</h2>
    <p>Une refonte brutale fait perdre ce qui avait été gagné. Vos clients vous reconnaissent à quelque chose — une couleur, une forme, le nom écrit d'une certaine façon. Le travail consiste à identifier ce quelque chose, le garder, et nettoyer tout le reste autour.</p>
    <p>En pratique, on procède dans cet ordre :</p>
    <ol>
      <li><strong>L'inventaire.</strong> On étale tout ce qui porte votre nom : enseigne, véhicule, cartes, devis, factures, page Facebook, sac. C'est souvent le moment où l'on comprend le problème sans avoir besoin d'en parler.</li>
      <li><strong>Le logo.</strong> Retouché ou redessiné, puis livré dans tous les formats dont vous auriez dû disposer depuis le début — vectoriel compris.</li>
      <li><strong>Ce qui se voit le plus.</strong> L'enseigne, la vitrine, le véhicule. C'est là que l'effet est immédiat.</li>
      <li><strong>Le quotidien.</strong> Devis, factures, cartes. Le travail le moins spectaculaire, et celui qui se rentabilise le plus vite — c'est le document que votre client lit au moment où il décide.</li>
    </ol>

    <h2>Un exemple</h2>
    <p><strong>Alliance Peintures</strong>, peintres en bâtiment, est exactement ce cas : une entreprise installée, une activité qui tourne, et une image qui ne suivait plus. La refonte a repris l'identité complète — logo, enseignes, cartes de visite, marquage des véhicules, flyers — en gardant la lisibilité d'un métier où l'on est jugé sur le sérieux avant le style. Le véhicule est visible sur la page <a href="realisations.html">réalisations</a>.</p>
    <p>Si votre image tient encore mais que vos supports partent dans tous les sens, la page <a href="prestations.html#identite">identité visuelle</a> décrit ce que comprend une remise au net. Et si vous venez d'ouvrir, c'est l'autre page qu'il faut lire : <a href="ouverture-commerce-66.html">ouvrir un commerce dans le 66</a>.</p>""",
 "Reprendre son image sans tout perdre",
 [("Faut-il tout changer en même temps&nbsp;?",
   "Non, et c'est rarement souhaitable. On commence par le logo et par ce qui se voit le plus, puis on remplace le reste au fil des réimpressions. Étaler sur six mois ne gêne personne, à condition que le cap soit fixé dès le départ."),
  ("Mes clients vont-ils ne plus me reconnaître&nbsp;?",
   "C'est la crainte la plus légitime, et c'est précisément pour ça qu'on part de ce qu'ils reconnaissent déjà. Dans la plupart des refontes, un élément fort est conservé — une couleur, une forme, un mot. Le changement se remarque sans surprendre."),
  ("Je n'ai plus les fichiers d'origine de mon logo. C'est grave&nbsp;?",
   "C'est très courant, et ça se règle : on redessine le logo en vectoriel à partir de ce qui existe. Vous repartez avec des fichiers que vous possédez vraiment, utilisables par n'importe quel imprimeur ou poseur."),
  ("Combien de temps ça prend&nbsp;?",
   "Deux à quatre semaines pour l'identité elle-même. Le déploiement sur les supports s'étale ensuite au rythme que vous choisissez — et au rythme de l'enseigniste, s'il y a une enseigne à refaire."),
  ("Et si je ne veux changer qu'une chose&nbsp;?",
   "C'est possible et parfois suffisant. Une carte de restaurant remise au propre, un devis mis à l'identité, une enseigne refaite : ce sont des interventions isolées qui ont du sens. Le premier échange sert à dire lesquelles valent le coup chez vous.")],
 "Votre image mérite un regard neuf&nbsp;?",
 "Le premier échange est gratuit. Montrez-moi ce que vous avez aujourd'hui — même en photo, même en désordre — et je vous dirai franchement ce qui mérite d'être repris, et ce qui peut rester tel quel.")


# ─────────────────────── 3. Restaurants, bars, salons de thé ───────────────────────

cible(
 "graphiste-restaurant-perpignan.html",
 "Graphiste pour restaurant à Perpignan — cartes, enseignes",
 "Cartes et menus, enseignes, vitrophanie pour les restaurants et bars des Pyrénées-Orientales. Mise en page lisible, version espagnole si besoin.",
 "Restaurants, bars, salons de thé",
 "Graphiste pour restaurant",
 "à Perpignan et dans le 66",
 "La carte est le moment où votre client décide combien il va dépenser. L'enseigne, le moment où il décide d'entrer. Ce sont les deux supports qui rapportent le plus.",
 """    <h2 style="margin-top:0">Une carte n'est pas une liste de plats</h2>
    <p>On mange très bien dans beaucoup d'endroits dont la carte est tapée au traitement de texte, centrée, les prix alignés à droite par des points de suite. C'est pourtant la première chose que voit quelqu'un qui n'est jamais entré.</p>
    <p>Trois principes changent tout, et aucun ne coûte un centime de plus à l'impression :</p>
    <ul class="liste-check">
      <li><strong>La hiérarchie.</strong> Le nom du plat se lit avant son prix, pas l'inverse. Un prix mis en avant devient un argument contre vous.</li>
      <li><strong>L'ordre.</strong> Le premier plat d'une section est celui qu'on lit vraiment ; les suivants sont parcourus. Ce qu'on place en tête n'est donc pas neutre.</li>
      <li><strong>L'espace.</strong> Une carte serrée se lit mal et presse le client. Une carte aérée donne envie de prendre son temps — et une entrée.</li>
    </ul>
    <p>S'y ajoute une question très concrète : la carte va-t-elle vivre sur une table, dehors, entre des mains grasses, pendant six mois&nbsp;? Le papier, le pelliculage et le format se décident à ce moment-là, pas après.</p>

    <h2>Le bilingue, ici, n'est pas un supplément d'âme</h2>
    <p>Dans les Pyrénées-Orientales, une partie de la clientèle arrive de Catalogne, surtout l'été. Une carte uniquement en français laisse une table hésiter sur le pas de la porte. Mais une carte bilingue mal composée devient illisible pour tout le monde : deux fois plus de texte dans le même espace, et plus personne ne trouve les plats.</p>
    <p>Ce qui fonctionne : une langue dominante, la seconde en retrait — plus petite, dans une teinte plus douce. On lit la sienne et on ignore l'autre sans effort. Je travaille en français et en espagnol, ce qui évite les traductions faites au jugé : une carte passée au traducteur automatique se repère en trois secondes par un client espagnol.</p>""",
 "Trois supports, trois rôles",
 "Ce qui compte vraiment en salle",
 [carte("p-corail", "fa-utensils", "La carte et le menu",
        "Carte principale, menu du jour, ardoise, set de table. Mise en page lisible, hiérarchie des prix, déclinaison saisonnière sans refaire le travail."),
  carte("p-bleu", "fa-sign-hanging", "L'enseigne et la vitrine",
        "Caisson lumineux, lettres découpées, bandeau, vitrophanie. Conçus pour être lus à vingt mètres, en passant, et calibrés pour le poseur."),
  carte("p-violet", "fa-mobile-screen", "Les réseaux et la fiche Google",
        "Gabarits de publication réutilisables, photos de plats bien cadrées, visuels de campagne. Le relais naturel de ce qui se passe en salle.")],
 """    <h2 style="margin-top:0">Des restaurants, pour de vrai</h2>
    <p><strong>Casa Aldo</strong>, restaurant italien : création du logo. Il a été dessiné dès le départ pour tenir dans un cercle lumineux, format qui pardonne peu les détails fins. La fabrication de l\'enseigne a été confiée à un partenaire.</p>
    <p><strong>Pizza Fry</strong>, pizzeria : le menu complet, carte des pizzas et carte des boissons, plus les dépliants et l'enseigne. Une mise en page qui tient debout sur une table, avec les formats et les prix lisibles d'un coup d'œil.</p>
    <p><strong>Le Cayrou</strong>, restaurant : logo et enseigne lumineuse de façade. Un trait simple, qui reste lisible de nuit comme de jour.</p>
    <p><strong>Ô Fait Maison</strong>, coffee shop et salon de thé : enseigne de devanture, décoration intérieure, flyers et cartes de visite. L'extérieur et l'intérieur se répondent, de sorte que le client qui pousse la porte reconnaît ce qu'il a vu de la rue.</p>
    <p>Ces quatre projets sont visibles sur la page <a href="realisations.html">réalisations</a>. Si vous ouvrez tout juste, lisez plutôt <a href="ouverture-commerce-66.html">ouvrir un commerce dans le 66</a> ; si votre carte a dix ans, c'est <a href="refaire-son-image.html">refaire son image</a>.</p>""",
 "Ce que les restaurateurs demandent le plus",
 [("Combien de temps pour une carte de restaurant&nbsp;?",
   "Comptez une à deux semaines pour la conception et les allers-retours, puis le délai de l'imprimeur. Pour une réédition saisonnière à partir d'un gabarit existant, quelques jours suffisent."),
  ("Peut-on changer les prix soi-même ensuite&nbsp;?",
   "Oui, si on le prévoit. Je peux livrer la carte dans un format que vous modifiez vous-même pour les prix et les plats du jour, en gardant la mise en page verrouillée. C'est à décider au départ, pas après."),
  ("Faut-il une carte bilingue&nbsp;?",
   "Cela dépend de votre emplacement et de votre saison. Sur la côte et au centre de Perpignan, l'été, c'est presque toujours rentable. Dans un quartier d'habitués, beaucoup moins. On en parle avant de décider."),
  ("Vous vous occupez aussi de l'impression&nbsp;?",
   "Si vous le souhaitez. Je travaille avec des imprimeurs de la région, je prépare les fichiers à leurs normes et je vérifie les bons à tirer. Vous pouvez aussi garder votre imprimeur : les fichiers sont prévus pour."),
  ("Et pour l'enseigne, il faut une autorisation&nbsp;?",
   "Le plus souvent oui, une autorisation préalable en mairie, et un avis supplémentaire en secteur protégé — une bonne partie du centre de Perpignan l'est. C'est à vérifier auprès de votre mairie et à anticiper dès la conception.")],
 "Votre carte mérite mieux qu'un traitement de texte",
 "Envoyez-moi une photo de votre carte actuelle et de votre devanture. Je vous dis en trente minutes ce qui se joue dessus, et ce qui mérite d'être repris en premier.")


# ──────────────────────── 4. Enseignes et signalétique ────────────────────────

cible(
 "enseigne-perpignan.html",
 "Enseigne et signalétique à Perpignan et dans le 66",
 "Enseignes lumineuses, lettres découpées, vitrophanie, totems et marquage de véhicule dans les Pyrénées-Orientales. Du fichier à la pose.",
 "Signalétique",
 "Enseignes et signalétique",
 "à Perpignan et dans le 66",
 "Une enseigne se lit à vingt mètres, en passant, en trois secondes. Tout le reste en découle : la taille, la matière, l'éclairage — et le fichier qu'on remet au poseur.",
 """    <h2 style="margin-top:0">Ce qui se pose sur une façade</h2>
    <p>Le mot «&nbsp;enseigne&nbsp;» recouvre des objets très différents, qui ne coûtent pas la même chose et ne se conçoivent pas de la même façon :</p>
    <ul class="liste-check">
      <li><strong>Le caisson lumineux</strong> — un bandeau rétroéclairé, lisible de nuit, qui demande un visuel simple et contrasté.</li>
      <li><strong>Les lettres découpées</strong> — en PVC, en dibond ou en alu, posées une à une. Élégantes, impitoyables avec les typographies trop fines.</li>
      <li><strong>Le bandeau imprimé</strong> — la solution la plus directe et la plus économique, à condition que le fichier soit calibré pour le grand format.</li>
      <li><strong>La vitrophanie</strong> — adhésifs de vitrine, horaires, dépoli, habillage saisonnier. Ce qu'on lit depuis le trottoir avant même d'avoir levé les yeux.</li>
      <li><strong>Le totem</strong> — sur un parking, une zone commerciale, une entrée de camping. Lisible de loin et en mouvement.</li>
      <li><strong>Le marquage de véhicule</strong> — l'enseigne la moins chère au kilomètre parcouru, et celle qu'on rate le plus souvent faute de gabarit.</li>
    </ul>
    <div class="encart">
      <strong>Le test, avant de valider quoi que ce soit&nbsp;:</strong> imprimez le visuel en A4, posez-le au bout d'un couloir, reculez de dix mètres. Si vous ne lisez pas le nom en une seconde, l'enseigne ne marchera pas non plus.
    </div>""",
 "Avant de faire fabriquer",
 "Les trois points qui coûtent cher à rattraper",
 [carte("p-orange", "fa-stamp", "L'autorisation",
        "Déclaration préalable en mairie dans la plupart des cas, règlement local de publicité quand il existe, avis de l'architecte des Bâtiments de France en secteur protégé."),
  carte("p-turq", "fa-ruler-combined", "Les cotes réelles",
        "Une façade n'est jamais celle du plan. Un relevé sur place évite le caisson de dix centimètres trop large, qu'on ne découvre que le jour de la pose."),
  carte("p-bleu", "fa-file-code", "Le fichier du poseur",
        "Tracé vectoriel, polices converties, cotes, matière et couleurs indiquées. Un fichier approximatif se paie en allers-retours, puis en délai.")],
 """    <h2 style="margin-top:0">La mairie a son mot à dire, et ce n'est pas une formalité</h2>
    <p>Poser une enseigne suppose, dans bien des cas, une <strong>autorisation préalable</strong> (Cerfa n°&nbsp;16308*01), avec plan coté et insertion sur photo de la façade. Les communes dotées d'un règlement local de publicité y ajoutent leurs règles : surface, nombre d'enseignes, matériaux, éclairage, horaires d'extinction.</p>
    <p>À Perpignan, une grande partie du centre est en secteur patrimonial protégé, et l'avis de l'architecte des Bâtiments de France porte alors sur les couleurs, les matières et le mode d'éclairage. Plusieurs communes du littoral encadrent en plus l'affichage saisonnier. Les règles sont locales et changent : <strong>à vérifier auprès de votre mairie avant de lancer la fabrication</strong>, et à intégrer dès la conception plutôt qu'après.</p>

    """ + demarches() + """

    <h2>Du fichier à la pose</h2>
    <p>Je conçois le visuel et je prépare le fichier aux normes du fabricant. Si vous le souhaitez, je consulte les enseignistes et poseurs avec qui je travaille dans la région, je compare les devis, je vérifie le bon à tirer et je contrôle la conformité à la réception. Vous gardez un seul interlocuteur du premier crayonné à la pose — et si vous avez déjà votre poseur, les fichiers sont prévus pour qu'il travaille avec.</p>

    <h2>Des façades, et ce qui les accompagne</h2>
    <p><strong>Le Cayrou</strong>, restaurant : enseigne lumineuse de façade, un trait simple qui tient de nuit. <strong>Ô Fait Maison</strong> : enseigne de devanture et décoration intérieure conçues ensemble. <strong>Alliance Peintures</strong> : marquage de flotte, du hayon aux portes latérales. Et <strong>Cap Loisirs</strong> : l'affiche tarifaire des prestations, qui relève de la même exigence — être lue de loin, en passant.</p>
    <p>Tous sur la page <a href="realisations.html">réalisations</a>. Pour une ouverture, voir <a href="ouverture-commerce-66.html">ouvrir un commerce dans le 66</a> ; pour une enseigne fatiguée, <a href="refaire-son-image.html">refaire son image</a>.</p>""",
 "Ce qu'on me demande avant de poser",
 [("Combien de temps entre la commande et la pose&nbsp;?",
   "Quatre à six semaines sont courantes pour un caisson ou des lettres découpées, fabrication et pose comprises. Il faut y ajouter le délai d'instruction de l'autorisation préalable quand elle est nécessaire."),
  ("Mon logo actuel peut-il servir d'enseigne&nbsp;?",
   "Pas toujours tel quel. Un logo conçu pour un écran a souvent des détails trop fins, des dégradés ou des contre-formes qui disparaissent en découpe. On adapte — ou on en profite pour le remettre au net."),
  ("Qui s'occupe de l'autorisation&nbsp;?",
   "La demande est au nom de l'exploitant ou du propriétaire, donc vous. Je fournis les pièces graphiques du dossier : plan coté et insertion sur photo. Beaucoup d'enseignistes accompagnent aussi la démarche."),
  ("Faut-il forcément une enseigne lumineuse&nbsp;?",
   "Non, et ce n'est pas toujours autorisé. Tout dépend de vos horaires, de l'exposition de la façade et des règles de la commune. Un bandeau non lumineux bien contrasté peut mieux fonctionner qu'un caisson mal placé."),
  ("Travaillez-vous hors de Perpignan&nbsp;?",
   "Oui, dans tout le département. Un déplacement se justifie quand il faut relever des cotes ou voir la façade en vrai ; le reste se traite très bien à distance. Voir la page zone d'intervention.")],
 "Une façade à habiller&nbsp;?",
 "Envoyez-moi une photo de la devanture, prise d'en face et de loin. C'est tout ce qu'il me faut pour un premier avis — gratuit, et franc, y compris si l'enseigne actuelle peut rester.")
