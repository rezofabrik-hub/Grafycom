/**
 * Worker Grafycom.
 *
 * Sert le site statique, et traite le formulaire de contact sur /api/contact.
 * Le message part par le service d'envoi de Cloudflare, par le lien EMAIL
 * declare dans wrangler.toml. Il n'y a donc aucune cle d'API a garder :
 * l'envoi est autorise par le lien lui-meme, pas par un secret.
 *
 * Pourquoi pas un prestataire exterieur : le formulaire ecrit toujours a la
 * meme adresse, celle de Sandra. Cloudflare facture l'envoi vers une
 * destination verifiee du compte a zero, sur toutes les offres. Un
 * fournisseur de moins a gerer, une cle de moins a renouveler.
 *
 * DEUX ENVOYEURS POSSIBLES, et le code choisit seul.
 *
 * 1. Resend, des que le secret RESEND_API_KEY existe sur le Worker.
 *    C'est la voie retenue : le compte existe deja, le domaine y est
 *    declare en eu-west-1, les messages sont signes DKIM, et l'envoi
 *    ne depend pas d'une destination verifiee - donc demain on peut
 *    aussi ecrire au client, pas seulement a Sandra.
 *    A preparer une fois : les 4 enregistrements DNS que Resend donne
 *    (DKIM sur resend._domainkey, SPF sur send., CNAME rsend), puis le
 *    secret dans les reglages du Worker. Le CNAME doit etre en DNS only.
 *
 * 2. Le lien EMAIL de Cloudflare, tant que ce secret n'existe pas.
 *    Il demande Email Routing actif sur grafycom.fr et CONTACT_TO
 *    verifiee comme destination du compte, faute de quoi l'envoi est
 *    refuse (E_SENDER_DOMAIN_NOT_AVAILABLE).
 *
 * Ce choix au vol evite un deploiement en deux temps : ajouter le secret
 * suffit a basculer, et le retirer suffit a revenir en arriere.
 *
 * Les deux adresses sont dans wrangler.toml : ce ne sont pas des secrets,
 * et les avoir sous les yeux vaut mieux que de les chercher dans une
 * interface.
 */

import { identite, api } from "./admin.js";
import { PAGE_ADMIN } from "./admin-page.js";

const CHAMPS = [
  ["nom", "Nom"],
  ["structure", "Structure"],
  ["email", "Courriel"],
  ["telephone", "Téléphone"],
  ["budget", "Budget envisagé"],
  ["delai", "Délai"],
];

function redirection(url, origine) {
  return Response.redirect(new URL(url, origine).toString(), 303);
}

function echappe(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]
  ));
}

/* ---------------------------------------------------------------------
 * LES PHOTOS JOINTES A LA DEMANDE
 *
 * Un visiteur qui demande un devis a presque toujours quelque chose a
 * montrer : sa vitrine actuelle, son ancienne carte, le mur ou l'enseigne
 * doit aller, le vehicule a marquer. Le decrire par ecrit prend dix
 * lignes et reste flou ; la photo repond en une seconde. C'est la raison
 * du champ, et elle vaut pour le devis autant que pour le visiteur :
 * une demande illustree se chiffre du premier coup.
 *
 * Les limites ci-dessous ne sont pas des precautions de principe.
 * Resend refuse un message de plus de 40 Mo, et une piece jointe voyage
 * en base64, ce qui l'alourdit d'un tiers : 10 Mo de fichiers font
 * environ 13,4 Mo dans l'appel. Large, et tenable dans la memoire du
 * Worker.
 *
 * En pratique on n'y arrive jamais, parce que le navigateur reduit les
 * photos avant de les envoyer (voir assets/site.js). Ces limites servent
 * au cas sans JavaScript, ou le fichier part tel qu'il sort du telephone.
 * ------------------------------------------------------------------- */
const PHOTOS_MAX = 4;
const PHOTO_OCTETS_MAX = 5 * 1024 * 1024;
const PHOTOS_OCTETS_MAX = 10 * 1024 * 1024;

/**
 * Reconnait un fichier a ses premiers octets, et non au type que le
 * navigateur declare.
 *
 * Le type declare se change en une ligne : il dit ce que l'expediteur
 * veut bien dire. La signature, elle, est dans le fichier. Un
 * executable renomme en .jpg est refuse ici, alors qu'il passerait
 * n'importe quel controle d'extension - et c'est la boite de Sandra
 * qui est au bout.
 *
 * Renvoie { mime, ext }, ou null si rien n'est reconnu.
 */
