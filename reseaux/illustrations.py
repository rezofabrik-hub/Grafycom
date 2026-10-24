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


def ecrire(d, x, y, texte, nom, taille, couleur_nom="encre",
           centre=False):
    """Pose un texte et renvoie sa largeur. Centre sur x si demandé."""
    f = police(nom, taille)
    l = f.getlength(texte)
    d.text((x - l / 2 if centre else x, y), texte, font=f,
           fill=rvb(couleur_nom))
    return l


def pave(d, x, y, texte, nom, taille, largeur, couleur_nom="brun",
         interligne=1.26):
    """Pose un texte en le coupant à `largeur`. Renvoie le bas atteint.

    `ecrire` ne pose qu'une ligne, et une ligne trop longue sort du
    cadre sans prévenir — c'est exactement ce qui est arrivé aux trois
    légendes de `illu_cmjn_coupe` au premier jet, dont la fin tombait
    hors de l'image. Mesurer avant d'écrire coûte six lignes.
    """
    f = police(nom, taille)
    lignes, courante = [], ""
    for mot in texte.split():
        essai = (courante + " " + mot).strip()
        if f.getlength(essai) <= largeur or not courante:
            courante = essai
        else:
            lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    pas = round(taille * interligne)
    for i, ligne in enumerate(lignes):
        d.text((x, y + i * pas), ligne, font=f, fill=rvb(couleur_nom))
    return y + len(lignes) * pas


def tirets(d, p0, p1, couleur_nom, largeur=3, pas=22, trait=12):
    """Une ligne en pointillés — Pillow n'en trace pas."""
    x0, y0 = p0
    x1, y1 = p1
    longueur = max(abs(x1 - x0), abs(y1 - y0))
    if not longueur:
        return
    dx, dy = (x1 - x0) / longueur, (y1 - y0) / longueur
    n = 0
    while n < longueur:
        m = min(n + trait, longueur)
        d.line([(x0 + dx * n, y0 + dy * n), (x0 + dx * m, y0 + dy * m)],
               fill=rvb(couleur_nom), width=largeur)
        n += pas


def cadre_tirets(d, boite, couleur_nom, largeur=3, pas=22, trait=12):
    x0, y0, x1, y1 = boite
    for a, b in (((x0, y0), (x1, y0)), ((x0, y1), (x1, y1)),
                 ((x0, y0), (x0, y1)), ((x1, y0), (x1, y1))):
        tirets(d, a, b, couleur_nom, largeur, pas, trait)


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


def illu_enseigne_sequence():
    """Les cinq étapes, dans l'ordre, et la branche qui s'y ajoute.

    L'article les donne en liste. Une liste se lit mal en diagonale ;
    une suite numérotée se retient. La branche de l'architecte des
    Bâtiments de France est dessinée à part, parce qu'elle ne concerne
    pas tout le monde et qu'elle ne s'insère pas dans la suite : elle
    s'y ajoute.
    """
    im, d = fond()
    etapes = [
        "Consulter le RLP et le PLU de la commune",
        "Vérifier si l'adresse est en secteur protégé",
        "Concevoir l'enseigne avec ces contraintes",
        "Déposer le Cerfa 16308*01, en trois exemplaires",
        "Attendre la réponse avant de lancer la fabrication",
    ]
    for i, texte in enumerate(etapes):
        y = 62 + i * 68
        d.ellipse([60, y, 60 + 44, y + 44], fill=rvb("bleu"))
        ecrire(d, 82, y + 9, str(i + 1), "Inter-800", 26, "blanc",
               centre=True)
        ecrire(d, 126, y + 10, texte, "Inter-600", 25)
        if i < len(etapes) - 1:
            tirets(d, (82, y + 48), (82, y + 64), "sable_fonce", 2, 8, 4)
    d.rounded_rectangle([60, 404, LARGE - 60, 516], radius=10,
                        fill=rvb("creme_rose"))
    d.rectangle([60, 404, 64, 516], fill=rvb("corail"))
    ecrire(d, 92, 424, "À l'étape 2, une branche s'ouvre",
           "Inter-800", 23, "corail")
    ecrire(d, 92, 458,
           "Secteur patrimonial protégé ou abords d'un monument : l'avis de",
           "Inter-400", 23, "brun")
    ecrire(d, 92, 484,
           "l'architecte des Bâtiments de France s'ajoute à la démarche.",
           "Inter-400", 23, "brun")
    titre_bas(d, "Cinq étapes, et une qui ne dépend pas de vous.")
    return im


def illu_enseigne_cerfa():
    """Le bon numéro et l'ancien, côte à côte.

    C'est l'erreur la plus coûteuse de l'article, et la seule qu'une
    image règle d'un coup d'œil : on compare deux nombres.
    """
    im, d = fond()
    for x0, num, bon in ((80, "16308*01", True), (632, "14798*01", False)):
        x1 = x0 + 488
        d.rounded_rectangle([x0, 84, x1, 404], radius=12,
                            fill=rvb("blanc" if bon else "creme"),
                            outline=rvb("sable_fonce"), width=2)
        d.rectangle([x0, 84, x1, 92], fill=rvb("bleu" if bon else "taupe"))
        ecrire(d, (x0 + x1) / 2, 124, "CERFA N°", "Inter-600", 22,
               "taupe", centre=True)
        f = police("Playfair-800", 62)
        lg = f.getlength(num)
        d.text(((x0 + x1 - lg) / 2, 158), num, font=f,
               fill=rvb("encre" if bon else "taupe"))
        if not bon:
            d.line([(x0 + x1 - lg) / 2 - 16, 196,
                    (x0 + x1 + lg) / 2 + 16, 196],
                   fill=rvb("corail"), width=6)
        ecrire(d, (x0 + x1) / 2, 252,
               "En vigueur" if bon else "Périmé",
               "Inter-800", 28, "bleu" if bon else "corail", centre=True)
        lignes = (["Notice n° 52393#01.",
                   "Téléchargeable sur service-public.gouv.fr."]
                  if bon else
                  ["Depuis le 1er juillet 2026.",
                   "Un dossier déposé avec lui est incomplet."])
        for j, ligne in enumerate(lignes):
            ecrire(d, (x0 + x1) / 2, 300 + j * 32, ligne, "Inter-400", 23,
                   "brun", centre=True)
    titre_bas(d, "Des sites publics renvoient encore vers celui de droite.")
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


