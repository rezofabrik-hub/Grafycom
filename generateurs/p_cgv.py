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
    <p class="chapeau">En vigueur au %(maj)s. Elles s'appliquent à toute prestation commandée à Grafycom, que le client soit une entreprise, une association ou un particulier.</p>
  </div>
</section>

<section>
  <div class="conteneur prose">

    <div class="encart">
      <strong>Prestations entre professionnels.</strong> Grafycom contracte exclusivement avec des clients professionnels — entreprises, commerçants, artisans, professions libérales, associations et collectivités — agissant dans le cadre de leur activité. Les présentes conditions sont rédigées en conséquence.
    </div>

    <h2 style="margin-top:34px">1. Objet et champ d'application</h2>
    <p>Les présentes conditions régissent les prestations de conception graphique et de gestion de projet fournies par Grafycom, nom commercial de Sandra Martinez Gala, entrepreneur individuel immatriculée sous le SIRET 999&nbsp;556&nbsp;301&nbsp;00011 (ci-après «&nbsp;le prestataire&nbsp;»).</p>
    <p>Elles s'appliquent à l'exclusion de toute autre condition, notamment des conditions générales d'achat du client. Toute commande implique leur acceptation sans réserve. Le fait de ne pas se prévaloir d'une clause ne vaut pas renonciation à celle-ci.</p>
    <p><strong>Le prestataire contracte exclusivement avec des professionnels</strong> — personnes physiques ou morales agissant dans le cadre de leur activité commerciale, industrielle, artisanale, libérale ou associative. Les prestations ne sont pas proposées aux consommateurs au sens de l'article liminaire du code de la consommation. En signant le devis, le client déclare agir à titre professionnel.</p>

    <h2>2. Devis et formation du contrat</h2>
    <p>Chaque prestation fait l'objet d'un devis écrit et détaillé, précisant le périmètre, les livrables, le nombre d'allers-retours compris, le délai et le prix. Le devis est <strong>valable un mois</strong> à compter de son émission.</p>
    <p>Le contrat est formé à la date de réception par le prestataire du devis daté, signé et portant la mention «&nbsp;bon pour accord&nbsp;», accompagné du versement de l'acompte prévu.</p>
    <p>Toute demande sortant du périmètre du devis fait l'objet d'un devis complémentaire, soumis à validation avant exécution. Aucun travail hors périmètre n'est facturé sans accord écrit préalable.</p>

    <h2>3. Prix et paiement</h2>
    <p>Les prix sont exprimés en euros. <strong>TVA non applicable, article 293 B du code général des impôts</strong>&nbsp;: les montants indiqués sont nets, aucune TVA n'est facturée ni récupérable.</p>
    <p>Sauf mention contraire au devis&nbsp;: un <strong>acompte de 30&nbsp;%%</strong> est versé à la commande, le solde à la livraison. Le paiement s'effectue par virement, à réception de facture.</p>
    <p>Les sommes versées à la commande constituent des <strong>acomptes</strong> et non des arrhes&nbsp;: elles engagent définitivement les deux parties à exécuter le contrat. Elles restent acquises au prestataire en cas d'annulation du fait du client, sans préjudice du paiement du travail déjà réalisé.</p>

    <h3>Retard de paiement</h3>
    <p>Toute somme non réglée à l'échéance entraîne de plein droit, sans mise en demeure préalable, l'application de pénalités de retard au taux d'intérêt appliqué par la Banque centrale européenne à son opération de refinancement la plus récente, majoré de dix points de pourcentage, ainsi qu'une <strong>indemnité forfaitaire de 40&nbsp;€</strong> pour frais de recouvrement (articles L441-10 et D441-5 du code de commerce). Une indemnité complémentaire peut être réclamée si les frais exposés sont supérieurs.</p>


    <h2>4. Déroulement de la prestation</h2>
    <p>Le client fournit en temps utile l'ensemble des éléments nécessaires&nbsp;: textes, logos, photographies, contenus et informations. Le prestataire ne peut être tenu responsable d'un retard imputable à un défaut de fourniture ou à une validation tardive.</p>
    <p>Le nombre d'allers-retours compris est fixé au devis. Les modifications au-delà de ce nombre, ou revenant sur des éléments déjà validés par écrit, font l'objet d'une facturation complémentaire au tarif horaire indiqué au devis.</p>
    <p>Avant toute impression ou fabrication, le client reçoit un <strong>bon à tirer</strong>. Sa validation écrite engage le client&nbsp;: aucune réclamation portant sur un élément figurant au bon à tirer validé ne peut être retenue ensuite, notamment s'agissant des textes, des prix et de l'orthographe.</p>

    <h2>5. Délais</h2>
    <p>Les délais indiqués courent à compter de la réception de l'acompte et de la totalité des éléments nécessaires. Ils sont donnés à titre indicatif et leur dépassement ne peut donner lieu à annulation de la commande ni à indemnité.</p>
    <p>Le prestataire n'est pas responsable des retards imputables au client, à un tiers intervenant (imprimeur, poseur, hébergeur) ou à un cas de force majeure.</p>

    <h2>6. Livraison et fichiers</h2>
    <p>À la livraison, le client reçoit les fichiers d'exploitation adaptés à l'usage prévu (PDF prêts à imprimer, images optimisées pour le web) ainsi que les fichiers sources, sauf mention contraire au devis.</p>
    <p>Le prestataire conserve une copie des fichiers pendant une durée de <strong>trois ans</strong> à titre de service, sans obligation d'archivage. Il appartient au client de sauvegarder les fichiers livrés.</p>

    <h2>7. Propriété intellectuelle et cession de droits</h2>
    <p>Les créations restent la propriété du prestataire jusqu'au paiement intégral du prix. La cession des droits n'intervient qu'à complet paiement.</p>
    <p>Conformément à l'article L131-3 du code de la propriété intellectuelle, la cession est définie au devis, lequel précise&nbsp;: les <strong>droits cédés</strong> (reproduction, représentation, adaptation), les <strong>supports</strong> concernés, l'<strong>étendue géographique</strong> et la <strong>durée</strong>. À défaut de précision, la cession porte sur les seuls supports mentionnés au devis, pour la France, pour la durée légale de protection.</p>
    <p>Le <strong>droit moral</strong> de l'auteur est incessible&nbsp;: le prestataire conserve le droit au respect de son œuvre et à la paternité de celle-ci.</p>
    <p>Les propositions non retenues restent la propriété du prestataire et ne peuvent être exploitées par le client sous quelque forme que ce soit.</p>
    <p>Le client garantit détenir les droits sur tous les éléments qu'il fournit (textes, images, polices, marques) et garantit le prestataire contre toute réclamation d'un tiers à ce titre.</p>
    <p>Sauf opposition écrite du client, le prestataire peut mentionner le travail réalisé à titre de référence, dans son portfolio et sa communication.</p>

    <h2>8. Annulation et résiliation</h2>
    <p>En cas d'annulation par le client après formation du contrat, en dehors de l'exercice régulier du droit de rétractation, l'acompte reste acquis au prestataire et le travail déjà réalisé est facturé au prorata.</p>
    <p>Le prestataire peut suspendre ou résilier la prestation en cas de défaut de paiement, de fourniture d'éléments manifestement illicites, ou d'absence de réponse du client pendant plus de deux mois. Dans ce dernier cas, le dossier est clos et le travail réalisé facturé.</p>

    <h2>9. Responsabilité</h2>
    <p>Le prestataire est tenu d'une obligation de moyens. Sa responsabilité est limitée au montant de la prestation concernée et ne couvre pas les dommages indirects (perte d'exploitation, perte de chiffre d'affaires, atteinte à l'image).</p>
    <p>Le prestataire ne saurait être tenu responsable de la qualité d'exécution d'un tiers (imprimeur, poseur) choisi par le client, ni d'un défaut résultant d'un élément validé par le client au bon à tirer.</p>
    <p>Ces limitations ne s'appliquent pas en cas de faute lourde ou dolosive.</p>

    <h2>10. Données personnelles</h2>
    <p>Les données collectées dans le cadre de la relation commerciale sont traitées conformément à la <a href="confidentialite.html">politique de confidentialité</a>.</p>

    <h2>11. Droit applicable et litiges</h2>
    <p>Les présentes conditions sont soumises au droit français.</p>
    <p>Les parties s'efforceront de résoudre amiablement tout différend. À défaut d'accord dans un délai de trente jours, compétence exclusive est attribuée au tribunal du ressort du siège du prestataire, y compris en cas de référé, de pluralité de défendeurs ou d'appel en garantie.</p>

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
maj = "23 septembre 2026"

page("cgv.html",
     "Conditions générales de vente — Grafycom",
     "Conditions générales de vente de Grafycom, Perpignan : devis, paiement, délais, cession de droits et responsabilité. Prestations entre professionnels.",
     BODY % {"mail": MAIL, "maj": maj},
     ogtitle="Conditions générales de vente — Grafycom",
     robots="noindex, follow")