function signature(o) {
  if (o.length < 12) return null;
  const txt = (d, f) => String.fromCharCode.apply(null, o.subarray(d, f));
  if (o[0] === 0xff && o[1] === 0xd8 && o[2] === 0xff) return { mime: "image/jpeg", ext: "jpg" };
  if (o[0] === 0x89 && txt(1, 4) === "PNG") return { mime: "image/png", ext: "png" };
  if (txt(0, 3) === "GIF") return { mime: "image/gif", ext: "gif" };
  if (txt(0, 4) === "%PDF") return { mime: "application/pdf", ext: "pdf" };
  if (txt(0, 4) === "RIFF" && txt(8, 12) === "WEBP") return { mime: "image/webp", ext: "webp" };
  // HEIC et HEIF : conteneur ISO-BMFF, « ftyp » en position 4 puis la
  // marque du profil. C'est le format par defaut des iPhone, et le
  // refuser reviendrait a refuser les photos d'un visiteur sur deux.
  if (txt(4, 8) === "ftyp") {
    const marque = txt(8, 12);
    if (/^(heic|heix|hevc|heim|heis|hevm|hevs|mif1|msf1)$/.test(marque)) {
      const heif = marque === "mif1" || marque === "msf1";
      return { mime: heif ? "image/heif" : "image/heic", ext: heif ? "heif" : "heic" };
    }
  }
  return null;
}

/**
 * Un nom de fichier presentable - reconstruit, et non nettoye.
 *
 * L'extension vient de la signature, jamais du nom : c'est la seule
 * facon qu'un fichier arrive dans la boite de Sandra sous son vrai
 * type. Les accents partent parce que les clients de messagerie les
 * rendent encore de travers, et le chemin eventuel est coupe net.
 */
function nomPropre(brut, ext, rang) {
  let n = String(brut || "").split(/[\\/]/).pop();
  n = n.replace(/\.[^.]*$/, "");
  n = n.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  n = n.replace(/[^A-Za-z0-9 ._-]+/g, "-").replace(/[-\s]+/g, "-").replace(/^[-.]+|[-.]+$/g, "");
  if (n.length > 48) n = n.slice(0, 48);
  if (!n) n = "photo-" + rang;
  return n + "." + ext;
}

/** base64 par tranches : fromCharCode sur 10 Mo d'un coup fait deborder la pile. */
function base64(o) {
  let s = "";
  const pas = 0x8000;
  for (let i = 0; i < o.length; i += pas) {
    s += String.fromCharCode.apply(null, o.subarray(i, i + pas));
  }
  return btoa(s);
}

function poidsLisible(n) {
  return n >= 1048576
    ? (n / 1048576).toFixed(1).replace(".", ",") + " Mo"
    : Math.max(1, Math.round(n / 1024)) + " ko";
}

/**
 * Lit les photos du formulaire et les prepare pour l'envoi.
 *
 * Renvoie { pieces } ou { erreur } ; l'erreur est le code que la page
 * contact sait traduire en une phrase utile - « quatre au maximum »,
 * et non « erreur 400 ».
 */
async function photosJointes(d) {
  const bruts = d.getAll("photos")
    .filter((f) => f && typeof f === "object" && typeof f.arrayBuffer === "function" && f.size > 0);
  if (!bruts.length) return { pieces: [] };
  if (bruts.length > PHOTOS_MAX) return { erreur: "photos-nombre" };

  let total = 0;
  const pieces = [];
  for (let i = 0; i < bruts.length; i++) {
    const f = bruts[i];
    if (f.size > PHOTO_OCTETS_MAX) return { erreur: "photos-poids" };
    total += f.size;
    if (total > PHOTOS_OCTETS_MAX) return { erreur: "photos-poids" };

    const octets = new Uint8Array(await f.arrayBuffer());
    const sig = signature(octets);
    if (!sig) return { erreur: "photos-type" };

    pieces.push({
      filename: nomPropre(f.name, sig.ext, i + 1),
      content_type: sig.mime,
      content: base64(octets),
      octets: f.size,
    });
  }
  return { pieces };
}

/**
 * Envoi par Resend.
 *
 * Choisi quand le secret RESEND_API_KEY existe sur le Worker. Le domaine
 * grafycom.fr y est declare en eu-west-1 : les messages sont signes DKIM
 * et partent d'Europe.
 *
 * L'API REST attend reply_to en minuscules avec un tiret bas. La forme
 * replyTo n'existe que dans la bibliotheque Node, qui la convertit ;
 * ici on parle a l'API directement, donc reply_to.
 */
