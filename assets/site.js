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
      format: "Le formulaire n'a pas été transmis correctement. Réessayez, ou écrivez-moi directement.",
      'photos-nombre': "Quatre photos au maximum. Gardez les plus parlantes : je vous demanderai le reste si besoin.",
      'photos-poids': "Les photos sont trop lourdes pour partir par courriel (5 Mo par fichier, 10 Mo en tout). Envoyez-en moins, ou écrivez-moi et je vous donnerai un lien de dépôt.",
      'photos-type': "Un des fichiers n'est ni une image ni un PDF — ou son contenu ne correspond pas à son nom. Seuls les formats JPEG, PNG, WebP, HEIC et PDF sont acceptés."
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

  /* --- Repli du formulaire de contact ---
     Depuis le 31 octobre 2026, contact.html porte un attribut action et le
     message part par le Worker : ce bloc ne s'exécute donc plus sur le site
     tel qu'il est publié, et c'est voulu. Il reste le filet de sécurité du
     jour où FORMULAIRE_ACTIF repasserait à False — une panne de l'envoyeur,
     une migration — où le formulaire doit continuer à transmettre quelque
     chose plutôt que rien. Le test porte sur l'attribut, pas sur une
     constante : le code lit la page qu'il a sous les yeux. */
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


  /* --- Les photos jointes à la demande de devis ---

     Le champ n'est qu'un <input type="file"> : sans ce bloc, il fonctionne
     déjà, et le Worker reçoit les fichiers tels qu'ils sortent du téléphone.
     Ce qui est ajouté ici tient à deux choses.

     1. LE POIDS. Une photo d'iPhone pèse 3 à 5 Mo. Quatre font 16 Mo, soit
        au-delà de ce que le courriel accepte, et plusieurs minutes d'attente
        en 4G au bord d'une route — exactement la situation du commerçant qui
        photographie sa vitrine. Réduite à 2000 px de côté en JPEG 82, la même
        photo pèse 300 à 500 ko et reste bien plus détaillée que ce qu'il faut
        pour juger d'une enseigne. Le travail se fait dans le navigateur : rien
        n'est téléversé pour être redimensionné ensuite.

     2. CE QU'ON VOIT AVANT D'ENVOYER. Le champ natif affiche « 3 fichiers »
        et rien d'autre. Ici chaque photo apparaît en vignette, avec son poids
        réel après réduction, et se retire d'un clic. On peut aussi les
        déposer sur la zone.

     La liste de référence est le tableau `choisis`, pas l'input : une FileList
     ne se modifie pas, donc retirer une photo demande de réécrire l'input à
     partir du tableau. Quand le navigateur ne le permet pas, l'envoi passe
     par fetch, qui n'a pas cette contrainte. */
  var zone = document.querySelector('.depot');
  var entree = document.getElementById('photos');
  var liste = document.querySelector('.photos-liste');
  var devis = document.querySelector('form.devis');

  if (zone && entree && liste && devis && window.FileReader && window.Promise) {
    var NOMBRE_MAX = 4;             // doit suivre PHOTOS_MAX dans src/index.js
    var FICHIER_MAX = 5 * 1024 * 1024;
    var TOTAL_MAX = 10 * 1024 * 1024;
    var COTE_MAX = 2000;            // px, sur le plus grand côté
    var QUALITE = 0.82;
    var SEUIL_JPEG = 500 * 1024;    // en dessous, réduire n'apporte rien
    var SEUIL_PNG = 1500 * 1024;    // au-delà, un PNG est une photo, pas un logo

    var choisis = [];
    var sansEcriture = false;       // vrai si l'input ne se réécrit pas
    var note = document.createElement('p');
    note.className = 'photos-note';
    note.setAttribute('role', 'status');
    note.hidden = true;
    liste.parentNode.insertBefore(note, liste.nextSibling);

    function dire(texte, refus) {
      note.textContent = texte || '';
      note.hidden = !texte;
      note.classList.toggle('refus', Boolean(refus));
    }

    function poids(n) {
      return n >= 1048576
        ? (n / 1048576).toFixed(1).replace('.', ',') + ' Mo'
        : Math.max(1, Math.round(n / 1024)) + ' ko';
    }

    function total() {
      return choisis.reduce(function (n, f) { return n + f.size; }, 0);
    }

    /* Décoder une image sans passer par blob:. La CSP du site n'autorise que
       'self' et data: en img-src, et URL.createObjectURL produit un blob: —
       une <img> construite ainsi serait bloquée sans message d'erreur.
       createImageBitmap lit le fichier directement et ne concerne pas la CSP ;
       le repli encode en data:, qui est autorisé. */
    function decoder(f) {
      return new Promise(function (ok, non) {
        function parDataURL() {
          var lecteur = new FileReader();
          lecteur.onerror = non;
          lecteur.onload = function () {
            var img = new Image();
            img.onload = function () { ok(img); };
            img.onerror = non;
            img.src = lecteur.result;
          };
          try { lecteur.readAsDataURL(f); } catch (e) { non(); }
        }
        if (typeof createImageBitmap !== 'function') { parDataURL(); return; }
        /* imageOrientation : sans elle, une photo prise à la verticale
           ressort couchée — l'orientation vit dans l'EXIF, que la
           décompression ignore par défaut. L'option est récente, d'où le
           deuxième essai sans elle. */
        createImageBitmap(f, { imageOrientation: 'from-image' }).then(ok, function () {
          createImageBitmap(f).then(ok, parDataURL);
        });
      });
    }

    function surCanevas(src, cote) {
      var k = Math.min(1, cote / Math.max(src.width, src.height));
      var c = document.createElement('canvas');
      c.width = Math.max(1, Math.round(src.width * k));
      c.height = Math.max(1, Math.round(src.height * k));
      var ctx = c.getContext('2d');
      // Fond blanc d'abord : un PNG transparent aplati en JPEG donnerait
      // du noir là où il n'y avait rien.
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, c.width, c.height);
      ctx.drawImage(src, 0, 0, c.width, c.height);
      return c;
    }

    function aReduire(f) {
      if (f.type === 'application/pdf') return false;
      if (/^image\/(jpeg|pjpeg)$/.test(f.type)) return f.size > SEUIL_JPEG;
      // Un PNG ou un WebP léger est presque toujours un logo : l'aplatir en
      // JPEG lui coûterait sa transparence sans rien gagner. Au-delà du
      // seuil c'est une photo ou une capture d'écran.
      if (/^image\/(png|webp)$/.test(f.type)) return f.size > SEUIL_PNG;
      // HEIC, HEIF, type non déclaré : aucun navigateur ne garantit de
      // savoir les décoder. Mieux vaut les laisser partir entiers que les
      // perdre — le Worker les accepte.
      return false;
    }

    function reduire(f) {
      if (!aReduire(f) || !document.createElement('canvas').toBlob) {
        return Promise.resolve(f);
      }
      return decoder(f).then(function (src) {
        var c = surCanevas(src, COTE_MAX);
        if (src.close) src.close();
        return new Promise(function (ok) {
          c.toBlob(function (b) {
            // Une « réduction » qui alourdit n'est pas une réduction.
            if (!b || b.size >= f.size) { ok(f); return; }
            var nom = f.name.replace(/\.[^.]*$/, '') + '.jpg';
            try { ok(new File([b], nom, { type: 'image/jpeg' })); }
            catch (e) { b.nomVoulu = nom; ok(b); }
          }, 'image/jpeg', QUALITE);
        });
      }, function () { return f; });  // indécodable : l'original part tel quel
    }

    function nomDe(f) { return f.name || f.nomVoulu || 'photo.jpg'; }

    /* La vignette, et le carré gris si le navigateur ne sait pas lire le
       format. Le cas existe : un HEIC d'iPhone ne se décode que dans Safari.
       Le fichier part quand même — le Worker l'accepte — mais une image vide
       laisserait croire qu'il s'est passé quelque chose de travers. */
    function vignette(f, img) {
      decoder(f).then(function (src) {
        var c = surCanevas(src, 120);
        if (src.close) src.close();
        try { img.src = c.toDataURL('image/jpeg', 0.7); } catch (e) { sansApercu(img); }
      }, function () { sansApercu(img); });
    }

    function sansApercu(img) {
      if (!img.parentNode) return;
      var bloc = document.createElement('span');
      bloc.className = 'vignette-pdf';
      bloc.innerHTML = '<i class="fa-regular fa-image" aria-hidden="true"></i>';
      img.parentNode.replaceChild(bloc, img);
    }

    /* Réécrire l'input à partir de `choisis`, pour que l'envoi natif du
       formulaire porte exactement ce que le visiteur voit. Si le navigateur
       refuse, on le note une fois et l'envoi basculera sur fetch. */
    function synchroniser() {
      if (sansEcriture || typeof DataTransfer !== 'function') { sansEcriture = true; return; }
      try {
        var dt = new DataTransfer();
        choisis.forEach(function (f) {
          dt.items.add(f instanceof File ? f : new File([f], nomDe(f), { type: f.type }));
        });
        entree.files = dt.files;
        if (entree.files.length !== choisis.length) sansEcriture = true;
      } catch (e) {
        sansEcriture = true;
      }
    }

    function afficher() {
      liste.textContent = '';
      liste.hidden = choisis.length === 0;
      choisis.forEach(function (f, rang) {
        var li = document.createElement('li');
        var apercu;
        if (f.type === 'application/pdf') {
          apercu = document.createElement('span');
          apercu.className = 'vignette-pdf';
          apercu.innerHTML = '<i class="fa-solid fa-file-pdf" aria-hidden="true"></i>';
        } else {
          apercu = document.createElement('img');
          apercu.alt = '';
          vignette(f, apercu);
        }
        var nom = document.createElement('span');
        nom.className = 'nom';
        nom.textContent = nomDe(f);
        nom.title = nomDe(f);
        var p = document.createElement('span');
        p.className = 'poids';
        p.textContent = poids(f.size);
        var retirer = document.createElement('button');
        retirer.type = 'button';
        retirer.setAttribute('aria-label', 'Retirer ' + nomDe(f));
        retirer.innerHTML = '<i class="fa-solid fa-xmark" aria-hidden="true"></i>';
        retirer.addEventListener('click', function () {
          choisis.splice(rang, 1);
          conclure(choisis.length
            ? choisis.length + (choisis.length > 1 ? ' photos' : ' photo') + ' — ' + poids(total()) + ' en tout.'
            : 'Photo retirée.');
        });
        li.appendChild(apercu);
        li.appendChild(nom);
        li.appendChild(p);
        li.appendChild(retirer);
        liste.appendChild(li);
      });
    }

    /* Toute sortie d'accepter() passe par ici, et ce n'est pas une
       coquetterie d'écriture. Le sélecteur de fichiers a DÉJÀ remplacé le
       contenu de l'input avant que ce code s'exécute : si l'on repart sans
       réécrire l'input, les photos déjà prêtes disparaissent de l'envoi tout
       en restant affichées à l'écran. Le visiteur voit trois vignettes et
       Sandra reçoit un fichier.

       Le cas se produit à chaque refus — doublon, fichier trop lourd,
       mauvais format — c'est-à-dire précisément quand le visiteur a besoin
       qu'on ne lui perde rien. Trouvé par le test du navigateur, pas à la
       lecture. */
    function conclure(texte, refus) {
      synchroniser();
      afficher();
      dire(texte, refus);
    }

    function accepter(fichiers) {
      var candidats = Array.prototype.slice.call(fichiers).filter(function (f) {
        return f && f.size > 0 && (/^image\//.test(f.type) || f.type === 'application/pdf' || !f.type);
      });
      if (!candidats.length) {
        conclure('Seules les images et les PDF peuvent être joints.', true);
        return;
      }

      /* Le dédoublonnage compare au FICHIER CHOISI, jamais à celui qui est
         déjà dans la liste : la réduction a changé sa taille, et parfois son
         nom. D'où la signature de l'original gardée sur chaque entrée. */
      var deja = choisis.map(function (f) { return f.cleOrigine; });
      candidats = candidats.filter(function (f) {
        return deja.indexOf((f.name || '') + '|' + f.size) === -1;
      });
      if (!candidats.length) { conclure('Cette photo est déjà dans la liste.'); return; }

      var refuses = [];
      var place = NOMBRE_MAX - choisis.length;
      if (candidats.length > place) {
        refuses.push('quatre photos au maximum');
        candidats = candidats.slice(0, Math.max(0, place));
      }
      candidats = candidats.filter(function (f) {
        // 20 Mo : même réduit de quatre cinquièmes, un tel fichier ne
        // passerait pas. Autant le dire avant de faire travailler le
        // téléphone pour rien.
        if (f.size > FICHIER_MAX * 4) {
          refuses.push('« ' + f.name + ' » dépasse 20 Mo');
          return false;
        }
        return true;
      });
      if (!candidats.length) {
        conclure('Rien n\u2019a été ajouté : ' + refuses.join(', ') + '.', true);
        return;
      }

      dire(candidats.length > 1 ? 'Préparation des photos…' : 'Préparation de la photo…');
      Promise.all(candidats.map(function (f) {
        var cle = (f.name || '') + '|' + f.size;
        return reduire(f).then(function (pret) {
          try { pret.cleOrigine = cle; } catch (e) {}
          return pret;
        });
      })).then(function (prets) {
        prets.forEach(function (f) {
          if (f.size > FICHIER_MAX) { refuses.push('« ' + nomDe(f) + ' » reste au-dessus de 5 Mo'); return; }
          if (total() + f.size > TOTAL_MAX) { refuses.push('« ' + nomDe(f) + ' » ferait dépasser 10 Mo en tout'); return; }
          choisis.push(f);
        });
        if (refuses.length) {
          conclure('Non retenu : ' + refuses.join(', ') + '.', true);
        } else {
          conclure(choisis.length + (choisis.length > 1 ? ' photos prêtes à partir — ' : ' photo prête à partir — ')
                   + poids(total()) + ' en tout.');
        }
      }, function () {
        conclure("Ces photos n'ont pas pu être préparées. Réessayez, ou écrivez-moi directement.", true);
      });
    }

    entree.addEventListener('change', function () {
      accepter(entree.files);
      // Remis à zéro pour que choisir deux fois le même fichier déclenche
      // bien un deuxième « change ». La liste de référence est `choisis`.
      if (sansEcriture) { try { entree.value = ''; } catch (e) {} }
    });

    ['dragenter', 'dragover'].forEach(function (nom) {
      zone.addEventListener(nom, function (e) { e.preventDefault(); zone.classList.add('survol'); });
    });
    ['dragleave', 'dragend'].forEach(function (nom) {
      zone.addEventListener(nom, function () { zone.classList.remove('survol'); });
    });
    zone.addEventListener('drop', function (e) {
      e.preventDefault();
      zone.classList.remove('survol');
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length) {
        accepter(e.dataTransfer.files);
      }
    });

    /* Envoi par fetch, et seulement si l'input n'a pas pu être réécrit :
       sinon le formulaire part tout seul, en POST ordinaire, exactement
       comme sans JavaScript. Un chemin de moins à maintenir. */
    devis.addEventListener('submit', function (e) {
      if (!devis.getAttribute('action') || !sansEcriture || !choisis.length) return;
      if (typeof window.fetch !== 'function' || typeof FormData !== 'function') return;
      e.preventDefault();
      if (!devis.reportValidity()) return;

      var bouton = devis.querySelector('button[type="submit"]');
      var avant = bouton ? bouton.innerHTML : '';
      if (bouton) { bouton.disabled = true; bouton.textContent = 'Envoi en cours…'; }

      var donnees = new FormData(devis);
      donnees.delete('photos');
      choisis.forEach(function (f) { donnees.append('photos', f, nomDe(f)); });

      fetch(devis.getAttribute('action'), { method: 'POST', body: donnees })
        .then(function (r) { window.location.assign(r.url || '/merci.html'); })
        .catch(function () {
          if (bouton) { bouton.disabled = false; bouton.innerHTML = avant; }
          dire("L'envoi n'a pas abouti. Réessayez, ou écrivez-moi directement.", true);
        });
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
