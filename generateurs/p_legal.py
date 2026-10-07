# -*- coding: utf-8 -*-
from gen import page, MAIL, TEL, TEL_URI

TODO = '<mark style="background:#f9c33f;padding:2px 6px;border-radius:4px">[À COMPLÉTER&nbsp;: %s]</mark>'

ML = ("""
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">Informations légales</span>
    <h1>Mentions légales</h1>
    <div class="trait"></div>
  </div>
</section>

<section>
  <div class="conteneur prose">
    <div class="encart">
      Ces mentions sont obligatoires pour un site professionnel (article 6-III de la loi pour la confiance dans l'économie numérique). Les informations d'identification ci-dessous proviennent du registre national des entreprises.
    </div>

    <h2 style="margin-top:34px">Éditeur du site</h2>
    <p>
      <strong>Grafycom</strong> — nom commercial de Sandra Martinez Gala<br>
      Entrepreneur individuel<br>
      SIREN&nbsp;: 999&nbsp;556&nbsp;301<br>
      SIRET du siège&nbsp;: 999&nbsp;556&nbsp;301&nbsp;00011<br>
      TVA&nbsp;: non applicable, article 293 B du code général des impôts<br>
      Siège&nbsp;: Perpignan (66000) — adresse postale communiquée sur demande<br>
      Directrice de la publication&nbsp;: Sandra Martinez Gala<br>
      Téléphone&nbsp;: <a href="tel:%(tel_uri)s">%(tel)s</a><br>
      Courriel&nbsp;: <a href="mailto:%(mail)s">%(mail)s</a>
    </p>
    <!-- L'adresse du siège est publique au registre national des entreprises
         (annuaire-entreprises.data.gouv.fr) mais n'est pas publiée ici, à la
         demande de l'éditrice. L'article 6-III de la LCEN l'exige : voir la
         section « Ce qui reste à trancher » du README. -->

    <h2>Hébergeur</h2>
    <p>
      GitHub,&nbsp;Inc.<br>
      88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis<br>
      <a href="https://github.com" rel="noopener">github.com</a>
    </p>
    <p>Le site est un ensemble de fichiers statiques servis par GitHub&nbsp;Pages. Aucune donnée de visiteur n'y est enregistrée par l'éditrice&nbsp;; voir la <a href="confidentialite.html">politique de confidentialité</a>.</p>

    <h2>Propriété intellectuelle</h2>
    <p>L'ensemble du site — structure, textes, logo Grafycom, visuels, mise en page — est protégé par le code de la propriété intellectuelle. Toute reproduction ou représentation, totale ou partielle, sans autorisation écrite préalable est interdite.</p>
    <p>Les créations présentées dans la rubrique «&nbsp;Réalisations&nbsp;» sont la propriété de leurs commanditaires respectifs et sont reproduites ici à titre de référence professionnelle, avec leur accord.</p>

    <h2>Cession des droits sur les créations</h2>
    <p>Pour les travaux commandés à Grafycom, les droits d'exploitation sont cédés au client dans les conditions prévues au devis et aux conditions générales de vente. Sauf mention contraire écrite, la cession porte sur les supports et la durée qui y sont définis. Grafycom conserve le droit de mentionner le travail réalisé dans son portfolio, sauf demande contraire du client.</p>

    <h2>Crédits photographiques</h2>
    <p>Les photographies qui illustrent les secteurs d'activité sur la page d'accueil, ainsi que celles de la page «&nbsp;Réalisations&nbsp;», sont des <strong>réalisations de Grafycom</strong>. Les marques qui y figurent appartiennent à leurs titulaires respectifs et ne sont montrées qu'à titre de référence de travaux.</p>
    <p>Sur la page «&nbsp;Prestations&nbsp;», quatre rubriques montrent des réalisations de Grafycom. Les deux dernières restent illustrées par des photographies libres de droits&nbsp;:</p>
    <ul>
      <li><strong>Réseaux sociaux</strong> — «&nbsp;Phone (Unsplash)&nbsp;», par Jenu Prasad jenuprasad, <a href="http://creativecommons.org/publicdomain/zero/1.0/deed.en" rel="noopener">CC0</a>, via <a href="https://commons.wikimedia.org/wiki/File:Phone_(Unsplash).jpg" rel="noopener">Wikimedia Commons</a>.</li>
      <li><strong>Gestion de projet</strong> — «&nbsp;Camera keys notebook coffee (Unsplash)&nbsp;», par Melinda Pack melindapack, <a href="http://creativecommons.org/publicdomain/zero/1.0/deed.en" rel="noopener">CC0</a>, via <a href="https://commons.wikimedia.org/wiki/File:Camera_keys_notebook_coffee_(Unsplash).jpg" rel="noopener">Wikimedia Commons</a>.</li>
    </ul>

    <p>Le logo Grafycom et l'ensemble des créations présentées dans la rubrique «&nbsp;Réalisations&nbsp;» ne relèvent pas de ces licences&nbsp;: voir le paragraphe «&nbsp;Propriété intellectuelle&nbsp;» ci-dessus.</p>

    <h2>Liens hypertextes</h2>
    <p>Le site peut renvoyer vers des sites tiers. Grafycom n'exerce aucun contrôle sur leur contenu et décline toute responsabilité à leur égard.</p>

    <h2>Données personnelles</h2>
    <p>Le traitement des données transmises via le formulaire de contact est décrit dans la <a href="confidentialite.html">politique de confidentialité</a>.</p>

    <h2>Clientèle</h2>
    <p>Grafycom fournit ses prestations <strong>exclusivement à des clients professionnels</strong> — entreprises, commerçants, artisans, professions libérales, associations et collectivités — agissant dans le cadre de leur activité. Les prestations ne sont pas proposées aux consommateurs au sens de l'article liminaire du code de la consommation.</p>
    <p>Le dispositif de médiation de la consommation prévu à l'article L612-1 du même code, qui s'impose aux professionnels contractant avec des consommateurs, est par conséquent sans objet. Les conditions de la relation commerciale figurent aux <a href="cgv.html">conditions générales de vente</a>.</p>

    <h2>Droit applicable</h2>
    <p>Le présent site est soumis au droit français. En cas de litige, et à défaut de résolution amiable, les tribunaux français sont seuls compétents.</p>

    <p style="margin-top:34px;font-size:14px;color:var(--taupe)">Dernière mise à jour&nbsp;: 20 septembre 2026</p>
  </div>
</section>
""") % {"mail": MAIL, "tel": TEL, "tel_uri": TEL_URI}

