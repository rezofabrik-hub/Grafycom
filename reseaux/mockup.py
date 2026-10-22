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
    python3 reseaux/mockup.py recto.png verso.png sortie.png [depliant|feuillet]
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


def depliant(recto, verso, sortie, large=1700, haut=1150, pli=0.5):
    """Un pli roulé debout, et la face intérieure ouverte devant.

    `pli` dit où la pliure tombe, en fraction de la largeur : 0.5 pour
    une feuille pliée en deux. Mal placée, la pliure coupe un bloc au
    milieu et le volume se voit faux — c'est le premier défaut à
    corriger sur une mise en situation.

    Le volet de COUVERTURE est celui de droite, et c'est lui qu'on
    place presque de face : c'est la page qu'on lit en premier dans la
    vraie vie, et la mettre en fuite rend l'image illisible.
    """
    planche = Image.new("RGBA", (large, haut), FOND + (255,))

    r = Image.open(recto).convert("RGBA")
    l, h = r.size
    x = int(l * pli)
    dos_src = r.crop((0, 0, x, h))            # le volet qui part en arrière
    couv_src = r.crop((x, 0, l, h))           # la couverture

    # le dos d'abord : il est derrière, et sa pliure s'assombrit
    _poser(planche, _pli(dos_src, part=1.0, force=0.22, largeur=0.55,
                         creux=False),
           [(872, 212), (1148, 112), (1148, 584), (872, 650)], flou=22,
           decalage=(14, 18), opacite=88)
    # la couverture ensuite, presque de face
    _poser(planche, _pli(couv_src, part=0.0, force=0.14, largeur=0.3,
                         creux=False),
           [(1148, 112), (1556, 168), (1556, 640), (1148, 584)], flou=24,
           decalage=(16, 22), opacite=96)

    # la face intérieure, ouverte à plat au premier plan
    v = Image.open(verso).convert("RGBA")
    v = _pli(v, part=pli, force=0.20, largeur=0.14)
    _poser(planche, v,
           [(112, 420), (1016, 492), (952, 1064), (78, 944)], flou=32,
           decalage=(18, 28), opacite=120)

    planche.convert("RGB").save(sortie)
    return sortie


def feuillet(recto, verso, sortie, large=1700, haut=1150):
    """Deux faces d'un imprimé à plat, posées l'une devant l'autre.

    Pour une pièce qui NE SE PLIE PAS. Un dépliant plié montre son
    volume ; un feuillet n'en a pas, et lui en inventer un se voit :
    la pliure tombe au milieu d'un bloc, et le volet qui porte le logo
    part en arrière alors que c'est lui qu'on doit lire en premier.

    La face de couverture passe donc devant, bien posée, et le verso
    derrière, décalé — c'est ainsi qu'on pose deux feuilles sur une
    table quand on veut montrer les deux.
    """
    planche = Image.new("RGBA", (large, haut), FOND + (255,))

    # le verso en retrait, plus incliné : il se lit en second
    v = Image.open(verso).convert("RGBA")
    _poser(planche, v,
           [(742, 96), (1562, 208), (1498, 724), (686, 588)], flou=26,
           decalage=(16, 22), opacite=96)

    # le recto au premier plan, presque de face : c'est lui qu'on lit
    r = Image.open(recto).convert("RGBA")
    _poser(planche, r,
           [(128, 420), (1022, 500), (962, 1066), (86, 950)], flou=34,
           decalage=(20, 30), opacite=122)

    planche.convert("RGB").save(sortie)
    return sortie


def main():
    if len(sys.argv) not in (4, 5):
        raise SystemExit(__doc__.strip().split("Usage")[-1].strip())
    forme = depliant
    if len(sys.argv) == 5:
        forme = {"depliant": depliant, "feuillet": feuillet}[sys.argv[4]]
    recto, verso, sortie = (pathlib.Path(a) for a in sys.argv[1:4])
    for f in (recto, verso):
        if not f.exists():
            raise SystemExit("fichier introuvable : %s" % f)
    print(forme(recto, verso, sortie))


if __name__ == "__main__":
    main()