def illu_cmjn_papiers():
    """Le même quadri, quatre papiers.

    L'article dit que le papier change la couleur autant que l'encre.
    La démonstration est visuelle ou elle n'est pas : quatre fois le
    même aplat, posé sur quatre surfaces, et l'œil fait le reste.
    """
    im, d = fond()
    encre = rvb("orange")
    papiers = [("Couché brillant", "blanc", 1.00),
               ("Couché mat", "creme", 0.90),
               ("Offset non couché", "sable", 0.78),
               ("Kraft", "taupe", 0.62)]
    for i, (nom, fond_nom, force) in enumerate(papiers):
        x = 78 + i * 266
        d.rounded_rectangle([x, 96, x + 230, 356], radius=8,
                            fill=rvb(fond_nom), outline=rvb("sable_fonce"),
                            width=2)
        # L'encre ne change pas ; ce qui change, c'est ce qu'elle
        # recouvre et combien la surface la boit.
        p = rvb(fond_nom)
        tache = tuple(round(p[k] + (encre[k] - p[k]) * force) for k in range(3))
        d.rounded_rectangle([x + 34, 132, x + 196, 294], radius=4, fill=tache)
        ecrire(d, x + 115, 374, nom, "Inter-600", 22, "encre", centre=True)
    ecrire(d, LARGE / 2, 432,
           "Même fichier, même encre, même machine.",
           "Inter-400", 25, "brun", centre=True)
    titre_bas(d, "Le papier n'est pas un support. C'est un ingrédient.")
    return im


def illu_cmjn_coupe():
    """Fond perdu, format final, zone de sécurité.

    Trois traits concentriques, et tout est dit : ce qui dépasse, ce
    qu'on coupe, et ce qu'on ne doit pas approcher.
    """
    im, d = fond()
    cx, cy = 332, 268
    perdu = [cx - 240, cy - 170, cx + 240, cy + 170]
    final = [cx - 216, cy - 146, cx + 216, cy + 146]
    secu = [cx - 168, cy - 98, cx + 168, cy + 98]
    d.rectangle(perdu, fill=rvb("sable"))
    d.rectangle(final, fill=rvb("creme_rose"))
    cadre_tirets(d, perdu, "corail", 3, 18, 9)
    d.rectangle(final, outline=rvb("encre"), width=3)
    cadre_tirets(d, secu, "taupe", 2, 16, 8)
    # Les traits de coupe, aux quatre angles.
    for sx in (final[0], final[2]):
        for sy in (final[1], final[3]):
            dx = -34 if sx == final[0] else 34
            dy = -34 if sy == final[1] else 34
            d.line([(sx, sy + dy), (sx, sy + dy / 2.4)],
                   fill=rvb("encre"), width=2)
            d.line([(sx + dx, sy), (sx + dx / 2.4, sy)],
                   fill=rvb("encre"), width=2)
    ecrire(d, cx, cy - 16, "VOTRE VISUEL", "Playfair-700", 34, "taupe",
           centre=True)

    legendes = [
        ("corail", "Fond perdu",
         "3 à 5 mm au-delà du format. Sans lui, la moindre imprécision "
         "de coupe laisse un filet blanc sur la tranche."),
        ("encre", "Format final",
         "Le trait de coupe : la taille du document une fois massicoté."),
        ("taupe", "Zone de sécurité",
         "Texte, logo, téléphone — rien d'important ne s'approche du "
         "bord, la coupe le rognerait."),
    ]
    xl, large = 648, LARGE - 60 - 648
    y = 112
    for couleur, titre, corps in legendes:
        d.rectangle([xl, y + 8, xl + 30, y + 14], fill=rvb(couleur))
        ecrire(d, xl + 46, y, titre, "Inter-800", 25, "encre")
        y = pave(d, xl + 46, y + 38, corps, "Inter-400", 21,
                 large - 46) + 30
    titre_bas(d, "Trois traits. Celui du milieu seul sera visible.")
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



