#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique les visuels des publications, sans quota et sans connecteur.

Pourquoi ce fichier existe
--------------------------
Les visuels ont d'abord été commandés à Canva. Trois défauts mesurés, tous
publics si on ne les attrape pas :

1. le format partait en 1080x1920 quand on demandait un post ;
2. le pseudo ressortait « @grafycom graphiste », sans le point ;
3. et surtout, la police choisie n'avait pas les accents français :
   « crédible » devenait « crıdible », « problème » devenait « problØme ».

S'y ajoute un quota de crédits qui s'épuise, et qui arrête la production
au milieu d'un cycle.

Ici, rien de tout ça. Le texte est écrit par Pillow avec Inter — la police
du site, extraite de assets/fonts et instanciée en graisse 800, 600 et 400,
accents compris. Le format est imposé en dur. Le pseudo est une constante.
Aucun appel réseau, aucun crédit, autant de visuels qu'on veut.

Ce que ce fichier NE fait pas : les photographies. Une devanture, une
matière, un plan de travail se photographient. C'est le métier de Sandra,
et une photo inventée sur le compte d'une graphiste se retourne contre elle.

Usage
-----
    python3 reseaux/visuels.py --exemple        # régénère le carrousel du 7
    python3 reseaux/visuels.py --liste          # les gabarits disponibles

Depuis un script :
    from visuels import Planche, LARGE, HAUT
