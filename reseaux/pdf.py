#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique les PDF de relecture, un par document à valider.

Pourquoi un PDF
---------------
Les documents vivent en markdown dans le dépôt, c'est bien pour les
corriger. Mais on ne relit pas 2 000 lignes de markdown dans un terminal,
on les relit posé, au calme, en cochant. D'où ces PDF : la même matière,
paginée, avec les cases de validation déjà dans le texte.

La charte n'est pas recopiée : elle est lue dans generateurs/charte.py,
qui la lit elle-même dans assets/style.css. Les polices sont celles du
site, embarquées en base64 — un PDF doit rester juste même ouvert sur une
machine qui n'a ni Inter ni Playfair.

Usage
-----
    python3 reseaux/pdf.py                 # tous les documents
    python3 reseaux/pdf.py calendrier      # un seul
    python3 reseaux/pdf.py --sortie /tmp   # ailleurs que dans pdf/
"""
import argparse
import asyncio
import base64
import datetime as dt
import io
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent
SOURCE = RACINE / "propositions/a-valider"
POLICES = RACINE / "polices"
sys.path.insert(0, str(RACINE.parent / "generateurs"))
from charte import C  # noqa: E402

# L'ordre de lecture, pas l'ordre alphabétique : on commence par l'état,
# on finit par ce qui demande une décision.
ORDRE = [
    ("A-FOURNIR", "Ce qu'il me manque",
     "Par ordre de priorité, vérifié fichier par fichier"),
    ("PRET-A-VALIDER", "Ce qui est terminé", "L'état exact, canal par canal"),
    ("calendrier", "Le calendrier", "Tout ce qui est écrit, daté, dans l'ordre"),
    ("instagram-facebook", "Instagram & Facebook", "Les 29 publications"),
    ("fiche-google", "Fiche Google", "Les 26 textes de fiche"),
    ("stories", "Les stories", "Les 6 semaines, écran par écran"),
    ("blog", "Le blog", "L'index des 7 articles"),
    ("messages-prives", "Messages privés", "Le message d'accueil et les réponses types"),
    ("photos-a-prendre", "Photos à prendre", "Les prises de vue pour Sandra"),
    ("visuels-a-produire", "Visuels à produire", "Ce qu'il reste à dessiner"),
    ("BRIEF-PHOTOS-IA", "Brief visuels réalistes",
     "Ce qu'il faut générer, et ce qu'il ne faut jamais générer"),
    ("acquisition", "Abonnés et clients",
     "Ce que le plan fait pour l'objectif, mesuré"),
    ("arbitrages", "Arbitrages", "Ce qui demande une décision"),
    ("LISEZ-MOI", "Mode d'emploi", "Par où commencer, et comment valider"),
]

# Celui-ci n'est pas un document de relecture : c'est le document qu'on
# DONNE, en message prive, a qui prepare une enseigne. Sa couverture le
# dit autrement — pas de « a valider », pas de rappel interne.
LIVRABLES = {
    "checklist-enseigne": (
        "Avant de commander votre enseigne",
        "Six points à vérifier avant de signer"),
}


def _fonte(nom, fichier, graisse, style="normal"):
    b = base64.b64encode((POLICES / fichier).read_bytes()).decode()
    return ("@font-face{font-family:'%s';font-weight:%s;font-style:%s;"
            "src:url(data:font/ttf;base64,%s) format('truetype');}"
            % (nom, graisse, style, b))


def css():
    fontes = "".join([
        _fonte("Inter", "Inter-400.ttf", 400),
        _fonte("Inter", "Inter-600.ttf", 600),
        _fonte("Inter", "Inter-800.ttf", 800),
        _fonte("Playfair", "Playfair-500.ttf", 500),
        _fonte("Playfair", "Playfair-700.ttf", 700),
        _fonte("Caveat", "Caveat.ttf", 400),
    ])
    degrade = ("linear-gradient(90deg,%s 0%%,%s 18%%,%s 33%%,%s 52%%,"
               "%s 70%%,%s 84%%,%s 94%%,%s 100%%)"
               % (C["bleu"], C["bleu_vif"], C["turquoise"], C["violet"],
                  C["magenta"], C["corail"], C["orange"], C["jaune"]))
    return fontes + """
