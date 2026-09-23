/**
 * Worker Grafycom.
 *
 * Sert le site statique, et traite le formulaire de contact sur /api/contact.
 * Le message part par Resend. Ni la clé d'API ni les adresses ne figurent
 * dans le dépôt : ce sont des secrets Cloudflare, modifiables sans toucher
 * au code ni redéployer.
 *
 * Secrets attendus (Workers & Pages > Settings > Variables and Secrets) :
 *   RESEND_API_KEY   clé d'API Resend                        (obligatoire)
 *   CONTACT_TO       adresse qui reçoit les demandes          (obligatoire)
 *   CONTACT_FROM     expéditeur, sur un domaine vérifié chez Resend
 *                    (facultatif ; par défaut onboarding@resend.dev, qui ne
 *                     délivre qu'au titulaire du compte Resend)
 */

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

  if (!env.RESEND_API_KEY || !env.CONTACT_TO) {
    console.error("RESEND_API_KEY ou CONTACT_TO manquant");
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

  let reponse;
  try {
    reponse = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: env.CONTACT_FROM || "Grafycom <onboarding@resend.dev>",
        to: [env.CONTACT_TO],
        reply_to: email,
        subject: `Demande de devis — ${nom}`,
        text: texte,
        html,
      }),
    });
  } catch (e) {
    console.error("Resend injoignable", e);
    return redirection("/contact.html?erreur=envoi", origine);
  }

  if (!reponse.ok) {
    console.error("Resend a refusé l'envoi", reponse.status, await reponse.text());
    return redirection("/contact.html?erreur=envoi", origine);
  }

  return redirection("/merci.html", origine);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/contact") return contact(request, env);
    return env.ASSETS.fetch(request);
  },
};
