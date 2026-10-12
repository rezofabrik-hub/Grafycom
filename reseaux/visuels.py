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
    return ImageFont.truetype(str(f), taille)


def couper(texte: str, fonte, largeur: int) -> list[str]:
    """Découpe un texte à la largeur donnée, en respectant les retours forcés."""
    lignes = []
    for para in texte.split("\n"):
        mots, courante = para.split(), ""
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
    def titre(self, texte, taille=96, couleur="encre", interligne=1.06, y=None):
        f = police(800, taille)
        if y is not None:
            self.y = y
        for ligne in couper(texte, f, self.l - 2 * MARGE):
            self.d.text((MARGE, self.y), ligne, font=f, fill=teinte(couleur))
            self.y += int(taille * interligne)
        return self

    def texte(self, contenu, taille=38, couleur="brun", graisse=400,
              interligne=1.38, avant=22):
        f = police(graisse, taille)
        self.y += avant
        for ligne in couper(contenu, f, self.l - 2 * MARGE):
            self.d.text((MARGE, self.y), ligne, font=f, fill=teinte(couleur))
            self.y += int(taille * interligne)
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

    def h_titre(self, texte, taille=96, interligne=1.06):
        f = police(800, taille)
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
        self.d.rectangle([MARGE, 300, self.l - MARGE, 1050],
                         outline=teinte("taupe"), width=4)
        f = police(600, 34)
        self.d.text((MARGE + 40, 350), "PHOTO À FOURNIR", font=f,
                    fill=teinte("corail"))
        self.y = 430
        self.texte(description, 38, "brun", 400, avant=0)
        self.y = 950
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
    p.filet(y=230)
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
    p.centrer(p.h_titre(t, 92) + p.h_texte("Et elle va vous coûter des clients.", 44, avant=40))
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
    p.centrer(p.h_titre(t, 74) + 44)
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
    p.centrer(p.h_titre(t, 110) + p.h_texte("La réponse surprend la plupart des chefs d'entreprise.", 42, avant=50))
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
        ("violet", "blanc", "Demandez un BAT.\nToujours.", "C'est gratuit, et ça évite de tout refaire."),
    ]
    for i, (fond, enc, titre, sous) in enumerate(plans, 1):
        p = Planche(fond, LARGE_S, HAUT_S)
        h = p.h_titre(titre, 96) + (p.h_texte(sous, 46, avant=60) if sous else 0)
        p.centrer(h, 0.44)
        p.titre(titre, 96, enc)
        if sous:
            p.texte(sous, 46, enc, 400, avant=60)
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
        ("violet", "blanc", "Une couleur\nn'est jamais neutre.", "Elle dit quelque chose avant vous."),
    ]
    for i, (fond, enc, titre, sous) in enumerate(plans, 1):
        p = Planche(fond, LARGE_S, HAUT_S)
        h = p.h_titre(titre, 96) + (p.h_texte(sous, 46, avant=60) if sous else 0)
        p.centrer(h, 0.44)
        p.titre(titre, 96, enc)
        if sous:
            p.texte(sous, 46, enc, 400, avant=60)
        p.signature(enc)
        f.append(p.ecrire(d / ("plan%d.png" % i)))
    return f


