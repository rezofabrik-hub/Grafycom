#!/usr/bin/env python3
"""Rend transparent le fond uni d'une image, par diffusion depuis les bords.

Pourquoi pas un simple « tout ce qui est clair devient transparent » : une
aquarelle a des zones presque blanches, un vêtement blanc aussi. Un seuil
global les perce. En partant des bords et en ne se propageant que de
proche en proche, on ne retire que le fond réellement extérieur au sujet.

    python3 outils/detourer.py entree.jpg sortie.webp
    python3 outils/detourer.py portrait.jpg sortie.webp --seuil 246 --largeur 1200

Le résultat est toujours à vérifier à l'œil, sur fond clair ET sur fond
sombre : un halo résiduel ne se voit que sur le second.
"""

from __future__ import annotations

import argparse
import sys
from collections import deque


def detourer(chemin_entree, chemin_sortie, seuil=240, largeur=None,
             adoucir=1.2, qualite=90, bords="tous"):
    from PIL import Image, ImageFilter
    import numpy as np

    src = Image.open(chemin_entree).convert("RGB")
    a = np.asarray(src).astype(np.int16)
    h, w, _ = a.shape

    clair = (a[:, :, 0] >= seuil) & (a[:, :, 1] >= seuil) & (a[:, :, 2] >= seuil)

    fond = np.zeros((h, w), dtype=bool)
    pile = deque()

    def amorcer(y, x):
        if clair[y, x] and not fond[y, x]:
            fond[y, x] = True
            pile.append((y, x))

    lignes = {"haut": [0], "bas": [h - 1]}
    if bords == "tous":
        for x in range(w):
            amorcer(0, x); amorcer(h - 1, x)
        for y in range(h):
            amorcer(y, 0); amorcer(y, w - 1)
    elif bords == "sans-bas":
        # Pour un portrait dont le vêtement clair touche le bord inférieur :
        # partir du bas reviendrait à le manger.
        for x in range(w):
            amorcer(0, x)
        for y in range(h):
            amorcer(y, 0); amorcer(y, w - 1)
    else:
        raise ValueError("bords : « tous » ou « sans-bas »")

    # Propagation par segments : une ligne entière d'un coup, sinon quelques
    # millions de pixels prennent la soirée.
    while pile:
        y, x = pile.popleft()
        g = x
        while g > 0 and clair[y, g - 1] and not fond[y, g - 1]:
            g -= 1; fond[y, g] = True
        d = x
        while d < w - 1 and clair[y, d + 1] and not fond[y, d + 1]:
            d += 1; fond[y, d] = True
        for vy in (y - 1, y + 1):
            if 0 <= vy < h:
                for vx in range(g, d + 1):
                    if clair[vy, vx] and not fond[vy, vx]:
                        fond[vy, vx] = True; pile.append((vy, vx))

    part = fond.sum() / (h * w)
    masque = Image.fromarray(np.where(fond, 0, 255).astype("uint8"))
    if adoucir:
        masque = masque.filter(ImageFilter.GaussianBlur(adoucir))

    out = src.convert("RGBA")
    out.putalpha(masque)
    if largeur and largeur < w:
        out = out.resize((largeur, round(h * largeur / w)), Image.LANCZOS)
    out.save(chemin_sortie, quality=qualite, method=6)
    return part, out.size


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("entree")
    a.add_argument("sortie")
    a.add_argument("--seuil", type=int, default=240,
                   help="à partir de quelle clarté un pixel est du fond (0-255)")
    a.add_argument("--largeur", type=int, help="redimensionner à cette largeur")
    a.add_argument("--adoucir", type=float, default=1.2,
                   help="flou du masque, en pixels ; 0 pour un bord net")
    a.add_argument("--bords", default="tous", choices=["tous", "sans-bas"],
                   help="d'où part la diffusion")
    args = a.parse_args()

    try:
        part, taille = detourer(args.entree, args.sortie, args.seuil,
                                args.largeur, args.adoucir, bords=args.bords)
    except Exception as e:
        print(f"Échec : {e}", file=sys.stderr)
        return 1
    print(f"{args.sortie} — {taille[0]}x{taille[1]}, "
          f"{part:.0%} de l'image rendue transparente.")
    print("À vérifier à l'œil, sur fond clair et sur fond sombre.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
