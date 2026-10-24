#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les sept articles du blog, en un PDF qui se lit comme un magazine.

Pourquoi celui-ci en plus de `pdf.py`
-------------------------------------
`pdf.py` fabrique `blog.pdf`, qui est l'**index** : ce qui existe, à
quelle date, à quel statut. On n'y lit pas un article. Or ce qu'on
valide, c'est le texte — 5 700 mots répartis dans sept fichiers
markdown que personne ne relit dans un terminal.

Ce script-ci prend les articles eux-mêmes et les compose : ouverture
pleine largeur, chapô, corps sur deux colonnes, lettrine, exergues,
figures légendées, encadrés. La mise en page n'est pas un ornement —
un article de conseil se relit mieux sur deux colonnes courtes qu'en
une seule ligne de 17 cm, et les figures ne se jugent qu'à leur place
dans le texte.

Ce que ce fichier ne refait pas
-------------------------------
La conversion du markdown. Elle vit dans `generateurs/md_article.py`,
et le site s'en sert aussi : ce PDF montre donc exactement ce que la
page affichera, ce qui est la seule raison de valider sur un PDF.

Les couleurs ne sont pas écrites ici non plus : `generateurs/charte.py`
les lit dans `assets/style.css`.

Usage
-----
    python3 reseaux/articles.py                  les sept
    python3 reseaux/articles.py qui-possede      un seul, par son slug
    python3 reseaux/articles.py --sortie /tmp
"""
import argparse
import asyncio
import base64
import datetime as dt
import pathlib
import re
import sys

ICI = pathlib.Path(__file__).resolve().parent
RACINE = ICI.parent
ARTICLES = ICI / "blog"
POLICES = ICI / "polices"
IMAGES = RACINE / "assets" / "img" / "blog"
sys.path.insert(0, str(RACINE / "generateurs"))
from charte import C  # noqa: E402
from md_article import (convertir, en_francais, entete,  # noqa: E402
                        taille_png)

# Le statut tel qu'il est écrit dans l'en-tête, et ce qu'il veut dire
# pour qui relit. « validé » est le seul mot qui déclenche la parution :
# voir les deux verrous dans propositions/a-valider/blog.md.
STATUTS = {
    "validé": ("✅", "validé — paraîtra tout seul à sa date"),
    "à relire": ("⚠️", "attend ta lecture"),
    "réécrit, à relire": ("♻️", "réécrit le 23 octobre, attend ta lecture"),
}


def fonte(nom, fichier, graisse, style="normal"):
    b = base64.b64encode((POLICES / fichier).read_bytes()).decode()
    return ("@font-face{font-family:'%s';font-weight:%s;font-style:%s;"
            "src:url(data:font/ttf;base64,%s) format('truetype')}"
            % (nom, graisse, style, b))


def css():
    fontes = "".join([
        fonte("Inter", "Inter-400.ttf", 400),
        fonte("Inter", "Inter-600.ttf", 600),
        fonte("Inter", "Inter-800.ttf", 800),
        fonte("Playfair", "Playfair-500.ttf", 500),
        fonte("Playfair", "Playfair-700.ttf", 700),
        fonte("Playfair", "Playfair-800.ttf", 800),
        fonte("Caveat", "Caveat.ttf", 400),
    ])
    return fontes + """