def illu_droits_cession():
    """Les quatre choses qu'un écrit de cession doit nommer.

    L'article cite l'article L.131-3 sans le numéroter : un écrit qui
    oublie une de ces quatre mentions ne cède pas. Quatre colonnes, une
    par mention, avec ce qu'on y écrit vraiment.
    """
    im, d = fond()
    cols = [
        ("Les droits cédés",
         "Reproduction, représentation, adaptation, modification."),
        ("Les supports",
         "Print, numérique, signalétique, véhicules, textile, objets."),
        ("Le territoire",
         "Pour une identité d'entreprise : le monde entier."),
        ("La durée",
         "Toute la durée de protection, pour ne pas rouvrir le sujet."),
    ]
    larg = (LARGE - 120 - 3 * 24) / 4
    for i, (titre, corps) in enumerate(cols):
        x = 60 + i * (larg + 24)
        d.rounded_rectangle([x, 96, x + larg, 400], radius=10,
                            fill=rvb("blanc"), outline=rvb("sable_fonce"),
                            width=2)
        d.rectangle([x, 96, x + larg, 102], fill=rvb("violet"))
        ecrire(d, x + larg / 2, 128, "0%d" % (i + 1), "Playfair-800", 34,
               "sable_fonce", centre=True)
        pave(d, x + 22, 182, titre, "Inter-800", 25, larg - 44, "encre")
        pave(d, x + 22, 252, corps, "Inter-400", 21, larg - 44, "brun")
    ecrire(d, LARGE / 2, 434,
           "Une mention qui manque, c'est un droit qui n'est pas cédé.",
           "Inter-600", 24, "violet", centre=True)
    titre_bas(d, "L'écrit ne se devine pas. Il s'énumère.")
    return im


def illu_droits_livraison():
    """Payer n'est pas acquérir : ce qu'on reçoit, ce qu'on possède.

    Le titre de la première section de l'article, mis en image. À
    gauche ce que beaucoup de commerçants ont reçu ; à droite ce qui
    fait d'eux les propriétaires.
    """
    im, d = fond()
    for x0, titre, sous, items, couleur, plein in (
            (74, "Ce qu'on reçoit souvent", "Une image aplatie",
             ["un fichier .jpg ou .png",
              "qu'on ne peut pas agrandir",
              "ni décliner en monochrome",
              "ni retoucher proprement"], "taupe", False),
            (632, "Ce qui fait de vous le propriétaire",
             "Deux pièces, et pas une",
             ["l'écrit de cession signé",
              "les sources vectorielles (.ai, .eps, .pdf)",
              "les déclinaisons couleur et monochrome",
              "les exports pour l'écran et pour l'impression"], "violet", True)):
        x1 = x0 + 494
        d.rounded_rectangle([x0, 84, x1, 436], radius=12,
                            fill=rvb("blanc" if plein else "creme"),
                            outline=rvb("sable_fonce"), width=2)
        d.rectangle([x0, 84, x1, 90], fill=rvb(couleur))
        y = pave(d, x0 + 28, 112, titre, "Inter-800", 26,
                 x1 - x0 - 56, "encre")
        ecrire(d, x0 + 28, y + 4, sous, "Inter-400", 22, "taupe")
        y += 46
        for item in items:
            # La coche se trace, elle ne s'écrit pas : Inter n'a pas de
            # glyphe « ✓ » et le posait en carré vide.
            if plein:
                d.line([(x0 + 30, y + 16), (x0 + 36, y + 23),
                        (x0 + 48, y + 7)], fill=rvb(couleur), width=4,
                       joint="curve")
            else:
                d.line([(x0 + 30, y + 15), (x0 + 48, y + 15)],
                       fill=rvb(couleur), width=3)
            y = pave(d, x0 + 62, y, item, "Inter-400", 23,
                     x1 - x0 - 94, "brun") + 12
    titre_bas(d, "Sans l'écrit, vous avez payé un travail, pas un logo.")
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


def illu_vitrine_deux_cotes():
    """Les trois familles, vues des deux côtés du verre.

    C'est la seule comparaison qui décide : ce que la rue voit, et ce
    que le commerçant voit depuis sa caisse. Une même grille, deux
    rangées, et la réponse se lit en diagonale.
    """
    im, d = fond()
    familles = ["Dépoli", "Microperforé", "Lettres découpées"]
    larg, ecart, x0 = 272, 38, 262
    for r, cote in enumerate(("Depuis la rue", "Depuis l'intérieur")):
        y = 104 + r * 196
        pave(d, 60, y + 44, cote, "Inter-600", 22, 180, "taupe")
        for c, nom in enumerate(familles):
            x = x0 + c * (larg + ecart)
            if r == 0:
                ecrire(d, x + larg / 2, 64, nom, "Inter-800", 25,
                       "encre", centre=True)
            d.rectangle([x, y, x + larg, y + 150], fill=rvb("creme_rose"),
                        outline=rvb("brun"), width=3)
            if c == 0:                      # dépoli : opaque des deux côtés
                d.rectangle([x + 3, y + 3, x + larg - 3, y + 147],
                            fill=rvb("sable"))
                ecrire(d, x + larg / 2, y + 62, "opaque", "Inter-600", 22,
                       "taupe", centre=True)
            elif c == 1:                    # microperforé : plein / ajouré
                if r == 0:
                    d.rectangle([x + 3, y + 3, x + larg - 3, y + 147],
                                fill=rvb("turquoise"))
                    ecrire(d, x + larg / 2, y + 60, "l'image est pleine",
                           "Inter-600", 21, "blanc", centre=True)
                else:
                    for px in range(x + 12, x + larg - 10, 14):
                        for py in range(y + 12, y + 140, 14):
                            d.ellipse([px, py, px + 6, py + 6],
                                      fill=rvb("turquoise"))
                    # Une plaque claire sous le libellé : posé à même la
                    # trame, il devenait illisible.
                    d.rectangle([x + 30, y + 56, x + larg - 30, y + 94],
                                fill=rvb("creme"))
                    ecrire(d, x + larg / 2, y + 64, "on voit la rue",
                           "Inter-600", 21, "encre", centre=True)
            else:                           # lettres : le verre reste nu
                f = police("Playfair-800", 56)
                mot = "NOM"
                if r == 0:
                    d.text((x + (larg - f.getlength(mot)) / 2, y + 44),
                           mot, font=f, fill=rvb("turquoise"))
                    note = "le reste est transparent"
                else:
                    # Depuis l'interieur, on voit le DOS des lettres :
                    # le nom est inverse, et il se lit en silhouette a
                    # contre-jour. La premiere version le posait a
                    # l'endroit, en plus pale — c'etait faux, et c'est
                    # Laurent qui l'a releve le 24 octobre.
                    lg = int(f.getlength(mot)) + 8
                    tuile = Image.new("RGB", (lg, 76), rvb("creme_rose"))
                    ImageDraw.Draw(tuile).text((4, -6), mot, font=f,
                                               fill=rvb("brun"))
                    tuile = tuile.transpose(Image.FLIP_LEFT_RIGHT)
                    im.paste(tuile, (int(x + (larg - lg) / 2), y + 40))
                    note = "vu de dos, le nom s'inverse"
                ecrire(d, x + larg / 2, y + 112, note, "Inter-400", 19,
                       "taupe", centre=True)
    titre_bas(d, "Quatre mètres sur deux : huit mètres carrés à décider.")
    return im


