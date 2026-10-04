# -*- coding: utf-8 -*-
from gen import page, MAIL, TEL, TEL_URI, FORMULAIRE_ACTIF, ENVOI_FORMULAIRE

BODY = """
<section class="heros">
  <div class="conteneur centre" style="position:relative;z-index:1">
    <span class="eyebrow">Contact</span>
    <h1>Parlons de <span class="texte-degrade">votre projet</span></h1>
    <div class="trait"></div>
    <p class="chapeau">Le premier échange est gratuit et sans engagement. Décrivez-moi votre activité et ce qui vous gêne dans votre image actuelle&nbsp;: je vous réponds sous 48&nbsp;heures ouvrées avec un avis honnête et, si le projet s'y prête, un devis détaillé. Vous pouvez aussi appeler directement le <a href="tel:%(tel_uri)s">%(tel)s</a>.</p>
  </div>
</section>

<section>
  <div class="conteneur form-grille">

    <!-- Aucun service d'envoi n'est branché : tant que l'attribut action reste
         absent, le formulaire ouvre le logiciel de messagerie du visiteur avec
         un message prérempli. Voir le README pour brancher un vrai envoi. -->
    <form class="devis" data-mailto="%(mail)s"%(action)s novalidate>%(champs)s
      <h2 style="margin-bottom:6px">Demande de devis</h2>
      <p style="font-size:15px;margin-bottom:26px">Les champs marqués d'un astérisque sont nécessaires pour vous répondre.</p>

      <div class="champ">
        <label for="nom">Votre nom *</label>
        <input type="text" id="nom" name="nom" required autocomplete="name">
      </div>

      <div class="champ">
        <label for="structure">Votre entreprise ou association <span class="opt">(facultatif)</span></label>
        <input type="text" id="structure" name="structure" autocomplete="organization">
      </div>

      <div class="grille g2" style="gap:16px">
        <div class="champ">
          <label for="email">Courriel *</label>
          <input type="email" id="email" name="email" required autocomplete="email">
        </div>
        <div class="champ">
          <label for="telephone">Téléphone <span class="opt">(facultatif)</span></label>
          <input type="tel" id="telephone" name="telephone" autocomplete="tel">
        </div>
      </div>

      <div class="champ">
        <label>Votre besoin <span class="opt">(plusieurs choix possibles)</span></label>
        <div class="cases">
          <label class="case"><input type="checkbox" name="besoin" value="Logo / identité visuelle"> Logo, identité visuelle</label>
          <label class="case"><input type="checkbox" name="besoin" value="Menus / cartes"> Menus, cartes</label>
          <label class="case"><input type="checkbox" name="besoin" value="Supports imprimés"> Supports imprimés</label>
          <label class="case"><input type="checkbox" name="besoin" value="Signalétique / enseigne"> Signalétique, enseigne</label>
          <label class="case"><input type="checkbox" name="besoin" value="Réseaux sociaux / web"> Réseaux sociaux, web</label>
          <label class="case"><input type="checkbox" name="besoin" value="Je ne sais pas encore"> Je ne sais pas encore</label>
        </div>
      </div>

      <div class="grille g2" style="gap:16px">
        <div class="champ">
          <label for="budget">Budget envisagé <span class="opt">(facultatif)</span></label>
          <select id="budget" name="budget">
            <option value="">Je préfère en parler</option>
            <option>Moins de 500 €</option>
            <option>500 à 1 500 €</option>
            <option>1 500 à 3 000 €</option>
            <option>Plus de 3 000 €</option>
          </select>
        </div>
        <div class="champ">
          <label for="delai">Pour quand&nbsp;? <span class="opt">(facultatif)</span></label>
          <select id="delai" name="delai">
            <option value="">Pas d'échéance précise</option>
            <option>C'est urgent</option>
            <option>Dans le mois</option>
            <option>Dans les trois mois</option>
            <option>Je prépare pour plus tard</option>
          </select>
        </div>
      </div>

      <div class="champ">
        <label for="message">Votre projet *</label>
        <textarea id="message" name="message" required placeholder="Votre activité, vos clients, ce qui existe déjà et ce qui vous gêne aujourd'hui. Pas besoin de vocabulaire technique : écrivez simplement."></textarea>
      </div>

      <!-- Pot de miel anti-robots : invisible et hors du parcours au clavier.
           Un humain ne le voit pas, un robot le remplit et l'envoi est rejeté. -->
      <div class="pot-de-miel" aria-hidden="true">
        <label for="entreprise-site">Ne remplissez pas ce champ</label>
        <input type="text" id="entreprise-site" name="botcheck" tabindex="-1" autocomplete="off">
      </div>

      <div class="champ rgpd">
        <input type="checkbox" id="rgpd" name="rgpd" required>
        <label for="rgpd" style="font-weight:400;font-size:13px">J'accepte que les informations saisies soient utilisées pour me recontacter au sujet de ma demande. Elles ne sont ni revendues ni transmises à un tiers — voir la <a href="confidentialite.html">politique de confidentialité</a>. *</label>
      </div>

      <button type="submit" class="btn btn-couleur" style="width:100%%">Envoyer ma demande <i class="fa-solid fa-paper-plane" aria-hidden="true"></i></button>
      <p class="form-aide">Vous préférez écrire ou appeler directement&nbsp;? <a href="mailto:%(mail)s">%(mail)s</a> — <a href="tel:%(tel_uri)s">%(tel)s</a></p>
    </form>

    <aside>
      <div class="bloc-contact">
        <h3 style="margin-bottom:10px">Grafycom</h3>
        <p style="font-size:15px">Studio de communication visuelle — Sandra, infographiste et chef de projet.</p>
        <div style="margin-top:18px">
          <div class="ligne-contact">
            <i class="fa-solid fa-envelope" aria-hidden="true"></i>
            <div><strong>Courriel</strong><a href="mailto:%(mail)s">%(mail)s</a></div>
          </div>
          <div class="ligne-contact">
            <i class="fa-solid fa-phone" aria-hidden="true"></i>
            <div><strong>Téléphone</strong><a href="tel:%(tel_uri)s">%(tel)s</a></div>
          </div>
          <div class="ligne-contact">
            <i class="fa-solid fa-location-dot" aria-hidden="true"></i>
            <div><strong>Où</strong><span style="font-size:15px">Perpignan (66000) — déplacements dans tout le département des Pyrénées-Orientales, visio partout ailleurs.</span></div>
          </div>
          <div class="ligne-contact">
            <i class="fa-solid fa-clock" aria-hidden="true"></i>
            <div><strong>Réponse</strong><span style="font-size:15px">Sous 48 heures ouvrées.</span></div>
          </div>
          <div class="ligne-contact">
            <i class="fa-solid fa-language" aria-hidden="true"></i>
            <div><strong>Langues</strong><span style="font-size:15px">Français et espagnol.</span></div>
          </div>
        </div>
      </div>

      <div class="carte carte-creme" style="margin-top:22px">
        <h3>Ce qui aide à bien vous répondre</h3>
        <ul class="liste-check">
          <li>Ce que vous faites, et pour qui</li>
          <li>Ce qui existe déjà (logo, carte, enseigne), même si ça ne vous plaît plus</li>
          <li>Ce qui vous gêne concrètement aujourd'hui</li>
          <li>Une échéance, s'il y en a une</li>
        </ul>
        <p style="font-size:15px;margin-top:16px">Rien de tout cela n'est obligatoire. Un simple «&nbsp;j'ai besoin d'aide pour mon image, on en parle&nbsp;?&nbsp;» fait très bien l'affaire.</p>
      </div>
    </aside>

  </div>
</section>

<section class="fond-creme">
  <div class="conteneur centre">
    <span class="eyebrow">Zone d'intervention</span>
    <h2>Dans le 66, et au-delà</h2>
    <div class="trait"></div>
    <p class="chapeau">Perpignan, Canet-en-Roussillon, Saint-Cyprien, Argelès-sur-Mer, Collioure, Céret, Thuir, Prades, Le Barcarès, Leucate, Rivesaltes, Elne, Saint-Estève&nbsp;— et partout ailleurs en visio.</p>
  </div>
</section>
""" % {
    "mail": MAIL, "tel": TEL, "tel_uri": TEL_URI,
    "action": (' action="%s" method="POST"' % ENVOI_FORMULAIRE) if FORMULAIRE_ACTIF else "",
    "champs": "",
}

page("contact.html",
     "Contact & devis gratuit — Grafycom Perpignan",
     "Contactez Grafycom à Perpignan pour votre logo ou vos supports de communication. Premier échange gratuit, réponse sous 48 h ouvrées.",
     BODY,
     ogtitle="Contacter Grafycom — Perpignan")
