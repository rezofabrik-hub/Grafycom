/**
 * Back-office Grafycom — porte d'entree et API.
 *
 * QUI PEUT ENTRER
 * Cloudflare Access garde /admin/*. Laurent s'y connecte avec son compte
 * Cloudflare : aucun mot de passe a inventer ni a retenir.
 *
 * Il ne suffit PAS de verifier la presence de l'en-tete Cf-Access-Jwt-
 * Assertion : si l'application Access n'etait pas configuree, n'importe
 * qui pourrait envoyer cet en-tete a la main. On verifie donc la
 * signature du jeton contre les cles publiques de l'equipe, et son
 * champ aud contre celui de l'application.
 *
 * FERME PAR DEFAUT
 * Tant que ADMIN_TEAM et ADMIN_AUD ne sont pas renseignes, tout /admin/*
 * repond 403. Il n'existe donc aucun instant, meme entre le deploiement
 * et la configuration d'Access, ou le back-office serait ouvert.
 */

const CLES = { valeur: null, expire: 0 };

function b64url(s) {
  const base = s.replace(/-/g, "+").replace(/_/g, "/");
  const bin = atob(base + "=".repeat((4 - base.length % 4) % 4));
  return Uint8Array.from(bin, (c) => c.charCodeAt(0));
}

async function clesPubliques(team) {
  const maintenant = Date.now();
  if (CLES.valeur && CLES.expire > maintenant) return CLES.valeur;
  const r = await fetch(`https://${team}.cloudflareaccess.com/cdn-cgi/access/certs`);
  if (!r.ok) throw new Error(`cles Access injoignables (${r.status})`);
  const { keys } = await r.json();
  CLES.valeur = keys || [];
  CLES.expire = maintenant + 3600_000;
  return CLES.valeur;
}

/** Verifie le jeton Access. Renvoie l'adresse de l'utilisateur, ou null. */
export async function identite(request, env) {
  const team = (env.ADMIN_TEAM || "").trim();
  const aud = (env.ADMIN_AUD || "").trim();
  if (!team || !aud) return null;             // ferme par defaut

  const jeton = request.headers.get("Cf-Access-Jwt-Assertion");
  if (!jeton) return null;
  const [tete, charge, signature] = jeton.split(".");
  if (!tete || !charge || !signature) return null;

  let entete, corps;
  try {
    entete = JSON.parse(new TextDecoder().decode(b64url(tete)));
    corps = JSON.parse(new TextDecoder().decode(b64url(charge)));
  } catch { return null; }

  // L'audience doit etre celle de CETTE application, sinon un jeton
  // valable pour une autre application du compte ouvrirait celle-ci.
  const auds = Array.isArray(corps.aud) ? corps.aud : [corps.aud];
  if (!auds.includes(aud)) return null;

  const now = Math.floor(Date.now() / 1000);
  if (typeof corps.exp !== "number" || corps.exp < now) return null;
  if (typeof corps.nbf === "number" && corps.nbf > now + 60) return null;

  let cles;
  try { cles = await clesPubliques(team); } catch { return null; }
  const jwk = cles.find((k) => k.kid === entete.kid);
  if (!jwk) return null;

  let cle;
  try {
    cle = await crypto.subtle.importKey(
      "jwk", jwk,
      { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
      false, ["verify"],
    );
  } catch { return null; }

  const ok = await crypto.subtle.verify(
    "RSASSA-PKCS1-v1_5", cle, b64url(signature),
    new TextEncoder().encode(`${tete}.${charge}`),
  );
  if (!ok) return null;
  return corps.email || "inconnu";
}

const CANAUX = ["Instagram + Facebook", "Stories", "Fiche Google", "Blog", "DM"];
const STATUTS = ["propose", "valide", "refuse", "publie"];

function json(donnees, code = 200) {
  return new Response(JSON.stringify(donnees), {
    status: code,
    headers: { "Content-Type": "application/json; charset=utf-8",
               "Cache-Control": "no-store" },
  });
}

async function journalise(env, qui, quoi, cible) {
  await env.DB.prepare(
    "INSERT INTO journal (quand, qui, quoi, cible) VALUES (?, ?, ?, ?)"
  ).bind(new Date().toISOString(), qui, quoi, cible).run();
}

export async function api(request, env, url, qui) {
  const chemin = url.pathname.replace(/^\/admin\/api/, "") || "/";

  if (chemin === "/publications" && request.method === "GET") {
    const { results } = await env.DB.prepare(
      "SELECT * FROM publications ORDER BY jour, heure, rang"
    ).all();
    return json({ qui, canaux: CANAUX, publications: results || [] });
  }

  if (chemin === "/publication" && request.method === "POST") {
    let d;
    try { d = await request.json(); } catch { return json({ erreur: "format" }, 400); }
    const id = String(d.id || "").trim();
    if (!id) return json({ erreur: "id manquant" }, 400);

    const champs = [];
    const valeurs = [];
    if (d.statut !== undefined) {
      if (!STATUTS.includes(d.statut)) return json({ erreur: "statut inconnu" }, 400);
      champs.push("statut = ?"); valeurs.push(d.statut);
    }
    for (const c of ["texte", "hashtags", "note", "titre", "heure", "visuel", "lien"]) {
      if (d[c] !== undefined) { champs.push(`${c} = ?`); valeurs.push(String(d[c])); }
    }
    if (!champs.length) return json({ erreur: "rien a changer" }, 400);
    champs.push("maj = ?"); valeurs.push(new Date().toISOString());
    valeurs.push(id);

    const r = await env.DB.prepare(
      `UPDATE publications SET ${champs.join(", ")} WHERE id = ?`
    ).bind(...valeurs).run();
    if (!r.meta.changes) return json({ erreur: "publication introuvable" }, 404);

    await journalise(env, qui, d.statut ? `statut → ${d.statut}` : "texte modifié", id);
    const ligne = await env.DB.prepare(
      "SELECT * FROM publications WHERE id = ?").bind(id).first();
    return json({ publication: ligne });
  }

  if (chemin === "/journal" && request.method === "GET") {
    const { results } = await env.DB.prepare(
      "SELECT * FROM journal ORDER BY id DESC LIMIT 100").all();
    return json({ journal: results || [] });
  }

  return json({ erreur: "route inconnue" }, 404);
}
