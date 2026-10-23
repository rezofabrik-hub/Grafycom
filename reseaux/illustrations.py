#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les illustrations d'en-tête des articles du blog.

POURQUOI DES SCHÉMAS ET PAS DES IMAGES DÉCORATIVES
Un article de conseil se lit mieux avec une image qui dit quelque chose.
Une photo d'ambiance prise dans une banque d'images n'apprend rien et se
reconnaît ; un schéma qui explique le propos de l'article, lui, fait
gagner du temps au lecteur. Chaque illustration ici porte l'argument
central de son article.

CE QUE CE FICHIER NE FAIT PAS
Les photographies. Une devanture, une matière, un bon à tirer se
photographient — c'est le métier de Sandra, et une photo inventée sur le
compte d'une graphiste se retourne contre elle. Les emplacements où une
vraie photo vaudrait mieux qu'un schéma sont signalés par --photos.

LA CHARTE
Aucune couleur n'est écrite ici : tout vient de generateurs/charte.py,
qui lit la feuille de style du site. Une couleur hors charte arrête le
programme.

    python3 reseaux/illustrations.py            produit les illustrations
    python3 reseaux/illustrations.py --photos   liste les photos à faire
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
sys.path.insert(0, str(RACINE / "generateurs"))
from charte import C, DEGRADE  # noqa: E402
from charte import couleur as teinte  # noqa: E402

POLICES = ICI / "polices"
SORTIE = RACINE / "assets" / "img" / "blog"

# Format 1200x630 : celui des aperçus de partage. L'illustration sert
# donc deux fois, en tête d'article et dans la vignette qui s'affiche
# quand le lien est partagé.
LARGE, HAUT = 1200, 630


def police(nom, taille):
    f = POLICES / f"{nom}.ttf"
    if not f.exists():
        raise SystemExit(f"police manquante : {f}")
    return ImageFont.truetype(str(f), taille)


def rvb(nom):
    h = teinte(nom).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def fond():
    im = Image.new("RGB", (LARGE, HAUT), rvb("creme"))
    d = ImageDraw.Draw(im)
    # Le filet dégradé du site, en haut : la signature visuelle commune à
    # tous les supports.
    for x in range(LARGE):
        t = x / (LARGE - 1)
        for i in range(len(DEGRADE) - 1):
            p0, c0 = DEGRADE[i]
            p1, c1 = DEGRADE[i + 1]
            if p0 <= t <= p1:
                k = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                a = tuple(int(c0.lstrip("#")[j:j+2], 16) for j in (0, 2, 4))
                b = tuple(int(c1.lstrip("#")[j:j+2], 16) for j in (0, 2, 4))
                d.line([(x, 0), (x, 7)],
                       fill=tuple(round(a[j] + (b[j]-a[j])*k) for j in range(3)))
                break
    return im, d


def legende(d, x, y, texte, taille=21, couleur_nom="taupe", centre=False):
    f = police("Inter-600", taille)
    if centre:
        x -= f.getlength(texte) / 2
    d.text((x, y), texte, font=f, fill=rvb(couleur_nom))


def titre_bas(d, texte, couleur_nom="encre"):
    f = police("Playfair-700", 34)
    d.text((60, HAUT - 78), texte, font=f, fill=rvb(couleur_nom))


# ------------------------------------------------------------ enseigne

