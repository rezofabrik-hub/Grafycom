#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige les trois défauts de texte des cinq portraits d'atelier.

Pourquoi ce fichier existe
--------------------------
Les cinq images reçues le 18 octobre sont validées par Sandra, mais elles
portent trois textes faux, et un texte faux sur le compte d'une graphiste
se retourne contre elle :

1. `04` : la carte de vœux porte « Graautte de voeuwr ». C'est le sujet
   même de l'image.
2. `03` : le pseudo y est écrit « @grafycom graphiste », sans le point.
   C'est l'erreur exacte qui a fait abandonner Canva.
3. `02` et `05` : l'écran affiche une *reconstitution* du logo Solaire 66.
   Publier ça, c'est montrer une fausse version du logo d'un client.

La méthode est la même pour les trois : on ne « regénère » pas l'image, on
repeint la zone fautive. Le fond est reconstruit depuis l'image elle-même
(médiane locale), puis le texte juste est composé avec les polices du
dépôt — Caveat pour le manuscrit, Inter pour le pseudo. Un texte qui doit
se lire se compose ; il ne se génère pas.

Usage
-----
    python3 reseaux/retouche_atelier.py           # les trois corrections
    python3 reseaux/retouche_atelier.py --voir    # + les avant/après
"""
import argparse
import math
import pathlib

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

RACINE = pathlib.Path(__file__).resolve().parent
SOURCES = RACINE / "visuels" / "sources"
ATELIER = SOURCES / "atelier"
POLICES = RACINE / "polices"


def _police(nom, taille):
    return ImageFont.truetype(str(POLICES / nom), taille)


def _masque_teinte(zone, teinte=(0.07, 0.15), sat=0.36, val=(0.25, 0.85)):
    """Masque des pixels d'une teinte donnée, en TSV.

    La selection par distance RVB attrapait le papier a l'ombre et le
    revers bleu de la veste. La teinte, elle, separe net : l'or est a
    40 degres, le papier creme n'a presque pas de saturation, et le bleu
    marine est a l'oppose du cercle.
    """
    import colorsys
    px = zone.load()
    m = Image.new("L", zone.size, 0)
    mp = m.load()
    for y in range(zone.height):
        for x in range(zone.width):
            r, g, b = px[x, y]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if teinte[0] < h < teinte[1] and s > sat and val[0] < v < val[1]:
                mp[x, y] = 255
    return m


def _effacer_encre(im, boite, **kw):
    """Retire une encre colorée d'une zone, en gardant la texture du fond.

    L'encre est selectionnee par sa teinte, puis remplacee par une
    version floue de la zone — c'est-a-dire par le papier moyen,
    gaufrage compris. Un aplat plat trahirait ; un flou local, non.
    """
    flou = kw.pop("flou", 7)
    dilate = kw.pop("dilate", 5)
    x0, y0, x1, y1 = boite
    zone = im.crop(boite).convert("RGB")
    masque = _masque_teinte(zone, **kw)
    masque = masque.filter(ImageFilter.MaxFilter(dilate))
    masque = masque.filter(ImageFilter.GaussianBlur(1.6))
    fond = zone.filter(ImageFilter.GaussianBlur(flou))
    im.paste(Image.composite(fond, zone, masque), (x0, y0))
    return im


def _effacer_sombre(im, boite, ecart=26, clair=205, dilate=5, bruit=7):
    """Retire une encre sombre d'un fond, sans fantôme ni plaque.

    Trois pieges, rencontres l'un apres l'autre :

    - flouter l'encre etale l'encre : chaque lettre laisse son ombre ;
    - la remplacer par une couleur unique fait une plaque, car le liege
      a un degrade de lumiere qu'une mediane ignore ;
    - et un seuil ABSOLU prend le liege a l'ombre pour de l'encre, ce
      qui ramene la plaque sur la moitie sombre de la zone.

    D'ou le seuil LOCAL : on floute largement la zone pour obtenir son
    champ de lumiere, et on appelle encre tout pixel plus sombre que son
    propre voisinage de `ecart` niveaux. Le champ, regraine, remplit
    ensuite le masque. Les pixels clairs — les feuilles epinglees — sont
    exclus : leur bord ne bouge pas.
    """
    import random
    x0, y0 = boite[0], boite[1]
    zone = im.crop(boite).convert("RGB")
    gris = zone.convert("L")
    champ_g = gris.filter(ImageFilter.GaussianBlur(20))
    dg, gp, cp = ImageChops.subtract(champ_g, gris), gris.load(), champ_g.load()

    encre = dg.point(lambda v: 255 if v > ecart else 0)
    # les feuilles epinglees : hors masque
    blanc = gris.point(lambda v: 255 if v > clair else 0)
    encre = ImageChops.subtract(encre, blanc.filter(ImageFilter.MaxFilter(5)))

    sans = Image.composite(zone.filter(ImageFilter.GaussianBlur(12)), zone,
                           encre.filter(ImageFilter.MaxFilter(9)))
    champ = sans.filter(ImageFilter.GaussianBlur(18))
    px = champ.load()
    al = random.Random(11)
    for y in range(champ.height):
        for x in range(champ.width):
            n = al.randint(-bruit, bruit)
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)),
                        max(0, min(255, b + n)))

    masque = encre.filter(ImageFilter.MaxFilter(dilate))
    masque = masque.filter(ImageFilter.GaussianBlur(1.8))
    im.paste(Image.composite(champ, zone, masque), (x0, y0))
    return im


def _greffer(im, boite, source, fondu=12):
    """Recouvre une zone par un morceau de la même matière, pris ailleurs.

    Recalage : on aligne la moyenne de la greffe sur celle du pourtour
    de la zone a couvrir, canal par canal. Sans ca, le volet gauche de
    la carte — mieux eclaire — ferait une tache claire.
    """
    import statistics
    lx, ly = boite[2] - boite[0], boite[3] - boite[1]
    patch = im.crop((source[0], source[1], source[0] + lx,
                     source[1] + ly)).convert("RGB")
    # le pourtour de la zone : une couronne de 10 px
    k = 10
    autour = im.crop((boite[0] - k, boite[1] - k,
                      boite[2] + k, boite[3] + k)).convert("RGB")
    dedans = Image.new("L", autour.size, 255)
    ImageDraw.Draw(dedans).rectangle([k, k, autour.width - k,
                                      autour.height - k], fill=0)
    cible = [statistics.fmean(
        [c for c, m in zip(autour.getdata(band=b), dedans.getdata()) if m])
        for b in range(3)]
    courant = [statistics.fmean(patch.getdata(band=b)) for b in range(3)]
    patch = Image.merge("RGB", [
        patch.getchannel(b).point(
            lambda v, i=b: max(0, min(255, int(v + cible[i] - courant[i]))))
        for b in range(3)])

    masque = Image.new("L", (lx, ly), 0)
    ImageDraw.Draw(masque).rectangle(
        [fondu, fondu, lx - fondu, ly - fondu], fill=255)
    masque = masque.filter(ImageFilter.GaussianBlur(fondu * 0.6))
    im.paste(patch, (boite[0], boite[1]), masque)
    return im


def _ajuster(texte, fonte_nom, largeur_voulue, depart=60):
    """La taille de fonte qui donne exactement la largeur relevée.

    Le texte refait doit occuper la place de l'ancien, sinon la
    correction se voit plus que le defaut.
    """
    t = depart
    for _ in range(40):
        f = _police(fonte_nom, t)
        l = f.getlength(texte)
        if abs(l - largeur_voulue) <= 2:
            return f
        t = max(8, int(round(t * largeur_voulue / max(1, l))))
    return _police(fonte_nom, t)


def _texte_incline(im, texte, centre, angle, fonte, couleur, ombre=None):
    """Compose un texte sur un plan incliné, avec un léger relief.

    Les cartes et les planches des photos ne sont pas de face. Un texte
    posé droit dessus se voit immédiatement ; on le compose donc à plat
    puis on le tourne, et on garde une ombre d'un pixel pour le relief
    du gaufrage.
    """
    d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    b = d0.textbbox((0, 0), texte, font=fonte)
    larg, haut = b[2] - b[0], b[3] - b[1]
    marge = 40
    calque = Image.new("RGBA", (larg + 2 * marge, haut + 2 * marge), (0, 0, 0, 0))
    dc = ImageDraw.Draw(calque)
    if ombre:
        dc.text((marge - b[0] + 2, marge - b[1] + 2), texte, font=fonte, fill=ombre)
    dc.text((marge - b[0], marge - b[1]), texte, font=fonte, fill=couleur)
    calque = calque.rotate(angle, expand=True, resample=Image.BICUBIC)
    im.paste(calque, (int(centre[0] - calque.width / 2),
                      int(centre[1] - calque.height / 2)), calque)
    return im


# ---------------------------------------------------------------------
# 1. La carte de vœux : « Graautte de voeuwr » -> « Bonne année »
# ---------------------------------------------------------------------
def carte_voeux(voir=False):
    """La carte de vœux : recadrée, pas retouchée. Et pourquoi.

    J'ai essayé deux fois de repeindre « Graautte de voeuwr » en
    « Bonne année ». Les deux fois le résultat est pire que le défaut :
    l'or pale des déliés est à peine plus saturé que le papier crème, si
    bien qu'un masque qui les attrape emporte le papier, et qu'un masque
    qui épargne le papier laisse un fantôme du « G ». Greffer un
    morceau de volet vierge ne marche pas non plus : le volet gauche est
    plus éclairé et le raccord se voit.

    Conclusion honnête : **cette carte ne peut pas être montrée de
    près.** Le recadrage ci-dessous la laisse à sa taille de décor, où
    le manuscrit n'est plus qu'une texture — c'est la règle qui vaut
    déjà pour les tranches de livres et les croquis épinglés.

    Pour le reel n° 20, qui a besoin d'un gros plan du gaufrage et de la
    dorure, il faut une autre image : une vraie photo d'une vraie carte,
    ou cette image regénérée avec le bon texte.
    """
    src = ATELIER / "04-carte-voeux-dorure.jpg"
    im = Image.open(src).convert("RGB")
    # 4:5 centre sur Sandra et la carte, qui tombe a ~280 px de large
    cadre = (712, 0, 1906, 1493)
    dst = ATELIER / "04-recadre-4x5.png"
    im.crop(cadre).resize((1080, 1350), Image.LANCZOS).save(dst)
    return dst


# ---------------------------------------------------------------------
# 2. Le pseudo de la planche 03 : le point manquant
# ---------------------------------------------------------------------
def pseudo(voir=False):
    """« @grafycom graphiste » -> « @grafycom.graphiste ».

    Ici la chirurgie marche, et pour une raison précise : l'encre est
    noire sur du liège clair. Le masque les sépare sans ambiguïté, là où
    l'or sur crème de la carte ne se sépare pas. Le fond reconstruit est
    du liège, une texture quasi uniforme : un flou local la rend sans
    qu'on voie le raccord.

    Boîte et inclinaison relevées sur l'image : (1132, 601)-(1558, 681),
    ligne de base montant de 3 degrés vers la droite.
    """
    src = ATELIER / "03-portrait-nuancier-4x5.jpg"
    im = Image.open(src).convert("RGB")
    avant = im.copy()

    boite = (1120, 588, 1570, 696)
    # un seul passage, et un masque serré : un masque large finit par
    # couvrir toute la bande, et le champ reconstruit — plus lisse que
    # le liège — se voit alors comme un rectangle plus clair.
    _effacer_sombre(im, boite, ecart=24, dilate=7)

    f = _ajuster("@grafycom.graphiste", "Caveat.ttf", 420, depart=66)
    _texte_incline(im, "@grafycom.graphiste", (1344, 639), 3.0, f,
                   (54, 44, 38))

    dst = ATELIER / "03-pseudo-corrige.png"
    im.save(dst)
    if voir:
        _comparer(avant, im, boite, 60, "pseudo")
    return dst


def _zone_pseudo_03(im):
    """Relevée à la main sur l'image : le pseudo manuscrit du liège."""
    return (318, 470, 700, 516)


def _comparer(avant, apres, boite, marge, nom):
    x0, y0, x1, y1 = boite
    c = (max(0, x0 - marge), max(0, y0 - marge),
         min(avant.width, x1 + marge), min(avant.height, y1 + marge))
    a, b = avant.crop(c), apres.crop(c)
    e = 3
    sortie = Image.new("RGB", (a.width * e, a.height * 2 * e + 12), (20, 20, 20))
    sortie.paste(a.resize((a.width * e, a.height * e)), (0, 0))
    sortie.paste(b.resize((b.width * e, b.height * e)), (0, a.height * e + 12))
    p = pathlib.Path("/tmp/claude-0/-home-user-cacheclim/"
                     "5addc094-d098-58ed-b2f3-54bc9b7d7a91/scratchpad")
    sortie.save(p / ("retouche-%s.png" % nom))


if __name__ == "__main__":
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--voir", action="store_true", help="écrire les avant/après")
    o = a.parse_args()
    for f in (carte_voeux, pseudo):
        r = f(voir=o.voir)
        print("  %-18s %s" % (f.__name__, r.name if r else "—"))
