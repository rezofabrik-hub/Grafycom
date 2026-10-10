#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Transforme un cycle de l'agent social en lignes du back-office.

L'agent ecrit un cycle en Markdown. En tete, un tableau « BON A
PUBLIER » : une ligne par publication, avec sa date, son heure et son
canal. Plus bas, le contenu reel : la legende, la direction visuelle,
les hashtags, le texte de la fiche Google, les stories.

Ce script lit les deux. Le tableau donne la liste et l'ordre ; le corps
donne ce qu'il y a a relire. Un back-office qui n'afficherait que des
titres ne servirait a rien : on ne valide pas un titre.

    python3 outils/importer-cycle.py reseaux/propositions/cycle-2026-10-12.md

Il produit du SQL, qu'on relit avant de l'appliquer. Les identifiants
sont derives de la date, de l'heure et du canal : reimporter le meme
cycle met a jour les lignes au lieu d'en creer des doubles, et ne touche
jamais au statut - une validation deja faite survit a un reimport.
"""
import hashlib
import pathlib
import re
import sys

MOIS = {m: i + 1 for i, m in enumerate(
    "janvier fevrier mars avril mai juin juillet aout "
    "septembre octobre novembre decembre".split())}

RANGEE = re.compile(
    r"^\|\s*(?:☐|☑|x|X|)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|"
    r"\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")
SECTION = re.compile(
    r"^##\s+(\d+)\s+—\s+\w+\s+(\d{1,2})\s+(\w+),\s*([\dh\s]+?)\s*·\s*([^·]+)·\s*(.+)$")
STORY = re.compile(
    r"^###\s+Story\s+\w+\s+—\s+\w+\s+(\d{1,2}),\s*([\dh\s]+?)\s*·\s*(.+)$")
SOUS = re.compile(r"^###\s+(.+?)\s*$")


def sans_accent(s):
    for a, b in zip("éèêëàâîïôûùç", "eeeeaaiiouuc"):
        s = s.replace(a, b)
    return s


def nettoie(x):
    return re.sub(r"\*\*|`", "", x).strip()


def bloc(lignes):
    """Rend un bloc lisible : on retire le marqueur de citation et le gras."""
    t = "\n".join(lignes).strip()
    t = re.sub(r"^>\s?", "", t, flags=re.M)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def ident(iso, heure, canal, titre):
    cle = "%s|%s|%s|%s" % (iso, heure, canal, titre)
    return hashlib.sha1(cle.encode("utf-8")).hexdigest()[:16]


def lire_tableau(texte, annee):
    """La liste des publications, dans l'ordre du tableau de tete."""
    lignes = []
    for brut in texte.splitlines():
        m = RANGEE.match(brut)
        if not m:
            continue
        jour, heure, canal, element = (x.strip() for x in m.groups())
        if jour.lower().startswith(("date", "---", ":--")):
            continue
        d = re.match(r"^(\d{1,2})/(\d{1,2})$", jour)
        if d:
            iso = "%s-%02d-%02d" % (annee, int(d.group(2)), int(d.group(1)))
        elif jour.lower().startswith("en continu"):
            iso = "%s-12-31" % annee
        else:
            print("  date illisible, ligne ignoree : %r" % jour, file=sys.stderr)
            continue
        heure = "" if heure in ("—", "-", "") else heure
        lignes.append({"jour": iso, "heure": heure,
                       "canal": nettoie(canal), "titre": nettoie(element)})
    return lignes