def illu_enseigne():
    """Une devanture, et le périmètre où l'autorisation s'impose.

    Le propos de l'article : ce n'est pas la taille de l'enseigne qui
    déclenche l'autorisation, c'est le lieu. Le schéma montre donc deux
    façades identiques, l'une hors périmètre, l'autre dedans.
    """
    im, d = fond()
    for i, (x, dedans) in enumerate([(130, False), (660, True)]):
        y, larg, haut = 120, 410, 300
        d.rounded_rectangle([x, y, x + larg, y + haut], radius=8,
                            fill=rvb("sable"))
        d.rectangle([x, y, x + larg, y + 74], fill=rvb("encre"))
        f = police("Playfair-800", 38)
        mot = "VOTRE NOM"
        d.text((x + (larg - f.getlength(mot)) / 2, y + 16), mot,
               font=f, fill=rvb("creme"))
        d.rectangle([x + 46, y + 116, x + larg - 46, y + haut - 34],
                    fill=rvb("sable_fonce"))
        if dedans:
            # Le périmètre protégé, en tirets : on le dessine à la main,
            # Pillow ne trace pas de pointillés.
            m = 26
            bx0, by0, bx1, by1 = x - m, y - m, x + larg + m, y + haut + m
            pas, trait = 22, 12
            for px in range(bx0, bx1, pas):
                d.line([(px, by0), (min(px + trait, bx1), by0)],
                       fill=rvb("corail"), width=3)
                d.line([(px, by1), (min(px + trait, bx1), by1)],
                       fill=rvb("corail"), width=3)
            for py in range(by0, by1, pas):
                d.line([(bx0, py), (bx0, min(py + trait, by1))],
                       fill=rvb("corail"), width=3)
                d.line([(bx1, py), (bx1, min(py + trait, by1))],
                       fill=rvb("corail"), width=3)
            legende(d, x + larg / 2, y + haut + 48,
                    "Secteur protégé : autorisation préalable",
                    22, "corail", centre=True)
        else:
            legende(d, x + larg / 2, y + haut + 48,
                    "Hors périmètre : pas d'autorisation",
                    22, "taupe", centre=True)
    titre_bas(d, "La même enseigne. Deux rues différentes.")
    return im


# ---------------------------------------------------------------- CMJN

def illu_cmjn():
    """Lumière contre encre : les deux procédés, côte à côte.

    C'est l'explication même de l'article. À gauche, trois faisceaux qui
    s'additionnent et donnent du blanc. À droite, trois encres qui se
    superposent et assombrissent.
    """
    im, d = fond()
    r = 96
    # Synthèse additive, sur fond sombre
    d.rounded_rectangle([70, 110, 570, 470], radius=16, fill=rvb("encre"))
    cx, cy = 320, 275
    add = Image.new("RGB", (500, 360), rvb("encre"))
    da = ImageDraw.Draw(add)
    for dx, dy, nom in ((0, -54, "corail"), (-50, 36, "turquoise"),
                        (50, 36, "bleu_vif")):
        c = Image.new("RGB", add.size, (0, 0, 0))
        ImageDraw.Draw(c).ellipse([250 + dx - r, 165 + dy - r,
                                   250 + dx + r, 165 + dy + r], fill=rvb(nom))
        add = Image.blend(add, Image.blend(add, c, 1.0), 0.0) if False else add
        da = ImageDraw.Draw(add)
        # addition : on éclaircit, canal par canal
        from PIL import ImageChops
        add = ImageChops.add(add, c)
    im.paste(add, (70, 110))
    d = ImageDraw.Draw(im)
    legende(d, 320, 492, "RVB · lumière · s'additionne vers le blanc",
            21, "brun", centre=True)

    # Synthèse soustractive, sur fond blanc
    d.rounded_rectangle([630, 110, 1130, 470], radius=16, fill=rvb("blanc"))
    sous = Image.new("RGB", (500, 360), rvb("blanc"))
    from PIL import ImageChops
    for dx, dy, nom in ((0, -54, "turquoise"), (-50, 36, "magenta"),
                        (50, 36, "jaune")):
        c = Image.new("RGB", sous.size, (255, 255, 255))
        ImageDraw.Draw(c).ellipse([250 + dx - r, 165 + dy - r,
                                   250 + dx + r, 165 + dy + r], fill=rvb(nom))
        sous = ImageChops.multiply(sous, c)
    im.paste(sous, (630, 110))
    d = ImageDraw.Draw(im)
    legende(d, 880, 492, "CMJN · encre · s'assombrit vers le noir",
            21, "brun", centre=True)
    titre_bas(d, "Deux procédés inverses. D'où l'écart.")
    return im


# -------------------------------------------------------------- droits

