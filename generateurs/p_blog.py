# -*- coding: utf-8 -*-
"""Le blog : une page par article, plus l'index.

Les articles ne sont pas écrits ici. Ils vivent en Markdown dans
`reseaux/blog/`, un fichier par article, avec un en-tête de métadonnées.
C'est volontaire : le texte doit rester modifiable par quelqu'un qui
n'ouvre pas un fichier Python, et l'assistant éditorial écrit déjà dans
ce dossier.

Ce script lit ces fichiers, les convertit et produit :

  blog.html                  l'index, du plus récent au plus ancien
  blog-<slug>.html           une page par article

Puis il met à jour le bloc du blog dans sitemap.xml, entre ses deux
marqueurs. Un article ajouté au dossier entre donc au sitemap tout seul :
c'est la seule façon de ne pas l'oublier.

En-tête attendu en tête de chaque fichier Markdown :

    ---
    titre: "Le titre complet, qui devient le H1"
    slug: le-slug-de-l-adresse
    date: 2026-10-16
    meta: "La méta-description, environ 150 caractères."
    ---
"""
import html as _html
import io
import os
import pathlib
import re

from gen import page, appel, SITE

RACINE = pathlib.Path(__file__).resolve().parent.parent
ARTICLES = RACINE / "reseaux" / "blog"
SITEMAP = RACINE / "sitemap.xml"

DEBUT_BLOC = "  <!-- blog : bloc produit par generateurs/p_blog.py -->"
FIN_BLOC = "  <!-- fin blog -->"

MOIS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre")


def en_francais(iso: str) -> str:
    """2026-10-16 -> 16 octobre 2026."""
    try:
        a, m, j = (int(x) for x in iso.split("-"))
        return "%d %s %d" % (j, MOIS[m - 1], a)
    except Exception:
        return iso


def entete(texte: str) -> tuple[dict, str]:
    """Sépare l'en-tête de métadonnées du corps de l'article."""
    if not texte.startswith("---"):
        return {}, texte
    fin = texte.find("\n---", 3)
    if fin == -1:
        return {}, texte
    meta = {}
    for ligne in texte[3:fin].strip().splitlines():
        if ":" not in ligne:
            continue
        cle, _, valeur = ligne.partition(":")
        meta[cle.strip()] = valeur.strip().strip('"').strip("'")
    return meta, texte[fin + 4:].lstrip("\n")


