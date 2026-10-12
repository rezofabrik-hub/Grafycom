#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Décale tout le calendrier de publication, d'un bloc.

Pourquoi un outil plutôt qu'un chercher-remplacer
--------------------------------------------------
Les dates sont écrites sous quatre formes dans neuf documents et sept
articles : « lundi 12 octobre », « 12 octobre », « 12 oct », et
« 2026-10-12 » dans les noms de fichiers du blog et leurs en-têtes. Un
décalage demande de recalculer le jour de la semaine, pas seulement le
quantième — « lundi 12 octobre » décalé de sept jours devient « lundi 19
octobre », mais décalé de trois jours il devient « jeudi 15 octobre ».

Deux garde-fous, et ce sont eux qui justifient le fichier :

1. **Les dates ancrées ne bougent pas.** Le 24 décembre est l'échéance de
   Noël, le 1er juillet 2026 la péremption du Cerfa 14798*01, le 11
   novembre l'Armistice, le 31 octobre Halloween. Décaler ces dates
   produirait des énoncés faux.

2. **Les contenus saisonniers sont signalés.** Un reel sur Halloween publié
   le 30 octobre garde son sens ; publié le 6 novembre, il n'en a plus. Le
   programme ne tranche pas à ta place : il liste les conflits.

Usage
-----
    python3 reseaux/decaler.py --jours 7            # simulation
    python3 reseaux/decaler.py --depart 2026-10-19  # idem, par date
    python3 reseaux/decaler.py --jours 7 --appliquer

