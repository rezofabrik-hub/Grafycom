#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prépare une photo pour un en-tête d'article.

Recadre au format 1200x630 — celui des aperçus de partage —, convertit en
WebP et contrôle le poids. Le recadrage n'est pas centré bêtement : on
indique le point d'intérêt de la photo en fraction de sa hauteur, parce
que le sujet est rarement au milieu. Une enseigne est en haut, un plan de
travail est en bas.

    python3 reseaux/recadrer.py source.jpg enseigne 0.42

Le troisième argument est facultatif (0.5 par défaut) : 0 = le haut de la
photo, 1 = le bas.
"""

import sys
from pathlib import Path

from PIL import Image

LARGE, HAUT = 1200, 630
SORTIE = Path(__file__).resolve().parent.parent / "assets" / "img" / "blog"


def recadrer(source, nom, focale=0.5, qualite=82):
    im = Image.open(source).convert("RGB")
    l, h = im.size
    vise = LARGE / HAUT

    if l / h > vise:
        # Trop large : on rogne les côtés, en gardant le centre.
        nl = int(h * vise)
        x = (l - nl) // 2
        im = im.crop((x, 0, x + nl, h))
    else:
        # Trop haute : on rogne en hauteur autour du point d'intérêt.
        nh = int(l / vise)
        y = int(h * focale - nh / 2)
        y = max(0, min(y, h - nh))
        im = im.crop((0, y, l, y + nh))

    im = im.resize((LARGE, HAUT), Image.LANCZOS)
    SORTIE.mkdir(parents=True, exist_ok=True)
    chemin = SORTIE / f"{nom}.webp"
    im.save(chemin, "WEBP", quality=qualite, method=6)
    ko = chemin.stat().st_size // 1024
    print(f"  {chemin.name:22} {LARGE}x{HAUT}  {ko} Ko")
    if ko > 200:
        print(f"    attention : {ko} Ko, c'est lourd pour un en-tête.")
    return chemin


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    recadrer(sys.argv[1], sys.argv[2],
             float(sys.argv[3]) if len(sys.argv) > 3 else 0.5)