def illu_vitrine_microperfore():
    """Pourquoi un film percé est plein d'un côté et transparent de l'autre.

    Ce n'est pas une astuce de matière, c'est une histoire de distance
    et de lumière : de loin l'œil fond les trous dans l'image, de près
    il regarde au travers.
    """
    im, d = fond()
    # Le film, en coupe agrandie : une trame de trous d'environ 1 mm.
    fx0, fy0, fx1, fy1 = 400, 110, 800, 400
    d.rectangle([fx0, fy0, fx1, fy1], fill=rvb("turquoise"))
    for px in range(fx0 + 14, fx1 - 10, 26):
        for py in range(fy0 + 14, fy1 - 10, 26):
            d.ellipse([px, py, px + 11, py + 11], fill=rvb("creme"))
    d.rectangle([fx0, fy0, fx1, fy1], outline=rvb("encre"), width=3)
    ecrire(d, (fx0 + fx1) / 2, fy1 + 20,
           "Le film : des milliers de trous d'environ 1 mm",
           "Inter-600", 22, "encre", centre=True)

    # La rue, a gauche ; la boutique, a droite.
    pave(d, 60, 132, "DEPUIS LA RUE", "Inter-800", 22, 250, "taupe")
    pave(d, 60, 172,
         "À deux mètres, l'œil ne sépare plus les trous : il lit "
         "l'image, qui paraît pleine.", "Inter-400", 22, 250)
    tirets(d, (316, 268), (fx0 - 24, 268), "encre", 3, 18, 9)
    d.polygon([(fx0 - 24, 256), (fx0 - 24, 280), (fx0 - 4, 268)],
              fill=rvb("encre"))

    pave(d, 890, 132, "DEPUIS L'INTÉRIEUR", "Inter-800", 22, 250, "taupe")
    pave(d, 890, 172,
         "À trente centimètres, l'œil passe entre les trous : il voit "
         "la rue, et la boutique garde sa lumière.", "Inter-400", 22, 250)
    tirets(d, (884, 268), (fx1 + 24, 268), "encre", 3, 18, 9)
    d.polygon([(fx1 + 24, 256), (fx1 + 24, 280), (fx1 + 4, 268)],
              fill=rvb("encre"))
    titre_bas(d, "Plein dehors, transparent dedans. Le même film.")
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


