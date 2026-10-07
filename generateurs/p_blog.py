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
from datetime import date as _date

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
    citation = []      # lignes consecutives d'une citation « > »

    def vide_paragraphe():
        # En Markdown, un paragraphe se termine sur une ligne vide, pas sur
        # un retour a la ligne. Sans ce regroupement, chaque ligne du
        # fichier devenait un <p> : le texte s'affichait hache.
        if paragraphe:
            sortie.append("<p>%s</p>" % en_ligne(" ".join(paragraphe)))
            paragraphe.clear()

    def vide_citation():
        # Meme principe que pour le paragraphe : les lignes « > »
        # consecutives forment UNE citation. Sans ce regroupement, un
        # encart de six lignes sortait en six blockquotes empiles, chacun
        # avec sa barre violette et ses marges - ce qui se voyait.
        if citation:
            sortie.append("<blockquote><p>%s</p></blockquote>"
                          % " ".join(citation))
            citation.clear()

    def ferme():
        nonlocal liste
        vide_paragraphe()
        vide_citation()
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
            vide_paragraphe()
            citation.append(en_ligne(l[2:].strip()))
            continue
        if citation:
            vide_citation()

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


def VALIDE(statut: str) -> bool:
    """Le statut autorise-t-il la publication ?

    Volontairement strict : on cherche le mot « validé » en toutes
    lettres. « rédigé », « à relire », « prêt » ne suffisent pas — ils
    décrivent l'état du texte, pas l'accord de Laurent.
    """
    s = (statut or "").strip().lower()
    return s.startswith("validé") or s.startswith("valide")


def A_PARAITRE(jour: str) -> bool:
    """La date de l'article est-elle encore dans le futur ?

    Second verrou, independant du premier. Laurent valide un article une
    fois pour toutes, mais sa date de parution reste celle inscrite dans
    l'en-tete : un article du 30 octobre ne sort pas le 7. Sans ce
    controle, valider les trois d'un coup les publierait tous les trois
    le meme jour.

    La comparaison se fait en date UTC. L'ecart avec Paris ne porte que
    sur les premieres heures de la journee, et la publication automatique
    tourne le matin : la date a tourne des deux cotes.
    """
    if not jour:
        return False
    try:
        return _date.fromisoformat(jour.strip()) > _date.today()
    except ValueError:
        # Une date illisible vaut un article qu'on ne publie pas.
        return True


def lire_articles() -> tuple[list[dict], list[tuple]]:
    """Les articles validés, et la liste de ceux qui attendent."""
    articles: list[dict] = []
    attente: list[tuple] = []
    for f in sorted(ARTICLES.glob("*.md")):
        meta, corps = entete(f.read_text(encoding="utf-8"))
        titre_h1, html = convertir(corps)
        titre = meta.get("titre") or titre_h1
        slug = meta.get("slug") or f.stem
        if not titre or not slug:
            print("  ignoré (en-tête incomplet) : %s" % f.name)
            continue
        # VERROU DE VALIDATION
        # Un article ne part en ligne que si son en-tête porte
        # « statut: validé ». Tout autre statut, ou aucun, le laisse en
        # attente : il n'est ni publié, ni indexé, et sa page est retirée
        # du site si elle y était.
        # La règle vient de Laurent, le 7 octobre 2026 : rien ne se publie
        # sans son accord. Ne pas la contourner en écrivant « validé » à sa
        # place — c'est lui qui le fait, article par article.
        if not VALIDE(meta.get("statut", "")):
            attente.append((f.name, meta.get("statut", "(aucun statut)"), slug))
            continue
        # Valide, mais pas encore a sa date : il attend son tour.
        if A_PARAITRE(meta.get("date", "")):
            attente.append((f.name,
                            "validé — paraît le %s" % meta.get("date", "?"),
                            slug))
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
            # L'illustration d'en-tete, produite par
            # reseaux/illustrations.py depuis la charte du site. Le champ
            # est facultatif : un article sans illustration s'affiche
            # simplement sans.
            "titre_seo": meta.get("titre_seo", ""),
            "illustration": meta.get("illustration", ""),
            "alt": meta.get("illustration_alt", ""),
        })
    articles.sort(key=lambda a: a["date"], reverse=True)
    return articles, attente


