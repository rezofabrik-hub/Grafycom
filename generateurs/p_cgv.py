# -*- coding: utf-8 -*-
"""Conditions générales de vente — deux clientèles, professionnels et
particuliers, avec les obligations propres à chacune."""
from gen import page, MAIL, TEL, TEL_URI


BODY = ("""
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">Conditions générales</span>
    <h1>Conditions générales<br><span class="texte-degrade">de vente</span></h1>
    <div class="trait"></div>
    <p class="chapeau">En vigueur au %(maj)s. Elles s'appliquent à toute prestation commandée à Grafycom.</p>
  </div>
</section>

<section>
  <div class="conteneur prose">

    <div class="encart">
      <strong>Prestations entre professionnels.</strong> Grafycom contracte exclusivement avec des clients professionnels — entreprises, commerçants, artisans, professions libérales, associations et collectivités — agissant dans le cadre de leur activité. Les présentes conditions sont rédigées en conséquence.
    </div>

    <h2 style="margin-top:34px">1. Identification du prestataire</h2>
    <p>Les présentes conditions générales de vente sont conclues par <strong>Sandra Martinez Gala</strong>, entrepreneur individuel (EI).</p>
    <ul>
      <li>Nom commercial&nbsp;: <strong>GRAFYCOM</strong></li>
      <li>Siège social&nbsp;: 98 avenue Louis Torcatis, 66000 Perpignan, France</li>
      <li>Immatriculation&nbsp;: 999&nbsp;556&nbsp;301 R.C.S. Perpignan — SIRET 999&nbsp;556&nbsp;301&nbsp;00011</li>
      <li>Contact&nbsp;: <a href="mailto:%(mail)s">%(mail)s</a> — %(tel)s</li>
    </ul>

    <h2>2. Objet et activités</h2>
    <p>Les présentes conditions régissent l'ensemble des activités de l'entreprise, couvertes par une assurance responsabilité civile professionnelle&nbsp;:</p>
    <ul>
      <li>infographie, conseil en image et en communication&nbsp;;</li>
      <li>services administratifs divers&nbsp;;</li>
      <li>création, personnalisation et pose de signalétiques intérieures et extérieures, sur tous supports&nbsp;;</li>
      <li>apporteur d'affaires dans le domaine de la communication.</li>
    </ul>
    <p>Elles s'appliquent à l'exclusion de toute autre condition, notamment des conditions générales d'achat du client. Toute commande implique leur acceptation sans réserve. Le fait de ne pas se prévaloir d'une clause ne vaut pas renonciation à celle-ci.</p>
    <p><strong>Le prestataire contracte exclusivement avec des professionnels</strong> — personnes physiques ou morales agissant dans le cadre de leur activité commerciale, industrielle, artisanale, libérale ou associative. En signant le devis, le client déclare agir à titre professionnel.</p>

    <h2>3. Devis, commandes et paiement</h2>
    <p>Chaque prestation fait l'objet d'un devis écrit et détaillé, précisant le périmètre, les livrables, le nombre d'allers-retours compris, le délai et le prix. Le devis est <strong>valable un mois</strong> à compter de son émission.</p>
    <p>Le contrat est formé à la date de réception par le prestataire du devis daté, signé et portant la mention «&nbsp;bon pour accord&nbsp;», accompagné du versement prévu ci-dessous.</p>

    <h3>Montants et échéances</h3>
    <ul>
      <li><strong>Minimum de commande&nbsp;:</strong> un montant minimum de facturation de <strong>100&nbsp;€</strong> est appliqué à toute commande.</li>
      <li><strong>Commandes inférieures ou égales à 100&nbsp;€&nbsp;:</strong> paiement intégral à la commande.</li>
      <li><strong>Commandes supérieures à 100&nbsp;€&nbsp;:</strong> acompte de <strong>50&nbsp;%%</strong> à la commande, solde réglé avant la livraison.</li>
      <li><strong>Délai de versement&nbsp;:</strong> l'acompte, ou le paiement intégral pour les petits montants, est versé sous <strong>sept jours calendaires</strong> après la signature du devis. À défaut, la validation du devis est annulée de plein droit.</li>
    </ul>
    <p>Les sommes versées à la commande constituent des <strong>acomptes</strong> et non des arrhes&nbsp;: elles engagent définitivement les deux parties à exécuter le contrat. Elles restent acquises au prestataire en cas d'annulation du fait du client, sans préjudice du paiement du travail déjà réalisé.</p>
    <p>Toute demande sortant du périmètre du devis fait l'objet d'un devis complémentaire, soumis à validation avant exécution.</p>

    <h3>Retard de paiement</h3>
    <p>Tout retard de paiement donne lieu, de plein droit et sans mise en demeure préalable, à des pénalités de retard calculées sur la base de <strong>trois fois le taux d'intérêt légal</strong>, ainsi qu'à une <strong>indemnité forfaitaire de 40&nbsp;€</strong> pour frais de recouvrement (article L441-10 du code de commerce). Une indemnité complémentaire peut être réclamée si les frais exposés sont supérieurs.</p>

    <h2>4. Infographie et propriété intellectuelle</h2>

    <h3>Processus de création</h3>
    <p>La prestation comprend un maximum de <strong>deux propositions initiales</strong> ou <strong>deux allers-retours de corrections</strong>. Toute demande supplémentaire, ou revenant sur un élément déjà validé par écrit, fait l'objet d'une facturation complémentaire.</p>
    <p>Le client fournit en temps utile l'ensemble des éléments nécessaires&nbsp;: textes, logos, photographies, contenus et informations. Le prestataire ne peut être tenu responsable d'un retard imputable à un défaut de fourniture ou à une validation tardive.</p>

    <h3>Validation — le bon à tirer</h3>
    <p>Avant toute impression ou fabrication, le client reçoit un <strong>bon à tirer</strong>. Sa validation par le client est <strong>définitive</strong>. Elle porte sur le contenu (orthographe, numéros, textes), la mise en forme, la couleur et les dimensions lorsqu'elles sont indiquées. Elle dégage le prestataire de toute responsabilité pour une erreur constatée après validation.</p>

    <h3>Droits d'auteur et cession</h3>
    <p>Le prestataire reste titulaire des droits d'auteur sur ses créations. <strong>Le transfert des droits d'exploitation intervient après paiement intégral du prix.</strong></p>
    <p>Conformément à l'article L131-3 du code de la propriété intellectuelle, la cession est définie au devis, lequel précise&nbsp;: les <strong>droits cédés</strong> (reproduction, représentation, adaptation), les <strong>supports</strong> concernés, l'<strong>étendue géographique</strong> et la <strong>durée</strong>. À défaut de précision, la cession porte sur les seuls supports mentionnés au devis, pour la France, pour la durée légale de protection.</p>
    <p>Le <strong>droit moral</strong> de l'auteur est incessible&nbsp;: le prestataire conserve le droit au respect de son œuvre et à la paternité de celle-ci.</p>
    <p>Les propositions non retenues restent la propriété du prestataire et ne peuvent être exploitées par le client sous quelque forme que ce soit.</p>
    <p>Le prestataire n'est pas responsable des droits de reproduction des originaux fournis par le client. Celui-ci garantit détenir les droits sur tous les éléments qu'il fournit (textes, images, polices, marques) et garantit le prestataire contre toute réclamation d'un tiers à ce titre.</p>

    <h3>Propriété des fichiers</h3>
    <p>À la livraison, le client reçoit les <strong>fichiers d'exploitation</strong> adaptés à l'usage prévu&nbsp;: PDF prêts à imprimer, images optimisées pour le web, déclinaisons prévues au devis.</p>
    <p>Les <strong>fichiers sources</strong> (.ai, .psd, .indd et formats de travail équivalents) demeurent la propriété exclusive du prestataire. Leur transmission n'est pas automatique&nbsp;: elle fait l'objet d'un accord écrit et peut être facturée. <strong>Toute modification d'une création sans accord écrit du prestataire est interdite.</strong></p>
    <p>Le prestataire conserve une copie des fichiers pendant une durée de <strong>trois ans</strong> à titre de service, sans obligation d'archivage. Il appartient au client de sauvegarder les fichiers livrés.</p>

    <h2>5. Gestion et création de réseaux sociaux</h2>

    <h3>5.1 Périmètre et création de comptes</h3>
    <p>La prestation concerne soit la création de nouveaux comptes, soit la gestion des réseaux sociaux que le client possède déjà au jour de la signature. Pour toute création de compte, le client s'engage à fournir les informations d'identité et de contact nécessaires à l'ouverture des profils.</p>

    <h3>5.2 Fourniture et propriété des contenus</h3>
    <p>Pour chaque publication mensuelle, le client fournit l'intégralité du texte ainsi que les éléments visuels (photographies, logos, vidéos) <strong>avant le 5 du mois précédant la publication</strong>. Le client garantit détenir les droits de propriété intellectuelle et de reproduction sur l'ensemble de ces contenus. Le prestataire ne peut être tenu responsable du contenu publié dès lors qu'il a été fourni par le client.</p>

    <h3>5.3 Règlement</h3>
    <ul>
      <li><strong>Paiement mensuel&nbsp;:</strong> la prestation est réglée en totalité <strong>avant le 5 du mois de sa réalisation</strong>.</li>
      <li><strong>Abonnement long terme&nbsp;:</strong> pour un abonnement mensuel sur six mois, l'intégralité des six mois est réglée avant le 5 du premier mois.</li>
      <li>Aucun début d'exécution ni mise en ligne n'intervient sans réception préalable du règlement complet selon l'échéance prévue.</li>
    </ul>

    <h3>5.4 Exonération de responsabilité</h3>
    <p>Si le client ne fournit pas les éléments ou ne procède pas au règlement dans les délais impartis, le prestataire ne peut être tenu responsable de l'absence de publications ni de la rupture de visibilité qui en résulte.</p>
    <p>Le prestataire décline toute responsabilité en cas de bug technique, de modification des algorithmes, de suspension ou de suppression de compte par la plateforme (Meta, Instagram, LinkedIn, etc.), ces événements relevant de la force majeure ou de la politique de tiers.</p>

    <h3>5.5 Accès et confidentialité</h3>
    <p>Le client s'engage à fournir les accès nécessaires. Le prestataire s'engage à une confidentialité stricte et à ne divulguer ces accès à aucun tiers.</p>

    <h2>6. Services administratifs</h2>
    <p>Tout document édité pour un tiers est vérifié et validé par le client avant envoi. Le prestataire décline toute responsabilité en cas d'erreur constatée après mise à disposition pour relecture.</p>

    <h2>7. Signalétique et pose</h2>
    <ul>
      <li><strong>Installation et autorisations&nbsp;:</strong> le client assure l'accessibilité du site et obtient les autorisations nécessaires (mairie, syndic, bailleur).</li>
      <li><strong>Imprévus&nbsp;:</strong> tout report de pose imputable au client — autorisations manquantes, supports sales ou détériorés, site inaccessible — entraîne la facturation des frais de déplacement, du temps perdu et de la perte d'exploitation.</li>
      <li><strong>Réception&nbsp;:</strong> toute réclamation est notifiée par écrit dans les <strong>48 heures</strong> suivant la livraison ou la pose.</li>
    </ul>

    <h2>8. Apporteur d'affaires</h2>
    <p>La commission est due dès la mise en relation aboutissant à une commande ferme, même en l'absence de paiement complet par le client final au prestataire tiers.</p>

    <h2>9. Délais, responsabilité, assurance et force majeure</h2>
    <p>Les délais indiqués courent à compter de la réception de l'acompte et de la totalité des éléments nécessaires. Ils sont donnés à titre indicatif et leur dépassement ne peut donner lieu à annulation de la commande ni à indemnité.</p>
    <p><strong>Assurance&nbsp;:</strong> le prestataire dispose d'une assurance responsabilité civile professionnelle auprès d'AXA, couvrant l'ensemble de ses activités. Les références du contrat sont communiquées sur simple demande.</p>
    <p><strong>Limitation&nbsp;:</strong> le prestataire est tenu d'une obligation de moyens. Sa responsabilité est limitée au montant hors taxes de la commande concernée et ne couvre pas les dommages indirects (perte d'exploitation, perte de chiffre d'affaires, atteinte à l'image).</p>
    <p>Le prestataire ne saurait être tenu responsable de la qualité d'exécution d'un tiers (imprimeur, poseur, hébergeur) choisi par le client, ni d'un défaut résultant d'un élément validé par le client au bon à tirer.</p>
    <p><strong>Force majeure&nbsp;:</strong> le prestataire n'est pas responsable des retards causés par des événements extérieurs (pénurie, intempéries, défaillance d'un tiers) ni des erreurs causées par le client.</p>
    <p>Ces limitations ne s'appliquent pas en cas de faute lourde ou dolosive.</p>

    <h2>10. Annulation et résiliation</h2>
    <p>En cas d'annulation par le client après formation du contrat, l'acompte reste acquis au prestataire et le travail déjà réalisé est facturé au prorata.</p>
    <p>Le prestataire peut suspendre ou résilier la prestation en cas de défaut de paiement, de fourniture d'éléments manifestement illicites, ou d'absence de réponse du client pendant plus de deux mois. Dans ce dernier cas, le dossier est clos et le travail réalisé facturé.</p>

    <h2>11. Clauses générales</h2>
    <ul>
      <li><strong>TVA&nbsp;:</strong> TVA non applicable, article 293 B du code général des impôts. Les montants indiqués sont nets, aucune TVA n'est facturée ni récupérable.</li>
      <li><strong>Réserve de propriété&nbsp;:</strong> les produits livrés restent la propriété du prestataire jusqu'au paiement intégral.</li>
      <li><strong>Droit à l'image&nbsp;:</strong> sauf refus écrit du client, le prestataire peut utiliser les photographies de ses réalisations à des fins de promotion.</li>
      <li><strong>Données personnelles&nbsp;:</strong> les données collectées dans le cadre de la relation commerciale sont utilisées pour la seule gestion client et traitées conformément à la <a href="confidentialite.html">politique de confidentialité</a>. Les droits d'accès et de rectification sont garantis.</li>
    </ul>

    <h2>12. Droit applicable et litiges</h2>
    <p>Les présentes conditions sont soumises au droit français.</p>
    <p>Les parties s'efforceront de résoudre amiablement tout différend. À défaut d'accord dans un délai de trente jours, <strong>compétence exclusive est attribuée au tribunal de commerce de Perpignan</strong>, y compris en cas de référé, de pluralité de défendeurs ou d'appel en garantie.</p>

    <p style="margin-top:34px;font-size:14px;color:var(--taupe)">Dernière mise à jour&nbsp;: %(maj)s.</p>
  </div>
</section>
""")

# Date d'entrée en vigueur des conditions. Elle est écrite en dur, et
# c'est voulu : prise sur l'horloge, elle changeait à chaque
# régénération du site, annonçant à chaque fois de nouvelles conditions
# alors que pas une ligne n'avait bougé. Un document contractuel ne
# change pas de date parce qu'on a reconstruit une page.
#
# À modifier à la main, et seulement quand les conditions changent.
maj = "24 octobre 2026"

page("cgv.html",
     "Conditions générales de vente — Grafycom",
     "Conditions générales de vente de Grafycom, Perpignan : devis, paiement, délais, cession de droits et responsabilité. Prestations entre professionnels.",
     BODY % {"mail": MAIL, "tel": TEL, "maj": maj},
     ogtitle="Conditions générales de vente — Grafycom",
     robots="noindex, follow")
