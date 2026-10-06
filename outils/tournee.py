#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Transforme la liste de veille en tournées de visite ordonnées.

Une liste de 80 adresses dans le désordre ne se visite pas : on traverse
la ville trois fois et on abandonne au bout d'une heure. Ce script
regroupe par commune, puis ordonne chaque groupe par proximité réelle à
partir des coordonnées que la veille récupère désormais.

    python3 outils/tournee.py                      # la veille la plus récente
    python3 outils/tournee.py --note 3             # seulement le meilleur intérêt
    python3 outils/tournee.py --par-tournee 8      # taille d'une demi-journée
    python3 outils/tournee.py --fichier outils/prospects/prospects-66-....csv

Ce qui est écarté d'office, et pourquoi :

- les fiches sans adresse exploitable : on ne se déplace pas à l'aveugle ;
- les entreprises dont le dirigeant s'est opposé à la diffusion de ses
  données — la veille les a déjà retirées ;
- celles de outils/ne-pas-contacter.txt ;
- les notes d'intérêt faibles, par défaut : « activité non publiée » et
  « à qualifier » ne méritent pas un déplacement tant qu'on n'a pas lu de
  quoi il s'agit.

La sortie contient des noms et des adresses de personnes physiques. Elle
va dans outils/prospects/, exclu du dépôt par .gitignore. Elle ne doit
pas en sortir.
"""
import argparse
import csv
import math
import pathlib
import sys
import unicodedata

RACINE = pathlib.Path(__file__).resolve().parent
SORTIE = RACINE / "prospects"

# Le point de départ des tournées : le centre de Perpignan, place de la
# République. On part de là et on déroule au plus proche.
DEPART = (42.6986, 2.8954)


def sans_accent(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn").lower()


def distance(a, b) -> float:
    """Distance approximative en kilomètres entre deux points.

    Formule de la corde plane, suffisante à l'échelle d'un département :
    l'erreur sur 60 km est de quelques dizaines de mètres, et on ne
    cherche qu'un ordre de visite.
    """
    lat = math.radians((a[0] + b[0]) / 2)
    dx = (b[1] - a[1]) * math.cos(lat) * 111.32
    dy = (b[0] - a[0]) * 110.57
    return math.hypot(dx, dy)


def coordonnees(fiche) -> tuple | None:
    brut = (fiche.get("coord") or "").strip()
    if not brut or "," not in brut:
        return None
    try:
        lat, lon = (float(x) for x in brut.split(",", 1))
        return (lat, lon)
    except ValueError:
        return None


def ordonner(fiches, depart=DEPART):
    """Du plus proche au plus proche. Un glouton suffit ici.

    L'optimum du voyageur de commerce n'a aucun intérêt pour huit arrêts
    à pied : le glouton donne un trajet qu'on peut suivre sans réfléchir,
    et c'est tout ce qu'on lui demande.
    """
    restants = list(fiches)
    ordre, point = [], depart
    while restants:
        geo = [f for f in restants if coordonnees(f)]
        if not geo:                       # plus de coordonnées : on garde l'ordre
            ordre.extend(restants)
            break
        suivant = min(geo, key=lambda f: distance(point, coordonnees(f)))
        ordre.append(suivant)
        restants.remove(suivant)
        point = coordonnees(suivant)
    return ordre


def plus_recent() -> pathlib.Path:
    fichiers = sorted(SORTIE.glob("prospects-66-*.csv"))
    if not fichiers:
        sys.exit("ERREUR : aucune veille dans %s.\n"
                 "        Lancer d'abord : python3 outils/veille-entreprises.py "
                 "--quotidien --adresses" % SORTIE)
    return fichiers[-1]


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--fichier", help="le CSV de veille (défaut : le plus récent)")
    a.add_argument("--note", type=int, default=2,
                   help="intérêt minimal retenu, de 1 à 3 (défaut : 2)")
    a.add_argument("--par-tournee", type=int, default=8,
                   help="nombre d'arrêts par demi-journée (défaut : 8)")
    args = a.parse_args()

    chemin = pathlib.Path(args.fichier) if args.fichier else plus_recent()
    fiches = list(csv.DictReader(chemin.open(encoding="utf-8-sig")))

    gardees, ecartees = [], {"sans adresse": 0, "note faible": 0, "non vérifiée": 0}
    for f in fiches:
        if not f.get("adresse"):
            ecartees["sans adresse"] += 1; continue
        if f.get("diffusion") == "non vérifié":
            ecartees["non vérifiée"] += 1; continue
        if int(f.get("note") or 0) < args.note:
            ecartees["note faible"] += 1; continue
        gardees.append(f)

    # Perpignan d'un côté, le reste de l'autre.
    #
    # Grouper strictement par commune donnait 27 tournées pour 26 communes :
    # un arrêt isolé par village, ce qui ne se visite pas. Les communes
    # périphériques sont donc fondues en un seul parcours ordonné par
    # proximité, puis découpé : une demi-journée couvre ainsi plusieurs
    # villages voisins, ce qui est la façon dont on circule réellement.
    perpignan = [f for f in gardees if sans_accent(f["ville"]) == "perpignan"]
    ailleurs = [f for f in gardees if sans_accent(f["ville"]) != "perpignan"]

    groupes = []
    for liste, titre in ((perpignan, "Perpignan"), (ordonner(ailleurs), None)):
        if not liste:
            continue
        liste = ordonner(liste) if titre else liste
        for i in range(0, len(liste), args.par_tournee):
            paquet = liste[i:i + args.par_tournee]
            villes = []
            for f in paquet:
                if f["ville"] not in villes:
                    villes.append(f["ville"])
            nom = titre or " · ".join(villes)
            groupes.append((nom, paquet))

    def km(paquet):
        """Le chemin parcouru, pour savoir si la demi-journée tient."""
        pts = [coordonnees(f) for f in paquet if coordonnees(f)]
        return sum(distance(pts[i], pts[i + 1]) for i in range(len(pts) - 1))

    lignes = [
        "# Tournée de prospection — %s" % chemin.stem.replace("prospects-66-", ""),
        "",
        "%d entreprises retenues sur %d relevées, dans %d communes."
        % (len(gardees), len(fiches),
           len({f["ville"] for f in gardees})),
        "",
        "Écartées : %s." % ", ".join("%d %s" % (v, k) for k, v in ecartees.items() if v),
        "",
        "> **Avant de partir.** Ces entreprises viennent de s'immatriculer :",
        "> beaucoup n'ont pas encore ouvert, et l'adresse est parfois celle du",
        "> domicile du dirigeant. Si c'est une habitation, on ne sonne pas —",
        "> on note et on écrit. Le porte-à-porte, c'est pour les locaux",
        "> commerciaux.",
        "",
        "> **Ce qu'on emporte.** Un carton d'exemples imprimés, pas une",
        "> tablette : on vend de l'imprimé et du physique, autant le montrer.",
        "> Des cartes de visite. Et de quoi noter, parce qu'on ne retient pas",
        "> huit conversations.",
        "",
        "---",
        "",
    ]

    numero = 0
    for nom_groupe, paquet in groupes:
            numero += 1
            d = km(paquet)
            lignes += ["## Tournée %d — %s" % (numero, nom_groupe),
                       "",
                       "%d arrêts · environ %.0f km de trajet%s" % (
                           len(paquet), d,
                           " (à pied)" if d < 3 else ""),
                       ""]
            for n, f in enumerate(paquet, 1):
                nom = f.get("enseigne") or f["nom"]
                lignes.append("**%d. %s**" % (n, nom))
                if f.get("enseigne") and f["enseigne"] != f["nom"]:
                    lignes.append("  *immatriculée sous* %s" % f["nom"])
                lignes.append("  %s" % f["adresse"])
                if f.get("dirigeant") and f["dirigeant"].lower() not in f["nom"].lower():
                    lignes.append("  demander %s" % f["dirigeant"])
                act = f["activite"][:150] + ("…" if len(f["activite"]) > 150 else "")
                lignes.append("  *%s* — %s" % (f["secteur"], act))
                besoin = {
                    "Restauration & bouche": "carte, menu, enseigne, vitrophanie",
                    "Commerce de détail": "enseigne, vitrine, sacs, étiquettes",
                    "Artisanat & bâtiment": "marquage de véhicule, devis, panneau de chantier",
                    "Beauté & bien-être": "enseigne, carte de soins, prise de rendez-vous",
                    "Services de proximité": "logo, carte, marquage de véhicule",
                    "Loisirs & événementiel": "affiche, dépliant, signalétique",
                    "Tourisme & hébergement": "signalétique, dépliant, accueil",
                }.get(f["secteur"], "logo, carte de visite, enseigne")
                lignes.append("  → **à proposer :** %s" % besoin)
                lignes.append("  ☐ visitée   ☐ intéressée   ☐ à relancer   ☐ ne pas recontacter")
                lignes.append("")
            lignes.append("")

    lignes += [
        "---",
        "",
        "## Ce qu'on dit en entrant",
        "",
        "Trente secondes, pas plus. On n'est pas là pour vendre, on est là",
        "pour se faire connaître avant que le besoin arrive.",
        "",
        "> « Bonjour, Sandra, je suis graphiste à Perpignan. J'ai vu que vous",
        "> veniez d'ouvrir. Je passe juste déposer une carte — si un jour vous",
        "> avez besoin d'une enseigne, d'une carte ou d'un menu, vous saurez",
        "> où me trouver. Bonne installation ! »",
        "",
        "Puis on s'en va. Celui qui veut parler vous retiendra ; celui qui est",
        "débordé vous en sera reconnaissant.",
        "",
        "## Après",
        "",
        "Toute personne qui demande à ne plus être sollicitée va dans",
        "`outils/ne-pas-contacter.txt`, le jour même. La veille l'écartera",
        "dès le lendemain.",
    ]

    SORTIE.mkdir(exist_ok=True)
    cible = SORTIE / ("tournee-%s.md" % chemin.stem.replace("prospects-66-", ""))
    cible.write_text("\n".join(lignes), encoding="utf-8")

    print("%d entreprises retenues sur %d" % (len(gardees), len(fiches)))
    for k, v in ecartees.items():
        if v:
            print("  %-14s %d" % (k, v))
    print("\n%d tournées, %d communes couvertes"
          % (numero, len({f["ville"] for f in gardees})))
    print("  %s" % cible)
    return 0


if __name__ == "__main__":
    sys.exit(main())
