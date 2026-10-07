# -*- coding: utf-8 -*-
"""La charte graphique, lue dans la feuille de style du site.

RÈGLE
-----
Toute la communication de Grafycom — réseaux sociaux, fiche Google, blog,
documents imprimés — se décline d'après la charte du site. Ce module est
le seul endroit où cette charte est définie, et il ne la définit même pas :
il la LIT dans assets/style.css. La feuille de style du site reste donc
l'unique source de vérité, et rien ne peut diverger d'elle sans diverger
du site lui-même.

POURQUOI
--------
Avant ce module, la palette était recopiée à la main dans
reseaux/visuels.py, sous un commentaire qui disait « reprise des variables
CSS du site ». Elle avait déjà dérivé. Mesuré le 7 octobre 2026 :

  jaune       le script écrivait #f5e6a8, le site dit #f9c33f
              — même nom, deux couleurs. C'est la dérive la plus
              traîtresse : rien ne la signale, et les visuels partaient
              avec un jaune pâle là où le site a un jaune d'or.
  vert        #3a6b4a dans le script, introuvable dans la charte.
  neuf        bleu-vif, turquoise, magenta, orange, crème-rosé, sable,
  absentes    sable foncé, taupe, brun clair : jamais recopiées, donc
              jamais utilisables.

Une charte recopiée dérive toujours. Une charte lue ne le peut pas.

USAGE
-----
    from charte import C, rvb, DEGRADE, couleur

    C["violet"]        -> "#a86cd0"
    rvb("violet")      -> (168, 108, 208)
    couleur("vert")    -> arrête le programme : hors charte

    python3 charte.py              affiche la charte
    python3 charte.py --verifier   contrôle qu'aucun fichier n'écrit une
                                   couleur en dur hors charte
"""

import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CSS = RACINE / "assets" / "style.css"


def _lire_root():
    """Extrait le bloc :root de la feuille de style."""
    if not CSS.exists():
        raise SystemExit(f"charte introuvable : {CSS}")
    texte = CSS.read_text(encoding="utf-8")
    i = texte.find(":root")
    if i < 0:
        raise SystemExit(f"pas de bloc :root dans {CSS}")
    return texte[i:texte.index("}", i)]


_ROOT = _lire_root()


# --------------------------------------------------------------- couleurs

def _couleurs():
    """Les variables de couleur, nom Python (tiret -> souligné)."""
    trouve = {}
    for nom, val in re.findall(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{6})\b", _ROOT):
        trouve[nom.replace("-", "_")] = val.lower()
    if not trouve:
        raise SystemExit("aucune couleur lue dans :root — la CSS a changé de forme")
    return trouve


C = _couleurs()

# Les deux familles, pour qui veut piocher sans se tromper de registre.
# L'aquarelle du logo sert aux accents ; la base chaude sert aux fonds et
# au texte. Un fond pris dans l'aquarelle, et le visuel crie.
AQUARELLE = [n for n in ("bleu", "bleu_vif", "turquoise", "violet", "rose",
                         "magenta", "corail", "orange", "jaune") if n in C]
BASE = [n for n in ("creme", "creme_rose", "sable", "sable_fonce", "taupe",
                    "brun", "brun_clair", "encre", "blanc") if n in C]


