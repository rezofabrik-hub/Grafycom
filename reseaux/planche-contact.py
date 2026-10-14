#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Une planche-contact de tous les visuels produits, pour les relire.

Pourquoi ce fichier existe
--------------------------
`visuels.py --tout` produit 177 images dans 26 dossiers. Les relire une
par une dans un explorateur de fichiers, c'est 177 double-clics, et on ne
voit jamais un carrousel entier d'un coup — or c'est exactement ce qu'il
faut voir : une planche seule peut etre juste et la suite incoherente.

Ce script pose chaque publication sur une page A4, ses planches dans
l'ordre, numerotees. On relit en faisant defiler, on annote au nom du
fichier, et on corrige planche par planche.

Il ne lit AUCUNE liste codee en dur : il parcourt les dossiers de
`reseaux/visuels/`, dans l'ordre des dates que portent leurs noms. Un
gabarit ajoute demain apparait sans que ce fichier soit touche.

Usage
-----
    python3 reseaux/planche-contact.py            # tout le cycle
    python3 reseaux/planche-contact.py 2026-11    # un mois
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

RACINE = pathlib.Path(__file__).resolve().parent.parent
VISUELS = RACINE / "reseaux" / "visuels"
POLICES = RACINE / "reseaux" / "polices"
SORTIE = RACINE / "reseaux" / "pdf" / "planche-contact.pdf"

sys.path.insert(0, str(RACINE / "generateurs"))
from charte import C  # noqa: E402

LARGE, HAUT = 2480, 3508          # A4 a 300 dpi
MARGE = 150

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]

# « sources » contient les logos clients et les recuperations, pas des
# planches : ce ne sont pas des visuels a relire, et plusieurs ne sont
# pas publiables. On ne les met pas dans un document de relecture.
IGNORES = {"sources"}

# Au-dela, les vignettes deviennent trop petites pour qu'on voie quoi que
# ce soit. Les 44 ecrans de stories se repartissent donc sur quatre pages
# plutot que de tenir sur une, illisibles.
PAR_PAGE = 12


def police(nom, taille):
    return ImageFont.truetype(str(POLICES / nom), taille)


def titre_du_dossier(nom):
    """« 2026-11-23-vitrine-trottoir » -> date lisible et sujet."""
    morceaux = nom.split("-")
    try:
        annee, mois, jour = int(morceaux[0]), int(morceaux[1]), int(morceaux[2])
        date = "%d %s %d" % (jour, MOIS[mois - 1], annee)
        sujet = " ".join(morceaux[3:]).replace("_", " ")
    except (ValueError, IndexError):
        date, sujet = "", nom.replace("-", " ")
    return date, sujet.capitalize()


def page(dossier, fichiers, suite=None, total=None):
    date, sujet = titre_du_dossier(dossier.name)
    p = Image.new("RGB", (LARGE, HAUT), C["creme"])
    d = ImageDraw.Draw(p)
    entete = "%s · %d planches" % (date.upper(), total or len(fichiers))
    if suite:
        entete += " · %d/%d" % suite
    d.text((MARGE, MARGE), entete, font=police("Inter-800.ttf", 40),
           fill=C["taupe"])
    d.text((MARGE, MARGE + 70), sujet, font=police("Playfair-700.ttf", 92),
           fill=C["encre"])
    d.text((MARGE, MARGE + 200), dossier.name, font=police("Inter-400.ttf", 38),
           fill=C["brun"])
    d.line([MARGE, MARGE + 280, LARGE - MARGE, MARGE + 280],
           fill=C["sable_fonce"], width=4)

    premiere = Image.open(fichiers[0])
    ratio = premiere.height / premiere.width
    y = MARGE + 360
    dispo_l = LARGE - 2 * MARGE
    dispo_h = HAUT - y - MARGE - 90
    ecart, legende = 40, 70

    # On choisit le nombre de colonnes qui donne la plus GRANDE planche,
    # en tenant compte de la hauteur disponible et pas seulement de la
    # largeur : a ne regarder que la largeur, un carrousel de sept tenait
    # en quatre colonnes sur deux rangs et laissait la moitie de la page
    # vide. Une planche-contact a moitie vide ne sert pas a relire.
    meilleur = None
    for col in (2, 3, 4):
        lignes = (len(fichiers) + col - 1) // col
        par_large = (dispo_l - (col - 1) * ecart) / col
        par_haut = (dispo_h / lignes - legende - ecart) / ratio
        lg = int(min(par_large, par_haut))
        if lg > 0 and (meilleur is None or lg > meilleur[1]):
            meilleur = (col, lg)
    col, larg = meilleur

    for i, f in enumerate(fichiers):
        im = Image.open(f)
        h = int(im.height * larg / im.width)
        im = im.resize((larg, h), Image.LANCZOS)
        x = MARGE + (i % col) * (larg + ecart)
        yy = int(y + (i // col) * (larg * ratio + legende + ecart))
        p.paste(im, (x, yy))
        d.rectangle([x, yy, x + larg, yy + h], outline=C["sable_fonce"],
                    width=3)
        d.text((x, yy + h + 14), f.stem, font=police("Inter-600.ttf", 34),
               fill=C["taupe"])

    d.text((MARGE, HAUT - MARGE - 40),
           "Grafycom · planche-contact · à valider ou à corriger planche "
           "par planche", font=police("Inter-400.ttf", 34), fill=C["taupe"])
    return p


def main():
    filtre = sys.argv[1] if len(sys.argv) > 1 else ""
    if not VISUELS.exists():
        sys.exit("Aucun visuel. Lancer d'abord : python3 reseaux/visuels.py --tout")
    dossiers = sorted(d for d in VISUELS.iterdir()
                      if d.is_dir() and filtre in d.name
                      and d.name not in IGNORES and any(d.glob("*.png")))
    if not dossiers:
        sys.exit("Aucun dossier ne correspond à « %s »." % filtre)

    pages = []
    for dossier in dossiers:
        fichiers = sorted(dossier.glob("*.png"))
        lots = [fichiers[i:i + PAR_PAGE]
                for i in range(0, len(fichiers), PAR_PAGE)]
        for n, lot in enumerate(lots, 1):
            pages.append(page(dossier, lot,
                              (n, len(lots)) if len(lots) > 1 else None,
                              len(fichiers)))
        print("  %-34s %2d planches%s"
              % (dossier.name, len(fichiers),
                 " sur %d pages" % len(lots) if len(lots) > 1 else ""))

    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    pages[0].save(SORTIE, "PDF", resolution=300, save_all=True,
                  append_images=pages[1:])
    print("\n%d pages — %s (%.1f Mo)"
          % (len(pages), SORTIE, SORTIE.stat().st_size / 1e6))


if __name__ == "__main__":
    main()
