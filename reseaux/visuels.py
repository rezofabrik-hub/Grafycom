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
import pathlib
import re
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

RACINE = pathlib.Path(__file__).resolve().parent
POLICES = RACINE / "polices"
SORTIE = RACINE / "visuels"

LARGE, HAUT = 1080, 1350          # format 4:5, le post Instagram
LARGE_S, HAUT_S = 1080, 1920      # format 9:16, la story
MARGE = 86
PSEUDO = "@grafycom.graphiste"    # avec le point. C'est une constante
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


class Planche:
    """Une page de carrousel, ou un écran de story."""

    def __init__(self, fond="creme", large=LARGE, haut=HAUT):
        self.l, self.h = large, haut
        if fond in FONDS_DEGRADE:
            self.im = _degrade_lineaire(large, haut, *FONDS_DEGRADE[fond])
        else:
            self.im = Image.new("RGB", (large, haut), teinte(fond))
        self.d = ImageDraw.Draw(self.im)
        self.y = MARGE

    # -- fonds -------------------------------------------------------
    def bandeau_bas(self, couleur="violet", part=0.33):
        """Un aplat plein sur le bas de la planche."""
        haut = int(self.h * (1 - part))
        self.d.rectangle([0, haut, self.l, self.h], fill=teinte(couleur))
        return self

    # -- texte -------------------------------------------------------
    def titre(self, texte, taille=96, couleur="encre", interligne=1.16,
              y=None, centre=False):
        """Le titrage, en Playfair comme sur le site et dans le feed.

        L'interligne passe de 1.06 a 1.16 : une serif a jambages a besoin
        de plus d'air qu'une sans-serif, sinon les hampes du dessus
        touchent les accents du dessous.
        """
        f = titrage(taille)
        if y is not None:
            self.y = y
        for ligne in couper(texte, f, self.l - 2 * MARGE):
            x = MARGE
            if centre:
                x = (self.l - self.d.textlength(ligne, font=f)) / 2
            self.d.text((x, self.y), ligne, font=f, fill=teinte(couleur))
            self.y += int(taille * interligne)
        self._deborde()
        self._orphelin(texte, f)
        return self

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

    def surtitre(self, texte, couleur="taupe", taille=26, y=None, centre=False):
        """Le petit label en capitales espacees, au-dessus du titre.

        C'est la signature de mise en page du compte : « QUI SUIS-JE ? »,
        « CRÉATION DE LOGO ». Il situe la publication avant qu'on lise le
        titre, et il coute trois mots.
        """
        if y is not None:
            self.y = y
        f = police(800, taille)
        t = texte.upper()
        esp = max(2, taille // 8)
        larg = sum(self.d.textlength(c, font=f) + esp for c in t) - esp
        x = (self.l - larg) / 2 if centre else MARGE
        for c in t:
            self.d.text((x, self.y), c, font=f, fill=teinte(couleur))
            x += self.d.textlength(c, font=f) + esp
        self.y += int(taille * 1.5)
        return self

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

    def texte(self, contenu, taille=38, couleur="brun", graisse=400,
              interligne=1.38, avant=22):
        f = police(graisse, taille)
        self.y += avant
        for ligne in couper(contenu, f, self.l - 2 * MARGE):
            self.d.text((MARGE, self.y), ligne, font=f, fill=teinte(couleur))
            self.y += int(taille * interligne)
        self._deborde()
        return self

    def filet(self, largeur=180, epaisseur=10, y=None, apres=34):
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

    def abonnement(self, couleur="sable", texte=None):
        """La relance d'abonnement, sur le carton de fin d'un reel.

        Uniquement la : ce sont les reels qui atteignent les gens qui ne
        suivent pas encore le compte, et une demande repetee sur chaque
        planche ne se remarque plus. Elle se pose au-dessus de la
        signature, jamais dessus.
        """
        t = texte or "Abonnez-vous : un conseil par semaine."
        f = police(600, 30)
        y = self.h - MARGE - 26 - 48
        self.d.text((MARGE, y), t, font=f, fill=teinte(couleur))
        return self

    def signature(self, couleur="blanc"):
        """Le pseudo, en bas à gauche. Jamais saisi à la main ailleurs."""
        f = police(600, 26)
        self.d.text((MARGE, self.h - MARGE - 26), PSEUDO, font=f,
                    fill=teinte(couleur))
        return self

    def numero(self, n, total, couleur="brun"):
        f = police(600, 24)
        t = "%d/%d" % (n, total)
        self.d.text((self.l - MARGE - f.getlength(t), MARGE - 30), t,
                    font=f, fill=teinte(couleur))
        return self

    # -- formes ------------------------------------------------------
    def disques(self, couleurs, legendes=None, y=None, diam=230):
        """Trois pastilles de couleur, avec une légende facultative."""
        y = self.y if y is None else y
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
        y = self.y if y is None else y
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

    def h_titre(self, texte, taille=96, interligne=1.16):
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
        f = police(800, taille)
        w = f.getlength(texte)
        self.d.rounded_rectangle([x, y, x + w + pad * 2, y + taille + pad],
                                 radius=(taille + pad) // 2, fill=teinte(fond))
        self.d.text((x + pad, y + pad / 2 - 2), texte, font=f,
                    fill=teinte(couleur))
        return w + pad * 2

    def flouter(self, rayon=14):
        from PIL import ImageFilter
        self.im = self.im.filter(ImageFilter.GaussianBlur(rayon))
        self.d = ImageDraw.Draw(self.im)
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

    def chiffre(self, texte, taille=260, couleur="bleu", y=None, centre=False):
        """Un grand nombre, seul. Pour une heure, un prix, une mesure."""
        if y is not None:
            self.y = y
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
        self.im.paste(tourne, (cx - tourne.width // 2, cy - tourne.height // 2), tourne)
        return self

    def ecrire(self, chemin):
        if getattr(self, "orphelins", None):
            print("   ORPHELIN  %-22s %s seul(s) en fin de ligne"
                  % (pathlib.Path(chemin).name,
                     ", ".join("« %s »" % o for o in self.orphelins)))
        if getattr(self, "debordements", 0):
            print("   ATTENTION %s : %d bloc(s) descendent sous la "
                  "signature" % (pathlib.Path(chemin).name,
                                 self.debordements))
        p = pathlib.Path(chemin)
        p.parent.mkdir(parents=True, exist_ok=True)
        self.im.save(p, "PNG")
        return p


# ---------------------------------------------------------------------
# Le carrousel du 12 octobre, en exemple complet et reproductible.
# ---------------------------------------------------------------------
def carrousel_couleurs(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-10-12-couleurs"))
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
    p.titre("Le même prix. Deux fonds.", 62, y=170)
    p.deux_cartes("jaune", "bleu", "12 €", y=330)
    p.titre("Le contraste se vérifie.\nIl ne se devine pas.", 62, y=900)
    faits.append(p.ecrire(d / "05.png"))

    p = Planche("blanc")
    p.titre("Votre secteur en commentaire.", 86, y=320)
    p.texte("Je vous propose trois couleurs pour vous démarquer de vos "
            "concurrents directs.", 40, "brun", 400, avant=40)
    p.fleche("corail", y=820)
    p.signature("brun")
    faits.append(p.ecrire(d / "06.png"))

    return faits


def dilemme_enseigne(dossier=None):
    """Le test A/B du 15 octobre. La seconde planche est la premiere, floutee.

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
    d = pathlib.Path(dossier or (SORTIE / "2026-10-15-dilemme"))
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
    p.titre("Laquelle se lit\ndepuis le trottoir d'en face ?", 72, y=190)
    facades(p); reperes(p)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("creme")
    facades(p)
    p.flouter(8)
    reperes(p)                      # nets : ce sont des reperes
    p.titre("À vingt mètres,\nce n'est plus une typo.", 72, y=190)
    p.titre("C'est une silhouette.", 76, "corail", y=1120)
    faits.append(p.ecrire(d / "02.png"))
    return faits


def carrousel_typographie(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-10-19-typographie"))
    f = []
    p = Planche("blanc")
    t = "Cette police est magnifique."
    p.centrer(p.h_titre(t, 92) + p.h_texte("Et elle va vous coûter des clients.", 44, avant=40) + 39)
    p.surtitre("Typographie")
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
    d = pathlib.Path(dossier or (SORTIE / "2026-10-13-enseigne"))
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
    d = pathlib.Path(dossier or (SORTIE / "2026-10-22-quiz"))
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
    d = pathlib.Path(dossier or (SORTIE / "2026-10-20-droits"))
    f = []
    p = Planche("creme")
    t = "Qui possède\nvotre logo ?"
    p.centrer(p.h_titre(t, 110) + p.h_texte("La réponse surprend la plupart des chefs d'entreprise.", 42, avant=50) + 39)
    p.surtitre("Droits & propriété")
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
    p.titre("Ce qui se cède,\net ce qui ne se cède pas", 66, y=200)
    p.texte("Les droits patrimoniaux se cèdent : exploiter, reproduire, adapter.", 42, "encre", 600, avant=70)
    p.texte("Le droit moral, jamais. Il reste à l'auteur, à vie.", 42, "corail", 600, avant=40)
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


def plans_reel_cmjn(dossier=None):
    """Les cinq plans du reel du 16 octobre, en 9:16, a enchainer au montage."""
    d = pathlib.Path(dossier or (SORTIE / "2026-10-16-reel-cmjn"))
    f = []
    plans = [
        ("creme", "encre", "Pourquoi ce n'est jamais\nla même couleur", ""),
        ("blanc", "encre", "RVB", "De la lumière.\nRouge, vert, bleu.\nPlus on en met, plus c'est clair."),
        ("encre", "blanc", "CMJN", "Quatre encres.\nCyan, magenta, jaune, noir.\nChaque couche retire de la lumière."),
        ("creme", "encre", "Le papier\nchange tout", "Un mat absorbe.\nUn couché renvoie."),
        ("encre", "blanc", "Demandez un BAT.\nToujours.", "C'est gratuit, et ça évite de tout refaire."),
    ]
    for i, (fond, enc, titre, sous) in enumerate(plans, 1):
        p = Planche(fond, LARGE_S, HAUT_S)
        h = p.h_titre(titre, 96) + (p.h_texte(sous, 46, avant=60) if sous else 0)
        p.centrer(h, 0.44)
        p.titre(titre, 96, enc)
        if sous:
            p.texte(sous, 46, enc, 400, avant=60)
        if i == len(plans):          # le carton de fin, et lui seul
            p.abonnement("sable" if fond == "encre" else "taupe")
        p.signature(enc)
        f.append(p.ecrire(d / ("plan%d.png" % i)))
    return f


def plans_reel_halloween(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-10-23-reel-halloween"))
    f = []
    plans = [
        ("encre", "orange", "Pourquoi Halloween\nest orange et noir", ""),
        ("orange", "encre", "Le contraste\nmaximal", "On le repère avant de comprendre ce qu'on regarde."),
        ("encre", "orange", "La nature\nl'utilise déjà", "Guêpes, serpents, rubans de chantier.\nLe message : attention."),
        ("creme", "encre", "Et pour\nvotre vitrine ?", "Parfait en saisonnier.\nÉpuisant toute l'année."),
        ("encre", "blanc", "Une couleur\nn'est jamais neutre.", "Elle dit quelque chose avant vous."),
    ]
    for i, (fond, enc, titre, sous) in enumerate(plans, 1):
        p = Planche(fond, LARGE_S, HAUT_S)
        h = p.h_titre(titre, 96) + (p.h_texte(sous, 46, avant=60) if sous else 0)
        p.centrer(h, 0.44)
        p.titre(titre, 96, enc)
        if sous:
            p.texte(sous, 46, enc, 400, avant=60)
        if i == len(plans):          # le carton de fin, et lui seul
            p.abonnement("sable" if fond == "encre" else "taupe")
        p.signature(enc)
        f.append(p.ecrire(d / ("plan%d.png" % i)))
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
    d = pathlib.Path(dossier or (SORTIE / "2026-10-17-blog-rdv"))
    f = []

    p = Planche("sable_chaud")
    p.surtitre("Le blog", y=270)
    p.filet()
    p.titre("Un nouvel article\nchaque vendredi matin.", 84, "encre")
    p.y = 640
    p.texte("Sur grafycom.fr/blog. Gratuit, sans inscription.", 42, "brun",
            400, avant=0)
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
    p.titre("Les quatre prochains", 76, "encre", y=180)
    p.y = 380
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
    d = pathlib.Path(dossier or (SORTIE / "2026-10-29-dilemme-carte"))
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
    d = pathlib.Path(dossier or (SORTIE / "2026-11-09-retroplanning"))
    f = []

    p = Planche("sable_chaud")
    p.surtitre("Fin d'année", y=250)
    p.filet()
    p.titre("Vos cartes de vœux\nde Noël se décident\ncette semaine.", 86,
            "encre")
    p.y = 760
    p.texte("Pas en décembre. Voici pourquoi.", 42, "brun", 400, avant=0)
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
    p.y = 740
    p.texte("En commentaire. Je vous dis la date limite réelle pour le "
            "décider — pas celle de l'imprimeur, la vôtre.", 40, "brun",
            400, avant=0)
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
    d = pathlib.Path(dossier or (SORTIE / "2026-11-12-dilemme-voeux"))
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
    d = pathlib.Path(dossier or (SORTIE / "2026-11-19-quiz-fin-annee"))
    f = []

    p = Planche("sable_chaud")
    p.surtitre("Quiz", y=230)
    p.filet()
    p.titre("4 idées reçues\nsur vos impressions\nde fin d'année.", 86,
            "encre")
    p.y = 760
    p.texte("Vous en avez combien de justes ?", 46, "brun", 600, avant=0)
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


def _plans_tournage(dossier, titre, plans, numero_total):
    """Les planches de tournage d'un reel, en 9:16.

    Ce ne sont pas les images du reel : ce sont les fiches que Sandra suit
    au telephone. Chacune porte le chrono, le cadrage a filmer et le texte
    incruste tel qu'il apparaitra. visuels.py ne fabrique pas de
    photographies, et un reel sur la matiere se tourne.
    """
    d = pathlib.Path(dossier)
    f = []
    for i, (chrono, cadrage, incruste, cloture) in enumerate(plans, 1):
        if cloture:
            # le carton de fin, lui, est un vrai visuel : il se publie
            p = Planche("encre", LARGE_S, HAUT_S)
            p.centrer(p.h_titre(incruste, 80) + 44, 0.42)
            p.filet()
            p.titre(incruste, 80, "blanc")
            p.y += 40
            p.texte(cadrage, 42, "creme", 400, avant=20)
            p.abonnement("sable")
            p.signature("sable")
            p.d.text((p.l - MARGE - 160, MARGE), chrono, font=police(600, 30),
                     fill=teinte("sable"))
        else:
            p = Planche("creme", LARGE_S, HAUT_S)
            p.d.text((MARGE, MARGE), titre, font=police(800, 30),
                     fill=teinte("taupe"))
            p.d.text((p.l - MARGE - 160, MARGE), chrono,
                     font=police(600, 30), fill=teinte("corail"))
            p.d.line([MARGE, MARGE + 60, p.l - MARGE, MARGE + 60],
                     fill=teinte("sable_fonce"), width=2)
            p.y = 260
            p.d.text((MARGE, 230), "À FILMER", font=police(800, 28),
                     fill=teinte("corail"))
            p.y = 300
            p.texte(cadrage, 44, "encre", 400, avant=0)
            yc = max(p.y + 80, 900)
            p.d.text((MARGE, yc), "TEXTE INCRUSTÉ", font=police(800, 28),
                     fill=teinte("violet"))
            p.y = yc + 80
            p.encadre(incruste, 52, "blanc", "violet", pad=38, graisse=800,
                      couleur="encre")
            p.y = p.h - MARGE - 120
            p.texte("Plan %d sur %d — fiche de tournage, ne se publie pas."
                    % (i, numero_total), 30, "taupe", 400, avant=0)
        f.append(p.ecrire(d / ("plan%d.png" % i)))
    return f


def plans_reel_matieres(dossier=None):
    """n° 20, vendredi 13 novembre — ce que vos clients sentent avant de lire."""
    plans = [
        ("0-3 s",
         "Macro, lumière rasante venue du côté. Un pouce passe lentement "
         "sur un motif gaufré. On voit le relief avant de voir le dessin.",
         "Ce que vos clients sentent avant de lire", False),
        ("3-8 s",
         "Deux cartes tombent côte à côte sur une table en bois. L'une se "
         "plie et ondule, l'autre reste droite et claque.",
         "120 g / 350 g", False),
        ("8-14 s",
         "Plan fixe sur un gaufrage éclairé de côté, puis la même carte "
         "éclairée de face : le motif disparaît presque.",
         "Le gaufrage : du relief, pas de l'encre", False),
        ("14-19 s",
         "Rotation lente d'une carte sous une lampe. Un trait doré "
         "s'allume, puis s'éteint selon l'angle.",
         "La dorure : une feuille, pas du jaune", False),
        ("19-24 s",
         "Un beau visuel sur un mauvais papier déçoit. Un visuel simple "
         "sur un beau papier se garde.",
         "Choisissez la matière\navant le dessin", True),
    ]
    return _plans_tournage(dossier or (SORTIE / "2026-11-13-reel-matieres"),
                           "REEL 24 s · matières", plans, 5)


def plans_reel_bilan(dossier=None):
    """n° 24, samedi 21 novembre — faut-il refaire son logo en janvier."""
    plans = [
        ("0-3 s",
         "Un carnet de croquis rempli de recherches de logo se ferme d'un "
         "coup sec. Lumière d'atelier, venue du côté.",
         "Non, pas en janvier", False),
        ("3-9 s",
         "Un calendrier mural : le doigt tourne la page de décembre à "
         "janvier. Puis un logo clignote entre deux versions presque "
         "identiques.",
         "Changer par calendrier,\nce n'est pas changer par besoin", False),
        ("9-15 s",
         "Trois cartons posés un par un sur la table, chacun avec une "
         "question écrite à la main.",
         "1. Lisible partout ?\n2. Fichiers en main ?\n3. Dit-il ce que vous "
         "vendez ?", False),
        ("15-21 s",
         "Le même logo décliné sur un polo, une carte, un panneau : il "
         "tient sur deux supports, il se brouille sur le troisième. Zoom "
         "sur celui qui se brouille.",
         "Deux « oui », un « non » :\non ajuste", False),
        ("21-26 s",
         "Si la réponse est non aux trois, on repart de la feuille "
         "blanche. Sinon, un problème précis se répare.",
         "Un bilan,\npas une résolution", True),
    ]
    return _plans_tournage(dossier or (SORTIE / "2026-11-21-reel-bilan"),
                           "REEL 26 s · bilan", plans, 5)


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
      "Votre vitrine fait 6 m².",
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
     ("S6-E", "creme", "encre", "Coulisses du reel",
      "Cinq plans de cinq secondes, un carnet et une lampe.",
      "", ["Le tournage du jour."]),
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
    "plans-reel-matieres": plans_reel_matieres,
    "plans-reel-bilan": plans_reel_bilan,
    "blog-rendez-vous": carrousel_blog_rdv,
    "plans-reel-cmjn": plans_reel_cmjn,
    "plans-reel-halloween": plans_reel_halloween,
    "stories": stories,
}




def solaire_66(dossier=None):
    """Publication du 2 novembre : l'identité Solaire 66.

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
    d = pathlib.Path(dossier or (SORTIE / "2026-11-02-solaire-66"))
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
    p.titre("Ces deux couleurs" + "\n" + "ne sont pas un goût.", 92, y=150)
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
    p.titre("Regardez le O.", 110, y=160)
    p.poser(S / "solaire-66-logo.png", 540, 560, 880, ombre=0)
    p.y = 870
    p.texte("Ce n'est pas un O avec un soleil posé dessus. C'est le soleil "
            "qui tient le rôle du O. Un symbole posé à côté d'un nom peut "
            "toujours s'en détacher ; devenu une lettre, il ne peut plus "
            "partir sans emporter le mot.", 38, "brun", 400, avant=0)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("creme")
    p.titre("Une carte de visite" + "\n" + "fait 85 millimètres.", 88, y=140)
    p.poser(S / "solaire-66-carte-verso.png", 700, 900, 540, angle=-6,
            rogner_mm=2, mm_par_px=MM)
    p.poser(S / "solaire-66-carte-recto.png", 390, 640, 540, angle=6,
            rogner_mm=2, mm_par_px=MM)
    p.signature("brun")
    faits.append(p.ecrire(d / "04.png"))

    # La planche qui porte la demonstration : a l'echelle exacte.
    p = Planche("creme")
    p.titre("À l'échelle exacte.", 96, y=140)
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
    p.titre("En une seule couleur.", 80, y=150)
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
    p.titre("Dessiné en grand." + "\n" + "Vérifié en petit.", 92)
    p.y = 470
    p.texte("Sur un panneau de chantier, un logo peut tout se permettre. "
            "Sur 8,5 centimètres, dans un avatar, brodé sur un polo, le "
            "détail devient de la bouillie.", 38, "brun", 400, avant=0)
    p.y = 720
    p.texte("C'est pour ça qu'une identité livrée ne contient jamais un "
            "seul fichier.", 40, "encre", 600, avant=0)
    p.signature("blanc")
    faits.append(p.ecrire(d / "07.png"))

    return faits


# ---------------------------------------------------------------------
# Un logo fictif, dessine, pour les demonstrations de reduction.
# Il n'imite aucune marque existante : c'est un exercice, et la legende
# de la publication le dit.
# ---------------------------------------------------------------------
def _logo_fictif(d, cx, cy, r, detail=True):
    from PIL import ImageDraw
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=teinte("bleu"))
    d.ellipse([cx - r * .72, cy - r * .72, cx + r * .72, cy + r * .72],
              fill=teinte("bleu_vif"))
    d.ellipse([cx - r * .44, cy - r * .44, cx + r * .44, cy + r * .44],
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
    """n° 9, lundi 26 octobre — un logo tient-il en petit."""
    d = pathlib.Path(dossier or (SORTIE / "2026-10-26-logo-reduction"))
    faits = []

    p = Planche("creme")
    p.surtitre("Conseil", y=130)
    p.titre("Votre logo tient-il" + "\n" + "sur un stylo ?", 96)
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
            "corail", 42, "brun", y=520, interligne=1.6)
    p.signature("brun")
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("creme")
    p.titre("Un logo doit exister" + "\n" + "en une seule couleur.", 84, y=150)
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
    p.titre("Le même, cinq fois," + "\n" + "sans retouche.", 88, y=150)
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
    p.titre("Faites le test" + "\n" + "ce soir.", 104, "blanc")
    p.y = 640
    p.texte("Réduisez votre logo à la taille d'un ongle. Si vous ne le "
            "reconnaissez plus, vos clients non plus.", 40, "creme", 400,
            avant=0)
    p.fleche("corail", y=950)
    p.signature("sable")
    faits.append(p.ecrire(d / "06.png"))
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
        return
    if args.exemple:
        for f in carrousel_couleurs():
            im = Image.open(f)
            print("%-52s %sx%s" % (f, im.size[0], im.size[1]))
        return
    a.print_help()


# Les deux gabarits ci-dessous sont definis apres le registre : on les
# y ajoute ici, sinon --liste et --tout les ignorent en silence.
GABARITS["solaire-66"] = solaire_66
GABARITS["logo-reduction"] = pub09_logo_reduction


if __name__ == "__main__":
    main()