async function envoiResend(env, m) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: `Grafycom <${env.CONTACT_FROM}>`,
      to: [env.CONTACT_TO],
      reply_to: m.replyTo,
      subject: m.subject,
      text: m.text,
      html: m.html,
      // Omis quand il n'y en a pas : un tableau vide est un tableau,
      // et autant ne pas faire parler l'API de ce qui n'existe pas.
      ...(m.attachments && m.attachments.length ? { attachments: m.attachments } : {}),
    }),
  });
  // Resend repond en JSON meme en erreur. On remonte le corps tel quel :
  // c'est lui qui dit « domaine non verifie » ou « cle invalide », et sans
  // lui on cherche a l'aveugle.
  const corps = await r.text();
  if (!r.ok) throw new Error(`Resend ${r.status} : ${corps}`);
  try { return JSON.parse(corps); } catch { return {}; }
}

async function contact(request, env) {
  const origine = new URL(request.url).origin;

  if (request.method !== "POST") {
    return new Response("Méthode non autorisée", { status: 405, headers: { Allow: "POST" } });
  }

  let d;
  try {
    d = await request.formData();
  } catch {
    return redirection("/contact.html?erreur=format", origine);
  }

  // Pot de miel : rempli, c'est un robot. On répond comme si tout allait bien,
  // pour ne pas lui apprendre qu'il a été repéré.
  if ((d.get("botcheck") || "").trim() !== "") {
    return redirection("/merci.html", origine);
  }

  const nom = (d.get("nom") || "").trim();
  const email = (d.get("email") || "").trim();
  const message = (d.get("message") || "").trim();
  if (!nom || !email || !message || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return redirection("/contact.html?erreur=champs", origine);
  }
  if (message.length > 8000 || nom.length > 200) {
    return redirection("/contact.html?erreur=champs", origine);
  }

  // Les photos avant l'envoyeur : un fichier refuse doit etre dit au
  // visiteur, pas decouvert apres qu'on a essaye d'ecrire.
  const lot = await photosJointes(d);
  if (lot.erreur) return redirection("/contact.html?erreur=" + lot.erreur, origine);

  if (!env.CONTACT_TO || !env.CONTACT_FROM || !(env.RESEND_API_KEY || env.EMAIL)) {
    console.error("aucun envoyeur disponible, ou CONTACT_TO / CONTACT_FROM manquant");
    return redirection("/contact.html?erreur=envoi", origine);
  }

  const besoins = d.getAll("besoin").filter(Boolean);
  const lignes = CHAMPS
    .map(([cle, libelle]) => [libelle, (d.get(cle) || "").trim()])
    .filter(([, v]) => v);
  lignes.push(["Besoin", besoins.length ? besoins.join(", ") : "non précisé"]);

  /* Les pieces jointes ne partent que par Resend. Le lien EMAIL de
     Cloudflare prend un message simple, pas un envoi MIME multipart :
     fabriquer les frontieres a la main pour un chemin de secours qui
     ne sert pas serait du code jamais exerce, donc du code qui ne
     marche pas le jour ou il sert.
  
     Alors le message part quand meme - perdre une demande serait pire
     que perdre les photos - mais il le dit, avec la liste des fichiers,
     pour que Sandra puisse les redemander en repondant. Le visiteur
     l'apprend par elle, et non par un silence. */
  const jointes = Boolean(env.RESEND_API_KEY);
  const pieces = lot.pieces;
  let notePJ = "", notePJhtml = "";
  if (pieces.length) {
    const liste = pieces.map((p) => `${p.filename} (${poidsLisible(p.octets)})`);
    const titre = pieces.length > 1
      ? `${pieces.length} photos jointes`
      : "1 photo jointe";
    if (jointes) {
      notePJ = `\n${titre} :\n` + liste.map((l) => `- ${l}`).join("\n") + "\n";
      notePJhtml =
        `<p style="font:15px/1.7 system-ui,sans-serif;margin-top:18px">` +
        `<strong>${echappe(titre)} :</strong><br>` +
        liste.map((l) => echappe(l)).join("<br>") + "</p>";
    } else {
      const alerte = "Le visiteur a joint " + (pieces.length > 1
        ? pieces.length + " fichiers qui n'ont pas pu etre transmis"
        : "un fichier qui n'a pas pu etre transmis") +
        " (l'envoi est passe par le lien de secours). A redemander en repondant a ce message :";
      notePJ = `\n${alerte}\n` + liste.map((l) => `- ${l}`).join("\n") + "\n";
      notePJhtml =
        `<p style="font:15px/1.7 system-ui,sans-serif;margin-top:18px;` +
        `background:#fdecea;border-left:4px solid #f2585c;padding:12px 14px">` +
        `<strong>${echappe(alerte)}</strong><br>` +
        liste.map((l) => echappe(l)).join("<br>") + "</p>";
    }
  }

  const texte =
    lignes.map(([l, v]) => `${l} : ${v}`).join("\n") +
    `\n\nProjet :\n${message}\n` + notePJ;

  const html =
    "<table style=\"font:15px/1.6 system-ui,sans-serif;border-collapse:collapse\">" +
    lignes.map(([l, v]) =>
      `<tr><td style="padding:4px 14px 4px 0;color:#6d5a50">${echappe(l)}</td>` +
      `<td style="padding:4px 0"><strong>${echappe(v)}</strong></td></tr>`
    ).join("") +
    "</table>" +
    `<p style="font:15px/1.7 system-ui,sans-serif;margin-top:18px"><strong>Projet :</strong><br>` +
    `${echappe(message).replace(/\n/g, "<br>")}</p>` +
    notePJhtml;

  try {
    // replyTo porte l'adresse du visiteur : Sandra repond directement
    // depuis sa boite, sans recopier quoi que ce soit. L'expediteur,
    // lui, reste le domaine - une adresse d'expedition empruntee au
    // visiteur serait rejetee par les controles anti-usurpation.
    // Le compte des photos dans l'objet : Sandra voit depuis sa liste
    // de messages qu'il y a de quoi regarder avant de repondre.
    const sujet = `Demande de devis — ${nom}` +
      (jointes && pieces.length ? ` (${pieces.length} photo${pieces.length > 1 ? "s" : ""})` : "");

    // Deux chemins, et le choix se fait tout seul. Tant que le secret
    // RESEND_API_KEY n'existe pas sur le Worker, rien ne change : on
    // reste sur le lien Cloudflare. Le jour ou Laurent ajoute le secret,
    // l'envoi bascule sur Resend sans redeploiement.
    if (env.RESEND_API_KEY) {
      const envoi = await envoiResend(env, {
        replyTo: email,
        subject: sujet,
        text: texte,
        html,
        attachments: pieces.map(({ filename, content_type, content }) => (
          { filename, content_type, content }
        )),
      });
      console.log("message envoyé par Resend", envoi && envoi.id,
                  pieces.length ? pieces.length + " pièce(s) jointe(s)" : "sans pièce jointe");
    } else {
      const envoi = await env.EMAIL.send({
        from: { email: env.CONTACT_FROM, name: "Grafycom" },
        to: env.CONTACT_TO,
        replyTo: { email, name: nom },
        subject: sujet,
        text: texte,
        html,
      });
      console.log("message envoyé par Cloudflare", envoi && envoi.messageId);
      if (pieces.length) {
        console.error("pièces jointes non transmises : le lien EMAIL de " +
                      "Cloudflare ne porte pas de fichier. Poser RESEND_API_KEY.");
      }
    }
  } catch (e) {
    // Les causes previsibles : domaine d'expedition pas encore integre
    // au service, ou destinataire pas verifie. Le message dit laquelle.
    console.error("envoi refusé", e && e.message ? e.message : e);
    return redirection("/contact.html?erreur=envoi", origine);
  }

  return redirection("/merci.html", origine);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/contact") return contact(request, env);

    // Le back-office. La page n'est pas un fichier du site : elle
    // n'existe que servie ici, apres verification. Un fichier dans
    // dist/ serait accessible a tous, garde ou pas.
    if (url.pathname === "/admin" || url.pathname.startsWith("/admin/")) {
      const qui = await identite(request, env);
      if (!qui) {
        return new Response(
          "Back-office réservé.\n\nSi vous êtes Laurent et que vous voyez ce " +
          "message, l'application Cloudflare Access n'est pas encore " +
          "configurée, ou ADMIN_TEAM / ADMIN_AUD ne sont pas renseignés " +
          "dans wrangler.toml.\n",
          { status: 403, headers: { "Content-Type": "text/plain; charset=utf-8" } });
      }
      if (url.pathname.startsWith("/admin/api")) return api(request, env, url, qui);
      return new Response(PAGE_ADMIN, {
        headers: { "Content-Type": "text/html; charset=utf-8",
                   "Cache-Control": "no-store",
                   "X-Robots-Tag": "noindex, nofollow" },
      });
    }

    // La racine n'a pas de fichier a son nom. wrangler.toml demande
    // html_handling = "none" pour que /prestations.html soit servi tel
    // quel, sans redirection : en contrepartie, plus rien ne devine
    // qu'une adresse qui finit par / designe son index.html. On le dit
    // ici, pour la seule adresse concernee.
    if (url.pathname === "/") {
      return env.ASSETS.fetch(new Request(new URL("/index.html", url), request));
    }
    return env.ASSETS.fetch(request);
  },
};