def en_ligne(t: str) -> str:
    """Gras, italique, code et liens, après échappement du HTML."""
    t = _html.escape(t, quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    # Markdown echappe l'asterisque par « \* » pour qu'il ne devienne pas
    # de l'italique. L'antislash ne doit pas se retrouver a l'ecran.
    t = re.sub(r"\\([*_`\[\]])", r"\1", t)
    # Les espaces insécables françaises avant la ponctuation double.
    t = re.sub(r" ([?!:;»])", r"&nbsp;\1", t)
    t = t.replace("« ", "«&nbsp;")
    return t


def convertir(markdown: str) -> tuple[str, str]:
    """Rend le corps en HTML. Renvoie (titre H1, corps sans le H1)."""
    titre, sortie = "", []
    liste = None       # None, "ul" ou "ol"
    paragraphe = []    # lignes consecutives du paragraphe en cours

    def vide_paragraphe():
        # En Markdown, un paragraphe se termine sur une ligne vide, pas sur
        # un retour a la ligne. Sans ce regroupement, chaque ligne du
        # fichier devenait un <p> : le texte s'affichait hache.
        if paragraphe:
            sortie.append("<p>%s</p>" % en_ligne(" ".join(paragraphe)))
            paragraphe.clear()

    def ferme():
        nonlocal liste
        vide_paragraphe()
        if liste:
            sortie.append("</%s>" % liste)
            liste = None

    for brute in markdown.splitlines():
        l = brute.strip()

        if not l:
            ferme()
            continue

        if l.startswith("# "):
            ferme()
            titre = l[2:].strip()
            continue
        if l.startswith("### "):
            ferme()
            sortie.append("<h3>%s</h3>" % en_ligne(l[4:].strip()))
            continue
        if l.startswith("## "):
            ferme()
            sortie.append("<h2>%s</h2>" % en_ligne(l[3:].strip()))
            continue
        if l.startswith("---"):
            ferme()
            continue
        if l.startswith("> "):
            ferme()
            sortie.append("<blockquote><p>%s</p></blockquote>"
                          % en_ligne(l[2:].strip()))
            continue

        puce = re.match(r"^[-*]\s+(.*)$", l)
        numero = re.match(r"^\d+\.\s+(.*)$", l)
        if puce or numero:
            voulue = "ol" if numero else "ul"
            vide_paragraphe()
            if liste != voulue:
                ferme()
                sortie.append("<%s>" % voulue)
                liste = voulue
            sortie.append("<li>%s</li>"
                          % en_ligne((numero or puce).group(1)))
            continue

        if liste:
            ferme()
        paragraphe.append(l)

    ferme()
    return titre, "\n".join(sortie)


def lire_articles() -> list[dict]:
    """Tous les articles du dossier, du plus récent au plus ancien."""
    articles = []
    for f in sorted(ARTICLES.glob("*.md")):
        meta, corps = entete(f.read_text(encoding="utf-8"))
        titre_h1, html = convertir(corps)
        titre = meta.get("titre") or titre_h1
        slug = meta.get("slug") or f.stem
        if not titre or not slug:
            print("  ignoré (en-tête incomplet) : %s" % f.name)
            continue
        # Le chapô : le premier paragraphe, qui sert aussi de résumé
        # sur l'index. Pas de résumé à écrire deux fois.
        premier = re.search(r"<p>(.*?)</p>", html, re.S)
        chapo = re.sub(r"<[^>]+>", "", premier.group(1)) if premier else ""
        articles.append({
            "titre": titre, "slug": slug,
            "date": meta.get("date", ""),
            "meta": meta.get("meta", chapo[:155]),
            "html": html, "chapo": chapo,
            "fichier": "blog-%s.html" % slug,
        })
    articles.sort(key=lambda a: a["date"], reverse=True)
    return articles


def jsonld_article(a: dict) -> str:
    import json
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BlogPosting",
             "headline": a["titre"],
             "description": a["meta"],
             "datePublished": a["date"],
             "dateModified": a["date"],
             "inLanguage": "fr-FR",
             "mainEntityOfPage": "%s/%s" % (SITE, a["fichier"]),
             "author": {"@type": "Organization", "name": "Grafycom"},
             "publisher": {"@type": "Organization", "name": "Grafycom",
                           "url": SITE}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil",
                 "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog",
                 "item": SITE + "/blog.html"},
                {"@type": "ListItem", "position": 3, "name": a["titre"]},
            ]},
        ],
    }, ensure_ascii=False, indent=1)


def page_article(a: dict) -> None:
    corps = """<section class="heros">
  <div class="conteneur">
    <nav class="fil" aria-label="Fil d'Ariane">
      <a href="index.html">Accueil</a> <span aria-hidden="true">›</span>
      <a href="blog.html">Blog</a>
    </nav>
    <h1>%(titre)s</h1>
    <p class="date-article"><time datetime="%(date)s">%(date_fr)s</time></p>
  </div>
</section>

<section>
  <div class="conteneur conteneur-texte article">
%(html)s
  </div>
</section>

<section class="fond-creme">
  <div class="conteneur conteneur-texte centre">
    <p><a href="blog.html">← Tous les articles</a></p>
  </div>
</section>
""" % {"titre": _html.escape(a["titre"]), "date": a["date"],
       "date_fr": en_francais(a["date"]), "html": a["html"]}

    corps += appel("Un projet en préparation&nbsp;?",
                   "Un premier échange est gratuit, et franc — y compris "
                   "quand la réponse est que vous n'avez besoin de rien.")

    page(a["fichier"],
         "%s | Grafycom" % a["titre"][:62],
         a["meta"],
         corps,
         ogtitle=a["titre"],
         jsonld=jsonld_article(a))