def jsonld_article(a: dict) -> str:
    import json
    # Google demande une image pour un article : sans elle, la fiche
    # n'est pas eligible aux resultats enrichis. On donne l'illustration
    # de l'article, pas le logo du studio.
    bloc = {"@type": "BlogPosting",
            "headline": a["titre"],
            "description": a["meta"],
            "datePublished": a["date"],
            "dateModified": a["date"],
            "inLanguage": "fr-FR",
            "wordCount": len(re.findall(r"[\wÀ-ÿ'’-]+",
                                        re.sub(r"<[^>]+>", " ", a["html"]))),
            "mainEntityOfPage": "%s/%s" % (SITE, a["fichier"]),
            # L'auteur est une personne, pas une organisation : c'est ce
            # que Google attend d'un article de conseil, et c'est vrai.
            "author": {"@type": "Person", "name": "Sandra",
                       "jobTitle": "Infographiste et chef de projet",
                       "worksFor": {"@type": "Organization",
                                    "name": "Grafycom", "url": SITE},
                       "url": SITE + "/a-propos.html"},
            "publisher": {"@type": "Organization", "name": "Grafycom",
                          "url": SITE,
                          "logo": {"@type": "ImageObject",
                                   "url": SITE + "/assets/img/logo-grafycom-carre.jpg"}}}
    if a.get("illustration"):
        bloc["image"] = "%s/assets/img/blog/%s" % (SITE, a["illustration"])
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            bloc,
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil",
                 "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog",
                 "item": SITE + "/blog.html"},
                {"@type": "ListItem", "position": 3, "name": a["titre"]},
            ]},
        ],
    }, ensure_ascii=False, indent=1)


def figure(a: dict) -> str:
    """La figure d'en-tete, si l'article en declare une.

    Le texte alternatif est obligatoire des qu'il y a une image : une
    illustration qui porte l'argument de l'article doit etre lisible par
    quelqu'un qui ne la voit pas.
    """
    if not a.get("illustration"):
        return ""
    alt = a.get("alt") or ""
    if not alt:
        raise SystemExit(
            "%s declare une illustration sans « illustration_alt ». "
            "Ajouter une description dans l'en-tete du .md." % a["slug"])
    return ('    <figure class="illu-article">\n'
            '      <img src="assets/img/blog/%s" alt="%s" '
            'width="1200" height="630" loading="eager">\n'
            '    </figure>\n'
            % (_html.escape(a["illustration"], quote=True),
               _html.escape(alt, quote=True)))


def titre_balise(a: dict) -> str:
    """Le <title>, celui que Google affiche dans ses resultats.

    L'ancienne version coupait a 62 caracteres sans egard pour les mots :
    « ...comment obtenir l'autorisation prealabl | Grafycom ». Un mot
    tronque dans un resultat de recherche, c'est un clic perdu.

    Deux corrections. Un article peut declarer « titre_seo » dans son
    en-tete : un titre court ecrit pour la recherche, qui n'a pas a etre
    celui affiche en haut de la page. A defaut, on coupe sur le dernier
    espace avant la limite, jamais au milieu d'un mot.
    """
    suffixe = " | Grafycom"
    limite = 60 - len(suffixe)
    t = (a.get("titre_seo") or "").strip() or a["titre"]
    if len(t) > limite:
        coupe = t[:limite].rsplit(" ", 1)[0].rstrip(" ,;:—-")
        t = coupe or t[:limite]
    return t + suffixe


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
%(illustration)s%(html)s
  </div>
</section>

<section class="fond-creme">
  <div class="conteneur conteneur-texte centre">
    <p><a href="blog.html">← Tous les articles</a></p>
  </div>
</section>
""" % {"titre": _html.escape(a["titre"]), "date": a["date"],
       "date_fr": en_francais(a["date"]), "html": a["html"],
       "illustration": figure(a)}

    corps += appel("Un projet en préparation&nbsp;?",
                   "Un premier échange est gratuit, et franc — y compris "
                   "quand la réponse est que vous n'avez besoin de rien.")

    page(a["fichier"],
         titre_balise(a),
         a["meta"],
         corps,
         ogtitle=a["titre"],
         ogtype="article",
         ogimage=("assets/img/blog/%s" % a["illustration"]) if a.get("illustration") else None,
         ogdate=a.get("date") or None,
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
    articles, attente = lire_articles()
    for a in articles:
        page_article(a)
    page_index(articles)
    maj_sitemap(articles)

    # Un article dépublié doit disparaître du site, pas seulement cesser
    # d'être ajouté : sa page resterait sinon en ligne, atteignable par
    # son adresse directe et par les moteurs.
    retires = []
    for nom, statut, slug in attente:
        page = RACINE / ("blog-%s.html" % slug)
        if page.exists():
            page.unlink()
            retires.append(page.name)

    print("  %d article(s) publié(s)." % len(articles))
    if attente:
        print("  %d en attente de validation :" % len(attente))
        for nom, statut, slug in attente:
            print("      %-46s statut : %s" % (nom, statut))
    if retires:
        print("  %d page(s) retirée(s) du site :" % len(retires))
        for r in retires:
            print("      %s" % r)
    if attente:
        if any("validé — paraît" in st for _, st, _ in attente):
            print("\n  Les articles validés sortiront d'eux-mêmes à leur date,")
            print("  par la routine de publication. Rien à faire.")
        else:
            print("\n  Pour publier : mettre « statut: validé » dans l'en-tête")
            print("  du .md, puis relancer ce script.")


main()
