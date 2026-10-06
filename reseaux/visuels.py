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

from PIL import Image, ImageDraw, ImageFont

RACINE = pathlib.Path(__file__).resolve().parent
POLICES = RACINE / "polices"
SORTIE = RACINE / "visuels"

LARGE, HAUT = 1080, 1350          # format 4:5, le post Instagram
MARGE = 86
PSEUDO = "@grafycom.graphiste"    # avec le point. C'est une constante
                                  # justement pour qu'il ne se perde plus.

# La charte, reprise des variables CSS du site.
C = {
    "creme":  "#f7f1ef",
    "blanc":  "#ffffff",
    "encre":  "#2f2723",
    "violet": "#a86cd0",
    "bleu":   "#2f7fc4",
    "corail": "#f2585c",
    "rose":   "#e75ba6",
    "vert":   "#3a6b4a",
    "jaune":  "#f5e6a8",
    "brun":   "#6d5a50",
}


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


class Planche:
    """Une page de carrousel, ou un écran de story."""

    def __init__(self, fond="creme", large=LARGE, haut=HAUT):
        self.l, self.h = large, haut
        self.im = Image.new("RGB", (large, haut), C.get(fond, fond))
        self.d = ImageDraw.Draw(self.im)
        self.y = MARGE

    # -- fonds -------------------------------------------------------
    def bandeau_bas(self, couleur="violet", part=0.33):
        """Un aplat plein sur le bas de la planche."""
        haut = int(self.h * (1 - part))
        self.d.rectangle([0, haut, self.l, self.h], fill=C.get(couleur, couleur))
        return self

    # -- texte -------------------------------------------------------
    def titre(self, texte, taille=96, couleur="encre", interligne=1.06, y=None):
        f = police(800, taille)
        if y is not None:
            self.y = y
        for ligne in couper(texte, f, self.l - 2 * MARGE):
            self.d.text((MARGE, self.y), ligne, font=f, fill=C.get(couleur, couleur))
            self.y += int(taille * interligne)
        return self

    def texte(self, contenu, taille=38, couleur="brun", graisse=400,
              interligne=1.38, avant=22):
        f = police(graisse, taille)
        self.y += avant
        for ligne in couper(contenu, f, self.l - 2 * MARGE):
            self.d.text((MARGE, self.y), ligne, font=f, fill=C.get(couleur, couleur))
            self.y += int(taille * interligne)
        return self

    def signature(self, couleur="blanc"):
        """Le pseudo, en bas à gauche. Jamais saisi à la main ailleurs."""
        f = police(600, 26)
        self.d.text((MARGE, self.h - MARGE - 26), PSEUDO, font=f,
                    fill=C.get(couleur, couleur))
        return self

    def numero(self, n, total, couleur="brun"):
        f = police(600, 24)
        t = "%d/%d" % (n, total)
        self.d.text((self.l - MARGE - f.getlength(t), MARGE - 30), t,
                    font=f, fill=C.get(couleur, couleur))
        return self

    # -- formes ------------------------------------------------------
    def disques(self, couleurs, legendes=None, y=None, diam=230):
        """Trois pastilles de couleur, avec une légende facultative."""
        y = self.y if y is None else y
        n = len(couleurs)
        espace = (self.l - 2 * MARGE - n * diam) // max(n - 1, 1)
        x = MARGE
        for i, c in enumerate(couleurs):
            self.d.ellipse([x, y, x + diam, y + diam], fill=C.get(c, c))
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
            self.d.rectangle([x, y, x + larg, y + haut], fill=C.get(fond, fond))
            w = f.getlength(texte)
            self.d.text((x + (larg - w) / 2, y + haut / 2 - 75), texte,
                        font=f, fill=C["blanc"])
        self.y = y + haut + 40
        return self

    def fleche(self, couleur="corail", y=None, taille=54):
        y = self.y if y is None else y
        f = police(800, taille)
        self.d.text((MARGE, y), "→", font=f, fill=C.get(couleur, couleur))
        self.y = y + taille + 20
        return self

    # -- sortie ------------------------------------------------------
    def ecrire(self, chemin):
        p = pathlib.Path(chemin)
        p.parent.mkdir(parents=True, exist_ok=True)
        self.im.save(p, "PNG")
        return p


# ---------------------------------------------------------------------
# Le carrousel du 7 octobre, en exemple complet et reproductible.
# ---------------------------------------------------------------------
def carrousel_couleurs(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-10-07-couleurs"))
    faits = []

    p = Planche("creme").bandeau_bas("violet", 0.30)
    p.titre("Votre couleur dit déjà ce que vous vendez.", 104, y=230)
    p.signature("blanc")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("blanc")
    p.titre("Avant même de lire votre nom…", 62, y=170)
    p.disques(["vert", "bleu", "rose"], y=460)
    p.texte("Le client a déjà deviné votre secteur.", 42, "encre", 600, avant=90)
    faits.append(p.ecrire(d / "02.png"))

    p = Planche("blanc")
    p.disques(["vert", "bleu", "rose"],
              ["BIO\nSANTÉ", "BANQUE\nCONSEIL", "SOIN\nENFANCE"], y=250)
    p.titre("Ce ne sont pas des règles.\nCe sont des réflexes.", 66, y=820)
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("violet")
    p.titre("Les suivre vous rend crédible.\nLes casser vous rend mémorable.",
            78, "blanc", y=300)
    p.texte("Le problème, c'est de le faire sans le savoir.", 40, "blanc", 400,
            avant=60)
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


GABARITS = {"carrousel-couleurs": carrousel_couleurs}


def main():
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--exemple", action="store_true",
                   help="produire le carrousel du 7 octobre")
    a.add_argument("--liste", action="store_true", help="les gabarits connus")
    args = a.parse_args()

    if args.liste:
        for k in GABARITS:
            print(" ", k)
        return
    if args.exemple:
        for f in carrousel_couleurs():
            im = Image.open(f)
            print("%-52s %sx%s" % (f, im.size[0], im.size[1]))
        return
    a.print_help()


if __name__ == "__main__":
    main()
