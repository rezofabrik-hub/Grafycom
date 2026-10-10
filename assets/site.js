/* Grafycom — interactions communes
   Menu mobile, année du copyright, visuels en attente, formulaire de contact. */
(function () {
  'use strict';

  // --- Menu mobile ---
  var burger = document.querySelector('.burger');
  var nav = document.querySelector('nav.principal');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var ouvert = nav.classList.toggle('ouvert');
      burger.setAttribute('aria-expanded', ouvert ? 'true' : 'false');
      burger.innerHTML = ouvert
        ? '<i class="fa-solid fa-xmark" aria-hidden="true"></i>'
        : '<i class="fa-solid fa-bars" aria-hidden="true"></i>';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('ouvert');
        burger.setAttribute('aria-expanded', 'false');
        burger.innerHTML = '<i class="fa-solid fa-bars" aria-hidden="true"></i>';
      }
    });
  }

  // --- Année courante ---
  document.querySelectorAll('[data-annee]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* --- Visuels pas encore déposés ---
     Une image portant data-attente affiche un cadre explicite tant que le
     fichier n'est pas dans assets/img/ : pas d'icône « image cassée ». */
  function remplacer(img) {
    if (!img.parentNode) return;
    var bloc = document.createElement('div');
    bloc.className = 'placeholder-visuel';
    // Le chemin du fichier reste en info-bulle : utile à qui maintient le site,
    // invisible pour le visiteur, à qui il ne dirait rien.
    bloc.title = 'Fichier attendu : ' + img.getAttribute('src');
    bloc.innerHTML = '<i class="fa-regular fa-image" aria-hidden="true"></i>'
      + '<strong>' + (img.getAttribute('data-attente') || 'Visuel à venir') + '</strong>';
    img.parentNode.replaceChild(bloc, img);
  }

  document.querySelectorAll('img[data-attente]').forEach(function (img) {
    // L'erreur de chargement peut être survenue avant l'exécution de ce script.
    if (img.complete && img.naturalWidth === 0) { remplacer(img); return; }
    img.addEventListener('error', function () { remplacer(img); });
  });

  /* --- Retour d'erreur après un envoi refusé ---
     Le Worker renvoie vers /contact.html?erreur=… plutôt que d'afficher une
     page nue : le visiteur retrouve ses repères, et on lui dit quoi faire. */
  var erreur = new URLSearchParams(window.location.search).get('erreur');
  if (erreur) {
    var textes = {
      champs: "Il manque quelque chose : votre nom, une adresse de courriel valide et une description de votre projet sont nécessaires pour vous répondre.",
      envoi: "L'envoi n'a pas abouti — le problème vient de chez moi, pas de vous. Réessayez dans un instant, ou appelez-moi directement.",
      format: "Le formulaire n'a pas été transmis correctement. Réessayez, ou écrivez-moi directement."
    };
    var cible = document.querySelector('form.devis');
    if (cible) {
      var avis = document.createElement('p');
      avis.setAttribute('role', 'alert');
      avis.style.cssText = 'background:#fdecea;border-left:4px solid #f2585c;border-radius:0 12px 12px 0;'
        + 'padding:16px 18px;margin-bottom:24px;font-size:15px;color:#7a2a2a';
      avis.textContent = textes[erreur] || textes.envoi;
      cible.insertBefore(avis, cible.firstChild);
      avis.scrollIntoView({ block: 'center' });
    }
  }

  /* --- Formulaire de contact ---
     Tant qu'aucun service d'envoi n'est branché (voir README), le formulaire
     compose un courriel prérempli plutôt que de perdre le message. */
  var form = document.querySelector('form.devis[data-mailto]');
  if (form) {
    form.addEventListener('submit', function (e) {
      if (form.getAttribute('action')) return; // un service d'envoi est configuré
      e.preventDefault();
      if (!form.reportValidity()) return;

      var d = new FormData(form);
      var besoins = d.getAll('besoin');
      var corps = [
        'Nom : ' + (d.get('nom') || ''),
        'Structure : ' + (d.get('structure') || ''),
        'Courriel : ' + (d.get('email') || ''),
        'Téléphone : ' + (d.get('telephone') || ''),
        'Besoin : ' + (besoins.length ? besoins.join(', ') : 'non précisé'),
        'Budget envisagé : ' + (d.get('budget') || 'non précisé'),
        'Délai : ' + (d.get('delai') || 'non précisé'),
        '',
        'Projet :',
        (d.get('message') || '')
      ].join('\n');

      window.location.href = 'mailto:' + form.getAttribute('data-mailto')
        + '?subject=' + encodeURIComponent('Demande de devis — ' + (d.get('nom') || 'nouveau projet'))
        + '&body=' + encodeURIComponent(corps);
    });
  }

  /* --- Entree du back-office : cinq clics sur le logo ---
     Une porte discrete, pas une serrure. La serrure est ailleurs :
     Cloudflare Access garde /admin, et le Worker verifie la signature
     du jeton. Ce compteur ne protege rien et n'a pas a le faire - il
     evite seulement d'afficher un lien « Administration » dans le pied
     de page de chaque visiteur.

     Le compte vit dans sessionStorage, et non dans une variable. Un
     clic sur le logo mene a l'accueil : la page se recharge, et une
     variable serait perdue a chaque fois - le cinquieme clic ne
     serait jamais atteint. Un visiteur ordinaire clique une fois,
     arrive sur l'accueil, et ne voit aucune difference.

     L'ecoute porte sur « click » et non « pointerdown » : sur
     pointerdown, preventDefault n'arrete pas le lien, dont la
     navigation se declenche au click et ecrase la redirection. Mesure
     faite, pas supposee : le compteur montait bien jusqu'a cinq, mais
     la page partait vers l'accueil. */
  var logo = document.querySelector('.logo img') || document.querySelector('.logo');
  if (logo) {
    logo.addEventListener('click', function (e) {
      var n = 1;
      try {
        var brut = sessionStorage.getItem('gfc-porte');
        if (brut) {
          var d = JSON.parse(brut);
          if (Date.now() - d.t < 3000) n = d.n + 1;
        }
        sessionStorage.setItem('gfc-porte', JSON.stringify({ n: n, t: Date.now() }));
      } catch (err) {
        return;  /* navigation privee : la porte ne s'ouvre pas, tant pis */
      }
      if (n >= 5) {
        e.preventDefault();
        try { sessionStorage.removeItem('gfc-porte'); } catch (err2) {}
        window.location.href = '/admin';
      }
    });
  }
})();