page("mentions-legales.html",
     "Mentions légales | Grafycom",
     "Mentions légales du site Grafycom : éditeur, hébergeur, propriété intellectuelle et droit applicable.",
     ML, robots="noindex, follow")


CONF = ("""
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">Vos données</span>
    <h1>Politique de confidentialité</h1>
    <div class="trait"></div>
    <p class="chapeau">Ce site ne dépose aucun cookie de suivi et ne collecte que ce que vous écrivez vous-même dans le formulaire de contact.</p>
  </div>
</section>

<section>
  <div class="conteneur prose">
    <div class="encart">
      <strong>À jour du site tel qu'il fonctionne aujourd'hui&nbsp;:</strong> statique, sans cookie, sans mesure d'audience, sans aucune ressource chargée depuis un service tiers. Si vous ajoutez un outil de statistiques, un pixel de réseau social, une carte interactive ou un service d'envoi de formulaire, ce document doit être mis à jour et un bandeau de consentement devient nécessaire.
    </div>

    <h2 style="margin-top:34px">Qui est responsable de vos données</h2>
    <p>Grafycom, dont les coordonnées figurent dans les <a href="mentions-legales.html">mentions légales</a>, est responsable du traitement des données collectées sur ce site.</p>

    <h2>Quelles données sont collectées</h2>
    <p>Uniquement celles que vous renseignez dans le formulaire de contact&nbsp;: nom, nom de la structure, adresse de courriel, numéro de téléphone si vous le donnez, nature du besoin, budget et délai indiqués, et le contenu de votre message.</p>
    <p>Aucun champ caché, aucun profilage, aucune collecte à votre insu.</p>

    <h2>Pourquoi</h2>
    <p>Pour répondre à votre demande, établir un devis et, le cas échéant, suivre le projet. La base légale est votre consentement, matérialisé par la case à cocher du formulaire, puis l'exécution du contrat si nous travaillons ensemble.</p>
    <p>Vos coordonnées ne servent à aucune prospection commerciale non sollicitée, et ne sont ni vendues, ni louées, ni transmises à un tiers à des fins commerciales.</p>

    <h2>Combien de temps</h2>
    <p>Trois ans à compter du dernier contact pour une demande restée sans suite. Pour les clients, la durée légale de conservation des documents comptables et contractuels, soit dix ans pour les pièces comptables.</p>

    <h2>Qui y a accès</h2>
    <p>Sandra, seule. Les prestataires techniques strictement nécessaires (hébergeur du site, fournisseur de messagerie) peuvent héberger ces données dans le cadre de leur service, sans y accéder pour leur propre compte.</p>

    <h2>Cookies</h2>
    <p>Ce site ne dépose <strong>aucun cookie</strong> — ni publicitaire, ni de mesure d'audience, ni technique. Il n'utilise aucun traceur.</p>
    <p>Toutes les ressources — polices de caractères, icônes, images, feuille de style, script — sont <strong>servies depuis ce site</strong>. Aucune requête n'est adressée à un service tiers&nbsp;: votre adresse IP n'est transmise à personne d'autre qu'à l'hébergeur, dans le simple fait d'afficher la page. C'est un choix délibéré&nbsp;: un site qui charge ses polices chez Google communique l'adresse IP de chacun de ses visiteurs à Google, sans que personne l'ait demandé.</p>
    <p>Aucun bandeau de consentement n'est donc nécessaire, puisqu'il n'y a rien à consentir.</p>

    <h2>Vos droits</h2>
    <p>Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation et d'opposition sur vos données, ainsi que d'un droit à la portabilité. Pour les exercer, écrivez à <a href="mailto:%(mail)s">%(mail)s</a>&nbsp;; une réponse vous sera apportée sous un mois.</p>
    <p>Si la réponse ne vous satisfait pas, vous pouvez saisir la CNIL&nbsp;: <a href="https://www.cnil.fr" rel="noopener">www.cnil.fr</a>, 3 place de Fontenoy, TSA 80715, 75334 Paris Cedex 07.</p>

    <h2>Sécurité</h2>
    <p>Le site est diffusé exclusivement en HTTPS, avec redirection automatique depuis HTTP. Il applique une politique de sécurité de contenu (<em>Content Security Policy</em>) qui n'autorise le chargement d'aucune ressource extérieure au site et interdit son affichage dans un cadre tiers. Les messages reçus sont conservés dans une messagerie protégée par mot de passe.</p>

    <p style="margin-top:34px;font-size:14px;color:var(--taupe)">Dernière mise à jour&nbsp;: 20 septembre 2026</p>
  </div>
</section>
""") % {"mail": MAIL, "tel": TEL, "tel_uri": TEL_URI}

page("confidentialite.html",
     "Politique de confidentialité | Grafycom",
     "Comment Grafycom traite les données transmises via le formulaire de contact : finalité, durée de conservation, droits d'accès et de suppression.",
     CONF, robots="noindex, follow")