def illu_droits():
    """Vectoriel contre image aplatie, agrandis tous les deux.

    Le propos : un JPEG est une photo de votre logo, pas votre logo. On
    montre donc le même signe agrandi, net d'un côté, en marches de
    l'autre.
    """
    im, d = fond()
    for x0, pixelise, etiquette, teinte_nom in (
            (130, False, "Fichier vectoriel", "turquoise"),
            (660, True, "JPEG agrandi", "corail")):
        d.rounded_rectangle([x0, 120, x0 + 410, 420], radius=16,
                            fill=rvb("blanc"))
        vign = Image.new("RGB", (300, 220), rvb("blanc"))
        dv = ImageDraw.Draw(vign)
        f = police("Playfair-800", 150)
        dv.text((90, 20), "G", font=f, fill=rvb("violet"))
        dv.ellipse([38, 150, 74, 186], fill=rvb("rose"))
        if pixelise:
            # On écrase puis on réétire : c'est exactement ce que subit
            # une image matricielle qu'on agrandit.
            vign = vign.resize((26, 19), Image.BILINEAR)
            vign = vign.resize((300, 220), Image.NEAREST)
        im.paste(vign, (x0 + 55, 170))
        legende(d, x0 + 205, 444, etiquette, 22, teinte_nom, centre=True)
    titre_bas(d, "Un JPEG est une photo de votre logo. Pas votre logo.")
    return im



# ------------------------------------------------------------- vitrine

def illu_vitrine():
    """Les trois habillages, dans le meme cadre de vitrine.

    L'article compare depoli, microperfore et lettres decoupees. Montres
    cote a cote dans trois vitrines identiques, l'ecart se lit d'un coup :
    le depoli masque, le microperfore laisse voir de l'interieur, les
    lettres ne couvrent presque rien.
    """
    im, d = fond()
    x0, y, larg, haut = 90, 110, 320, 300
    for i, (titre, desc) in enumerate([
            ("Dépoli", "masque tout, laisse la lumière"),
            ("Microperforé", "opaque dehors, transparent dedans"),
            ("Lettres découpées", "on ne couvre que le dessin")]):
        x = x0 + i * 345
        # la vitre
        d.rectangle([x, y, x + larg, y + haut], fill=rvb("blanc"),
                    outline=rvb("sable_fonce"), width=3)
        d.rectangle([x, y + haut, x + larg, y + haut + 14],
                    fill=rvb("encre"))
        if i == 0:
            d.rectangle([x + 3, y + 3, x + larg - 3, y + haut - 3],
                        fill=rvb("sable"))
        elif i == 1:
            # la trame de perforation, dessinee point par point
            for py in range(y + 10, y + haut - 8, 9):
                for px in range(x + 10, x + larg - 8, 9):
                    d.ellipse([px, py, px + 4, py + 4], fill=rvb("taupe"))
        else:
            f = police("Playfair-800", 86)
            mot = "NOM"
            d.text((x + (larg - f.getlength(mot)) / 2, y + haut / 2 - 60),
                   mot, font=f, fill=rvb("encre"))
        legende(d, x + larg / 2, y + haut + 36, titre, 24, "encre",
                centre=True)
        legende(d, x + larg / 2, y + haut + 66, desc, 19, "taupe",
                centre=True)
    titre_bas(d, "Trois façons de couvrir une vitre. Trois effets.")
    return im


# --------------------------------------------------------- retroplanning