def carrousel_devis(dossier=None):
    """Publication n° 6 — ce qui doit figurer sur un devis.

    Le dossier 2026-10-20-droits existait pour cette date, mais il dessine
    « Qui possede votre logo ? » : un autre sujet que le texte de la
    publication n° 6. Les deux jeux sont donc distincts, et celui-ci est
    dessine d'apres la direction visuelle ecrite, slide par slide.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-10-20-devis"))
    f = []
    ZONES = [("en-tete", "EN-TÊTE"), ("identite", "IDENTITÉ"),
             ("corps", "CORPS"), ("pied", "PIED DE PAGE")]
    TEINTES = {"en-tete": "bleu", "identite": "turquoise",
               "corps": "violet", "pied": "corail"}

    def feuille(p, x, y, larg, haut, zones=(), etiquettes=False):
        """Un devis en fil de fer. Les zones nommees se surlignent.

        Les hauteurs sont calculees en parts de la feuille, pas en pixels
        fixes : le meme dessin sert en grand sur la slide 3 et en vignette
        sur la slide 5, sans que le corps deborde du cadre.
        """
        p.d.rectangle([x, y, x + larg, y + haut], fill=teinte("blanc"),
                      outline=teinte("sable_fonce"), width=3)
        pad = int(haut * 0.035)
        h_ent = int(haut * 0.16)
        h_ide = int(haut * 0.11)
        h_pie = int(haut * 0.17)
        h_cor = haut - h_ent - h_ide - h_pie - 5 * pad
        y1 = y + pad
        y2 = y1 + h_ent + pad
        y3 = y2 + h_ide + pad
        y4 = y3 + h_cor + pad
        bandes = {"en-tete": (y1, h_ent), "identite": (y2, h_ide),
                  "corps": (y3, h_cor), "pied": (y4, h_pie)}

        for nom, _ in ZONES:
            yy, hh = bandes[nom]
            if nom in zones:
                p.d.rectangle([x + pad, yy, x + larg - pad, yy + hh],
                              fill=teinte(TEINTES[nom]))

        def lignes(yy, hh, pas, l1, decr, claire):
            n = max(1, int((hh - 8) / pas))
            coul = "blanc" if claire else "sable_fonce"
            for i in range(n):
                ll = int(l1 * (1 - decr * i))
                p.d.rounded_rectangle(
                    [x + 2 * pad, yy + 6 + i * pas,
                     x + 2 * pad + ll, yy + 6 + i * pas + max(6, pas // 4)],
                    radius=4, fill=teinte(coul))

        ech = larg / 480.0
        lignes(y1, h_ent, int(30 * ech), larg - int(300 * ech), 0.22,
               "en-tete" in zones)
        lignes(y2, h_ide, int(30 * ech), larg - int(420 * ech), 0.30,
               "identite" in zones)
        lignes(y3, h_cor, int(42 * ech), larg - int(120 * ech), 0.04,
               "corps" in zones)
        lignes(y4, h_pie, int(32 * ech), larg - int(360 * ech), 0.18,
               "pied" in zones)

        if etiquettes:
            fe = police(800, 26)
            for nom, lib in ZONES:
                yy, hh = bandes[nom]
                p.d.text((x + larg + 26, yy + hh / 2 - 15), lib, font=fe,
                         fill=teinte(TEINTES[nom]))
        return p

    # S1 — l'accroche, le devis et la loupe sur son pied de page
    p = Planche("creme")
    feuille(p, 300, 150, 480, 660)
    cx, cy, r = 740, 740, 92
    p.d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=teinte("corail"),
                width=14)
    p.d.line([cx + 64, cy + 64, cx + 150, cy + 150], fill=teinte("corail"),
             width=16)
    p.y = 900
    p.titre("Ce qui doit figurer\nsur votre devis.", 82, "encre")
    p.signature("brun")
    p.numero(1, 6, "taupe")
    f.append(p.ecrire(d / "01.png"))

    # S2 — l'enjeu, en aplat bleu
    p = Planche("sable_chaud")
    t = ("Un devis mal renseigné,\nce n'est pas\nun détail "
         "administratif.")
    st = "C'est une crédibilité en moins au moment de la signature."
    p.centrer(p.h_titre(t, 76) + p.h_texte(st, 42, avant=50) + 44)
    p.filet()
    p.titre(t, 76, "encre")
    p.texte(st, 42, "brun", 400, avant=50)
    p.signature("brun")
    p.numero(2, 6, "taupe")
    f.append(p.ecrire(d / "02.png"))

    # S3 — le squelette, zones surlignees et nommees
    p = Planche("creme_rose")
    p.titre("Quatre zones.\nChacune a son rôle.", 72, "encre", y=140)
    feuille(p, 150, 400, 540, 700,
            zones=("en-tete", "identite", "corps", "pied"), etiquettes=True)
    p.signature("brun")
    p.numero(3, 6, "taupe")
    f.append(p.ecrire(d / "03.png"))

    # S4 — l'en-tete
    p = Planche("creme")
    p.titre("Dans l'en-tête", 88, "encre", y=260)
    p.y = 440
    p.puces(["La dénomination de l'entreprise",
             "La forme juridique",
             "L'adresse de l'établissement",
             "Le numéro SIREN",
             "Le numéro de TVA, le cas échéant"],
            "bleu", 44, "brun")
    p.signature("brun")
    p.numero(4, 6, "taupe")
    f.append(p.ecrire(d / "04.png"))

    # S5 — le pied de page
    p = Planche("creme")
    p.titre("En pied de page", 88, "encre", y=170)
    p.y = 330
    p.puces(["La durée de validité de l'offre",
             "Les conditions de règlement",
             "La case de signature, et la mention\n« Bon pour accord »"],
            "corail", 44, "brun")
    feuille(p, 330, 720, 420, 420, zones=("pied",))
    p.signature("brun")
    p.numero(5, 6, "taupe")
    f.append(p.ecrire(d / "05.png"))

    # S6 — la chute, en aplat violet
    p = Planche("encre")
    t = "Le design d'un devis,\nce n'est pas de la\ndécoration."
    st = "C'est ce qui le rend lisible — et signé."
    p.centrer(p.h_titre(t, 80) + p.h_texte(st, 44, avant=56) + 44)
    p.filet()
    p.titre(t, 80, "blanc")
    p.texte(st, 44, "creme", 600, avant=56)
    p.signature("sable")
    p.numero(6, 6, "sable")
    f.append(p.ecrire(d / "06.png"))
    return f


def stories(dossier=None):
    """Les dix ecrans de stories du cycle, en 9:16."""
    d = pathlib.Path(dossier or (SORTIE / "stories"))
    f = []
    ecrans = [
        ("07-teasing", "creme", "encre", "Nouveau post.\nVotre couleur parle avant vous.",
         "Sondage", ["Le bleu marine évoque plutôt…", "A : la confiance", "B : le luxe"]),
        ("13-quiz-1", "sable_chaud", "encre", "Enseigne :\ndéclaration ou autorisation ?",
         "Quiz", ["Déclaration préalable", "Autorisation préalable"]),
        ("13-quiz-2", "sable_chaud", "encre", "Autorisation.\nCerfa 16308*01, en mairie,\nen trois exemplaires.",
         "Mention du post", ["Le détail est dans le post du jour"]),
        ("14-questions", "sable_chaud", "encre",
         "Une question sur votre\nidentité visuelle ?",
         "Boîte à questions", ["Je réponds à tout.", "Même aux questions bêtes.", "Surtout à celles-là."]),
        ("08-vote-1", "blanc", "encre", "Laquelle se lit\nà vingt mètres ?",
         "Sondage", ["A", "B"]),
        ("08-vote-2", "creme", "encre", "Réponse : B.\nÀ vingt mètres, une typo\ndevient une silhouette.",
         "Curseur emoji", ["Vous aviez deviné ?"]),
        ("09-blog", "creme", "encre", "Nouvel article :\nl'autorisation d'enseigne,\nétape par étape.",
         "Sticker Lien", ["grafycom.fr/blog"]),
        ("12-teasing", "creme", "encre", "Cette police est magnifique.\nEt pourtant…",
         "Curseur emoji", ["Vous choisissez vos polices au feeling ?"]),
        ("20-teasing", "blanc", "encre", "Avez-vous un contrat de cession\npour votre logo ?",
         "Sondage", ["A : oui, je l'ai", "B : aucune idée"]),
        ("21-coulisses", "creme", "encre",
         "Trois pistes pour un même logo.\nDeux finiront à la corbeille.",
         "", ["C'est normal. C'est même le travail."]),
    ]
    for nom, fond, enc, titre, st, lignes in ecrans:
        p = Planche(fond, LARGE_S, HAUT_S)
        p.titre(titre, 72, enc, y=460)
        if st:
            p.sticker(st, lignes, y=HAUT_S - 700)
        else:
            p.texte(lignes[0], 44, enc, 400, avant=60)
        p.signature(enc)
        f.append(p.ecrire(d / ("%s.png" % nom)))
    return f


GABARITS = {
    "carrousel-couleurs": carrousel_couleurs,
    "dilemme-enseigne": dilemme_enseigne,
    "carrousel-typographie": carrousel_typographie,
    "carrousel-enseigne": carrousel_enseigne,
    "quiz-idees-recues": quiz_idees_recues,
    "carrousel-droits": carrousel_droits,
    "carrousel-devis": carrousel_devis,
    "plans-reel-cmjn": plans_reel_cmjn,
    "plans-reel-halloween": plans_reel_halloween,
    "stories": stories,
}




def solaire_66(dossier=None):
    """Publication du 2 novembre : l'identité Solaire 66.

    Solaire 66 est la société de Laurent, qui commande aussi ces
    publications : l'accord de publication est acquis à la source.

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
    p.poser(S / "solaire-66-logo.png", 540, 620, 960, ombre=0)
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
    p.titre("Votre logo tient-il" + "\n" + "sur un stylo ?", 96, y=150)
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