:root{--encre:%(encre)s;--brun:%(brun)s;--brun-clair:%(brun_clair)s;
 --taupe:%(taupe)s;--creme:%(creme)s;--creme-rose:%(creme_rose)s;
 --sable:%(sable)s;--sable-fonce:%(sable_fonce)s;--bleu:%(bleu)s;
 --violet:%(violet)s;--corail:%(corail)s;--turquoise:%(turquoise)s;
 --orange:%(orange)s;--blanc:#fff}
*{box-sizing:border-box}
body{margin:0;color:var(--encre);background:var(--blanc);
 font-family:'Inter','Noto Color Emoji',sans-serif;
 font-size:9.6pt;line-height:1.58;-webkit-font-smoothing:antialiased}

/* --- la couverture du dossier ------------------------------------- */
.couv{height:247mm;display:flex;flex-direction:column;
 justify-content:center;break-after:page}
.filet{height:7px;margin-bottom:30mm;background:linear-gradient(90deg,
 %(bleu)s 0%%,%(bleu_vif)s 18%%,%(turquoise)s 33%%,%(violet)s 52%%,
 %(magenta)s 70%%,%(corail)s 84%%,%(orange)s 94%%,%(jaune)s 100%%)}
.marque{font-size:8.4pt;font-weight:600;letter-spacing:.17em;
 text-transform:uppercase;color:var(--taupe);margin-bottom:9mm}
.couv h1{font-family:'Playfair',Georgia,serif;font-weight:800;
 font-size:33pt;line-height:1.07;margin:0 0 7mm;max-width:15cm}
.couv .sous{font-size:12.2pt;line-height:1.5;color:var(--brun);
 margin:0 0 16mm;max-width:13cm}
.sommaire{border-top:1px solid var(--sable-fonce);max-width:15cm}
.sommaire div{display:flex;gap:6mm;padding:2.6mm 0;
 border-bottom:1px solid var(--sable)}
.sommaire .n{font-family:'Playfair',serif;font-weight:700;
 color:var(--taupe);width:7mm;flex:none}
.sommaire .t{flex:1}
.sommaire .s{color:var(--taupe);font-size:8.6pt;white-space:nowrap}
.couv .rappel{margin-top:14mm;padding:5mm 6mm;background:var(--creme);
 border-left:3px solid var(--violet);font-size:9pt;color:var(--brun);
 max-width:15cm}

/* --- l'ouverture d'un article ------------------------------------- */
.art{break-before:page}
.kicker{font-size:8pt;font-weight:600;letter-spacing:.15em;
 text-transform:uppercase;color:var(--taupe);
 display:flex;gap:4mm;align-items:baseline}
.kicker .num{font-family:'Playfair',serif;font-size:15pt;font-weight:800;
 letter-spacing:0;color:var(--sable-fonce);text-transform:none}
.art h1{font-family:'Playfair',Georgia,serif;font-weight:800;
 font-size:25pt;line-height:1.1;margin:3mm 0 0;text-wrap:balance;
 max-width:16cm}
.chapo{font-size:12pt;line-height:1.48;color:var(--brun);
 margin:5mm 0 0;max-width:15cm;font-weight:400}
.chapo strong{color:var(--encre);font-weight:600}
.une{margin:7mm 0 0}
.une img{width:100%%;height:auto;display:block;
 border:1px solid var(--sable-fonce)}
figcaption{font-size:7.8pt;line-height:1.45;color:var(--taupe);
 margin-top:1.8mm;padding-left:2mm;border-left:2px solid var(--sable-fonce)}
.filets{display:flex;gap:2px;margin:7mm 0 5mm}
.filets i{height:3px;flex:1}

/* --- le corps, sur deux colonnes ---------------------------------- */
/* Fer a gauche, pas justifie : Chromium ne cesure pas le francais —
   verifie, la hauteur d'un bloc est la meme avec « hyphens:auto » et
   sans. Justifier une colonne de 83 mm sans cesure, c'est fabriquer
   des rivieres de blanc a chaque ligne un peu longue. */
.corps{column-count:2;column-gap:7mm;
 column-rule:1px solid var(--sable);text-align:left;hyphens:none}
.corps p{margin:0 0 2.4mm;orphans:2;widows:2}
/* La lettrine n'appartient qu'au premier bloc : « :first-of-type » ne
   suffisait pas, le kicker est un div lui aussi et passait devant. */
.corps.debut > p:first-of-type::first-letter{font-family:'Playfair',serif;
 font-weight:800;font-size:31pt;line-height:.82;float:left;
 padding:1.4mm 1.6mm 0 0;color:var(--corail)}
.corps h2{font-family:'Playfair',Georgia,serif;font-weight:700;
 font-size:12.4pt;line-height:1.18;margin:5mm 0 2mm;
 break-after:avoid;text-align:left;hyphens:none}
.corps h2::before{content:"";display:block;width:11mm;height:2px;
 background:var(--corail);margin-bottom:2mm}
.corps h3{font-family:'Inter',sans-serif;font-weight:600;font-size:9.6pt;
 margin:4mm 0 1.4mm;break-after:avoid;text-align:left}
.corps ul,.corps ol{margin:0 0 2.6mm;padding-left:4.6mm}
.corps li{margin-bottom:1.1mm}
.corps a{color:var(--encre);text-decoration:none;
 border-bottom:1px solid var(--turquoise)}
.corps code{font-family:'Inter',monospace;font-size:8.6pt;
 background:var(--creme);padding:0 .9mm;border-radius:2px}
.corps strong{font-weight:600}

/* --- exergue, encadré, citation, figure --------------------------- */
.exergue{column-span:all;margin:6mm 0;padding:5mm 0;
 border-top:2px solid var(--encre);border-bottom:1px solid var(--sable-fonce);
 font-family:'Playfair',Georgia,serif;font-weight:500;font-size:16pt;
 line-height:1.28;text-align:center;color:var(--encre);
 break-inside:avoid;hyphens:none}
.exergue strong{font-weight:700}
blockquote{margin:0 0 3mm;padding:3.4mm 4mm;background:var(--creme);
 border-left:3px solid var(--sable-fonce);break-inside:avoid}
blockquote p{margin:0;font-size:9pt;line-height:1.5;color:var(--brun)}
blockquote.alerte{background:#fdf3f3;border-left-color:var(--corail)}
blockquote.alerte p{color:var(--encre)}
.figure-article{margin:5mm 0 6mm;break-inside:avoid}
/* « height:auto » n'est pas decoratif : l'attribut height du HTML
   donne le ratio, et sans lui la figure se posait a 630 px de haut en
   travers des deux colonnes — Chromium renoncait a la dessiner. */
.figure-article img{width:100%%;height:auto;display:block;
 border:1px solid var(--sable-fonce)}
.figure-article figcaption{max-width:15cm}

/* --- le pied de validation ---------------------------------------- */
.valide{column-span:all;margin-top:7mm;padding:4.6mm 5mm;
 background:var(--creme-rose);border:1px solid var(--sable-fonce);
 font-size:8.8pt;line-height:1.52;break-inside:avoid}
.valide b{font-weight:600}
.valide .ligne{display:flex;gap:4mm;margin-top:2.4mm;color:var(--brun)}
.coche{font-size:11pt;line-height:1}
.fich{font-family:'Inter',monospace;font-size:8pt;color:var(--taupe)}
""" % C


def filets():
    noms = ("bleu", "bleu_vif", "turquoise", "violet", "magenta",
            "corail", "orange", "jaune")
    return ('<div class="filets">%s</div>'
            % "".join('<i style="background:%s"></i>' % C[n] for n in noms))


def lire():
    """Les sept articles, dans l'ordre de parution."""
    out = []
    for f in sorted(ARTICLES.glob("20*.md")):
        meta, corps = entete(f.read_text(encoding="utf-8"))
        titre_h1, html = convertir(corps, f.name)
        # « loading=lazy » est bon pour le site et fatal ici : une image
        # sous la ligne de flottaison n'est jamais chargée au moment où
        # Chromium imprime, et la figure sort blanche — à la bonne
        # taille, avec sa légende, ce qui la rend difficile à voir.
        html = html.replace(' loading="lazy"', "")
        out.append({
            "fichier": f.name,
            "titre": meta.get("titre") or titre_h1,
            "slug": meta.get("slug", f.stem),
            "date": meta.get("date", ""),
            "statut": meta.get("statut", "—"),
            "illustration": meta.get("illustration", ""),
            "alt": meta.get("illustration_alt", ""),
            "mots": len(re.sub(r"<[^>]+>", " ", html).split()),
            "html": html,
        })
    return out


def jour(iso):
    """2026-10-30 -> vendredi 30 octobre 2026."""
    sem = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi",
           "dimanche")
    try:
        d = dt.date.fromisoformat(iso)
        return "%s %s" % (sem[d.weekday()], en_francais(iso))
    except ValueError:
        return iso


def couverture(arts):
    lignes = "".join(
        '<div><span class="n">%d</span><span class="t">%s</span>'
        '<span class="s">%s</span></div>'
        % (i, a["titre"], STATUTS.get(a["statut"], ("", a["statut"]))[0]
           + " " + jour(a["date"]).split(" ", 1)[1].rsplit(" ", 1)[0])
        for i, a in enumerate(arts, 1))
    attente = sum(1 for a in arts if a["statut"] != "validé")
    return """<section class="couv">
  <div class="filet"></div>
  <div class="marque">Grafycom &middot; à valider</div>
  <h1>Le blog, article par article</h1>
  <p class="sous">Les %d textes complets, mis en page comme ils
  paraîtront. %s mots en tout, du %s au %s.</p>
  <div class="sommaire">%s</div>
  <div class="rappel"><b>%d articles sur %d attendent ta lecture.</b>
  Un article paraît quand <b>deux</b> conditions sont réunies : son
  en-tête porte <b>statut&nbsp;: validé</b>, en toutes lettres, et sa
  date est arrivée. Tu peux donc tout valider d'un coup sans que tout
  sorte le même jour.</div>
</section>""" % (len(arts), format(sum(a["mots"] for a in arts), ",d")
                 .replace(",", " "),
                 jour(arts[0]["date"]).rsplit(" ", 1)[0],
                 jour(arts[-1]["date"]), lignes, attente, len(arts))


FIGURE_HTML = re.compile(r'<figure class="figure-article">.*?</figure>',
                         re.S)


def bandes(corps):
    """Le corps en blocs de deux colonnes, figures posées entre eux.

    Une figure déclarée « column-span: all » garde sa place dans la
    page et n'y dessine rien : Chromium réserve la boîte, au bon
    rapport, et laisse l'image blanche. Le défaut est d'autant plus
    traître que la page a l'air juste — c'est la légende, seule sous un
    cadre vide, qui le trahit.

    On ne traverse donc pas les colonnes : on les ferme. Chaque figure
    coupe le corps en deux blocs, elle se pose pleine largeur entre les
    deux, et chaque bloc équilibre ses propres colonnes. C'est d'ailleurs
    la composition d'un magazine : une bande d'image, puis du texte.
    """
    morceaux, fin = [], 0
    for m in FIGURE_HTML.finditer(corps):
        bloc = corps[fin:m.start()]
        morceaux.append(('<div class="corps%s">%s</div>'
                         % (" debut" if not morceaux else "", bloc))
                        if bloc.strip() else "")
        morceaux.append(m.group(0))
        fin = m.end()
    reste = corps[fin:]
    if not morceaux:
        return '<div class="corps debut">%s</div>' % reste
    if reste.strip():
        morceaux.append('<div class="corps">%s</div>' % reste)
    return "\n".join(x for x in morceaux if x)


def article(a, n):
    corps = a["html"]
    # Le premier paragraphe monte en chapô : c'est lui qui donne envie
    # de lire la suite, et il ne se lit pas en corps de texte justifié
    # sur deux colonnes.
    chapo = ""
    m = re.match(r"\s*<p>(.*?)</p>", corps, re.S)
    if m:
        chapo = '<p class="chapo">%s</p>' % m.group(1)
        corps = corps[m.end():]

    une = ""
    if a["illustration"] and (IMAGES / a["illustration"]).exists():
        larg, haut = taille_png(IMAGES / a["illustration"])
        une = ('<figure class="une"><img src="assets/img/blog/%s" alt="" '
               'width="%d" height="%d"><figcaption>%s</figcaption></figure>'
               % (a["illustration"], larg, haut, a["alt"]))

    icone, dit = STATUTS.get(a["statut"], ("•", a["statut"]))
    return """<article class="art">
  <div class="kicker"><span class="num">%02d</span><span>%s</span>
    <span>&middot;</span><span>%d mots</span></div>
  <h1>%s</h1>
  %s
  %s
  %s
  %s
  <div class="corps fin">
    <div class="valide">
      <b>%s Statut : %s</b>
      <div class="ligne"><span class="coche">&#9744;</span>
      <span>Pour le valider : ouvrir <span class="fich">reseaux/blog/%s</span>,
      remplacer la ligne <span class="fich">statut:</span> par
      <span class="fich">statut: validé</span>. Il paraîtra le %s,
      tout seul.</span></div>
    </div>
  </div>
</article>""" % (n, jour(a["date"]), a["mots"], a["titre"], chapo, une,
                 filets(), bandes(corps), icone, dit, a["fichier"],
                 jour(a["date"]))


def document(arts):
    return ("<!doctype html><html lang=fr><head><meta charset=utf-8>"
            "<title>Le blog, article par article</title>"
            "<style>%s</style></head><body>%s%s</body></html>"
            % (css(), couverture(arts),
               "".join(article(a, i) for i, a in enumerate(arts, 1))))


async def fabrique(arts, sortie):
    from playwright.async_api import async_playwright
    sortie.mkdir(parents=True, exist_ok=True)
    cible = sortie / "articles.pdf"
    # La page s'écrit à la racine du dépôt et s'ouvre par son adresse de
    # fichier : les figures gardent alors le chemin relatif qu'elles ont
    # sur le site, « assets/img/blog/... », et le navigateur les trouve.
    # L'autre voie — les embarquer en base64 — tenait du bricolage : huit
    # cents kilo-octets d'images dans le HTML, un décodage que Chromium
    # ne terminait pas avant l'impression, et des figures blanches à la
    # bonne taille. Blanches ET bien placées, c'est le pire des deux.
    provisoire = RACINE / ".articles-relecture.html"
    provisoire.write_text(document(arts), encoding="utf-8")
    try:
        return await _imprime(provisoire, cible)
    finally:
        provisoire.unlink(missing_ok=True)


async def _imprime(provisoire, cible):
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        exe = next((str(c) for c in sorted(
            pathlib.Path("/opt/pw-browsers").glob(
                "chromium-*/chrome-linux/chrome"), reverse=True)), None)
        nav = await (pw.chromium.launch(executable_path=exe) if exe
                     else pw.chromium.launch())
        page = await nav.new_page()
        await page.goto(provisoire.as_uri(), wait_until="load")
        await page.pdf(
            path=str(cible), format="A4", print_background=True,
            margin={"top": "16mm", "bottom": "18mm",
                    "left": "17mm", "right": "17mm"},
            display_header_footer=True,
            header_template="<div></div>",
            footer_template=(
                "<div style='width:100%;font-size:7.2pt;color:#a2897c;"
                "font-family:sans-serif;padding:0 17mm;display:flex;"
                "justify-content:space-between'><span>Grafycom &middot; "
                "le blog &middot; à valider</span>"
                "<span class='pageNumber'></span></div>"))
        await nav.close()
    return cible


def main():
    a = argparse.ArgumentParser(
        description=__doc__.split("\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("slugs", nargs="*", help="filtre sur le slug ; tous si omis")
    a.add_argument("--sortie", default=str(ICI / "pdf"))
    args = a.parse_args()

    arts = lire()
    if args.slugs:
        arts = [x for x in arts
                if any(s in x["slug"] or s in x["fichier"] for s in args.slugs)]
        if not arts:
            sys.exit("Aucun article ne correspond.")
    for x in arts:
        print("  %-46s %4d mots  %s" % (x["slug"], x["mots"], x["statut"]))
    cible = asyncio.run(fabrique(arts, pathlib.Path(args.sortie)))
    print("\n%s — %.1f ko" % (cible, cible.stat().st_size / 1024))


if __name__ == "__main__":
    main()
