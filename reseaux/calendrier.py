#!/usr/bin/env python3
"""Squelette de calendrier éditorial : les dates et la rotation des piliers.

Ce script ne rédige rien — écrire les légendes est un travail de langue,
pas de boucle. Il produit la grille vide : quelles dates, quel pilier, quel
jeu de hashtags, dans quel ordre. Le reste se remplit à la main ou se
demande à l'assistant, avec la formule donnée dans LIGNE-EDITORIALE.md.

Usage :
    python3 reseaux/calendrier.py --mois 2026-11
    python3 reseaux/calendrier.py --mois 2026-11 --jours lun,jeu
"""

from __future__ import annotations

import argparse
import calendar
import csv
import datetime as dt
import pathlib
import sys

JOURS = {"lun": 0, "mar": 1, "mer": 2, "jeu": 3, "ven": 4, "sam": 5, "dim": 6}
NOMS_JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi",
              "dimanche"]
NOMS_MOIS = ["", "janvier", "février", "mars", "avril", "mai", "juin",
             "juillet", "août", "septembre", "octobre", "novembre",
             "décembre"]

# Mardi : on apprend quelque chose. Vendredi : on montre.
# La rotation évite que deux publications du même pilier se suivent.
ROTATION_APPREND = ["Le regard", "Le territoire", "Le regard", "La personne"]
ROTATION_MONTRE = ["Les coulisses", "Les réalisations", "Les coulisses",
                   "Le territoire"]

FORMATS = {
    "Le regard": "carrousel 3 à 5 vues",
    "Les coulisses": "photo simple ou reel court",
    "Le territoire": "carrousel 3 vues",
    "Les réalisations": "avant / après",
    "La personne": "photo simple",
}
JEUX = {
    "Le regard": "B — métier",
    "Les coulisses": "B — métier",
    "Le territoire": "A — local",
    "Les réalisations": "A — local",
    "La personne": "A — local",
}

RACINE = pathlib.Path(__file__).resolve().parent


def dates_du_mois(annee: int, mois: int, jours: list[int]) -> list[dt.date]:
    nb = calendar.monthrange(annee, mois)[1]
    toutes = (dt.date(annee, mois, j) for j in range(1, nb + 1))
    return [d for d in toutes if d.weekday() in jours]


def main() -> int:
    a = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--mois", required=True, metavar="AAAA-MM",
                   help="le mois à préparer, par exemple 2026-11")
    a.add_argument("--jours", default="mar,ven",
                   help="jours de publication (défaut : mar,ven)")
    args = a.parse_args()

    try:
        annee, mois = (int(x) for x in args.mois.split("-"))
        dt.date(annee, mois, 1)
    except ValueError:
        print(f"Mois illisible : « {args.mois} ». Attendu : AAAA-MM.",
              file=sys.stderr)
        return 1

    try:
        jours = [JOURS[j.strip().lower()[:3]] for j in args.jours.split(",")]
    except KeyError as mauvais:
        print(f"Jour inconnu : {mauvais}. Au choix : {', '.join(JOURS)}.",
              file=sys.stderr)
        return 1

    dates = dates_du_mois(annee, mois, sorted(jours))
    if not dates:
        print("Aucune date : vérifiez --jours.", file=sys.stderr)
        return 1

    premier = min(jours)
    lignes = []
    for n, d in enumerate(dates):
        apprend = d.weekday() == premier
        rotation = ROTATION_APPREND if apprend else ROTATION_MONTRE
        pilier = rotation[(n // len(jours)) % len(rotation)]
        lignes.append({
            "n": n + 1,
            "date": d.isoformat(),
            "jour": NOMS_JOURS[d.weekday()],
            "pilier": pilier,
            "intention": "on apprend quelque chose" if apprend else "on montre",
            "format": FORMATS[pilier],
            "hashtags": JEUX[pilier],
            "sujet": "",
            "etat": "à écrire",
        })

    base = f"calendrier-{annee}-{mois:02d}"
    chemin_csv = RACINE / f"{base}.csv"
    with chemin_csv.open("w", encoding="utf-8-sig", newline="") as f:
        ecrivain = csv.DictWriter(f, fieldnames=list(lignes[0]))
        ecrivain.writeheader()
        ecrivain.writerows(lignes)

    md = [f"# Calendrier éditorial — {NOMS_MOIS[mois]} {annee}", "",
          f"{len(lignes)} publications. Grille vide : les sujets et les textes "
          "restent à écrire — voir `LIGNE-EDITORIALE.md` pour la formule à me "
          "donner.", ""]
    for l in lignes:
        d = dt.date.fromisoformat(l["date"])
        md += [f"## {l['n']} · {l['jour'].capitalize()} {d.day} "
               f"{NOMS_MOIS[d.month]} — {l['pilier']}",
               f"**Format** {l['format']} · **Hashtags** jeu {l['hashtags']} "
               f"· *{l['intention']}*", "",
               "**Visuel** — à définir", "",
               "**Texte alternatif** — à écrire", "",
               "> Texte à écrire.", "", "---", ""]

    chemin_md = RACINE / f"{base}-squelette.md"
    chemin_md.write_text("\n".join(md), encoding="utf-8")

    print(f"{len(lignes)} créneaux, du {dates[0]:%d/%m} au {dates[-1]:%d/%m}.")
    for l in lignes:
        d = dt.date.fromisoformat(l["date"])
        print(f"  {l['jour']:9s} {d.day:2d}  {l['pilier']}")
    print(f"\n  {chemin_csv}\n  {chemin_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
