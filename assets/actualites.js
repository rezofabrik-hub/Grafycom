/* Grafycom — page Actualités
   Lit les publications de Sandra dans la base de l'Espace Pro (Supabase) et
   les affiche en cartes. La clé ci-dessous est la clé « publishable » du
   projet : publique par nature, faite pour le navigateur. Ce que l'on peut
   lire avec elle est borné par la base (RLS) : seulement les publications
   cochées « Site internet », programmées, et dont la date est arrivée.

   Tout le texte passe par textContent : aucune balise venue de la base
   n'est jamais interprétée. Seuls les liens http(s) sont recréés, élément
   par élément.

   En cas d'erreur (réseau, base indisponible, réponse inattendue), la page
   garde son message d'attente : rien ne casse. */
(function () {
  'use strict';

  var SUPABASE = 'https://jkydfgfuzhgtqbmuzitt.supabase.co';
  var CLE = 'sb_publishable_FGVzZsgo3HSNhRJzNJtOfg_19SV8KrI';
  var URL_API = SUPABASE + '/rest/v1/publications'
    + '?select=id,titre,texte,photos,publier_le'
    + '&partenaire_slug=eq.sandra&order=publier_le.desc&limit=20';

  var MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
    'août', 'septembre', 'octobre', 'novembre', 'décembre'];

  var cible = document.getElementById('actualites');
  if (!cible || !window.fetch) return;

  /* 2026-11-02T08:00:00+00:00 -> « 2 novembre 2026 », à l'heure de Perpignan. */
  function dateFr(iso) {
    var d = new Date(iso);
    if (isNaN(d.getTime())) return null;
    var j, m, a;
    try {
      var parties = new Intl.DateTimeFormat('fr-FR', {
        timeZone: 'Europe/Paris', day: 'numeric', month: 'numeric', year: 'numeric'
      }).formatToParts(d);
      parties.forEach(function (p) {
        if (p.type === 'day') j = +p.value;
        if (p.type === 'month') m = +p.value;
        if (p.type === 'year') a = +p.value;
      });
    } catch (e) { /* navigateur sans Intl complet : heure locale */ }
    if (!j || !m || !a) { j = d.getDate(); m = d.getMonth() + 1; a = d.getFullYear(); }
    return (j === 1 ? '1er' : String(j)) + ' ' + MOIS[m - 1] + ' ' + a;
  }

  /* Seules les photos du projet sont affichées : la politique de sécurité de
     la page bloquerait toute autre origine, autant ne pas afficher d'image
     cassée. */
  function urlPhoto(p) {
    var u = p && typeof p.url === 'string' ? p.url : '';
    return u.indexOf(SUPABASE + '/') === 0 ? u : null;
  }

  /* Texte -> noeuds : texte brut, et liens http(s) cliquables. Les sauts de
     ligne sont conservés par le CSS (white-space: pre-line). */
  var RE_LIEN = /https?:\/\/[^\s<>"]+/g;
  function remplirTexte(el, texte) {
    var dernier = 0, m;
    RE_LIEN.lastIndex = 0;
    while ((m = RE_LIEN.exec(texte)) !== null) {
      var brut = m[0];
      // La ponctuation qui suit un lien n'en fait pas partie.
      var fin = brut.replace(/[.,;:!?»)\]'’]+$/, '');
      // Une parenthèse fermante fait partie du lien si elle en ferme une.
      while (brut.length > fin.length && brut.charAt(fin.length) === ')'
             && (fin.split('(').length > fin.split(')').length)) {
        fin += ')';
      }
      var href = null;
      try {
        var u = new URL(fin);
        if (u.protocol === 'http:' || u.protocol === 'https:') href = u.href;
      } catch (e) { href = null; }
      if (!href) continue;
      el.appendChild(document.createTextNode(texte.slice(dernier, m.index)));
      var a = document.createElement('a');
      a.href = href;
      a.textContent = fin;
      a.target = '_blank';
      a.rel = 'noopener';
      el.appendChild(a);
      dernier = m.index + fin.length;
      RE_LIEN.lastIndex = dernier;
    }
    el.appendChild(document.createTextNode(texte.slice(dernier)));
  }

  function image(url, alt, classe) {
    var img = document.createElement('img');
    img.src = url;
    img.alt = alt;
    img.loading = 'lazy';
    img.decoding = 'async';
    if (classe) img.className = classe;
    // Une photo introuvable disparaît, plutôt qu'une icône d'image cassée.
    img.addEventListener('error', function () {
      var bloc = img.parentNode && img.parentNode.tagName === 'A' ? img.parentNode : img;
      if (bloc.parentNode) bloc.parentNode.removeChild(bloc);
    });
    return img;
  }

  function carte(pub) {
    var titre = typeof pub.titre === 'string' ? pub.titre.trim() : '';
    var texte = typeof pub.texte === 'string' ? pub.texte.trim() : '';
    var date = pub.publier_le ? dateFr(pub.publier_le) : null;
    var photos = (Array.isArray(pub.photos) ? pub.photos : []).map(urlPhoto)
      .filter(Boolean);
    if (!titre && !texte && !photos.length) return null;

    var art = document.createElement('article');
    art.className = 'actu';

    if (photos.length) {
      var fig = document.createElement('div');
      fig.className = 'actu-photos';
      var sujet = titre || ('Publication du ' + (date || 'studio'));
      fig.appendChild(image(photos[0],
        photos.length > 1 ? sujet + ' — photo 1 sur ' + photos.length : sujet,
        'actu-photo'));
      if (photos.length > 1) {
        var vignettes = document.createElement('div');
        vignettes.className = 'actu-vignettes';
        photos.slice(1).forEach(function (url, i) {
          var lien = document.createElement('a');
          lien.href = url;
          lien.target = '_blank';
          lien.rel = 'noopener';
          lien.appendChild(image(url,
            sujet + ' — photo ' + (i + 2) + ' sur ' + photos.length));
          vignettes.appendChild(lien);
        });
        fig.appendChild(vignettes);
      }
      art.appendChild(fig);
    }

    var corps = document.createElement('div');
    corps.className = 'actu-corps';
    if (date) {
      var p = document.createElement('p');
      p.className = 'date-article';
      var t = document.createElement('time');
      t.dateTime = pub.publier_le;
      t.textContent = date;
      p.appendChild(t);
      corps.appendChild(p);
    }
    if (titre) {
      var h = document.createElement('h2');
      h.textContent = titre;
      corps.appendChild(h);
    }
    if (texte) {
      var txt = document.createElement('p');
      txt.className = 'actu-texte';
      remplirTexte(txt, texte);
      corps.appendChild(txt);
    }
    art.appendChild(corps);
    return art;
  }

  var minuteur = null, controle = null;
  if (window.AbortController) {
    controle = new AbortController();
    minuteur = setTimeout(function () { controle.abort(); }, 10000);
  }

  fetch(URL_API, {
    headers: { apikey: CLE, Authorization: 'Bearer ' + CLE, Accept: 'application/json' },
    signal: controle ? controle.signal : undefined
  })
    .then(function (r) { return r.ok ? r.json() : []; })
    .then(function (liste) {
      if (!Array.isArray(liste)) return;
      var cartes = [];
      liste.forEach(function (pub) {
        try {
          var c = pub && carte(pub);
          if (c) cartes.push(c);
        } catch (e) { /* une publication mal formée ne bloque pas les autres */ }
      });
      if (!cartes.length) return;
      var flux = document.createElement('div');
      flux.className = 'actus-liste';
      cartes.forEach(function (c) { flux.appendChild(c); });
      cible.textContent = '';
      cible.appendChild(flux);
    })
    .catch(function () { /* message d'attente conservé */ })
    .then(function () { if (minuteur) clearTimeout(minuteur); });
})();