def illu_voeux_fenetre():
    """Décembre saturé, janvier vide : la même carte, deux effets.

    L'argument de l'article tient dans une comparaison de densité. Deux
    boîtes aux lettres, l'une pleine, l'autre avec une seule enveloppe,
    et la fenêtre de janvier bornée au 31.
    """
    im, d = fond()
    for x0, mois, n, couleur, phrase in (
            (74, "DÉCEMBRE", 18, "taupe",
             "Votre carte arrive au milieu de trente autres, la semaine "
             "où votre client fait son inventaire."),
            (632, "JANVIER", 1, "violet",
             "Elle arrive seule, sur un bureau qu'on vient tout juste "
             "de retrouver.")):
        x1 = x0 + 494
        d.rounded_rectangle([x0, 84, x1, 404], radius=12, fill=rvb("blanc"),
                            outline=rvb("sable_fonce"), width=2)
        d.rectangle([x0, 84, x1, 90], fill=rvb(couleur))
        ecrire(d, (x0 + x1) / 2, 112, mois, "Inter-800", 24, couleur,
               centre=True)
        # Les enveloppes : une grille pour decembre, une seule pour janvier.
        cols, lw, lh, pas = (6, 58, 36, 11) if n > 1 else (1, 182, 116, 0)
        bx = (x0 + x1) / 2 - (cols * lw + (cols - 1) * pas) / 2
        for i in range(n):
            ex = bx + (i % cols) * (lw + pas)
            ey = 158 + (i // cols) * (lh + pas)
            d.rectangle([ex, ey, ex + lw, ey + lh],
                        fill=rvb("creme" if n > 1 else "creme_rose"),
                        outline=rvb("sable_fonce" if n > 1 else couleur),
                        width=2)
            d.line([(ex, ey), (ex + lw / 2, ey + lh * 0.55),
                    (ex + lw, ey)],
                   fill=rvb("sable_fonce" if n > 1 else couleur), width=2)
        pave(d, x0 + 28, 302, phrase, "Inter-400", 22, x1 - x0 - 56)
    d.rounded_rectangle([74, 428, LARGE - 74, 516], radius=10,
                        fill=rvb("creme_rose"))
    pave(d, 102, 450,
         "Le 31 janvier est la limite, pas la cible : passé le 25, une "
         "carte ressemble à un oubli rattrapé. Visez la première "
         "quinzaine.", "Inter-600", 23, LARGE - 204, "encre")
    return im


def illu_voeux_fermeture():
    """La semaine où rien n'avance, et ce qu'elle déplace.

    Les ateliers ferment entre Noël et le 2 janvier. Ce n'est pas un
    détail de calendrier : c'est ce qui oblige à boucler le bon à tirer
    avant les fêtes plutôt qu'après.
    """
    im, d = fond()
    y = 196
    x0, x1 = 90, LARGE - 90
    d.line([(x0, y), (x1, y)], fill=rvb("sable_fonce"), width=4)
    # La bande de fermeture, du 24 decembre au 2 janvier.
    fx0 = x0 + (x1 - x0) * 0.46
    fx1 = x0 + (x1 - x0) * 0.62
    d.rectangle([fx0, y - 46, fx1, y + 46], fill=rvb("creme_rose"))
    cadre_tirets(d, (fx0, y - 46, fx1, y + 46), "corail", 3, 18, 9)
    ecrire(d, (fx0 + fx1) / 2, y - 86, "Ateliers fermés", "Inter-800", 24,
           "corail", centre=True)
    ecrire(d, (fx0 + fx1) / 2, y - 18, "rien n'avance", "Inter-600", 23,
           "corail", centre=True)
    ecrire(d, (fx0 + fx1) / 2, y + 58, "du 24 décembre au 2 janvier",
           "Inter-600", 21, "corail", centre=True)

    jalons = [(0.02, "Création", "maintenant"),
              (0.26, "Bon à tirer", "avant les fêtes"),
              (0.72, "Fabrication", "dès la reprise"),
              (0.96, "Réception", "mi-janvier")]
    for p, titre, quand in jalons:
        x = x0 + (x1 - x0) * p
        d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=rvb("violet"))
        ecrire(d, x, y + 84, titre, "Inter-800", 23, "encre", centre=True)
        ecrire(d, x, y + 114, quand, "Inter-400", 21, "taupe", centre=True)
    pave(d, 90, 364,
         "Un fichier envoyé le 23 décembre ne part pas en machine le 24 : "
         "il attend la reprise. C'est une raison de plus de boucler le bon "
         "à tirer avant les fêtes — le fichier doit être prêt à partir le "
         "jour où l'atelier rouvre, pas commencer ce jour-là.",
         "Inter-400", 23, LARGE - 180)
    titre_bas(d, "Une semaine de fermeture déplace tout le reste.")
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


def illu_trottoir_hauteur():
    """La bande réellement lue, et tout ce qui ne l'est pas.

    L'article donne un chiffre : entre 1,40 m et 1,70 m du sol, soit
    une bande d'environ trente centimètres. Une élévation cotée le dit
    mieux qu'un paragraphe.
    """
    im, d = fond()
    # La vitrine, en elevation : 2 m de haut, cotee a gauche.
    vx0, vx1 = 300, 940
    sol, haut = 470, 90          # 470 px = 2 m, donc 1 m = 190 px
    d.rectangle([vx0, haut, vx1, sol], fill=rvb("creme_rose"),
                outline=rvb("brun"), width=4)
    par_metre = (sol - haut) / 2.0
    y170 = sol - 1.70 * par_metre
    y140 = sol - 1.40 * par_metre
    d.rectangle([vx0 + 4, y170, vx1 - 4, y140], fill=rvb("turquoise"))
    ecrire(d, (vx0 + vx1) / 2, (y170 + y140) / 2 - 16,
           "la seule zone vraiment lue", "Inter-800", 25, "blanc",
           centre=True)
    # La cote, a gauche.
    for yy, lab in ((y170, "1,70 m"), (y140, "1,40 m")):
        tirets(d, (176, yy), (vx0, yy), "taupe", 2, 14, 7)
        ecrire(d, 60, yy - 13, lab, "Inter-600", 22, "taupe")
    d.line([(166, y170), (166, y140)], fill=rvb("turquoise"), width=5)
    ecrire(d, 166, y170 - 38, "≈ 30 cm", "Inter-800", 23, "turquoise",
           centre=True)
    ecrire(d, (vx0 + vx1) / 2, haut + 26,
           "au-dessus, personne ne lève la tête", "Inter-400", 22,
           "taupe", centre=True)
    ecrire(d, (vx0 + vx1) / 2, sol - 52,
           "en dessous, on ne baisse pas les yeux", "Inter-400", 22,
           "taupe", centre=True)
    # Le passant, a huit metres.
    ecrire(d, 1010, 300, "le client", "Inter-600", 22, "encre")
    ecrire(d, 1010, 330, "est à 8 m,", "Inter-400", 21, "taupe")
    ecrire(d, 1010, 356, "et il marche", "Inter-400", 21, "taupe")
    titre_bas(d, "Tout le reste est présent, et pratiquement invisible.")
    return im