def couleur(nom):
    """La valeur d'une couleur de la charte. Refuse tout le reste.

    C'est ici que la règle devient une contrainte : une couleur qui n'est
    pas dans la feuille de style du site ne peut pas être employée, et le
    programme s'arrête au lieu de produire un visuel hors charte.
    """
    if nom in C:
        return C[nom]
    if isinstance(nom, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", nom or ""):
        raise SystemExit(
            f"couleur en dur refusée : {nom}\n"
            "La charte se décline depuis assets/style.css. Pour ajouter une "
            "couleur, l'ajouter d'abord au bloc :root du site.")
    proches = [n for n in C if nom and n.startswith(str(nom)[:3])]
    raise SystemExit(
        f"couleur hors charte : « {nom} »\n"
        + (f"Vouliez-vous dire : {', '.join(proches)} ?\n" if proches else "")
        + f"Couleurs disponibles : {', '.join(sorted(C))}")


def rvb(nom):
    h = couleur(nom).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cmjn(nom):
    """Conversion indicative vers CMJN, pour une commande d'impression.

    Indicative, et le mot compte : la conversion exacte dépend du profil
    ICC du papier et de la presse. Ces valeurs servent à remplir un bon de
    commande et à discuter avec l'imprimeur, pas à valider un bon à tirer.
    Pour une couleur qui doit être rigoureusement identique d'un support à
    l'autre — le logo —, on désigne un Pantone, pas un CMJN.
    """
    r, v, b = (x / 255 for x in rvb(nom))
    k = 1 - max(r, v, b)
    if k >= 1:
        return (0, 0, 0, 100)
    c = (1 - r - k) / (1 - k)
    m = (1 - v - k) / (1 - k)
    j = (1 - b - k) / (1 - k)
    return tuple(round(x * 100) for x in (c, m, j, k))


# ---------------------------------------------------------------- dégradé

def _degrade():
    """Les arrêts de --degrade, le dégradé arc-en-ciel du logo.

    Les arrêts citent les variables (var(--bleu) 0%, ...), on les résout
    donc contre C : là encore, aucune valeur n'est recopiée.
    """
    m = re.search(r"--degrade:\s*linear-gradient\(([^;]+)\);", _ROOT, re.S)
    if not m:
        return []
    arrets = []
    for var, pos in re.findall(r"var\(--([a-z0-9-]+)\)\s*([0-9.]+)%",
                               m.group(1)):
        nom = var.replace("-", "_")
        if nom in C:
            arrets.append((float(pos) / 100, C[nom]))
    return arrets


DEGRADE = _degrade()


# --------------------------------------------------------------- polices

# Lues dans l'appel Google Fonts du site : elles doivent rester celles-là.
POLICES = {
    "titre": ("Playfair Display", "serif", "Titres et chiffres marquants"),
    "texte": ("Inter", "sans-serif", "Texte courant, légendes, boutons"),
    "manuscrit": ("Caveat", "cursive", "Surtitres, notes manuscrites"),
    "mono": ("Courier Prime", "monospace", "Mentions techniques, repères"),
}

# Fichiers .ttf employés par le générateur de visuels.
FONTES = {
    "titre": ["Playfair-800", "Playfair-700", "Playfair-500"],
    "texte": ["Inter-800", "Inter-600", "Inter-400"],
    "manuscrit": ["Caveat"],
}


# --------------------------------------------------------------- contrôle

# Fichiers qui ont le droit d'écrire une couleur en dur : la feuille de
# style, qui EST la charte, et le présent module, qui la lit.
DISPENSES = {"assets/style.css", "generateurs/charte.py"}

# Couleurs techniques tolérées partout : noir et blanc purs, et les
# notations courtes.
TOLEREES = {"#000000", "#ffffff", "#fff", "#000"}


def verifier():
    """Cherche les couleurs écrites en dur hors de la charte.

    Parcourt les scripts du dépôt — pas les pages HTML, qui sont
    produites par les générateurs et dont les quelques couleurs en ligne
    viennent déjà des variables CSS.
    """
    souci = 0
    valeurs = set(C.values())
    for f in sorted(RACINE.rglob("*.py")):
        rel = f.relative_to(RACINE).as_posix()
        if rel in DISPENSES or "/_" in rel or rel.startswith("dist/"):
            continue
        dans_docstring = False
        for n, ligne in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            # Un commentaire ou une docstring peut citer une couleur
            # pour l'expliquer — y compris celles que ce contrôle a
            # servi à débusquer. On ne lit que le code.
            if ligne.count('"""') == 1:
                dans_docstring = not dans_docstring
                continue
            if dans_docstring or ligne.lstrip().startswith("#"):
                continue
            for h in re.findall(r"#[0-9a-fA-F]{6}\b", ligne):
                if h.lower() in valeurs or h.lower() in TOLEREES:
                    continue
                print(f"  {rel}:{n}  {h}  hors charte")
                souci += 1
    if souci:
        print(f"\n{souci} couleur(s) hors charte. "
              "Les remplacer par un nom de la charte, ou ajouter la couleur "
              "au bloc :root du site si elle doit en faire partie.")
    else:
        print("Aucune couleur hors charte dans les scripts.")
    return souci


def afficher():
    print(f"CHARTE GRAFYCOM — lue dans {CSS.relative_to(RACINE)}\n")
    print("AQUARELLE DU LOGO — accents, jamais les fonds")
    for n in AQUARELLE:
        c = cmjn(n)
        print(f"  {n:12} {C[n]}   RVB {str(rvb(n)):18} "
              f"CMJN {c[0]:>3} {c[1]:>3} {c[2]:>3} {c[3]:>3}")
    print("\nBASE CHAUDE — fonds, texte, filets")
    for n in BASE:
        c = cmjn(n)
        print(f"  {n:12} {C[n]}   RVB {str(rvb(n)):18} "
              f"CMJN {c[0]:>3} {c[1]:>3} {c[2]:>3} {c[3]:>3}")
    print(f"\nDÉGRADÉ ({len(DEGRADE)} arrêts)")
    print("  " + " → ".join(f"{h} {int(p*100)}%" for p, h in DEGRADE))
    print("\nPOLICES")
    for role, (nom, pile, usage) in POLICES.items():
        print(f"  {role:10} {nom:18} ({pile})  {usage}")
    print("\nCMJN indicatif : la conversion exacte dépend du profil "
          "d'impression.\nPour une couleur du logo, désigner un Pantone.")


if __name__ == "__main__":
    if "--verifier" in sys.argv:
        sys.exit(1 if verifier() else 0)
    afficher()
