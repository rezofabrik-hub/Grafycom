#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le calendrier, avec les visuels de chaque publication en regard.

Pourquoi ce fichier existe
--------------------------
Trois documents disent la même chose sous trois formes, et aucun ne
sert à l'instant où l'on programme. `calendrier.md` donne les dates
sans les images. `planche-contact.pdf` donne les images sans les
dates, rangées par dossier. `instagram-facebook.md` donne les textes,
publication par publication, sur deux mille lignes.

Celui-ci met les trois ensemble, dans l'ordre du temps : un jour, son
heure, ses planches en vignettes, ses stories, son texte de fiche
Google et son article. On le fait défiler, on programme, on passe au
jour suivant.

Ce qu'il ne fait pas
--------------------
Il n'invente aucune date. Toutes viennent de
`propositions/a-valider/calendrier.md`, qui reste la source. Un jour
déplacé là-bas se déplace ici au prochain passage. Les visuels sont
rapprochés par la DATE de leur dossier — `2026-10-26-couleurs` revient
au lundi 26 — et non par un numéro saisi à la main, qui dériverait.

Usage
-----
    python3 reseaux/calendrier-illustre.py
    python3 reseaux/calendrier-illustre.py --sortie /tmp
"""
import argparse
import asyncio
import base64
import datetime as dt
import html
import pathlib
import re
import shutil
import sys

ICI = pathlib.Path(__file__).resolve().parent
RACINE = ICI.parent
VISUELS = ICI / "visuels"
POLICES = ICI / "polices"
CAL = ICI / "propositions/a-valider/calendrier.md"
sys.path.insert(0, str(RACINE / "generateurs"))
from charte import C  # noqa: E402

MOIS = {"janvier": 1, "février": 2, "mars": 3, "avril": 4, "mai": 5,
        "juin": 6, "juillet": 7, "août": 8, "septembre": 9, "octobre": 10,
        "novembre": 11, "décembre": 12}
JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi",
         "dimanche")
MOIS_L = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet",
          "août", "septembre", "octobre", "novembre", "décembre")

# Les vignettes sont fabriquées à cette largeur plutôt que passées en
# pleine résolution : 199 planches de 1080 px donnent un PDF que
# personne n'ouvre deux fois.
VIGNETTE = 300
TEMPO = RACINE / ".calendrier-vignettes"


def fonte(nom, fichier, graisse, style="normal"):
    b = base64.b64encode((POLICES / fichier).read_bytes()).decode()
    return ("@font-face{font-family:'%s';font-weight:%s;font-style:%s;"
            "src:url(data:font/ttf;base64,%s) format('truetype')}"
            % (nom, graisse, style, b))


def lignes_du_calendrier():
    """Les lignes datées, dans l'ordre où elles sont écrites."""
    out = []
    for ligne in CAL.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"\| (?:~~)?(\w+) (\d{1,2})(?:er)? (\w+)(?:~~)? \| "
                     r"([^|]*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \|", ligne)
        if not m or m.group(3) not in MOIS:
            continue
        jour = dt.date(2026, MOIS[m.group(3)], int(m.group(2)))
        heure = re.sub(r"\*+", "", m.group(4)).strip()
        out.append({
            "date": jour,
            "heure": heure,
            "canal": re.sub(r"\*+", "", m.group(5)).strip(),
            "format": re.sub(r"\*+", "", m.group(6)).strip(),
            "quoi": m.group(7).strip(),
            "sortie": ligne.strip().startswith("| ~~"),
        })
    return out


def dossiers_par_date():
    """« 2026-10-26-couleurs » revient au 26 octobre."""
    out = {}
    for d in sorted(VISUELS.iterdir()):
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})-", d.name)
        if d.is_dir() and m:
            jour = dt.date(*(int(x) for x in m.groups()))
            out.setdefault(jour, []).append(d)
    return out


def vignette(source):
    """Une copie réduite, écrite une fois, réutilisée telle quelle."""
    from PIL import Image
    nom = (source.stem if source.parent.name == "stories"
           else "%s--%s" % (source.parent.name, source.stem))
    cible = TEMPO / (nom + ".jpg")
    if not cible.exists():
        im = Image.open(source).convert("RGB")
        h = round(im.height * VIGNETTE / im.width)
        im.resize((VIGNETTE, h), Image.LANCZOS).save(
            cible, "JPEG", quality=82, optimize=True, progressive=True)
    return cible.relative_to(RACINE).as_posix()