def illu_trottoir_nuit():
    """Le soir, le verre choisit son camp.

    Si la rue est plus éclairée que la boutique, la vitrine réfléchit.
    Le client s'y voit lui-même, voit les voitures derrière lui, et
    passe. C'est le point le plus simple à corriger de l'article.
    """
    im, d = fond()
    for x0, titre, bon in ((74, "Intérieur plus clair que la rue", True),
                           (632, "Rue plus claire que l'intérieur", False)):
        x1 = x0 + 494
        d.rounded_rectangle([x0, 84, x1, 414], radius=12,
                            fill=rvb("encre"), outline=rvb("sable_fonce"),
                            width=2)
        vx0, vy0, vx1, vy1 = x0 + 46, 134, x1 - 46, 356
        if bon:
            d.rectangle([vx0, vy0, vx1, vy1], fill=rvb("creme"))
            # Ce qu'on voit : le fond de boutique, eclaire.
            d.rectangle([vx0 + 54, vy0 + 46, vx1 - 54, vy1 - 30],
                        fill=rvb("sable"))
            ecrire(d, (vx0 + vx1) / 2, vy0 + 98, "on voit l'intérieur",
                   "Inter-800", 25, "brun", centre=True)
            d.rectangle([vx0, vy0, vx1, vy1], outline=rvb("jaune"), width=4)
        else:
            # Le reflet se dessine dans une vignette aux dimensions du
            # verre : tracées à même la planche, les obliques sortaient
            # du cadre et allaient barrer la vitrine d'à côté.
            lv, hv = int(vx1 - vx0), int(vy1 - vy0)
            vitre = Image.new("RGB", (lv, hv), rvb("brun"))
            dv = ImageDraw.Draw(vitre)
            for i in range(-4, 14):
                dx = i * 44
                dv.line([(dx, hv), (dx + 120, 0)],
                        fill=rvb("brun_clair"), width=10)
            im.paste(vitre, (int(vx0), int(vy0)))
            d.rectangle([vx0, vy0, vx1, vy1], outline=rvb("sable_fonce"),
                        width=4)
            plq = ((vx0 + vx1) / 2 - 150, vy0 + 84,
                   (vx0 + vx1) / 2 + 150, vy0 + 128)
            d.rectangle(plq, fill=rvb("encre"))
            ecrire(d, (vx0 + vx1) / 2, vy0 + 92, "le verre fait miroir",
                   "Inter-800", 25, "jaune", centre=True)
        pave(d, x0 + 46, 372, titre, "Inter-600", 23, x1 - x0 - 92,
             "creme")
    pave(d, 74, 442,
         "La lumière doit aller de l'intérieur vers l'extérieur : un "
         "éclairage orienté vers le produit, un fond de boutique allumé, "
         "et le verre redevient transparent.",
         "Inter-400", 23, LARGE - 148)
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


def illu_logo_tailles():
    """Le même logo à quatre tailles réelles, et ce qui tombe.

    L'article pose la question « est-il lisible partout, sur vos
    supports réels ? ». La réponse ne se raconte pas : on pose le même
    dessin à quatre échelles, et on regarde ce qui disparaît.
    """
    im, d = fond()
    tailles = [(220, "Enseigne", "2 m de large"),
               (130, "Véhicule", "40 cm"),
               (70, "Carte de visite", "15 mm"),
               (34, "Favicon", "32 px")]
    # Des emplacements de largeur fixe : alignés sur la taille du
    # dessin, « Carte de visite » venait toucher « Favicon ».
    fente = (LARGE - 160) / 4
    for i, (cote, usage, mesure) in enumerate(tailles):
        cx = 80 + fente * (i + 0.5)
        x = cx - cote / 2
        cy = 240
        y0 = cy - cote / 2
        d.rounded_rectangle([x, y0, x + cote, y0 + cote],
                            radius=max(3, cote * 0.08), fill=rvb("bleu"))
        # Le monogramme, et une baseline qui ne survit pas a la reduction.
        f = police("Playfair-800", max(9, int(cote * 0.46)))
        d.text((x + (cote - f.getlength("G")) / 2, y0 + cote * 0.17), "G",
               font=f, fill=rvb("creme"))
        if cote >= 70:
            fb = police("Inter-600", max(6, int(cote * 0.10)))
            mot = "GRAFYCOM"
            d.text((x + (cote - fb.getlength(mot)) / 2, y0 + cote * 0.72),
                   mot, font=fb, fill=rvb("creme"))
        ecrire(d, cx, cy + 148, usage, "Inter-800", 23, "encre",
               centre=True)
        ecrire(d, cx, cy + 178, mesure, "Inter-400", 21, "taupe",
               centre=True)
        if cote < 70:
            cadre_tirets(d, (cx - 42, cy - 42, cx + 42, cy + 42),
                         "corail", 2, 14, 7)
            ecrire(d, cx, cy + 56, "plus de nom", "Inter-600", 20,
                   "corail", centre=True)
    titre_bas(d, "Ce qui tombe en premier, c'est ce qui portait le nom.")
    return im


def illu_logo_fichiers():
    """Vectoriel contre pixel, agrandis côte à côte.

    « Il faudrait le vectoriel » : la phrase ne veut rien dire tant
    qu'on n'a pas vu la différence. Le même tracé, agrandi des deux
    façons.
    """
    im, d = fond()
    for x0, titre, exts, net in ((74, "Vectoriel", ".ai  .eps  .pdf", True),
                                 (632, "Pixel", ".jpg  .png", False)):
        x1 = x0 + 494
        d.rounded_rectangle([x0, 84, x1, 420], radius=12, fill=rvb("blanc"),
                            outline=rvb("sable_fonce"), width=2)
        d.rectangle([x0, 84, x1, 90], fill=rvb("bleu" if net else "taupe"))
        ecrire(d, (x0 + x1) / 2, 112, titre, "Inter-800", 26,
               "encre", centre=True)
        ecrire(d, (x0 + x1) / 2, 148, exts, "Inter-400", 22, "taupe",
               centre=True)
        # Le même monogramme des deux côtés. À droite, il est vraiment
        # réduit à 18 px puis réagrandi au plus proche voisin : la
        # dégradation n'est pas dessinée, elle est subie.
        cote = 186
        tuile = Image.new("RGB", (cote, cote), rvb("blanc"))
        dt = ImageDraw.Draw(tuile)
        dt.rounded_rectangle([0, 0, cote - 1, cote - 1], radius=16,
                             fill=rvb("bleu"))
        fg = police("Playfair-800", 112)
        dt.text(((cote - fg.getlength("G")) / 2, 18), "G", font=fg,
                fill=rvb("creme"))
        if not net:
            tuile = (tuile.resize((18, 18), Image.LANCZOS)
                          .resize((cote, cote), Image.NEAREST))
        im.paste(tuile, (int((x0 + x1) / 2 - cote / 2), 188))
        ecrire(d, (x0 + x1) / 2, 392,
               "se redimensionne sans perte" if net
               else "se dégrade dès qu'on l'agrandit",
               "Inter-600", 22, "bleu" if net else "corail", centre=True)
    pave(d, 74, 448,
         "Un JPEG est une photo de votre logo. Sans le fichier "
         "vectoriel, vous ne pouvez ni l'agrandir, ni en tirer une "
         "version monochrome, ni changer une couleur proprement.",
         "Inter-400", 23, LARGE - 148)
    return im