def illu_retroplanning():
    """Le compte a rebours, lu de droite a gauche.

    Tout le propos : on ne compte pas depuis aujourd'hui, on compte
    depuis la boite aux lettres. La frise est donc flechee vers la
    gauche, et les deux reperes nomment ses extremites.

    Recomptee le 23 octobre, en meme temps que l'article et le
    carrousel n° 17. Elle portait « reception / 24 dec. » et un total
    de 22 jours ouvres : la fenetre d'impression pour Noel s'etant
    fermee au 15 novembre, ce total n'avait plus de sens le 20. Les
    etapes ne portent donc plus des durees mais des MOMENTS, parce que
    le calendrier n'est plus continu — il s'arrete apres le bon a
    tirer et reprend en janvier.
    """
    im, d = fond()
    etapes = [("Création", "maintenant"), ("Bon à tirer", "décembre"),
              ("Impression", "janvier"), ("Réception", "mi-janvier")]
    cy = 250
    xs = [170, 450, 730, 1010]
    for i, (nom, delai) in enumerate(etapes):
        x = xs[i]
        d.ellipse([x - 42, cy - 42, x + 42, cy + 42], fill=rvb("corail"))
        fn = police("Inter-800", 38)
        n = str(i + 1)
        d.text((x - fn.getlength(n) / 2, cy - 26), n, font=fn,
               fill=rvb("blanc"))
        legende(d, x, cy + 64, nom, 23, "encre", centre=True)
        legende(d, x, cy + 94, delai, 20, "taupe", centre=True)
        if i < 3:                       # une fleche, vers la gauche
            xa, xb = xs[i + 1] - 58, x + 58
            if i == 1:
                # L'intervalle entre l'impression (janvier) et le bon a
                # tirer (decembre) est le seul ou RIEN ne se passe : le
                # fichier attend les fetes. Le legender sans le dessiner
                # laisserait la frise dire le contraire de sa propre
                # legende, donc ce trait-la est pointille.
                t = xa
                while t > xb + 18:
                    d.line([(t, cy), (max(t - 14, xb + 18), cy)],
                           fill=rvb("sable_fonce"), width=5)
                    t -= 26
                legende(d, (xa + xb) / 2, cy - 44, "les fêtes", 19, "taupe",
                        centre=True)
            else:
                d.line([(xa, cy), (xb + 18, cy)], fill=rvb("sable_fonce"),
                       width=5)
            d.polygon([(xb, cy), (xb + 22, cy - 12), (xb + 22, cy + 12)],
                      fill=rvb("sable_fonce"))
    legende(d, 170, cy - 92, "aujourd'hui", 20, "taupe", centre=True)
    legende(d, 1010, cy - 92, "la boîte aux lettres", 20, "taupe",
            centre=True)
    titre_bas(d, "Le calendrier se coupe en deux, et on compte à rebours.")
    return im


# ------------------------------------------------------------ trottoir

def illu_trottoir():
    """Ce qui reste lisible a mesure qu'on s'eloigne.

    La meme vitrine, vue de 3, 10 et 20 metres. Le detail disparait, le
    contraste reste : c'est exactement ce que l'article demande de
    hierarchiser avant de decorer.
    """
    im, d = fond()
    from PIL import ImageFilter
    for i, (dist, flou, lignes) in enumerate([("3 m", 0, 3), ("10 m", 2, 2),
                                              ("20 m", 5, 1)]):
        x, y, larg, haut = 90 + i * 345, 115, 320, 290
        vitre = Image.new("RGB", (larg, haut), rvb("encre"))
        dv = ImageDraw.Draw(vitre)
        f = police("Playfair-800", 54)
        mot = "NOËL"
        dv.text(((larg - f.getlength(mot)) / 2, 46), mot, font=f,
                fill=rvb("jaune"))
        fp = police("Inter-400", 21)
        petits = ["ouvert le dimanche", "idées cadeaux à partir de 12 €",
                  "emballage offert"]
        for j in range(3):
            if j < 3 - i:
                dv.text(((larg - fp.getlength(petits[j])) / 2, 140 + j * 34),
                        petits[j], font=fp, fill=rvb("creme"))
        if flou:
            vitre = vitre.filter(ImageFilter.GaussianBlur(flou))
        im.paste(vitre, (x, y))
        d.rectangle([x, y, x + larg, y + haut], outline=rvb("sable_fonce"),
                    width=3)
        legende(d, x + larg / 2, y + haut + 30, dist, 24, "encre",
                centre=True)
        legende(d, x + larg / 2, y + haut + 60,
                "%d ligne%s lisible%s" % (lignes, "s" if lignes > 1 else "",
                                          "s" if lignes > 1 else ""),
                19, "taupe", centre=True)
    titre_bas(d, "À vingt mètres, il ne reste qu'un mot. Choisissez-le.")
    return im


