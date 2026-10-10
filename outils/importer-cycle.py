#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Transforme un cycle de l'agent social en lignes du back-office.

L'agent ecrit un cycle en Markdown, avec en tete un tableau « BON A
PUBLIER » : une ligne par publication, avec sa date, son heure et son
canal. C'est deja la liste a cocher ; ce script la rend cliquable.

Il produit du SQL, qu'on applique ensuite a la base D1. Il n'ecrit rien
lui-meme : on relit le SQL avant de l'appliquer, comme le reste.

    python3 outils/importer-cycle.py reseaux/propositions/cycle-2026-10-12.md

Les identifiants sont derives de la date, de l'heure et du canal, donc
stables : reimporter le meme cycle met a jour les lignes au lieu d'en
creer des doubles. Le statut et le texte deja relus sont preserves -
reimporter ne defait jamais une validation.
"""
import hashlib
import pathlib
import re
import sys

LIGNE = re.compile(
    r"^\|\s*(?:☐|☑|x|X|)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|"
    r"\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")


def apostrophes(s):
    return s.replace("'", "''")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    chemin = pathlib.Path(sys.argv[1])
    texte = chemin.read_text(encoding="utf-8")

    # L'annee ne figure pas dans le tableau, seulement dans le titre.
    an = re.search(r"\b(20\d\d)\b", texte)
    annee = an.group(1) if an else "2026"
    cycle = chemin.stem

    lignes = []
    for brut in texte.splitlines():
        m = LIGNE.match(brut)
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
        # Le gras Markdown sert a attirer l'oeil dans le tableau. Il n'a
        # rien a faire en base : « **Blog** » n'est pas un canal.
        propre = lambda x: re.sub(r"\*\*|`", "", x).strip()
        canal = propre(canal)
        titre = propre(element)
        cle = "%s|%s|%s|%s" % (iso, heure, canal, titre)
        ident = hashlib.sha1(cle.encode("utf-8")).hexdigest()[:16]
        lignes.append((ident, iso, heure, canal, titre))

    if not lignes:
        print("Aucune ligne reconnue dans %s" % chemin, file=sys.stderr)
        return 1

    print("-- %d publication(s), cycle %s" % (len(lignes), cycle))
    for rang, (ident, iso, heure, canal, titre) in enumerate(lignes):
        # ON CONFLICT ne touche ni au statut ni au texte : une relecture
        # deja faite survit a un reimport.
        print(
            "INSERT INTO publications (id,cycle,jour,heure,canal,titre,rang,maj) "
            "VALUES ('%s','%s','%s','%s','%s','%s',%d,datetime('now')) "
            "ON CONFLICT(id) DO UPDATE SET jour=excluded.jour, heure=excluded.heure, "
            "canal=excluded.canal, titre=excluded.titre, rang=excluded.rang;"
            % (ident, apostrophes(cycle), iso, apostrophes(heure),
               apostrophes(canal), apostrophes(titre), rang))
    return 0


if __name__ == "__main__":
    sys.exit(main())