# La premiere de chaque liste est l'illustration d'en-tete, celle que
# l'article declare dans son champ « illustration » et que Google reprend
# en vignette de partage. Les suivantes se posent DANS le texte, a
# l'endroit ou l'article les appelle, par la marque
# « [figure: fichier | legende | description] ».
#
# Pourquoi plusieurs par article : un article de conseil de 800 mots qui
# n'a qu'une image en tete se lit comme un mur. Celles-ci ne decorent
# pas — chacune porte un argument que le texte developpe, et aucune ne
# se contente de redire le titre.
# ----------------------------------------------------------------- avis

def etoiles(d, x, y, n=5, taille=11, couleur_nom="jaune", ecart=17):
    """Une rangée d'étoiles, tracées — Inter n'a pas le glyphe.

    Cinq branches, construites au compas : c'est plus court que de
    chercher une police qui porte « ★ » et qui ait aussi les accents.
    """
    import math
    for k in range(n):
        cx = x + k * ecart
        pts = []
        for i in range(10):
            r = taille if i % 2 == 0 else taille * 0.42
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((cx + r * math.cos(a), y + r * math.sin(a)))
        d.polygon(pts, fill=rvb(couleur_nom))


def illu_avis():
    """Les cinq avis, en deux groupes, comme sur la page réalisations.

    La page les sépare au lieu de les mélanger, et c'est une décision
    de fond : une mention globale « laissés à l'époque de la structure
    précédente » devenait fausse pour deux cinquièmes du bloc, et un
    lecteur qui attrape un détail faux cesse de croire le reste.
    """
    im, d = fond()
    grafycom = [("Laurent", "Solaire 66",
                 "su m'écouter et donner vie à mon projet"),
                ("Social Miroir", "",
                 "son écoute, sa créativité et son grand "
                 "professionnalisme")]
    avant = [("Sarah Otman", "Ô Fait Maison",
              "l'accueil, l'écoute et le professionnalisme"),
             ("Ludivine Le Blay", "La Casquette Bleue",
              "le « service client » au cœur des prestations"),
             ("Jade Lopez", "Mia Beauty",
              "plus de cinq ans, et toujours une mission")]

    def carte(x, larg, haut, y, nom, maison, extrait, vif):
        d.rounded_rectangle([x, y, x + larg, y + haut], radius=10,
                            fill=rvb("blanc"), outline=rvb("sable_fonce"),
                            width=2)
        d.rectangle([x, y, x + larg, y + 5],
                    fill=rvb("jaune" if vif else "sable_fonce"))
        etoiles(d, x + 20, y + 30, taille=9, ecart=15)
        bas = pave(d, x + 20, y + 54, "« %s »" % extrait, "Inter-400", 20,
                   larg - 40, "brun")
        d.text((x + 20, haut + y - 46), nom, font=police("Inter-600", 21),
               fill=rvb("encre"))
        if maison:
            d.text((x + 20, haut + y - 22), maison,
                   font=police("Inter-400", 19), fill=rvb("taupe"))
        return bas

    ecrire(d, 60, 56, "PROJETS MENÉS PAR GRAFYCOM", "Inter-800", 20,
           "jaune")
    for i, (nom, maison, ex) in enumerate(grafycom):
        carte(60 + i * 548, 524, 196, 88, nom, maison, ex, True)

    ecrire(d, 60, 310, "PROJETS MENÉS AU SEIN DE LA STRUCTURE PRÉCÉDENTE",
           "Inter-800", 20, "taupe")
    for i, (nom, maison, ex) in enumerate(avant):
        carte(60 + i * 362, 338, 196, 342, nom, maison, ex, False)
    return im


