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

  // Creer une publication a soi. L'agent propose un cycle ; Laurent
  // ajoute ce qu'il veut, quand il veut, sans passer par un cycle.
  if (chemin === "/publication" && request.method === "PUT") {
    let d;
    try { d = await request.json(); } catch { return json({ erreur: "format" }, 400); }
    const jour = String(d.jour || "").trim();
    const titre = String(d.titre || "").trim();
    const canal = String(d.canal || "").trim();
    if (!/^\d{4}-\d{2}-\d{2}$/.test(jour)) return json({ erreur: "date attendue au format AAAA-MM-JJ" }, 400);
    if (!titre) return json({ erreur: "il faut un titre" }, 400);
    if (!CANAUX.includes(canal)) return json({ erreur: "canal inconnu" }, 400);

    // Un identifiant tire du hasard, et non du contenu : deux
    // publications du meme jour sur le meme canal sont legitimes, et un
    // identifiant calcule sur le titre les ferait se recouvrir.
    const id = crypto.randomUUID().replace(/-/g, "").slice(0, 16);
    await env.DB.prepare(
      "INSERT INTO publications (id,cycle,jour,heure,canal,titre,texte,hashtags,"
      + "visuel,note,statut,rang,maj) VALUES (?,?,?,?,?,?,?,?,?,?,'propose',999,?)"
    ).bind(id, String(d.cycle || "ajouts"), jour, String(d.heure || ""), canal, titre,
           String(d.texte || ""), String(d.hashtags || ""), String(d.visuel || ""),
           String(d.note || ""), new Date().toISOString()).run();
    await journalise(env, qui, "publication créée", id);
    const ligne = await env.DB.prepare(
      "SELECT * FROM publications WHERE id = ?").bind(id).first();
    return json({ publication: ligne });
  }

  if (chemin === "/publication" && request.method === "DELETE") {
    let d;
    try { d = await request.json(); } catch { return json({ erreur: "format" }, 400); }
    const id = String(d.id || "").trim();
    if (!id) return json({ erreur: "id manquant" }, 400);
    // Les photos attachees partent avec : sans cela elles resteraient
    // dans le stockage sans que rien ne les montre ni ne les efface.
    if (env.FICHIERS) {
      const l = await env.FICHIERS.list({ prefix: `pub/${id}/` });
      for (const o of l.objects || []) await env.FICHIERS.delete(o.key);
    }
    const r = await env.DB.prepare(
      "DELETE FROM publications WHERE id = ?").bind(id).run();
    if (!r.meta.changes) return json({ erreur: "publication introuvable" }, 404);
    await journalise(env, qui, "publication supprimée", id);
    return json({ supprime: id });
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

  // --- Photos -------------------------------------------------------
  // Elles vivent dans R2, pas dans le depot : une photo de 3 Mo n'a rien
  // a faire dans un historique git, qui ne l'oublierait jamais.
  //
  // Elles ne sont pas servies publiquement. Laurent les telecharge d'ici
  // pour les deposer dans Meta Business Suite ; une photo client mise en
  // ligne par megarde, avant l'accord du client, serait difficile a
  // rattraper.
  if (chemin.startsWith("/photo")) {
    if (!env.FICHIERS) {
      return json({ erreur: "stockage non activé",
                    detail: "R2 n'est pas encore branché sur ce Worker." }, 503);
    }

    if (chemin === "/photos" && request.method === "GET") {
      const pub = url.searchParams.get("pub") || "";
      if (!pub) return json({ erreur: "publication manquante" }, 400);
      const l = await env.FICHIERS.list({ prefix: `pub/${pub}/` });
      return json({ photos: (l.objects || []).map((o) => ({
        cle: o.key, nom: o.key.split("/").pop(),
        taille: o.size, date: o.uploaded,
      })) });
    }

    if (chemin === "/photo" && request.method === "PUT") {
      const pub = url.searchParams.get("pub") || "";
      const nom = (url.searchParams.get("nom") || "").replace(/[^\w.\-]/g, "_");
      if (!pub || !nom) return json({ erreur: "publication ou nom manquant" }, 400);
      const type = request.headers.get("Content-Type") || "";
      if (!/^image\/(jpeg|png|webp|avif|gif)$/.test(type)) {
        return json({ erreur: "ce n'est pas une image" }, 415);
      }
      const taille = Number(request.headers.get("Content-Length") || 0);
      if (taille > 25 * 1024 * 1024) {
        return json({ erreur: "image trop lourde (25 Mo maximum)" }, 413);
      }
      const cle = `pub/${pub}/${Date.now()}-${nom}`;
      await env.FICHIERS.put(cle, request.body, {
        httpMetadata: { contentType: type },
      });
      await journalise(env, qui, "photo ajoutée", cle);
      return json({ cle, nom });
    }

    if (chemin === "/photo" && request.method === "GET") {
      const cle = url.searchParams.get("cle") || "";
      if (!cle.startsWith("pub/")) return json({ erreur: "clé invalide" }, 400);
      const o = await env.FICHIERS.get(cle);
      if (!o) return json({ erreur: "introuvable" }, 404);
      return new Response(o.body, {
        headers: {
          "Content-Type": o.httpMetadata?.contentType || "application/octet-stream",
          "Cache-Control": "private, max-age=300",
          "Content-Disposition": `inline; filename="${cle.split("/").pop()}"`,
        },
      });
    }

    if (chemin === "/photo" && request.method === "DELETE") {
      const cle = url.searchParams.get("cle") || "";
      if (!cle.startsWith("pub/")) return json({ erreur: "clé invalide" }, 400);
      await env.FICHIERS.delete(cle);
      await journalise(env, qui, "photo supprimée", cle);
      return json({ supprime: cle });
    }

    return json({ erreur: "route photo inconnue" }, 404);
  }

  if (chemin === "/journal" && request.method === "GET") {
    const { results } = await env.DB.prepare(
      "SELECT * FROM journal ORDER BY id DESC LIMIT 100").all();
    return json({ journal: results || [] });
  }

  return json({ erreur: "route inconnue" }, 404);
}