def page_index(articles: list[dict]) -> None:
    if articles:
        cartes = "\n".join(
            '      <article class="billet">\n'
            '        <p class="date-article"><time datetime="%s">%s</time></p>\n'
            '        <h2><a href="%s">%s</a></h2>\n'
            '        <p>%s</p>\n'
            '        <p><a class="lien-suite" href="%s">Lire l\'article →</a></p>\n'
            '      </article>'
            % (a["date"], en_francais(a["date"]), a["fichier"],
               _html.escape(a["titre"]),
               _html.escape(a["chapo"][:220] + ("…" if len(a["chapo"]) > 220 else "")),
               a["fichier"])
            for a in articles)
    else:
        cartes = ('      <p>Les premiers articles arrivent très '
                  'prochainement.</p>')

    corps = """<section class="heros">
  <div class="conteneur">
    <p class="eyebrow">Le blog</p>
    <h1>Comprendre avant de commander</h1>
    <p class="chapeau">Réglementation des enseignes, choix des supports,
    préparation des fichiers&nbsp;: ce qu'il vaut mieux savoir avant de
    lancer une fabrication. Écrit pour les commerces et artisans des
    Pyrénées-Orientales.</p>
  </div>
</section>

<section>
  <div class="conteneur conteneur-texte">
%s
  </div>
</section>
""" % cartes

    corps += appel("Une question qui n'a pas sa réponse ici&nbsp;?",
                   "Posez-la. Si elle revient souvent, elle deviendra le "
                   "prochain article.")

    page("blog.html",
         "Blog — enseignes, impression et identité visuelle | Grafycom",
         "Conseils pratiques pour les commerces et artisans du 66 : "
         "réglementation des enseignes, choix des supports, préparation "
         "des fichiers d'impression.",
         corps, ogtitle="Le blog de Grafycom")


def maj_sitemap(articles: list[dict]) -> None:
    """Réécrit le bloc du blog dans sitemap.xml, entre ses marqueurs.

    Sans ça, un article publié resterait invisible de Google jusqu'à ce
    que quelqu'un pense à éditer le sitemap à la main. Personne n'y pense.
    """
    if not SITEMAP.exists():
        print("  sitemap.xml introuvable, bloc non mis à jour")
        return
    texte = SITEMAP.read_text(encoding="utf-8")

    lignes = [DEBUT_BLOC,
              '  <url><loc>%s/blog.html</loc><changefreq>weekly</changefreq>'
              '<priority>0.8</priority></url>' % SITE]
    for a in articles:
        lignes.append(
            '  <url><loc>%s/%s</loc><lastmod>%s</lastmod>'
            '<changefreq>yearly</changefreq><priority>0.7</priority></url>'
            % (SITE, a["fichier"], a["date"]))
    lignes.append(FIN_BLOC)
    bloc = "\n".join(lignes)

    if DEBUT_BLOC in texte and FIN_BLOC in texte:
        avant = texte.split(DEBUT_BLOC)[0]
        apres = texte.split(FIN_BLOC, 1)[1]
        texte = avant + bloc + apres
    else:
        texte = texte.replace("</urlset>", bloc + "\n</urlset>")

    SITEMAP.write_text(texte, encoding="utf-8")
    print("  sitemap : %d adresse(s) de blog" % (len(articles) + 1))


def main():
    if not ARTICLES.exists():
        print("reseaux/blog/ n'existe pas : rien à produire.")
        return
    articles = lire_articles()
    for a in articles:
        page_article(a)
    page_index(articles)
    maj_sitemap(articles)
    print("  %d article(s) publié(s)." % len(articles))


main()