"""
import argparse
import os
import pathlib
import re
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

RACINE = pathlib.Path(__file__).resolve().parent
POLICES = RACINE / "polices"
SORTIE = RACINE / "visuels"

LARGE, HAUT = 1080, 1350          # format 4:5, le post Instagram
LARGE_S, HAUT_S = 1080, 1920      # format 9:16, la story
MARGE = 86

# ---------------------------------------------------------------------
# La direction « typo pleine page », choisie le 18 octobre 2026.
# ---------------------------------------------------------------------
# Le diagnostic etait net : le titre occupait un quart de la planche la
# ou un carrousel d'aujourd'hui en remplit les deux tiers, le contraste
# brun-sur-creme etait aimable mais ne s'arretait pas dans un feed, et
# les 177 planches partageaient le meme squelette sans une variation
# d'echelle.
#
# Trois reglages corrigent l'essentiel, et ils sont ICI plutot que dans
# chaque gabarit : une direction artistique qui se decide a 177 endroits
# n'en est pas une, et le jour ou elle change il faut la rechanger 177
# fois.
TITRE_ECHELLE = 1.35      # le titre, en plus grand
TITRE_INTERLIGNE = 1.12   # resserre, mais pas en dessous : Playfair a des
                          # jambages, et sous 1,10 les hampes touchent les
                          # accents de la ligne du dessous.
GRAIN = 11                # l'ecart-type du bruit. Zero pour l'eteindre.

PSEUDO = "@grafycom.graphiste"

# Les photographies d'atelier. Le registre est ici et nulle part
# ailleurs : un chemin recopie dans un gabarit se perime en silence le
# jour ou le fichier change de nom.
SOURCES = pathlib.Path(__file__).resolve().parent / "visuels" / "sources"
PHOTOS = {
    # n° 1, clôture — le nuancier Pantone, sur le carrousel couleur
    "sandra-nuancier":   SOURCES / "atelier" / "01-recadre-4x5.png",
    # n° 13, clôture — l'écran porte le VRAI logo Solaire 66, incrusté
    # en perspective depuis sources/solaire-66-logo.png : celui que la
    # photo affichait était une approximation, et la publication est
    # justement celle consacrée à ce client.
    "sandra-ecran":      SOURCES / "atelier" / "07-recadre-4x5.png",
    # n° 24, dernier écran du dernier reel
    "sandra-sourire":    SOURCES / "atelier" / "06-recadre-4x5.png",
    "sandra-carte":      SOURCES / "atelier" / "04-recadre-4x5.png",
}    # avec le point. C'est une constante
                                  # justement pour qu'il ne se perde plus.

# La charte n'est plus recopiee ici : elle est LUE dans la feuille de
# style du site, par generateurs/charte.py. Recopier une palette, c'est
# la laisser deriver — et elle avait derive. Mesure le 7 octobre 2026 :
# ce fichier ecrivait un jaune #f5e6a8 la ou le site dit #f9c33f, un vert
# #3a6b4a introuvable dans la charte, et ignorait neuf couleurs du site.
sys.path.insert(0, str(RACINE.parent / "generateurs"))
from charte import C, DEGRADE  # noqa: E402
from charte import couleur as teinte  # noqa: E402


def police(graisse: int, taille: int) -> ImageFont.FreeTypeFont:
    f = POLICES / ("Inter-%d.ttf" % graisse)
    if not f.exists():
        sys.exit("ERREUR : %s manquante. Voir le commentaire en tête de ce "
                 "fichier : les polices viennent de assets/fonts." % f)
    fonte = ImageFont.truetype(str(f), taille)
    fonte.chemin = f
    return fonte


# Inter n'a ni « → » ni « ≠ » ni « ← » : ecrits avec elle, ils sortent en
# carre vide. C'etait deja arrive — fleche() existe pour cette raison — et
# c'est rearrive le 12 octobre sur deux fiches de tournage. Un carre vide
# ne se voit pas dans un diff, seulement sur l'image. On verifie donc, une
# fois pour toutes, que chaque caractere ecrit existe dans la fonte.
_CMAP = {}


def _manquants(texte, fonte):
    chemin = getattr(fonte, "chemin", None)
    if chemin is None:
        return set()
    if chemin not in _CMAP:
        try:
            from fontTools.ttLib import TTFont
            _CMAP[chemin] = set(TTFont(str(chemin)).getBestCmap())
        except Exception:
            _CMAP[chemin] = None          # verification impossible : on passe
    couvert = _CMAP[chemin]
    if couvert is None:
        return set()
    return {c for c in texte if c not in "\n\t\u00a0"
            and ord(c) not in couvert}


def titrage(taille: int, graisse: int = 700) -> ImageFont.FreeTypeFont:
    """Playfair — la fonte de titrage du site, et celle du feed.

    La feuille de style du site compose tous les h1 a h4 en Playfair
    Display ; les publications deja parues font pareil. Les planches
    etaient en Inter 800, une sans-serif geometrique : correctes, mais
    elles ne ressemblaient pas au compte. Laurent l'a dit le 13 octobre,
    et la feuille de style lui donne raison.

    Inter reste la fonte du texte courant, comme sur le site.
    """
    f = POLICES / ("Playfair-%d.ttf" % graisse)
    if not f.exists():
        sys.exit("ERREUR : %s manquante." % f)
    fonte = ImageFont.truetype(str(f), taille)
    fonte.chemin = f
    return fonte


def manuscrite(taille: int) -> ImageFont.FreeTypeFont:
    """Caveat — la seule fonte manuscrite de la charte du site."""
    f = POLICES / "Caveat.ttf"
    if not f.exists():
        sys.exit("ERREUR : %s manquante." % f)
    fonte = ImageFont.truetype(str(f), taille)
    fonte.chemin = f
    return fonte


def typographie(texte: str) -> str:
    """Les espaces insecables de la typographie francaise.

    Avant « ? ! ; : » et a l'interieur des guillemets, l'usage francais
    demande une espace insecable. Ce n'est pas qu'une question de gout :
    sans elle, le point d'interrogation part seul a la ligne suivante, et
    c'est arrive deux fois en passant les titres en Playfair.
    """
    t = texte.replace("\u00a0", " ")
    t = re.sub(r" +([?!;:»])", "\u00a0\\1", t)
    t = re.sub(r"(«) +", "\\1\u00a0", t)
    return t


def couper(texte: str, fonte, largeur: int) -> list[str]:
    """Découpe un texte à la largeur donnée, en respectant les retours forcés.

    Vérifie au passage que la fonte sait écrire chaque caractère : un
    glyphe absent ne produit pas d'erreur, il produit un carré vide qu'on
    ne voit qu'en ouvrant l'image.
    """
    texte = typographie(texte)
    absents = _manquants(texte, fonte)
    if absents:
        sys.exit("ERREUR : la fonte %s n'a pas %s — ils sortiraient en carré "
                 "vide.\n  Texte : %r\n  Pour une flèche, utiliser "
                 "Planche.fleche(), qui la trace."
                 % (getattr(fonte, "chemin", "?"),
                    " ".join("« %s »" % c for c in sorted(absents)), texte))
    lignes = []
    for para in texte.split("\n"):
        # on ne coupe que sur l'espace ordinaire : l'insecable doit
        # justement empecher la coupe, et str.split() la traite comme
        # n'importe quel blanc.
        mots, courante = [m for m in re.split(r"[ \t]+", para) if m], ""
        for mot in mots:
            essai = (courante + " " + mot).strip()
            if fonte.getlength(essai) <= largeur or not courante:
                courante = essai
            else:
                lignes.append(courante)
                courante = mot
        lignes.append(courante)
    return lignes


# Le site n'a aucun aplat sature plein : ses fonds de page sont le creme,
# le creme rose et ce degrade chaud. Les planches doivent s'y tenir, sinon
# le feed et le site ne se ressemblent plus. Valeurs lues dans
# assets/style.css, --degrade-chaud.
FONDS_DEGRADE = {
    "sable_chaud": (150.0, [(0.0, "#f7f1ef"), (0.55, "#f1e6e1"),
                            (1.0, "#e9dcd5")]),
}


def _fonds_couleur():
    """Les fonds pleine page, construits depuis la charte et pas à côté.

    Le feed etait a 45 % de creme, de blanc et d'encre, et a 0,5 % de
    couleur. Or la marque EST un aquarelle arc-en-ciel : le logo porte
    six teintes sur une seule tache. Un feed qui n'en montre aucune ne
    ressemble pas a l'enseigne qu'il represente.

    Chaque fond est un degrade de deux voisins du cercle chromatique de
    la charte — jamais une couleur inventee, jamais un melange hors
    charte : les arrets sont les valeurs lues dans style.css. L'angle
    change d'un fond a l'autre pour que deux planches voisines ne se
    ressemblent pas.
    """
    paires = {
        "violet_encre":   (160.0, ("violet", "bleu")),
        "bleu_turquoise": (135.0, ("bleu", "turquoise")),
        "turquoise_bleu": (200.0, ("turquoise", "bleu_vif")),
        "rose_violet":    (150.0, ("rose", "violet")),
        "corail_orange":  (120.0, ("corail", "orange")),
        "orange_jaune":   (170.0, ("orange", "jaune")),
        "magenta_corail": (140.0, ("magenta", "corail")),
        "bleu_vif_violet": (185.0, ("bleu_vif", "violet")),
    }
    # Les teintes de la charte sont faites pour de petits accents sur
    # du creme. A pleine page sous du texte, elles sont trop claires :
    # mesure faite, aucune encre de la charte n'atteint 4,5:1 sur un
    # turquoise ou un orange purs, et le controle de contraste le dit
    # planche apres planche. On les approfondit donc vers l'encre — qui
    # est elle aussi dans la charte, comme pour tous les _melange() du
    # fichier. La teinte reste reconnaissable, le texte passe.
    fonds = {}
    for nom, (angle, (a, b)) in paires.items():
        fonds[nom] = (angle, [(0.0, C[a]), (1.0, C[b])])
    return fonds


def _fill(c):
    """Un nom de la charte, ou une teinte déjà calculée depuis la charte.

    teinte() refuse un hexadecimal, et elle a raison : une couleur ecrite
    en dur dans le code derive. Mais _accent_lisible() ne l'ecrit pas,
    elle la CALCULE a l'execution a partir de deux valeurs de la charte
    — la teinte et l'encre. Elle n'apparait nulle part dans le source,
    et charte.py --verifier, qui lit le source, n'a rien a y redire.
    """
    return c if isinstance(c, str) and c.startswith("#") else teinte(c)


# Ce que le controle de contraste laisse passer, pour que le total soit
# lisible en fin de cycle et pas noye dans la sortie. Vingt lignes
# eparpillees entre cent quatre-vingts planches ne se comptent pas a
# l'oeil, et un residu qu'on ne compte pas est un residu qui grossit.
RESIDU = []

_ACCENT = None


def accent(nom=None):
    """La teinte d'accent de la publication en cours.

    Une variable de module, et pas un argument de Planche : le surtitre
    revient sur cinq ou six planches d'un meme carrousel, et passer la
    teinte a chaque appel, c'est cinq endroits ou elle peut diverger.
    Chaque gabarit la pose une fois, en tete.
    """
    global _ACCENT
    if nom is not None:
        _ACCENT = nom
    return _ACCENT


def _accent_lisible(nom, fond_lum, exige=4.5, pas=0.06, marge=0.4):
    """La teinte d'accent, approfondie juste assez pour se lire.

    Une teinte de la charte en petit corps sur du creme ne passe pas :
    le violet y est a 3,0:1, le bleu a 3,6:1, et le seuil est 4,5. Les
    poser telles quelles, c'est un surtitre qu'on devine.

    On les approfondit donc vers l'encre — qui est dans la charte, comme
    pour tous les _melange() du fichier — par pas de 6 %, et on s'arrete
    AU PREMIER PAS QUI PASSE. Pas de valeur choisie a l'oeil : le violet
    reste le plus violet qu'un surtitre lisible autorise, et pas un
    cran de plus.
    """
    # La marge existe pour la même raison que dans _assez_fonce : le
    # calcul porte sur la teinte nue, la mesure finale se fait après le
    # grain et sur la médiane d'une couronne autour des glyphes. Viser
    # le seuil exact laissait les cotes « 2 m » à 4,33.
    base = C.get(nom, nom)
    for i in range(14):
        teint = _vers_encre(base, i * pas)
        if _rapport(_luminance(teint), fond_lum) >= exige + marge:
            return teint
    return _vers_encre(base, 13 * pas)


def _assez_fonce(fond, encre, exige=4.9, pas=0.06):
    """Une teinte de la charte, approfondie jusqu'à porter son texte.

    Le pendant de _accent_lisible() : là on cherchait une encre lisible
    sur un fond donné, ici on cherche un fond qui porte une encre
    donnée. Même méthode, même garde-fou — on s'arrête au premier pas
    qui passe, et la teinte reste la plus franche que la lisibilité
    autorise.

    La cible est 4,9 et non 4,5 : le calcul porte sur l'aplat nu, alors
    que la mesure finale se fait APRÈS le grain et sur la médiane d'une
    couronne autour des glyphes, qui inclut leurs bords adoucis. Viser
    exactement le seuil laissait la planche à 4,48 — passer de justesse
    sur le papier, c'est échouer à l'écran.
    """
    base = C.get(fond, fond)
    le = _luminance(C.get(encre, encre))
    for i in range(14):
        t = _vers_encre(base, i * pas)
        if _rapport(le, _luminance(t)) >= exige:
            return t
    return _vers_encre(base, 13 * pas)


def _vers_encre(hexa, k):
    """Une teinte de la charte, approfondie vers l'encre de la charte."""
    enc = C["encre"]
    a = [int(hexa[i:i + 2], 16) for i in (1, 3, 5)]
    e = [int(enc[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(a[i] + (e[i] - a[i]) * k)
                                   for i in range(3))


FONDS_DEGRADE.update(_fonds_couleur())

# Les fonds ou le texte doit passer en clair. Calcule, pas recopie : la
# luminance releve du fond, pas de l'avis du developpeur.
def _sombre(nom):
    if nom in FONDS_DEGRADE:
        arrets = FONDS_DEGRADE[nom][1]
        vals = []
        for _, h in arrets:
            r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
            vals.append(0.2126 * r + 0.7152 * g + 0.0722 * b)
        return sum(vals) / len(vals) < 150
    hx = teinte(nom)
    r, g, b = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b < 150


def _degrade_lineaire(large, haut, angle, arrets):
    """Un degrade lineaire a la maniere de CSS, angle en degres.

    Calcule en basse definition puis agrandi : un degrade est lisse par
    nature, l'agrandissement ne laisse aucun artefact visible et evite
    1,4 million d'iterations Python par planche.
    """
    import math
    ech = max(1, min(large, haut) // 96)
    w, h = max(2, large // ech), max(2, haut // ech)
    a = math.radians(angle)
    dx, dy = math.sin(a), -math.cos(a)
    L = abs(w * math.sin(a)) + abs(h * math.cos(a))
    cx, cy = w / 2.0, h / 2.0
    arrets = sorted(arrets)
    rvb = [(p, tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)))
           for p, c in arrets]
    im = Image.new("RGB", (w, h))
    px = im.load()
    for y in range(h):
        for x in range(w):
            t = ((x - cx) * dx + (y - cy) * dy) / L + 0.5
            t = 0.0 if t < 0 else (1.0 if t > 1 else t)
            j = 0
            while j < len(rvb) - 2 and t > rvb[j + 1][0]:
                j += 1
            p0, c0 = rvb[j]
            p1, c1 = rvb[j + 1]
            k = 0.0 if p1 == p0 else (t - p0) / (p1 - p0)
            k = 0.0 if k < 0 else (1.0 if k > 1 else k)
            px[x, y] = (int(c0[0] + (c1[0] - c0[0]) * k),
                        int(c0[1] + (c1[1] - c0[1]) * k),
                        int(c0[2] + (c1[2] - c0[2]) * k))
    return im.resize((large, haut), Image.BICUBIC)


class _Dessin:
    """Un ImageDraw qui retient les textes qu'on lui demande d'écrire.

    Pourquoi : la couleur du fond est devenue automatique, mais les
    gabarits ecrivent aussi en direct — « p.d.text(...) » — avec des
    couleurs choisies contre l'ancien fond clair. Un menu de restaurant
    en creme sur du magenta ne se lit plus, et rien ne le signalait.

    On ne peut pas relire 300 appels a la main a chaque changement de
    direction. On enregistre donc ce qui est ecrit, et _contraste() le
    mesure a l'enregistrement : la lisibilite devient un controle, au
    meme titre que le chevauchement et le debordement.
    """

    # Le contraire de chaque encre de la charte. Pas un inverse
    # calcule : un choix, pour que « discret » reste discret des deux
    # cotes — taupe sur creme et creme sur violet jouent le meme role.
    # Deux escaliers d'encre, du plus discret au plus franc. Quand une
    # encre ne tient pas sur son fond, on monte l'escalier d'en face
    # jusqu'a ce que le rapport passe — et on s'arrete la. « Discret »
    # reste discret tant que c'est lisible, et devient franc quand il
    # faut : c'est l'arbitrage qu'un oeil ferait, rendu mesurable.
    CLAIRES = ["creme", "sable", "blanc"]
    FONCEES = ["taupe", "brun", "encre"]

    def __init__(self, im):
        self._im = im
        self._d = ImageDraw.Draw(im)
        self.textes = []
        self.rattrapes = []

    def __getattr__(self, nom):
        return getattr(self._d, nom)

    def _fond_sous(self, xy, texte, fonte):
        """La luminance médiane de ce qui se trouve sous ces glyphes."""
        try:
            b = self._d.textbbox(xy, texte, font=fonte)
        except Exception:
            return None
        x0, y0, x1, y1 = (int(v) for v in b)
        x0, y0 = max(0, x0), max(0, y0)
        x1 = min(self._im.width, max(x0 + 1, x1))
        y1 = min(self._im.height, max(y0 + 1, y1))
        if x1 <= x0 or y1 <= y0:
            return None
        vals = sorted(self._im.crop((x0, y0, x1, y1)).convert("L").getdata())
        if not vals:
            return None
        return _luminance((vals[len(vals) // 2],) * 3)

    # Le seuil depend du role, pas seulement du corps. WCAG demande
    # 4,5:1 pour de la matiere a lire ; le pseudo en pied de planche et
    # le « 3/6 » du coin sont des MARQUES — on sait d'avance ce qu'elles
    # disent, on ne les lit pas, on les repere. 3:1 y suffit, et exiger
    # 4,5 obligerait a mettre du blanc pur sur des fonds moyens ou rien
    # d'autre ne passe : on gagnerait un chiffre et on perdrait la
    # discretion qui est tout l'interet de ces deux signes.
    def text(self, xy, texte, *a, role=None, **kw):
        """Écrit — et change l'encre si le fond la rend illisible.

        Les 125 planches passent des couleurs en dur, choisies quand
        tous les fonds etaient clairs. Les relire une par une a chaque
        changement de direction est exactement ce qui finit par laisser
        passer un menu creme sur magenta.

        Alors on mesure : la luminance de ce qui est DEJA dessine sous
        les glyphes, le rapport WCAG avec l'encre demandee, et si le
        rapport ne tient pas on prend le contraire de cette encre —
        quand il fait mieux. Jamais une couleur inventee : le contraire
        est lui aussi dans la charte.
        """
        fonte = kw.get("font") or (a[0] if a else None)
        fill = kw.get("fill") or (a[1] if len(a) > 1 else None)
        if texte and str(texte).strip() and fill and fonte is not None:
            nom = next((k for k, v in C.items()
                        if isinstance(fill, str) and fill.lower() == v.lower()),
                       None)
            fondl = self._fond_sous(xy, texte, fonte)
            connue = nom in C
            if nom and fondl is not None and connue:
                corps = getattr(fonte, "size", 40)
                exige = 3.0 if (corps >= 54 or role == "marque") else 4.5
                r = _rapport(_luminance(fill), fondl)
                if r < exige:
                    # Les deux escaliers, et on garde le meilleur. Sur
                    # un fond moyen — un violet, un corail — ni le clair
                    # ni le fonce ne gagne d'avance : seule la mesure le
                    # dit, et un escalier choisi par avance se trompe
                    # exactement la.
                    # Une teinte d'accent — un bleu, un corail — ne se
                    # remplace pas par une encre neutre : on perdrait la
                    # couleur, qui est l'intention. On l'APPROFONDIT,
                    # comme pour les surtitres, jusqu'au premier pas qui
                    # passe. C'est la même règle, appliquée au même
                    # endroit pour tout le fichier : « bleu » écrit dans
                    # un gabarit reste bleu, et devient lisible.
                    if nom not in self.CLAIRES + self.FONCEES:
                        teint = _accent_lisible(nom, fondl, exige)
                        if _rapport(_luminance(teint), fondl) > r:
                            self.rattrapes.append(
                                (str(texte)[:30], nom, teint, round(r, 2),
                                 round(_rapport(_luminance(teint), fondl), 2)))
                            fill = teint
                            if "fill" in kw:
                                kw["fill"] = fill
                            else:
                                a = list(a)
                                if len(a) > 1:
                                    a[1] = fill
                                else:
                                    kw["fill"] = fill
                                a = tuple(a)
                            self.textes.append((xy, str(texte), fonte, fill,
                                                role))
                            return self._d.text(xy, texte, *a, **kw)
                    autre, r2 = nom, r
                    for cand in self.CLAIRES + self.FONCEES:
                        rc = _rapport(_luminance(cand), fondl)
                        if rc > r2:
                            autre, r2 = cand, rc
                        if r2 >= exige:
                            break
                    if autre != nom and r2 > r:
                        self.rattrapes.append((str(texte)[:30], nom, autre,
                                               round(r, 2), round(r2, 2)))
                        fill = teinte(autre)
                        if "fill" in kw:
                            kw["fill"] = fill
                        else:
                            a = list(a)
                            if len(a) > 1:
                                a[1] = fill
                            else:
                                kw["fill"] = fill
                            a = tuple(a)
            self.textes.append((xy, str(texte), fonte, fill, role))
        return self._d.text(xy, texte, *a, **kw)


def _luminance(couleur):
    """La luminance relative WCAG d'une couleur, nom de charte ou RVB."""
    if isinstance(couleur, str):
        hx = couleur if couleur.startswith("#") else teinte(couleur)
        rvb = tuple(int(hx[i:i + 2], 16) for i in (1, 3, 5))
    else:
        rvb = tuple(couleur[:3])
    c = []
    for v in rvb:
        v /= 255.0
        c.append(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def _rapport(a, b):
    """Le rapport de contraste WCAG entre deux luminances."""
    clair, sombre = max(a, b), min(a, b)
    return (clair + 0.05) / (sombre + 0.05)


def _grouper(soucis):
    """Recolle les lettres d'un surtitre en un seul signalement.

    surtitre() ecrit caractere par caractere, pour l'interlettrage.
    Signaler « I », « D », « E »... fait seize lignes pour un defaut.
    """
    sortie, tampon = [], []
    for t, r, e in soucis:
        if len(t) == 1:
            tampon.append((t, r, e))
            continue
        if tampon:
            sortie.append(("".join(x[0] for x in tampon),
                           min(x[1] for x in tampon), tampon[0][2]))
            tampon = []
        sortie.append((t, r, e))
    if tampon:
        sortie.append(("".join(x[0] for x in tampon),
                       min(x[1] for x in tampon), tampon[0][2]))
    return sortie


def _etiquette(chemin):
    """« dossier/fichier », parce que « 02.png » revient vingt-cinq fois."""
    c = pathlib.Path(chemin)
    return "%s/%s" % (c.parent.name, c.name)


class Planche:
    """Une page de carrousel, ou un écran de story."""

    def __init__(self, fond="creme", large=LARGE, haut=HAUT):
        self.l, self.h = large, haut
        if fond in FONDS_DEGRADE:
            self.im = _degrade_lineaire(large, haut, *FONDS_DEGRADE[fond])
        else:
            self.im = Image.new("RGB", (large, haut), teinte(fond))
        self.d = _Dessin(self.im)
        self._y = MARGE
        # Le fond decide de la couleur du texte, et il la decide tout
        # seul. Le faire a la main, c'est 125 appels a relire a chaque
        # changement de direction, et un oubli qui sort illisible. La
        # luminance est CALCULEE depuis la charte, comme le reste.
        self.fond = fond
        self.sombre = _sombre(fond)

    # Le curseur vertical passe par une propriete, et pas par un simple
    # attribut. Raison : les gabarits ecrivent souvent « p.y = 640 » pour
    # poser le bloc suivant a une ordonnee choisie a la main. Quand les
    # titres ont grossi, plusieurs de ces 640 se sont retrouves AU-DESSUS
    # du bas du titre, et le texte est venu se poser dessus. Aucun
    # controle ne le voyait : ni _deborde(), qui ne regarde que le bas de
    # planche, ni _place(), qu'une affectation directe contourne.
    #
    # Le setter attrape donc tout recul du curseur, d'ou qu'il vienne.
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, valeur):
        if valeur < getattr(self, "_y", 0) - 20:
            self.chevauchements = getattr(self, "chevauchements", [])
            self.chevauchements.append(("bloc", int(self._y - valeur)))
        self._y = valeur

    # -- fonds -------------------------------------------------------
    def bandeau_bas(self, couleur="violet", part=0.33):
        """Un aplat plein sur le bas de la planche."""
        haut = int(self.h * (1 - part))
        self.d.rectangle([0, haut, self.l, self.h], fill=teinte(couleur))
        return self

    # -- texte -------------------------------------------------------
    def _redessiner(self):
        """Repointe le crayon sur la nouvelle image, sans perdre le relevé."""
        anciens = getattr(self.d, "textes", [])
        rattrapes = getattr(self.d, "rattrapes", [])
        self.d = _Dessin(self.im)
        self.d.textes = anciens
        self.d.rattrapes = rattrapes
        return self

    def _encre(self, demande, clair="blanc", fonce="encre"):
        """La couleur demandée, ou celle que le fond impose."""
        if demande is not None:
            return demande
        return clair if self.sombre else fonce

    def titre(self, texte, taille=96, couleur=None, interligne=None,
              y=None, centre=False, echelle=True):
        """Le titrage, en Playfair comme sur le site et dans le feed.

        L'interligne passe de 1.06 a 1.16 : une serif a jambages a besoin
        de plus d'air qu'une sans-serif, sinon les hampes du dessus
        touchent les accents du dessous.
        """
        if echelle:
            taille = int(taille * TITRE_ECHELLE)
        if interligne is None:
            interligne = TITRE_INTERLIGNE
        couleur = self._encre(couleur)
        f = titrage(taille)
        poses = []
        if y is not None:
            self._place(y, "titre")
            self.y = y
        for ligne in couper(texte, f, self.l - 2 * MARGE):
            x = MARGE
            if centre:
                x = (self.l - self.d.textlength(ligne, font=f)) / 2
            self.d.text((x, self.y), ligne, font=f, fill=teinte(couleur))
            poses.append((x, self.y, ligne))
            self.y += int(taille * interligne)
        self._empreinte(poses, f)
        self._deborde()
        self._orphelin(texte, f)
        return self

    def _empreinte(self, poses, fonte):
        """Releve l'encre du titre, pour savoir ensuite si on a ecrit dessus.

        Les deux gardes precedentes raisonnent sur le curseur : elles
        voient un bloc pose trop haut, pas un dessin pose a une ordonnee
        fixe que le titre, en grossissant, est venu rejoindre. Le disque
        de « Votre logo tient-il sur un stylo ? » traversait la
        troisieme ligne, et rien ne l'a signale.

        On garde donc deux choses : le masque des glyphes du titre, et
        la planche telle qu'elle etait juste apres l'avoir ecrit. A
        l'enregistrement, tout pixel du masque qui a change entre-temps
        est un element dessine par-dessus le texte.
        """
        masque = Image.new("L", (self.l, self.h), 0)
        md = ImageDraw.Draw(masque)
        for x, y, ligne in poses:
            md.text((x, y), ligne, font=fonte, fill=255)
        ancien = getattr(self, "_masque_titre", None)
        self._masque_titre = masque if ancien is None \
            else ImageChops.lighter(ancien, masque)
        self._apres_titre = self.im.copy()
        return self

    def _titre_recouvert(self):
        """Compte les pixels de titre repeints depuis qu'il a ete ecrit."""
        masque = getattr(self, "_masque_titre", None)
        if masque is None or getattr(self, "_apres_titre", None) is None:
            return 0
        ecart = ImageChops.difference(self.im.convert("RGB"),
                                      self._apres_titre.convert("RGB"))
        ecart = ecart.convert("L").point(lambda v: 255 if v > 30 else 0)
        touche = ImageChops.multiply(ecart, masque.point(
            lambda v: 255 if v > 120 else 0))
        return sum(touche.histogram()[128:])

    def _orphelin(self, texte, fonte):
        """Signale une derniere ligne reduite a un mot court.

        Le passage en Playfair a change toutes les coupes d'un coup : la
        ou Inter tenait, la serif deborde d'un caractere et renvoie « ? »
        ou « pas » seul a la ligne. C'est le defaut typographique le plus
        visible, et le plus facile a rater sur 95 planches.
        """
        for para in texte.split("\n"):
            lignes = couper(para, fonte, self.l - 2 * MARGE)
            if len(lignes) > 1 and len(lignes[-1].strip()) <= 3:
                self.orphelins = getattr(self, "orphelins", [])
                self.orphelins.append(lignes[-1].strip())
        return self

    def surtitre(self, texte, couleur=None, taille=26, y=None, centre=False,
                 bandeau=False):
        """Le label en capitales espacees, sur un bandeau sombre en tete.

        C'etait un petit mot taupe qui flottait au-dessus du titre. Il
        est devenu un bandeau pleine largeur : il ancre la planche, il
        donne le contraste dur qui manquait, et il laisse au titre toute
        la hauteur en dessous — c'est lui qui rend la « typo pleine
        page » possible sans que la planche parte en l'air.

        L'argument `y` est ignore quand le bandeau est actif.

        Il est hors service par defaut, et ce n'est pas un renoncement :
        essaye le 18 octobre, il n'apparaissait que sur la planche qui
        appelle surtitre(), soit UNE sur sept. Un carrousel avec un seul
        bandeau sombre est moins tenu qu'un carrousel sans. Le jour ou on
        le veut, c'est sur la premiere ET la derniere planche de chaque
        carrousel — l'accroche et l'appel — et nulle part ailleurs.
        """
        if couleur is None and accent() and not self.sombre:
            # la luminance du fond, relevee et pas supposee : le creme,
            # le blanc et le sable chaud ne donnent pas le meme seuil.
            fl = _luminance((sorted(self.im.convert("L").getdata())
                             [self.l * self.h // 2],) * 3)
            couleur = _accent_lisible(accent(), fl)
        couleur = self._encre(couleur, "creme", "taupe")
        if bandeau:
            h = 230
            self.d.rectangle([0, 0, self.l, h], fill=teinte("encre"))
            f = police(800, taille + 8)
            t = texte.upper()
            esp = max(3, (taille + 8) // 7)
            x = MARGE
            for c in t:
                self.d.text((x, h - taille - 46), c, font=f,
                            fill=teinte("creme"))
                x += self.d.textlength(c, font=f) + esp
            self.y = h + 80
            return self
        if y is not None:
            self.y = y
        f = police(800, taille)
        t = texte.upper()
        esp = max(2, taille // 8)
        larg = sum(self.d.textlength(c, font=f) + esp for c in t) - esp
        x = (self.l - larg) / 2 if centre else MARGE
        for c in t:
            self.d.text((x, self.y), c, font=f, fill=_fill(couleur))
            x += self.d.textlength(c, font=f) + esp
        self.y += int(taille * 1.5)
        return self

    def _place(self, y, quoi=""):
        """Signale un element pose au-dessus de ce qui precede.

        _deborde() ne surveillait que le bas de planche. Le passage en
        typo pleine page a casse autre chose : un titre qui fait
        desormais quatre lignes la ou il en faisait deux vient recouvrir
        le dessin pose a une ordonnee fixe en dessous. Le fichier sort,
        aucune alerte, et le defaut ne se voit qu'en ouvrant l'image.

        On compare donc chaque ordonnee explicite au bas du bloc
        precedent. Vingt pixels de tolerance : certains gabarits
        chevauchent volontairement de quelques pixels.
        """
        if y is not None and y < self.y - 20:
            self.chevauchements = getattr(self, "chevauchements", [])
            self.chevauchements.append((quoi or "élément", int(self.y - y)))
        return y

    def _deborde(self):
        """Previent si le texte descend sous la ligne de signature.

        Le passage en Playfair change toutes les metriques d'un coup :
        une coupe qui tenait sur trois lignes peut en faire quatre. Sans
        ce controle, le debordement ne se verrait qu'en ouvrant les 95
        images une par une.
        """
        plancher = self.h - MARGE - 26
        if self.y > plancher:
            self.debordements = getattr(self, "debordements", 0) + 1
        return self

    def texte(self, contenu, taille=38, couleur=None, graisse=400,
              interligne=1.38, avant=22):
        couleur = self._encre(couleur, "creme", "brun")
        f = police(graisse, taille)
        self.y += avant
        for ligne in couper(contenu, f, self.l - 2 * MARGE):
            self.d.text((MARGE, self.y), ligne, font=f, fill=teinte(couleur))
            self.y += int(taille * interligne)
        self._deborde()
        return self

    def filet(self, largeur=260, epaisseur=12, y=None, apres=34):
        """Le filet degrade du site — la regle .trait, a l'echelle.

        C'est l'accent de la charte : le site ne pose jamais un aplat
        bleu ou violet sur toute une page, il pose ce filet de 4 px sur
        un fond creme. Les planches font pareil.
        """
        if y is not None:
            self.y = y
        barre = _degrade_lineaire(largeur, epaisseur, 90.0,
                                  [(p, h) for p, h in DEGRADE])
        masque = Image.new("L", (largeur, epaisseur), 0)
        ImageDraw.Draw(masque).rounded_rectangle(
            [0, 0, largeur - 1, epaisseur - 1], radius=epaisseur // 2,
            fill=255)
        self.im.paste(barre, (MARGE, self.y), masque)
        self.y += epaisseur + apres
        return self

    def photo(self, nom, ancrage="centre", voile=None, part=0.62,
              grisaille=0.0, opacite=232):
        """Une photographie en fond perdu, et de quoi écrire dessus.

        C'est le levier qui manquait. Un dessin au trait, si juste
        soit-il, se lit comme un schema ; une photographie se lit comme
        une preuve. Les cinq images d'atelier existent, Sandra les a
        validees, et le pilier « la personne » de photos-a-prendre.md
        etait vide.

        `voile` pose un degrade sombre du bas vers le haut, sur `part`
        de la hauteur. Ce n'est pas une decoration : sans lui, un titre
        clair pose sur une photographie devient illisible des que la
        photo s'eclaircit, et on ne le voit qu'une fois publie.

        Les photos vivent dans visuels/sources/, qui n'est pas versionne
        — le depot est public, et les portraits de Sandra n'ont pas a y
        etre avant qu'elle ait choisi lesquels sortent. Une photo
        absente ne fait donc pas tomber la production : la planche sort
        sur son fond de couleur, et l'absence est signalee.
        """
        chemin = PHOTOS.get(nom, SOURCES / "atelier" / nom)
        if not pathlib.Path(chemin).exists():
            self.photos_absentes = getattr(self, "photos_absentes", [])
            self.photos_absentes.append(nom)
            return self

        im = Image.open(chemin).convert("RGB")
        # remplir sans deformer : on couvre, puis on recadre
        k = max(self.l / im.width, self.h / im.height)
        im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))),
                       Image.LANCZOS)
        dx = (im.width - self.l) // 2
        dy = {"haut": 0, "bas": im.height - self.h,
              "centre": (im.height - self.h) // 2}[ancrage]
        self.im.paste(im.crop((dx, dy, dx + self.l, dy + self.h)), (0, 0))

        if grisaille:
            gris = self.im.convert("L").convert("RGB")
            self.im = Image.blend(self.im, gris, grisaille)

        if voile:
            h = int(self.h * part)
            calque = Image.new("RGBA", (self.l, h), (0, 0, 0, 0))
            d = ImageDraw.Draw(calque)
            hx = teinte(voile)
            r, v, b = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
            for i in range(h):
                # Rampe douce sur la premiere moitie, puis PLATEAU. Une
                # rampe qui monte jusqu'en bas n'est opaque qu'au tout
                # dernier pixel : le titre, pose aux deux tiers, restait
                # sur une photo claire et devenait illisible.
                t = i / h
                a = int(opacite * min(1.0, (t / 0.55) ** 1.5))
                d.line([(0, i), (self.l, i)], fill=(r, v, b, a))
            self.im.paste(calque, (0, self.h - h), calque)

        self._redessiner()
        self.sur_photo = True
        return self

    def lavis(self, teintes=None, cx=None, cy=None, rayon=None, force=0.52):
        """La tache d'aquarelle du logo, en grand, derrière le texte.

        Le logo Grafycom est une tache aquarellee qui porte six teintes.
        Les planches n'en montraient aucune.

        Premiere tentative : des disques superposes en mode ecran. Rate,
        et pour une raison physique — l'aquarelle est un pigment
        TRANSLUCIDE sur du papier, elle assombrit ce qu'elle couvre ;
        le mode ecran eclaircit, et la tache sortait blanche sur le
        creme. Ici chaque teinte est posee en alpha, l'une sur l'autre,
        et les recouvrements foncent comme deux lavis qui se melangent.

        Le bord est un contour irregulier a 40 sommets, pas un cercle :
        c'est lui, et pas la couleur, qui fait lire « aquarelle ».
        """
        import math
        import random
        noms = teintes or ["bleu_vif", "turquoise", "violet", "rose",
                           "corail", "jaune"]
        cx = int(self.l * 0.64) if cx is None else cx
        cy = int(self.h * 0.62) if cy is None else cy
        R = rayon or int(min(self.l, self.h) * 0.46)
        al = random.Random(5)

        tache = Image.new("RGBA", (self.l, self.h), (0, 0, 0, 0))
        for i, nom in enumerate(noms):
            a = 2 * math.pi * i / len(noms) + 0.6
            x = cx + int(math.cos(a) * R * 0.44)
            y = cy + int(math.sin(a) * R * 0.36)
            r = int(R * al.uniform(0.54, 0.74))
            hx = teinte(nom)
            rvb = tuple(int(hx[j:j + 2], 16) for j in (1, 3, 5))
            c = Image.new("RGBA", (self.l, self.h), rvb + (0,))
            m = Image.new("L", (self.l, self.h), 0)
            ImageDraw.Draw(m).ellipse([x - r, y - r, x + r, y + r], fill=210)
            c.putalpha(m.filter(ImageFilter.GaussianBlur(R * 0.24)))
            tache = Image.alpha_composite(tache, c)

        bord = Image.new("L", (self.l, self.h), 0)
        pts = []
        for i in range(40):
            a = 2 * math.pi * i / 40
            rr = R * al.uniform(0.80, 1.08)
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.88))
        ImageDraw.Draw(bord).polygon(pts, fill=255)
        bord = bord.filter(ImageFilter.GaussianBlur(R * 0.07))

        alpha = ImageChops.multiply(tache.getchannel("A"), bord)
        tache.putalpha(alpha.point(lambda v: int(v * force)))

        fond = self.im.convert("RGBA")
        self.im = Image.alpha_composite(fond, tache).convert("RGB")
        self._redessiner()
        return self

    def abonnement(self, couleur=None, texte=None):
        """La relance d'abonnement, sur le carton de fin d'un reel.

        Uniquement la : ce sont les reels qui atteignent les gens qui ne
        suivent pas encore le compte, et une demande repetee sur chaque
        planche ne se remarque plus. Elle se pose au-dessus de la
        signature, jamais dessus.
        """
        couleur = self._encre(couleur, "sable", "brun")
        t = texte or "Abonnez-vous : un conseil par semaine."
        f = police(600, 30)
        y = self.h - MARGE - 26 - 48
        self.d.text((MARGE, y), t, font=f, fill=teinte(couleur))
        return self

    def signature(self, couleur=None):
        """Le pseudo, en bas à gauche. Jamais saisi à la main ailleurs."""
        couleur = self._encre(couleur, "creme", "brun")
        f = police(600, 26)
        self.d.text((MARGE, self.h - MARGE - 26), PSEUDO, font=f,
                    fill=teinte(couleur), role="marque")
        return self

    def numero(self, n, total, couleur=None):
        couleur = self._encre(couleur, "creme", "brun")
        f = police(600, 24)
        t = "%d/%d" % (n, total)
        self.d.text((self.l - MARGE - f.getlength(t), MARGE - 30), t,
                    font=f, fill=teinte(couleur), role="marque")
        return self

    # -- formes ------------------------------------------------------
    def disques(self, couleurs, legendes=None, y=None, diam=230):
        """Trois pastilles de couleur, avec une légende facultative."""
        y = self.y if y is None else self._place(y, "disques")
        n = len(couleurs)
        espace = (self.l - 2 * MARGE - n * diam) // max(n - 1, 1)
        x = MARGE
        for i, c in enumerate(couleurs):
            self.d.ellipse([x, y, x + diam, y + diam], fill=teinte(c))
            if legendes and legendes[i]:
                f = police(600, 25)
                for j, l in enumerate(legendes[i].split("\n")):
                    w = f.getlength(l)
                    self.d.text((x + (diam - w) / 2, y + diam + 22 + j * 32),
                                l, font=f, fill=C["brun"])
            x += diam + espace
        self.y = y + diam + (90 if legendes else 50)
        return self

    def deux_cartes(self, gauche, droite, texte="12 €", y=None,
                    larg=390, haut=470):
        """Deux aplats portant le même texte : la démonstration de contraste.

        Le texte est écrit dans la même couleur sur les deux : c'est tout
        l'intérêt. Si on trichait, la démonstration ne vaudrait rien.
        """
        y = self.y if y is None else self._place(y, "deux cartes")
        f = police(800, 118)
        ecart = self.l - 2 * MARGE - 2 * larg
        for i, fond in enumerate((gauche, droite)):
            x = MARGE + i * (larg + ecart)
            self.d.rectangle([x, y, x + larg, y + haut], fill=teinte(fond))
            w = f.getlength(texte)
            self.d.text((x + (larg - w) / 2, y + haut / 2 - 75), texte,
                        font=f, fill=C["blanc"])
        self.y = y + haut + 40
        return self

    def fleche(self, couleur="corail", y=None, taille=54):
        """Une fleche TRACEE, pas ecrite.

        Inter n'a pas le glyphe « → » : ecrit avec cette police, il
        sortait en carre vide — et il sortait ainsi dans les visuels deja
        produits. Un trait et un triangle ne dependent d'aucune police.
        """
        y = self.y if y is None else y
        t = teinte(couleur)
        long_, ep = int(taille * 1.25), max(3, taille // 13)
        cy = y + taille // 2
        self.d.line([(MARGE, cy), (MARGE + long_ - taille // 3, cy)],
                    fill=t, width=ep)
        self.d.polygon([(MARGE + long_, cy),
                        (MARGE + long_ - taille // 2.6, cy - taille // 4),
                        (MARGE + long_ - taille // 2.6, cy + taille // 4)],
                       fill=t)
        self.y = y + taille + 20
        return self

    # -- mesure et centrage ------------------------------------------
    #
    # Une planche dont le texte est collé en haut laisse un vide en bas qui
    # se voit tout de suite. On mesure donc le bloc avant de le dessiner,
    # et on le pose au centre optique : legerement au-dessus du milieu
    # geometrique, parce que l'oeil place le centre plus haut qu'il n'est.

    def h_titre(self, texte, taille=96, interligne=None, echelle=True):
        """La hauteur qu'occupera titre() — memes reglages, sinon
        centrer() centrerait un bloc qui n'est pas celui qu'on dessine."""
        if echelle:
            taille = int(taille * TITRE_ECHELLE)
        if interligne is None:
            interligne = TITRE_INTERLIGNE
        f = titrage(taille)
        return len(couper(texte, f, self.l - 2 * MARGE)) * int(taille * interligne)

    def h_texte(self, contenu, taille=38, interligne=1.38, avant=22, graisse=400):
        f = police(graisse, taille)
        n = len(couper(contenu, f, self.l - 2 * MARGE))
        return avant + n * int(taille * interligne)

    def centrer(self, hauteur_totale, remonte=0.46):
        self.y = int(self.h * remonte - hauteur_totale / 2)
        return self

    # -- formes supplementaires ----------------------------------------
    def devanture(self, x, y, larg, haut, mot, graisse, taille,
                  fond="sable", bandeau="encre", texte_couleur="creme"):
        """Une facade schematique avec son enseigne, pour le test A/B."""
        self._place(y, "devanture")
        self.d.rectangle([x, y, x + larg, y + haut], fill=teinte(fond))
        hb = int(haut * 0.26)
        self.d.rectangle([x, y, x + larg, y + hb], fill=teinte(bandeau))
        f = police(graisse, taille)
        w = f.getlength(mot)
        self.d.text((x + (larg - w) / 2, y + hb / 2 - taille * 0.62), mot,
                    font=f, fill=teinte(texte_couleur))
        # La vitrine, pour que ca ressemble a un commerce.
        self.d.rectangle([x + larg * .12, y + hb + haut * .18,
                          x + larg * .88, y + haut * .86], fill=teinte("sable_fonce"))
        return self

    def pastille(self, x, y, texte, fond, couleur="blanc", taille=30, pad=16):
        """Une étiquette ronde : un mot court sur une teinte de la charte.

        Le fond est approfondi jusqu'à porter son texte. Mesure : du
        blanc sur le corail de la charte donne 4,07:1, et il en faut
        4,5 — « QUIZ », « FAUX », « B » et les numéros de planche
        étaient tous juste en dessous. Approfondir l'étiquette plutôt
        que l'écriture est le seul choix possible ici : le texte est
        déjà blanc, il n'y a pas plus clair.
        """
        f = police(800, taille)
        w = f.getlength(texte)
        self.d.rounded_rectangle([x, y, x + w + pad * 2, y + taille + pad],
                                 radius=(taille + pad) // 2,
                                 fill=_assez_fonce(fond, couleur))
        self.d.text((x + pad, y + pad / 2 - 2), texte, font=f,
                    fill=teinte(couleur))
        return w + pad * 2

    def flouter(self, rayon=14):
        from PIL import ImageFilter
        self.im = self.im.filter(ImageFilter.GaussianBlur(rayon))
        self._redessiner()
        return self

    def sticker(self, titre, lignes, y=None, fond="blanc"):
        """Le cartouche qui imite un sticker Instagram, pour les stories."""
        y = self.y if y is None else y
        ft, fl = police(600, 24), police(600, 30)
        haut = 30 + 34 + len(lignes) * 44 + 24
        self.d.rounded_rectangle([MARGE, y, self.l - MARGE, y + haut],
                                 radius=28, fill=teinte(fond))
        self.d.text((MARGE + 30, y + 24), titre.upper(), font=ft, fill=C["brun"])
        for i, l in enumerate(lignes):
            self.d.text((MARGE + 30, y + 66 + i * 44), l, font=fl, fill=C["encre"])
        self.y = y + haut + 24
        return self

    # -- sortie ------------------------------------------------------
    def puces(self, items, pastille="corail", taille=40, couleur="brun",
              numerote=False, y=None, interligne=1.5, diam=22):
        """Une liste a pastilles. Les items passent a la ligne proprement."""
        if y is not None:
            self._place(y, "puces")
            self.y = y
        f = police(400, taille)
        for i, it in enumerate(items, 1):
            cx, cy = MARGE + diam // 2, self.y + taille // 2
            if numerote:
                self.d.ellipse([cx - diam, cy - diam, cx + diam, cy + diam],
                               fill=teinte(pastille))
                fn = police(800, int(diam * 1.1))
                n = str(i)
                l = self.d.textlength(n, font=fn)
                self.d.text((cx - l / 2, cy - diam * 0.72), n, font=fn,
                            fill=teinte("blanc"))
            else:
                r = diam // 2
                self.d.ellipse([cx - r, cy - r, cx + r, cy + r],
                               fill=teinte(pastille))
            x = MARGE + diam * 2 + 18
            for ligne in couper(it, f, self.l - x - MARGE):
                self.d.text((x, self.y), ligne, font=f, fill=teinte(couleur))
                self.y += int(taille * 1.3)
            self.y += int(taille * (interligne - 1.3))
        return self

    def chiffre(self, texte, taille=260, couleur="bleu", y=None, centre=False,
                echelle=True):
        """Un grand nombre, seul. Pour une heure, un prix, une mesure.

        Il suit l'echelle du titre : sans ca, le passage en typo pleine
        page laissait le chiffre seul en petit au milieu d'une planche
        dont tout le reste avait grossi.
        """
        if y is not None:
            self._place(y, "chiffre")
            self.y = y
        if echelle:
            taille = int(taille * TITRE_ECHELLE)
        f = police(800, taille)
        l = self.d.textlength(texte, font=f)
        x = (self.l - l) / 2 if centre else MARGE
        self.d.text((x, self.y), texte, font=f, fill=teinte(couleur))
        self.y += int(taille * 1.08)
        return self

    def encadre(self, texte, taille=40, fond="creme_rose", filet="violet",
                y=None, pad=34, graisse=400, couleur="brun"):
        """Un bloc de texte dans un cadre a filet lateral."""
        if y is not None:
            self._place(y, "encadré")
            self.y = y
        f = police(graisse, taille)
        lignes = couper(texte, f, self.l - 2 * MARGE - 2 * pad - 10)
        h = len(lignes) * int(taille * 1.36) + 2 * pad
        self.d.rectangle([MARGE, self.y, self.l - MARGE, self.y + h],
                         fill=teinte(fond))
        self.d.rectangle([MARGE, self.y, MARGE + 10, self.y + h],
                         fill=teinte(filet))
        yy = self.y + pad
        for ligne in lignes:
            self.d.text((MARGE + pad + 10, yy), ligne, font=f,
                        fill=teinte(couleur))
            yy += int(taille * 1.36)
        self.y += h
        return self

    def photo_a_fournir(self, description):
        """Une planche d'attente, explicite.

        visuels.py ne fabrique pas de photographies : une devanture, une
        matiere, un plan de travail se photographient. Plutot que de
        laisser un trou dans le carrousel, on pose une planche qui dit ce
        qui manque. Elle ne se publie jamais telle quelle.
        """
        haut = int(self.h * 0.22)
        bas = int(self.h * 0.78)
        self.d.rectangle([MARGE, haut, self.l - MARGE, bas],
                         outline=teinte("taupe"), width=4)
        f = police(600, 34)
        self.d.text((MARGE + 40, haut + 50), "PHOTO À FOURNIR", font=f,
                    fill=teinte("corail"))
        self.y = haut + 130
        self.texte(description, 38, "brun", 400, avant=0)
        self.y = bas - 60
        self.texte("Cette planche ne se publie pas. Elle attend l'image.",
                   30, "taupe", 400, avant=0)
        return self

    def poser(self, chemin, cx, cy, largeur, angle=0.0, ombre=28,
              rogner_mm=0.0, mm_par_px=None):
        """Pose une image plate : carte, panneau, document.

        Pour une MISE EN SITUATION STUDIO, pas photographique : rotation
        douce et ombre portee, sur le fond de la charte. Une mise en
        situation sur une vraie palissade ou dans une vraie main demande
        une photo de base, et la regle est claire — jamais une image dont
        les droits ne sont pas clairs.

        rogner_mm : un fichier d'impression porte son fond perdu. Le
        montrer, c'est montrer un fichier de production et non l'objet
        fini. On rogne donc les 2 mm reglementaires avant de poser.
        """
        if not pathlib.Path(chemin).exists():
            # sources/ n'est pas versionné — le dépôt est public, et ni
            # les logos clients ni les portraits de Sandra n'ont à y
            # être. Conséquence mesurée le 22 octobre : sur un conteneur
            # neuf, le cycle entier tombait sur un FileNotFoundError au
            # premier fichier absent. photo() savait déjà le signaler
            # sans mourir ; poser() ne le savait pas. Un outil de
            # production qui s'arrête parce qu'un fichier non versionné
            # manque est un outil qui ne tourne pas sur une autre
            # machine.
            self.images_absentes = getattr(self, "images_absentes", [])
            self.images_absentes.append(pathlib.Path(chemin).name)
            return self
        im = Image.open(chemin).convert("RGBA")
        if rogner_mm and mm_par_px:
            r = int(rogner_mm * mm_par_px)
            im = im.crop((r, r, im.width - r, im.height - r))
        h = int(im.height * largeur / im.width)
        im = im.resize((largeur, h), Image.LANCZOS)

        if ombre:
            # L'ombre est la silhouette de l'objet, pas un rectangle flou
            # pose dessous : une carte tournee doit avoir une ombre tournee.
            sil = Image.new("RGBA", im.size, (0, 0, 0, 90))
            sil.putalpha(im.split()[3].point(lambda a: 90 if a > 8 else 0))
            sil = sil.rotate(angle, expand=True, resample=Image.BICUBIC)
            marge = ombre * 3
            fond = Image.new("RGBA", (sil.width + 2 * marge, sil.height + 2 * marge), (0, 0, 0, 0))
            fond.paste(sil, (marge, marge))
            fond = fond.filter(ImageFilter.GaussianBlur(ombre))
            self.im.paste(fond, (cx - fond.width // 2, cy - fond.height // 2 + ombre // 2), fond)

        tourne = im.rotate(angle, expand=True, resample=Image.BICUBIC)
        self._place(cy - tourne.height // 2, "image")
        self.im.paste(tourne, (cx - tourne.width // 2, cy - tourne.height // 2), tourne)
        return self

    def _grain(self):
        """Un bruit fin sur toute la planche.

        C'est ce qui separe le plus vite un aplat de 2019 d'un visuel
        d'aujourd'hui, et ca coute trois lignes. Calcule au tiers de la
        definition puis agrandi : le grain reste visible, et on evite
        deux millions de tirages aleatoires par planche.
        """
        if not GRAIN:
            return self
        import random
        from PIL import ImageChops
        al = random.Random(7)
        p = (self.l // 3, self.h // 3)
        bruit = Image.new("L", p)
        bruit.putdata([int(al.gauss(128, GRAIN)) for _ in range(p[0] * p[1])])
        bruit = bruit.resize((self.l, self.h), Image.BILINEAR)
        # En FUSION (overlay) et pas en transparence. La premiere version
        # composait ce bruit gris a 9 % par-dessus la planche : chaque
        # teinte etait tiree vers le gris, et le creme #f7f1ef sortait a
        # #ece7e5. Onze points sur chaque canal, sur les 177 planches,
        # pour un effet cense ne rien changer aux couleurs.
        #
        # La fusion, elle, laisse le pixel intact la ou le bruit vaut
        # exactement 128, eclaircit au-dessus et assombrit en dessous :
        # la moyenne est conservee, donc la charte aussi. C'est la seule
        # facon honnete de grainer un aplat dont la valeur est imposee.
        fusion = ImageChops.overlay(self.im.convert("RGB"),
                                    Image.merge("RGB", (bruit, bruit, bruit)))
        self.im = Image.blend(self.im.convert("RGB"), fusion, 0.5)
        self._redessiner()
        return self

    def _contraste(self, seuil=None):
        """Mesure la lisibilité de chaque texte écrit sur la planche.

        Pour chaque texte releve : la luminance de son encre est connue,
        celle de son fond est relevee sur l'image finale dans une
        couronne autour des glyphes — le fond REEL, degrade, lavis et
        photo compris, et pas celui qu'on croit. Le rapport WCAG en
        decoule. Sous 3, un texte de titre ne se lit plus ; on signale.
        """
        souci = []
        for xy, texte, fonte, fill, role in getattr(self.d, "textes", []):
            if fonte is None:
                continue
            # Le seuil depend de la taille, comme dans WCAG : un gros
            # titre tient a 3:1, une ligne de legende non. Et sur un
            # feed, une legende est vue en vignette — on prend 4,5.
            corps = getattr(fonte, "size", 40)
            exige = seuil if seuil else (
                3.0 if (corps >= 54 or role == "marque") else 4.5)
            m = Image.new("L", (self.l, self.h), 0)
            ImageDraw.Draw(m).text(xy, texte, font=fonte, fill=255)
            boite = m.getbbox()
            if not boite:
                continue
            glyphes = m.point(lambda v: 255 if v > 140 else 0)
            autour = ImageChops.subtract(
                m.filter(ImageFilter.MaxFilter(9)).point(
                    lambda v: 255 if v > 40 else 0), glyphes)
            if not autour.getbbox():
                continue
            gris = self.im.convert("L")
            vals = [v for v, a in zip(gris.getdata(), autour.getdata()) if a]
            if not vals:
                continue
            vals.sort()
            fondl = _luminance((vals[len(vals) // 2],) * 3)
            r = _rapport(_luminance(fill), fondl)
            if r < exige:
                souci.append((texte[:34], round(r, 2), round(exige, 1)))
        return souci

    def ecrire(self, chemin):
        n = self._titre_recouvert()
        if n > 400:
            self.chevauchements = getattr(self, "chevauchements", [])
            self.chevauchements.append(("titre", n))
        self._grain()
        if getattr(self, "orphelins", None):
            print("   ORPHELIN  %-22s %s seul(s) en fin de ligne"
                  % (_etiquette(chemin),
                     ", ".join("« %s »" % o for o in self.orphelins)))
        if getattr(self, "chevauchements", None):
            print("   CHEVAUCHE %-22s %s"
                  % (_etiquette(chemin),
                     ", ".join("%s recouvert de %d px" % (q, d)
                               for q, d in self.chevauchements)))
        for t, r, e in (_grouper(self._contraste())
                        if os.environ.get("GRAFYCOM_CONTRASTE") else []):
            RESIDU.append((_etiquette(chemin), r, e, t))
            print("   CONTRASTE %-28s %.2f:1 (il faut %.1f)  « %s »"
                  % (_etiquette(chemin), r, e, t))
        for quoi, g, dte in getattr(self, "debordements_lateraux", []):
            print("   HORS CADRE %-22s %s déborde de %d px à gauche, "
                  "%d px à droite" % (_etiquette(chemin), quoi, g, dte))
        manquantes = (getattr(self, "images_absentes", [])
                      + getattr(self, "photos_absentes", []))
        if manquantes:
            print("   SANS IMAGE %-22s %s"
                  % (_etiquette(chemin), ", ".join(manquantes)))
        if getattr(self, "debordements", 0):
            print("   ATTENTION %s : %d bloc(s) descendent sous la "
                  "signature" % (_etiquette(chemin),
                                 self.debordements))
        p = pathlib.Path(chemin)
        p.parent.mkdir(parents=True, exist_ok=True)
        self.im.save(p, "PNG")
        return p


# ---------------------------------------------------------------------
# Le carrousel du 12 octobre, en exemple complet et reproductible.
# ---------------------------------------------------------------------
def carrousel_couleurs(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-10-26-couleurs"))
    accent("violet")
    faits = []

    p = Planche("sable_chaud")
    p.surtitre("Identité visuelle", y=200)
    p.filet()
    p.titre("Votre couleur dit déjà ce que vous vendez.", 104)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("blanc")
    p.titre("Avant même de lire votre nom…", 62, y=170)
    p.disques(["turquoise", "bleu", "rose"], y=460)
    p.texte("Le client a déjà deviné votre secteur.", 42, "encre", 600, avant=90)
    faits.append(p.ecrire(d / "02.png"))

    p = Planche("blanc")
    p.disques(["turquoise", "bleu", "rose"],
              ["BIO\nSANTÉ", "BANQUE\nCONSEIL", "SOIN\nENFANCE"], y=250)
    p.titre("Ce ne sont pas des règles.\nCe sont des réflexes.", 66, y=820)
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("sable_chaud")
    t = "Les suivre vous rend crédible.\nLes casser vous rend mémorable."
    st = "Le problème, c'est de le faire sans le savoir."
    p.centrer(p.h_titre(t, 78) + p.h_texte(st, 40, avant=60) + 44)
    p.filet()
    p.titre(t, 78, "encre")
    p.texte(st, 40, "brun", 400, avant=60)
    faits.append(p.ecrire(d / "04.png"))

    p = Planche("creme")
    p.titre("Le même prix. Deux fonds.", 58, y=150)
    p.deux_cartes("jaune", "bleu", "12 €", y=360)
    p.titre("Le contraste se vérifie.\nIl ne se devine pas.", 62, y=900)
    faits.append(p.ecrire(d / "05.png"))

    p = Planche("blanc")
    p.titre("Votre secteur en commentaire.", 86, y=320)
    p.texte("Je vous propose trois couleurs pour vous démarquer de vos "
            "concurrents directs.", 40, "brun", 400, avant=40)
    p.fleche("corail", y=820)
    p.signature("brun")
    faits.append(p.ecrire(d / "06.png"))

    # Pilier « la personne ». La planche de clôture du premier carrousel
    # du cycle : le compte s'ouvre sur une démonstration de couleur, il
    # se referme sur la personne qui l'a faite, un nuancier à la main.
    # C'est le même sujet, vu par la fenêtre d'à côté.
    p = Planche("creme")
    p.photo("sandra-nuancier", ancrage="haut", voile="encre", part=0.56)
    p.y = 830
    p.titre("Je choisis les couleurs\nd'après votre métier,\npas d'après la mode.",
            58, "blanc")
    p.texte("Sandra, Grafycom — Perpignan.", 34, "creme", 600, avant=26)
    p.signature("creme")
    faits.append(p.ecrire(d / "07.png"))

    return faits


def dilemme_enseigne(dossier=None):
    """n° 3, jeudi 22 octobre — le test A/B. La seconde planche est la
    premiere, floutee.

    Le flou n'illustre pas, il demontre. Il est applique par le script a la
    planche nette : les deux images sont donc rigoureusement identiques
    sauf le flou, et on ne peut pas tricher.

    Le reglage du rayon est le coeur du visuel. Trop fort, les deux mots
    disparaissent et la demonstration ne prouve rien — c'etait le cas au
    premier essai, a 16 pixels. A 8, le lettrage fin se dissout et le
    lettrage gras tient : c'est precisement ce qu'on veut montrer.

    Les lettres A et B sont tracees APRES le flou. Ce sont des reperes de
    lecture, pas des elements de la scene : les flouter les rendrait
    inutiles.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-10-29-dilemme"))
    accent("corail")
    faits = []
    LARG, HAUTF, ECART = 420, 430, 60
    X0 = (LARGE - 2 * LARG - ECART) // 2
    Y0 = 500

    def facades(p):
        # Meme mot, meme corps. Seule la graisse change : c'est la variable
        # testee, et la seule.
        p.devanture(X0, Y0, LARG, HAUTF, "MAISON", 400, 62)
        p.devanture(X0 + LARG + ECART, Y0, LARG, HAUTF, "MAISON", 800, 62)
        return p

    def reperes(p):
        f = police(800, 62)
        for i, lettre in enumerate(("A", "B")):
            x = X0 + i * (LARG + ECART)
            w = f.getlength(lettre)
            p.d.text((x + (LARG - w) / 2, Y0 + HAUTF + 34), lettre,
                     font=f, fill=C["corail"])
        return p

    p = Planche("creme")
    p.filet(y=116)
    p.titre("Laquelle se lit depuis\nle trottoir d'en face ?", 58, y=180)
    facades(p); reperes(p)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("creme")
    facades(p)
    p.flouter(8)
    reperes(p)                      # nets : ce sont des reperes
    p.titre("À vingt mètres,\nce n'est plus une typo.", 68, y=170)
    p.titre("C'est une silhouette.", 64, "corail", y=1130)
    faits.append(p.ecrire(d / "02.png"))
    return faits


def carrousel_typographie(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-11-02-typographie"))
    accent("magenta")
    f = []
    p = Planche("blanc")
    t = "Cette police est magnifique."
    p.centrer(p.h_titre(t, 92) + p.h_texte("Et elle va vous coûter des clients.", 44, avant=40) + 39)
    p.surtitre("Typographie")
    p.filet()
    p.titre(t, 92)
    p.texte("Et elle va vous coûter des clients.", 44, "corail", 600, avant=40)
    p.signature("brun"); f.append(p.ecrire(d / "01.png"))

    p = Planche("creme")
    p.titre("Lisible sur une carte.\nIllisible sur une bâche.", 70, y=220)
    p.texte("La même police, quatre supports, quatre résultats.", 40, "brun", 400, avant=50)
    p.devanture(MARGE, 700, 400, 380, "MAISON", 400, 40)
    p.devanture(MARGE + 480, 700, 400, 380, "MAISON", 800, 48)
    f.append(p.ecrire(d / "02.png"))

    p = Planche("sable_chaud")
    t = "Trois questions\navant de choisir\nune police."
    p.centrer(p.h_titre(t, 86) + 44)
    p.filet(); p.titre(t, 86, "encre")
    f.append(p.ecrire(d / "03.png"))

    p = Planche("blanc")
    p.titre("1. À quelle distance\nsera-t-elle lue ?", 70, y=230)
    p.texte("Une carte de visite se lit à bout de bras.\n"
            "Un menu, à table, parfois le soir.\n"
            "Une enseigne, à vingt mètres.\n\n"
            "Ce ne sont pas les mêmes polices.", 42, "brun", 400, avant=60)
    f.append(p.ecrire(d / "04.png"))

    p = Planche("creme")
    p.titre("2. Tient-elle\nen tout petit ?", 70, y=200)
    p.texte("Vos mentions, votre numéro, votre adresse. Si c'est illisible "
            "à six points, le problème n'est pas l'imprimeur.", 40, "brun", 400, avant=40)
    p.titre("3. Avez-vous le droit\nde l'utiliser ?", 70, y=830)
    p.texte("Une police gratuite n'est pas forcément libre pour un usage "
            "commercial.", 40, "brun", 400, avant=30)
    f.append(p.ecrire(d / "05.png"))

    p = Planche("encre")
    t = "Une identité,\nc'est deux polices."
    st = "Une pour les titres, une pour le texte. Pas cinq."
    p.centrer(p.h_titre(t, 88) + p.h_texte(st, 42, avant=50) + 44)
    p.filet()
    p.titre(t, 88, "blanc"); p.texte(st, 42, "creme", 400, avant=50)
    p.signature("sable"); f.append(p.ecrire(d / "06.png"))
    return f


def carrousel_enseigne(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-11-10-enseigne"))
    accent("bleu")
    f = []
    p = Planche("sable_chaud")
    t = "Votre enseigne a besoin\nd'une autorisation.\nPas d'une déclaration."
    p.centrer(p.h_titre(t, 74) + 44 + 39)
    p.surtitre("Réglementation")
    p.filet(); p.titre(t, 74, "encre")
    p.signature("brun"); f.append(p.ecrire(d / "01.png"))

    p = Planche("blanc")
    p.titre("La confusion\nla plus répandue", 76, y=200)
    p.d.line([MARGE, 620, MARGE + 620, 620], fill=C["corail"], width=6)
    p.texte("Déclaration préalable", 54, "brun", 600, avant=20)
    p.y = 700
    p.texte("Autorisation préalable", 54, "violet", 800, avant=60)
    f.append(p.ecrire(d / "02.png"))

    p = Planche("creme")
    t = "Cerfa n° 16308*01"
    p.centrer(p.h_titre(t, 92) + p.h_texte("À déposer en mairie,\nen trois exemplaires.", 46, avant=50))
    p.titre(t, 92); p.texte("À déposer en mairie,\nen trois exemplaires.", 46, "brun", 600, avant=50)
    f.append(p.ecrire(d / "03.png"))

    p = Planche("blanc")
    p.titre("Au-delà de trois\ndispositifs ?", 76, y=250)
    p.texte("Le formulaire se remplit une seconde fois.", 44, "brun", 400, avant=50)
    p.texte("Enseigne en bandeau · caisson en drapeau · lettrage de vitrine "
            "· adhésif de porte. Ça fait déjà quatre.", 38, "corail", 600, avant=70)
    f.append(p.ecrire(d / "04.png"))

    p = Planche("creme")
    p.titre("Ce qui change\nselon la commune", 74, y=200)
    for i, (n, txt) in enumerate((("1", "Le Règlement Local de Publicité"),
                                  ("2", "Le Plan Local d'Urbanisme"),
                                  ("3", "Le secteur patrimonial protégé"))):
        y = 620 + i * 150
        p.pastille(MARGE, y, n, "corail", "blanc", 34)
        p.d.text((MARGE + 110, y + 8), txt, font=police(600, 40), fill=C["encre"])
    f.append(p.ecrire(d / "05.png"))

    p = Planche("sable_chaud")
    t = "À Perpignan, le centre ancien\nest en secteur protégé."
    st = ("L'avis des Architectes des Bâtiments de France s'ajoute au dossier. "
          "Il oriente le choix des matières bien avant celui du logo.")
    p.centrer(p.h_titre(t, 68) + p.h_texte(st, 40, avant=50) + 44)
    p.filet()
    p.titre(t, 68, "encre"); p.texte(st, 40, "brun", 400, avant=50)
    f.append(p.ecrire(d / "06.png"))

    p = Planche("encre")
    t = "Une enseigne se pense\nen amont."
    p.centrer(p.h_titre(t, 86) + p.h_texte("Pas après le logo.", 50, avant=40) + 44)
    p.filet()
    p.titre(t, 86, "blanc"); p.texte("Pas après le logo.", 50, "creme", 600, avant=40)
    p.signature("sable"); f.append(p.ecrire(d / "07.png"))
    return f


def quiz_idees_recues(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-11-05-quiz"))
    accent("rose")
    f = []
    p = Planche("sable_chaud")
    p.pastille(MARGE, 240, "QUIZ", "corail", "blanc", 30)
    p.filet(y=330)
    t = "4 idées reçues\nsur l'impression\net les enseignes."
    p.titre(t, 84, "encre")
    p.texte("Combien allez-vous rater ?", 46, "brun", 600, avant=40)
    p.signature("brun"); f.append(p.ecrire(d / "01.png"))

    questions = [
        ("« Une enseigne se déclare\nen mairie. »", "FAUX", "Elle s'autorise. Cerfa 16308*01."),
        ("« Un logo doit rester lisible\nen noir et blanc. »", "VRAI", "Sinon il échoue sur un tampon, une gravure, une broderie."),
        ("« 300 DPI convient\nà toutes les bâches. »", "FAUX", "La résolution se calcule à la distance de lecture."),
        ("« Une police gratuite est libre\npour un usage commercial. »", "FAUX", "Presque jamais vérifié, et c'est celui qui coûte."),
    ]
    for i, (q, rep, expl) in enumerate(questions, start=2):
        fond = "blanc" if i % 2 == 0 else "creme"
        p = Planche(fond)
        p.titre(q, 64, y=240)
        x = p.pastille(MARGE, 700, "VRAI", "bleu", "blanc", 32)
        p.pastille(MARGE + x + 24, 700, "FAUX", "corail", "blanc", 32)
        p.y = 860
        p.titre(rep, 92, "violet" if rep == "VRAI" else "corail")
        p.texte(expl, 38, "brun", 400, avant=20)
        f.append(p.ecrire(d / ("%02d.png" % i)))
    return f


def carrousel_droits(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-11-03-droits"))
    accent("bleu")
    f = []
    p = Planche("creme")
    t = "Qui possède\nvotre logo ?"
    p.centrer(p.h_titre(t, 110) + p.h_texte("La réponse surprend la plupart des chefs d'entreprise.", 42, avant=50) + 39)
    p.surtitre("Droits & propriété")
    p.filet()
    p.titre(t, 110); p.texte("La réponse surprend la plupart des chefs d'entreprise.", 42, "brun", 400, avant=50)
    p.signature("brun"); f.append(p.ecrire(d / "01.png"))

    p = Planche("sable_chaud")
    t = "Vous l'avez payé.\nVous ne le possédez\npas forcément."
    st = "Payer une création ne transfère pas les droits d'auteur. Le transfert se fait par écrit, et seulement par écrit."
    p.centrer(p.h_titre(t, 80) + p.h_texte(st, 40, avant=50) + 44)
    p.filet()
    p.titre(t, 80, "encre"); p.texte(st, 40, "brun", 400, avant=50)
    f.append(p.ecrire(d / "02.png"))

    p = Planche("blanc")
    p.titre("Ce qui se cède,\net ce qui ne\nse cède pas.", 66, y=180)
    p.texte("Les droits patrimoniaux se cèdent : exploiter, reproduire, adapter.", 42, "encre", 600, avant=70)
    p.texte("Le droit moral, jamais.\nIl reste à l'auteur, à vie.", 42, "corail", 600, avant=40)
    f.append(p.ecrire(d / "03.png"))

    p = Planche("creme")
    p.titre("Une cession se précise", 74, y=240)
    for i, txt in enumerate(("Pour quels supports.", "Sur quel territoire.",
                             "Pour combien de temps.")):
        y = 560 + i * 140
        p.pastille(MARGE, y, str(i + 1), "violet", "blanc", 34)
        p.d.text((MARGE + 110, y + 8), txt, font=police(600, 44), fill=C["encre"])
    f.append(p.ecrire(d / "04.png"))

    p = Planche("blanc")
    p.titre("Pourquoi ça compte\nun jour", 74, y=200)
    p.texte("Le jour où vous vendez l'entreprise.\n"
            "Le jour où vous déposez votre marque.\n"
            "Le jour où vous changez de prestataire.", 44, "brun", 400, avant=70)
    f.append(p.ecrire(d / "05.png"))

    p = Planche("encre")
    t = "Demandez votre\ncontrat de cession."
    st = "S'il n'existe pas, c'est le moment de le faire."
    p.centrer(p.h_titre(t, 88) + p.h_texte(st, 44, avant=50) + 44)
    p.filet()
    p.titre(t, 88, "blanc"); p.texte(st, 44, "creme", 600, avant=50)
    p.signature("sable"); f.append(p.ecrire(d / "06.png"))
    return f


MOIS_COURTS = ["janv", "févr", "mars", "avr", "mai", "juin", "juil",
               "août", "sept", "oct", "nov", "déc"]


def _quatre_prochains_articles(combien=4):
    """Les titres et dates lus dans reseaux/blog/, pas recopies.

    Cette planche annonce des articles dates. Recopiee a la main, elle
    devient fausse des que le calendrier se decale — et un decalage de
    quelques jours etait justement demande le 12 octobre. Elle lit donc
    l'en-tete des fichiers, qui est la source.
    """
    import datetime
    dossier = RACINE / "blog"
    arts = []
    for f in sorted(dossier.glob("*.md")):
        tete = {}
        for ligne in f.read_text(encoding="utf-8").split("\n")[1:14]:
            if ligne.strip() == "---":
                break
            if ":" in ligne:
                k, _, v = ligne.partition(":")
                tete[k.strip()] = v.strip().strip('"')
        if "date" not in tete or "titre" not in tete:
            continue
        try:
            d = datetime.date.fromisoformat(tete["date"])
        except ValueError:
            continue
        # titre_seo est la forme courte, ecrite pour tenir : elle dit le
        # sujet en une ligne la ou le titre complet en fait trois.
        # Couper le titre long au premier deux-points perdait justement la
        # moitie informative — « Enseigne de commerce » sans
        # « l'autorisation prealable ».
        court = tete.get("titre_seo") or tete["titre"]
        if len(court) > 52:
            court = court[:49].rstrip(" ,:") + "…"
        arts.append((d, "%d %s — %s" % (d.day, MOIS_COURTS[d.month - 1],
                                            court)))
    arts.sort()
    return [t for _, t in arts[:combien]]


def carrousel_blog_rdv(dossier=None):
    """Publication n° 4 bis — annoncer le rendez-vous du blog.

    Les stories relaient chaque article a sa sortie, mais rien ne disait
    aux abonnes qu'il y en a un chaque semaine. C'est une annonce, pas un
    relais : elle ne se republie pas, elle s'epingle.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-10-31-blog-rdv"))
    accent("bleu_vif")
    f = []

    p = Planche("sable_chaud")
    p.surtitre("Le blog", y=270)
    p.filet()
    p.titre("Un nouvel article\nchaque vendredi matin.", 78, "encre")
    p.texte("Sur grafycom.fr/blog. Gratuit, sans inscription.", 42, "brun",
            400, avant=56)
    p.signature("brun")
    p.numero(1, 4, "taupe")
    f.append(p.ecrire(d / "01.png"))

    p = Planche("creme")
    p.titre("Ce qu'on y traite", 80, "encre", y=180)
    p.puces(["La réglementation des enseignes et des vitrines",
             "L'impression : couleurs, matières, fichiers",
             "Les droits, la propriété, les fichiers sources",
             "Les coups de main saisonniers, en avance"],
            "corail", 40, "brun", y=400, interligne=1.7)
    p.y = 1080
    p.texte("Des sujets vérifiés, pas des avis.", 38, "encre", 600,
            avant=0)
    p.signature("brun")
    p.numero(2, 4, "taupe")
    f.append(p.ecrire(d / "02.png"))

    p = Planche("blanc")
    p.titre("Les quatre prochains", 70, "encre", y=180)
    p.y = 430
    p.puces(_quatre_prochains_articles(), "violet", 36, "brun",
            interligne=1.55)
    p.signature("brun")
    p.numero(3, 4, "taupe")
    f.append(p.ecrire(d / "03.png"))

    p = Planche("encre")
    t = "grafycom.fr/blog"
    st = "Le lien est en bio. Activez les notifications pour ne rien rater."
    p.centrer(p.h_titre(t, 86) + p.h_texte(st, 42, avant=50) + 44)
    p.filet()
    p.titre(t, 86, "blanc")
    p.texte(st, 42, "creme", 400, avant=50)
    p.signature("sable")
    p.numero(4, 4, "sable")
    f.append(p.ecrire(d / "04.png"))
    return f


def dilemme_carte_prix(dossier=None):
    """Publication n° 11 — la place du prix sur une carte de restaurant.

    Deux images rigoureusement identiques : memes plats, memes prix, meme
    police, meme corps, memes marges. Le SEUL ecart est la place du prix.
    C'est la condition de la demonstration — ajouter une couleur ou un
    cadre a l'image B ferait gagner B pour une autre raison, et le post
    ne prouverait plus rien.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-12-dilemme-carte"))
    accent("corail")
    f = []
    PLATS = [
        ("Velouté de potimarron", "Crème de châtaigne, huile de noisette", "9"),
        ("Œuf parfait", "Poireaux brûlés, comté affiné 24 mois", "12"),
        ("Encornets à la plancha", "Ail doux, persil plat, citron confit", "16"),
        ("Épaule d'agneau confite", "Haricots tarbais, jus au romarin", "24"),
        ("Rouget de roche", "Fenouil rôti, bouillon d'arêtes", "26"),
        ("Tarte fine aux pommes", "Caramel au beurre salé, glace vanille", "9"),
    ]

    def carte(p, alignes):
        fn = police(600, 40)      # le nom du plat
        fd = police(400, 30)      # la description
        p.d.text((MARGE, 170), "NOS PLATS", font=police(800, 26),
                 fill=teinte("taupe"))
        p.d.line([MARGE, 222, p.l - MARGE, 222], fill=teinte("sable_fonce"),
                 width=2)
        y = 280
        x_prix = p.l - MARGE
        for nom, desc, prix in PLATS:
            if alignes:
                # le nom a gauche, le prix cale a droite, relies par des points
                p.d.text((MARGE, y), nom, font=fn, fill=teinte("encre"))
                lp = p.d.textlength(prix + " €", font=fn)
                p.d.text((x_prix - lp, y), prix + " €", font=fn,
                         fill=teinte("encre"))
                x0 = MARGE + p.d.textlength(nom, font=fn) + 14
                x1 = x_prix - lp - 14
                xp = x0
                while xp < x1:
                    p.d.ellipse([xp, y + 26, xp + 3, y + 29],
                                fill=teinte("sable_fonce"))
                    xp += 12
                p.d.text((MARGE, y + 52), desc, font=fd, fill=teinte("brun"))
            else:
                # le prix colle a la fin de la description, au fil du texte
                p.d.text((MARGE, y), nom, font=fn, fill=teinte("encre"))
                p.d.text((MARGE, y + 52), desc + " - " + prix + " €",
                         font=fd, fill=teinte("brun"))
            y += 148
        return p

    for lettre, alignes, coul in (("A", False, "bleu"), ("B", True, "corail")):
        p = Planche("creme")
        carte(p, alignes)
        p.pastille(p.l - MARGE - 86, MARGE - 24, lettre, coul, "blanc", 34)
        p.signature("brun")
        f.append(p.ecrire(d / ("%s.png" % lettre.lower())))
    return f


def carrousel_retroplanning(dossier=None):
    """Publication n° 17 — le retroplanning des cartes de voeux.

    La frise de la slide 2 se lit de DROITE a GAUCHE, du 24 decembre vers
    aujourd'hui. C'est tout le propos : on ne compte pas depuis
    aujourd'hui, on compte a rebours depuis la boite aux lettres. Une
    frise dessinee dans l'autre sens dirait le contraire du texte.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-23-retroplanning"))
    accent("violet")
    f = []

    p = Planche("sable_chaud")
    p.surtitre("Fin d'année", y=250)
    p.filet()
    p.titre("Vos cartes de vœux\nde Noël se décident\ncette semaine.", 86,
            "encre")
    p.texte("Pas en décembre. Voici pourquoi.", 42, "brun", 400, avant=56)
    p.fleche("corail", y=1120)
    p.signature("brun")
    p.numero(1, 6, "taupe")
    f.append(p.ecrire(d / "01.png"))

    # S2 — la frise a rebours
    p = Planche("blanc")
    p.titre("On compte à rebours.", 76, "encre", y=170)
    etapes = [("4", "Réception", "24 déc."), ("3", "Impression", "8 jours"),
              ("2", "Bon à tirer", "4 jours"), ("1", "Création", "10 jours")]
    cx = [880, 640, 400, 160]          # de droite a gauche
    cy = 540
    for i, (n, nom, delai) in enumerate(etapes):
        x = cx[i]
        p.d.ellipse([x - 46, cy - 46, x + 46, cy + 46], fill=teinte("corail"))
        fn = police(800, 44)
        l = p.d.textlength(n, font=fn)
        p.d.text((x - l / 2, cy - 30), n, font=fn, fill=teinte("blanc"))
        for txt, dy, fo, co in ((nom, 70, police(600, 30), "encre"),
                                (delai, 112, police(400, 26), "taupe")):
            l = p.d.textlength(txt, font=fo)
            p.d.text((x - l / 2, cy + dy), txt, font=fo, fill=teinte(co))
        if i < len(etapes) - 1:        # une fleche vers la gauche
            xa, xb = x - 62, cx[i + 1] + 62
            p.d.line([(xa, cy), (xb + 16, cy)], fill=teinte("sable_fonce"),
                     width=5)
            p.d.polygon([(xb, cy), (xb + 20, cy - 11), (xb + 20, cy + 11)],
                        fill=teinte("sable_fonce"))
    # les deux reperes qui fixent le sens de lecture de la frise
    for txt, x in (("aujourd'hui", 160), ("la boîte aux lettres", 880)):
        fo = police(800, 24)
        l = p.d.textlength(txt, font=fo)
        p.d.text((x - l / 2, cy - 132), txt, font=fo, fill=teinte("taupe"))
    p.y = 760
    p.texte("On ne compte pas à partir d'aujourd'hui.\n"
            "On compte à rebours depuis la boîte aux lettres.", 42, "encre",
            600, avant=0)
    p.y = 960
    p.texte("Vingt-deux jours ouvrés de production. Dernier jour pour "
            "lancer la création : mardi 24 novembre.", 36, "brun", 400,
            avant=0)
    p.signature("brun")
    p.numero(2, 6, "taupe")
    f.append(p.ecrire(d / "02.png"))

    # S3 — les trois etapes qu'on oublie de compter
    p = Planche("creme")
    p.titre("Les trois étapes\nqu'on oublie de compter", 68, "encre", y=170)
    y = 480
    for txt in ("Le texte à écrire.", "Le fichier à préparer.",
                "Les adresses à réunir."):
        p.d.line([(MARGE, y + 26), (MARGE + 52, y + 26)],
                 fill=teinte("violet"), width=7)
        p.d.text((MARGE + 80, y), txt, font=police(600, 52),
                 fill=teinte("encre"))
        y += 130
    p.y = 880
    p.texte("Elles prennent plus de temps que l'impression, et ce sont les "
            "seules qui ne se sous-traitent pas.", 38, "bleu", 600, avant=0)
    p.y = 1030
    p.texte("Ce sont elles qui occupent les deux semaines d'ici au 24 "
            "novembre. D'où : cette semaine.", 34, "brun", 400, avant=0)
    p.signature("brun")
    p.numero(3, 6, "taupe")
    f.append(p.ecrire(d / "03.png"))

    # S4 — le bon a tirer
    p = Planche("sable_chaud")
    t = "Le bon à tirer n'est\npas une formalité."
    st = "C'est un aller-retour, et parfois deux. Prévoyez-le."
    p.centrer(p.h_titre(t, 82) + p.h_texte(st, 42, avant=50) + 44)
    p.filet()
    p.titre(t, 82, "encre")
    p.texte(st, 42, "brun", 400, avant=50)
    p.signature("brun")
    p.numero(4, 6, "taupe")
    f.append(p.ecrire(d / "04.png"))

    # S5 — les quatre supports, pictogrammes au trait
    p = Planche("blanc")
    p.titre("Tout part chez le même\nimprimeur, au même moment.", 62,
            "encre", y=170)
    v, ep = teinte("violet"), 5
    bx, by, bw, bh = 120, 520, 190, 190
    def cadre(i):
        return bx + i * 215, by
    # 1. une carte
    x, y = cadre(0)
    p.d.rectangle([x, y + 40, x + 170, y + 150], outline=v, width=ep)
    p.d.line([(x + 24, y + 78), (x + 100, y + 78)], fill=v, width=ep)
    p.d.line([(x + 24, y + 108), (x + 70, y + 108)], fill=v, width=ep)
    # 2. une etiquette
    x, y = cadre(1)
    p.d.polygon([(x + 30, y + 30), (x + 170, y + 30), (x + 170, y + 160),
                 (x + 30, y + 160), (x + 2, y + 95)], outline=v, width=ep)
    p.d.ellipse([x + 26, y + 80, x + 56, y + 110], outline=v, width=ep)
    # 3. un sachet
    x, y = cadre(2)
    p.d.rectangle([x + 28, y + 60, x + 160, y + 170], outline=v, width=ep)
    p.d.arc([x + 62, y + 22, x + 126, y + 86], 180, 360, fill=v, width=ep)
    # 4. un adhesif de vitrine
    x, y = cadre(3)
    p.d.rectangle([x + 20, y + 30, x + 170, y + 170], outline=v, width=ep)
    p.d.line([(x + 20, y + 110), (x + 170, y + 70)], fill=v, width=ep)
    p.d.line([(x + 20, y + 140), (x + 170, y + 100)], fill=v, width=ep)
    for i, lib in enumerate(("Carte", "Étiquette", "Sachet", "Vitrine")):
        x, _ = cadre(i)
        fo = police(600, 28)
        l = p.d.textlength(lib, font=fo)
        p.d.text((x + 95 - l / 2, by + 200), lib, font=fo, fill=teinte("brun"))
    p.y = 830
    p.texte("Décidé ensemble : un seul fichier, un seul délai, un seul "
            "transport.", 40, "encre", 600, avant=0)
    p.y = 990
    p.texte("Décidé séparément : trois relances, et trois fois les frais "
            "de port.", 40, "corail", 600, avant=0)
    p.signature("brun")
    p.numero(5, 6, "taupe")
    f.append(p.ecrire(d / "05.png"))

    # S6 — l'appel
    p = Planche("creme")
    p.filet(y=300)
    p.titre("Dites-moi ce que vous\nvoulez imprimer\npour les fêtes.", 80,
            "encre")
    p.texte("En commentaire. Je vous dis la date limite réelle pour le "
            "décider — pas celle de l'imprimeur, la vôtre.", 40, "brun",
            400, avant=56)
    p.fleche("corail", y=1050)
    p.signature("brun")
    p.numero(6, 6, "taupe")
    f.append(p.ecrire(d / "06.png"))
    return f


def dilemme_voeux(dossier=None):
    """Publication n° 19 — deux cartes de voeux, meme papier, autre texte.

    Comme pour le dilemme n° 11, le seul ecart entre A et B doit etre
    celui qu'on demontre : ici le texte et la place du logo. Meme format,
    meme fond, meme marque, meme signature. Le logo est fictif (la marque
    generique de _logo_fictif) : on ne met jamais en defaut l'identite
    d'un client reel dans une demonstration publique.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-26-dilemme-voeux"))
    accent("magenta")
    f = []

    def carte(p, x, y, w, h):
        """La carte posee a plat, avec son ombre portee."""
        om = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
        ImageDraw.Draw(om).rectangle([40, 46, w + 40, h + 44],
                                     fill=(47, 39, 35, 54))
        om = om.filter(ImageFilter.GaussianBlur(16))
        p.im.paste(Image.alpha_composite(
            p.im.crop((x - 40, y - 40, x + w + 40, y + h + 40)).convert("RGBA"),
            om).convert("RGB"), (x - 40, y - 40))
        p.d.rectangle([x, y, x + w, y + h], fill=teinte("blanc"))
        return p

    X, Y, W, H = 190, 300, 700, 500

    # ---- A : centree, propre, froide -------------------------------
    p = Planche("creme")
    carte(p, X, Y, W, H)
    _logo_fictif(p.d, X + W // 2, Y + 196, 86, detail=False)
    fo = police(600, 38)
    t = "Joyeuses fêtes et bonne année"
    l = p.d.textlength(t, font=fo)
    p.d.text((X + W / 2 - l / 2, Y + 340), t, font=fo, fill=teinte("encre"))
    p.pastille(p.l - MARGE - 86, MARGE - 24, "A", "bleu", "blanc", 34)
    p.y = 900
    p.texte("Laquelle vous donne envie d'y retourner ?", 40, "brun", 600,
            avant=0)
    p.signature("brun")
    f.append(p.ecrire(d / "a.png"))

    # ---- B : le texte d'abord, la marque en pied --------------------
    p = Planche("creme")
    carte(p, X, Y, W, H)
    # la coupe est mesuree sur la largeur utile de la carte, pas devinee :
    # ecrites a la main sur trois lignes, elles debordaient de 170 px.
    fm = manuscrite(54)
    mot = ("Merci d'avoir poussé notre porte cette année. On rouvre le "
           "4 janvier, et on vous garde la table du fond.")
    lignes = couper(mot, fm, W - 80)
    yy = Y + 78
    for ligne in lignes:
        l = p.d.textlength(ligne, font=fm)
        p.d.text((X + W / 2 - l / 2, yy), ligne, font=fm, fill=teinte("encre"))
        yy += 66
    _logo_fictif(p.d, X + W // 2, Y + H - 96, 40, detail=False)
    p.pastille(p.l - MARGE - 86, MARGE - 24, "B", "violet", "blanc", 34)
    p.y = 900
    p.texte("Laquelle vous donne envie d'y retourner ?", 40, "brun", 600,
            avant=0)
    p.y = 1010
    p.texte("Texte inventé pour la démonstration — aucun commerce réel.",
            28, "taupe", 400, avant=0)
    p.signature("brun")
    f.append(p.ecrire(d / "b.png"))
    return f


def quiz_fin_annee(dossier=None):
    """Publication n° 23 — quatre idees recues sur les impressions de fin
    d'annee. Les quatre reponses sont verifiees : la dorure a chaud est
    une feuille metallisee et non une encre, les fonds perdus de 3 mm
    partent a la coupe, et la signaletique de tri demande une place
    reservee des le depart. La quatrieme est un « vrai... mais » assume :
    faux pour l'impression, vrai pour la decision.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-12-03-quiz-fin-annee"))
    accent("bleu")
    f = []

    p = Planche("sable_chaud")
    p.surtitre("Quiz", y=230)
    p.filet()
    p.titre("4 idées reçues\nsur vos impressions\nde fin d'année.", 86,
            "encre")
    p.texte("Vous en avez combien de justes ?", 46, "brun", 600, avant=56)
    p.fleche("corail", y=1090)
    p.signature("brun")
    p.numero(1, 6, "taupe")
    f.append(p.ecrire(d / "01.png"))

    p = Planche("creme")
    p.titre("Vrai ou faux ?", 76, "encre", y=160)
    p.puces([
        "Le doré d'une dorure, c'est de l'encre jaune bien saturée.",
        "Sur un emballage, la signalétique de tri se place à la fin, "
        "quand le dessin est prêt.",
        "Les fonds perdus de 3 mm, c'est une marge de confort : on peut "
        "s'en passer.",
        "Mi-novembre, c'est trop tard pour une carte de vœux imprimée."],
        "bleu", 36, "bleu", numerote=True, y=360, interligne=1.5)
    p.y = 1150
    p.texte("Répondez en commentaire avant de swiper.", 36, "corail", 600,
            avant=0)
    p.signature("brun")
    p.numero(2, 6, "taupe")
    f.append(p.ecrire(d / "02.png"))

    reponses = [
        ("FAUX", "corail", "1. La dorure",
         "Une dorure à chaud, c'est une feuille métallisée pressée sur le "
         "papier. Aucune encre jaune ne brille. C'est pour ça que ça se "
         "voit, et que ça se paie."),
        # Formule tenue sur le terrain de la mise en page, et non sur
        # celui de la regle : la taille minimale d'une signaletique de tri
        # n'a pas ete verifiee a la source, et c'est ce qui bloque deja la
        # publication n° 18. Ce qui est dit ici est vrai quel que soit le
        # texte applicable.
        ("FAUX", "corail", "2. La signalétique de tri",
         "Elle se place dès la mise en page, avec sa zone de respiration. "
         "Ajoutée à la fin, elle se colle en travers de ce qu'on avait "
         "soigné."),
        ("FAUX", "corail", "3. Les fonds perdus",
         "Les 3 mm débordent du format et partent à la coupe. Sans eux, un "
         "liseré blanc apparaît sur un bord. La massicoteuse n'est pas "
         "précise au dixième."),
        ("VRAI… mais", "violet", "4. Mi-novembre",
         "Faux pour l'impression : il reste du temps pour imprimer. Vrai "
         "pour la décision : il n'en reste plus pour hésiter."),
    ]
    for i, (verdict, coul, titre, txt) in enumerate(reponses, 3):
        p = Planche("blanc")
        p.d.text((MARGE, 170), titre, font=police(600, 34),
                 fill=teinte("taupe"))
        taille = 150 if len(verdict) < 6 else 96
        p.titre(verdict, taille, coul, y=250)
        p.y = 560
        p.texte(txt, 44, "encre", 400, avant=0)
        p.signature("brun")
        p.numero(i, 6, "taupe")
        if i == 6:
            # la signature est a 1238 : le score se pose au-dessus, pas
            # dessus.
            p.fleche("corail", y=1040)
            p.y = 1110
            p.texte("Votre score en commentaire.", 36, "brun", 600, avant=0)
        f.append(p.ecrire(d / ("%02d.png" % i)))
    return f


def stories(dossier=None):
    """Les 41 ecrans de stories du cycle, en 9:16, nommes par leur code.

    Les dix ecrans precedents portaient des noms herites d'un cycle
    anterieur — 07-teasing, 13-quiz-1 — qui ne correspondaient plus a
    rien dans le document de validation. Ils portent maintenant leur code
    S1-A, S1-B, et ainsi de suite : on retrouve l'ecran a partir du
    planning sans avoir a deviner.

    Tous sont typographiques. Le document decrit parfois une photo en
    arriere-plan ; visuels.py n'en fabrique pas, et Laurent a dit le 13
    octobre que les prises de vue sont difficiles a caser. Un ecran
    typographique propre vaut mieux qu'un ecran qui attend une photo qui
    ne viendra pas — et il reste publiable tel quel.
    """
    d = pathlib.Path(dossier or (SORTIE / "stories"))
    accent("violet")
    f = []
    # code, fond, encre, surtitre, texte, titre du sticker, lignes
    E = [
     ("S1-A", "sable_chaud", "encre", "Nouveau post",
      "Votre couleur parle avant vous.",
      "Sondage", ["Le bleu marine évoque plutôt…", "A : la confiance", "B : le luxe"]),
     ("S1-B1", "sable_chaud", "encre", "Réglementation",
      "Enseigne : déclaration ou autorisation ?",
      "Quiz", ["Pour poser une enseigne, il faut…",
               "Une déclaration préalable", "Une autorisation préalable"]),
     ("S1-B2", "sable_chaud", "encre", "La réponse",
      "Autorisation.\nCerfa 16308*01, en mairie, en trois exemplaires.",
      "Mention du post", ["Le détail est dans le post du jour."]),
     ("S1-C", "sable_chaud", "encre", "Boîte à questions",
      "Une question sur votre identité visuelle ?",
      "Boîte à questions", ["Je réponds à tout.", "Même aux questions bêtes.",
                            "Surtout à celles-là."]),
     ("S1-D1", "creme", "encre", "Le vote du jeudi",
      "Laquelle se lit à vingt mètres ?", "Sondage", ["A", "B"]),
     ("S1-D2", "sable_chaud", "encre", "La réponse",
      "Réponse : B.\nÀ vingt mètres, une typo devient une silhouette.",
      "Curseur emoji", ["Vous aviez deviné ?"]),
     ("S1-E", "creme", "encre", "Nouvel article",
      "L'autorisation d'enseigne, étape par étape.",
      "Lien", ["grafycom.fr/blog"]),
     ("S2-A", "sable_chaud", "encre", "Nouveau post",
      "Cette police est magnifique.\nEt pourtant…",
      "Curseur emoji", ["Vous choisissez vos polices au feeling ?"]),
     ("S2-B", "sable_chaud", "encre", "Droits & propriété",
      "Avez-vous un contrat de cession pour votre logo ?",
      "Sondage", ["Votre logo, vous le possédez…",
                  "A : oui, j'ai l'écrit", "B : aucune idée"]),
     ("S2-C", "creme", "encre", "Coulisses",
      "Trois pistes pour un même logo.\nDeux finiront à la corbeille.",
      "", ["C'est normal. C'est même le travail."]),
     ("S2-D1", "sable_chaud", "encre", "Le quiz du jeudi",
      "4 idées reçues. Testez-vous.",
      "Quiz 4 choix", ["Laquelle est VRAIE ?", "Une enseigne se déclare",
                       "Un logo doit tenir en noir et blanc",
                       "300 DPI convient à tout",
                       "Une police gratuite est libre"]),
     ("S2-D2", "sable_chaud", "encre", "La réponse",
      "Un logo doit tenir en noir et blanc.",
      "Mention du post", ["Les trois autres sont fausses.",
                          "Le détail est dans le post."]),
     ("S2-E", "creme", "encre", "Nouvel article",
      "Choisir le bon support d'impression.",
      "Lien", ["grafycom.fr/blog"]),
     ("S2-F", "encre", "blanc", "Halloween",
      "Décorer sa vitrine ne coûte rien, et se remarque.",
      "Curseur emoji", ["Les trois pièges : trop de texte,",
                        "orange sur noir illisible,",
                        "adhésif qu'on ne décollera pas lundi."]),
     ("S3-A", "creme", "encre", "Nouveau post",
      "Votre logo tient-il sur un stylo ?",
      "Sondage", ["Qu'est-ce qui disparaît en premier ?",
                  "A : les couleurs", "B : le texte sous le symbole"]),
     ("S3-B1", "sable_chaud", "encre", "Quiz enseigne",
      "Vous éclairez votre enseigne existante.\nFaut-il refaire une démarche ?",
      "Quiz", ["Non, elle est déjà autorisée", "Oui, probablement"]),
     ("S3-B2", "sable_chaud", "encre", "La réponse",
      "Oui, probablement.",
      "Mention du post", ["Éclairer une enseigne, c'est la modifier.",
                          "Une nouvelle autorisation serait due.",
                          "À confirmer en mairie."]),
     ("S3-C", "sable_chaud", "encre", "Boîte à questions",
      "Une question sur votre enseigne, vos imprimés, votre logo ?",
      "Boîte à questions", ["Je réponds à tout,",
                            "même aux questions qui paraissent bêtes.",
                            "Surtout à celles-là."]),
     ("S3-D1", "creme", "encre", "Le vote du jeudi",
      "Même carte, mêmes prix.\nLaquelle fait commander le plat ?",
      "Sondage", ["A : prix au fil du texte", "B : prix alignés à droite"]),
     ("S3-D2", "sable_chaud", "encre", "La réponse",
      "A.",
      "Curseur emoji", ["Une colonne de prix se lit de haut en bas :",
                        "le client compare six chiffres,",
                        "et choisit un chiffre."]),
     ("S3-E1", "creme", "encre", "Nouvel article",
      "Habiller sa vitrine : dépoli, microperforé, lettres découpées.",
      "Lien", ["grafycom.fr/blog"]),
     ("S3-E2", "sable_chaud", "encre", "Le reel est en ligne",
      "Votre vitrine\nfait 6 m².",
      "Mention du post", ["Le reel du jour"]),
     ("S4-A", "creme", "encre", "Nouveau post",
      "Je présente toujours trois pistes.\nDeux sont faites pour être écartées.",
      "Curseur emoji", ["Vous trouvez ça logique ?"]),
     ("S4-B1", "sable_chaud", "encre", "Quiz langue",
      "« Sunset Coffee », et sur le store « Best coffee in town ».\nLequel pose question ?",
      "Quiz", ["Le nom", "Le slogan"]),
     ("S4-B2", "sable_chaud", "encre", "La réponse",
      "Le slogan.",
      "Mention du post", ["Ce qui vous nomme resterait libre.",
                          "Ce qui informe le client serait attendu",
                          "en français, ou accompagné."]),
     ("S4-C", "creme", "encre", "Coulisses",
      "14 h 40. Une piste de logo qui ne sortira jamais.",
      "", ["Elle sert quand même : c'est en la regardant",
           "qu'on comprend ce qu'on cherche."]),
     ("S4-D1", "sable_chaud", "encre", "Le quiz du jeudi",
      "Quatre matières en gros plan.\nCelle-ci, c'est quoi ?",
      "Quiz 4 choix", ["Alu composite", "Plexiglas", "PVC expansé",
                       "Inox brossé"]),
     ("S4-D2", "creme", "encre", "Les quatre réponses",
      "Chaque matière a son emploi.",
      "Mention du post", ["Alu composite : le panneau qui ne gondole pas.",
                          "Plexi : l'intérieur, les lettres.",
                          "Dépoli : la vitrine qu'on masque.",
                          "Papier gaufré : la carte qu'on garde."]),
     ("S4-E", "creme", "encre", "Nouvel article",
      "Les supports de fin d'année se commandent maintenant.",
      "Lien", ["grafycom.fr/blog"]),
     ("S4-F", "sable_chaud", "encre", "Le reel du jour",
      "Pour Noël, vous êtes déjà en retard.",
      "Compte à rebours", ["Bon à tirer de fin d'année",
                           "réglé au 7 décembre"]),
     ("S5-A", "sable_chaud", "encre", "Nouveau post",
      "Vos cartes de vœux de Noël se décident cette semaine.",
      "Sondage", ["Pour vos supports de fin d'année…",
                  "A : déjà commandé", "B : j'y pense depuis septembre"]),
     ("S5-B1", "sable_chaud", "encre", "Réglementation",
      "Votre emballage de fête a une mention à porter.",
      "Quiz", ["La signalétique de tri se place…",
               "Quand le dessin est prêt", "Avant de dessiner"]),
     ("S5-B2", "sable_chaud", "encre", "La réponse",
      "Avant de dessiner.",
      "Mention du post", ["Elle a besoin d'une place",
                          "et d'une zone de respiration.",
                          "Ajoutée à la fin, elle se colle en travers."]),
     ("S5-C1", "creme", "encre", "Le vote du jeudi",
      "Deux cartes de vœux. Même papier, même logo.",
      "Sondage", ["Laquelle garderiez-vous ?", "A : Joyeuses fêtes",
                  "B : Merci d'être venu"]),
     ("S5-C2", "sable_chaud", "encre", "La réponse",
      "La B.",
      "Curseur emoji", ["Pas parce qu'elle est plus belle :",
                        "parce qu'elle parle à quelqu'un."]),
     ("S5-D", "creme", "encre", "Nouvel article",
      "Votre vitrine de fin d'année, vue du trottoir.",
      "Lien", ["grafycom.fr/blog"]),
     ("S5-E", "sable_chaud", "encre", "Boîte à questions",
      "Vous préparez quelque chose pour les fêtes ?",
      "Boîte à questions", ["Votre question, et j'y réponds."]),
     ("S6-A", "encre", "blanc", "Nouveau post",
      "Votre vitrine de Noël est faite pour celui qui passe.",
      "Curseur emoji", ["Votre vitrine, vous la regardez",
                        "depuis le trottoir d'en face ?"]),
     ("S6-B1", "sable_chaud", "encre", "Quiz réglementation",
      "Un sticker « -30 % » sur votre vitrine : on le déclare ou on l'autorise ?",
      "Quiz", ["Pour une enseigne, il faut…",
               "Une déclaration préalable", "Une autorisation préalable"]),
     ("S6-B2", "blanc", "encre", "La réponse",
      "Une autorisation.",
      "Mention du post", ["Une enseigne dit qui vous êtes : on l'autorise.",
                          "Une publicité dit ce que vous vendez :",
                          "on la déclare."]),
     ("S6-C1", "sable_chaud", "encre", "Le quiz du jeudi",
      "Le doré d'une dorure à chaud, c'est quoi ?",
      "Quiz 4 choix", ["De l'encre jaune très saturée",
                       "Une feuille métallisée pressée à chaud",
                       "Un vernis teinté",
                       "Une quadrichromie renforcée"]),
     ("S6-C2", "encre", "blanc", "La réponse",
      "Une feuille métallisée, pressée à chaud.",
      "Mention du post", ["Aucune encre ne brille.",
                          "C'est pour ça que ça se voit,",
                          "et que ça se paie."]),
     ("S6-D", "creme", "encre", "Nouvel article",
      "Faut-il refaire son logo pour la nouvelle année ?",
      "Lien", ["grafycom.fr/blog"]),
     # S6-E annoncait « cinq plans, un carnet et une lampe » : le reel
     # n° 24 ne se tourne plus, il est dessine. Une story qui promet des
     # coulisses de tournage qui n'existent pas se voit tout de suite.
     ("S6-E", "creme", "encre", "Coulisses",
      "Deux pages de calendrier, décembre et janvier.",
      "", ["Identiques à un mot près.",
           "C'est tout l'argument du reel du jour."]),
    ]
    for code, fond, enc, sur, titre, st, lignes in E:
        p = Planche(fond, LARGE_S, HAUT_S)
        p.surtitre(sur, "taupe" if enc == "encre" else "sable", y=300)
        p.filet()
        p.titre(titre, 76, enc)
        if st:
            p.sticker(st, lignes, y=HAUT_S - 760)
        else:
            p.y += 40
            p.texte("\n".join(lignes), 42, enc, 400, avant=20)
        p.signature(enc if enc != "encre" else "brun")
        f.append(p.ecrire(d / ("%s.png" % code)))
    return f



GABARITS = {
    "carrousel-couleurs": carrousel_couleurs,
    "dilemme-enseigne": dilemme_enseigne,
    "carrousel-typographie": carrousel_typographie,
    "carrousel-enseigne": carrousel_enseigne,
    "quiz-idees-recues": quiz_idees_recues,
    "carrousel-droits": carrousel_droits,
    "dilemme-carte-prix": dilemme_carte_prix,
    "retroplanning-voeux": carrousel_retroplanning,
    "dilemme-voeux": dilemme_voeux,
    "quiz-fin-annee": quiz_fin_annee,
    "blog-rendez-vous": carrousel_blog_rdv,
    "stories": stories,
}




def solaire_66(dossier=None):
    """n° 13, lundi 9 novembre : l'identité Solaire 66.

    Solaire 66 et Grafycom sont deux entreprises distinctes, dirigées par
    deux personnes distinctes — precision de Laurent le 13 octobre. C'est
    donc un client comme un autre, dont l'accord de publication est acquis
    a la source puisqu'il commande aussi ces publications.

    Les sources sont vectorielles (LOGO_OK.pdf, rendu à 100 dpi sur une
    planche de 1000 mm puis recadré sur le dessin) et les cartes viennent
    du PDF d'impression à 300 dpi.

    DIMENSIONS REELLES, fournies par Laurent, jamais devinées :
      panneau de chantier  120 x 80 cm
      carte de visite      8,5 x 5,5 cm
    La planche 5 les pose à l'échelle exacte — 8,5 / 120 = 7,08 %.

    Ce gabarit ne fait pas de mise en situation photographique : la carte
    n'est pas dans une main, le panneau n'est pas sur une palissade. Ça
    demanderait une photo de base, et on ne publie pas une image dont les
    droits ne sont pas clairs.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-16-solaire-66"))
    accent("bleu")
    S = RACINE / "visuels" / "sources"
    MM = 1052 / 89              # px par mm du rendu 300 dpi des cartes
    PANNEAU_CM, CARTE_CM = 120.0, 8.5
    faits = []

    p = Planche("blanc")
    p.surtitre("Réalisation", y=140, centre=True)
    p.poser(S / "solaire-66-logo.png", 540, 640, 960, ombre=0)
    p.y = 1150
    p.texte("Solaire 66 — identité livrée", 34, "taupe", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("creme")
    p.titre("Ces deux couleurs" + "\n" + "ne sont pas un goût.", 72, y=150)
    for cx, hexa, legende in ((330, "#10638b", "la mer"),
                              (750, "#f5b32d", "le soleil")):
        p.d.ellipse([cx - 150, 560, cx + 150, 860], fill=hexa)
        f = police(600, 40)
        l = p.d.textlength(legende, font=f)
        p.d.text((cx - l / 2, 900), legende, font=f, fill=teinte("brun"))
    p.y = 1000
    p.texte("Elles viennent de Canet-en-Roussillon, où l'entreprise est "
            "installée. Une palette qui vient du lieu tient plus longtemps "
            "qu'une palette qui vient d'une tendance.", 38, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "02.png"))

    p = Planche("blanc")
    p.titre("Regardez\nle O.", 100, y=160)
    p.poser(S / "solaire-66-logo.png", 540, 680, 880, ombre=0)
    p.y = 900
    p.texte("Ce n'est pas un O avec un soleil posé dessus. C'est le soleil "
            "qui tient le rôle du O. Un symbole posé à côté d'un nom peut "
            "toujours s'en détacher ; devenu une lettre, il ne peut plus "
            "partir sans emporter le mot.", 38, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("creme")
    p.titre("Une carte de visite" + "\n" + "fait 85 millimètres.", 74, y=140)
    p.poser(S / "solaire-66-carte-verso.png", 700, 900, 540, angle=-6,
            rogner_mm=2, mm_par_px=MM)
    p.poser(S / "solaire-66-carte-recto.png", 390, 640, 540, angle=6,
            rogner_mm=2, mm_par_px=MM)
    p.signature("brun")
    faits.append(p.ecrire(d / "04.png"))

    # La planche qui porte la demonstration : a l'echelle exacte.
    p = Planche("creme")
    p.titre("À l'échelle exacte.", 80, y=140)
    larg_panneau = 860
    larg_carte = int(round(larg_panneau * CARTE_CM / PANNEAU_CM))
    p.poser(S / "solaire-66-panneau.png", 500, 640, larg_panneau, angle=0)
    p.poser(S / "solaire-66-carte-recto.png", 880, 1010, larg_carte, angle=0,
            rogner_mm=2, mm_par_px=MM)
    f = police(600, 30)
    p.d.text((MARGE, 975), "panneau 120 × 80 cm", font=f, fill=teinte("taupe"))
    p.d.text((790, 1060), "8,5 cm", font=f, fill=teinte("taupe"))
    p.y = 1120
    p.texte("La carte occupe 7 % de la largeur du panneau. Le même dessin "
            "doit tenir aux deux.", 34, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "05.png"))

    # Le monochrome : possible parce que les contreformes sont ajourees.
    p = Planche("creme")
    p.titre("En une seule couleur.", 68, y=150)
    p.poser(S / "solaire-66-logo-mono-bleu.png", 540, 450, 620, ombre=0)
    p.d.rectangle([0, 660, LARGE, 1030], fill=teinte("encre"))
    p.poser(S / "solaire-66-logo-mono-blanc.png", 540, 845, 620, ombre=0)
    p.y = 1075
    p.texte("Gravure, broderie, tampon : une seule encre. Les lettres sont "
            "ajourées, pas remplies de blanc — c'est ce qui le permet.",
            33, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "06.png"))

    p = Planche("sable_chaud")
    p.filet(y=200)
    p.titre("Dessiné en grand." + "\n" + "Vérifié en petit.", 78)
    p.y = 520
    p.texte("Sur un panneau de chantier, un logo peut tout se permettre. "
            "Sur 8,5 centimètres, dans un avatar, brodé sur un polo, le "
            "détail devient de la bouillie.", 38, "brun", 400, avant=0)
    p.y = 720
    p.texte("C'est pour ça qu'une identité livrée ne contient jamais un "
            "seul fichier.", 40, "encre", 600, avant=0)
    p.signature("blanc")
    faits.append(p.ecrire(d / "07.png"))

    # Pilier « la personne », sur la seule publication du cycle qui
    # montre un vrai client. Un travail livré se raconte mieux avec la
    # personne qui l'a livré.
    p = Planche("creme")
    p.photo("sandra-ecran", ancrage="centre", voile="encre", part=0.54)
    p.y = 856
    p.titre("Trois semaines,\net un logo qui tient\nsur un stylo.", 60, "blanc")
    p.texte("Sandra, Grafycom — Perpignan.", 34, "creme", 600, avant=26)
    p.signature("creme")
    faits.append(p.ecrire(d / "08.png"))

    return faits


# ---------------------------------------------------------------------
# Un logo fictif, dessine, pour les demonstrations de reduction.
# Il n'imite aucune marque existante : c'est un exercice, et la legende
# de la publication le dit.
# ---------------------------------------------------------------------
def _logo_fictif(d, cx, cy, r, detail=True, variante=0.0):
    """Le logo d'exercice. variante decale legerement les deux anneaux.

    La n° 24 doit montrer « deux versions presque identiques » : si elles
    etaient rigoureusement identiques, on croirait a une erreur de
    montage ; si elles differaient vraiment, la demonstration tomberait.
    Un ecart de quelques pourcents sur les anneaux est exactement ce que
    produit une refonte faite par calendrier.
    """
    from PIL import ImageDraw
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=teinte("bleu"))
    m = .72 + variante
    i = .44 - variante * 0.6
    d.ellipse([cx - r * m, cy - r * m, cx + r * m, cy + r * m],
              fill=teinte("bleu_vif"))
    d.ellipse([cx - r * i, cy - r * i, cx + r * i, cy + r * i],
              fill=teinte("creme"))
    if detail and r > 26:
        for i in range(10):          # les contours fins, premiers a disparaitre
            a = r * (.80 + i * .012)
            d.arc([cx - a, cy - a, cx + a, cy + a], 200 + i * 14, 250 + i * 14,
                  fill=teinte("blanc"), width=max(1, int(r / 60)))
        f = police(600, max(8, int(r * .17)))
        t = "ATELIER DU PONT"
        l = d.textlength(t, font=f)
        d.text((cx - l / 2, cy + r * 1.12), t, font=f, fill=teinte("encre"))


def pub09_logo_reduction(dossier=None):
    """n° 9, lundi 2 novembre — un logo tient-il en petit."""
    d = pathlib.Path(dossier or (SORTIE / "2026-11-09-logo-reduction"))
    accent("bleu")
    faits = []

    p = Planche("creme")
    p.surtitre("Conseil", y=130)
    p.filet()
    p.titre("Votre logo tient-il" + "\n" + "sur un stylo ?", 78)
    _logo_fictif(p.d, 400, 760, 210)
    _logo_fictif(p.d, 790, 760, 26)
    f = police(400, 30)
    p.d.text((742, 830), "même logo, 8 mm", font=f, fill=teinte("taupe"))
    p.y = 1120
    p.texte("Exercice de style — logo non commandé.", 30, "taupe", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("blanc")
    p.titre("On réduit, et on regarde.", 86, y=150)
    for cx, r in ((280, 180), (640, 86), (870, 44)):
        _logo_fictif(p.d, cx, 640, r)
    p.y = 920
    p.texte("Le test prend trois secondes : on réduit, et on regarde ce qui "
            "disparaît en premier.", 38, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "02.png"))

    p = Planche("sable_chaud")
    p.filet(y=170)
    p.titre("Ce qui disparaît" + "\n" + "en premier.", 92, "encre")
    p.puces(["les dégradés", "les ombres portées", "les contours fins",
             "le texte placé sous le symbole"],
            "corail", 42, "brun", y=640, interligne=1.6)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("creme")
    p.titre("Un logo doit exister" + "\n" + "en une seule couleur.", 64, y=150)
    _logo_fictif(p.d, 300, 700, 150)
    p.d.ellipse([570, 550, 870, 850], fill=teinte("encre"))
    p.d.ellipse([570 + 42, 550 + 42, 870 - 42, 850 - 42], fill=teinte("creme"))
    p.d.ellipse([570 + 84, 550 + 84, 870 - 84, 850 - 84], fill=teinte("encre"))
    p.y = 930
    p.texte("Tampon, broderie, gravure, fax du comptable : tout ça n'a "
            "qu'une encre.", 38, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "04.png"))

    p = Planche("creme")
    p.titre("Le même, cinq fois," + "\n" + "sans retouche.", 72, y=150)
    supports = [("carte de visite", 240, 560), ("polo brodé", 560, 560),
                ("flanc de camionnette", 880, 560), ("panneau", 320, 850),
                ("favicon", 760, 850)]
    f = police(600, 26)
    for nom, cx, cy in supports:
        _logo_fictif(p.d, cx, cy, 72)
        l = p.d.textlength(nom, font=f)
        p.d.text((cx - l / 2, cy + 92), nom, font=f, fill=teinte("violet"))
    p.y = 1030
    p.texte("Si l'un des cinq demande une retouche, c'est le logo qu'il "
            "faut revoir, pas le support.", 36, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "05.png"))

    p = Planche("encre")
    p.filet(y=320)
    p.titre("Faites le test" + "\n" + "ce soir.", 92, "blanc")
    p.y = 700
    p.texte("Réduisez votre logo à la taille d'un ongle. Si vous ne le "
            "reconnaissez plus, vos clients non plus.", 40, "creme", 400,
            avant=0)
    p.fleche("corail", y=950)
    p.signature("sable")
    faits.append(p.ecrire(d / "06.png"))
    return faits

# =====================================================================
# LES SCENES DESSINEES
# ---------------------------------------------------------------------
# Huit publications du cycle de novembre attendaient une photographie :
# une rue au crepuscule, deux devantures, quatre matieres en macro, un
# emballage, une vitrine de nuit, un calendrier. Sandra a dit que les
# prises de vue etaient tres difficiles pour elle. Plutot que de laisser
# huit trous dans le calendrier, ces huit publications sont redessinees.
#
# Ce n'est pas un pis-aller, et surtout ce n'est pas la meme chose que
# demander l'image a un modele generatif :
#
# 1. Un dessin ne pretend pas etre une photo. Une image generee, si — et
#    elle se trahit sur les enseignes, en pseudo-lettres. Le 13 octobre,
#    deux images proposees ici portaient « S A.CKS » et « Tïvllts » sur
#    leurs devantures. Une facade dessinee de loin porte des barres
#    abstraites : personne ne lit un texte qui n'est pas ecrit, et quand
#    un lettrage doit se lire, il est compose avec Inter, accents inclus.
# 2. Les droits sont clairs : le trace sort de ce fichier.
# 3. Aucun commerce reel n'est reconnaissable. Quatre de ces huit
#    publications parlent de non-conformite ; aucune ne peut illustrer
#    le sujet avec la vitrine de quelqu'un, meme floutee.
# 4. Sur deux sujets, le dessin montre mieux que la photo. La coupe d'un
#    alu composite fait voir l'ame noire entre les deux peaux, qu'aucune
#    macro ne donne aussi nettement ; et la meme vitrine redessinee a
#    trois distances fait une demonstration qu'aucun cadrage unique ne
#    rend.
#
# Ce que le dessin ne remplace pas, et ou la liste de
# photos-a-prendre.md reste entiere : les matieres en lumiere rasante
# (une dorure, un gaufrage, un vernis selectif) et les realisations en
# situation. Ces deux familles se photographient le jour ou ce sera
# possible ; les planches dessinees tiennent d'ici la.
# =====================================================================

HAUTEUR_DEVANTURE_M = 3.2     # hauteur de reference d'une devanture, en
                              # metres : c'est elle qui place la bande
                              # des yeux a 1,40-1,70 m dans les dessins.


def _melange(a, b, k):
    """Un ton intermediaire entre deux couleurs de la charte.

    La nuit, une facade n'est pas de la couleur de la charte : elle en
    est une version assombrie. Plutot que d'ecrire des valeurs en dur —
    ce que charte.py --verifier refuse, et avec raison — on interpole
    entre deux couleurs qui viennent, elles, de la feuille de style.
    """
    ca, cb = teinte(a), teinte(b)
    return tuple(int(int(ca[i:i + 2], 16)
                     + (int(cb[i:i + 2], 16) - int(ca[i:i + 2], 16)) * k)
                 for i in (1, 3, 5))


# ---------------------------------------------------------------------
# Le rendu des objets : ce qui separe un schema d'un objet pose quelque
# part. Trois choses, et aucune ne coute un centime :
#
#   1. une ombre de contact. Un objet sans ombre flotte, et c'est le
#      premier signe qui fait lire « illustration » plutot que « chose
#      photographiee » ;
#   2. un modele de lumiere. Un aplat uni n'existe pas dans le monde :
#      une surface prend plus de lumiere d'un cote que de l'autre ;
#   3. un grain de matiere. Le papier, le kraft, le beton ont un bruit
#      propre ; le verre n'en a pas, et c'est ce contraste qui dit
#      « verre ».
#
# Elles s'appliquent aux objets dessines, jamais au fond de la planche
# ni au texte : un titre grene est un titre sale.
# ---------------------------------------------------------------------
def pose(flou=20, force=78, bas=15, cote=6, modele=0.26,
         grain=9):
    """Décorateur : l'objet dessiné reçoit l'ombre de sa propre silhouette.

    L'ombre rectangulaire de _ombre_contact() suppose que l'objet
    remplit sa boite. C'est vrai d'une devanture, faux d'un sachet, d'une
    carte tournee ou d'un logo rond — et une ombre carree sous un objet
    rond est pire que pas d'ombre du tout.

    Ici on ne suppose rien : on photographie la planche avant l'appel,
    on laisse la fonction dessiner, et on compare. Les pixels qui ont
    change SONT la silhouette de l'objet. On la floute, on la decale,
    on la pose sur l'etat d'avant, puis on remet l'objet par-dessus.
    L'ombre est donc exacte quoi que la fonction ait trace, et le jour
    ou une fonction change de forme, l'ombre suit sans qu'on y touche.
    """
    def enveloppe(fn):
        import functools

        @functools.wraps(fn)
        def appel(p, *a, **kw):
            avant = p.im.copy()
            r = fn(p, *a, **kw)
            if not GRAIN and not force:
                return r
            diff = ImageChops.difference(p.im.convert("RGB"),
                                         avant.convert("RGB")).convert("L")
            silhouette = diff.point(lambda v: 255 if v > 16 else 0)
            if not silhouette.getbbox():
                return r
            ombre = Image.new("RGBA", p.im.size, (0, 0, 0, 0))
            teint = Image.new("RGBA", p.im.size, (32, 26, 22, 255))
            decale = Image.new("L", p.im.size, 0)
            decale.paste(silhouette, (cote, bas))
            ombre.paste(teint, (0, 0),
                        decale.point(lambda v: int(v * force / 255)))
            # La silhouette est déjà calculée : elle dit aussi où
            # l'objet S'ARRÊTE. _deborde() ne surveille que le bas de
            # planche, et rien ne regardait les côtés — une rangée de
            # vignettes trop large sortait du cadre sans un mot. C'est
            # gratuit ici, et ça ferme le dernier bord non gardé.
            bx = silhouette.getbbox()
            if bx and (bx[0] < MARGE - 24 or bx[2] > p.l - MARGE + 24):
                p.debordements_lateraux = getattr(
                    p, "debordements_lateraux", [])
                p.debordements_lateraux.append(
                    (fn.__name__, max(0, MARGE - bx[0]),
                     max(0, bx[2] - (p.l - MARGE))))

            ombre = ombre.filter(ImageFilter.GaussianBlur(flou))
            fond = Image.alpha_composite(avant.convert("RGBA"), ombre)

            # L'ombre decolle l'objet du fond ; elle ne lui donne pas de
            # volume. Un aplat uni reste un aplat uni, et c'est le second
            # signe qui fait lire « schema » : dans le monde, une surface
            # prend plus de lumiere d'un cote que de l'autre, et une
            # matiere a un grain. Les deux se posent ICI, sur la seule
            # silhouette de l'objet — jamais sur le fond de la planche,
            # jamais sur le texte des gabarits.
            objet = p.im.convert("RGB")
            if modele:
                rampe = _degrade_lineaire(p.l, p.h, 138.0,
                                          [(0.0, "#ffffff"), (1.0, "#000000")])
                gris = rampe.convert("L").point(
                    lambda v: int(128 + (v - 128) * modele))
                objet = ImageChops.overlay(
                    objet, Image.merge("RGB", (gris,) * 3))
            if grain:
                import random
                al = random.Random(13)
                pt = (max(1, p.l // 3), max(1, p.h // 3))
                petit = Image.new("L", pt)
                petit.putdata([128 + al.randint(-grain, grain)
                               for _ in range(pt[0] * pt[1])])
                bruit = petit.resize((p.l, p.h), Image.BILINEAR)
                objet = Image.blend(
                    objet, ImageChops.overlay(objet,
                                              Image.merge("RGB", (bruit,) * 3)),
                    0.5)

            fond.paste(objet.convert("RGBA"), (0, 0), silhouette)
            p.im = fond.convert("RGB")
            p._redessiner()
            return r
        return appel
    return enveloppe


def _ombre_contact(p, boite, flou=22, force=86, bas=16, cote=6):
    """L'ombre portée d'un objet posé, decalee vers le bas.

    Decalee vers le bas et a peine sur le cote : la lumiere des
    planches vient d'en haut a gauche, comme celle d'une fenetre, et
    une ombre qui partirait dans un autre sens se remarque aussitot.
    """
    x0, y0, x1, y1 = boite
    calque = Image.new("RGBA", p.im.size, (0, 0, 0, 0))
    ImageDraw.Draw(calque).rounded_rectangle(
        [x0 + cote, y0 + bas, x1 + cote, y1 + bas],
        radius=max(2, int((x1 - x0) * 0.02)), fill=(32, 26, 22, force))
    calque = calque.filter(ImageFilter.GaussianBlur(flou))
    p.im = Image.alpha_composite(p.im.convert("RGBA"), calque).convert("RGB")
    p._redessiner()
    return p


def _modele(p, boite, couleur, angle=138.0, amplitude=0.16, rayon=0):
    """Une surface éclairée, au lieu d'un aplat uni.

    La couleur donnee reste la couleur de l'objet : on l'eclaircit d'un
    cote et on l'assombrit de l'autre, autour d'elle. L'objet garde donc
    sa valeur de charte, et gagne un volume.
    """
    x0, y0, x1, y1 = (int(v) for v in boite)
    lx, ly = max(1, x1 - x0), max(1, y1 - y0)
    base = teinte(couleur) if isinstance(couleur, str) else None
    if base is None:
        rvb = couleur
    else:
        rvb = tuple(int(base[i:i + 2], 16) for i in (1, 3, 5))
    clair = tuple(min(255, int(c + 255 * amplitude * 0.55)) for c in rvb)
    sombre = tuple(max(0, int(c - 255 * amplitude * 0.45)) for c in rvb)
    hx = lambda c: "#%02x%02x%02x" % c
    deg = _degrade_lineaire(lx, ly, angle, [(0.0, hx(clair)), (1.0, hx(sombre))])
    if rayon:
        m = Image.new("L", (lx, ly), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, lx - 1, ly - 1],
                                            radius=rayon, fill=255)
        p.im.paste(deg, (x0, y0), m)
    else:
        p.im.paste(deg, (x0, y0))
    p._redessiner()
    return p


def _grain_matiere(p, boite, force=9, echelle=2):
    """Le grain propre d'une matière, sur la seule surface concernée."""
    import random
    x0, y0, x1, y1 = (int(v) for v in boite)
    lx, ly = max(1, x1 - x0), max(1, y1 - y0)
    al = random.Random(3)
    petit = Image.new("L", (max(1, lx // echelle), max(1, ly // echelle)))
    petit.putdata([128 + al.randint(-force, force)
                   for _ in range(petit.width * petit.height)])
    bruit = petit.resize((lx, ly), Image.BILINEAR)
    zone = p.im.crop((x0, y0, x1, y1)).convert("RGB")
    fusion = ImageChops.overlay(zone, Image.merge("RGB", (bruit,) * 3))
    p.im.paste(Image.blend(zone, fusion, 0.55), (x0, y0))
    p._redessiner()
    return p


def _reflet_verre(p, boite, force=52, largeur=0.26, angle=-22):
    """La bande spéculaire d'une vitre. C'est elle qui dit « c'est du verre »."""
    import math
    x0, y0, x1, y1 = (int(v) for v in boite)
    lx, ly = max(1, x1 - x0), max(1, y1 - y0)
    calque = Image.new("RGBA", (lx, ly), (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)
    w = int(lx * largeur)
    dec = int(ly * math.tan(math.radians(abs(angle))))
    for i, (ox, a) in enumerate(((0.10, force), (0.44, int(force * 0.45)))):
        bx = int(lx * ox)
        d.polygon([(bx, 0), (bx + w, 0), (bx + w - dec, ly), (bx - dec, ly)],
                  fill=(255, 255, 255, a))
    calque = calque.filter(ImageFilter.GaussianBlur(max(2, lx // 90)))
    zone = p.im.crop((x0, y0, x1, y1)).convert("RGBA")
    p.im.paste(Image.alpha_composite(zone, calque).convert("RGB"), (x0, y0))
    p._redessiner()
    return p


def _halo(p, cx, cy, rx, ry, couleur, force=110, flou=46):
    """Une lueur, pour une enseigne allumee ou une vitrine eclairee.

    Un aplat net ne fait pas une lumiere : c'est le degrade au bord qui
    la fait. On dessine donc l'ellipse sur un calque, on la floute, et
    on la compose par transparence.
    """
    calque = Image.new("RGBA", p.im.size, (0, 0, 0, 0))
    ImageDraw.Draw(calque).ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                                   fill=teinte(couleur) + "%02x" % force)
    calque = calque.filter(ImageFilter.GaussianBlur(flou))
    p.im = Image.alpha_composite(p.im.convert("RGBA"), calque).convert("RGB")
    p._redessiner()
    return p


def _bloc(p, x, y, texte, taille=34, couleur="brun", graisse=400,
          largeur=None, interligne=1.34, centre=False):
    """Un paragraphe pose a une abscisse libre, pour les mises en colonnes.

    Planche.texte() ecrit toujours a la marge : c'est ce qu'il faut pour
    une page de carrousel, et ce qui ne marche pas pour deux colonnes
    cote a cote. Renvoie l'ordonnee atteinte, pour enchainer.
    """
    f = police(graisse, taille)
    largeur = largeur or (p.l - x - MARGE)
    for ligne in couper(texte, f, largeur):
        xx = x + (largeur - p.d.textlength(ligne, font=f)) / 2 if centre else x
        p.d.text((xx, y), ligne, font=f, fill=teinte(couleur))
        y += int(taille * interligne)
    return y


def _bandeau_travers(p, texte, couleur="violet", y=None, taille=56,
                     sous_titre=None, couleur_texte="blanc"):
    """Le bandeau plein en travers de l'image, la S1 de quatre carrousels.

    Il sert a poser le titre sur une scene : sans aplat derriere, un
    texte blanc sur un dessin se lit mal des que le dessin a du detail.
    """
    f = police(800, taille)
    lignes = couper(texte, f, p.l - 2 * MARGE)
    fs = police(400, 32)
    lignes_s = couper(sous_titre, fs, p.l - 2 * MARGE) if sous_titre else []
    haut = (40 + len(lignes) * int(taille * 1.2)
            + (len(lignes_s) * 44 + 16 if lignes_s else 0) + 40)
    y = int(p.h * 0.50 - haut / 2) if y is None else y
    # Le bandeau est APPROFONDI juste assez pour que son texte passe.
    # Mesure : du crème sur le violet de la charte donne 4,13:1, et le
    # seuil d'un texte de légende est 4,5. Les teintes de la charte sont
    # faites pour de petits accents sur du crème, pas pour porter du
    # texte en aplat — c'est le même constat que pour les surtitres, et
    # la même réponse : on s'arrête au premier pas qui passe.
    fonce = _assez_fonce(couleur, couleur_texte)
    p.d.rectangle([0, y, p.l, y + haut], fill=fonce)
    yy = y + 40
    for ligne in lignes:
        p.d.text((MARGE, yy), ligne, font=f, fill=teinte(couleur_texte))
        yy += int(taille * 1.2)
    if lignes_s:
        yy += 16
        for ligne in lignes_s:
            p.d.text((MARGE, yy), ligne, font=fs, fill=teinte(couleur_texte))
            yy += 44
    p.y = y + haut + 30
    return p


# ---------------------------------------------------------------------
# La rue au crepuscule — n° 10, et reemployee en n° 14 et 21.
# ---------------------------------------------------------------------
def _enseigne_lointaine(p, x, y, larg, haut, couleur, allumee=True,
                        barres=3):
    """Une enseigne vue de loin : un caisson et des barres, pas un mot.

    C'est le choix qui distingue ce dessin d'une image generee. A cette
    echelle, un oeil ne lit pas une enseigne de l'autre cote de la rue,
    il voit un bandeau clair et le rythme de ses lettres. Des barres
    disent cela exactement, et ne pretendent pas ecrire un nom.
    """
    p.d.rounded_rectangle([x, y, x + larg, y + haut], radius=max(2, haut // 5),
                          fill=teinte(couleur) if allumee
                          else _melange(couleur, "encre", 0.72))
    f = _melange("blanc", couleur, 0.15) if allumee else _melange("encre", couleur, 0.25)
    ep = max(2, haut // 6)
    marge = larg * 0.12
    util = larg - 2 * marge
    pas = util / barres
    for i in range(barres):
        bx = x + marge + i * pas
        p.d.rectangle([bx, y + haut / 2 - ep / 2,
                       bx + pas * 0.62, y + haut / 2 + ep / 2], fill=f)
    return p


def _facade_rue(p, x, y_sol, larg, haut_total, teinte_mur, allumee=True,
                etages=2, couleur_enseigne="corail", nuit=0.62):
    """Une facade d'immeuble de centre ancien, en elevation.

    Rez-de-chaussee commercial, enseigne en bandeau, un ou deux etages
    de fenetres au-dessus. Le parametre nuit dose l'assombrissement :
    0 en plein jour, 0,62 au crepuscule.
    """
    y_haut = y_sol - haut_total
    mur = _melange(teinte_mur, "encre", nuit)
    p.d.rectangle([x, y_haut, x + larg, y_sol], fill=mur)
    # la corniche, qui donne l'epaisseur du bati
    p.d.rectangle([x - 4, y_haut, x + larg + 4, y_haut + max(5, haut_total // 42)],
                  fill=_melange(teinte_mur, "encre", min(1.0, nuit + 0.14)))

    h_rdc = int(haut_total * 0.38)
    y_rdc = y_sol - h_rdc
    h_bandeau = int(h_rdc * 0.30)

    # les fenetres des etages : eclairees au hasard regulier, pas toutes
    if etages:
        h_zone = haut_total - h_rdc - max(5, haut_total // 42)
        h_f = int(h_zone / etages * 0.52)
        l_f = int(larg * 0.20)
        for e in range(etages):
            yy = y_haut + max(5, haut_total // 42) + int(h_zone / etages * (e + 0.26))
            for i in range(2):
                xx = x + larg * (0.16 + i * 0.46)
                vive = (e + i) % 3 != 1
                p.d.rectangle([xx, yy, xx + l_f, yy + h_f],
                              fill=_melange("jaune", "encre",
                                            0.34 if vive else 0.78))

    # la vitrine du rez-de-chaussee, et sa porte
    y_vit, y_pied = y_rdc + h_bandeau, y_sol - haut_total * 0.018
    p.d.rectangle([x + larg * 0.07, y_vit, x + larg * 0.93, y_pied],
                  fill=_melange("jaune", "encre", 0.30 if allumee else 0.84))
    p.d.line([(x + larg * 0.36, y_vit), (x + larg * 0.36, y_pied)],
             fill=_melange(teinte_mur, "encre", 0.84), width=max(2, larg // 110))
    p.d.rectangle([x + larg * 0.70, y_vit + (y_pied - y_vit) * 0.10,
                   x + larg * 0.88, y_pied],
                  fill=_melange("orange", "encre", 0.40 if allumee else 0.88))
    p.d.line([(x + larg * 0.66, y_vit), (x + larg * 0.66, y_pied)],
             fill=_melange(teinte_mur, "encre", 0.86), width=max(2, larg // 90))
    # le bandeau d'enseigne
    p.d.rectangle([x, y_rdc, x + larg, y_rdc + h_bandeau],
                  fill=_melange(teinte_mur, "encre", min(1.0, nuit + 0.22)))
    _enseigne_lointaine(p, x + larg * 0.14, y_rdc + h_bandeau * 0.22,
                        larg * 0.72, h_bandeau * 0.56, couleur_enseigne,
                        allumee, barres=3 if larg > 150 else 2)
    return (x + larg / 2, y_rdc + h_bandeau * 0.5, larg * 0.5, h_bandeau * 0.9)


def _rue_crepuscule(p, y_haut, y_bas, nuit=0.54):
    """Une rue commercante a la tombee du jour, enseignes allumees.

    C'est l'image que la n° 10 demandait en photo, et celle que la liste
    de prises de vue signalait comme « a photographier en priorite,
    parce qu'elle sert trois fois ». Elle sert trois fois ici aussi,
    sans sortie a 17 h 30.
    """
    y_sol = int(y_bas - (y_bas - y_haut) * 0.14)
    ciel = _degrade_lineaire(p.l, y_sol - y_haut, 180.0,
                             [(0.0, C["bleu"]), (0.42, C["violet"]),
                              (0.78, C["corail"]), (1.0, C["jaune"])])
    p.im.paste(ciel, (0, y_haut))
    p._redessiner()

    # la rue : le trottoir d'en face, la bordure, puis la chaussee. Le
    # reflet des vitrines sur le bitume mouille d'automne n'est pas un
    # effet : sans lui, le bas de l'image est un aplat mort.
    p.d.rectangle([0, y_sol, p.l, y_bas], fill=_melange("taupe", "encre", 0.82))
    h_trot = (y_bas - y_sol) * 0.34
    p.d.rectangle([0, y_sol, p.l, y_sol + h_trot],
                  fill=_melange("taupe", "encre", 0.68))
    p.d.line([(0, y_sol + h_trot), (p.l, y_sol + h_trot)],
             fill=_melange("taupe", "encre", 0.52), width=4)

    # six facades de largeurs et de hauteurs differentes : une rue reguliere
    # ne ressemble a rien, et un centre ancien n'est jamais regulier.
    bati = [(0.00, 0.19, 0.74, "sable", "corail", 2, True, 0.00),
            (0.19, 0.15, 0.90, "sable_fonce", "jaune", 2, True, 0.05),
            (0.34, 0.21, 0.66, "creme_rose", "turquoise", 1, True, -0.05),
            (0.55, 0.13, 0.84, "brun_clair", "violet", 2, False, 0.07),
            (0.68, 0.18, 0.72, "sable", "orange", 1, True, 0.02),
            (0.86, 0.14, 0.95, "sable_fonce", "bleu_vif", 2, True, -0.03)]
    haut_max = (y_sol - y_haut) * 0.92
    lueurs = []
    for gx, gl, gh, mur, coul, et, on, ecart in bati:
        res = _facade_rue(p, int(p.l * gx), y_sol, int(p.l * gl),
                          int(haut_max * gh), mur, on, et, coul,
                          min(0.9, max(0.0, nuit + ecart)))
        if on:
            lueurs.append((res, coul))
    for (cx, cy, rx, ry), coul in lueurs:
        _halo(p, cx, cy, rx * 1.12, ry * 1.9, coul, 74, 20)
    return p


# ---------------------------------------------------------------------
# La vitrine — n° 12, n° 21, n° 22. Dessinee une fois, declinee.
# ---------------------------------------------------------------------
def _flocon(d, cx, cy, r, couleur, ep=3):
    for a in (0, 60, 120):
        import math
        dx, dy = math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r
        d.line([(cx - dx, cy - dy), (cx + dx, cy + dy)],
               fill=teinte(couleur), width=ep)


def _sapin(d, cx, cy, h, couleur):
    for i in range(3):
        l = h * (0.46 - i * 0.11)
        yy = cy - h * 0.5 + i * h * 0.26
        d.polygon([(cx, yy), (cx - l, yy + h * 0.34), (cx + l, yy + h * 0.34)],
                  fill=teinte(couleur))
    d.rectangle([cx - h * 0.06, cy + h * 0.34, cx + h * 0.06, cy + h * 0.46],
                fill=teinte(couleur))


def _citrouille_plate(d, cx, cy, larg, couleur):
    """Une citrouille en silhouette, d'une seule couleur : un motif."""
    h = larg * 0.82
    for dx, l in ((0.0, 1.0), (-0.24, 0.72), (0.24, 0.72)):
        d.ellipse([cx + larg * dx - larg * l / 2, cy - h / 2,
                   cx + larg * dx + larg * l / 2, cy + h / 2], fill=couleur)
    d.rectangle([cx - larg * 0.05, cy - h / 2 - larg * 0.16,
                 cx + larg * 0.05, cy - h / 2 + larg * 0.04], fill=couleur)
    return d


@pose(flou=26, force=72, bas=18, cote=8)
def _vitrine(p, x, y, larg, haut, *, trait=False, eclairee=True,
             fascia=True, couverture=0.0, bandeau=0.0, oeil=False,
             encombre=False, reflet=False, lettres=None, stickers=None,
             echelle=False, decor="flocons", zone_vide=False,
             couleur_decor="violet", opacite_decor=0x9e,
             enseigne=None, sous_enseigne=None):
    """Une devanture en elevation, vue d'en face.

    Une seule fonction pour les trois publications qui demandaient une
    photo de vitrine, parce que c'est la meme vitrine : la n° 12 la
    montre nue puis habillee, la n° 21 la montre de nuit et a hauteur
    des yeux, la n° 22 lui colle deux adhesifs de fetes. Les redessiner
    separement, c'est se garantir trois vitrines differentes dans un
    meme feed.

    Les hauteurs sont en metres via HAUTEUR_DEVANTURE_M : c'est ce qui
    permet de placer la bande des yeux a 1,40-1,70 m sans la deviner.
    """
    p._place(y, "vitrine")
    ep = max(4, int(larg // 52))
    cadre = "brun" if trait else "encre"
    hf = haut * 0.17 if fascia else 0
    hp = haut * 0.055                      # le soubassement
    gy0, gy1 = y + hf, y + haut - hp       # la zone vitree
    gh = gy1 - gy0
    px_par_m = haut / HAUTEUR_DEVANTURE_M

    # -- le vitrage -------------------------------------------------
    if trait:
        p.d.rectangle([x, gy0, x + larg, gy1], fill=teinte("blanc"),
                      outline=teinte(cadre), width=ep)
    else:
        if eclairee:
            interieur = _degrade_lineaire(int(larg), int(gh), 180.0,
                                          [(0.0, C["jaune"]), (0.62, C["orange"]),
                                           (1.0, C["corail"])])
            p.im.paste(Image.blend(interieur,
                                   Image.new("RGB", interieur.size,
                                             _melange("jaune", "creme", 0.55)),
                                   0.52), (int(x), int(gy0)))
            p._redessiner()
        else:
            p.d.rectangle([x, gy0, x + larg, gy1],
                          fill=_melange("encre", "bleu", 0.22))

    # -- ce qu'il y a derriere la vitre -----------------------------
    if encombre and not trait:
        # un rayonnage charge : c'est le fond contre lequel un texte
        # colle sur le verre devra se lire, et il bouge toute la journee.
        for r in range(3):
            yy = gy0 + gh * (0.22 + r * 0.26)
            p.d.rectangle([x + larg * 0.06, yy, x + larg * 0.94, yy + gh * 0.035],
                          fill=_melange("brun", "encre", 0.35))
            for i in range(7):
                bl = larg * (0.07 + (i % 3) * 0.012)
                bx = x + larg * (0.08 + i * 0.122)
                bh = gh * (0.10 + ((i + r) % 4) * 0.022)
                p.d.rectangle([bx, yy - bh, bx + bl, yy],
                              fill=_melange(["corail", "turquoise", "jaune",
                                             "violet", "bleu_vif"][(i + r) % 5],
                                            "encre", 0.40 if eclairee else 0.66))

    if encombre and not trait:
        # Le rayonnage est derrière la vitre ; le lettrage sera dessus.
        # Les flouter pareil, c'est les mettre sur le même plan, et
        # c'est ce qui empêchait la vitre de se lire comme une surface.
        #
        # Ce n'est pas un effet d'appareil photo — visuels.py ne fait
        # pas de photographies, et un dessin ne doit pas prétendre en
        # être une. C'est la règle de dessin la plus ancienne qui soit :
        # ce qui est loin se traite avec moins de netteté que ce qui est
        # près. Deux pixels suffisent à le dire.
        gx0, gx1 = int(x), int(x + larg)
        gy0i, gy1i = int(gy0), int(gy1)
        zone = p.im.crop((gx0, gy0i, gx1, gy1i))
        p.im.paste(zone.filter(ImageFilter.GaussianBlur(2.4)), (gx0, gy0i))
        p._redessiner()

    if reflet and not trait:
        # vitrine eteinte la nuit : le verre renvoie la rue d'en face.
        # C'est exactement ce que la legende decrit, et ca ne se montre
        # qu'en dessinant le reflet — une photo de miroir ne se lit pas.
        for i, (gx, gl, gh2) in enumerate(((0.04, 0.17, 0.42), (0.23, 0.13, 0.56),
                                           (0.38, 0.19, 0.36), (0.60, 0.15, 0.48),
                                           (0.78, 0.18, 0.40))):
            bx, bl = x + larg * gx, larg * gl
            bh = gh * gh2
            p.d.rectangle([bx, gy1 - bh, bx + bl, gy1],
                          fill=_melange("bleu", "encre", 0.58 + (i % 3) * 0.05))
        p.d.ellipse([x + larg * 0.70, gy0 + gh * 0.12,
                     x + larg * 0.78, gy0 + gh * 0.24],
                    fill=_melange("jaune", "encre", 0.52))
        # les trainees de lumiere sur le verre : en transparence, sinon
        # elles rayent le dessin au lieu de le vitrer.
        calque = Image.new("RGBA", p.im.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(calque)
        for i in range(5):
            xx = x + larg * (0.02 + i * 0.21)
            dc.line([(xx, gy1), (xx + larg * 0.22, gy0)],
                    fill=teinte("blanc") + "2a", width=max(4, ep * 2))
            dc.line([(xx + larg * 0.05, gy1), (xx + larg * 0.25, gy0)],
                    fill=teinte("blanc") + "18", width=max(2, ep))
        masque = Image.new("L", p.im.size, 0)
        ImageDraw.Draw(masque).rectangle([x, gy0, x + larg, gy1], fill=255)
        calque.putalpha(Image.composite(calque.split()[3],
                                        Image.new("L", p.im.size, 0), masque))
        p.im = Image.alpha_composite(p.im.convert("RGBA"), calque).convert("RGB")
        p._redessiner()

    # -- le decor de fetes ------------------------------------------
    if couverture > 0 or bandeau > 0:
        if couverture > 0:
            dy0, dy1 = gy0, gy0 + gh * couverture
        else:
            dy0 = gy0 + gh * 0.30
            dy1 = dy0 + gh * bandeau
        # l'adhesif laisse passer la lumiere : un aplat opaque eteindrait
        # la vitrine, et c'est justement ce que la publication reproche
        # aux decors qui couvrent tout.
        calque = Image.new("RGBA", p.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(calque).rectangle([x, dy0, x + larg, dy1],
                                         fill=teinte(couleur_decor)
                                         + ("46" if trait
                                            else "%02x" % opacite_decor))
        p.im = Image.alpha_composite(p.im.convert("RGBA"), calque).convert("RGB")
        p._redessiner()
        n = max(3, int(larg / 110))
        for i in range(n):
            cx = x + larg * (0.5 + (i - (n - 1) / 2) * 0.9 / n)
            cy = (dy0 + dy1) / 2
            if decor == "citrouilles":
                _citrouille_plate(p.d, cx, cy,
                                  min(larg * 0.062, (dy1 - dy0) * 0.58),
                                  teinte("encre"))
            elif decor == "sapins":
                _sapin(p.d, cx, cy, min(gh * 0.22, (dy1 - dy0) * 0.74),
                       couleur_decor)
            else:
                _flocon(p.d, cx, cy, min(larg * 0.045, (dy1 - dy0) * 0.34),
                        couleur_decor, max(3, ep - 1))

    # -- la porte et les meneaux ------------------------------------
    xp = x + larg * 0.72
    p.d.rectangle([xp, gy0 + gh * 0.06, x + larg, gy1],
                  outline=teinte(cadre), width=ep)
    p.d.ellipse([xp + larg * 0.02, gy0 + gh * 0.56,
                 xp + larg * 0.042, gy0 + gh * 0.60], fill=teinte(cadre))
    p.d.line([(x + larg * 0.36, gy0), (x + larg * 0.36, gy1)],
             fill=teinte(cadre), width=ep)
    p.d.line([(xp - ep / 2, gy0), (xp - ep / 2, gy1)],
             fill=teinte(cadre), width=ep)

    # -- la bande des yeux ------------------------------------------
    if oeil:
        y140 = y + haut - 1.40 * px_par_m
        y170 = y + haut - 1.70 * px_par_m
        calque = Image.new("RGBA", p.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(calque).rectangle([x, y170, x + larg, y140],
                                         fill=teinte("corail") + "3c")
        p.im = Image.alpha_composite(p.im.convert("RGBA"), calque).convert("RGB")
        p._redessiner()
        for yy in (y140, y170):
            p.d.line([(x - 18, yy), (x + larg + 18, yy)], fill=teinte("corail"),
                     width=3)

    # -- le lettrage adhesif ----------------------------------------
    if lettres:
        f = police(600, int(px_par_m * 0.17))
        yy = y + haut - 1.66 * px_par_m
        for ligne in lettres.split("\n"):
            l = p.d.textlength(ligne, font=f)
            p.d.text((x + (larg - l) / 2, yy), ligne, font=f,
                     fill=teinte("blanc" if not trait else "encre"))
            yy += int(px_par_m * 0.22)

    # -- les adhesifs promotionnels ---------------------------------
    for st in (stickers or []):
        texte, couleur, (rx, ry), taille = st
        f = police(800, taille)
        l = p.d.textlength(texte, font=f)
        cx, cy = x + larg * rx, gy0 + gh * ry
        p.d.rounded_rectangle([cx - l / 2 - 26, cy - taille * 0.80,
                               cx + l / 2 + 26, cy + taille * 0.80],
                              radius=int(taille * 0.8), fill=teinte(couleur))
        p.d.text((cx - l / 2, cy - taille * 0.62), texte, font=f,
                 fill=teinte("blanc"))

    # -- la zone reservee, vide et cernee ---------------------------
    if zone_vide:
        zx, zy = x + larg * 0.08, gy1 - gh * 0.30
        p.d.rectangle([zx, zy, zx + larg * 0.26, zy + gh * 0.20],
                      outline=teinte("corail"), width=4)

    # -- le cadre, le bandeau d'enseigne, le soubassement -----------
    if fascia:
        p.d.rectangle([x - ep, y, x + larg + ep, y + hf],
                      fill=teinte("blanc") if trait else _melange("encre", "brun", 0.30),
                      outline=teinte(cadre), width=ep if trait else 0)
    p.d.rectangle([x - ep, gy1, x + larg + ep, y + haut],
                  fill=teinte("blanc") if trait else _melange("brun", "encre", 0.45),
                  outline=teinte(cadre) if trait else None,
                  width=ep if trait else 0)
    p.d.rectangle([x - ep, y, x + larg + ep, y + haut], outline=teinte(cadre),
                  width=ep)

    # -- le nom sur le bandeau, et la ligne ajoutee dessous ---------
    if enseigne and fascia:
        fe = police(800, int(hf * 0.46))
        le = p.d.textlength(enseigne, font=fe)
        if le > larg * 0.88:
            fe = police(800, int(hf * 0.46 * larg * 0.88 / le))
            le = p.d.textlength(enseigne, font=fe)
        p.d.text((x + (larg - le) / 2, y + hf * 0.26), enseigne, font=fe,
                 fill=teinte("encre" if trait else "creme"))
    if sous_enseigne:
        # la ligne secondaire va sur un bandeau a elle, pas sur le verre :
        # un texte clair pose sur une vitrine eclairee ne se lit pas, et
        # cette publication-ci se joue entierement sur ce qui se lit.
        bh2 = hf * 0.82
        by2 = y + hf
        p.d.rectangle([x - ep, by2, x + larg + ep, by2 + bh2],
                      fill=teinte("blanc") if trait
                      else _melange("encre", "violet", 0.18))
        fs = police(600, int(bh2 * 0.42))
        ls = p.d.textlength(sous_enseigne, font=fs)
        if ls > larg * 0.92:
            fs = police(600, int(bh2 * 0.42 * larg * 0.92 / ls))
            ls = p.d.textlength(sous_enseigne, font=fs)
        p.d.text((x + (larg - ls) / 2, by2 + bh2 * 0.22), sous_enseigne,
                 font=fs, fill=teinte("encre" if trait else "creme"))
        p.d.rectangle([x - ep, by2, x + larg + ep, by2 + bh2],
                      outline=teinte(cadre), width=ep)

    # -- l'echelle en metres ----------------------------------------
    if echelle:
        xe = x - 44
        p.d.line([(xe, y), (xe, y + haut)], fill=teinte("taupe"), width=3)
        f = police(600, 22)
        for m in range(0, int(HAUTEUR_DEVANTURE_M) + 1):
            yy = y + haut - m * px_par_m
            p.d.line([(xe - 12, yy), (xe + 12, yy)], fill=teinte("taupe"), width=3)
            t = "%d m" % m
            p.d.text((xe - 14 - p.d.textlength(t, font=f), yy - 13), t,
                     font=f, fill=teinte("taupe"))

    # -- la peau du verre, en dernier -------------------------------
    # Pose avant le lettrage, elle le voilerait ; pose apres, elle passe
    # dessus comme un reflet passe sur un adhesif — ce qui est le cas.
    if not trait:
        _reflet_verre(p, (x, gy0, x + larg, gy1),
                      force=38 if eclairee else 58)
    return (x, gy0, x + larg, gy1)


# ---------------------------------------------------------------------
# Les quatre matieres, dessinees en coupe — n° 15.
# ---------------------------------------------------------------------
# Le quiz demandait quatre macrophotographies. La coupe dessinee change
# la nature de l'exercice, et sur trois des quatre matieres elle montre
# plus : l'ame noire d'un alu composite entre ses deux peaux ne se voit
# sur une photo que si la tranche est parfaitement eclairee, alors
# qu'elle est l'information meme. En echange, le gaufrage et le dépoli
# perdent ce que seule la lumiere rasante donne. C'est dit dans la
# legende de la publication : on montre des coupes, pas des photos.

MATIERES = {
    "alu": ("Alu composite", "le panneau extérieur qui ne gondole pas"),
    "plexi": ("Plexiglas", "l'intérieur, les lettres, la plaque professionnelle"),
    "depoli": ("Adhésif dépoli", "la vitrine, et ça se retire"),
    "gaufre": ("Papier gaufré", "la carte qu'on garde"),
}


@pose(flou=14, force=72, bas=10, cote=5)
def _matiere(p, x, y, cote, genre, epaisseur=0.16):
    """Un echantillon vu de trois quarts, sa tranche tournee vers nous.

    L'epaisseur est volontairement exageree : a l'echelle reelle, trois
    millimetres d'alu composite sur un panneau d'un metre ne font pas un
    pixel. Un dessin technique grossit toujours ce qu'il explique.
    """
    p._place(y, "matière")
    e = cote * epaisseur
    biais = e * 0.9
    haut = cote - e

    def face(couleur, decal=0):
        p.d.rectangle([x, y + e + decal, x + cote - biais, y + cote + decal],
                      fill=couleur)

    if genre == "alu":
        face(_melange("sable", "taupe", 0.30))
        # la tranche : peau, ame noire, peau. C'est toute l'information.
        p.d.polygon([(x, y + e), (x + biais, y), (x + cote, y),
                     (x + cote - biais, y + e)],
                    fill=_melange("sable", "blanc", 0.55))
        # la tranche de droite, en trois couches empilees
        for h0, h1, c in ((0.00, 0.22, _melange("blanc", "taupe", 0.26)),
                          (0.22, 0.78, _melange("encre", "brun", 0.10)),
                          (0.78, 1.00, _melange("blanc", "taupe", 0.34))):
            p.d.polygon([(x + cote - biais, y + e + haut * h0),
                         (x + cote, y + haut * h0),
                         (x + cote, y + haut * h1),
                         (x + cote - biais, y + e + haut * h1)], fill=c)
        f = police(600, max(16, int(cote * 0.062)))
        p.d.text((x + cote * 0.08, y + cote * 0.70), "3 mm", font=f,
                 fill=_melange("encre", "sable", 0.35))

    elif genre == "plexi":
        face(_melange("blanc", "turquoise", 0.16))
        p.d.polygon([(x, y + e), (x + biais, y), (x + cote, y),
                     (x + cote - biais, y + e)],
                    fill=_melange("blanc", "turquoise", 0.30))
        # la tranche polie : c'est elle qui conduit la lumiere, et c'est
        # a ca qu'on reconnait le plexi d'un verre ou d'un PVC.
        p.d.polygon([(x + cote - biais, y + e), (x + cote, y),
                     (x + cote, y + haut), (x + cote - biais, y + cote)],
                    fill=teinte("turquoise"))
        _halo(p, x + cote - biais / 2, y + cote * 0.5, biais * 1.4, haut * 0.52,
              "turquoise", 86, 22)
        for i in range(3):
            xx = x + cote * (0.16 + i * 0.22)
            p.d.line([(xx, y + cote), (xx + cote * 0.22, y + e)],
                     fill=_melange("blanc", "turquoise", 0.55),
                     width=max(3, int(cote * 0.016)))

    elif genre == "depoli":
        # la vitre, et derriere elle un rayonnage. En haut le verre est
        # nu, en bas l'adhesif brouille la forme sans eteindre la lumiere.
        sous = Image.new("RGB", (int(cote), int(haut)),
                         _melange("jaune", "creme", 0.62))
        ds = ImageDraw.Draw(sous)
        for i, (gx, gl, gh2, c) in enumerate(((0.08, 0.20, 0.46, "corail"),
                                              (0.34, 0.16, 0.62, "turquoise"),
                                              (0.56, 0.22, 0.38, "violet"),
                                              (0.80, 0.14, 0.54, "orange"))):
            ds.rectangle([cote * gx, haut * (1 - gh2), cote * (gx + gl), haut],
                         fill=_melange(c, "creme", 0.30))
        ds.rectangle([0, haut * 0.70, cote, haut * 0.74],
                     fill=_melange("brun", "creme", 0.40))
        bas = sous.crop((0, int(haut * 0.42), int(cote), int(haut)))
        bas = bas.filter(ImageFilter.GaussianBlur(int(cote * 0.035)))
        bas = Image.blend(bas, Image.new("RGB", bas.size, teinte("blanc")), 0.46)
        sous.paste(bas, (0, int(haut * 0.42)))
        p.im.paste(sous, (int(x), int(y + e)))
        p._redessiner()
        p.d.line([(x, y + e + haut * 0.42), (x + cote, y + e + haut * 0.42)],
                 fill=_melange("blanc", "taupe", 0.25), width=max(3, int(cote * 0.014)))
        p.d.rectangle([x, y + e, x + cote, y + cote],
                      outline=_melange("encre", "brun", 0.30),
                      width=max(3, int(cote * 0.018)))

    elif genre == "gaufre":
        # un gaufrage n'a pas de couleur : il n'a qu'une ombre et une
        # lumiere. On le dessine donc en deux traits decales, comme il
        # se voit en lumiere rasante venant de la gauche.
        p.d.rectangle([x, y + e, x + cote, y + cote], fill=teinte("creme"))
        d = max(3, int(cote * 0.016))
        cx, cy, r = x + cote * 0.50, y + e + cote * 0.44, cote * 0.21
        for decal, c in ((-d, teinte("blanc")),
                         (d, _melange("taupe", "brun", 0.30))):
            p.d.ellipse([cx - r + decal, cy - r + decal,
                         cx + r + decal, cy + r + decal],
                        outline=c, width=max(4, int(cote * 0.026)))
            p.d.line([(cx - r * 0.42 + decal, cy + r * 0.52 + decal),
                      (cx + r * 0.42 + decal, cy + r * 0.52 + decal)],
                     fill=c, width=max(4, int(cote * 0.022)))
        p.d.rectangle([x, y + e, x + cote, y + cote],
                      outline=_melange("taupe", "creme", 0.35),
                      width=max(2, int(cote * 0.010)))
    return p


def _grille_matieres(p, y, genres, cote=None, ecart=28, numeros=True):
    """Les quatre echantillons en grille 2x2, numerotes."""
    cote = cote or (p.l - 2 * MARGE - ecart) // 2
    for i, g in enumerate(genres):
        x = MARGE + (i % 2) * (cote + ecart)
        yy = y + (i // 2) * (cote + ecart)
        _matiere(p, x, yy, cote, g)
        if numeros:
            p.pastille(x + 16, yy + cote - 62, str(i + 1), "corail", taille=28)
    return y + 2 * cote + ecart


# ---------------------------------------------------------------------
# Le calendrier, l'emballage, le formulaire — n° 16, n° 18, n° 10 et 22.
# ---------------------------------------------------------------------
def _bande_jours(p, x, y, larg, debut, fin, jalons=None, haut_case=None):
    """Les jours du 14 novembre au 24 decembre, en une seule grille.

    Le plan du reel demandait un doigt qui remonte les cases d'un
    calendrier. Dessine, le geste devient meilleur : on voit les six
    semaines d'un coup, le 24 decembre au bout, et les trois jalons
    poses dessus. Un calendrier filme ne montre qu'un mois a la fois.
    """
    import datetime
    jalons = jalons or {}
    cote = larg / 7.0
    haut_case = haut_case or cote * 0.84
    # on part du lundi de la semaine du debut, sinon la grille ment
    depart = debut - datetime.timedelta(days=debut.weekday())
    f = police(600, int(cote * 0.30))
    fm = police(800, int(cote * 0.19))
    jour = depart
    ligne = 0
    while jour <= fin:
        col = jour.weekday()
        cx = x + col * cote
        cy = y + ligne * haut_case
        dans = debut <= jour <= fin
        marque = jalons.get(jour)
        if marque:
            coul, _ = marque
            p.d.rounded_rectangle([cx + 3, cy + 3, cx + cote - 3, cy + haut_case - 3],
                                  radius=int(cote * 0.14), fill=teinte(coul))
            enc = "blanc"
        elif dans:
            p.d.rounded_rectangle([cx + 3, cy + 3, cx + cote - 3, cy + haut_case - 3],
                                  radius=int(cote * 0.14),
                                  fill=_melange("blanc", "sable", 0.35))
            enc = "brun"
        else:
            p.d.rounded_rectangle([cx + 3, cy + 3, cx + cote - 3, cy + haut_case - 3],
                                  radius=int(cote * 0.14),
                                  outline=_melange("sable", "taupe", 0.40), width=2)
            enc = "sable_fonce"
        t = str(jour.day)
        p.d.text((cx + cote / 2 - p.d.textlength(t, font=f) / 2,
                  cy + haut_case * 0.26), t, font=f, fill=teinte(enc))
        if jour.day == 1 or jour == depart:
            m = ["JANV", "FÉVR", "MARS", "AVR", "MAI", "JUIN", "JUIL",
                 "AOÛT", "SEPT", "OCT", "NOV", "DÉC"][jour.month - 1]
            p.d.text((cx + cote / 2 - p.d.textlength(m, font=fm) / 2,
                      cy + haut_case * 0.70), m, font=fm,
                     fill=teinte("taupe" if not marque else "blanc"))
        jour += datetime.timedelta(days=1)
        if jour.weekday() == 0:
            ligne += 1
    return y + (ligne + 1) * haut_case


@pose(flou=20, force=76, bas=14, cote=6)
def _sachet(p, cx, y, larg, haut, trait=False, zone=False, bandeau=True,
            logo=True, couleur="violet"):
    """Un sachet cadeau en elevation, avec ou sans sa zone reservee.

    La n° 18 demandait deux images du meme sachet : soigne, puis au
    trait avec un rectangle vide au dos. Dessiner les deux garantit que
    c'est bien le meme sachet — photographie, il ne l'aurait jamais ete.
    """
    p._place(y, "sachet")
    x0, x1 = cx - larg / 2, cx + larg / 2
    ep = max(3, int(larg * 0.016))
    corps = teinte("blanc") if trait else _melange("sable", "creme", 0.45)
    p.d.rectangle([x0, y, x1, y + haut], fill=corps,
                  outline=teinte("brun" if trait else "taupe"), width=ep)
    # le soufflet de cote et le pli du haut : deux traits, et le
    # rectangle devient un sac. Sans eux, c'est une boite.
    p.d.line([(x0 + larg * 0.17, y), (x0 + larg * 0.17, y + haut)],
             fill=_melange("taupe", "creme", 0.45 if not trait else 0.0)
             if not trait else teinte("brun"), width=max(2, ep - 1))
    p.d.line([(x0, y + haut * 0.12), (x1, y + haut * 0.12)],
             fill=teinte("brun") if trait else _melange("taupe", "creme", 0.30),
             width=max(2, ep - 1))
    # les deux anses
    for s in (-1, 1):
        ax = cx + s * larg * 0.22
        p.d.arc([ax - larg * 0.11, y - haut * 0.16, ax + larg * 0.11, y + haut * 0.12],
                180, 360, fill=teinte("brun" if trait else "taupe"), width=ep + 1)
    if bandeau:
        by = y + haut * 0.40
        bh = haut * 0.20
        if trait:
            p.d.rectangle([x0, by, x1, by + bh],
                          fill=_melange(couleur, "blanc", 0.86))
        else:
            p.d.rectangle([x0, by, x1, by + bh], fill=teinte(couleur))
        if not trait:
            for i in range(5):
                _flocon(p.d, x0 + larg * (0.12 + i * 0.19), by + bh / 2,
                        larg * 0.035, "blanc", max(2, ep - 1))
    if logo:
        r = larg * 0.085
        ly = y + haut * 0.74
        p.d.ellipse([cx - r, ly - r, cx + r, ly + r],
                    fill=teinte("blanc") if trait else teinte("corail"),
                    outline=teinte("brun") if trait else None,
                    width=ep if trait else 0)
        if not trait:
            p.d.ellipse([cx - r * 0.52, ly - r * 0.52, cx + r * 0.52, ly + r * 0.52],
                        fill=teinte("creme"))
    if zone:
        zl, zh = larg * 0.34, haut * 0.15
        zx, zy = x1 - zl - larg * 0.09, y + haut - zh - haut * 0.09
        p.d.rectangle([zx, zy, zx + zl, zy + zh], outline=teinte("corail"),
                      width=max(4, ep + 1))
        f = police(600, max(15, int(larg * 0.048)))
        lib = "cette place"
        p.d.text((zx + zl / 2 - p.d.textlength(lib, font=f) / 2, zy + zh + 10),
                 lib, font=f, fill=teinte("corail"))
    return p


@pose(flou=16, force=70, bas=11, cote=5)
def _feuille_formulaire(p, cx, y, larg, haut, numero, titre, lignes=5):
    """Une feuille de formulaire, SCHEMATISEE et dite comme telle.

    La publication demandait « une capture du haut du Cerfa ». On ne
    reproduit pas un document administratif : ni emblème, ni mise en
    page officielle, rien qui puisse circuler comme s'il s'agissait du
    vrai. Ce qui compte est le numero, et il est exact — c'est
    justement le sujet de la publication. La feuille dessinee le porte,
    et porte aussi la mention qui dit ce qu'elle est.
    """
    p._place(y, "formulaire")
    x0 = cx - larg / 2
    p.d.rectangle([x0 + 10, y + 12, x0 + larg + 10, y + haut + 12],
                  fill=_melange("taupe", "creme", 0.55))
    p.d.rectangle([x0, y, x0 + larg, y + haut], fill=teinte("blanc"),
                  outline=teinte("taupe"), width=3)
    p.d.rectangle([x0, y, x0 + larg, y + haut * 0.20],
                  fill=_melange("bleu", "blanc", 0.86))
    f = police(800, int(larg * 0.075))
    p.d.text((x0 + larg * 0.07, y + haut * 0.055), numero, font=f,
             fill=teinte("bleu"))
    ft = police(600, int(larg * 0.047))
    yy = y + haut * 0.26
    for ligne in couper(titre, ft, larg * 0.86):
        p.d.text((x0 + larg * 0.07, yy), ligne, font=ft, fill=teinte("encre"))
        yy += int(larg * 0.047 * 1.3)
    yy += haut * 0.03
    for i in range(lignes):
        p.d.rectangle([x0 + larg * 0.07, yy, x0 + larg * 0.14, yy + larg * 0.042],
                      outline=teinte("taupe"), width=2)
        p.d.line([(x0 + larg * 0.18, yy + larg * 0.034),
                  (x0 + larg * (0.93 - (i % 3) * 0.12), yy + larg * 0.034)],
                 fill=_melange("taupe", "blanc", 0.45), width=3)
        yy += larg * 0.075
    f2 = police(400, max(15, int(larg * 0.040)))
    p.d.text((x0 + larg * 0.07, y + haut - larg * 0.075), "schéma", font=f2,
             fill=teinte("taupe"))
    return p


def _horloge(p, cx, cy, r, couleur="corail", heure=17, minute=0):
    p.d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=teinte(couleur),
                width=max(4, int(r * 0.10)))
    import math
    for n in range(12):
        a = math.radians(n * 30 - 90)
        p.d.line([(cx + math.cos(a) * r * 0.82, cy + math.sin(a) * r * 0.82),
                  (cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92)],
                 fill=teinte(couleur), width=max(2, int(r * 0.05)))
    ah = math.radians((heure % 12) * 30 + minute * 0.5 - 90)
    am = math.radians(minute * 6 - 90)
    p.d.line([(cx, cy), (cx + math.cos(ah) * r * 0.48, cy + math.sin(ah) * r * 0.48)],
             fill=teinte(couleur), width=max(4, int(r * 0.09)))
    p.d.line([(cx, cy), (cx + math.cos(am) * r * 0.74, cy + math.sin(am) * r * 0.74)],
             fill=teinte(couleur), width=max(3, int(r * 0.06)))
    return p


# ---------------------------------------------------------------------
# Les trois demonstrations — n° 12 et n° 21.
# ---------------------------------------------------------------------
@pose(flou=18, force=66, bas=12, cote=5)
def _microperfore(p, x, y, larg, haut):
    """Le microperfore, vu des deux cotes dans la meme image.

    C'est le plan que le reel demandait de filmer en passant la camera
    de l'exterieur a l'interieur. Un dessin coupe en deux le montre
    mieux qu'un mouvement de camera, parce que les deux etats sont
    visibles en meme temps — et c'est la comparaison qui explique, pas
    le mouvement.
    """
    mi = x + larg / 2
    # a gauche, vu de la rue : une image pleine
    aff = _degrade_lineaire(int(larg / 2), int(haut), 150.0,
                            [(0.0, C["violet"]), (0.5, C["magenta"]),
                             (1.0, C["corail"])])
    p.im.paste(aff, (int(x), int(y)))
    p._redessiner()
    f = police(800, int(haut * 0.10))
    t = "SOLDES"
    p.d.text((x + larg / 4 - p.d.textlength(t, font=f) / 2, y + haut * 0.42),
             t, font=f, fill=teinte("blanc"))

    # a droite, vu de l'interieur : la rue, a travers les perforations
    p.d.rectangle([mi, y, x + larg, y + haut],
                  fill=_melange("bleu", "creme", 0.76))
    for i, (gx, gl, gh) in enumerate(((0.04, 0.16, 0.44), (0.24, 0.13, 0.60),
                                      (0.40, 0.18, 0.38), (0.62, 0.14, 0.52),
                                      (0.80, 0.16, 0.42))):
        p.d.rectangle([mi + larg / 2 * gx, y + haut * (1 - gh),
                       mi + larg / 2 * (gx + gl), y + haut],
                      fill=_melange("taupe", "creme", 0.45 + (i % 3) * 0.08))
    # la trame : des points d'encre, et du jour entre eux
    pas = max(7, int(haut * 0.034))
    r = pas * 0.21
    for yy in range(int(y + r), int(y + haut - r), pas):
        for xx in range(int(mi + r), int(x + larg - r), pas):
            p.d.ellipse([xx - r, yy - r, xx + r, yy + r],
                        fill=_melange("violet", "magenta", 0.4))

    p.d.line([(mi, y), (mi, y + haut)], fill=teinte("blanc"), width=6)
    p.d.rectangle([x, y, x + larg, y + haut], outline=teinte("encre"), width=5)
    fl = police(600, max(20, int(haut * 0.062)))
    for cx, lib in ((x + larg / 4, "de la rue"),
                    (mi + larg / 4, "de l'intérieur")):
        l = p.d.textlength(lib, font=fl)
        p.d.rounded_rectangle([cx - l / 2 - 16, y + haut + 14,
                               cx + l / 2 + 16, y + haut + 14 + haut * 0.10],
                              radius=14, fill=teinte("encre"))
        p.d.text((cx - l / 2, y + haut + 18), lib, font=fl, fill=teinte("creme"))
    return y + haut + 20 + haut * 0.10


@pose(flou=18, force=66, bas=12, cote=5)
def _depoli(p, x, y, larg, haut):
    """Le depoli : on cache le bas, la lumiere passe quand meme."""
    sous = Image.new("RGB", (int(larg), int(haut)),
                     _melange("jaune", "creme", 0.55))
    ds = ImageDraw.Draw(sous)
    # les formes traversent la ligne de depoli : c'est le meme objet
    # qu'on voit net en haut et brouille en bas. Sans ce recouvrement,
    # la demonstration ne demontre rien.
    for gx, gl, gh, c in ((0.06, 0.18, 0.74, "corail"), (0.30, 0.14, 0.88, "turquoise"),
                          (0.50, 0.20, 0.66, "violet"), (0.76, 0.16, 0.80, "orange")):
        ds.rectangle([larg * gx, haut * (1 - gh), larg * (gx + gl), haut],
                     fill=_melange(c, "creme", 0.22))
    ds.rectangle([0, haut * 0.32, larg, haut * 0.36],
                 fill=_melange("brun", "creme", 0.35))
    bas = sous.crop((0, int(haut * 0.46), int(larg), int(haut)))
    bas = bas.filter(ImageFilter.GaussianBlur(int(larg * 0.022)))
    bas = Image.blend(bas, Image.new("RGB", bas.size, teinte("blanc")), 0.50)
    sous.paste(bas, (0, int(haut * 0.46)))
    p.im.paste(sous, (int(x), int(y)))
    p._redessiner()
    p.d.line([(x, y + haut * 0.46), (x + larg, y + haut * 0.46)],
             fill=teinte("blanc"), width=5)
    p.d.rectangle([x, y, x + larg, y + haut], outline=teinte("encre"), width=5)
    f = police(600, max(18, int(haut * 0.058)))
    p.d.text((x + 22, y + haut * 0.46 - int(haut * 0.058) - 16),
             "verre nu", font=f, fill=teinte("encre"))
    p.d.text((x + 22, y + haut * 0.46 + 16), "dépoli", font=f,
             fill=teinte("encre"))
    return p


@pose(flou=18, force=66, bas=12, cote=5)
def _lettres_sur_verre(p, x, y, larg, haut):
    """Lettres decoupees contre pave blanc : la comparaison du reel."""
    demi = larg / 2 - 14
    for i, plein in enumerate((True, False)):
        xx = x + i * (demi + 28)
        fond = Image.new("RGB", (int(demi), int(haut)),
                         _melange("jaune", "creme", 0.48))
        df = ImageDraw.Draw(fond)
        for gx, gl, gh, c in ((0.08, 0.22, 0.42, "turquoise"),
                              (0.40, 0.18, 0.56, "corail"),
                              (0.66, 0.24, 0.38, "violet")):
            df.rectangle([demi * gx, haut * (1 - gh), demi * (gx + gl), haut],
                         fill=_melange(c, "creme", 0.30))
        p.im.paste(fond, (int(xx), int(y)))
        p._redessiner()
        f = police(800, int(haut * 0.11))
        lignes = ["MAISON", "BERNAT"]
        if plein:
            lh = len(lignes) * int(haut * 0.135) + 26
            p.d.rectangle([xx + demi * 0.08, y + haut * 0.30,
                           xx + demi * 0.92, y + haut * 0.30 + lh],
                          fill=teinte("blanc"))
        yy = y + haut * 0.30 + 14
        for ligne in lignes:
            l = p.d.textlength(ligne, font=f)
            p.d.text((xx + demi / 2 - l / 2, yy), ligne, font=f,
                     fill=teinte("encre"))
            yy += int(haut * 0.135)
        p.d.rectangle([xx, y, xx + demi, y + haut], outline=teinte("encre"),
                      width=5)
        fl = police(600, max(18, int(haut * 0.055)))
        lib = "pavé blanc" if plein else "lettres découpées"
        p.d.text((xx + demi / 2 - p.d.textlength(lib, font=fl) / 2,
                  y + haut + 16), lib, font=fl, fill=teinte("brun"))
    return p


def _trois_distances(p, y, echelles=((2, 0.44), (8, 0.27), (25, 0.15))):
    """La meme vitrine a trois distances — la demonstration de la n° 21.

    Aucune photographie ne fait cela en une image : il faudrait trois
    prises de vue au meme instant, au meme endroit, a trois reculs
    differents. Dessinee, la devanture est rigoureusement la meme et
    seule l'echelle change — c'est ce qui rend la demonstration
    honnete. Les trois sont alignees sur le sol, comme elles le sont
    dans la rue : alignees sur leur milieu, elles flotteraient.
    """
    utile = p.l - 2 * MARGE
    largeurs = [utile * e for _, e in echelles]
    ecart = (utile - sum(largeurs)) / (len(largeurs) - 1)
    y_sol = y + largeurs[0] * 0.58
    x = MARGE
    f = police(600, 30)
    # La perspective atmosphérique, et pas un flou d'objectif. Ce qui
    # est loin perd du contraste avant de perdre de la netteté : c'est
    # vrai dans une rue, et c'est la convention de dessin qui le dit
    # depuis toujours. On fond donc chaque devanture vers le fond de la
    # planche, d'autant plus qu'elle est loin. Le trait reste net — un
    # dessin flouté prétendrait être une photographie, et visuels.py
    # n'en fait pas.
    recul = {0: 0.0, 1: 0.20, 2: 0.42}
    for i, ((m, _), larg) in enumerate(zip(echelles, largeurs)):
        haut = larg * 0.58
        avant = p.im.copy()
        _vitrine(p, x, y_sol - haut, larg, haut, trait=True,
                 lettres="MAISON BERNAT\n9 h – 19 h")
        if recul.get(i):
            p.im = Image.blend(p.im.convert("RGB"), avant.convert("RGB"),
                               recul[i])
            p._redessiner()
        t = "%d m" % m
        p.d.text((x + larg / 2 - p.d.textlength(t, font=f) / 2, y_sol + 26),
                 t, font=f, fill=teinte("corail"))
        x += larg + ecart
    return y_sol + 26 + 40


@pose(flou=18, force=80, bas=12, cote=6)
def _carte(p, cx, cy, larg, haut, angle=0.0, fond="creme", gaufre=False,
           texte=None, ombre=20):
    """Une carte imprimee posee a plat, legerement tournee.

    Planche.poser() fait cela a partir d'un fichier ; ici il n'y a pas
    de fichier, la carte est dessinee. Meme principe : l'ombre est la
    silhouette tournee de l'objet, pas un rectangle flou pose dessous.
    """
    l, h = int(larg), int(haut)
    im = Image.new("RGBA", (l, h), teinte(fond) + "ff")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, l - 1, h - 1], outline=_melange("taupe", "creme", 0.45),
                width=2)
    if gaufre:
        # le gaufrage : deux traits decales, lumiere venant de la gauche
        dd = max(2, int(l * 0.012))
        r = l * 0.17
        ccx, ccy = l / 2, h * 0.40
        for decal, c in ((-dd, teinte("blanc")),
                         (dd, _melange("taupe", "brun", 0.35))):
            d.ellipse([ccx - r + decal, ccy - r + decal,
                       ccx + r + decal, ccy + r + decal], outline=c,
                      width=max(3, int(l * 0.022)))
    if texte:
        ft = manuscrite(int(h * 0.15))
        lt = d.textlength(texte, font=ft)
        d.text((l / 2 - lt / 2, h * 0.68), texte, font=ft, fill=teinte("brun"))
    if ombre:
        sil = Image.new("RGBA", im.size, (0, 0, 0, 80))
        sil = sil.rotate(angle, expand=True, resample=Image.BICUBIC)
        marge = ombre * 3
        fo = Image.new("RGBA", (sil.width + 2 * marge, sil.height + 2 * marge),
                       (0, 0, 0, 0))
        fo.paste(sil, (marge, marge))
        fo = fo.filter(ImageFilter.GaussianBlur(ombre))
        p.im.paste(fo, (int(cx - fo.width / 2), int(cy - fo.height / 2 + ombre / 2)), fo)
    tourne = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    p.im.paste(tourne, (int(cx - tourne.width / 2), int(cy - tourne.height / 2)),
               tourne)
    p._redessiner()
    return p


@pose(flou=20, force=78, bas=14, cote=7)
def _emballage_kraft(p, cx, cy, larg, haut, bandeau=True, pastille=True):
    """Un paquet en papier kraft, son bandeau imprime et sa pastille."""
    x0, y0 = cx - larg / 2, cy - haut / 2
    e = haut * 0.14
    # la face du dessus, en biais : sans elle, un paquet est un rectangle
    p.d.polygon([(x0, y0 + e), (x0 + larg * 0.14, y0),
                 (x0 + larg, y0), (x0 + larg - larg * 0.14, y0 + e)],
                fill=_melange("sable_fonce", "orange", 0.08))
    p.d.rectangle([x0, y0 + e, x0 + larg - larg * 0.14, y0 + haut],
                  fill=_melange("sable_fonce", "orange", 0.22))
    p.d.polygon([(x0 + larg - larg * 0.14, y0 + e), (x0 + larg, y0),
                 (x0 + larg, y0 + haut - e),
                 (x0 + larg - larg * 0.14, y0 + haut)],
                fill=_melange("sable_fonce", "brun", 0.26))
    larg = larg - larg * 0.14
    haut = haut - e
    y0 = y0 + e
    # les plis du papier, qui font la difference entre un paquet et un carre
    for gx in (0.30, 0.68):
        p.d.line([(x0 + larg * gx, y0), (x0 + larg * gx, y0 + haut)],
                 fill=_melange("sable_fonce", "brun", 0.30), width=3)
    if bandeau:
        by, bh = y0 + haut * 0.44, haut * 0.22
        p.d.rectangle([x0 - 6, by, x0 + larg + 6, by + bh], fill=teinte("violet"))
        for i in range(4):
            _flocon(p.d, x0 + larg * (0.16 + i * 0.23), by + bh / 2,
                    larg * 0.042, "blanc", 4)
    if pastille:
        r = larg * 0.10
        p.d.ellipse([cx + larg * 0.26 - r, y0 + haut * 0.80 - r,
                     cx + larg * 0.26 + r, y0 + haut * 0.80 + r],
                    fill=teinte("corail"))
        p.d.ellipse([cx + larg * 0.26 - r * 0.5, y0 + haut * 0.80 - r * 0.5,
                     cx + larg * 0.26 + r * 0.5, y0 + haut * 0.80 + r * 0.5],
                    fill=teinte("creme"))
    return p


def _fond_du_texte(p, x, y, larg, haut):
    """Le meme texte sur verre, devant deux fonds — n° 21, S5.

    A gauche un rayonnage charge, a droite un panneau uni. Le texte est
    rigoureusement identique : c'est le fond qui le rend lisible ou non,
    et c'est ce que la legende affirme.
    """
    demi = larg / 2 - 16
    for i, encombre in enumerate((True, False)):
        xx = x + i * (demi + 32)
        sous = Image.new("RGB", (int(demi), int(haut)),
                         _melange("jaune", "creme", 0.50))
        ds = ImageDraw.Draw(sous)
        if encombre:
            for r in range(3):
                yy = haut * (0.26 + r * 0.26)
                ds.rectangle([0, yy, demi, yy + haut * 0.022],
                             fill=_melange("brun", "creme", 0.30))
                for k in range(5):
                    bl = demi * (0.11 + (k % 3) * 0.02)
                    bx = demi * (0.04 + k * 0.19)
                    bh = haut * (0.13 + ((k + r) % 4) * 0.03)
                    ds.rectangle([bx, yy - bh, bx + bl, yy],
                                 fill=_melange(["corail", "turquoise", "jaune",
                                                "violet", "orange"][(k + r) % 5],
                                               "creme", 0.18))
        else:
            ds.rectangle([0, 0, demi, haut], fill=_melange("encre", "brun", 0.22))
        # Le rayonnage est DERRIÈRE la vitre, les lettres seront DESSUS.
        # Les traiter avec la même netteté, c'est les mettre sur le même
        # plan — et toute la démonstration de cette planche tient sur le
        # fait qu'ils n'y sont pas. Deux pixels de flou suffisent à le
        # dire, et le panneau uni d'en face n'en reçoit pas : il est à
        # la même distance, mais il n'a rien à perdre.
        if encombre:
            sous = sous.filter(ImageFilter.GaussianBlur(demi * 0.009))
        p.im.paste(sous, (int(xx), int(y)))
        p._redessiner()
        f = police(800, int(haut * 0.11))
        for k, ligne in enumerate(("OUVERT", "le dimanche")):
            fk = f if k == 0 else police(600, int(haut * 0.072))
            l = p.d.textlength(ligne, font=fk)
            p.d.text((xx + demi / 2 - l / 2, y + haut * (0.34 + k * 0.15)),
                     ligne, font=fk, fill=teinte("blanc"))
        p.d.rectangle([xx, y, xx + demi, y + haut], outline=teinte("encre"),
                      width=5)
        fl = police(600, max(18, int(haut * 0.058)))
        lib = "devant le rayonnage" if encombre else "devant un panneau uni"
        # le reflet se pose APRÈS le lettrage : un reflet passe sur un
        # adhésif, il ne passe pas dessous. Faible, et seulement sur le
        # panneau encombré — l'autre est un panneau plein, pas du verre.
        if encombre:
            _reflet_verre(p, (xx, y, xx + demi, y + haut), force=34,
                          largeur=0.24, angle=-20)
        p.d.text((xx + demi / 2 - p.d.textlength(lib, font=fl) / 2,
                  y + haut + 16), lib, font=fl, fill=teinte("brun"))
    return y + haut + 16 + 40


def _trottoir_den_face(p, y_haut, y_bas):
    """La vitrine vue depuis le trottoir d'en face, de nuit — n° 21, S1.

    Ce n'est pas la meme image que la rue du crepuscule : ici une seule
    devanture, vue de face, avec la chaussee au premier plan. C'est le
    point de vue que la publication reclame — celui du passant, pas
    celui du commercant qui recule de deux metres dans sa boutique.
    """
    H = y_bas - y_haut
    ciel = _degrade_lineaire(p.l, int(H * 0.44), 180.0,
                             [(0.0, C["encre"]), (0.6, C["bleu"]),
                              (1.0, C["violet"])])
    p.im.paste(ciel, (0, y_haut))
    p._redessiner()
    y_sol = y_haut + H * 0.74
    p.d.rectangle([0, y_haut + H * 0.44, p.l, y_sol],
                  fill=_melange("taupe", "encre", 0.74))
    larg = p.l * 0.78
    haut = larg * 0.52
    _vitrine(p, (p.l - larg) / 2, y_sol - haut, larg, haut, eclairee=True,
             enseigne="MAISON BERNAT", couverture=0.0)
    _halo(p, p.l / 2, y_sol - haut * 0.45, larg * 0.58, haut * 0.62,
          "jaune", 58, 48)
    # la chaussee, et la bordure du trottoir d'ou l'on regarde
    p.d.rectangle([0, y_sol, p.l, y_bas], fill=_melange("taupe", "encre", 0.86))
    p.d.line([(0, y_sol), (p.l, y_sol)], fill=_melange("taupe", "encre", 0.56),
             width=5)
    p.d.rectangle([0, y_bas - (y_bas - y_sol) * 0.22, p.l, y_bas],
                  fill=_melange("taupe", "encre", 0.68))
    for i in range(5):
        xx = p.l * (0.05 + i * 0.21)
        p.d.rectangle([xx, y_sol + (y_bas - y_sol) * 0.34,
                       xx + p.l * 0.11, y_sol + (y_bas - y_sol) * 0.42],
                      fill=_melange("blanc", "taupe", 0.45))
    # le reflet de la vitrine sur la chaussee : c'est lui qui dit que la
    # scene est de nuit, et que la lumiere vient de la boutique.
    _halo(p, p.l / 2, y_sol + (y_bas - y_sol) * 0.30, larg * 0.40,
          (y_bas - y_sol) * 0.34, "jaune", 40, 40)
    return p


# =====================================================================
# LES HUIT PUBLICATIONS REDESSINEES
# =====================================================================
def pub10_enseigne_hiver(dossier=None):
    """n° 10, mardi 3 novembre — l'enseigne quand la nuit tombe a 17 h.

    La S1 demandait une photo de rue commercante au crepuscule, cadree
    « sans qu'aucune enseigne ne soit identifiable » — contrainte que le
    dessin satisfait par construction. La S5 demandait une capture du
    Cerfa : on dessine un schema de formulaire, on ne reproduit pas un
    document administratif.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-10-27-enseigne-hiver"))
    accent("violet")
    faits = []

    p = Planche("sable_chaud")
    _rue_crepuscule(p, 0, 880)
    _bandeau_travers(p, "Depuis dimanche, votre enseigne s'allume une "
                        "heure plus tôt.", "violet", y=170, taille=54)
    p.y = 960
    p.texte("Le changement d'heure a rallongé d'une heure par jour le "
            "moment où elle travaille toute seule.", 36, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("creme")
    p.surtitre("Enseigne", y=150)
    p.chiffre("17 h", 230, "bleu", y=260)
    p.y = 580
    p.texte("C'est l'heure à laquelle votre devanture devient votre seul "
            "support de communication.\n\nJusqu'en mars.", 46, "encre", 600,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "02.png"))

    p = Planche("blanc")
    p.titre("Trois questions,\ndans cet ordre.", 78, y=160)
    p.puces(["Elle est lisible, ou elle ne sert à rien.",
             "Elle est éclairée, ou elle n'existe pas.",
             "Elle est autorisée, ou elle se démonte."],
            "corail", 42, "brun", numerote=True, y=520, interligne=1.7)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("creme")
    p.titre("Éclairer une enseigne,\nc'est la modifier.", 76, y=170)
    p.y = 520
    p.encadre("Passer d'un panneau peint à un caisson lumineux "
              "nécessiterait une nouvelle autorisation. À vérifier auprès "
              "de votre mairie.", 40, "creme_rose", "violet", pad=36)
    p.y += 40
    p.texte("Le conditionnel est volontaire : ce point n'est pas vérifié à "
            "la source, et je préfère vous le dire.", 32, "taupe", 400)
    p.signature("brun")
    faits.append(p.ecrire(d / "04.png"))

    p = Planche("blanc")
    p.titre("Une autorisation,\npas une déclaration.", 72, y=140)
    _feuille_formulaire(p, p.l / 2, 480, 520, 560, "Cerfa n° 16308*01",
                        "Autorisation préalable — enseigne, en mairie",
                        lignes=6)
    p.y = 1090
    p.texte("Une déclaration, on la dépose. Une autorisation, on l'attend.",
            36, "brun", 600, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "05.png"))

    p = Planche("sable_chaud")
    _horloge(p, p.l / 2, 420, 170, "corail", 21, 30)
    p.y = 660
    p.filet()
    p.texte("Les enseignes lumineuses seraient soumises à des plages "
            "d'extinction nocturne, et le Règlement Local de Publicité de "
            "votre commune peut les durcir.\n\nPerpignan a son RLP ; le "
            "centre ancien est en secteur protégé.", 38, "brun", 400,
            avant=10)
    p.signature("brun")
    faits.append(p.ecrire(d / "06.png"))

    p = Planche("violet")
    p.filet(y=300)
    p.titre("Votre rue\nen commentaire.", 86, "blanc")
    p.y += 30
    p.texte("Je vous dis quelles pièces réunir avant de commander quoi que "
            "ce soit.", 40, "creme", 400, avant=20)
    p.fleche("corail", y=1060)
    p.signature("creme")
    faits.append(p.ecrire(d / "07.png"))
    return faits


def pub12_reel_vitrophanie(dossier=None):
    """n° 12, vendredi 6 novembre — les trois familles d'adhesifs.

    Le decoupage demandait quatre plans tournes au telephone et proposait,
    en secours, un prompt d'image generee pour le plan d'ouverture. Les
    deux sont ecartes : le tournage parce qu'il ne se fera pas, le prompt
    parce que LIGNE-EDITORIALE.md l'interdit et qu'une vitrine inventee
    sur le compte d'une graphiste de vitrophanie est exactement le genre
    d'image qui se retourne contre elle.

    Ce sont donc cinq ECRANS FINIS, pas des fiches de tournage : le reel
    se monte en les enchainant avec la voix off, sans rien filmer. Les
    deux demonstrations centrales — le microperfore vu des deux cotes,
    les lettres decoupees contre le pave blanc — montrent d'ailleurs plus
    que le plan qu'elles remplacent, parce qu'elles mettent les deux
    etats dans la meme image au lieu de les separer par un mouvement de
    camera.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-13-reel-vitrophanie"))
    accent("turquoise")
    faits = []

    p = Planche("sable_chaud", LARGE_S, HAUT_S)
    p.surtitre("Reel · 0-3 s", "taupe", y=200)
    p.filet()
    p.titre("Vous avez un panneau\nde 6 m².\nIl est vide.", 94, y=300)
    _vitrine(p, 120, 900, 840, 480, trait=True, enseigne="VOTRE NOM")
    f = police(600, 34)
    p.d.text((120, 1430), "6 m² de verre, et rien dessus", font=f,
             fill=teinte("corail"))
    # la cote, dessinee comme sur un plan
    p.d.line([(120, 1500), (960, 1500)], fill=teinte("corail"), width=4)
    for xx in (120, 960):
        p.d.line([(xx, 1482), (xx, 1518)], fill=teinte("corail"), width=4)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran1.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("3-8 s", "taupe", y=200)
    p.titre("Dépoli :\non cache, on garde\nla lumière.", 76, y=280)
    _depoli(p, 90, 700, 900, 620)
    p.y = 1430
    p.texte("Il masque le bas de la vitrine — les cartons, le dos des "
            "présentoirs — sans assombrir la boutique.", 42, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran2.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("8-13 s", "taupe", y=200)
    p.titre("Microperforé :\nplein dehors,\ntransparent dedans.", 66, y=280)
    _microperfore(p, 90, 760, 900, 560)
    p.y = 1480
    p.texte("Des milliers de trous d'un millimètre. Une image pleine vue de "
            "la rue, la rue vue de l'intérieur.", 42, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran3.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("13-18 s", "taupe", y=200)
    p.titre("Lettres découpées :\nsobre, et ça dure.", 70, y=280)
    _lettres_sur_verre(p, 90, 740, 900, 560)
    p.y = 1420
    p.texte("Pas de rectangle blanc qui jaunit autour du texte. C'est ce "
            "qui vieillit le mieux.", 42, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran4.png"))

    p = Planche("encre", LARGE_S, HAUT_S)
    _vitrine(p, 120, 420, 840, 480, eclairee=True, enseigne="VOTRE NOM",
             bandeau=0.26, couleur_decor="violet")
    p.y = 1060
    p.filet()
    p.titre("Et ça se décolle.", 92, "blanc")
    p.y += 30
    p.texte("Un adhésif de vitrine n'est pas une enseigne. Vous changez "
            "d'avis au printemps, la vitre est intacte.", 40, "creme", 400,
            avant=20)
    p.abonnement("sable")
    p.signature("sable")
    faits.append(p.ecrire(d / "ecran5.png"))
    return faits


def pub14_francais_devanture(dossier=None):
    """n° 14, mardi 10 novembre — le slogan en anglais sur la devanture.

    La S1 demandait « une photo de devanture avec un slogan en anglais,
    floutee ou recomposee ». Dessinee, la devanture n'a pas besoin
    d'etre floutee : elle n'appartient a personne. Et surtout le slogan
    se lit — ce qui est la condition pour que la publication fonctionne,
    puisqu'elle parle de ce qui est ecrit dessus.

    La S4 demande la meme devanture avec la ligne francaise ajoutee.
    C'est le meme appel de fonction avec un argument de plus : la
    demonstration est donc rigoureusement « on n'a rien retire ».
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-17-francais-devanture"))
    accent("magenta")
    faits = []

    p = Planche("sable_chaud")
    p.d.rectangle([0, 0, p.l, 760], fill=_melange("sable", "creme", 0.30))
    _vitrine(p, 110, 250, 860, 460, eclairee=True, enseigne="SUNSET COFFEE",
             sous_enseigne="Best coffee in town — open all day")
    _bandeau_travers(p, "Votre slogan en anglais\nest-il légal ?", "bleu",
                     y=800, taille=58,
                     sous_titre="La réponse est oui. Avec une condition.")
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("creme")
    p.surtitre("La règle, en une phrase", y=170)
    p.titre("Ce qui informe le client\ndoit être compréhensible\nen français.",
            62, y=280)
    p.y = 760
    p.filet()
    p.texte("Ce qui vous nomme ne serait pas concerné de la même façon.",
            42, "brun", 600, avant=10)
    p.signature("brun")
    faits.append(p.ecrire(d / "02.png"))

    p = Planche("blanc")
    p.titre("Nommer, ou informer.", 72, y=150)
    col = (p.l - 2 * MARGE - 36) / 2
    for i, (titre_c, items, coul, verdict) in enumerate((
            ("NOMMER", ["un nom de marque", "une dénomination",
                        "une enseigne"], "turquoise", "Ce serait votre identité."),
            ("INFORMER", ["un slogan", "un descriptif", "une promotion",
                          "une mention de service"], "corail",
             "Là, le français serait attendu."))):
        x = MARGE + i * (col + 36)
        p.d.rounded_rectangle([x, 400, x + col, 1000], radius=26,
                              fill=_melange(coul, "blanc", 0.88))
        p.pastille(x + 26, 432, titre_c, coul, taille=26)
        yy = 526
        for it in items:
            p.d.ellipse([x + 32, yy + 12, x + 46, yy + 26], fill=teinte(coul))
            yy = _bloc(p, x + 62, yy, it, 34, "encre", 400, col - 90)
            yy += 14
        _bloc(p, x + 32, 884, verdict, 32, "brun", 600, col - 64)
    p.y = 1046
    p.texte("La ligne de partage est écrite au conditionnel : elle n'est "
            "pas vérifiée à la source.", 30, "taupe", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("creme")
    p.titre("On ne retire rien.\nOn ajoute une ligne.", 72, y=140)
    _vitrine(p, 110, 480, 860, 460, eclairee=True, enseigne="SUNSET COFFEE",
             sous_enseigne="Le meilleur café de la ville — ouvert toute la journée")
    p.y = 1020
    p.texte("Le nom reste en grand. La promesse se lit en français dessous, "
            "dans un corps plus petit. La parade est graphique, pas "
            "juridique.", 38, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "04.png"))

    p = Planche("sable_chaud")
    p.filet(y=280)
    p.titre("Et le catalan ?", 100, "encre")
    p.y += 50
    p.texte("Une carte bilingue français/catalan ne pose pas le même "
            "problème : le français y est présent.\n\nC'est l'unilingue "
            "étranger qui expose.", 42, "brun", 400, avant=20)
    p.signature("brun")
    faits.append(p.ecrire(d / "05.png"))

    p = Planche("blanc")
    p.titre("Vous avez un slogan\nen anglais ?", 86, y=280)
    p.y += 30
    p.texte("Postez-le en commentaire : je vous propose la ligne française "
            "qui va dessous sans alourdir le visuel.", 40, "brun", 400,
            avant=20)
    p.fleche("corail", y=940)
    p.signature("brun")
    faits.append(p.ecrire(d / "06.png"))
    return faits


def pub15_quiz_matieres(dossier=None):
    """n° 15, jeudi 12 novembre — reconnaitre quatre supports.

    Le quiz demandait quatre macrophotographies. Ce sont des coupes
    dessinees, et la legende de la publication le dit : « quatre
    matieres dessinees en coupe » et non « photographiees de tres
    pres ». Le jeu reste le meme — nommer la matiere — mais il devient
    plus facile sur l'alu composite, dont la coupe EST la reponse, et
    plus difficile sur le gaufrage, qui perd la lumiere rasante.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-19-quiz-matieres"))
    accent("turquoise")
    faits = []
    ordre = ["alu", "plexi", "depoli", "gaufre"]
    reponses = {
        "alu": ["alu composite", "plexi", "PVC expansé", "inox brossé"],
        "plexi": ["plexi coulé", "verre", "polycarbonate", "résine"],
        "depoli": ["verre sablé", "adhésif dépoli", "film solaire", "peinture"],
    }

    p = Planche("sable_chaud")
    p.surtitre("Quiz", y=130)
    p.titre("Quatre supports.\nVous en reconnaissez\ncombien ?", 60, y=200)
    _grille_matieres(p, 600, ordre, cote=285)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    for n, genre in enumerate(ordre[:3], 1):
        p = Planche("creme")
        p.pastille(MARGE, 120, "N° %d" % n, "corail", taille=30)
        cote = 520
        _matiere(p, (p.l - cote) / 2, 230, cote, genre)
        yy = 230 + cote + 56
        f = police(600, 40)
        for rep in reponses[genre]:
            p.d.rounded_rectangle([MARGE, yy, p.l - MARGE, yy + 82],
                                  radius=20, fill=teinte("blanc"))
            p.d.text((MARGE + 34, yy + 20), rep, font=f, fill=teinte("encre"))
            yy += 96
        p.signature("brun")
        faits.append(p.ecrire(d / ("0%d.png" % (n + 1))))

    p = Planche("sable_chaud")
    p.filet(y=130)
    p.titre("Les quatre réponses.", 70, "encre")
    yy = 430
    for genre in ordre:
        nom, usage = MATIERES[genre]
        _matiere(p, MARGE, yy, 150, genre)
        _bloc(p, MARGE + 190, yy + 18, nom, 40, "encre", 600, 640)
        _bloc(p, MARGE + 190, yy + 70, usage, 32, "brun", 400, 640)
        yy += 190
    p.fleche("corail", y=1150)
    p.d.text((MARGE + 110, 1156), "Votre score en commentaire.",
             font=police(600, 34), fill=teinte("brun"))
    p.signature("brun")
    faits.append(p.ecrire(d / "05.png"))
    return faits


def pub16_reel_fin_annee(dossier=None):
    """n° 16, reel de fin d'annee — decembre se decide en novembre.

    Le decoupage demandait cinq plans tournes, dont une table de famille
    avec « des mains de plusieurs generations », et proposait un prompt
    d'image generee pour ce dernier plan. Le prompt est ecarte, comme
    pour la n° 12. Les mains le sont aussi : un plan de mains dessine
    serait soit maladroit, soit une illustration de banque d'images
    deguisee. La table reste, vue de dessus, avec ce qu'il y a dessus —
    c'est ce que le plan devait montrer.

    Ce sont des ECRANS FINIS : le reel se monte en les enchainant.

    L'arbitrage n° 1 de A-FAIRE-APRES-RELECTURE.md place ce reel APRES
    le carrousel n° 17 : c'est le carrousel qui ouvre le sujet de fin
    d'annee, le reel enfonce le clou. D'ou le samedi 28 novembre.

    Tout ce qui est date ici suit ce deplacement : la bande de jours
    part du 28, le compte passe de cinq semaines a quatre, et les
    jalons glissent d'autant. Un reel qui dit « on est le 28 novembre »
    en montrant une grille qui part du 21 se trahit tout seul.
    """
    import datetime
    d = pathlib.Path(dossier or (SORTIE / "2026-11-28-reel-fin-annee"))
    accent("corail")
    faits = []

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("Reel · 0-3 s", "taupe", y=180)
    p.titre("Pour Noël,\nvous êtes déjà\nen retard.", 100, y=260)
    _bande_jours(p, 90, 760, 900, datetime.date(2026, 11, 28),
                 datetime.date(2026, 12, 24),
                 {datetime.date(2026, 12, 24): ("encre", "")},
                 haut_case=116)
    p.y = 1600
    p.texte("Quatre semaines. C'est tout ce qui reste.", 46, "brun", 600,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran1.png"))

    p = Planche("sable_chaud", LARGE_S, HAUT_S)
    p.surtitre("3-9 s", "taupe", y=180)
    p.titre("Une carte imprimée\nse garde.\nUn mail se ferme.", 70, y=250)
    # la carte qui porte le texte passe par-dessus : dessinee en
    # premier, l'autre lui mangeait la moitie du mot.
    _carte(p, 700, 1100, 360, 480, -7, gaufre=True)
    _carte(p, 390, 1030, 360, 480, 9, gaufre=True, texte="Bonne année")
    p.y = 1480
    p.texte("Une carte reste sur un bureau trois semaines. Ce n'est pas de "
            "la nostalgie, c'est de la durée d'exposition.", 42, "brun",
            400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran2.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("9-15 s", "taupe", y=180)
    p.titre("Un bandeau suffit.\nPas un packaging\nentier.", 78, y=250)
    _emballage_kraft(p, p.l / 2, 1050, 760, 560)
    p.y = 1480
    p.texte("Un bandeau imprimé et un adhésif au logo transforment un "
            "papier kraft. Le client photographie ça.", 42, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran3.png"))

    p = Planche("blanc", LARGE_S, HAUT_S)
    p.surtitre("15-21 s", "taupe", y=180)
    p.titre("Création · BAT ·\nLivraison", 92, y=250)
    jalons = [("fin novembre", "création", "violet"),
              ("début décembre", "bon à tirer", "bleu"),
              ("mi-décembre", "livraison", "corail")]
    yy = 700
    for quand, quoi, coul in jalons:
        p.d.ellipse([MARGE, yy, MARGE + 46, yy + 46], fill=teinte(coul))
        if quand != jalons[-1][0]:
            p.d.line([(MARGE + 23, yy + 46), (MARGE + 23, yy + 220)],
                     fill=_melange(coul, "blanc", 0.55), width=6)
        _bloc(p, MARGE + 86, yy - 4, quoi, 52, "encre", 600, 760)
        _bloc(p, MARGE + 86, yy + 62, quand, 36, "taupe", 400, 760)
        yy += 220
    p.y = 1480
    p.texte("Un jour de retard au début, c'est une semaine de retard à la "
            "fin : en décembre les imprimeurs travaillent à plein.", 42,
            "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran4.png"))

    p = Planche("encre", LARGE_S, HAUT_S)
    # la table vue de dessus : un plateau de bois, et ce qu'on y a pose.
    p.d.rectangle([0, 420, p.l, 1340], fill=_melange("brun", "encre", 0.42))
    for i in range(8):
        yy = 420 + i * 124
        p.d.line([(0, yy), (p.l, yy)], fill=_melange("brun", "encre", 0.52),
                 width=4)
    _carte(p, 690, 800, 300, 400, -9, fond="creme", gaufre=True)
    _carte(p, 330, 720, 300, 400, 14, fond="creme", gaufre=True,
           texte="Bonne année")
    _emballage_kraft(p, 520, 1120, 460, 320)
    p.y = 1380
    p.filet()
    p.titre("Décembre se décide\nen novembre.", 68, "blanc")
    p.abonnement("sable")
    p.signature("sable")
    faits.append(p.ecrire(d / "ecran5.png"))
    return faits


def pub18_emballage_tri(dossier=None):
    """n° 18, mardi 17 novembre — la place a reserver sur un emballage.

    La S1 demandait une photo de sachet cadeau, la S2 le meme sachet en
    dessin au trait. Les deux sont dessines : c'est la seule facon de
    garantir que c'est le MEME sachet, ce que la demonstration exige.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-24-emballage-tri"))
    accent("turquoise")
    faits = []

    p = Planche("creme")
    _sachet(p, p.l / 2, 180, 460, 620)
    _bandeau_travers(p, "Votre bel emballage de fête\na une mention à "
                        "porter.", "violet", y=880, taille=52)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("blanc")
    p.titre("Il lui faut cette place.", 62, y=140)
    _sachet(p, p.l / 2, 350, 450, 600, trait=True, zone=True)
    p.y = 1030
    p.texte("La question est de savoir qui la réserve, et quand.", 40,
            "brun", 600, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "02.png"))

    p = Planche("blanc")
    p.surtitre("Le principe", y=150)
    p.titre("Un emballage destiné\nau grand public devrait\nporter une "
            "signalétique\nde tri.", 54, y=230)
    p.y = 760
    p.texte("Le pictogramme accompagné de la consigne, élément par élément.",
            42, "brun", 400, avant=0)
    p.y = 1070
    p.texte("Cadre généralement cité : loi AGEC de 2020. À confirmer auprès "
            "de votre éco-organisme.", 30, "bleu", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("creme")
    p.titre("Dans quel ordre ?", 76, y=150)
    col = (p.l - 2 * MARGE - 36) / 2
    for i, (texte_c, coul, barre) in enumerate((
            ("On dessine, puis on cherche où la mettre.", "corail", True),
            ("On réserve la zone, puis on dessine autour.", "violet", False))):
        x = MARGE + i * (col + 36)
        fonte = police(600, 38)
        lignes = couper(texte_c, fonte, col - 68)
        hc = 70 + len(lignes) * int(38 * 1.34) + 70
        p.d.rounded_rectangle([x, 430, x + col, 430 + hc], radius=26,
                              fill=teinte("blanc"),
                              outline=teinte(coul), width=0 if barre else 5)
        yy = 430 + 70
        for ligne in lignes:
            p.d.text((x + 34, yy), ligne, font=fonte, fill=teinte("encre"))
            if barre:
                # chaque ligne est barree : un seul trait au milieu du bloc
                # ne barre que la ligne du milieu, et ca se voit.
                lw = p.d.textlength(ligne, font=fonte)
                p.d.line([(x + 30, yy + 26), (x + 38 + lw, yy + 26)],
                         fill=teinte("corail"), width=4)
            yy += int(38 * 1.34)
    p.y = 880
    p.texte("Le second ordre coûte dix minutes. Le premier coûte une "
            "réimpression.", 38, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "04.png"))

    p = Planche("sable_chaud")
    p.filet(y=300)
    p.titre("Un emballage dessiné\nsans cette place\nse refait.", 84, "encre")
    p.y += 50
    p.texte("Et un emballage de Noël qui se refait, c'est un emballage qui "
            "arrive en janvier.", 42, "brun", 400, avant=20)
    p.signature("brun")
    faits.append(p.ecrire(d / "05.png"))

    p = Planche("blanc")
    p.titre("Trois interlocuteurs,\ndans cet ordre.", 72, y=150)
    p.puces(["Votre éco-organisme dit ce que vous devez afficher.",
             "Votre imprimeur dit à quelle taille c'est lisible.",
             "Le graphiste place les deux dans le dessin."],
            "corail", 40, "brun", numerote=True, y=520, interligne=1.7)
    p.signature("brun")
    faits.append(p.ecrire(d / "06.png"))

    p = Planche("encre")
    p.filet(y=330)
    p.titre("Vous préparez\nun emballage\npour les fêtes ?", 92, "blanc")
    p.y += 40
    p.texte("Dites-moi en commentaire ce que vous vendez : je vous dis "
            "quelles questions poser, et à qui.", 40, "creme", 400, avant=20)
    p.fleche("corail", y=1120)
    p.signature("sable")
    faits.append(p.ecrire(d / "07.png"))
    return faits


def pub21_vitrine_trottoir(dossier=None):
    """n° 21, lundi 23 novembre — la vitrine vue du trottoir d'en face.

    Sept planches au lieu des six prevues. La septieme est la meme
    devanture redessinee a 2, 8 et 25 metres : c'est la demonstration
    que la publication reclame sans pouvoir la faire en photo, puisqu'il
    faudrait trois prises de vue au meme instant. Le texte alternatif de
    la publication est a mettre a jour en consequence.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-30-vitrine-trottoir"))
    accent("violet")
    faits = []

    p = Planche("creme")
    _trottoir_den_face(p, 0, 830)
    _bandeau_travers(p, "Votre vitrine de Noël est faite\npour celui qui "
                        "passe. Pas pour\ncelui qui est dedans.", "violet",
                     y=880, taille=46)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("blanc")
    p.titre("La hauteur des yeux.", 76, y=140)
    _vitrine(p, 170, 380, 780, 500, trait=True, oeil=True, echelle=True,
             enseigne="VOTRE NOM")
    p.y = 980
    p.texte("Entre 1,40 m et 1,70 m : c'est la seule zone vraiment lue. Le "
            "reste est deviné.", 40, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "02.png"))

    p = Planche("creme")
    p.titre("Couvrir, ou laisser voir.", 70, y=130)
    _vitrine(p, 90, 380, 430, 300, eclairee=True, couverture=0.96,
             couleur_decor="corail", decor="sapins", opacite_decor=0xee)
    _vitrine(p, 560, 380, 430, 300, eclairee=True, bandeau=0.30,
             couleur_decor="corail", decor="sapins")
    f = police(600, 30)
    for x, lib in ((90, "le verre couvert"), (560, "un bandeau, du verre libre")):
        p.d.text((x, 710), lib, font=f, fill=teinte("brun"))
    p.y = 800
    p.texte("On entre pour ce qu'on voit à l'intérieur. Un décor qui bouche "
            "la vue protège votre boutique des regards — et des clients.",
            38, "bleu", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("sable_chaud")
    p.filet(y=240)
    p.titre("À 17 h en décembre,\nil fait nuit.", 72, "encre")
    _vitrine(p, 240, 660, 600, 330, eclairee=False, reflet=True,
             enseigne="VOTRE NOM")
    p.y = 1020
    p.texte("Si l'intérieur n'est pas éclairé, votre vitrine devient un "
            "miroir et votre client s'y voit lui-même.", 40, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "04.png"))

    p = Planche("blanc")
    p.titre("Un texte sur verre se lit\ncontre ce qu'il y a derrière.",
            58, y=140)
    _fond_du_texte(p, MARGE, 448, p.l - 2 * MARGE, 460)
    p.y = 982
    p.texte("Et ce qu'il y a derrière bouge toute la journée.", 40, "brun",
            600, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "05.png"))

    p = Planche("creme")
    p.titre("La même vitrine,\ntrois reculs.", 74, y=140)
    _trois_distances(p, 460)
    p.y = 840
    p.texte("À 2 m tout se lit. À 8 m les horaires sont déjà partis. À "
            "25 m il ne reste que la forme — et c'est à 25 m qu'on décide "
            "de traverser.", 38, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "06.png"))

    p = Planche("creme")
    p.titre("Photographiez votre vitrine\ndepuis le trottoir d'en face.",
            60, y=300)
    p.y += 30
    p.texte("Envoyez-la-moi en message : je vous dis ce qui se lit et ce "
            "qui se perd.", 40, "brun", 400, avant=20)
    p.fleche("corail", y=940)
    p.signature("brun")
    faits.append(p.ecrire(d / "07.png"))
    return faits


def pub22_sticker_enseigne(dossier=None):
    """n° 22, mardi 24 novembre — un sticker de Noel, c'est quoi au juste.

    La S1 demandait la photo d'une vitrine portant deux adhesifs. Elle
    est dessinee, et c'est preferable ici plus qu'ailleurs : la
    publication explique qu'un de ces deux adhesifs pourrait etre
    requalifie. Illustrer ca avec la vitrine d'un commerce reel, c'est
    le designer comme le mauvais eleve.

    L'arbitrage n° 2 de A-FAIRE-APRES-RELECTURE.md fait de « quand ca
    devient une enseigne » le sujet principal de cette publication.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-12-01-sticker-enseigne"))
    accent("rose")
    faits = []

    p = Planche("creme")
    p.d.rectangle([0, 0, p.l, 820], fill=_melange("sable", "creme", 0.35))
    _vitrine(p, 100, 230, 880, 470, eclairee=True, enseigne="VOTRE NOM",
             stickers=[("Joyeuses fêtes", "violet", (0.30, 0.26), 38),
                       ("-30 %", "bleu", (0.62, 0.66), 52)])
    _bandeau_travers(p, "Un sticker de Noël sur votre vitrine :\nenseigne, "
                        "publicité, ou rien du tout ?", "violet", y=860,
                     taille=46)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("creme_rose")
    p.titre("Ce n'est pas\ndu vocabulaire.", 76, y=140)
    col = (p.l - 2 * MARGE - 36) / 2
    for i, (mot, quoi, verbe, coul) in enumerate((
            ("Enseigne", "elle dit qui vous êtes et où.", "On l'autorise.",
             "violet"),
            ("Publicité", "elle dit ce que vous vendez à quel prix.",
             "On la déclare.", "bleu"))):
        x = MARGE + i * (col + 36)
        p.d.rounded_rectangle([x, 420, x + col, 920], radius=26,
                              fill=teinte("blanc"), outline=teinte(coul),
                              width=5)
        _bloc(p, x + 34, 470, mot, 52, coul, 800, col - 68)
        _bloc(p, x + 34, 560, quoi, 34, "brun", 400, col - 68)
        _bloc(p, x + 34, 800, verbe, 38, "encre", 600, col - 68)
    p.y = 980
    p.texte("Une déclaration, on la dépose. Une autorisation, on l'attend.",
            38, "brun", 600, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "02.png"))

    p = Planche("creme")
    p.titre("L'un décore.\nL'autre vend.", 86, y=150)
    for i, (texte_b, coul) in enumerate((("Joyeuses fêtes", "violet"),
                                         ("-30 % jusqu'au 24", "bleu"))):
        fb = police(800, 54)
        lb = p.d.textlength(texte_b, font=fb)
        yy = 480 + i * 200
        p.d.rounded_rectangle([MARGE, yy, MARGE + lb + 80, yy + 118],
                              radius=58, fill=teinte(coul))
        p.d.text((MARGE + 40, yy + 28), texte_b, font=fb, fill=teinte("blanc"))
    p.y = 920
    p.texte("Le premier décore. Le second vend. Ce ne sont probablement pas "
            "les mêmes règles.", 38, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("bleu")
    p.filet(y=280)
    p.titre("C'est votre commune\nqui tranche.", 88, "blanc")
    p.y += 40
    p.texte("Le Règlement Local de Publicité et le PLU fixent les surfaces, "
            "la durée, l'éclairage.\n\nÀ trois kilomètres de distance, la "
            "réponse change.", 40, "creme", 400, avant=20)
    p.signature("creme")
    faits.append(p.ecrire(d / "04.png"))

    p = Planche("blanc")
    p.titre("Et surtout :\npas le 14798*01.", 72, y=130)
    _feuille_formulaire(p, p.l / 2, 420, 480, 500, "Cerfa n° 16308*01",
                        "Le formulaire en vigueur, en mairie", lignes=5)
    p.y = 920
    p.encadre("Le 14798*01 est périmé. Un dossier déposé avec l'ancien "
              "formulaire est considéré comme incomplet depuis le "
              "1er juillet 2026 — et il remonte encore dans les recherches.",
              36, "blanc", "corail", pad=32)
    p.signature("brun")
    faits.append(p.ecrire(d / "05.png"))

    p = Planche("violet")
    p.filet(y=320)
    p.titre("Dites-moi votre commune\nen commentaire.", 72, "blanc")
    p.y += 40
    p.texte("Je vous dis quelle question poser. Un appel au service "
            "urbanisme coûte dix minutes, et c'est gratuit.", 40, "creme",
            400, avant=20)
    p.fleche("corail", y=1060)
    p.signature("creme")
    faits.append(p.ecrire(d / "06.png"))
    return faits


# ---------------------------------------------------------------------
# Les matieres en main — n° 20.
# ---------------------------------------------------------------------
# Ces trois dessins sont les seuls du lot qui remplacent une photo par
# quelque chose de MOINS riche. Une dorure, un gaufrage, un papier qui
# ondule se sentent ; une photo en lumiere rasante en garde quelque
# chose, un trace non. En echange, le dessin met les deux etats cote a
# cote — gaufrage de cote ET de face, dorure allumee ET eteinte — la ou
# le tournage les separait par un mouvement de camera. C'est ce qui est
# demontre qui change, pas seulement ce qui est montre : le sujet de ce
# reel est precisement que la matiere n'existe que sous un certain
# angle, et une paire le dit mieux qu'une rotation.

@pose(flou=14, force=70, bas=9, cote=4)
def _carte_tranche(p, x, y, larg, haut, etiquette):
    """Une carte epaisse vue legerement de trois quarts, sa tranche visible.

    Le grammage ne se montre pas de face : il se montre par l'epaisseur.
    Trois millimetres grossis, comme pour les matieres du quiz.
    """
    e = haut * 0.10
    biais = e * 0.9
    p.d.polygon([(x, y + e), (x + biais, y), (x + larg, y),
                 (x + larg - biais, y + e)],
                fill=_melange("blanc", "creme", 0.35))
    p.d.rectangle([x, y + e, x + larg - biais, y + haut],
                  fill=teinte("creme"))
    p.d.polygon([(x + larg - biais, y + e), (x + larg, y),
                 (x + larg, y + haut - e), (x + larg - biais, y + haut)],
                fill=_melange("creme", "taupe", 0.42))
    f = police(600, max(20, int(haut * 0.11)))
    p.d.text((x + larg / 2 - p.d.textlength(etiquette, font=f) / 2,
              y + haut + 18), etiquette, font=f, fill=teinte("creme"))
    return p


@pose(flou=14, force=66, bas=9, cote=4)
def _papier_profil(p, x, y, larg, affaissement, etiquette, couleur="corail"):
    """Une feuille vue sur la tranche, tenue a gauche, qui s'affaisse.

    C'est le test que tout imprimeur fait sans y penser : on pince une
    carte par un bord et on regarde si l'autre bord tombe. Un 120 g
    s'affaisse, un 350 g reste droit. Dessine de profil, le grammage
    devient visible — ce qu'une photo de face ne montre jamais.
    """
    ep = max(5, int(larg * 0.014))
    pince = larg * 0.16
    p.d.rounded_rectangle([x, y - 22, x + pince, y + 22], radius=10,
                          fill=teinte("taupe"))
    pts_haut, pts_bas = [], []
    n = 40
    for i in range(n + 1):
        t = i / n
        xx = x + pince + (larg - pince) * t
        yy = y + affaissement * t * t
        pts_haut.append((xx, yy - ep / 2))
        pts_bas.append((xx, yy + ep / 2))
    p.d.polygon(pts_haut + list(reversed(pts_bas)),
                fill=_melange("creme", "blanc", 0.6),
                outline=teinte("brun"))
    for pts in (pts_haut, pts_bas):
        p.d.line(pts, fill=teinte("brun"), width=max(2, ep // 3))
    f = police(800, max(26, int(larg * 0.075)))
    l = p.d.textlength(etiquette, font=f)
    p.d.text((x + larg - l, y + affaissement + 48), etiquette, font=f,
             fill=teinte(couleur))
    return p


@pose(flou=16, force=70, bas=10, cote=5)
def _gaufrage(p, x, y, cote, rasante=True, legende=None,
              couleur_legende="brun"):
    """Un gaufrage, eclaire de cote ou de face.

    Un gaufrage n'a pas de couleur : il n'a qu'une ombre et une lumiere.
    En lumiere rasante, les deux sont decalees et le relief apparait ;
    de face, elles se superposent et il ne reste presque rien. Les deux
    dessins sortent du meme code, avec un seul parametre de decalage —
    donc on ne peut pas tricher en exagerant l'un des deux.
    """
    p._place(y, "gaufrage")
    p.d.rectangle([x, y, x + cote, y + cote], fill=teinte("creme"),
                  outline=_melange("taupe", "creme", 0.40), width=3)
    ep = max(4, int(cote * 0.030))
    cx, cy, r = x + cote * 0.50, y + cote * 0.44, cote * 0.21
    if rasante:
        d = max(3, int(cote * 0.018))
        paires = ((-d, teinte("blanc")),
                  (d, _melange("taupe", "brun", 0.40)))
    else:
        # de face, l'ombre et la lumiere se superposent : il ne reste
        # qu'un trace presque efface. C'est le sujet du plan, il ne faut
        # donc pas tricher en en laissant un peu « pour qu'on voie ».
        paires = ((0, _melange("creme", "taupe", 0.10)),)
    for decal, c in paires:
        p.d.ellipse([cx - r + decal, cy - r + decal,
                     cx + r + decal, cy + r + decal], outline=c, width=ep)
        p.d.line([(cx - r * 0.44 + decal, cy + r * 0.56 + decal),
                  (cx + r * 0.44 + decal, cy + r * 0.56 + decal)],
                 fill=c, width=ep)
    if legende:
        f = police(600, max(20, int(cote * 0.072)))
        p.d.text((x + cote / 2 - p.d.textlength(legende, font=f) / 2,
                  y + cote + 18), legende, font=f,
                 fill=teinte(couleur_legende))
    return p


@pose(flou=16, force=70, bas=10, cote=5)
def _dorure(p, x, y, larg, haut, allume=True, legende=None,
            couleur_legende="brun"):
    """Un filet de dorure a chaud, qui accroche ou non la lumiere.

    Ce n'est pas du jaune : c'est une feuille metallisee. Allumee, elle
    porte un degrade qui va du brun sombre a l'or blanc et revient ;
    eteinte, elle est plus sombre que le papier. C'est exactement ce que
    le plan filme devait montrer en tournant la carte.
    """
    p._place(y, "dorure")
    p.d.rectangle([x, y, x + larg, y + haut], fill=teinte("creme"),
                  outline=_melange("taupe", "creme", 0.40), width=3)
    bx, bl = x + larg * 0.12, larg * 0.76
    bh = max(10, int(haut * 0.085))
    by = y + haut * 0.46
    if allume:
        barre = _degrade_lineaire(int(bl), bh, 90.0,
                                  [(0.0, C["brun"]), (0.26, C["orange"]),
                                   (0.46, C["jaune"]), (0.58, C["blanc"]),
                                   (0.74, C["jaune"]), (1.0, C["brun"])])
        p.im.paste(barre, (int(bx), int(by)))
        p._redessiner()
        _halo(p, bx + bl / 2, by + bh / 2, bl * 0.34, bh * 2.4, "jaune", 64, 26)
    else:
        p.d.rectangle([bx, by, bx + bl, by + bh],
                      fill=_melange("brun", "encre", 0.42))
    if legende:
        fl = police(600, max(20, int(haut * 0.13)))
        p.d.text((x + larg / 2 - p.d.textlength(legende, font=fl) / 2,
                  y + haut + 18), legende, font=fl,
                 fill=teinte(couleur_legende))
    return p


def pub20_reel_matieres(dossier=None):
    """n° 20, vendredi 20 novembre — ce que vos clients sentent avant de lire.

    Remplace les fiches de tournage par cinq ecrans finis, comme les
    n° 12 et n° 16. Le prompt d'image generee du plan d'ouverture est
    retire pour la meme raison qu'ailleurs.

    Reserve honnete, ecrite aussi dans photos-a-prendre.md : c'est le
    sujet ou le dessin perd le plus. Une dorure photographiee en lumiere
    rasante garde quelque chose que le trace n'a pas. Si un jour les
    echantillons sont sous la main, ces ecrans se remplacent un par un.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-27-reel-matieres"))
    accent("jaune")
    faits = []

    p = Planche("sable_chaud", LARGE_S, HAUT_S)
    p.surtitre("Reel · 0-3 s", "taupe", y=200)
    p.filet()
    p.titre("Ce que vos clients\nsentent\navant de lire.", 84, y=280)
    _gaufrage(p, 180, 900, 700, rasante=True)
    p.y = 1640
    p.texte("Avant de lire votre carte, votre client la touche. Et il a "
            "déjà une opinion.", 42, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran1.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("3-8 s", "taupe", y=200)
    p.titre("120 g / 350 g", 110, y=280)
    _papier_profil(p, 110, 760, 860, 300, "120 g", "corail")
    _papier_profil(p, 110, 1290, 860, 8, "350 g", "bleu")
    p.y = 1560
    p.texte("Le grammage, c'est le poids du papier. Le prix change peu. La "
            "sensation change tout.", 42, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran2.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("8-14 s", "taupe", y=200)
    p.titre("Le gaufrage :\ndu relief,\npas de l'encre.", 92, y=270)
    _gaufrage(p, 90, 900, 420, True, "lumière de côté")
    _gaufrage(p, 570, 900, 420, False, "lumière de face")
    p.y = 1480
    p.texte("Le même relief, deux éclairages. De face, il disparaît presque "
            "— c'est pour ça qu'on l'oublie au moment de choisir, et qu'on "
            "le remarque toujours en main.", 40, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran3.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("14-19 s", "taupe", y=200)
    p.titre("La dorure :\nune feuille,\npas du jaune.", 92, y=270)
    _dorure(p, 90, 900, 420, 300, True, "sous un angle")
    _dorure(p, 570, 900, 420, 300, False, "sous un autre")
    p.y = 1340
    p.texte("Une feuille métallisée pressée à chaud. Elle réfléchit la "
            "lumière, elle change selon l'angle, et elle coûte un passage "
            "de plus en atelier.", 40, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran4.png"))

    p = Planche("encre", LARGE_S, HAUT_S)
    _gaufrage(p, 90, 470, 280, True, "gaufrage", "sable")
    _dorure(p, 400, 470, 280, 280, True, "dorure", "sable")
    _carte_tranche(p, 710, 470, 280, 280, "350 g")
    p.y = 920
    p.filet()
    p.titre("Choisissez la matière\navant le dessin.", 84, "blanc")
    p.y += 30
    p.texte("Un beau visuel sur un mauvais papier déçoit. Un visuel simple "
            "sur un beau papier se garde.", 40, "creme", 400, avant=20)
    p.abonnement("sable")
    p.signature("sable")
    faits.append(p.ecrire(d / "ecran5.png"))
    return faits


# ---------------------------------------------------------------------
# Le bilan de fin d'annee — n° 24.
# ---------------------------------------------------------------------
@pose(flou=18, force=74, bas=12, cote=6)
def _page_calendrier(p, x, y, larg, haut, mois, annee, dernier=None,
                     couleur="violet"):
    """Une page de calendrier mural, avec sa spirale et son mois en grand.

    Le plan filme voulait un doigt qui tourne la page de decembre a
    janvier. Deux pages cote a cote disent la meme chose, et disent en
    plus ce que le mouvement cachait : que rien n'a change entre les
    deux, sauf le nom du mois.
    """
    import calendar
    p.d.rectangle([x, y, x + larg, y + haut], fill=teinte("blanc"),
                  outline=_melange("taupe", "blanc", 0.4), width=3)
    hb = haut * 0.26
    p.d.rectangle([x, y, x + larg, y + hb], fill=teinte(couleur))
    f = police(800, int(hb * 0.46))
    nom = ["JANVIER", "FÉVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET",
           "AOÛT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DÉCEMBRE"][mois - 1]
    p.d.text((x + larg / 2 - p.d.textlength(nom, font=f) / 2, y + hb * 0.18),
             nom, font=f, fill=teinte("blanc"))
    fa = police(600, int(hb * 0.22))
    p.d.text((x + larg / 2 - p.d.textlength(str(annee), font=fa) / 2,
              y + hb * 0.68), str(annee), font=fa,
             fill=_melange("blanc", couleur, 0.35))
    # la spirale, qui fait que c'est un calendrier et pas une affiche
    for i in range(6):
        cx = x + larg * (0.12 + i * 0.152)
        p.d.ellipse([cx - 9, y - 16, cx + 9, y + 16],
                    outline=teinte("taupe"), width=4)
    # la grille des jours, sans chiffres : ce n'est pas elle qu'on lit
    cols, lignes = 7, 5
    gx, gy = x + larg * 0.07, y + hb + haut * 0.08
    cw = (larg * 0.86) / cols
    ch = (haut - hb - haut * 0.16) / lignes
    fd = police(400, max(12, int(ch * 0.42)))
    jour = 1
    total = calendar.monthrange(annee, mois)[1]
    debut = calendar.monthrange(annee, mois)[0]
    for r in range(lignes):
        for c in range(cols):
            if r * 7 + c < debut or jour > total:
                continue
            xx, yy = gx + c * cw, gy + r * ch
            t = str(jour)
            p.d.text((xx + cw / 2 - p.d.textlength(t, font=fd) / 2,
                      yy + ch * 0.2), t, font=fd,
                     fill=teinte("taupe" if jour != dernier else "corail"))
            jour += 1
    return p


@pose(flou=14, force=64, bas=9, cote=4)
def _support_logo(p, cx, cy, taille, genre, brouille=False,
                  couleur_legende="taupe"):
    """Le meme logo pose sur un polo, une carte ou un panneau.

    Le plan filme devait montrer un logo qui tient sur deux supports et
    se brouille sur le troisieme. Dessine, le brouillage n'est pas une
    licence : le logo est rendu puis REELLEMENT degrade — floute et
    reduit en paliers, comme une broderie qui ne sait pas rendre un
    contour fin. On voit donc disparaitre exactement ce qui disparait.
    """
    t = taille
    if genre == "polo":
        # une silhouette de polo : deux epaules, deux manches, un col
        p.d.rounded_rectangle([cx - t * .46, cy - t * .40, cx + t * .46,
                               cy + t * .52], radius=int(t * .07),
                              fill=_melange("bleu", "encre", 0.28))
        for s in (-1, 1):
            p.d.polygon([(cx + s * t * .46, cy - t * .36),
                         (cx + s * t * .72, cy - t * .10),
                         (cx + s * t * .58, cy + t * .06),
                         (cx + s * t * .46, cy - t * .12)],
                        fill=_melange("bleu", "encre", 0.36))
        p.d.polygon([(cx - t * .13, cy - t * .40), (cx, cy - t * .18),
                     (cx + t * .13, cy - t * .40)],
                    fill=_melange("bleu", "blanc", 0.22))
    elif genre == "carte":
        p.d.rectangle([cx - t * .62, cy - t * .36, cx + t * .62, cy + t * .36],
                      fill=teinte("creme"),
                      outline=_melange("taupe", "creme", 0.4), width=3)
    else:                                    # panneau
        p.d.rectangle([cx - t * .62, cy - t * .44, cx + t * .62, cy + t * .30],
                      fill=_melange("sable", "taupe", 0.30),
                      outline=_melange("taupe", "brun", 0.40), width=3)
        for s in (-1, 1):
            p.d.rectangle([cx + s * t * .36 - t * .035, cy + t * .30,
                           cx + s * t * .36 + t * .035, cy + t * .56],
                          fill=_melange("taupe", "encre", 0.45))

    r = int(t * (0.13 if genre == "polo" else 0.17))
    lx, ly = (cx, cy + t * .04) if genre == "polo" else (cx, cy - t * .04)
    if brouille:
        # le logo est dessine en grand, puis reduit comme le ferait une
        # aiguille : floute, puis quantifie. Rien n'est « dessine flou ».
        cote = r * 6
        vignette = Image.new("RGB", (cote, cote),
                             _melange("bleu", "encre", 0.28))
        dv = ImageDraw.Draw(vignette)
        _logo_fictif(dv, cote // 2, cote // 2, int(cote * 0.42), detail=True)
        vignette = vignette.filter(ImageFilter.GaussianBlur(cote * 0.018))
        vignette = vignette.resize((max(5, cote // 14), max(5, cote // 14)),
                                   Image.BILINEAR)
        vignette = vignette.resize((int(r * 2.4), int(r * 2.4)),
                                   Image.NEAREST)
        p.im.paste(vignette, (int(lx - r * 1.2), int(ly - r * 1.2)))
        p._redessiner()
    else:
        _logo_fictif(p.d, lx, ly, r, detail=True)

    f = police(600, max(18, int(t * 0.10)))
    lib = {"polo": "polo brodé", "carte": "carte de visite",
           "panneau": "panneau"}[genre]
    p.d.text((cx - p.d.textlength(lib, font=f) / 2, cy + t * .66), lib,
             font=f, fill=teinte(couleur_legende))
    return p


def pub24_reel_bilan(dossier=None):
    """n° 24, samedi 28 novembre — faut-il refaire son logo en janvier.

    Comme les n° 12, 16 et 20 : cinq ecrans finis a la place des fiches
    de tournage, et le prompt d'image generee du plan d'ouverture retire.

    Le carnet de croquis qui se ferme disparait — un carnet dessine qui
    se ferme ne se ferme pas, c'est un plan qui n'existe qu'en mouvement.
    Il est remplace par ce que le plan voulait dire : deux pages de
    calendrier, decembre et janvier, rigoureusement identiques sauf le
    nom du mois. C'est l'argument de la publication, pose d'emblee.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-12-05-reel-bilan"))
    accent("corail")
    faits = []

    p = Planche("sable_chaud", LARGE_S, HAUT_S)
    p.surtitre("Reel · 0-3 s", "taupe", y=200)
    p.filet()
    p.titre("Non,\npas en janvier.", 116, y=290)
    _page_calendrier(p, 110, 820, 400, 520, 12, 2026, couleur="bleu")
    _page_calendrier(p, 580, 820, 400, 520, 1, 2027, couleur="violet")
    p.fleche("corail", y=1420)
    p.y = 1520
    p.texte("Chaque mois de janvier, on me demande de refaire un logo. Et "
            "souvent, je réponds non.", 42, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran1.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("3-9 s", "taupe", y=200)
    p.titre("Changer par calendrier,\nce n'est pas changer\npar besoin.",
            72, y=280)
    _logo_fictif(p.d, 330, 980, 190, detail=True)
    _logo_fictif(p.d, 760, 980, 190, detail=True, variante=0.045)
    f = police(600, 32)
    for x, lib in ((330, "version actuelle"), (760, "« nouvelle » version")):
        p.d.text((x - p.d.textlength(lib, font=f) / 2, 1270), lib, font=f,
                 fill=teinte("taupe"))
    p.y = 1400
    p.texte("Un logo qui marche n'a pas à être renouvelé comme un "
            "abonnement. La mémorisation est lente — c'est précisément ce "
            "qu'on achète.", 42, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran2.png"))

    p = Planche("blanc", LARGE_S, HAUT_S)
    p.surtitre("9-15 s", "taupe", y=200)
    p.titre("Trois questions,\navant de redessiner.", 88, y=280)
    questions = ["Lisible partout ?", "Fichiers en main ?",
                 "Dit-il ce que vous\nvendez aujourd'hui ?"]
    y = 700
    for i, q in enumerate(questions, 1):
        fm = manuscrite(62)
        lignes = q.split("\n")
        h = 150 + (len(lignes) - 1) * 72
        p.d.rounded_rectangle([MARGE, y, p.l - MARGE, y + h], radius=22,
                              fill=teinte("creme"),
                              outline=_melange("taupe", "creme", 0.4), width=3)
        p.pastille(MARGE + 30, y + 28, str(i), "corail", taille=30)
        yy = y + 24
        for ligne in lignes:
            p.d.text((MARGE + 140, yy), ligne, font=fm, fill=teinte("encre"))
            yy += 72
        y += h + 38
    p.y = 1520
    p.texte("Elles se posent en fin d'année, quand on a du recul, et elles "
            "coûtent dix minutes.", 42, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran3.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("15-21 s", "taupe", y=200)
    p.titre("Deux « oui »,\nun « non » :\non ajuste.", 96, y=280)
    for cx, genre, flou in ((245, "carte", False), (540, "panneau", False),
                            (835, "polo", True)):
        _support_logo(p, cx, 1040, 208, genre, brouille=flou)
    p.y = 1420
    p.texte("Le même logo : il tient sur deux supports, il se brouille sur "
            "le troisième. Un problème précis se répare.", 42, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran4.png"))

    p = Planche("encre", LARGE_S, HAUT_S)
    for cx, genre in ((245, "carte"), (540, "panneau"), (835, "polo")):
        _support_logo(p, cx, 700, 208, genre, couleur_legende="sable")
    p.y = 1080
    p.filet()
    p.titre("Un bilan,\npas une résolution.", 92, "blanc")
    p.y += 20
    p.texte("Trois « non », on repart de la feuille blanche — et ça se "
            "décide en connaissance de cause.", 40, "creme", 400, avant=20)
    p.abonnement("sable")
    p.signature("sable")
    faits.append(p.ecrire(d / "ecran5.png"))
    # Dernier écran du dernier reel du cycle : le pilier « la personne »
    # ferme la boucle ouverte par la première publication.
    p = Planche("creme", LARGE_S, HAUT_S)
    p.photo("sandra-sourire", ancrage="centre", voile="encre", part=0.46)
    p.y = 1280
    p.titre("Si votre logo vous gêne,\nparlons-en.", 62, "blanc")
    p.texte("Sandra, Grafycom — Perpignan.", 36, "creme", 600, avant=24)
    p.abonnement("sable")
    p.signature("creme")
    faits.append(p.ecrire(d / "ecran6.png"))

    return faits


# ---------------------------------------------------------------------
# RVB et CMJN — n° 4. Le seul endroit du fichier ou la charte ne
# s'applique pas, et c'est deliberе.
# ---------------------------------------------------------------------
# Un schema RVB doit etre fait avec le rouge, le vert et le bleu d'un
# ecran, c'est-a-dire les trois canaux a fond. Un schema CMJN doit etre
# fait avec les quatre encres d'imprimerie. Ce ne sont pas des couleurs
# choisies : ce sont les valeurs physiques dont la publication parle.
# Les remplacer par des couleurs de la charte rendrait le schema FAUX —
# on expliquerait la synthese additive avec des teintes qui ne sont pas
# des primaires.
#
# Elles sont donc ecrites en RVB et pas en hexadecimal, pour qu'on voie
# du premier coup d'oeil que ce sont des canaux et non des teintes, et
# elles ne servent QUE dans les deux schemas ci-dessous. Elles n'ont
# rien a faire dans le reste du fichier, ni dans la charte du site.
PRIMAIRES_LUMIERE = [("R", (255, 0, 0)), ("V", (0, 255, 0)), ("B", (0, 0, 255))]
PRIMAIRES_ENCRE = [("C", (0, 174, 239)), ("M", (236, 0, 140)),
                   ("J", (255, 241, 0)), ("N", (35, 31, 32))]


def _synthese(p, x, y, cote, additive=True):
    """Les primaires qui se superposent, melangees pour de vrai.

    Les recouvrements ne sont PAS dessines a la main : chaque disque est
    pose sur son propre calque, et les calques sont combines par le
    melange qui correspond au procede — addition pour la lumiere,
    multiplication pour l'encre. Le blanc au centre du schema RVB et le
    presque-noir du schema CMJ sont donc calcules, pas decides. Un
    schema de synthese dont on choisit les intersections ne demontre
    rien du tout.
    """
    from PIL import ImageChops
    cote = int(cote)
    fond = (0, 0, 0) if additive else (255, 255, 255)
    melange = Image.new("RGB", (cote, cote), fond)
    primaires = PRIMAIRES_LUMIERE if additive else PRIMAIRES_ENCRE[:3]
    r = cote * 0.30
    centres = [(cote * 0.50, cote * 0.36),
               (cote * 0.36, cote * 0.60),
               (cote * 0.64, cote * 0.60)]
    for (nom, rvb), (cx, cy) in zip(primaires, centres):
        calque = Image.new("RGB", (cote, cote), fond)
        ImageDraw.Draw(calque).ellipse([cx - r, cy - r, cx + r, cy + r],
                                       fill=rvb)
        melange = (ImageChops.add(melange, calque) if additive
                   else ImageChops.multiply(melange, calque))
    p.im.paste(melange, (int(x), int(y)))
    p._redessiner()
    p.d.rectangle([x, y, x + cote, y + cote],
                  outline=_melange("taupe", "creme", 0.4), width=3)
    f = police(800, max(20, int(cote * 0.075)))
    for (nom, _), (cx, cy) in zip(primaires, centres):
        dx = (cx - cote / 2) * 1.75
        dy = (cy - cote * 0.52) * 1.75
        tx, ty = x + cote / 2 + dx, y + cote * 0.52 + dy
        p.d.text((tx - p.d.textlength(nom, font=f) / 2, ty - f.size * 0.6),
                 nom, font=f, fill=teinte("blanc" if additive else "encre"))
    return p


def _hors_gamme(rvb, force=0.30):
    """Ce que devient une couleur d'ecran passee en encre — approche.

    Ce n'est PAS une conversion colorimetrique : il n'y a ni profil ni
    moteur ICC ici, et pretendre le contraire serait malhonnete. C'est
    une approximation volontairement simple — on rapproche la teinte de
    son gris et on l'assombrit un peu — qui reproduit ce qu'on constate
    sur un bleu electrique imprime en quadri : il perd son eclat avant
    de perdre sa teinte. La legende de la publication ne promet rien de
    plus que ce constat.
    """
    gris = sum(rvb) / 3
    return tuple(int(c + (gris - c) * force * 1.6) * 90 // 100 for c in rvb)


@pose(flou=24, force=86, bas=18, cote=7)
def _ecran(p, cx, cy, larg, couleur):
    """Un moniteur, son pied, et un aplat de couleur dedans."""
    p._place(cy - larg * 0.31, "écran")
    haut = larg * 0.62
    p.d.rounded_rectangle([cx - larg / 2, cy - haut / 2, cx + larg / 2,
                           cy + haut / 2], radius=int(larg * 0.035),
                          fill=_melange("encre", "brun", 0.25))
    m = larg * 0.035
    p.d.rectangle([cx - larg / 2 + m, cy - haut / 2 + m,
                   cx + larg / 2 - m, cy + haut / 2 - m * 1.6], fill=couleur)
    p.d.rectangle([cx - larg * 0.07, cy + haut / 2, cx + larg * 0.07,
                   cy + haut / 2 + larg * 0.10],
                  fill=_melange("encre", "brun", 0.35))
    p.d.rounded_rectangle([cx - larg * 0.22, cy + haut / 2 + larg * 0.09,
                           cx + larg * 0.22, cy + haut / 2 + larg * 0.14],
                          radius=8, fill=_melange("encre", "brun", 0.35))
    # La dalle est du verre : sans sa bande spéculaire, elle se lit
    # comme un rectangle de couleur, ce qui est précisément le défaut
    # que la publication dénonce — on croit voir la couleur, on voit un
    # écran. Faible, parce qu'un écran allumé réfléchit peu.
    _reflet_verre(p, (cx - larg / 2 + m, cy - haut / 2 + m,
                      cx + larg / 2 - m, cy + haut / 2 - m * 1.6),
                  force=30, largeur=0.30, angle=-18)
    return p


@pose(flou=16, force=72, bas=11, cote=5)
def _feuille_imprimee(p, cx, cy, larg, couleur, angle=-4):
    """La meme couleur, posee sur du papier."""
    haut = larg * 0.70
    im = Image.new("RGBA", (int(larg), int(haut)), teinte("blanc") + "ff")
    d = ImageDraw.Draw(im)
    m = larg * 0.09
    d.rectangle([m, m, larg - m, haut - m], fill=couleur)
    sil = Image.new("RGBA", im.size, (0, 0, 0, 70)).rotate(
        angle, expand=True, resample=Image.BICUBIC)
    marge = 60
    fo = Image.new("RGBA", (sil.width + 2 * marge, sil.height + 2 * marge),
                   (0, 0, 0, 0))
    fo.paste(sil, (marge, marge))
    fo = fo.filter(ImageFilter.GaussianBlur(20))
    p.im.paste(fo, (int(cx - fo.width / 2), int(cy - fo.height / 2 + 10)), fo)
    t = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    p.im.paste(t, (int(cx - t.width / 2), int(cy - t.height / 2)), t)
    p._redessiner()
    return p


@pose(flou=16, force=70, bas=10, cote=5)
def _papier_rendu(p, x, y, larg, haut, couleur, couche, legende):
    """Le meme aplat sur un mat et sur un couche brillant.

    Le mat absorbe : la couleur est legerement rabattue et le grain du
    papier se voit. Le couche renvoie : la couleur reste saturee et une
    bande de lumiere traverse l'aplat. Les deux partent de la MEME
    valeur d'encre — c'est ce que la voix off affirme.
    """
    if couche:
        p.d.rectangle([x, y, x + larg, y + haut], fill=couleur)
        bande = Image.new("RGBA", (int(larg), int(haut)), (0, 0, 0, 0))
        ImageDraw.Draw(bande).polygon(
            [(larg * 0.10, haut), (larg * 0.42, 0), (larg * 0.62, 0),
             (larg * 0.30, haut)], fill=teinte("blanc") + "4e")
        bande = bande.filter(ImageFilter.GaussianBlur(int(larg * 0.035)))
        p.im = Image.alpha_composite(
            p.im.convert("RGBA"),
            Image.new("RGBA", p.im.size, (0, 0, 0, 0))).convert("RGB")
        p.im.paste(bande, (int(x), int(y)), bande)
        p._redessiner()
    else:
        # le mat absorbe : la couleur est rabattue vers le gris du
        # papier, et le grain de la fibre casse l'aplat. L'ecart avec le
        # couche doit se voir en vignette, sinon la planche ne demontre
        # rien — c'est tout ce qu'on lui demande.
        mat = tuple(int(c + (196 - c) * 0.26) for c in couleur)
        p.d.rectangle([x, y, x + larg, y + haut], fill=mat)
        import random
        al = random.Random(4)
        clair = tuple(min(255, c + 30) for c in mat)
        sombre = tuple(max(0, c - 22) for c in mat)
        for _ in range(int(larg * haut / 90)):
            gx = al.uniform(x + 3, x + larg - 3)
            gy = al.uniform(y + 3, y + haut - 3)
            r = al.choice((1, 1, 2))
            p.d.ellipse([gx - r, gy - r, gx + r, gy + r],
                        fill=clair if al.random() > 0.45 else sombre)
    p.d.rectangle([x, y, x + larg, y + haut],
                  outline=_melange("taupe", "creme", 0.4), width=3)
    f = police(600, max(20, int(larg * 0.085)))
    p.d.text((x + larg / 2 - p.d.textlength(legende, font=f) / 2,
              y + haut + 18), legende, font=f, fill=teinte("brun"))
    return p


def pub04_reel_cmjn(dossier=None):
    """n° 4, vendredi 23 octobre — pourquoi ce n'est jamais la meme couleur.

    Remplace les fiches de tournage par cinq ecrans finis. C'est la
    publication du cycle ou le dessin est le plus clairement SUPERIEUR
    au tournage : la synthese additive et la synthese soustractive sont
    des schemas, pas des scenes. Elles se filment mal, elles se
    dessinent bien — et ici elles ne sont meme pas dessinees, elles sont
    CALCULEES : les recouvrements sortent d'une addition et d'une
    multiplication de calques.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-06-reel-cmjn"))
    accent("turquoise")
    faits = []
    vif = (53, 169, 221)                     # le bleu vif de la charte
    terne = _hors_gamme(vif)

    p = Planche("sable_chaud", LARGE_S, HAUT_S)
    p.surtitre("Reel · 0-3 s", "taupe", y=190)
    p.filet()
    p.titre("Pourquoi ce n'est\njamais la même\ncouleur.", 76, y=260)
    _ecran(p, p.l / 2, 880, 600, vif)
    _feuille_imprimee(p, p.l / 2, 1430, 440, terne)
    f = police(600, 32)
    for y, lib in ((1170, "à l'écran"), (1610, "imprimé")):
        p.d.text((p.l / 2 - p.d.textlength(lib, font=f) / 2, y), lib,
                 font=f, fill=teinte("taupe"))
    p.y = 1660
    p.texte("Vous validez un bleu éclatant à l'écran. Vous recevez "
            "l'impression.", 40, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran1.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("3-9 s", "taupe", y=190)
    p.titre("RVB : de la lumière.", 100, y=260)
    _synthese(p, 140, 620, 800, additive=True)
    p.y = 1520
    p.texte("Un écran fabrique les couleurs avec de la lumière. Il "
            "additionne du rouge, du vert et du bleu. Plus il en met, plus "
            "c'est lumineux — au centre, c'est blanc.", 40, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran2.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("9-15 s", "taupe", y=190)
    p.titre("CMJN : de l'encre.", 100, y=260)
    _synthese(p, 140, 620, 800, additive=False)
    p.y = 1520
    p.texte("Une imprimante fait l'inverse. Elle dépose de l'encre sur du "
            "papier blanc, et chaque couche retire de la lumière — au "
            "centre, c'est presque noir.", 40, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran3.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("15-20 s", "taupe", y=190)
    p.titre("Le papier\nchange tout.", 104, y=260)
    _papier_rendu(p, 90, 760, 420, 420, vif, False, "mat")
    _papier_rendu(p, 570, 760, 420, 420, vif, True, "couché brillant")
    p.y = 1340
    p.texte("La même encre, deux papiers. Un mat absorbe et adoucit. Un "
            "couché renvoie et sature. Le même fichier donne deux "
            "résultats.", 40, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran4.png"))

    p = Planche("encre", LARGE_S, HAUT_S)
    _ecran(p, 330, 620, 400, vif)
    _feuille_imprimee(p, 760, 640, 340, terne, angle=5)
    p.y = 1000
    p.filet()
    p.titre("Demandez un BAT.\nToujours.", 98, "blanc")
    p.y += 30
    p.texte("Ne validez jamais une couleur sur un écran. Un bon à tirer, "
            "c'est gratuit, et ça évite de tout refaire.", 40, "creme", 400,
            avant=20)
    p.abonnement("sable")
    p.signature("sable")
    faits.append(p.ecrire(d / "ecran5.png"))
    return faits


# ---------------------------------------------------------------------
# Orange et noir — n° 8.
# ---------------------------------------------------------------------
# C'est le plan 9-15 s qui rendait ce reel difficile : « images rapides,
# panneau de danger, ruban de chantier, guepe, signalisation routiere ».
# Trouvees sur internet, elles sont interdites par la ligne editoriale.
# Filmees, elles demandent une sortie. Generees, c'est la meme
# interdiction. Dessinees, elles sont a la fois libres de droits et plus
# justes : ce que la publication montre n'est pas UN panneau, c'est le
# CODE commun a quatre objets qui n'ont rien a voir entre eux. Un
# pictogramme le dit mieux qu'une photographie, qui porterait en plus
# une marque, une rue, une meteo dont on n'a que faire.

def _ruban_chantier(p, x, y, larg, haut, pas=None):
    """Un ruban de chantier : des bandes a 45 degres, orange et noir."""
    pas = pas or max(28, int(haut * 0.52))
    p.d.rectangle([x, y, x + larg, y + haut], fill=teinte("orange"))
    bande = Image.new("RGB", (int(larg), int(haut)), teinte("orange"))
    db = ImageDraw.Draw(bande)
    for i in range(-int(haut), int(larg) + int(haut), pas * 2):
        db.polygon([(i, haut), (i + pas, haut), (i + pas + haut, 0), (i + haut, 0)],
                   fill=teinte("encre"))
    p.im.paste(bande, (int(x), int(y)))
    p._redessiner()
    return p


def _panneau_danger(p, cx, cy, cote):
    """Le triangle de danger : noir sur orange, point d'exclamation trace."""
    h = cote * 0.87
    r = cote * 0.07
    p.d.polygon([(cx, cy - h / 2), (cx - cote / 2, cy + h / 2),
                 (cx + cote / 2, cy + h / 2)], fill=teinte("orange"))
    p.d.polygon([(cx, cy - h / 2 + r * 1.9), (cx - cote / 2 + r * 2.2, cy + h / 2 - r),
                 (cx + cote / 2 - r * 2.2, cy + h / 2 - r)],
                outline=teinte("encre"), width=max(5, int(cote * 0.055)))
    # le point d'exclamation : trace, pas ecrit — aucune fonte en jeu
    l = max(6, int(cote * 0.075))
    p.d.polygon([(cx - l, cy - cote * 0.12), (cx + l, cy - cote * 0.12),
                 (cx + l * 0.6, cy + cote * 0.16),
                 (cx - l * 0.6, cy + cote * 0.16)], fill=teinte("encre"))
    p.d.ellipse([cx - l, cy + cote * 0.24, cx + l, cy + cote * 0.24 + l * 2],
                fill=teinte("encre"))
    return p


def _guepe(p, cx, cy, larg):
    """Une guepe, de dessus : tete et thorax noirs, abdomen raye.

    Trois cents millions d'annees avant la signalisation routiere, le
    meme message avec les memes deux couleurs. C'est tout l'argument de
    la publication, et il tient dans cette silhouette.
    """
    ha = larg * 0.34
    ep = max(3, int(larg * 0.012))
    # les ailes d'abord, pour qu'elles passent sous le corps
    for s in (-1, 1):
        aile = Image.new("RGBA", (int(larg * 0.32), int(ha * 0.26)),
                         (0, 0, 0, 0))
        ImageDraw.Draw(aile).ellipse(
            [0, 0, aile.width - 1, aile.height - 1],
            fill=teinte("blanc") + "9a",
            outline=_melange("taupe", "brun", 0.25), width=2)
        aile = aile.rotate(s * 16, expand=True, resample=Image.BICUBIC)
        p.im.paste(aile, (int(cx - larg * 0.16),
                          int(cy + s * ha * 0.52 - aile.height / 2)), aile)
    p._redessiner()
    # tete et thorax
    p.d.ellipse([cx - larg * 0.46, cy - ha * 0.26,
                 cx - larg * 0.28, cy + ha * 0.26], fill=teinte("encre"))
    p.d.ellipse([cx - larg * 0.30, cy - ha * 0.34,
                 cx - larg * 0.04, cy + ha * 0.34], fill=teinte("encre"))
    # l'abdomen raye : c'est lui, le signal
    al, ah = int(larg * 0.52), int(ha * 0.72)
    abd = Image.new("RGBA", (al, ah), (0, 0, 0, 0))
    da = ImageDraw.Draw(abd)
    da.ellipse([0, 0, al - 1, ah - 1], fill=teinte("orange"))
    for k in range(4):
        da.rectangle([al * (0.10 + k * 0.21), 0, al * (0.20 + k * 0.21), ah],
                     fill=teinte("encre"))
    masque = Image.new("L", abd.size, 0)
    ImageDraw.Draw(masque).ellipse([0, 0, al - 1, ah - 1], fill=255)
    abd.putalpha(masque)
    p.im.paste(abd, (int(cx - larg * 0.06), int(cy - ah / 2)), abd)
    p._redessiner()
    # les antennes
    for s in (-1, 1):
        p.d.line([(cx - larg * 0.42, cy + s * ha * 0.14),
                  (cx - larg * 0.58, cy + s * ha * 0.50)],
                 fill=teinte("encre"), width=ep)
    return p


def _batracien(p, cx, cy, larg):
    """Une salamandre, tachee d'orange sur noir. Meme code, autre regne."""
    h = larg * 0.30
    p.d.ellipse([cx - larg * 0.42, cy - h * 0.46, cx + larg * 0.30, cy + h * 0.46],
                fill=teinte("encre"))
    p.d.polygon([(cx + larg * 0.26, cy - h * 0.20), (cx + larg * 0.50, cy),
                 (cx + larg * 0.26, cy + h * 0.20)], fill=teinte("encre"))
    for gx, gy, gr in ((-0.26, -0.12, 0.085), (-0.06, 0.10, 0.070),
                       (0.10, -0.14, 0.060), (-0.34, 0.14, 0.055)):
        p.d.ellipse([cx + larg * gx - larg * gr, cy + h * gy - larg * gr,
                     cx + larg * gx + larg * gr, cy + h * gy + larg * gr],
                    fill=teinte("orange"))
    for s in (-1, 1):
        for dx in (-0.30, 0.08):
            p.d.line([(cx + larg * dx, cy + s * h * 0.30),
                      (cx + larg * (dx - 0.06), cy + s * h * 0.78)],
                     fill=teinte("encre"), width=max(4, int(larg * 0.022)))
    return p


def _citrouille(p, cx, cy, larg):
    """Une citrouille, sur fond noir."""
    h = larg * 0.84
    for i, (dx, l) in enumerate(((0.0, 1.0), (-0.26, 0.74), (0.26, 0.74),
                                 (-0.44, 0.46), (0.44, 0.46))):
        c = teinte("orange") if i == 0 else _melange("orange", "encre",
                                                     0.10 + 0.06 * (i > 2))
        p.d.ellipse([cx + larg * dx - larg * l / 2, cy - h / 2,
                     cx + larg * dx + larg * l / 2, cy + h / 2], fill=c)
    p.d.ellipse([cx - larg * 0.50, cy - h / 2, cx + larg * 0.50, cy + h / 2],
                outline=_melange("orange", "encre", 0.35), width=5)
    # la queue
    p.d.rounded_rectangle([cx - larg * 0.045, cy - h / 2 - larg * 0.17,
                           cx + larg * 0.045, cy - h / 2 + larg * 0.04],
                          radius=int(larg * 0.03),
                          fill=_melange("brun", "encre", 0.30))
    return p


def pub08_reel_halloween(dossier=None):
    """n° 8, vendredi 30 octobre — pourquoi Halloween est orange et noir.

    Remplace les fiches de tournage par cinq ecrans finis. Le plan
    9-15 s etait le seul du cycle a porter un avertissement explicite —
    « pas de photo trouvee sur internet » — avec, pour seule porte de
    sortie, un prompt d'image generee. Les deux options tombaient sous
    la meme regle. Dessines, les quatre objets sont libres de droits, et
    la demonstration gagne : ce qu'on montre n'est pas un panneau, c'est
    le CODE commun a quatre choses qui n'ont rien a voir entre elles.
    Une photographie porterait en plus une marque, une rue, une meteo
    dont le sujet n'a que faire.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-10-30-reel-halloween"))
    accent("orange")
    faits = []

    p = Planche("encre", LARGE_S, HAUT_S)
    p.surtitre("Reel · 0-3 s", "orange", y=200)
    p.filet()
    p.titre("Pourquoi Halloween\nest orange\net noir.", 96, "blanc", y=280)
    _citrouille(p, p.l / 2, 1130, 620)
    p.y = 1560
    p.texte("Orange et noir. Pourquoi ces deux couleurs, et pas d'autres ?",
            42, "creme", 400, avant=0)
    p.signature("sable")
    faits.append(p.ecrire(d / "ecran1.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("3-9 s", "taupe", y=190)
    p.titre("Le contraste\nmaximal.", 110, y=260)
    # la demonstration : le meme mot sur les deux aplats, dans l'autre
    # couleur. Si on trichait sur l'un des deux, elle ne vaudrait rien.
    f = police(800, 92)
    for i, (fond, texte_c) in enumerate((("encre", "orange"),
                                         ("orange", "encre"))):
        y0 = 620 + i * 330
        p.d.rectangle([90, y0, 990, y0 + 290], fill=teinte(fond))
        l = p.d.textlength("ATTENTION", font=f)
        p.d.text((540 - l / 2, y0 + 95), "ATTENTION", font=f,
                 fill=teinte(texte_c))
    p.y = 1340
    p.texte("C'est l'un des contrastes les plus violents que l'œil humain "
            "sache traiter. On le repère avant même d'avoir compris ce "
            "qu'on regarde.", 42, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran2.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("9-15 s", "taupe", y=190)
    p.titre("La nature\nl'utilise déjà.", 104, y=260)
    _ruban_chantier(p, 90, 640, 420, 300)
    _panneau_danger(p, 780, 790, 330)
    _guepe(p, 300, 1120, 420)
    _batracien(p, 760, 1120, 400)
    f = police(600, 30)
    for cx, y, lib in ((300, 970, "ruban de chantier"), (780, 970, "panneau"),
                       (300, 1300, "guêpe"), (760, 1300, "salamandre")):
        p.d.text((cx - p.d.textlength(lib, font=f) / 2, y), lib, font=f,
                 fill=teinte("taupe"))
    p.y = 1420
    p.texte("La nature s'en sert pour dire « attention ». La signalisation "
            "aussi. Halloween n'a rien inventé : elle a emprunté le code "
            "de l'alerte.", 42, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran3.png"))

    p = Planche("creme", LARGE_S, HAUT_S)
    p.surtitre("15-19 s", "taupe", y=190)
    p.titre("Et pour\nvotre commerce ?", 84, y=250)
    _vitrine(p, 90, 700, 900, 410, eclairee=True, enseigne="VOTRE NOM")
    _vitrine(p, 90, 1160, 900, 420, eclairee=True, enseigne="VOTRE NOM",
             bandeau=0.46, couleur_decor="orange", decor="citrouilles",
             opacite_decor=0xf2)
    f = police(600, 32)
    for y, lib in ((1118, "toute l'année"), (1598, "en octobre")):
        p.d.text((90, y), lib, font=f, fill=teinte("taupe"))
    p.y = 1660
    p.texte("Il attire l'œil, mais il crie. Pour une vitrine saisonnière, "
            "c'est parfait.", 38, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "ecran4.png"))

    p = Planche("violet", LARGE_S, HAUT_S)
    p.filet(y=740)
    p.titre("Une couleur\nn'est jamais\nneutre.", 112, "blanc")
    p.y += 40
    p.texte("Elle dit quelque chose avant vous — et parfois autre chose que "
            "ce que vous vouliez dire.", 42, "creme", 400, avant=20)
    p.abonnement("sable")
    p.signature("creme")
    faits.append(p.ecrire(d / "ecran5.png"))
    return faits


def main():
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--exemple", action="store_true",
                   help="produire le carrousel du 12 octobre")
    a.add_argument("--liste", action="store_true", help="les gabarits connus")
    a.add_argument("--tout", action="store_true", help="produire tout le cycle")
    args = a.parse_args()

    if args.liste:
        for k in GABARITS:
            print(" ", k)
        return
    if args.tout:
        total = 0
        for nom, fn in GABARITS.items():
            faits = fn()
            total += len(faits)
            print("%-26s %2d planches" % (nom, len(faits)))
        print("\n%d visuels produits dans %s" % (total, SORTIE))
        if RESIDU:
            pire = min(r for _, r, _, _ in RESIDU)
            print("\n%d texte(s) sous le seuil de contraste, du plus "
                  "faible %.2f:1 au plus proche %.2f:1."
                  % (len(RESIDU), pire, max(r for _, r, _, _ in RESIDU)))
            print("Ce sont des légendes courtes posées SUR un objet "
                  "dessiné — « 3 mm » sur un échantillon d'alu, « 2026 » "
                  "sur une page de calendrier. L'encre y est déjà allée "
                  "au bout de la charte ; aller plus loin voudrait dire "
                  "changer la couleur de l'objet, qui porte un sens.")
        elif os.environ.get("GRAFYCOM_CONTRASTE"):
            print("\nContraste : aucun texte sous le seuil.")
        return
    if args.exemple:
        for f in carrousel_couleurs():
            im = Image.open(f)
            print("%-52s %sx%s" % (f, im.size[0], im.size[1]))
        return
    a.print_help()


# Les deux gabarits ci-dessous sont definis apres le registre : on les
# y ajoute ici, sinon --liste et --tout les ignorent en silence.

@pose(flou=14, force=66, bas=9, cote=4)
def _etiquette_ronde(p, cx, cy, r, mot=None, couleur="violet"):
    """Une etiquette ronde, du diametre qu'on lui donne.

    Elle sert deux fois dans la n° 15 bis : minuscule a l'echelle du
    reel, puis grande pour montrer ce qui y tient. C'est le meme
    dessin aux deux tailles, ce qui est precisement le propos.
    """
    p.d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=teinte("blanc"),
                outline=_melange(couleur, "blanc", 0.5), width=max(2, r // 22))
    # la marque : un disque plein, le seul element qui survit a 3 cm
    p.d.ellipse([cx - r * 0.34, cy - r * 0.34, cx + r * 0.34, cy + r * 0.34],
                fill=teinte(couleur))
    if mot:
        _bloc(p, cx - r, cy + r * 0.44, mot, max(11, int(r * 0.22)),
              "brun", 600, r * 2, centre=True)


def _regle(p, x0, x1, y, mesure):
    """Une reglette cotee. Sans elle, « 3 cm » n'est qu'un mot."""
    gris = _melange("taupe", "blanc", 0.35)
    p.d.line([(x0, y), (x1, y)], fill=gris, width=3)
    for x in (x0, x1):
        p.d.line([(x, y - 12), (x, y + 12)], fill=gris, width=3)
    _bloc(p, x0, y + 24, mesure, 28, "taupe", 400, x1 - x0, centre=True)


def pub15bis_quatre_supports(dossier=None):
    """n° 15 bis, samedi 21 novembre — un visuel, quatre supports.

    Arbitrage n° 3 de A-FAIRE-APRES-RELECTURE.md. Le creneau du 21 se
    libere quand le reel n° 16 part au 28 ; cette publication le
    reprend, avec l'angle qui manquait au cycle.

    Elle ne redit pas la n° 17. Le carrousel du 23 parle de LOGISTIQUE
    — meme imprimeur, meme delai, un seul fichier. Celle-ci parle de
    DESSIN : le meme visuel ne s'agrandit pas d'un support a l'autre,
    il se redessine. Deux sujets voisins, deux demonstrations
    differentes, et celle-ci vient d'abord parce qu'on decide quoi
    imprimer avant de decider quand.

    Creneau du samedi : on regarde, on ne lit plus. D'ou des planches
    tenues par l'objet, avec des legendes courtes.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-21-quatre-supports"))
    accent("violet")
    faits = []

    p = Planche("creme")
    p.surtitre("Conseil", y=200)
    p.filet()
    p.titre("Un visuel.\nQuatre supports.\nQuatre dessins.", 72)
    p.y = 760
    p.texte("Le même décor de fêtes doit tenir sur une étiquette de "
            "3 cm et sur une vitrine de 2 m. Ce n'est pas la même "
            "image agrandie quatre fois.", 40, "brun", 400, avant=0)
    _etiquette_ronde(p, 270, 1080, 56, couleur="violet")
    _etiquette_ronde(p, 520, 1080, 92, couleur="violet")
    _etiquette_ronde(p, 830, 1080, 128, couleur="violet")
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("blanc")
    p.titre("L'étiquette fait\n3 cm.", 80, y=150)
    _etiquette_ronde(p, 540, 640, 150, couleur="violet")
    _regle(p, 390, 690, 850, "3 cm")
    p.y = 960
    p.texte("À cette taille, un seul élément survit : la marque. Le "
            "slogan, les vœux, l'adresse du site — tout cela devient "
            "du gris. On ne les réduit pas, on les retire.", 38, "brun",
            400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "02.png"))

    p = Planche("creme")
    p.titre("Le sachet se lit\nà un mètre.", 76, y=150)
    _sachet(p, 540, 500, 360, 450, couleur="violet")
    p.y = 1030
    p.texte("Un mètre, c'est la distance du comptoir. La marque peut "
            "s'accompagner d'une ligne — pas de trois.", 38, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("blanc")
    p.titre("La carte est le seul\nendroit où le texte\nrespire.", 64,
            y=150)
    _carte(p, 540, 740, 420, 540, -4, gaufre=True, texte="Bonne année")
    p.y = 1070
    p.texte("On la tient à trente centimètres. C'est le seul support où "
            "les vœux ont leur place.", 38, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "04.png"))

    p = Planche("creme")
    p.titre("La vitrine se lit\ndu trottoir d'en face.", 66, y=150)
    _vitrine(p, 150, 500, 780, 440, decor="flocons", bandeau=0.30,
             couleur_decor="violet", eclairee=True, enseigne="VOTRE NOM")
    p.y = 1010
    p.texte("Huit mètres de recul. La marque grossit, le reste "
            "disparaît, et le décor ne doit pas manger la moitié du "
            "verre : on regarde à travers une vitrine.", 38, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "05.png"))

    p = Planche("blanc")
    p.titre("Le même visuel,\nquatre fois dessiné.", 66, y=150)
    _etiquette_ronde(p, 180, 700, 46, couleur="violet")
    _sachet(p, 400, 560, 150, 190, couleur="violet")
    _carte(p, 620, 660, 140, 180, -4, gaufre=True)
    # la marque violette sur la carte aussi : sans elle, a cette taille,
    # la carte est le seul des quatre objets qui ne porte rien.
    p.d.ellipse([620 - 15, 655 - 15, 620 + 15, 655 + 15],
                fill=teinte("violet"))
    _vitrine(p, 760, 580, 190, 150, decor="flocons", bandeau=0.30,
             couleur_decor="violet", eclairee=True)
    for x, mot in ((180, "3 cm"), (400, "18 cm"), (620, "15 cm"),
                   (855, "2 m")):
        _bloc(p, x - 80, 800, mot, 30, "taupe", 400, 160, centre=True)
    p.y = 900
    p.texte("Quatre échelles, quatre compositions, une seule marque. "
            "C'est ce qui fait qu'on les reconnaît ensemble sans "
            "qu'aucun ne soit l'agrandissement de l'autre.", 38, "brun",
            400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "06.png"))

    p = Planche("encre")
    p.filet()
    p.titre("Un visuel qu'on agrandit\nse voit.\nUn visuel qu'on redessine\nse lit.", 58, y=420)
    p.signature("sable")
    faits.append(p.ecrire(d / "07.png"))

    return faits

GABARITS["solaire-66"] = solaire_66
GABARITS["logo-reduction"] = pub09_logo_reduction

# Les huit publications redessinees. Elles sont enregistrees ICI, et pas
# dans le dictionnaire plus haut, pour la meme raison que les deux
# precedentes : elles sont definies apres lui. Une fonction ajoutee au
# dictionnaire avant d'exister leve une NameError ; une fonction oubliee
# du dictionnaire ne leve rien du tout et ne sort jamais — c'est arrive
# a solaire-66 et a logo-reduction, qui etaient restes muets.
GABARITS["enseigne-hiver"] = pub10_enseigne_hiver
GABARITS["reel-vitrophanie"] = pub12_reel_vitrophanie
GABARITS["francais-devanture"] = pub14_francais_devanture
GABARITS["quiz-matieres"] = pub15_quiz_matieres
GABARITS["quatre-supports"] = pub15bis_quatre_supports
GABARITS["reel-fin-annee"] = pub16_reel_fin_annee
GABARITS["emballage-tri"] = pub18_emballage_tri
GABARITS["vitrine-trottoir"] = pub21_vitrine_trottoir
GABARITS["sticker-enseigne"] = pub22_sticker_enseigne
GABARITS["reel-matieres"] = pub20_reel_matieres
# ---------------------------------------------------------------------
# n° 25, samedi 7 novembre — BIG FOOD. Pilier « réalisations ».
#
# Accord du client donné le 22 octobre. Sandra a fait LE LOGO, et rien
# d'autre : pas d'enseigne, pas de pose, pas de support. La taille du
# plan de travail du fichier (2 800 mm) m'avait fait écrire le
# contraire — un plan de travail dit comment un fichier a été réglé,
# jamais ce qu'on en a fait.
# ---------------------------------------------------------------------
def _couleurs_big_food():
    """Les trois couleurs du logo, relevées DANS le fichier.

    Pas écrites en dur : une couleur client recopiée dérive comme une
    autre, et `charte.py --verifier` aurait raison de signaler un
    hexadécimal de plus dans le source. Ici le fichier est la source,
    et il ne peut pas se tromper sur lui-même.
    """
    import collections
    f = SOURCES / "clients" / "big-food.png"
    if not f.exists():
        return None
    im = Image.open(f).convert("RGB").resize((400, 100))
    freq = collections.Counter(im.getdata()).most_common(12)
    fond = freq[0][0]
    # l'orange : le plus sature des aplats restants
    def sat(c):
        return (max(c) - min(c)) / max(1, max(c))
    chauds = [c for c, _ in freq[1:]
              if c[0] > c[2] + 40 and sat(c) > 0.55]
    return {"fond": "#%02x%02x%02x" % fond,
            "orange": "#%02x%02x%02x" % (chauds[0] if chauds else (243, 146, 0)),
            "blanc": "#ffffff"}


def pub25_big_food(dossier=None):
    """n° 25, samedi 7 novembre — pourquoi les deux O sont des burgers."""
    d = pathlib.Path(dossier or (SORTIE / "2026-11-07-big-food"))
    accent("orange")
    L = SOURCES / "clients" / "big-food.png"
    C_BF = _couleurs_big_food()
    faits = []

    p = Planche("creme")
    p.surtitre("Réalisation", y=200)
    p.filet()
    p.titre("Pourquoi les deux O\nsont des burgers.", 68)
    p.poser(L, 540, 760, 900, ombre=30)
    p.y = 1000
    p.texte("BIG FOOD — logo, avec l'accord du client.", 32, "taupe", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    # Le logo en grand, sur son propre fond. C'est la seule planche du
    # cycle ou un aplat non charte occupe toute la page, et c'est
    # normal : c'est la couleur du client, pas celle de Grafycom.
    p = Planche("creme")
    if C_BF:
        p.d.rectangle([0, 0, p.l, p.h], fill=C_BF["fond"])
        p._redessiner()
        p.sombre = True
    else:
        p.images_absentes = ["big-food.png"]
    p.poser(L, 540, 640, 980, ombre=0)
    p.y = 980
    p.texte("Trois couleurs. Une seule lettre en couleur.", 42, "blanc", 600,
            avant=0)
    p.signature("blanc")
    faits.append(p.ecrire(d / "02.png"))

    p = Planche("blanc")
    p.titre("Un symbole posé à côté\nd'un nom peut s'en aller.", 58, y=150)
    _deux_mots(p, 500)
    p.y = 980
    p.texte("Devenu une lettre, il ne peut plus partir sans emporter le "
            "mot. C'est le même principe que le O de Solaire 66.", 38,
            "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("sable_chaud")
    p.titre("Une seule lettre\nen couleur.", 78, y=160)
    p.poser(L, 540, 620, 880, ombre=24)
    p.y = 880
    p.texte("Le B, et pas le mot entier. Une couleur qui touche tout ne "
            "désigne plus rien : elle devient le fond. Posée sur un seul "
            "caractère, elle donne un point d'entrée à l'œil.", 38, "brun",
            400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "04.png"))

    # Les deux compositions. La deux lignes n'existe qu'en capture
    # d'écran, 356 px de large : elle est posée à sa taille native,
    # jamais agrandie. Une image molle sur une planche qui parle de
    # netteté se verrait. Le .ai reste demandé pour les grands usages.
    p = Planche("blanc")
    p.titre("Deux compositions,\nun seul logo.", 64, y=150)
    p.poser(L, 540, 560, 740, ombre=22)
    p.poser(SOURCES / "clients" / "big-food-2lignes.png", 540, 850, 356,
            ombre=22)
    p.y = 1040
    p.texte("Une ligne quand la place est large — une devanture, un "
            "bandeau. Deux lignes quand elle est courte — un avatar, un "
            "tampon. Le même dessin, pas un redessin.", 34, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "05.png"))

    p = Planche("creme")
    p.titre("Ce qui disparaît\nen premier.", 80, y=150)
    _reduction_logo(p, L, 470)
    p.y = 1030
    p.texte("À la taille d'un favicon, les garnitures des burgers se "
            "ferment et il reste deux disques. Le mot, lui, tient.", 36,
            "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "06.png"))

    p = Planche("encre")
    p.filet(y=330)
    p.titre("Un logo se dessine\npour être lu.", 72, "blanc")
    p.y = 820
    p.texte("Pas pour être admiré de près. Celui-ci se lit avant qu'on ait "
            "fini de passer devant.", 40, "creme", 400, avant=0)
    p.abonnement("sable")
    p.signature("sable")
    faits.append(p.ecrire(d / "07.png"))
    return faits


@pose(flou=14, force=58, bas=9, cote=4)
def _deux_mots(p, y):
    """« FOOD » avec le symbole à côté, puis le symbole DANS le mot.

    La démonstration de la n° 25. Les deux lignes portent exactement le
    même mot et le même symbole : seule leur relation change, et c'est
    la condition pour que la comparaison prouve quelque chose.
    """
    f = police(800, 120)
    for i, (lib, colle) in enumerate((("à côté", False), ("dedans", True))):
        yy = y + i * 230
        mot = "FOOD" if colle else "FOOD"
        lm = p.d.textlength(mot, font=f)
        x = (p.l - lm) / 2 + (0 if colle else 50)
        if colle:
            # le symbole prend la place des deux O
            p.d.text((x, yy), "F", font=f, fill=teinte("encre"))
            lF = p.d.textlength("F", font=f)
            lO = p.d.textlength("O", font=f)
            for k in range(2):
                cx = x + lF + lO * (k + 0.5)
                _burger(p, cx, yy + 62, lO * 0.92)
            p.d.text((x + lF + 2 * lO, yy), "D", font=f, fill=teinte("encre"))
        else:
            p.d.text((x - 90, yy), mot, font=f, fill=teinte("encre"))
            _burger(p, x + lm - 30, yy + 62, 104)
        fl = police(600, 30)
        t = lib
        p.d.text(((p.l - p.d.textlength(t, font=fl)) / 2, yy + 150), t,
                 font=fl, fill=teinte("taupe"))
    return p


def _burger(p, cx, cy, diam):
    """Un burger stylisé — le symbole de la démonstration, pas le logo.

    Le vrai burger du logo est une illustration détaillée ; la réduire
    à cette taille la rendrait illisible et, surtout, la publication
    compare ici une RELATION entre un mot et un symbole, pas deux
    dessins. Un symbole simple sert mieux la démonstration, et il ne
    prétend pas être le logo du client.
    """
    r = diam / 2
    p.d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=teinte("encre"))
    p.d.ellipse([cx - r * 0.74, cy - r * 0.74, cx + r * 0.74, cy + r * 0.74],
                fill=teinte("blanc"))
    p.d.rectangle([cx - r * 0.74, cy - r * 0.16, cx + r * 0.74, cy + r * 0.16],
                  fill=teinte("encre"))
    return p


@pose(flou=16, force=64, bas=10, cote=5)
def _reduction_logo(p, chemin, y):
    """Le même fichier à trois tailles, aligné sur son bas.

    Alignées sur leur milieu, les trois versions flotteraient ; la
    réduction se lit quand elles posent sur la même ligne.
    """
    if not pathlib.Path(chemin).exists():
        p.images_absentes = getattr(p, "images_absentes", [])
        p.images_absentes.append(pathlib.Path(chemin).name)
        return p
    # convert("RGB") d'office noircissait un logo detoure : KRUSTY est
    # livre sans fond. On compose donc sur le fond de la planche.
    im = Image.open(chemin)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        try:
            dessous = teinte(p.fond) + "ff"
        except SystemExit:          # un fond degrade n'a pas de teinte
            dessous = "#ffffffff"
        sous = Image.new("RGBA", im.size, dessous)
        im = Image.alpha_composite(sous, im).convert("RGB")
    else:
        im = im.convert("RGB")
    f = police(600, 28)
    x = MARGE
    sol = y + 320
    utile = p.l - 2 * MARGE
    ecart = 44
    parts = (0.62, 0.26, 0.12)
    tailles = [int((utile - 2 * ecart) * k) for k in parts]
    for larg, lib in zip(tailles, ("en grand", "sur une carte",
                                   "en favicon")):
        h = int(im.height * larg / im.width)
        p.im.paste(im.resize((larg, h), Image.LANCZOS), (int(x), int(sol - h)))
        p._redessiner()
        t = lib
        p.d.text((x + (larg - p.d.textlength(t, font=f)) / 2, sol + 18), t,
                 font=f, fill=teinte("taupe"))
        x += larg + ecart
    return p



def _couleurs_krusty():
    """Les couleurs du logo KRUSTY, relevées DANS le fichier.

    Meme principe que pour BIG FOOD : rien de recopie a la main. Le
    fichier est livre sans fond, on ne compte donc que les pixels
    opaques.
    """
    import collections
    f = SOURCES / "clients" / "krusty.png"
    if not f.exists():
        return None
    im = Image.open(f).convert("RGBA").resize((500, 400))
    freq = collections.Counter(px[:3] for px in im.getdata()
                               if px[3] > 200).most_common(8)
    def sat(c):
        return (max(c) - min(c)) / max(1, max(c))
    violets = [c for c, _ in freq if c[2] > c[1] + 30 and c[0] > c[1]]
    chauds = [c for c, _ in freq if c[0] > c[2] + 60 and sat(c) > 0.55]
    if not violets or not chauds:
        return None
    return {"violet": "#%02x%02x%02x" % violets[0],
            "orange": "#%02x%02x%02x" % chauds[0],
            "blanc": "#ffffff"}


def _bande_epreuve(p, x0, y0, x1, y1, clair, fonce):
    """Une bande tramée, claire à gauche et foncée à droite.

    Un seul fond ne demontre rien : un aplat blanc plein s'y lit tres
    bien. Il faut que le mot TRAVERSE une frontiere pour qu'on voie
    lequel des trois traitements survit aux deux cotes. La trame est
    de la meme famille que celle du client, mais rien de son travail
    n'est reproduit ici : c'est une demonstration.
    """
    mi = (x0 + x1) // 2
    p.d.rectangle([x0, y0, mi, y1], fill=clair)
    p.d.rectangle([mi, y0, x1, y1], fill=fonce)
    r, pas = 9, 34
    j = 0
    y = y0 + 14
    while y < y1 - 4:
        x = x0 + 14 + (pas // 2 if j % 2 else 0)
        while x < x1 - 4:
            p.d.ellipse([x - r, y - r, x + r, y + r],
                        fill=fonce if x < mi else clair)
            x += pas
        y += pas
        j += 1
    p._redessiner()
    return mi


def pub26_krusty(dossier=None):
    """n° 26, samedi 14 novembre — pourquoi les lettres sont creuses.

    Deuxieme realisation hors rythme, comme BIG FOOD, et pour la meme
    raison : une realisation s'ajoute au cycle, elle ne prend pas le
    creneau d'une lecon.

    Le sujet n'est pas celui de la n° 25. BIG FOOD remplacait deux
    lettres par des burgers ; KRUSTY ne remplace rien, il pose. Et
    surtout : ses lettres sont CREUSES, blanches cernees de violet.
    C'est ce qui les laisse vivre sur un fond charge comme sur un fond
    clair, la ou un aplat plein meurt sur l'un des deux.

    Ce qui est demontre planche 3 est DESSINE : un fond trame de la
    meme famille, pas le depliant du client. On montre un principe, on
    ne republie pas une piece dont la paternite n'est pas etablie.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-14-krusty"))
    accent("violet")
    L = SOURCES / "clients" / "krusty.png"
    C_K = _couleurs_krusty()
    faits = []

    p = Planche("creme")
    p.surtitre("Réalisation", y=200)
    p.filet()
    p.titre("Pourquoi les lettres\nsont creuses.", 68)
    p.poser(L, 540, 770, 630, ombre=26)
    p.y = 1070
    p.texte("KRUSTY — logo, avec l'accord du client.", 32, "taupe", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    # Le logo seul, en grand. Fond blanc : c'est ainsi que le fichier
    # est construit, sans fond, et le cerne violet y est a son aise.
    p = Planche("blanc")
    p.poser(L, 540, 620, 940, ombre=0)
    p.y = 1080
    if C_K:
        p.texte("Trois couleurs : le violet du cerne, l'orange du K, "
                "le blanc des lettres. Rien d'autre.", 38, "brun", 400,
                avant=0)
    else:
        p.images_absentes = ["krusty.png"]
    p.signature("brun")
    faits.append(p.ecrire(d / "02.png"))

    # La demonstration : le meme mot, trois traitements, un fond charge.
    p = Planche("creme")
    p.titre("Le même mot,\ntrois fois.", 76, y=150)
    if C_K:
        v = C_K["violet"]
        rv = tuple(int(v[i:i + 2], 16) for i in (1, 3, 5))
        clair = "#%02x%02x%02x" % tuple(int(c + (255 - c) * 0.62) for c in rv)
        x0, x1 = MARGE, p.l - MARGE
        f = police(800, 86)
        essais = [("plein blanc", "#ffffff", None),
                  ("plein violet", v, None),
                  ("creux, cerné", "#ffffff", v)]
        y = 460
        for lib, remplissage, cerne in essais:
            _bande_epreuve(p, x0, y, x1, y + 128, clair, v)
            # ECHANTILLONS : deux des trois sont illisibles exprès,
            # c'est la demonstration meme. Le correcteur de contraste
            # de _Dessin les reparerait et la detruirait, donc ils
            # passent par un calque, hors de son passage.
            calque = Image.new("RGBA", (x1 - x0, 128), (0, 0, 0, 0))
            dc = ImageDraw.Draw(calque)
            kw = {"font": f, "fill": remplissage}
            if cerne:
                kw["stroke_width"] = 7
                kw["stroke_fill"] = cerne
            dc.text((126, 16), "KRUSTY", **kw)
            p.im.paste(calque, (x0, y), calque)
            p._redessiner()
            # le libellé, lui, se lit : il est sur le fond de la planche
            _bloc(p, x0, y + 138, lib, 28, "taupe", 600, x1 - x0)
            y += 196
    else:
        p.images_absentes = ["krusty.png"]
    p.y = 1070
    p.texte("À gauche le fond est clair, à droite il est foncé. Le "
            "blanc plein meurt à gauche, le violet plein meurt à "
            "droite. Seul le troisième traverse.", 36, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    # Le depliant, en vrai. Le mock-up est attendu sous ce nom ; tant
    # qu'il n'est pas la, poser() le signale et la planche sort sans
    # lui plutot que de faire tomber le cycle.
    #
    # Un SCHEMA avait ete dessine ici a sa place. Il est retire : sur
    # une publication « realisations », un dessin a la place d'un
    # imprime ne vaut rien. On montre la piece, ou on ne montre pas.
    p = Planche("blanc")
    p.titre("Il vit sur un fond\noù tout se dispute.", 66, y=150)
    p.poser(SOURCES / "clients" / "krusty-depliant.png", 540, 720, 900,
            ombre=26)
    p.y = 1070
    p.texte("Trois volets, une trame violette, des dizaines de vignettes "
            "et de prix. Sur ce fond-là, un logo plein se noie. Le cerné "
            "est ce qui le tient au-dessus.", 36, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "04.png"))

    p = Planche("creme")
    p.titre("Le burger ne\nremplace rien.", 78, y=150)
    p.poser(L, 540, 700, 760, ombre=24)
    p.y = 1050
    p.texte("La solution courante est de remplacer une lettre par un "
            "objet. Ici il se pose sur le Y, en débordant du mot. Le "
            "nom reste entier — on le lit avant de voir le burger.",
            36, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "05.png"))

    # L'arc : la ligne du bas est courbe, et le bloc devient un visage.
    p = Planche("creme")
    p.titre("La ligne du bas\nest un sourire.", 76, y=150)
    p.poser(L, 540, 660, 640, ombre=24)
    # l'arc ne s'ajoute pas au logo, il souligne celui qui y est deja.
    p.d.arc([318, 742, 762, 1000], start=12, end=168,
            fill=teinte("corail"), width=8)
    p._redessiner()
    p.y = 1050
    p.texte("« Tellement TASTY !! » ne court pas droit, il court en arc. "
            "Un arc posé sous un bloc de lettres se lit comme une "
            "bouche : le mot entier devient un visage.", 36, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "06.png"))

    p = Planche("blanc")
    p.titre("Ce qui disparaît\nen premier.", 80, y=150)
    _reduction_logo(p, L, 560)
    p.y = 1060
    p.texte("En favicon, l'arc se ferme et le cerne se referme sur les "
            "lettres. Il reste le burger et la masse du mot — c'est "
            "assez pour qu'on le reconnaisse.", 36, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "07.png"))

    p = Planche("encre")
    p.filet()
    p.titre("Un logo plein choisit\nson fond.\nUn logo cerné s'en\npasse.", 60, y=400)
    p.signature("sable")
    faits.append(p.ecrire(d / "08.png"))

    return faits


def _couleurs_sweet_dream():
    """Les deux roses du logo, relevés DANS le fichier.

    Le fichier est livre sans fond : on ne compte que l'opaque. Le
    rose clair porte les lettres, le magenta porte l'ombre — et c'est
    tout, il n'y a pas de troisieme encre.
    """
    import collections
    f = SOURCES / "clients" / "sweet-dream.png"
    if not f.exists():
        return None
    im = Image.open(f).convert("RGBA").resize((600, 160))
    freq = collections.Counter(px[:3] for px in im.getdata()
                               if px[3] > 200).most_common(6)
    if len(freq) < 2:
        return None
    clair, fonce = freq[0][0], freq[1][0]
    if sum(clair) < sum(fonce):
        clair, fonce = fonce, clair
    return {"clair": "#%02x%02x%02x" % clair,
            "fonce": "#%02x%02x%02x" % fonce}


def pub27_sweet_dream(dossier=None):
    """n° 27 — l'ombre portee nette, et ce qu'elle fait avec deux encres.

    Troisieme realisation hors rythme, intercalee dans le cycle :
    mercredi 25 novembre. Les realisations ne sont plus groupees apres
    la fin du cycle, elles alternent avec les publications
    d'information — c'est l'arbitrage du 22 octobre.

    Le sujet n'est ni celui de la n° 25 ni celui de la n° 26. BIG FOOD
    remplacait des lettres, KRUSTY les creusait. SWEET DREAM ne fait ni
    l'un ni l'autre : il DEDOUBLE. Une copie du dessin, decalee, dans
    la seconde encre — et deux aplats font un relief, sans degrade, sans
    flou, sans biseau.

    C'est la lecon la plus transposable des trois, parce qu'elle ne
    coute rien : elle marche en serigraphie, en flocage, en decoupe,
    partout ou un degrade ne passe pas.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-11-25-sweet-dream"))
    accent("rose")
    L = SOURCES / "clients" / "sweet-dream.png"
    L2 = SOURCES / "clients" / "sweet-dream-2lignes.png"
    DEP = SOURCES / "clients" / "sweet-dream-depliant.png"
    C_SD = _couleurs_sweet_dream()
    faits = []

    p = Planche("creme")
    p.surtitre("Réalisation", y=200)
    p.filet()
    p.titre("L'ombre n'est pas\nfloue.", 72)
    p.poser(L, 540, 760, 820, ombre=26)
    p.y = 1060
    p.texte("SWEET DREAM — logo, avec l'accord du client.", 32, "taupe",
            400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("blanc")
    p.poser(L, 540, 620, 940, ombre=0)
    p.y = 1080
    if C_SD:
        p.texte("Deux encres. Le rose clair porte les lettres, le "
                "magenta porte l'ombre. Il n'y a rien d'autre.", 38,
                "brun", 400, avant=0)
    else:
        p.images_absentes = ["sweet-dream.png"]
    p.signature("brun")
    faits.append(p.ecrire(d / "02.png"))

    # La demonstration : la meme ombre, floue puis nette.
    p = Planche("creme")
    p.titre("Floue, elle bave.\nNette, elle tient.", 70, y=150)
    if C_SD:
        clair, fonce = C_SD["clair"], C_SD["fonce"]
        f = police(800, 104)
        larg, haut = p.l - 2 * MARGE, 230
        for k, (y, flou, lib) in enumerate(
                ((470, True, "ombre floue"), (760, False, "ombre décalée"))):
            calque = Image.new("RGBA", (larg, haut), (0, 0, 0, 0))
            dc = ImageDraw.Draw(calque)
            if flou:
                dc.text((38, 46), "SWEET", font=f, fill=fonce)
                calque = calque.filter(ImageFilter.GaussianBlur(13))
                dc = ImageDraw.Draw(calque)
            else:
                dc.text((54, 62), "SWEET", font=f, fill=fonce)
            dc.text((38, 46), "SWEET", font=f, fill=clair)
            p.im.paste(calque, (MARGE, y), calque)
            p._redessiner()
            _bloc(p, MARGE, y + haut - 16, lib, 28, "taupe", 600, larg)
    else:
        p.images_absentes = ["sweet-dream.png"]
    p.y = 1070
    p.texte("Une ombre floue demande un dégradé : elle passe en "
            "quadri, elle meurt en sérigraphie, en flocage et en "
            "découpe. Une ombre décalée est un aplat de plus.", 36,
            "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("blanc")
    p.titre("La couronne\nrepose sur les lettres.", 64, y=150)
    p.poser(L, 540, 700, 800, ombre=24)
    p.y = 1010
    p.texte("Elle ne flotte pas au-dessus du mot : sa base s'appuie sur "
            "les deux E, dont la barre se prolonge pour l'accueillir. "
            "Un objet posé sur un mot doit le toucher.", 36, "brun",
            400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "04.png"))

    p = Planche("creme")
    p.titre("Deux compositions,\nun seul dessin.", 66, y=150)
    p.poser(L, 540, 540, 740, ombre=22)
    p.poser(L2, 540, 860, 400, ombre=22)
    p.y = 1070
    p.texte("Une ligne quand la place est large, deux quand elle est "
            "courte. Les deux sont dans le même fichier vectoriel — "
            "rien n'a été redessiné après coup.", 36, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "05.png"))

    p = Planche("blanc")
    p.titre("Ce qui disparaît\nen premier.", 80, y=150)
    _reduction_logo(p, L, 540)
    p.y = 1040
    p.texte("En favicon, l'ombre se referme sur les lettres et le mot "
            "s'épaissit. La couronne, elle, tient jusqu'au bout — "
            "c'est la forme la plus simple du dessin.", 36, "brun", 400,
            avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "06.png"))

    p = Planche("creme")
    p.titre("Le même logo,\nsur son dépliant.", 66, y=150)
    p.poser(DEP, 540, 740, 900, ombre=26)
    p.y = 1070
    p.texte("Sur l'imprimé il passe en blanc, et l'ombre magenta reste. "
            "C'est elle qu'on reconnaît : le décalage identifie le "
            "logo mieux que sa couleur.", 36, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "07.png"))

    p = Planche("encre")
    p.filet()
    p.titre("Un relief se dessine.\nIl ne se calcule pas.", 62, y=440)
    p.signature("sable")
    faits.append(p.ecrire(d / "08.png"))

    return faits

GABARITS["reel-bilan"] = pub24_reel_bilan
GABARITS["reel-cmjn"] = pub04_reel_cmjn
GABARITS["reel-halloween"] = pub08_reel_halloween
GABARITS["big-food"] = pub25_big_food
GABARITS["krusty"] = pub26_krusty
GABARITS["sweet-dream"] = pub27_sweet_dream


if __name__ == "__main__":
    main()