def lire_corps(texte, annee):
    """Le contenu, range par (date, heure, canal)."""
    contenu = {}
    lignes = texte.splitlines()
    i = 0
    while i < len(lignes):
        m = SECTION.match(lignes[i])
        s = STORY.match(lignes[i])

        if m:
            _, jj, mois, heure, _type, _pilier = m.groups()
            cle_mois = MOIS.get(sans_accent(mois.lower()))
            if not cle_mois:
                i += 1
                continue
            iso = "%s-%02d-%02d" % (annee, cle_mois, int(jj))
            heure = re.sub(r"\s+", " ", heure).strip()

            parts, courant, tampon = {}, None, []
            i += 1
            while i < len(lignes) and not lignes[i].startswith("## ") \
                    and not lignes[i].startswith("# "):
                sm = SOUS.match(lignes[i])
                if sm:
                    if courant:
                        parts[courant] = bloc(tampon)
                    courant, tampon = sans_accent(sm.group(1).lower()), []
                elif courant:
                    tampon.append(lignes[i])
                i += 1
            if courant:
                parts[courant] = bloc(tampon)

            def prend(prefixe):
                for k, v in parts.items():
                    if k.startswith(prefixe):
                        return v
                return ""

            # Le post Instagram + Facebook.
            accroche = prend("accroche")
            legende = prend("legende")
            contenu[(iso, heure, "Instagram + Facebook")] = {
                "texte": (accroche + "\n\n" + legende).strip() if accroche else legende,
                "hashtags": prend("hashtags"),
                "visuel": prend("direction visuelle") or prend("decoupage"),
                "note": prend("a fournir par sandra"),
            }
            # Le texte de la fiche Google, meme date, meme heure.
            google = prend("texte fiche google")
            if google:
                contenu[(iso, heure, "Fiche Google")] = {"texte": google}
            continue

        if s:
            jj, heure, titre = s.groups()
            heure = re.sub(r"\s+", " ", heure).strip()
            tampon = []
            i += 1
            while i < len(lignes) and not lignes[i].startswith("#"):
                tampon.append(lignes[i])
                i += 1
            # Le mois d'une story n'est pas ecrit : on le prend sur la
            # section la plus proche deja lue, qui porte le meme jour.
            for (iso_c, _, _) in contenu:
                if iso_c.endswith("-%02d" % int(jj)):
                    contenu[(iso_c, heure, "Stories")] = {
                        "texte": bloc(tampon), "note": nettoie(titre)}
                    break
            continue
        i += 1
    return contenu


def sql_texte(s):
    return "'" + s.replace("'", "''") + "'"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    chemin = pathlib.Path(sys.argv[1])
    texte = chemin.read_text(encoding="utf-8")
    an = re.search(r"\b(20\d\d)\b", texte)
    annee = an.group(1) if an else "2026"
    cycle = chemin.stem

    rangees = lire_tableau(texte, annee)
    corps = lire_corps(texte, annee)
    if not rangees:
        print("Aucune ligne reconnue dans %s" % chemin, file=sys.stderr)
        return 1

    remplies = 0
    print("-- %d publication(s), cycle %s" % (len(rangees), cycle))
    for rang, r in enumerate(rangees):
        c = corps.get((r["jour"], r["heure"], r["canal"]), {})
        if c.get("texte"):
            remplies += 1
        ident_ = ident(r["jour"], r["heure"], r["canal"], r["titre"])
        print(
            "INSERT INTO publications "
            "(id,cycle,jour,heure,canal,titre,texte,hashtags,visuel,note,rang,maj) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d,datetime('now')) "
            "ON CONFLICT(id) DO UPDATE SET jour=excluded.jour, heure=excluded.heure, "
            "canal=excluded.canal, titre=excluded.titre, rang=excluded.rang, "
            # Le contenu n'ecrase que s'il est vide cote base : ce que
            # Laurent a retouche dans le back-office ne se perd pas.
            "texte=CASE WHEN publications.texte='' THEN excluded.texte "
            "ELSE publications.texte END, "
            "hashtags=CASE WHEN publications.hashtags='' THEN excluded.hashtags "
            "ELSE publications.hashtags END, "
            "visuel=CASE WHEN publications.visuel='' THEN excluded.visuel "
            "ELSE publications.visuel END;"
            % (sql_texte(ident_), sql_texte(cycle), sql_texte(r["jour"]),
               sql_texte(r["heure"]), sql_texte(r["canal"]), sql_texte(r["titre"]),
               sql_texte(c.get("texte", "")), sql_texte(c.get("hashtags", "")),
               sql_texte(c.get("visuel", "")), sql_texte(c.get("note", "")), rang))
    print("-- %d/%d avec du contenu" % (remplies, len(rangees)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
