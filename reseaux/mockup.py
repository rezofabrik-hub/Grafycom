# -*- coding: utf-8 -*-
"""Fabrique une mise en situation d'un imprimé, à partir de ses faces.

Pourquoi ce fichier existe
--------------------------
Un dépliant montré à plat est un fichier ; montré en volume, c'est un
objet. Sur une publication « réalisations », la différence décide de
tout : le lecteur croit ce qu'il voit posé sur une table, pas ce qu'il
voit en aplat.

Les mises en situation se téléchargent d'ordinaire sous forme de
gabarits Photoshop. Ici, rien à télécharger et aucun droit à vérifier :
la perspective, l'ombre portée et le dégradé de pli sont calculés.

Ce que ce fichier NE fait pas : inventer une pièce. Il met en volume
des faces qu'on lui donne, rien d'autre.

Usage
-----
    python3 reseaux/mockup.py recto.png verso.png sortie.png
"""
import sys
import pathlib

from PIL import Image, ImageDraw, ImageFilter

FOND = (227, 222, 210)          # le gris chaud des mises en situation
OMBRE = (120, 112, 100)


def _coeffs(cible, source):
    """Les 8 coefficients perspective pour PIL, cible -> source.

    PIL lit la transformation à l'envers : pour chaque pixel produit,
    elle demande où le prendre dans la source. Résoudre dans l'autre
    sens donne une image vide, et c'est l'erreur classique.
    """
    A, B = [], []
    for (xc, yc), (xs, ys) in zip(cible, source):
        A.append([xc, yc, 1, 0, 0, 0, -xs * xc, -xs * yc])
        A.append([0, 0, 0, xc, yc, 1, -ys * xc, -ys * yc])
        B += [xs, ys]
    n = 8
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[p] = A[p], A[i]
        B[i], B[p] = B[p], B[i]
        for r in range(n):
            if r == i or A[r][i] == 0:
                continue
            k = A[r][i] / A[i][i]
            A[r] = [a - k * b for a, b in zip(A[r], A[i])]
            B[r] -= k * B[i]
    return [B[i] / A[i][i] for i in range(n)]


def _pli(im, part=0.5, force=0.16, largeur=0.34, creux=True):
    """Assombrit le papier de part et d'autre d'un pli.

    Sans ça, une face pliée reste deux rectangles collés. Le creux
    s'assombrit des deux côtés de la ligne de pli, pas seulement d'un,
    parce que c'est ainsi qu'une feuille se courbe ; `creux=False`
    donne le dégradé simple d'un volet qui s'éloigne.
    """
    l, h = im.size
    voile = Image.new("L", (l, h), 0)
    d = ImageDraw.Draw(voile)
    x = int(l * part)
    etendue = max(1, int(l * largeur))
    for dx in range(-etendue, etendue + 1):
        xx = x + dx
        if not (0 <= xx < l):
            continue
        t = 1 - abs(dx) / etendue
        if not creux and dx > 0:
            t = 0
        d.line([(xx, 0), (xx, h)], fill=int(255 * force * t ** 1.8))
    noir = Image.new("RGBA", (l, h), (0, 0, 0, 255))
    noir.putalpha(voile)
    return Image.alpha_composite(im.convert("RGBA"), noir)


def _poser(planche, face, quad, flou=26, decalage=(16, 22), opacite=104):
    """Pose une face sur la planche selon un quadrilatère, avec son ombre.

    L'ombre est la SILHOUETTE transformée, pas un rectangle flou posé
    dessous : une face en perspective n'a pas une ombre rectangulaire.
    """
    L, H = planche.size
    l, h = face.size
    coef = _coeffs(quad, [(0, 0), (l, 0), (l, h), (0, h)])
    gauche = Image.new("RGBA", (L, H), (0, 0, 0, 0))
    gauche.paste(face.convert("RGBA"), (0, 0))
    tordue = gauche.transform((L, H), Image.PERSPECTIVE, coef, Image.BICUBIC)

    silhouette = Image.new("L", (l, h), 255)
    sg = Image.new("L", (L, H), 0)
    sg.paste(silhouette, (0, 0))
    so = sg.transform((L, H), Image.PERSPECTIVE, coef, Image.BICUBIC)
    so = so.filter(ImageFilter.GaussianBlur(flou)).point(
        lambda v: int(v * opacite / 255))
    ombre = Image.new("RGBA", (L, H), OMBRE + (255,))
    ombre.putalpha(so)
    planche.alpha_composite(
        Image.new("RGBA", (L, H), (0, 0, 0, 0)))
    decale = Image.new("RGBA", (L, H), (0, 0, 0, 0))
    decale.paste(ombre, decalage, ombre)
    planche.alpha_composite(decale)
    planche.alpha_composite(tordue)
    return planche


def depliant(recto, verso, sortie, large=1700, haut=1150):
    """Un dépliant en volume : une face pliée debout, une face ouverte.

    La composition reprend celle qu'on voit partout pour un trois-volets
    — l'ouvert au premier plan en bas à gauche, le plié en retrait en
    haut à droite — parce que c'est celle qui montre les deux faces sans
    que l'une cache l'autre.
    """
    planche = Image.new("RGBA", (large, haut), FOND + (255,))

    # la face pliée, en retrait : deux volets qui forment un V ouvert
    r = Image.open(recto).convert("RGBA")
    l, h = r.size
    gauche_src = r.crop((0, 0, int(l * 0.62), h))
    droite_src = r.crop((int(l * 0.62), 0, l, h))
    _poser(planche, _pli(gauche_src, part=1.0, force=0.19,
                        largeur=0.5, creux=False),
           [(840, 128), (1245, 86), (1245, 492), (848, 512)], flou=22,
           decalage=(14, 18), opacite=92)
    _poser(planche, droite_src,
           [(1245, 86), (1512, 150), (1512, 556), (1245, 492)], flou=22,
           decalage=(14, 18), opacite=92)

    # la face ouverte, au premier plan, à plat et légèrement tournée
    v = Image.open(verso).convert("RGBA")
    v = _pli(v, part=0.5, force=0.20, largeur=0.16)
    _poser(planche, v,
           [(118, 404), (1012, 470), (896, 1040), (96, 896)], flou=30,
           decalage=(18, 26), opacite=116)

    planche.convert("RGB").save(sortie)
    return sortie


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__.strip().split("Usage")[-1].strip())
    recto, verso, sortie = (pathlib.Path(a) for a in sys.argv[1:])
    for f in (recto, verso):
        if not f.exists():
            raise SystemExit("fichier introuvable : %s" % f)
    print(depliant(recto, verso, sortie))


if __name__ == "__main__":
    main()