def css():
    fontes = "".join([
        fonte("Inter", "Inter-400.ttf", 400),
        fonte("Inter", "Inter-600.ttf", 600),
        fonte("Inter", "Inter-800.ttf", 800),
        fonte("Playfair", "Playfair-700.ttf", 700),
        fonte("Playfair", "Playfair-800.ttf", 800),
    ])
    return fontes + """
:root{--encre:%(encre)s;--brun:%(brun)s;--brun-clair:%(brun_clair)s;
 --taupe:%(taupe)s;--creme:%(creme)s;--creme-rose:%(creme_rose)s;
 --sable:%(sable)s;--sable-fonce:%(sable_fonce)s;--bleu:%(bleu)s;
 --violet:%(violet)s;--corail:%(corail)s;--turquoise:%(turquoise)s;
 --jaune:%(jaune)s;--blanc:#fff}
*{box-sizing:border-box}
body{margin:0;color:var(--encre);background:var(--blanc);
 font-family:'Inter','Noto Color Emoji',sans-serif;font-size:9.5pt;
 line-height:1.5;-webkit-font-smoothing:antialiased}

.couv{height:244mm;display:flex;flex-direction:column;
 justify-content:center;break-after:page}
.filet{height:7px;margin-bottom:26mm;background:linear-gradient(90deg,
 %(bleu)s 0%%,%(bleu_vif)s 18%%,%(turquoise)s 33%%,%(violet)s 52%%,
 %(magenta)s 70%%,%(corail)s 84%%,%(orange)s 94%%,%(jaune)s 100%%)}
.marque{font-size:8.4pt;font-weight:600;letter-spacing:.17em;
 text-transform:uppercase;color:var(--taupe);margin-bottom:8mm}
.couv h1{font-family:'Playfair',Georgia,serif;font-weight:800;
 font-size:31pt;line-height:1.08;margin:0 0 6mm;max-width:15cm}
.couv .sous{font-size:11.6pt;line-height:1.5;color:var(--brun);
 margin:0 0 12mm;max-width:14cm}
.couv .rappel{padding:5mm 6mm;background:var(--creme);
 border-left:3px solid var(--violet);font-size:9pt;color:var(--brun);
 max-width:15cm}

.semaine{font-family:'Playfair',serif;font-weight:800;font-size:17pt;
 margin:0 0 4mm;padding-bottom:2mm;border-bottom:2px solid var(--encre);
 break-after:avoid;break-before:page}
.semaine:first-of-type{break-before:auto}

.jour{margin:0 0 6mm;padding-bottom:4mm;
 border-bottom:1px solid var(--sable)}
.date{break-after:avoid}
.jour.vide{opacity:.55}
.date{display:flex;align-items:baseline;gap:3mm;margin-bottom:2.5mm}
.date .j{font-family:'Playfair',serif;font-weight:700;font-size:13pt}
.date .n{font-size:8pt;font-weight:600;letter-spacing:.12em;
 text-transform:uppercase;color:var(--taupe)}

.bloc{display:flex;gap:4mm;margin-bottom:3mm;break-inside:avoid}
.bloc .quand{flex:0 0 17mm;font-weight:800;font-size:10pt;
 padding-top:.6mm}
.bloc .corps{flex:1;min-width:0}
.bloc .titre{font-weight:600;font-size:10pt;margin-bottom:1.4mm}
.bloc .titre .etiq{display:inline-block;font-size:7.4pt;font-weight:800;
 letter-spacing:.08em;text-transform:uppercase;color:var(--blanc);
 background:var(--encre);padding:.6mm 1.6mm;border-radius:2px;
 vertical-align:1.5px;margin-right:2mm}
.etiq.ig{background:var(--violet)}
.etiq.story{background:var(--turquoise)}
.etiq.google{background:var(--bleu)}
.etiq.blog{background:var(--corail)}
.note{font-size:8.4pt;color:var(--taupe)}

.planches{display:flex;flex-wrap:wrap;gap:2mm;margin-top:1.5mm}
.planches figure{margin:0;width:22mm}
.planches img{width:100%%;height:auto;display:block;
 border:1px solid var(--sable-fonce);border-radius:1.5px}
.planches figcaption{font-size:6.6pt;color:var(--taupe);text-align:center;
 margin-top:.6mm}
.planches.stories figure{width:16mm}

.sortie{padding:2.5mm 3mm;background:var(--creme-rose);
 border-left:3px solid var(--corail);font-size:8.6pt;color:var(--brun)}
.repos{padding:2.5mm 3mm;background:var(--creme);
 border-left:3px solid var(--taupe);font-size:8.6pt;color:var(--brun)}
""" % C


def etiquette(canal):
    if canal.startswith("Instagram"):
        return "ig", "Instagram + Facebook"
    if canal == "Story":
        return "story", "Story"
    if canal.startswith("Fiche"):
        return "google", "Fiche Google"
    if canal == "Blog":
        return "blog", "Blog"
    return "", canal or "—"


def code_story(quoi):
    m = re.match(r"(S\d-[A-Z]\d?)", quoi)
    return m.group(1) if m else None


