#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prépare une photo pour le site ou pour les réseaux sociaux.

Recadre au format demandé, convertit, contrôle le poids. Le recadrage
n'est pas centré bêtement : on indique le point d'intérêt de la photo en
fraction de sa hauteur — et, pour les formats verticaux, de sa largeur —
parce que le sujet est rarement au milieu. Une enseigne est en haut, un
plan de travail est en bas.

    python3 reseaux/recadrer.py source.jpg enseigne              # article
    python3 reseaux/recadrer.py source.jpg vitrine --post        # 1080x1350
    python3 reseaux/recadrer.py source.jpg vitrine --story       # 1080x1920
    python3 reseaux/recadrer.py source.jpg vitrine --tous        # les trois
    python3 reseaux/recadrer.py source.jpg enseigne 0.42         # point de visée

Le point de visée va de 0 (le haut de la photo) à 1 (le bas) ; 0.5 par
défaut. Avec --cote, on vise aussi horizontalement, utile quand le sujet
est à gauche ou à droite et que le format coupe les bords.

LES FORMATS, ET POURQUOI CEUX-LÀ
  article  1200x630   l'aperçu quand on partage un lien
  post     1080x1350  le carrousel et le post Instagram ou Facebook
  story    1080x1920  la story et le reel

Ce sont ceux que fixe le cahier des charges. Instagram accepte d'autres
tailles mais recompresse ce qu'on lui donne : partir du bon format évite
de lui laisser décider.
"""

import sys
from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parent.parent

# nom : (largeur, hauteur, dossier de sortie, format, qualité, poids max en Ko)
FORMATS = {
    "article": (1200, 630, RACINE / "assets" / "img" / "blog", "WEBP", 82, 200),
    "post":    (1080, 1350, RACINE / "reseaux" / "visuels", "JPEG", 90, 900),
    "story":   (1080, 1920, RACINE / "reseaux" / "visuels", "JPEG", 90, 900),
}


def recadrer(source, nom, format_="article", focale=0.5, cote=0.5):
    large, haut, dossier, codec, qualite, poids_max = FORMATS[format_]
    im = Image.open(source)
    # Une photo en PNG transparent poserait du noir en JPEG : on l'aplatit
    # sur du blanc plutot que de laisser Pillow decider.
    if im.mode in ("RGBA", "LA", "P"):
        fond = Image.new("RGB", im.size, (255, 255, 255))
        im = im.convert("RGBA")
        fond.paste(im, mask=im.split()[-1])
        im = fond
    else:
        im = im.convert("RGB")

    l, h = im.size
    vise = large / haut

    if l / h > vise:
        # Trop large : on rogne les côtés autour du point de visée latéral.
        nl = int(h * vise)
        x = int(l * cote - nl / 2)
        x = max(0, min(x, l - nl))
        im = im.crop((x, 0, x + nl, h))
    else:
        # Trop haute : on rogne en hauteur autour du point d'intérêt.
        nh = int(l / vise)
        y = int(h * focale - nh / 2)
        y = max(0, min(y, h - nh))
        im = im.crop((0, y, l, y + nh))

    if im.size[0] < large:
        print("  attention : la source est plus petite que le format "
              "demandé (%d px de large pour %d). L'image sera floue."
              % (im.size[0], large))

    im = im.resize((large, haut), Image.LANCZOS)
    dossier.mkdir(parents=True, exist_ok=True)
    suffixe = {"WEBP": "webp", "JPEG": "jpg"}[codec]
    fichier = nom if format_ == "article" else "%s-%s" % (nom, format_)
    chemin = dossier / ("%s.%s" % (fichier, suffixe))
    im.save(chemin, codec, quality=qualite, method=6) if codec == "WEBP" \
        else im.save(chemin, codec, quality=qualite, optimize=True)
    ko = chemin.stat().st_size // 1024
    print("  %-26s %dx%d  %d Ko" % (chemin.name, large, haut, ko))
    if ko > poids_max:
        print("    attention : %d Ko, c'est lourd pour ce format." % ko)
    return chemin


def main(args):
    if len(args) < 2:
        raise SystemExit(__doc__)
    source, nom = args[0], args[1]
    reste = args[2:]

    demandes = [f for f in ("article", "post", "story") if "--" + f in reste]
    if "--tous" in reste:
        demandes = ["article", "post", "story"]
    if not demandes:
        demandes = ["article"]

    nombres = [x for x in reste if not x.startswith("--")]
    focale = float(nombres[0]) if nombres else 0.5
    cote = float(nombres[1]) if len(nombres) > 1 else 0.5
    if "--cote" in reste and len(nombres) > 1:
        cote = float(nombres[1])

    for f in demandes:
        recadrer(source, nom, f, focale, cote)


if __name__ == "__main__":
    main(sys.argv[1:])