# --------------------------------------------------------------- bilan

def illu_bilan():
    """Trois questions, et ce que repond chaque combinaison.

    L'article refuse la refonte par calendrier et propose un diagnostic.
    Le schema est ce diagnostic : trois cases, puis la conclusion.
    """
    im, d = fond()
    questions = ["Lisible partout ?", "Fichiers en main ?",
                 "Dit-il ce que vous vendez ?"]
    for i, q in enumerate(questions):
        x, y, larg, haut = 90, 100 + i * 96, 700, 72
        d.rounded_rectangle([x, y, x + larg, y + haut], radius=10,
                            fill=rvb("blanc"), outline=rvb("sable"), width=2)
        d.ellipse([x + 22, y + 20, x + 54, y + 52], fill=rvb("violet"))
        fn = police("Inter-800", 20)
        d.text((x + 32, y + 26), str(i + 1), font=fn, fill=rvb("blanc"))
        legende(d, x + 74, y + 24, q, 24, "encre")
    # la conclusion, a droite
    bx = 840
    d.rounded_rectangle([bx, 100, bx + 270, 196], radius=10,
                        fill=rvb("creme_rose"))
    legende(d, bx + 135, 124, "Un « non »", 23, "encre", centre=True)
    legende(d, bx + 135, 154, "on ajuste", 21, "turquoise", centre=True)
    d.rounded_rectangle([bx, 292, bx + 270, 388], radius=10,
                        fill=rvb("encre"))
    legende(d, bx + 135, 316, "Trois « non »", 23, "blanc", centre=True)
    legende(d, bx + 135, 346, "on redessine", 21, "jaune", centre=True)
    titre_bas(d, "Un bilan, pas une résolution.")
    return im


ILLUSTRATIONS = {
    "autorisation-enseigne-perpignan": ("enseigne.png", illu_enseigne),
    "couleurs-impression-ecran-cmjn": ("cmjn.png", illu_cmjn),
    "qui-possede-votre-logo": ("droits.png", illu_droits),
    "habiller-sa-vitrine-66": ("vitrine.png", illu_vitrine),
    "supports-fin-annee-66": ("retroplanning.png", illu_retroplanning),
    "vitrine-fin-annee-trottoir": ("trottoir.png", illu_trottoir),
    "refaire-son-logo-nouvelle-annee": ("bilan.png", illu_bilan),
}

# Là où une vraie photo vaudrait mieux qu'un schéma. Sandra les prend ;
# ce script ne les invente pas.
PHOTOS_A_FAIRE = [
    ("autorisation-enseigne-perpignan",
     "Une devanture réelle du centre ancien de Perpignan ou de "
     "Villefranche, enseigne comprise, prise de face."),
    ("couleurs-impression-ecran-cmjn",
     "Un bon à tirer posé à côté de l'écran qui affiche le même visuel : "
     "l'écart de couleur se voit, aucun schéma ne le remplace."),
    ("couleurs-impression-ecran-cmjn",
     "Un nuancier Pantone ouvert, en lumière du jour."),
    ("qui-possede-votre-logo",
     "Un jeu de fichiers sources ouvert sur l'écran, avec les calques — "
     "ce que le client reçoit vraiment."),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--photos", action="store_true",
                    help="lister les photographies à faire")
    a = ap.parse_args()

    if a.photos:
        print("Photographies à prendre — elles ne s'inventent pas :\n")
        for slug, quoi in PHOTOS_A_FAIRE:
            print(f"  [{slug}]\n    {quoi}\n")
        return 0

    SORTIE.mkdir(parents=True, exist_ok=True)
    for slug, (nom, fabrique) in ILLUSTRATIONS.items():
        im = fabrique()
        assert im.size == (LARGE, HAUT), "format non conforme"
        chemin = SORTIE / nom
        im.save(chemin, "PNG", optimize=True)
        print(f"  {chemin.relative_to(RACINE)}   ({slug})")
    print(f"\n{len(ILLUSTRATIONS)} illustration(s), {LARGE}x{HAUT}, "
          "couleurs de la charte uniquement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
