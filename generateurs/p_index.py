# -*- coding: utf-8 -*-
from gen import page, appel, ACCUEIL

JSONLD = """{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Grafycom",
  "description": "Infographiste et chef de projet à Perpignan. Identité visuelle 360°, logos, menus, cartes et supports de communication.",
  "url": "https://www.grafycom.fr/",
  "image": "https://www.grafycom.fr/assets/img/logo-grafycom-carre.jpg",
  "slogan": "L'image qui vous ressemble",
  "telephone": "+33782921981",
  "founder": { "@type": "Person", "name": "Sandra", "jobTitle": "Infographiste et chef de projet" },
  "priceRange": "€€",
  "address": { "@type": "PostalAddress", "addressLocality": "Perpignan", "postalCode": "66000", "addressRegion": "Pyrénées-Orientales", "addressCountry": "FR" },
  "areaServed": [ "Perpignan", "Pyrénées-Orientales", "Occitanie", "France" ],
  "knowsLanguage": [ "fr", "es" ],
  "serviceType": [ "Identité visuelle", "Création de logo", "Design graphique", "Menus et cartes", "Supports de communication", "Direction artistique" ]
}"""

BODY = """
<section class="heros">
  <div class="conteneur heros-grille">
    <div>
      <span class="eyebrow">Perpignan · Pyrénées-Orientales</span>
      <h1><span class="l">L'image</span> <span class="l texte-degrade">qui vous ressemble</span></h1>
      <p class="chapeau">Votre image de marque travaille-t-elle vraiment pour vous&nbsp;? Infographiste et chef de projet depuis plus de sept ans, je conçois des solutions 360° et sur mesure&nbsp;: logos, menus, cartes et supports de communication. Une ligne graphique cohérente, du premier crayonné à la pose de l'enseigne.</p>
      <div class="groupe-btn">
        <a href="contact.html" class="btn btn-couleur">Parlons de votre projet <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
        <a href="prestations.html" class="btn btn-secondaire">Voir les prestations</a>
      </div>
      <div class="reperes">
        <div class="repere"><strong>+7 ans</strong><span>d'expertise à votre service</span></div>
        <div class="repere"><strong>360°</strong><span>print, web, réseaux</span></div>
        <div class="repere"><strong>2 langues</strong><span>français · espagnol</span></div>
      </div>
    </div>
    <div class="heros-visuel">
      <img src="assets/img/logo-grafycom-carre.webp" alt="Logo Grafycom : un colibri tracé à l'encre sur une aquarelle multicolore" width="1200" height="1200">
    </div>
  </div>
</section>

<section>
  <div class="conteneur centre">
    <span class="eyebrow">Le point de départ</span>
    <h2>Une <b>identité visuelle cohérente</b><br>permet de&nbsp;:</h2>
    <div class="trait"></div>
    <div class="benefices">
      <div class="benefice">Inspirer la <b>confiance</b> immédiatement</div>
      <div class="benefice">Refléter votre <b>expertise réelle</b></div>
      <div class="benefice">Créer un <b>lien durable</b> avec votre clientèle</div>
    </div>
    <p class="chapeau" style="margin-top:36px">Un logo seul ne suffit pas. Ce qui installe une marque, c'est la répétition&nbsp;: les mêmes couleurs, la même typographie et le même ton sur votre devanture, votre carte, votre page Instagram et jusqu'à votre devis.</p>
  </div>
</section>

<section class="fond-creme">
  <div class="conteneur centre">
    <span class="eyebrow">Ce que je fais</span>
    <h2>Des solutions 360°, sur mesure</h2>
    <div class="trait"></div>
    <p class="chapeau">Tout ce qui porte votre nom, conçu au même endroit et dans la même logique.</p>
  </div>

  <div class="conteneur grille g3" style="margin-top:50px">
    <article class="carte">
      <div class="picto p-bleu"><i class="fa-solid fa-feather-pointed" aria-hidden="true"></i></div>
      <h3>Identité de marque</h3>
      <p>Logo, déclinaisons, palette de couleurs, typographies et règles d'usage réunies dans une charte claire, utilisable par n'importe quel imprimeur.</p>
    </article>
    <article class="carte">
      <div class="picto p-turq"><i class="fa-solid fa-utensils" aria-hidden="true"></i></div>
      <h3>Menus &amp; cartes</h3>
      <p>Cartes de restaurant, menus du jour, ardoises, sets de table. Une mise en page lisible et hiérarchisée, qui met vos plats — et vos marges — en valeur.</p>
    </article>
    <article class="carte">
      <div class="picto p-violet"><i class="fa-solid fa-print" aria-hidden="true"></i></div>
      <h3>Supports imprimés</h3>
      <p>Cartes de visite, flyers, affiches, kakémonos, brochures, packaging. Des fichiers préparés aux normes de l'imprimeur, fonds perdus et profils compris.</p>
    </article>
    <article class="carte">
      <div class="picto p-rose"><i class="fa-solid fa-store" aria-hidden="true"></i></div>
      <h3>Signalétique &amp; enseignes</h3>
      <p>Vitrines, adhésifs, panneaux, habillage de véhicule. Des visuels calibrés pour le grand format et pour le poseur qui les installera.</p>
    </article>
    <article class="carte">
      <div class="picto p-corail"><i class="fa-solid fa-mobile-screen" aria-hidden="true"></i></div>
      <h3>Réseaux sociaux</h3>
      <p>Bannières, gabarits de publication, carrousels et visuels de campagne. Vous gardez la main&nbsp;: les modèles restent réutilisables mois après mois.</p>
    </article>
    <article class="carte">
      <div class="picto p-orange"><i class="fa-solid fa-diagram-project" aria-hidden="true"></i></div>
      <h3>Gestion de projet</h3>
      <p>Chef de projet autant qu'infographiste&nbsp;: je coordonne imprimeurs, poseurs et prestataires, je vérifie les bons à tirer et je tiens les délais.</p>
    </article>
  </div>

  <div class="conteneur centre" style="margin-top:44px">
    <a href="prestations.html" class="btn btn-secondaire">Le détail des prestations <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
  </div>
</section>

<section class="fond-sable">
  <div class="conteneur centre">
    <span class="eyebrow">Je ne travaille pas seule</span>
    <h2>Un réseau de partenaires</h2>
    <div class="trait"></div>
    <p class="chapeau">Une identité visuelle ne s'arrête pas au fichier&nbsp;: il faut l'imprimer, la poser, la photographier, la mettre en ligne. Autant de métiers qui ne sont pas le mien. Je m'appuie sur des partenaires de la région, choisis et éprouvés — et vous gardez un seul numéro à appeler.</p>
  </div>

  <div class="conteneur grille g4" style="margin-top:50px">
    <article class="carte">
      <div class="picto p-bleu"><i class="fa-solid fa-print" aria-hidden="true"></i></div>
      <h3>Imprimeurs</h3>
      <p>Offset, numérique, grand format, façonnage. Je prépare les fichiers à leurs normes, je consulte, je compare les devis et je vérifie les bons à tirer avant lancement.</p>
    </article>
    <article class="carte">
      <div class="picto p-corail"><i class="fa-solid fa-sign-hanging" aria-hidden="true"></i></div>
      <h3>Enseignistes &amp; poseurs</h3>
      <p>Enseignes, vitrophanie, habillage de véhicule. Les dimensions et les contraintes de pose sont posées dès le premier crayonné, pas découvertes le jour de l'installation.</p>
    </article>
    <article class="carte">
      <div class="picto p-violet"><i class="fa-solid fa-camera" aria-hidden="true"></i></div>
      <h3>Photographes</h3>
      <p>Une belle mise en page avec de mauvaises photos reste une mauvaise communication. Quand le projet le demande, je fais appel à des photographes du département.</p>
    </article>
    <article class="carte">
      <div class="picto p-turq"><i class="fa-solid fa-code" aria-hidden="true"></i></div>
      <h3>Développeurs web</h3>
      <p>Je conçois la ligne graphique et les gabarits&nbsp;; la mise en ligne et la technique sont confiées à des développeurs avec qui je travaille régulièrement.</p>
    </article>
  </div>

  <div class="conteneur" style="margin-top:40px">
    <div class="encart">
      <strong>Ce que ça change pour vous&nbsp;:</strong> un seul interlocuteur, un seul planning, une seule personne à rappeler si quelque chose ne va pas. Vous restez libre de garder vos propres prestataires&nbsp;: les fichiers sont préparés pour être exploitables par n'importe quel imprimeur.
    </div>
  </div>
</section>

<section>
  <div class="conteneur grille g2" style="align-items:center; gap:clamp(30px,5vw,66px)">
    <div class="portrait">
      <img src="assets/img/sandra-grafycom.webp" alt="Sandra, fondatrice de Grafycom, en portrait. Mentions manuscrites autour d'elle&nbsp;: «&nbsp;hello, moi c'est Sandra&nbsp;», «&nbsp;j'accompagne votre réussite avec Grafycom&nbsp;», «&nbsp;solutions 360° : logos, menus, cartes et supports de communication&nbsp;», «&nbsp;+7 ans d'expertise à votre service&nbsp;»" width="900" height="1125" loading="lazy">
    </div>
    <div>
      <h2>Sandra</h2>
      <div class="trait"></div>
      <p>J'accompagne votre réussite avec Grafycom. Plus de sept ans à concevoir des identités visuelles, à préparer des fichiers d'impression et à coordonner des projets pour des commerces, des artisans et des associations de la région.</p>
      <p style="margin-top:14px">Beaucoup de dirigeants arrivent avec la même phrase&nbsp;: «&nbsp;je n'y connais rien en graphisme&nbsp;». C'est normal, ce n'est pas votre métier. Mon rôle est de traduire ce que vous avez en tête en quelque chose de visible — sans jargon, sans vous faire sentir à côté de la plaque.</p>
      <ul class="liste-check">
        <li>Un devis détaillé avant de commencer&nbsp;: vous savez ce que vous payez et ce que vous recevez.</li>
        <li>Des allers-retours prévus au contrat, pas facturés à la surprise.</li>
        <li>Les fichiers sources vous appartiennent à la livraison.</li>
        <li>Un accompagnement en français comme en espagnol, de part et d'autre de la frontière.</li>
      </ul>
      <div class="groupe-btn" style="margin-top:30px">
        <a href="a-propos.html" class="btn btn-secondaire">Mieux me connaître</a>
      </div>
    </div>
  </div>
</section>

<section class="fond-sable">
  <div class="conteneur centre">
    <span class="eyebrow">Comment ça se passe</span>
    <h2>Quatre étapes, aucune surprise</h2>
    <div class="trait"></div>
  </div>
  <div class="conteneur grille g4" style="margin-top:50px">
    <div class="etape"><span class="num">01</span><h3>On se parle</h3><p>Un échange gratuit pour comprendre votre activité, vos clients et ce qui coince aujourd'hui dans votre image.</p></div>
    <div class="etape"><span class="num">02</span><h3>Je propose</h3><p>Un devis détaillé, puis des pistes créatives argumentées — pas trois variantes au hasard.</p></div>
    <div class="etape"><span class="num">03</span><h3>On affine</h3><p>Les allers-retours prévus au devis, jusqu'à ce que le résultat vous ressemble vraiment.</p></div>
    <div class="etape"><span class="num">04</span><h3>Je livre et je suis</h3><p>Fichiers sources, déclinaisons, et le suivi d'impression ou de pose si vous le souhaitez.</p></div>
  </div>
  <div class="conteneur centre" style="margin-top:44px">
    <a href="methode.html" class="btn btn-secondaire">La méthode en détail <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
  </div>
</section>

<section id="secteurs">
  <div class="conteneur centre">
    <span class="eyebrow">Pour qui</span>
    <h2>Des projets à taille humaine</h2>
    <div class="trait"></div>
    <p class="chapeau">Commerces, artisans, restaurateurs, professions libérales, associations, TPE et PME des Pyrénées-Orientales — et partout ailleurs en visio.</p>
  </div>
  <!-- Photographies d'illustration issues de Wikimedia Commons (licences et
       auteurs crédités dans mentions-legales.html). Ce ne sont pas des
       réalisations de Grafycom : elles situent un secteur, rien de plus. -->
  <div class="conteneur grille g4" style="margin-top:46px">
    <article class="carte-secteur">
      <div class="secteur-photo"><img src="assets/img/secteurs/secteur-restauration.jpg" alt="Table de bistrot et chaises sur un trottoir parisien" width="960" height="720" loading="lazy"></div>
      <div class="secteur-texte"><div class="picto p-corail"><i class="fa-solid fa-wine-glass" aria-hidden="true"></i></div><h3>Restauration &amp; hôtellerie</h3><p>Cartes, menus, enseignes, habillage de terrasse, visuels de saison.</p></div>
    </article>
    <article class="carte-secteur">
      <div class="secteur-photo"><img src="assets/img/secteurs/secteur-artisans.jpg" alt="Atelier de charron et de charpentier, établis et outils" width="960" height="714" loading="lazy"></div>
      <div class="secteur-texte"><div class="picto p-orange"><i class="fa-solid fa-hammer" aria-hidden="true"></i></div><h3>Artisans &amp; bâtiment</h3><p>Logo, marquage de véhicule, panneaux de chantier, plaquettes commerciales.</p></div>
    </article>
    <article class="carte-secteur">
      <div class="secteur-photo"><img src="assets/img/secteurs/secteur-liberales.jpg" alt="Bureau clair avec fauteuils d'accueil et plantes" width="960" height="641" loading="lazy"></div>
      <div class="secteur-texte"><div class="picto p-turq"><i class="fa-solid fa-stethoscope" aria-hidden="true"></i></div><h3>Professions libérales</h3><p>Une image sobre et rassurante&nbsp;: cabinet, plaque, papeterie, prise de rendez-vous.</p></div>
    </article>
    <article class="carte-secteur">
      <div class="secteur-photo"><img src="assets/img/secteurs/secteur-associations.jpg" alt="Affiches de festival collées sur un mur coloré" width="960" height="695" loading="lazy"></div>
      <div class="secteur-texte"><div class="picto p-violet"><i class="fa-solid fa-people-group" aria-hidden="true"></i></div><h3>Associations &amp; événements</h3><p>Affiches, programmes, kakémonos, communication d'un festival ou d'une saison.</p></div>
    </article>
  </div>
</section>

<section class="fond-creme">
  <div class="conteneur">
    <div class="centre">
      <span class="eyebrow">Questions fréquentes</span>
      <h2>Ce qu'on me demande souvent</h2>
      <div class="trait"></div>
    </div>
    <div class="faq" style="margin-top:40px">
      <details open>
        <summary>Combien coûte un logo&nbsp;?</summary>
        <p>Le prix dépend du nombre de pistes créatives, des déclinaisons demandées (couleur, noir et blanc, format carré pour les réseaux, version pour la broderie ou le grand format) et de la charte qui l'accompagne. Plutôt qu'un tarif affiché au hasard, je vous envoie un devis détaillé après un premier échange&nbsp;: vous voyez exactement ce que couvre chaque ligne.</p>
      </details>
      <details>
        <summary>En combien de temps un projet est-il livré&nbsp;?</summary>
        <p>Comptez en général deux à quatre semaines pour une identité visuelle complète, quelques jours pour un support isolé comme un flyer ou un menu. Le vrai facteur, c'est la disponibilité de vos retours&nbsp;: un projet avance à la vitesse des allers-retours.</p>
      </details>
      <details>
        <summary>Est-ce que je récupère les fichiers sources&nbsp;?</summary>
        <p>Oui. À la livraison, vous recevez les fichiers d'exploitation (PDF prêts à imprimer, PNG et JPG pour le web) et les fichiers sources vectoriels. Vous n'êtes jamais prisonnier de votre prestataire.</p>
      </details>
      <details>
        <summary>Travaillez-vous uniquement à Perpignan&nbsp;?</summary>
        <p>Je suis installée à Perpignan et je me déplace dans tout le département&nbsp;: Canet, Argelès, Céret, Thuir, Prades, Le Barcarès… Pour les projets plus lointains, la visio et le partage de fichiers fonctionnent très bien.</p>
      </details>
      <details>
        <summary>Pouvez-vous gérer l'impression&nbsp;?</summary>
        <p>Oui, si vous le souhaitez. Je travaille avec des imprimeurs et des poseurs partenaires dans la région&nbsp;: je prépare les fichiers à leurs normes, je consulte, je vérifie les bons à tirer et je suis la production jusqu'à la livraison. Vous pouvez aussi garder votre propre imprimeur&nbsp;: les fichiers sont prévus pour.</p>
      </details>
      <details>
        <summary>Parlez-vous espagnol&nbsp;?</summary>
        <p>Oui. L'accompagnement se fait en français comme en espagnol, ce qui est pratique pour les entreprises transfrontalières et pour les supports destinés à une clientèle catalane ou espagnole.</p>
      </details>
    </div>
  </div>
</section>

""" + appel(
    "Racontez-moi votre projet",
    "Un logo à refaire, une carte à remettre au propre, une communication à reprendre de zéro&nbsp;? Le premier échange est gratuit et sans engagement&nbsp;: on regarde ensemble ce dont vous avez vraiment besoin.",
    fond="")

page(ACCUEIL,
     "Grafycom — Infographiste à Perpignan | Logo & identité",
     "Infographiste à Perpignan : création de logo, identité visuelle, menus et supports de communication. +7 ans d'expertise. Devis gratuit.",
     BODY,
     ogtitle="Grafycom — L'image qui vous ressemble",
     jsonld=JSONLD)