def document(lignes, dossiers):
    par_jour = {}
    for l in lignes:
        par_jour.setdefault(l["date"], []).append(l)

    # Les semaines commencent le lundi, comme le calendrier.
    pages, semaine_vue = [], None
    for jour in sorted(par_jour):
        lundi = jour - dt.timedelta(days=jour.weekday())
        if lundi != semaine_vue:
            semaine_vue = lundi
            fin = lundi + dt.timedelta(days=5)
            pages.append('<div class="semaine">Semaine du %d %s au %d %s</div>'
                         % (lundi.day, MOIS_L[lundi.month - 1],
                            fin.day, MOIS_L[fin.month - 1]))

        rangs = par_jour[jour]
        vide = all(r["sortie"] for r in rangs)
        bouts = ['<div class="jour%s">' % (" vide" if vide else "")]
        bouts.append('<div class="date"><span class="j">%s %d %s</span>'
                     '<span class="n">%s</span></div>'
                     % (JOURS[jour.weekday()].capitalize(), jour.day,
                        MOIS_L[jour.month - 1],
                        "aucune publication" if vide else ""))
        for r in rangs:
            if r["sortie"]:
                bouts.append('<div class="sortie">%s</div>'
                             % html.escape(re.sub(r"\*+|🛑 ?", "", r["quoi"])))
                continue
            if r["canal"] in ("—", ""):
                bouts.append('<div class="repos">%s</div>'
                             % html.escape(re.sub(r"\*+", "", r["quoi"])))
                continue
            cls, nom = etiquette(r["canal"])
            vignettes = ""
            if cls == "ig":
                for d in dossiers.get(jour, []):
                    fichiers = sorted(d.glob("*.png"))
                    vignettes += ('<div class="planches">%s</div>'
                                  % "".join(
                                      '<figure><img src="%s" alt="">'
                                      '<figcaption>%s</figcaption></figure>'
                                      % (vignette(f), f.stem)
                                      for f in fichiers))
            elif cls == "story":
                code = code_story(r["quoi"])
                f = VISUELS / "stories" / ("%s.png" % code) if code else None
                if f and f.exists():
                    vignettes = ('<div class="planches stories">'
                                 '<figure><img src="%s" alt="">'
                                 '<figcaption>%s</figcaption></figure></div>'
                                 % (vignette(f), code))
            bouts.append(
                '<div class="bloc"><div class="quand">%s</div>'
                '<div class="corps"><div class="titre">'
                '<span class="etiq %s">%s</span>%s</div>%s</div></div>'
                % (html.escape(r["heure"] or "—"), cls, html.escape(nom),
                   html.escape(re.sub(r"\*+", "", r["quoi"])), vignettes))
        bouts.append("</div>")
        pages.append("".join(bouts))

    couv = """<section class="couv">
  <div class="filet"></div>
  <div class="marque">Grafycom &middot; à programmer</div>
  <h1>Le calendrier,<br>avec les visuels</h1>
  <p class="sous">Du lundi 26 octobre au vendredi 11 décembre 2026.
  Chaque jour, ses publications, ses planches en vignettes et ses
  stories — dans l'ordre où elles partent.</p>
  <div class="rappel"><b>Les dates viennent de
  <code>calendrier.md</code></b>, les visuels de
  <code>reseaux/visuels/</code>, rapprochés par la date de leur
  dossier. Rien n'est saisi deux fois : un jour déplacé au calendrier
  se déplace ici au prochain passage.<br><br>
  <b>Seuls les articles paraissent tout seuls</b>, par le workflow du
  matin. Tout le reste se programme à la main.</div>
</section>"""
    return ("<!doctype html><html lang=fr><head><meta charset=utf-8>"
            "<title>Calendrier illustré</title><style>%s</style></head>"
            "<body>%s%s</body></html>"
            % (css(), couv, "".join(pages)))


async def imprime(provisoire, cible):
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
            margin={"top": "14mm", "bottom": "16mm",
                    "left": "14mm", "right": "14mm"},
            display_header_footer=True, header_template="<div></div>",
            footer_template=(
                "<div style='width:100%;font-size:7.2pt;color:#a2897c;"
                "font-family:sans-serif;padding:0 14mm;display:flex;"
                "justify-content:space-between'><span>Grafycom &middot; "
                "calendrier illustré</span>"
                "<span class='pageNumber'></span></div>"))
        await nav.close()
    return cible


def main():
    a = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    a.add_argument("--sortie", default=str(ICI / "pdf"))
    args = a.parse_args()

    TEMPO.mkdir(exist_ok=True)
    try:
        lignes = lignes_du_calendrier()
        dossiers = dossiers_par_date()
        print("  %d lignes datées, %d dossiers de visuels"
              % (len(lignes), len(dossiers)))
        sortie = pathlib.Path(args.sortie)
        sortie.mkdir(parents=True, exist_ok=True)
        provisoire = RACINE / ".calendrier-illustre.html"
        provisoire.write_text(document(lignes, dossiers), encoding="utf-8")
        try:
            cible = asyncio.run(imprime(provisoire,
                                        sortie / "calendrier-illustre.pdf"))
        finally:
            provisoire.unlink(missing_ok=True)
        print("\n%s — %.1f Mo" % (cible, cible.stat().st_size / 1e6))
    finally:
        shutil.rmtree(TEMPO, ignore_errors=True)


if __name__ == "__main__":
    main()
