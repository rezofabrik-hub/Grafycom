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

  if (!env.CONTACT_TO || !env.CONTACT_FROM || !(env.RESEND_API_KEY || env.EMAIL)) {
    console.error("aucun envoyeur disponible, ou CONTACT_TO / CONTACT_FROM manquant");
    return redirection("/contact.html?erreur=envoi", origine);
  }

  const besoins = d.getAll("besoin").filter(Boolean);
  const lignes = CHAMPS
    .map(([cle, libelle]) => [libelle, (d.get(cle) || "").trim()])
    .filter(([, v]) => v);
  lignes.push(["Besoin", besoins.length ? besoins.join(", ") : "non précisé"]);

  const texte =
    lignes.map(([l, v]) => `${l} : ${v}`).join("\n") +
    `\n\nProjet :\n${message}\n`;

  const html =
    "<table style=\"font:15px/1.6 system-ui,sans-serif;border-collapse:collapse\">" +
    lignes.map(([l, v]) =>
      `<tr><td style="padding:4px 14px 4px 0;color:#6d5a50">${echappe(l)}</td>` +
      `<td style="padding:4px 0"><strong>${echappe(v)}</strong></td></tr>`
    ).join("") +
    "</table>" +
    `<p style="font:15px/1.7 system-ui,sans-serif;margin-top:18px"><strong>Projet :</strong><br>` +
    `${echappe(message).replace(/\n/g, "<br>")}</p>`;

  try {
    // replyTo porte l'adresse du visiteur : Sandra repond directement
    // depuis sa boite, sans recopier quoi que ce soit. L'expediteur,
    // lui, reste le domaine - une adresse d'expedition empruntee au
    // visiteur serait rejetee par les controles anti-usurpation.
    const sujet = `Demande de devis — ${nom}`;

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
      });
      console.log("message envoyé par Resend", envoi && envoi.id);
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
