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


SOURCES = ICI / "propositions/a-valider"


def sections(fichier, motif):
    """Découpe un document en sections « ## », indexées par leur clé.

    Les trois documents de textes sont bâtis pareil : un « ## » par
    élément, et tout ce qui suit lui appartient jusqu'au suivant. On
    ne parse donc pas le contenu — on le découpe et on le rend tel
    quel. C'est ce qui permet d'avaler aussi bien les sections en
    liste à puces que celles en tableau, sans les connaître.
    """
    t = (SOURCES / fichier).read_text(encoding="utf-8")
    out, cle, corps = {}, None, []
    for ligne in t.split("\n"):
        if ligne.startswith("## "):
            if cle:
                out[cle] = "\n".join(corps).strip()
            m = re.match(motif, ligne[3:])
            cle, corps = (m.group(1) if m else None), []
        elif cle:
            corps.append(ligne)
    if cle:
        out[cle] = "\n".join(corps).strip()
    return out


def en_ligne(s):
    """Gras, italique, code — après échappement."""
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\\([*_`])", r"\1", s)
    return s


def fragment(md, sauter=()):
    """Un morceau de markdown en HTML : paragraphes, listes, citations,
    tableaux. Les sous-titres « ### » nommés dans `sauter` emportent
    leur section — c'est ainsi qu'on laisse de côté la direction
    visuelle d'une publication, que les vignettes montrent déjà.
    """
    out, liste, para, cite, tab = [], False, [], [], []

    def vider():
        nonlocal liste
        if para:
            out.append("<p>%s</p>" % en_ligne(" ".join(para)))
            para.clear()
        if cite:
            out.append('<blockquote>%s</blockquote>'
                       % "".join("<p>%s</p>" % en_ligne(" ".join(par))
                                 for par in cite if par))
            cite.clear()
        if tab:
            lignes = [l for l in tab if not re.match(r"^\|[-:\s|]+\|$", l)]
            rangs = []
            for l in lignes:
                cases = [c.strip() for c in l.strip().strip("|").split("|")]
                rangs.append("".join("<td>%s</td>" % en_ligne(c)
                                     for c in cases))
            out.append("<table>%s</table>"
                       % "".join("<tr>%s</tr>" % r for r in rangs))
            tab.clear()
        if liste:
            out.append("</ul>")
            liste = False

    ignore = False
    for brute in md.split("\n"):
        l = brute.strip()
        if l.startswith("### "):
            vider()
            ignore = any(s.lower() in l.lower() for s in sauter)
            if not ignore:
                out.append("<h4>%s</h4>" % en_ligne(l[4:]))
            continue
        if ignore or l.startswith("---"):
            continue
        if not l:
            vider()
            continue
        if l.startswith("|"):
            if para or cite:
                vider()
            tab.append(l)
            continue
        if tab:
            vider()
        if l == ">" or l.startswith("> "):
            if para:
                vider()
            if l == ">":
                cite.append([])
            else:
                if not cite:
                    cite.append([])
                cite[-1].append(l[2:])
            continue
        if cite:
            vider()
        m = re.match(r"^[-*]\s+(.*)$", l)
        if m:
            if para:
                vider()
            if not liste:
                out.append("<ul>")
                liste = True
            out.append("<li>%s</li>" % en_ligne(m.group(1)))
            continue
        if liste and brute[:1] in " \t" and out and \
                out[-1].endswith("</li>"):
            out[-1] = out[-1][:-5] + " " + en_ligne(l) + "</li>"
            continue
        if liste:
            vider()
        para.append(l)
    vider()
    return "".join(out)


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

.bloc{display:flex;gap:4mm;margin-bottom:3mm}
.bloc .quand{flex:0 0 17mm;font-weight:800;font-size:10pt;
 padding-top:.6mm}
.bloc .corps{flex:1;min-width:0}
.bloc .titre{font-weight:600;font-size:10pt;margin-bottom:1.4mm;
 break-after:avoid}
.bloc .titre .etiq{display:inline-block;font-size:7.4pt;font-weight:800;
 letter-spacing:.08em;text-transform:uppercase;color:var(--blanc);
 background:var(--encre);padding:.6mm 1.6mm;border-radius:2px;
 vertical-align:1.5px;margin-right:2mm}
.etiq.ig{background:var(--violet)}
.etiq.story{background:var(--turquoise)}
.etiq.google{background:var(--bleu)}
.etiq.blog{background:var(--corail)}
.note{font-size:8.4pt;color:var(--taupe)}

.planches{display:flex;flex-wrap:wrap;gap:2mm;margin-top:1.5mm;
 break-inside:avoid}
.planches figure{margin:0;width:22mm}
.planches img{width:100%%;height:auto;display:block;
 border:1px solid var(--sable-fonce);border-radius:1.5px}
.planches figcaption{font-size:6.6pt;color:var(--taupe);text-align:center;
 margin-top:.6mm}
.planches.stories figure{width:16mm}

.texte{margin:2mm 0 0;padding:3mm 3.5mm;background:var(--creme);
 border-left:3px solid var(--sable-fonce);font-size:8.8pt;
 line-height:1.55}
.texte.copier{background:var(--creme-rose);border-left-color:var(--violet)}
.texte h4{font-family:'Inter',sans-serif;font-size:7.4pt;font-weight:800;
 letter-spacing:.1em;text-transform:uppercase;color:var(--taupe);
 margin:0 0 1.4mm;break-after:avoid}
.texte h4 ~ h4{margin-top:3.4mm}
.texte p{margin:0 0 1.8mm}
.texte p:last-child{margin-bottom:0}
.texte ul{margin:0 0 1.8mm;padding-left:4mm}
.texte li{margin-bottom:.8mm}
.texte blockquote{margin:0 0 1.8mm;padding:0 0 0 2.5mm;
 border-left:2px solid var(--sable-fonce);color:var(--encre)}
.texte table{border-collapse:collapse;width:100%%;margin:0 0 1.8mm}
.texte td{border:1px solid var(--sable-fonce);padding:1.2mm 1.8mm;
 vertical-align:top;font-size:8.4pt}
.texte td:first-child{width:28mm;color:var(--taupe)}
.texte code{font-size:8pt;background:var(--sable);padding:0 .8mm;
 border-radius:1.5px}
.hash{font-size:8.2pt;color:var(--bleu);word-break:break-word}

.sortie{padding:2.5mm 3mm;background:var(--creme-rose);
 border-left:3px solid var(--corail);font-size:8.6pt;color:var(--brun)}
.repos{padding:2.5mm 3mm;background:var(--creme);
 border-left:3px solid var(--taupe);font-size:8.6pt;color:var(--brun)}

.emploi h2{font-family:'Playfair',serif;font-weight:800;font-size:16.5pt;
 margin:0 0 2mm;padding-bottom:2mm;border-bottom:2px solid var(--encre)}
.emploi .chapeau{font-size:9pt;line-height:1.45;color:var(--brun);
 margin:0 0 4mm;max-width:15cm}
.emploi .colonnes{column-count:2;column-gap:7mm}
.regle{break-inside:avoid;margin:0 0 3.2mm;padding-left:6.6mm;
 position:relative}
.regle .num{position:absolute;left:0;top:.3mm;width:4.4mm;height:4.4mm;
 border-radius:50%%;background:var(--violet);color:var(--blanc);
 font-size:7pt;font-weight:800;line-height:4.4mm;text-align:center}
.regle h3{font-size:8.9pt;font-weight:800;margin:0 0 1mm;line-height:1.28}
.regle p{margin:0;font-size:8.2pt;line-height:1.42;color:var(--brun)}
.regle ul{margin:.9mm 0 0;padding-left:4mm;font-size:8pt;
 color:var(--brun)}
.regle li{margin-bottom:.3mm}
.regle b{color:var(--encre)}
.regle code{font-size:8pt;background:var(--sable);padding:0 .8mm;
 border-radius:1.5px}
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


def texte_story(code, stor):
    """Le texte d'un écran, ou celui de la séquence qui le contient.

    Les séquences à deux écrans portent un chiffre au calendrier —
    S1-B1 et S1-B2 — mais six d'entre elles tiennent dans une seule
    section de `stories.md`, qui décrit les deux à la suite. Six
    écrans sortaient donc sans leur texte, en silence. On retombe sur
    la séquence : elle dit les deux, c'est ce qu'il faut lire.
    """
    if not code:
        return None
    if code in stor:
        return stor[code]
    if code[-1].isdigit() and code[:-1] in stor:
        return stor[code[:-1]]
    return None


def numero(quoi):
    """« n° 15 bis — ... » -> « 15 bis ». La clé des deux documents.

    Le gras du calendrier — `**n° 4 bis · annonce du blog**` — tombait
    ici : la publication était la seule en gras de la colonne, et son
    texte manquait sans que rien ne le dise.
    """
    m = re.match(r"n° (\d+(?: bis)?)", quoi.strip().strip("*").strip())
    return m.group(1) if m else None


# Les gestes qui ne se répètent pas jour après jour.
#
# Chacun existe dans les documents sources, mais une seule fois, à
# l'endroit où il s'applique d'abord : le sticker « Mention du post »
# est expliqué au premier teasing, la règle des deux heures en tête du
# calendrier, les trois champs de la fiche Google en tête de
# `fiche-google.md`. Quelqu'un qui programme le 15 novembre en suivant
# ce PDF ne les a jamais lus. Ils sont donc rassemblés ici, en tête, et
# aucun n'est inventé : chacun vient de `instagram-facebook.md`,
# `stories.md`, `calendrier.md`, `fiche-google.md`,
# `messages-prives.md` ou `arbitrages.md`.
REGLES = (
    ("Facebook part avec Instagram, sans rien refaire",
     "Les deux comptes sont synchronisés depuis Meta Business Suite : "
     "un contenu préparé pour Instagram paraît sur les deux. Aucune "
     "ligne de ce document ne demande un second passage côté "
     "Facebook."),

    ("Les stickers dessinés ne sont que des dessins",
     "Sondage, quiz, curseur emoji, boîte à questions : ce qu'on voit "
     "sur la vignette est l'illustration du sticker, pas le sticker. "
     "Le vrai se pose par-dessus dans Instagram au moment de publier, "
     "avec les options exactes écrites dans le cadre du jour. Sans ce "
     "geste, <b>personne ne peut répondre</b>, et l'écran ne sert à "
     "rien."),

    ("Le sticker « Mention du post »",
     "Quatorze écrans de teasing le portent : il renvoie au carrousel "
     "du même jour. Il se pose <b>après</b> le sticker interactif, et "
     "il n'a pas d'option à régler. Le carrousel doit donc être publié "
     "avant la story qui l'annonce — c'est pour cela que les teasings "
     "suivent d'un quart d'heure."),

    ("La réponse d'un quiz tombe deux heures après",
     "Chaque question a sa propre ligne dans les pages suivantes, et "
     "sa réponse en a une autre, deux heures plus tard. L'écart est "
     "voulu : assez pour qu'on réponde, assez tôt pour qu'on voie le "
     "résultat. Publier la réponse plus tôt annule la question."),

    ("Sept écrans vont en story à la une",
     "Ils portent une étoile dans leur cadre. Une story disparaît en "
     "24 h, et ceux-là sont les plus consultés de l'année sur leur "
     "sujet. Cinq collections, chacune à créer au premier écran qui "
     "lui revient :"
     "<ul>"
     "<li>« Réglementation » — couverture violette</li>"
     "<li>« Vitrines » — couverture violette <code>#a86cd0</code></li>"
     "<li>« Impression » — couverture bleue</li>"
     "<li>« Supports » — couverture bleu profond</li>"
     "<li>« Identité » — couverture bleu profond "
     "<code>#2f7fc4</code></li>"
     "</ul>"),

    ("Une seule publication s'épingle",
     "La <b>n° 4 bis</b>, « un nouvel article chaque vendredi », le "
     "samedi 31 octobre à 10 h 30. Elle s'épingle en haut du profil, "
     "et elle va aussi en story à la une — couverture crème, titre "
     "« Le blog ». C'est le seul épinglage prévu sur les sept "
     "semaines."),

    ("Les articles paraissent tout seuls",
     "Le passage du matin tourne à 8 h 07 : il relance le générateur "
     "et publie. Un article sort quand son en-tête porte "
     "<code>statut: validé</code> <b>et</b> que sa date est arrivée. "
     "Il n'y a rien à faire ce jour-là — sauf vérifier que la page est "
     "bien en ligne <b>avant</b> de poser le sticker Lien de la story "
     "qui la relaie."),

    ("La fiche Google se règle avant le premier texte",
     "Trois champs comptent plus que tout le reste : la <b>catégorie "
     "principale</b> <code>Graphiste</code>, qui décide sur quelles "
     "recherches la fiche apparaît ; la <b>zone desservie</b> avec "
     "l'affichage de l'adresse <b>décoché</b> ; et le <b>nom</b>, "
     "<code>Grafycom</code> seul. La liste complète, valeurs exactes "
     "comprises, est en tête de <code>outils/FICHE-GOOGLE.md</code>. "
     "Dix minutes, une fois pour toutes."),

    ("Le texte alternatif ne va pas dans la légende",
     "Chaque cadre rosé en porte un, sous son titre. Il se colle dans "
     "le champ « texte alternatif » des paramètres avancés, à l'écran "
     "de publication. Collé dans la légende, il la double."),

    ("Les messages privés ne se programment pas",
     "Cinq textes de référence attendent dans "
     "<code>messages-prives.md</code>, au tutoiement. Ce sont des "
     "réponses écrites d'avance pour ne pas avoir à les improviser un "
     "soir de fatigue, pas des envois : chacune s'adapte à la personne "
     "qui écrit."),

    ("Trois mardis sont vides, et c'est voulu",
     "Les 17 et 24 novembre et le 1<sup>er</sup> décembre apparaissent "
     "en gris. Les trois carrousels qui s'y trouvaient — n° 14, 18 et "
     "22 — sont sortis du calendrier le 23 octobre : leur point de "
     "réglementation n'était pas confirmé, et rien ne part sur du non "
     "vérifié. Leurs textes de fiche Google et leurs stories sont "
     "partis avec eux."),

    ("Montrer un client suppose son accord",
     "Une seule publication montre un vrai projet : <b>Solaire 66</b>, "
     "le mercredi 25 novembre, et l'accord y est acquis. Toute autre "
     "réalisation ajoutée plus tard demande le sien avant de partir, "
     "même quand le contrat cède les droits."),

    ("Les vignettes d'ici ne sont pas les fichiers à publier",
     "Elles sont réduites à 300 px de large pour que ce document reste "
     "ouvrable. Les planches en pleine définition sont dans "
     "<code>reseaux/visuels/</code>, un dossier par jour, un PNG par "
     "planche — et l'ordre de leurs noms est l'ordre du carrousel."),

    ("Rien ne part sans ta validation",
     "Ce document est une proposition, ses dates et ses heures "
     "comprises : les créneaux sont choisis, pas imposés. Une seule "
     "chose s'y déclenche seule, le passage du matin pour les "
     "articles. Tout le reste attend que quelqu'un appuie."),
)


def mode_emploi():
    """La page de tête : ce qui vaut pour tout le cycle."""
    regles = "".join(
        '<div class="regle"><div class="num">%d</div>'
        '<h3>%s</h3><p>%s</p></div>' % (i, titre, corps)
        for i, (titre, corps) in enumerate(REGLES, 1))
    return """<section class="emploi">
  <h2>Mode d'emploi</h2>
  <p class="chapeau">Quatorze gestes qui ne sont pas répétés jour après
  jour dans les pages suivantes, parce qu'ils valent pour tout le
  cycle. Les lire une fois suffit, et y revenir quand une journée
  renvoie ici.</p>
  <div class="colonnes">%s</div>
</section>""" % regles


def document(lignes, dossiers, textes=True):
    pubs = sections("instagram-facebook.md", r"(\d+(?: bis)?) —") if textes else {}
    goog = sections("fiche-google.md", r"(\d+(?: bis)?) —") if textes else {}
    stor = sections("stories.md", r"(S\d-[A-Z]\d?) —") if textes else {}
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
            vignettes, corps = "", ""
            if cls == "ig":
                for d in dossiers.get(jour, []):
                    fichiers = sorted(d.glob("*.png"))
                    vignettes += ('<div class="planches">%s</div>'
                                  % "".join(
                                      '<figure><img src="%s" alt="">'
                                      '<figcaption>%s</figcaption></figure>'
                                      % (vignette(f), f.stem)
                                      for f in fichiers))
                n = numero(r["quoi"])
                if n and n in pubs:
                    corps = ('<div class="texte copier">%s</div>'
                             % fragment(pubs[n],
                                        sauter=("direction visuelle",)))
            elif cls == "story":
                code = code_story(r["quoi"])
                f = VISUELS / "stories" / ("%s.png" % code) if code else None
                if f and f.exists():
                    vignettes = ('<div class="planches stories">'
                                 '<figure><img src="%s" alt="">'
                                 '<figcaption>%s</figcaption></figure></div>'
                                 % (vignette(f), code))
                txt = texte_story(code, stor)
                if txt:
                    corps = '<div class="texte">%s</div>' % fragment(txt)
            elif cls == "google":
                n = numero(re.sub(r"^texte ", "",
                                  r["quoi"].strip().strip("*").strip()))
                if n and n in goog:
                    corps = ('<div class="texte copier">%s</div>'
                             % fragment(goog[n]))
            bouts.append(
                '<div class="bloc"><div class="quand">%s</div>'
                '<div class="corps"><div class="titre">'
                '<span class="etiq %s">%s</span>%s</div>%s</div></div>'
                % (html.escape(r["heure"] or "—"), cls, html.escape(nom),
                   html.escape(re.sub(r"\*+", "", r["quoi"])),
                   vignettes + corps))
        bouts.append("</div>")
        pages.append("".join(bouts))

    couv = """<section class="couv">
  <div class="filet"></div>
  <div class="marque">Grafycom &middot; à programmer</div>
  <h1>Tout ce qui part,<br>dans l'ordre</h1>
  <p class="sous">Du lundi 26 octobre au vendredi 11 décembre 2026.
  Chaque jour, à chaque heure : les planches, la légende à copier, les
  hashtags, le texte alternatif, le sticker de la story et le texte de
  la fiche Google. Tout au même endroit, rien à aller chercher
  ailleurs.</p>
  <div class="rappel"><b>Les dates viennent de
  <code>calendrier.md</code></b>, les visuels de
  <code>reseaux/visuels/</code>, rapprochés par la date de leur
  dossier. Rien n'est saisi deux fois : un jour déplacé au calendrier
  se déplace ici au prochain passage.<br><br>
  <b>Seuls les articles paraissent tout seuls</b>, par le workflow du
  matin. Tout le reste se programme à la main.<br><br>
  <b>Les cadres rosés se copient tels quels</b> — légende, hashtags,
  texte de fiche Google. Les cadres crème sont des consignes : ce
  qu'il faut poser dans l'application, ou vérifier avant d'envoyer.
  <br><br>
  <b>La page suivante réunit les quatorze gestes</b> qui valent pour
  tout le cycle et qui ne sont donc pas réécrits chaque jour : les
  vrais stickers à poser, les stories à la une, l'épinglage, le
  réglage de la fiche Google. Elle se lit une fois.</div>
</section>"""
    return ("<!doctype html><html lang=fr><head><meta charset=utf-8>"
            "<title>Calendrier illustré</title><style>%s</style></head>"
            "<body>%s%s%s</body></html>"
            % (css(), couv, mode_emploi() if textes else "",
               "".join(pages)))


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
    a.add_argument("--court", action="store_true",
                   help="les visuels seuls, sans les textes")
    args = a.parse_args()

    TEMPO.mkdir(exist_ok=True)
    try:
        lignes = lignes_du_calendrier()
        dossiers = dossiers_par_date()
        print("  %d lignes datées, %d dossiers de visuels"
              % (len(lignes), len(dossiers)))
        sortie = pathlib.Path(args.sortie)
        sortie.mkdir(parents=True, exist_ok=True)
        nom = ("calendrier-illustre.pdf" if args.court
               else "tout-en-un.pdf")
        provisoire = RACINE / ".calendrier-illustre.html"
        provisoire.write_text(document(lignes, dossiers,
                                       textes=not args.court),
                              encoding="utf-8")
        try:
            cible = asyncio.run(imprime(provisoire, sortie / nom))
        finally:
            provisoire.unlink(missing_ok=True)
        print("\n%s — %.1f Mo" % (cible, cible.stat().st_size / 1e6))
    finally:
        shutil.rmtree(TEMPO, ignore_errors=True)


if __name__ == "__main__":
    main()
