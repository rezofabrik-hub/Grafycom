# -*- coding: utf-8 -*-
"""Le markdown des articles : en-tête, mise en ligne, conversion.

Pourquoi un fichier à part
--------------------------
Deux programmes lisent les mêmes articles et doivent en tirer exactement
le même HTML : `generateurs/p_blog.py`, qui fabrique les pages du site,
et `reseaux/articles.py`, qui fabrique le PDF de relecture. Si la
conversion était écrite deux fois, le PDF finirait par montrer autre
chose que la page — et c'est précisément sur ce PDF qu'on valide.

Importer `p_blog` depuis le PDF ne marchait pas : l'import *est* la
fabrication du site, chez `gen.py`. D'où ce module, qui ne fait rien
tout seul.

Les deux marques de mise en page sont documentées au-dessus de
`convertir`.
"""
import html as _html
import pathlib
import re

RACINE = pathlib.Path(__file__).resolve().parent.parent

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


# Une image posee AU MILIEU de l'article, et un exergue : les deux
# marques qui separent un article de blog d'un article de magazine.
# Elles s'ecrivent sur une ligne a elles, et se lisent encore comme une
# consigne si quelqu'un ouvre le markdown brut.
#
#   [figure: nom.png | La legende visible | La description alternative]
#   [exergue: La phrase mise en exergue]
#
# Les trois champs de la figure sont obligatoires, y compris le
# troisieme : une image sans description alternative est illisible pour
# qui n'y voit pas, et p_blog.py refuse deja celle d'en-tete sans alt.
FIGURE = re.compile(r"^\[figure\s*:\s*(.+?)\s*\]$")
EXERGUE = re.compile(r"^\[exergue\s*:\s*(.+?)\s*\]$")


def taille_png(chemin) -> tuple[int, int]:
    """Les dimensions d'un PNG, lues dans son en-tête IHDR.

    Les dire au navigateur n'est pas un détail : sans elles, le PDF de
    relecture posait la légende et rien au-dessus — une figure en
    « column-span » dont le ratio n'est pas connu se replie à zéro. Sur
    le site, elles évitent en prime que le texte saute au chargement.

    Lu à la main plutôt qu'avec Pillow : ce module est importé par les
    générateurs du site, et il n'a aucune dépendance.
    """
    e = chemin.read_bytes()[:24]
    if e[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("%s n'est pas un PNG" % chemin.name)
    return (int.from_bytes(e[16:20], "big"), int.from_bytes(e[20:24], "big"))


def figure_en_ligne(champs: str, ou: str = "") -> str:
    parts = [p.strip() for p in champs.split("|")]
    if len(parts) != 3 or not all(parts):
        raise SystemExit(
            "%s : « [figure: ...] » attend trois champs séparés par « | » "
            "— fichier, légende, description alternative. Reçu : %r"
            % (ou or "un article", champs))
    fichier, legende, alt = parts
    chemin = RACINE / "assets" / "img" / "blog" / fichier
    if not chemin.exists():
        raise SystemExit("%s : figure introuvable — assets/img/blog/%s"
                         % (ou or "un article", fichier))
    larg, haut = taille_png(chemin)
    return ('<figure class="figure-article">'
            '<img src="assets/img/blog/%s" alt="%s" width="%d" height="%d" '
            'loading="lazy"><figcaption>%s</figcaption></figure>'
            % (_html.escape(fichier, quote=True),
               _html.escape(alt, quote=True), larg, haut, en_ligne(legende)))


def convertir(markdown: str, ou: str = "") -> tuple[str, str]:
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
            # Un « > » qui commence par ⚠️ est un avertissement, pas une
            # citation : il se compose en encadré et non en retrait.
            classe = ' class="alerte"' if citation[0].startswith("⚠️") else ""
            sortie.append("<blockquote%s><p>%s</p></blockquote>"
                          % (classe, " ".join(citation)))
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

        m = FIGURE.match(l)
        if m:
            ferme()
            sortie.append(figure_en_ligne(m.group(1), ou))
            continue
        m = EXERGUE.match(l)
        if m:
            ferme()
            sortie.append('<p class="exergue">%s</p>' % en_ligne(m.group(1)))
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

        # Une puce qui tient sur deux lignes dans le fichier : la
        # seconde est indentee, et elle appartient a l'item precedent.
        # Sans ce cas, elle fermait la liste et devenait un paragraphe —
        # « au-dela de trois dispositifs, le formulaire doit etre rempli
        # une » d'un cote, « seconde fois. » de l'autre, et la numerotation
        # de la liste suivante repartait a 1. Le defaut etait sur le site
        # avant d'etre dans le PDF ; c'est le PDF qui l'a montre.
        if liste and brute[:1] in " \t" and sortie and \
                sortie[-1].endswith("</li>"):
            sortie[-1] = sortie[-1][:-5] + " " + en_ligne(l) + "</li>"
            continue

        if liste:
            ferme()
        paragraphe.append(l)

    ferme()
    return titre, "\n".join(sortie)
