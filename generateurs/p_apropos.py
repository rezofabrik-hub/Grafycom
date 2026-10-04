# -*- coding: utf-8 -*-
from gen import page, appel

JSONLD = """{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Sandra",
  "jobTitle": "Infographiste et chef de projet",
  "worksFor": { "@type": "Organization", "name": "Grafycom", "url": "https://www.grafycom.fr/" },
  "address": { "@type": "PostalAddress", "addressLocality": "Perpignan", "addressCountry": "FR" },
  "knowsLanguage": [ "fr", "es" ]
}"""

BODY = """
<section class="heros">
  <div class="conteneur heros-grille">
    <div>
      <h1>Sandra</h1>
      <div class="trait"></div>
      <p class="chapeau">Infographiste et chef de projet à Perpignan. J'accompagne votre réussite avec Grafycom&nbsp;: plus de sept ans d'expertise à votre service, pour une image qui vous ressemble vraiment.</p>
      <div class="groupe-btn" style="margin-top:30px">
        <a href="contact.html" class="btn btn-couleur">Me contacter <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
        <a href="prestations.html" class="btn btn-secondaire">Voir mes prestations</a>
      </div>
    </div>
    <div class="portrait">
      <img src="assets/img/sandra-grafycom.webp" alt="Sandra, fondatrice de Grafycom, en portrait. Mentions manuscrites autour d'elle&nbsp;: «&nbsp;hello, moi c'est Sandra&nbsp;», «&nbsp;j'accompagne votre réussite avec Grafycom&nbsp;», «&nbsp;solutions 360° : logos, menus, cartes et supports de communication&nbsp;», «&nbsp;+7 ans d'expertise à votre service&nbsp;»" width="900" height="1125">
    </div>
  </div>
</section>

<section>
  <div class="conteneur prose">
    <h2 style="margin-top:0">Pourquoi Grafycom</h2>
    <p>Parce qu'il y a un écart, souvent, entre la qualité de ce que font les gens et l'image qu'ils en donnent. Un artisan irréprochable dont la camionnette porte un lettrage fait à la va-vite. Un restaurant qui cuisine merveilleusement et dont la carte est tapée dans un traitement de texte. Une association pleine d'énergie dont l'affiche se perd sur le mur.</p>
    <p>Ce décalage coûte cher, et il est invisible&nbsp;: ce sont les clients qui ne poussent pas la porte. Mon métier consiste à le refermer.</p>

    <h2>Le colibri</h2>
    <p>Le logo de Grafycom n'a pas été choisi au hasard. Le colibri est le plus petit des oiseaux et l'un des plus précis&nbsp;: il tient en vol immobile, le temps qu'il faut, pour aller chercher exactement ce dont il a besoin. C'est une bonne image de ce travail — un studio à taille humaine, attentif au détail, qui se pose le temps de comprendre avant d'agir.</p>
    <p>Et l'aquarelle qui l'entoure dit le reste&nbsp;: la couleur, le mouvement, et l'idée qu'aucune identité ne ressemble à la précédente.</p>

    <h2>Infographiste <em>et</em> chef de projet</h2>
    <p>La double casquette n'est pas un argument commercial, c'est une nécessité de terrain. Concevoir un beau visuel ne sert à rien s'il arrive trop tard, s'il est mal imprimé, ou si le poseur découvre le jour J que les dimensions ne correspondent pas.</p>
    <p>Sur les projets qui font intervenir plusieurs prestataires, je tiens le fil&nbsp;: planning, consultation des imprimeurs, vérification des bons à tirer, contrôle à la réception. Vous avez un seul interlocuteur, du premier crayonné à la pose.</p>

    <h2>Un réseau de partenaires</h2>
    <p>Je ne travaille pas seule, et je préfère le dire franchement. Un studio à taille humaine qui prétendrait tout faire — concevoir, imprimer, poser, photographier, développer — ferait mal au moins trois de ces métiers. Je fais le mien, et je m'entoure pour le reste.</p>
    <p>Imprimeurs, enseignistes et poseurs, photographes, développeurs&nbsp;: ce sont des partenaires de la région, choisis au fil des projets, dont je connais les habitudes et les délais. C'est précisément ce que la casquette de chef de projet sert à coordonner. Vous n'avez qu'un interlocuteur, mais vous bénéficiez de plusieurs métiers.</p>
    <p>Et si vous avez déjà votre imprimeur ou votre développeur, c'est très bien aussi&nbsp;: les fichiers sont préparés pour être exploitables par n'importe quel professionnel. Vous n'êtes lié à personne.</p>

    <div class="encart">
      <strong>Ce que ça donne concrètement&nbsp;:</strong> vous m'appelez pour un logo, et vous repartez avec un logo qui fonctionne aussi bien brodé sur un polo qu'affiché sur un panneau de trois mètres — parce que la question de la broderie et du grand format a été posée dès le début, pas découverte après coup.
    </div>

    <h2>Bienveillant, et bilingue</h2>
    <p>Bienveillant, ce n'est pas un mot de brochure. Concrètement&nbsp;: personne ne devrait se sentir bête parce qu'il ne connaît pas la différence entre RVB et CMJN. Je n'utilise pas de vocabulaire technique sans l'expliquer, je ne vends pas ce qui n'est pas utile, et je dis quand un besoin ne relève pas de mon métier.</p>
    <p>Bilingue, c'est pratique dans les Pyrénées-Orientales&nbsp;: l'accompagnement et les supports se font en français comme en espagnol, pour les entreprises transfrontalières comme pour celles qui accueillent une clientèle espagnole ou catalane une bonne partie de l'année.</p>

    <h2>Où je travaille</h2>
    <p>Installée à Perpignan, je me déplace dans tout le département&nbsp;: Canet-en-Roussillon, Saint-Cyprien, Argelès-sur-Mer, Collioure, Céret, Thuir, Prades, Le Barcarès, Leucate… Pour les projets plus lointains, la visio et le partage de fichiers fonctionnent très bien — une partie de mes clients ne m'a jamais rencontrée en personne, et cela ne change rien au résultat.</p>
  </div>
</section>

<section class="fond-creme">
  <div class="conteneur centre">
    <span class="eyebrow">En résumé</span>
    <h2>Quatre choses à retenir</h2>
    <div class="trait"></div>
  </div>
  <div class="conteneur grille g4" style="margin-top:44px">
    <article class="carte"><div class="picto p-bleu"><i class="fa-solid fa-award" aria-hidden="true"></i></div><h3>+7 ans d'expertise</h3><p>Une expérience construite sur des projets réels, des contraintes d'impression réelles et des budgets réels.</p></article>
    <article class="carte"><div class="picto p-violet"><i class="fa-solid fa-heart" aria-hidden="true"></i></div><h3>Un accompagnement humain</h3><p>Un seul interlocuteur, du premier échange à la pose. Pas de jargon, pas de mauvaise surprise sur la facture.</p></article>
    <article class="carte"><div class="picto p-corail"><i class="fa-solid fa-palette" aria-hidden="true"></i></div><h3>Du sur-mesure</h3><p>Pas de gabarit acheté sur une banque d'images&nbsp;: chaque création part de votre histoire et de vos clients.</p></article>
    <article class="carte"><div class="picto p-turq"><i class="fa-solid fa-handshake" aria-hidden="true"></i></div><h3>Un réseau de partenaires</h3><p>Imprimeurs, poseurs, photographes, développeurs&nbsp;: les métiers qui ne sont pas le mien sont confiés à des professionnels de la région.</p></article>
  </div>
</section>

""" + appel(
    "On fait connaissance&nbsp;?",
    "Le premier échange est gratuit et sans engagement. Trente minutes suffisent souvent à y voir clair sur ce dont votre image a besoin.",
    fond="")

page("a-propos.html",
     "Sandra, infographiste à Perpignan — Grafycom",
     "Sandra, fondatrice de Grafycom à Perpignan : +7 ans en identité visuelle et gestion de projet, sans jargon, en français et en espagnol.",
     BODY,
     ogtitle="Hello, moi c'est Sandra — Grafycom",
     jsonld=JSONLD)