Sans --appliquer, rien n'est écrit : le programme affiche ce qu'il ferait.
"""
import argparse
import datetime as dt
import io
import pathlib
import re
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parent
ANNEE = 2026
DEPART_ACTUEL = dt.date(2026, 10, 12)

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi",
         "dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]
COURTS = ["janv", "févr", "mars", "avr", "mai", "juin", "juil", "août",
          "sept", "oct", "nov", "déc"]

# Les dates qui disent un fait, pas un créneau. Elles ne bougent jamais.
ANCREES = {
    (12, 24): "l'échéance de Noël",
    (11, 11): "l'Armistice — le jour sans publication",
    (7, 1):   "la péremption du Cerfa 14798*01",
    (1, 4):   "la réouverture inventée de la carte de vœux n° 19",
    (11, 24): "le dernier jour calculé pour lancer la création",
    (10, 31): "Halloween",
}

# Une date peut aussi dire QUAND quelque chose a été fait. « Corrigée le
# 12 octobre », « en ligne depuis le 7 octobre » : décaler ces mentions
# réécrirait l'histoire du projet. On les reconnaît à ce qui les précède.
PROVENANCE = re.compile(
    r"(?:ajout|remplac|corrig|tranch|donn|d[ée]cid|[ée]crit|mesur|v[ée]rifi"
    r"|constat|relev)[ée]?e?s?\s+le\s*$"
    r"|(?:depuis|jusqu'au|jusqu'\u00e0|avant|apr[èe]s)\s+(?:le\s+)?$"
    r"|(?:\u00c9tat|Etat)\s+au\s+$",
    re.IGNORECASE)


# Ce qui perd son sens si la date de publication s'éloigne de l'événement.
SAISONNIER = [
    ("n° 8, reel Halloween", dt.date(2026, 10, 23), dt.date(2026, 10, 31),
     "un reel sur Halloween publié après le 31 octobre n'a plus d'objet"),
    ("S3-F, story Halloween", dt.date(2026, 10, 31), dt.date(2026, 10, 31),
     "cette story est datée du jour même : elle ne peut pas se décaler"),
    ("n° 16, reel fin d'année", dt.date(2026, 11, 7), dt.date(2026, 12, 24),
     "sa voix off dit la date du jour — elle se décale avec, vérifier le "
     "texte"),
    ("n° 17, rétroplanning", dt.date(2026, 11, 9), dt.date(2026, 11, 24),
     "il dit « cette semaine » pour une échéance au 24 novembre, qui ne "
     "bouge pas"),
]

CIBLES = (sorted((RACINE / "propositions/a-valider").glob("*.md"))
          + sorted((RACINE / "blog").glob("*.md")))

_MOIS_RE = "|".join(MOIS)
_COURTS_RE = "|".join(COURTS)
_JOURS_RE = "|".join(JOURS)

MOTIF = re.compile(
    r"(?P<iso>\b20\d\d-\d\d-\d\d\b)"
    r"|(?P<intervalle>\b\d{1,2}(?:er)? au \d{1,2}(?:er)? (?:%s)\b)" % (
        _MOIS_RE,) + r""
    r"|(?P<jourlong>\b(?:%s) \d{1,2}(?:er)? (?:%s)\b)"
    r"|(?P<long>\b\d{1,2}(?:er)? (?:%s)\b)"
    r"|(?P<court>\b\d{1,2} (?:%s)\.?(?![a-zé]))"
    % (_JOURS_RE, _MOIS_RE, _MOIS_RE, _COURTS_RE),
    re.IGNORECASE)


_INTERVALLE = None   # compile plus bas, une fois _MOIS_RE connu


def _decale_intervalle(brut, jours):
    """« 12 au 18 octobre » : les deux bornes, le mois recalcule.

    Le premier quantieme n'a pas de mois a lui ; il emprunte celui du
    second. Decaler les deux separement produisait « 12 au 25 octobre ».
    """
    m = re.fullmatch(r"(\d{1,2})(?:er)? au (\d{1,2})(?:er)? ([a-zé]+)",
                     brut.strip(), re.IGNORECASE)
    if not m:
        return None
    q1, q2, mot = m.group(1), m.group(2), m.group(3).lower()
    if mot not in MOIS:
        return None
    mo = MOIS.index(mot) + 1
    try:
        d1 = dt.date(ANNEE, mo, int(q1))
        d2 = dt.date(ANNEE, mo, int(q2))
    except ValueError:
        return None
    n1 = d1 + dt.timedelta(days=jours)
    n2 = d2 + dt.timedelta(days=jours)
    g1 = "1er" if n1.day == 1 else str(n1.day)
    g2 = "1er" if n2.day == 1 else str(n2.day)
    if n1.month == n2.month:
        return "%s au %s %s" % (g1, g2, MOIS[n2.month - 1])
    # les bornes ont change de mois : on nomme les deux
    return "%s %s au %s %s" % (g1, MOIS[n1.month - 1], g2,
                               MOIS[n2.month - 1])


def _lit(txt):
    """Rend (date, forme) pour un fragment reconnu, ou (None, None)."""
    t = txt.strip()
    m = re.fullmatch(r"(20\d\d)-(\d\d)-(\d\d)", t)
    if m:
        a, mo, j = (int(x) for x in m.groups())
        return dt.date(a, mo, j), "iso"
    bas = t.lower().replace(" ", " ")
    jour_nomme = None
    for j in JOURS:
        if bas.startswith(j + " "):
            jour_nomme = j
            bas = bas[len(j) + 1:]
            break
    m = re.fullmatch(r"(\d{1,2})(er)? ([a-zé]+)\.?", bas)
    if not m:
        return None, None
    q, _, mot = m.groups()
    if mot in MOIS:
        mo = MOIS.index(mot) + 1
        forme = "jourlong" if jour_nomme else "long"
    elif mot in COURTS:
        mo = COURTS.index(mot) + 1
        forme = "court"
    else:
        return None, None
    try:
        return dt.date(ANNEE, mo, int(q)), forme
    except ValueError:
        return None, None


def _ecrit(d, forme, original):
    point = original.rstrip().endswith(".")
    if forme == "iso":
        return d.isoformat()
    if forme == "court":
        s = "%d %s" % (d.day, COURTS[d.month - 1])
        return s + ("." if point else "")
    q = "1er" if d.day == 1 else str(d.day)
    s = "%s %s" % (q, MOIS[d.month - 1])
    if forme == "jourlong":
        s = "%s %s" % (JOURS[d.weekday()], s)
        if original[:1].isupper():
            s = s[0].upper() + s[1:]
    return s


def decale(texte, jours, journal, fichier):
    def remplace(m):
        brut = m.group(0)
        if m.lastgroup == "intervalle" or m.groupdict().get("intervalle"):
            neuf = _decale_intervalle(brut, jours)
            if neuf and neuf != brut:
                journal["change"].append((fichier, brut, neuf))
                return neuf
            return brut
        d, forme = _lit(brut)
        if d is None:
            return brut
        if (d.month, d.day) in ANCREES:
            journal["ancrees"].add((fichier, brut, ANCREES[(d.month, d.day)]))
            return brut
        if d < DEPART_ACTUEL:
            journal["ancrees"].add((fichier, brut,
                                    "antérieure au calendrier : un fait, "
                                    "pas un créneau"))
            return brut
        if PROVENANCE.search(texte[max(0, m.start() - 40):m.start()]):
            journal["ancrees"].add((fichier, brut,
                                    "mention historique — ce qui la précède "
                                    "dit quand c'est arrivé"))
            return brut
        neuf = _ecrit(d + dt.timedelta(days=jours), forme, brut)
        if neuf != brut:
            journal["change"].append((fichier, brut, neuf))
        return neuf
    return MOTIF.sub(remplace, texte)


def main():
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    g = a.add_mutually_exclusive_group(required=True)
    g.add_argument("--jours", type=int, help="décalage, en jours")
    g.add_argument("--depart", help="nouvelle date de la publication n° 1 "
                                    "(AAAA-MM-JJ)")
    a.add_argument("--appliquer", action="store_true",
                   help="écrit les fichiers ; sans lui, simple simulation")
    args = a.parse_args()

    if args.depart:
        d = dt.date.fromisoformat(args.depart)
        jours = (d - DEPART_ACTUEL).days
    else:
        jours = args.jours
    if jours == 0:
        sys.exit("Décalage nul : rien à faire.")

    neuf_depart = DEPART_ACTUEL + dt.timedelta(days=jours)
    print("Décalage de %+d jours — la publication n° 1 passe du %s %s au "
          "%s %s.\n" % (jours, JOURS[DEPART_ACTUEL.weekday()],
                        DEPART_ACTUEL.strftime("%d/%m"),
                        JOURS[neuf_depart.weekday()],
                        neuf_depart.strftime("%d/%m")))

    if jours % 7:
        print("⚠️  %d jours n'est pas un nombre entier de semaines : chaque\n"
              "    créneau change de jour. La grille du calendrier — pédagogie\n"
              "    le lundi, réglementation le mardi, jeu le jeudi, reel le\n"
              "    vendredi ou samedi — ne tient plus.\n" % jours)

    journal = {"change": [], "ancrees": set()}
    ecritures = []
    for f in CIBLES:
        t = io.open(f, encoding="utf-8").read()
        n = decale(t, jours, journal, f.name)
        if n != t:
            ecritures.append((f, n))

    # les articles du blog portent leur date dans leur nom de fichier
    renommages = []
    for f in sorted((RACINE / "blog").glob("*.md")):
        m = re.match(r"(20\d\d-\d\d-\d\d)(-.*\.md)", f.name)
        if not m:
            continue
        d = dt.date.fromisoformat(m.group(1))
        if (d.month, d.day) in ANCREES:
            continue
        renommages.append((f, f.with_name(
            (d + dt.timedelta(days=jours)).isoformat() + m.group(2))))

    par_fichier = {}
    for fich, av, ap in journal["change"]:
        par_fichier.setdefault(fich, []).append((av, ap))
    print("DATES RÉÉCRITES")
    for fich in sorted(par_fichier):
        ex = par_fichier[fich]
        apercu = ", ".join("%s → %s" % c for c in ex[:2])
        print("  %-34s %3d  (%s…)" % (fich, len(ex), apercu))
    print("  %-34s %3d au total" % ("", len(journal["change"])))

    print("\nFICHIERS DU BLOG RENOMMÉS")
    for av, ap in renommages:
        print("  %s\n    → %s" % (av.name, ap.name))

    print("\nDATES ANCRÉES, LAISSÉES EN PLACE")
    for fich, brut, pourquoi in sorted(journal["ancrees"]):
        print("  %-28s %-22s %s" % (fich, brut, pourquoi))

    print("\nCONTENUS SAISONNIERS À VÉRIFIER")
    souci = False
    for nom, publiee, evenement, note in SAISONNIER:
        neuve = publiee + dt.timedelta(days=jours)
        marque = "  "
        if neuve > evenement:
            marque, souci = "⚠️", True
        print("  %s %-24s %s → %s   %s"
              % (marque, nom, publiee.strftime("%d/%m"),
                 neuve.strftime("%d/%m"), note))
    if souci:
        print("\n  ⚠️  Au moins un contenu passerait après son événement.\n"
              "      À trancher avant d'appliquer : le déplacer, le retirer,\n"
              "      ou le laisser à sa date d'origine.")

    if not args.appliquer:
        print("\n— Simulation. Rien n'a été écrit. Ajouter --appliquer.")
        return

    for f, n in ecritures:
        io.open(f, "w", encoding="utf-8").write(n)
    for av, ap in renommages:
        subprocess.run(["git", "mv", str(av), str(ap)], cwd=RACINE.parent,
                       check=True)
    print("\n%d fichiers réécrits, %d articles renommés."
          % (len(ecritures), len(renommages)))
    print("Pensez aux planches qui citent des dates : la slide 3 du n° 4 bis\n"
          "annonce les quatre prochains articles.")


if __name__ == "__main__":
    main()