:root{--encre:%(encre)s;--brun:%(brun)s;--taupe:%(taupe)s;--creme:%(creme)s;
  --creme-rose:%(creme_rose)s;--sable:%(sable)s;--sable-fonce:%(sable_fonce)s;
  --bleu:%(bleu)s;--violet:%(violet)s;--corail:%(corail)s;--blanc:#fff;}
*{box-sizing:border-box}
body{font-family:'Inter','Noto Color Emoji',sans-serif;font-size:10.2pt;
  line-height:1.62;color:var(--encre);margin:0;
  -webkit-font-smoothing:antialiased;}
h1,h2,h3,h4{font-family:'Playfair',Georgia,serif;font-weight:700;
  line-height:1.2;color:var(--encre);margin:1.5em 0 .5em;
  break-after:avoid;page-break-after:avoid;}
h1{font-size:21pt;margin-top:0;padding-top:.3em;
  break-before:page;page-break-before:always;}
h1:first-of-type{break-before:auto;page-break-before:auto;}
h2{font-size:15pt;border-top:1px solid var(--sable-fonce);padding-top:.8em;}
h3{font-size:12pt;}
h4{font-size:10.5pt;font-family:'Inter';font-weight:800;
  text-transform:uppercase;letter-spacing:.04em;color:var(--brun);}
p,ul,ol{margin:.55em 0}
li{margin:.22em 0}
strong{font-weight:800}
em{font-style:italic;color:var(--brun)}
a{color:var(--bleu);text-decoration:none}
del{text-decoration:line-through;color:var(--taupe);}
code{font-family:'DejaVu Sans Mono',monospace;font-size:8.6pt;
  background:var(--creme-rose);padding:1px 4px;border-radius:3px;
  color:var(--brun);}
pre{background:var(--creme);border-left:3px solid var(--violet);
  padding:10px 14px;border-radius:4px;overflow-wrap:anywhere;
  white-space:pre-wrap;font-size:8.6pt;break-inside:avoid;}
pre code{background:none;padding:0}
blockquote{margin:.8em 0;padding:11px 16px;background:var(--creme-rose);
  border-left:4px solid var(--violet);border-radius:0 6px 6px 0;
  break-inside:avoid;page-break-inside:avoid;}
blockquote p{margin:.3em 0}
blockquote>p:first-child>strong:first-child{color:var(--corail)}
table{border-collapse:collapse;width:100%%;margin:.8em 0;font-size:9pt;
  break-inside:auto;}
th{background:var(--encre);color:#fff;font-weight:600;text-align:left;
  padding:6px 9px;font-size:8.6pt;text-transform:uppercase;
  letter-spacing:.03em;}
td{padding:6px 9px;border-bottom:1px solid var(--sable);
  vertical-align:top;}
tr{break-inside:avoid;page-break-inside:avoid;}
tbody tr:nth-child(even){background:var(--creme)}
hr{border:0;height:3px;border-radius:3px;background:%(degrade)s;
  margin:1.6em 0;}
/* la case a cocher : on la veut visible et cochable a la main */
.coche{font-family:'DejaVu Sans',sans-serif;font-size:13pt;
  color:var(--violet);line-height:1;}
li.tache{list-style:none;margin-left:-1.1em;margin-top:.3em;
  padding-left:.1em;}
li.tache .coche{margin-right:.35em;vertical-align:-1px;}
/* ---- couverture ---- */
.couv{height:247mm;display:flex;flex-direction:column;
  justify-content:center;break-after:page;page-break-after:always;}
.couv .filet{height:5px;width:120px;border-radius:5px;
  background:%(degrade)s;margin-bottom:28px;}
.couv .marque{font-weight:800;font-size:11pt;letter-spacing:.14em;
  text-transform:uppercase;color:var(--taupe);margin-bottom:6px;}
.couv h1{font-size:34pt;margin:0 0 10px;border:0;break-before:auto;
  page-break-before:auto;}
.couv .sous{font-size:13pt;color:var(--brun);margin:0 0 40px;}
.couv .meta{font-size:9.4pt;color:var(--taupe);border-top:1px solid
  var(--sable-fonce);padding-top:14px;}
.couv .meta b{color:var(--encre);font-weight:600}
.rappel{margin-top:26px;padding:14px 18px;background:var(--creme);
  border-left:4px solid var(--corail);border-radius:0 6px 6px 0;
  font-size:9.6pt;}
""" % dict(C, degrade=degrade, creme_rose=C["creme_rose"],
           sable_fonce=C["sable_fonce"])


def couverture(titre, sous, doc, nb_mots):
    if doc in LIVRABLES:
        return """<section class="couv">
  <div class="filet"></div>
  <div class="marque">Grafycom &middot; Pyrénées-Orientales</div>
  <h1>%s</h1>
  <p class="sous">%s</p>
  <div class="meta">
    Gratuit, sans contrepartie. Rien à remplir, rien à renvoyer.<br>
    <b>grafycom.fr</b> &nbsp;·&nbsp; @grafycom.graphiste
  </div>
  <div class="rappel">Ce document donne des <b>repères</b>, pas un avis
  juridique. Les règles locales se vérifient en mairie, qui est la
  source.</div>
</section>""" % (titre, sous)
    return """<section class="couv">
  <div class="filet"></div>
  <div class="marque">Grafycom &middot; à valider</div>
  <h1>%s</h1>
  <p class="sous">%s</p>
  <div class="meta">
    <b>%s</b> &nbsp;·&nbsp; %s mots &nbsp;·&nbsp; édité le %s<br>
    Cycle du <b>lundi 26 octobre</b> au <b>vendredi 11 décembre 2026</b>
  </div>
  <div class="rappel"><b>Rien n'est programmé, rien n'est publié.</b>
  Aucune publication ne part sans ton accord explicite. Les cases
  &#9744; sont là pour être cochées pendant la lecture.</div>
</section>""" % (titre, sous, doc + ".md", nb_mots,
                 dt.date.today().strftime("%d/%m/%Y"))


def html(doc, titre, sous):
    import markdown
    src = io.open(SOURCE / (doc + ".md"), encoding="utf-8").read()
    nb = len(src.split())
    # Typographie francaise, et accessoirement des colonnes qui ne se
    # cassent pas en deux : « 8 h 00 » et « mardi 20 octobre » tiennent
    # sur une ligne grace aux espaces insecables.
    src = re.sub(r"\b(\d{1,2}) h (\d{2})\b", "\\1\u00a0h\u00a0\\2", src)
    src = re.sub(r"\b(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche) "
                 r"(\d{1,2}(?:er)?) (janvier|février|mars|avril|mai|juin|"
                 r"juillet|août|septembre|octobre|novembre|décembre)\b",
                 "\\1\u00a0\\2\u00a0\\3", src, flags=re.IGNORECASE)
    # « ~~barré~~ » : python-markdown ne connait pas la syntaxe et sortait
    # les tildes en clair — « ~~Une photo de rue~~ » imprime tel quel, ce
    # qui est pire que pas de barre du tout. On la convertit avant.
    src = re.sub(r"~~(.+?)~~", r"<del>\1</del>", src, flags=re.S)
    corps = markdown.markdown(
        # Pas de nl2br : les documents sont coupes a 76 colonnes dans le
        # depot, et chaque retour devenait un retour visuel — les phrases
        # se brisaient en plein milieu. Markdown rejoint les lignes d'un
        # meme paragraphe, c'est exactement ce qu'on veut.
        src, extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5")
    # « - [ ] » est une liste de taches : python-markdown ne la connait
    # pas et la rendait en « [ ] » litteral. On la transforme en vraie
    # case, de la meme famille que les ☐ deja ecrits dans les documents.
    corps = re.sub(r"<li>\s*\[ \]\s*",
                   '<li class="tache"><span class="coche">\u2610</span> ',
                   corps)
    corps = re.sub(r"<li>\s*\[[xX]\]\s*",
                   '<li class="tache"><span class="coche">\u2611</span> ',
                   corps)
    # les cases a cocher du markdown passent en span stylé
    corps = corps.replace("☐", '<span class="coche">☐</span>')
    # Un filet juste avant un titre de niveau 1 ne sert a rien :
    # le titre ouvre deja une page, et le filet en laissait une
    # presque vide.
    corps = re.sub(r"(?:<hr\s*/?>\s*)+(?=<h1)", "", corps)
    corps = re.sub(r"(?:<hr\s*/?>\s*){2,}", "<hr />", corps)
    return ("<!doctype html><html lang=fr><head><meta charset=utf-8>"
            "<title>%s</title><style>%s</style></head><body>%s%s</body></html>"
            % (titre, css(), couverture(titre, sous, doc, nb), corps))


async def fabrique(choisis, sortie):
    from playwright.async_api import async_playwright
    sortie.mkdir(parents=True, exist_ok=True)
    faits = []
    async with async_playwright() as pw:
        # Chromium est preinstalle dans l'environnement, a une version que
        # la bibliotheque ne devine pas toujours : on la lui nomme.
        exe = None
        for c in sorted(pathlib.Path("/opt/pw-browsers").glob(
                "chromium-*/chrome-linux/chrome"), reverse=True):
            exe = str(c)
            break
        nav = await (pw.chromium.launch(executable_path=exe) if exe
                     else pw.chromium.launch())
        page = await nav.new_page()
        for doc, titre, sous in choisis:
            f = SOURCE / (doc + ".md")
            if not f.exists():
                print("  %-22s absent, ignoré" % doc)
                continue
            await page.set_content(html(doc, titre, sous),
                                   wait_until="networkidle")
            cible = sortie / ("%s.pdf" % doc)
            await page.pdf(
                path=str(cible), format="A4", print_background=True,
                margin={"top": "17mm", "bottom": "19mm",
                        "left": "18mm", "right": "18mm"},
                display_header_footer=True,
                header_template="<div></div>",
                footer_template=(
                    "<div style='width:100%;font-size:7.4pt;"
                    "color:#a2897c;font-family:sans-serif;padding:0 18mm;"
                    "display:flex;justify-content:space-between'>"
                    "<span>Grafycom &middot; "
                    + titre.replace("&", "&amp;")
                    + ("" if doc in LIVRABLES else " &middot; à valider")
                    + "</span><span class='pageNumber'></span></div>"))
            faits.append(cible)
            print("  %-22s %6.1f ko" % (cible.name,
                                        cible.stat().st_size / 1024))
        await nav.close()
    return faits


def main():
    a = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("documents", nargs="*",
                   help="noms sans .md ; tous si omis")
    a.add_argument("--sortie", default=str(RACINE / "pdf"))
    args = a.parse_args()
    tous = ORDRE + [(d, n, s) for d, (n, s) in LIVRABLES.items()]
    choisis = tous
    if args.documents:
        voulus = {d.replace(".md", "") for d in args.documents}
        choisis = [c for c in tous if c[0] in voulus]
        inconnus = voulus - {c[0] for c in tous}
        if inconnus:
            sys.exit("Document inconnu : %s\nDisponibles : %s"
                     % (", ".join(sorted(inconnus)),
                        ", ".join(c[0] for c in tous)))
    print("Fabrication des PDF dans %s" % args.sortie)
    faits = asyncio.run(fabrique(choisis, pathlib.Path(args.sortie)))
    total = sum(f.stat().st_size for f in faits) / 1024 / 1024
    print("\n%d PDF, %.1f Mo au total." % (len(faits), total))


if __name__ == "__main__":
    main()
