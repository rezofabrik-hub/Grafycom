# -*- coding: utf-8 -*-
from gen import page, appel

ETAPE = """  <div class="conteneur grille g2" style="align-items:start;gap:clamp(24px,4vw,56px);margin-bottom:clamp(40px,5vw,64px)">
    <div><span class="num" style="font-family:'Playfair Display',serif;font-size:56px;font-weight:700;line-height:1;background:var(--degrade);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;display:block;margin-bottom:10px">{num}</span>
      <h2>{titre}</h2>
      <p class="mono" style="font-size:13px;letter-spacing:1.4px;color:var(--taupe);text-transform:uppercase">{duree}</p>
    </div>
    <div>
      <p>{texte}</p>
      <ul class="liste-check">{items}</ul>
    </div>
  </div>
"""

def etape(num, titre, duree, texte, items):
    return ETAPE.format(num=num, titre=titre, duree=duree, texte=texte,
                        items="".join("<li>%s</li>" % i for i in items))

BODY = """
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">Méthode</span>
    <h1>Comment se déroule<br><span class="texte-degrade">un projet</span></h1>
    <div class="trait"></div>
    <p class="chapeau">Travailler avec un graphiste, quand on ne l'a jamais fait, ressemble à une boîte noire&nbsp;: on ne sait ni combien de temps ça prend, ni ce qu'on doit fournir, ni à quel moment on peut encore changer d'avis. Voici la boîte, ouverte.</p>
  </div>
</section>

<section>
""" + etape("01", "On se parle", "30 à 60 minutes · gratuit",
    "Un appel, une visio ou un café. Je vous pose des questions sur votre activité, vos clients, vos concurrents et ce qui vous gêne aujourd'hui dans votre image. Vous n'avez rien à préparer&nbsp;: c'est moi qui viens avec les questions.",
    ["Aucun engagement, aucun frais",
     "Vous repartez avec un avis honnête sur ce qui est prioritaire",
     "Si votre besoin ne relève pas de mon métier, je vous le dis"]) + """
</section>

<section class="fond-creme">
""" + etape("02", "Le devis", "sous 2 à 5 jours",
    "Je vous envoie un devis détaillé ligne par ligne&nbsp;: ce qui est créé, en combien d'exemplaires, avec combien d'allers-retours, sous quel délai, et ce qui n'est pas compris. Vous savez exactement ce que vous achetez avant de signer.",
    ["Périmètre écrit, pas de zone grise",
     "Nombre d'allers-retours fixé à l'avance",
     "Acompte à la signature, solde à la livraison",
     "Le devis reste valable un mois : prenez le temps de comparer"]) + """
</section>

<section>
""" + etape("03", "La création", "1 à 3 semaines selon le projet",
    "Je travaille les pistes, puis je vous les présente <em>en situation</em> — sur une devanture, une carte, un écran — plutôt qu'en vignette sur fond blanc. Chaque proposition est argumentée&nbsp;: pourquoi cette forme, pourquoi ces couleurs, ce que ça dit de vous.",
    ["Des pistes distinctes, pas trois variantes de la même idée",
     "Une présentation commentée, en rendez-vous ou en visio",
     "Vos retours attendus par écrit ou de vive voix, comme vous préférez"]) + """
</section>

<section class="fond-creme">
""" + etape("04", "Les ajustements", "quelques jours",
    "On affine ensemble la piste retenue. C'est le moment des «&nbsp;un peu plus foncé&nbsp;», «&nbsp;et si on essayait sans le trait&nbsp;», «&nbsp;mon associée trouve que…&nbsp;». C'est normal et c'est prévu au devis. Un projet avance à la vitesse de vos retours&nbsp;: c'est le seul facteur que je ne maîtrise pas.",
    ["Les allers-retours prévus sont compris dans le prix",
     "Au-delà, je vous préviens avant de facturer quoi que ce soit",
     "Rien n'est validé tant que vous n'avez pas dit oui"]) + """
</section>

<section>
""" + etape("05", "La livraison", "le jour de la validation",
    "Vous recevez un dossier complet&nbsp;: fichiers d'exploitation pour l'impression et le web, fichiers sources vectoriels, et la charte qui explique comment utiliser tout cela. Ces fichiers vous appartiennent&nbsp;: vous pourrez travailler avec n'importe quel prestataire ensuite.",
    ["PDF haute définition prêts pour l'imprimeur",
     "PNG et JPG optimisés pour le web et les réseaux",
     "Fichiers sources vectoriels",
     "Charte graphique PDF : couleurs, typographies, règles d'usage"]) + """
</section>

<section class="fond-creme">
""" + etape("06", "Le suivi", "aussi longtemps que nécessaire",
    "Si vous le souhaitez, je gère l'impression et la pose avec des partenaires de la région, je vérifie les bons à tirer et je contrôle la conformité à la réception. Et six mois plus tard, quand il faudra un flyer de plus, vous n'aurez pas à tout réexpliquer.",
    ["Consultation et coordination des imprimeurs et poseurs",
     "Vérification des bons à tirer avant lancement",
     "Vos fichiers restent archivés chez moi",
     "Tarif préférentiel sur les supports complémentaires"]) + """
</section>

<section>
  <div class="conteneur">
    <div class="centre">
      <span class="eyebrow">Ce que j'attends de vous</span>
      <h2>Un bon projet se fait à deux</h2>
      <div class="trait"></div>
      <p class="chapeau">Rien de compliqué, mais ces trois choses changent tout sur le résultat final.</p>
    </div>
    <div class="grille g3" style="margin-top:44px">
      <article class="carte carte-creme"><div class="picto p-turq"><i class="fa-solid fa-comments" aria-hidden="true"></i></div><h3>De la franchise</h3><p>Si une piste ne vous plaît pas, dites-le simplement. «&nbsp;C'est bien&nbsp;» quand vous pensez «&nbsp;bof&nbsp;» nous fait perdre du temps à tous les deux.</p></article>
      <article class="carte carte-creme"><div class="picto p-violet"><i class="fa-solid fa-user-check" aria-hidden="true"></i></div><h3>Un décideur</h3><p>Idéalement une seule personne tranche. Les retours de cinq personnes qui ne se sont pas parlé produisent un compromis que personne n'aime.</p></article>
      <article class="carte carte-creme"><div class="picto p-corail"><i class="fa-solid fa-clock" aria-hidden="true"></i></div><h3>Des retours réguliers</h3><p>Une semaine de silence sur une validation, c'est une semaine de décalage sur la livraison. Prévenez-moi si vous êtes en coup de feu&nbsp;: on adapte le planning.</p></article>
    </div>
  </div>
</section>

""" + appel(
    "On commence par le premier point&nbsp;?",
    "Un échange de trente minutes, gratuit et sans engagement, suffit pour savoir si nous avons envie de travailler ensemble.",
    fond="fond-creme")

page("methode.html",
     "Comment se déroule un projet — Grafycom",
     "Les six étapes d'un projet chez Grafycom : échange gratuit, devis détaillé, création, ajustements, livraison des fichiers sources.",
     BODY,
     ogtitle="La méthode Grafycom, étape par étape")