def illu_avis_ecoute():
    """Par quoi chaque avis commence, et ce que ça dit du métier.

    C'est la seule chose que les cinq ont en commun, et elle n'était
    pas prévue : quatre ouvrent sur la relation, aucun sur le dessin.
    Le graphique ne compte rien — il aligne cinq débuts de phrase, et
    l'alignement suffit.
    """
    im, d = fond()
    lignes = [("Laurent — Solaire 66", "su m'écouter", True),
              ("Social Miroir", "son écoute", True),
              ("Sarah Otman — Ô Fait Maison", "l'accueil, l'écoute", True),
              ("Ludivine Le Blay — La Casquette Bleue",
               "le « service client »", True),
              ("Jade Lopez — Mia Beauty", "rapidité, efficacité", False)]
    ecrire(d, 60, 62, "PAR QUOI CHAQUE AVIS COMMENCE", "Inter-800", 21,
           "taupe")
    for i, (qui, mot, relation) in enumerate(lignes):
        y = 118 + i * 74
        d.rectangle([60, y + 6, 64, y + 46],
                    fill=rvb("turquoise" if relation else "sable_fonce"))
        ecrire(d, 86, y, qui, "Inter-400", 22, "taupe")
        ecrire(d, 86, y + 28, "« %s »" % mot, "Inter-800", 27,
               "encre" if relation else "brun")
    d.line([(60, 496), (LARGE - 60, 496)], fill=rvb("sable_fonce"), width=2)
    ecrire(d, 60, 518, "Aucun ne commence par le dessin.", "Inter-600", 26,
           "turquoise")
    return im


def illu_avis_reponse():
    """L'échange réel, et ce qu'aurait donné la réponse facile.

    À droite, l'avis de Social Miroir et la réponse que Sandra a
    publiée : elle nomme le projet au lieu de remercier dans le vide.
    À gauche, la même réponse écrite comme on les écrit d'habitude.
    Les deux textes de droite sont ceux de la fiche, mot pour mot.
    """
    im, d = fond()
    for x0, etiquette, texte, bon in (
            (80, "Remercier dans le vide",
             "Merci beaucoup pour votre retour, à très bientôt !", False),
            (632, "Nommer le projet",
             "Ça a été un plaisir de travailler avec vous pour ce projet "
             "original. Je vous remercie pour votre confiance et les "
             "moments d'échanges.", True)):
        x1 = x0 + 488
        d.rounded_rectangle([x0, 92, x1, 238], radius=12, fill=rvb("blanc"),
                            outline=rvb("sable_fonce"), width=2)
        etoiles(d, x0 + 26, 124, taille=10)
        # Le début de l'avis est coupé, et les points de suspension le
        # disent : trois lignes de citation passaient sous la signature.
        pave(d, x0 + 26, 146,
             "« …son écoute, sa créativité et son grand "
             "professionnalisme. »", "Inter-400", 21, x1 - x0 - 52, "brun")
        ecrire(d, x0 + 26, 206, "Social Miroir", "Inter-600", 19, "encre")
        d.rounded_rectangle([x0 + 44, 256, x1, 456], radius=12,
                            fill=rvb("creme_rose" if bon else "creme"))
        d.rectangle([x0 + 44, 256, x0 + 48, 456],
                    fill=rvb("turquoise" if bon else "taupe"))
        ecrire(d, x0 + 72, 274, "Réponse de Sandra", "Inter-600", 19,
               "taupe")
        pave(d, x0 + 72, 308, texte, "Inter-600", 23, x1 - x0 - 100,
             "encre" if bon else "taupe")
        ecrire(d, x0 + 72, 472, etiquette, "Inter-800", 22,
               "turquoise" if bon else "corail")
    pave(d, 80, 518,
         "Celle de droite est publiée. Celui qui hésite lit la "
         "conversation entière, pas seulement l'avis.",
         "Inter-400", 23, LARGE - 160)
    return im


ILLUSTRATIONS = {
    "autorisation-enseigne-perpignan": [
        ("enseigne.png", illu_enseigne),
        ("enseigne-sequence.png", illu_enseigne_sequence),
        ("enseigne-cerfa.png", illu_enseigne_cerfa)],
    "couleurs-impression-ecran-cmjn": [
        ("cmjn.png", illu_cmjn),
        ("cmjn-papiers.png", illu_cmjn_papiers),
        ("cmjn-coupe.png", illu_cmjn_coupe)],
    "qui-possede-votre-logo": [
        ("droits.png", illu_droits),
        ("droits-cession.png", illu_droits_cession),
        ("droits-livraison.png", illu_droits_livraison)],
    "habiller-sa-vitrine-66": [
        ("vitrine.png", illu_vitrine),
        ("vitrine-deux-cotes.png", illu_vitrine_deux_cotes),
        ("vitrine-microperfore.png", illu_vitrine_microperfore)],
    "supports-fin-annee-66": [
        ("retroplanning.png", illu_retroplanning),
        ("voeux-fenetre.png", illu_voeux_fenetre),
        ("voeux-fermeture.png", illu_voeux_fermeture)],
    "vitrine-fin-annee-trottoir": [
        ("trottoir.png", illu_trottoir),
        ("trottoir-hauteur.png", illu_trottoir_hauteur),
        ("trottoir-nuit.png", illu_trottoir_nuit)],
    "avis-clients-preuve-locale": [
        ("avis.png", illu_avis),
        ("avis-ecoute.png", illu_avis_ecoute),
        ("avis-reponse.png", illu_avis_reponse)],
    "refaire-son-logo-nouvelle-annee": [
        ("bilan.png", illu_bilan),
        ("logo-tailles.png", illu_logo_tailles),
        ("logo-fichiers.png", illu_logo_fichiers)],
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
    n = 0
    for slug, figures in ILLUSTRATIONS.items():
        for rang, (nom, fabrique) in enumerate(figures):
            im = fabrique()
            assert im.size == (LARGE, HAUT), f"{nom} : format non conforme"
            chemin = SORTIE / nom
            im.save(chemin, "PNG", optimize=True)
            print("  %-42s %s" % (chemin.relative_to(RACINE),
                                  "en-tête" if not rang else "dans le texte"))
            n += 1
        print()
    print(f"{n} illustrations pour {len(ILLUSTRATIONS)} articles, "
          f"{LARGE}x{HAUT}, couleurs de la charte uniquement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
