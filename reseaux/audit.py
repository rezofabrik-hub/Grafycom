# -*- coding: utf-8 -*-
"""Vérifie le dossier entier, et dit ce qu'il mesure.

Pourquoi ce fichier existe
--------------------------
Un cycle de publication se contrôle à trois endroits qui se contredisent
facilement : le moteur qui produit les visuels, le document qui porte les
textes, et le calendrier qui porte les dates. Tant que les trois sont
relus à l'œil, ils divergent — et ils l'ont fait : une publication s'est
retrouvée le même jour qu'une autre, et « n° 2 » a désigné deux
publications différentes selon le fichier qu'on ouvrait.

Ce qui se compte doit se compter. Ce fichier ne juge rien : il mesure, et
il montre l'écart. Les seuls jugements qu'il porte sont ceux qu'on peut
écrire en une règle — une semaine ne dépasse pas cinq publications, un
chemin cité existe, une date est la même partout.

Ce qu'il NE fait pas : relire les textes. Aucun programme ne dira si une
accroche est juste.

Usage
-----
    python3 reseaux/audit.py                      # tout sauf les visuels
    python3 reseaux/audit.py sortie-du-cycle.txt  # avec le rapport du cycle
"""
import ast
import collections
import datetime
import pathlib
import re
import subprocess
import sys

R = pathlib.Path(__file__).resolve().parent.parent
MOIS = {"janvier": 1, "février": 2, "mars": 3, "avril": 4, "mai": 5,
        "juin": 6, "juillet": 7, "août": 8, "septembre": 9, "octobre": 10,
        "novembre": 11, "décembre": 12}
PLAFOND = 5          # publications par semaine, réserve n° 3

# Les dépassements acceptés, et pourquoi. Une exception se motive ; une
# exception qu'on tait redevient un défaut au bout de trois semaines.
DEROGATIONS = {
    datetime.date(2026, 11, 23):
        "SWEET DREAM intercalée le 25 — arbitrage du 22 octobre",
}

# Les endroits où l'identité complète est OBLIGATOIRE : la loi l'exige sur
# les mentions légales, les CGV et tout document contractuel.
IDENTITE_LEGALE = {"mentions-legales.html", "cgv.html"}

ecarts, ok, notes = [], [], []


def faux(t):
    ecarts.append(t)


def juste(t):
    ok.append(t)


def lire(p):
    return (R / p).read_text(encoding="utf-8")


def _publications():
    """Numéro -> (date, heure, format), depuis les titres du document."""
    doc = lire("reseaux/propositions/a-valider/instagram-facebook.md")
    out = {}
    for m in re.finditer(
            r"^## (\d+(?: bis)?) — (\w+) (\d{1,2})(?:er)? (\w+), "
            r"([\dh\s]+) · ([^·\n]+) ·", doc, re.M):
        num, _, j, mois, heure, fmt = m.groups()
        out[num] = (datetime.date(2026, MOIS[mois], int(j)),
                    re.sub(r"\s+", " ", heure).strip(), fmt.strip())
    return out


def moteur():
    src = lire("reseaux/visuels.py")
    try:
        ast.parse(src)
        juste("visuels.py : syntaxe valide")
    except SyntaxError as e:
        faux("visuels.py : SYNTAXE CASSÉE — %s" % e)
    noms = [a or b for a, b in re.findall(
        r"^(?:def (\w+)|GABARITS\[\"([^\"]+)\"\])", src, re.M)]
    dbl = [n for n, c in collections.Counter(noms).items() if c > 1]
    if dbl:
        faux("visuels.py : définitions en double — %s" % ", ".join(dbl))
    else:
        juste("visuels.py : aucune définition en double")


def dates(pubs):
    """Le moteur, le document et le calendrier doivent dire la même date."""
    dossiers = {d.name[:10]: d.name
                for d in (R / "reseaux/visuels").iterdir()
                if d.is_dir() and re.match(r"20\d\d-\d\d-\d\d", d.name)}
    sans = [n for n, (d, *_) in pubs.items() if d.isoformat() not in dossiers]
    if sans:
        faux("publications sans dossier de visuels : %s" % ", ".join(sans))
    else:
        juste("chaque publication a son dossier de visuels (%d)" % len(pubs))

    attendus = {d.isoformat() for d, *_ in pubs.values()}
    orphelins = sorted(dossiers[o] for o in set(dossiers) - attendus)
    if orphelins:
        faux("dossiers sans publication, à supprimer : %s"
             % ", ".join(orphelins))
    else:
        juste("aucun dossier de visuels orphelin")

    cal = {}
    for ligne in lire("reseaux/propositions/a-valider/calendrier.md").split("\n"):
        # le tableau est du markdown : heures et numéros peuvent être
        # en gras, et un numéro peut traîner un commentaire derrière lui.
        m = re.match(r"\| (\w+) (\d{1,2})(?:er)? (\w+) \| \*{0,2}([\dh\s]+?)\*{0,2} \| "
                     r"Instagram \+ Facebook \| [^|]+ \| \*{0,2}n° (\d+(?: bis)?)",
                     ligne)
        if m:
            _, j, mois, heure, num = m.groups()
            cal[num] = (datetime.date(2026, MOIS[mois], int(j)),
                        re.sub(r"\s+", " ", heure).strip())
    absentes = sorted(set(pubs) - set(cal))
    if absentes:
        faux("absentes du calendrier : %s" % ", ".join(absentes))
    else:
        juste("chaque publication est au calendrier (%d)" % len(cal))

    divergent = []
    for num in sorted(set(pubs) & set(cal)):
        d1, h1, _ = pubs[num]
        d2, h2 = cal[num]
        if d1 != d2:
            divergent.append("n° %s : document %s ≠ calendrier %s"
                             % (num, d1, d2))
        elif h1 != h2:
            divergent.append("n° %s : heure %s ≠ %s" % (num, h1, h2))
    if divergent:
        for d in divergent:
            faux(d)
    else:
        juste("document et calendrier concordent sur toutes les dates")

    par_jour = collections.defaultdict(list)
    for n, (d, *_) in pubs.items():
        par_jour[d].append(n)
    col = {d: v for d, v in par_jour.items() if len(v) > 1}
    if col:
        faux("deux publications le même jour : %s"
             % "; ".join("%s → %s" % (d, ", ".join(v)) for d, v in col.items()))
    else:
        juste("aucune collision de date")

    sem = collections.Counter()
    for d, *_ in pubs.values():
        sem[d - datetime.timedelta(days=d.weekday())] += 1
    notes.append("densité par semaine : "
                 + " · ".join(str(sem[k]) for k in sorted(sem)))
    trop = sorted((k, v) for k, v in sem.items() if v > PLAFOND)
    non_prevus = [(k, v) for k, v in trop if k not in DEROGATIONS]
    for k, v in trop:
        if k in DEROGATIONS:
            notes.append("semaine du %s à %d publications — dérogation : %s"
                         % (k, v, DEROGATIONS[k]))
    if non_prevus:
        faux("semaine au-dessus de %d sans dérogation écrite : %s" % (
            PLAFOND, ", ".join("%s → %d" % (k, v) for k, v in non_prevus)))
    else:
        juste("aucun dépassement de %d publications hors dérogation écrite"
              % PLAFOND)


def comptes(pubs):
    """Ce que les documents annoncent doit être ce qu'on mesure."""
    vis = R / "reseaux/visuels"
    planches = sum(len(list((vis / d.name).glob("*.png"))) for d in vis.iterdir()
                   if d.is_dir() and re.match(r"20\d\d-\d\d-\d\d", d.name))
    stories = len(list((vis / "stories").glob("*.png")))
    arts = len(list((R / "reseaux/blog").glob("20*.md")))
    notes.append("mesuré : %d publications · %d planches · %d stories · "
                 "%d articles" % (len(pubs), planches, stories, arts))
    regles = {
        "reseaux/propositions/a-valider/calendrier.md": [
            (r"\| Publications Instagram \+ Facebook \| \*\*(\d+)\*\* \|",
             len(pubs)),
            (r"\| Écrans de story \| \*\*(\d+)\*\* \|", stories),
            (r"\| Articles de blog \| \*\*(\d+)\*\* \|", arts)],
        "reseaux/propositions/a-valider/PRET-A-VALIDER.md": [
            (r"les (\d+) publications sont complètes", len(pubs)),
            (r"\*\*(\d+) planches de publication\*\*", planches)],
        "reseaux/BRIEF-VISUELS.md": [
            (r"## 6\. Les (\d+) publications", len(pubs))],
        "reseaux/propositions/a-valider/LISEZ-MOI.md": [
            (r"(\d+) publications attendent ton accord", len(pubs))],
    }
    faux_avant = len(ecarts)
    for f, paires in regles.items():
        t = lire(f)
        for motif, attendu in paires:
            m = re.search(motif, t)
            if not m:
                faux("%s : compteur introuvable (%s…)" % (f, motif[:34]))
            elif int(m.group(1)) != attendu:
                faux("%s : annonce %s, mesuré %d" % (f, m.group(1), attendu))
    if len(ecarts) == faux_avant:
        juste("tous les compteurs des documents correspondent au mesuré")


def prudence():
    """Les règles qu'on ne discute pas."""
    # Le pseudo. Une citation du défaut n'est pas le défaut.
    mauvais = []
    for f in list(R.rglob("*.md")) + list(R.rglob("*.py")):
        if ".git" in f.parts:
            continue
        for ligne in f.read_text(encoding="utf-8", errors="ignore").split("\n"):
            if not re.search(r"@grafycom[ _-]graphiste", ligne):
                continue
            if any(c in ligne for c in "«\"`") or "jamais sans" in ligne:
                continue
            mauvais.append("%s : %s" % (f.relative_to(R), ligne.strip()[:60]))
    if mauvais:
        faux("pseudo sans le point : " + " ; ".join(mauvais[:4]))
    else:
        juste("le pseudo porte toujours son point")

    # Sandra : ni nom de famille ni adresse, SAUF mentions légales et CGV,
    # où la loi les exige. L'exception est la règle, ici.
    fuite = []
    for f in list(R.rglob("*.md")) + list(R.rglob("*.html")):
        if ".git" in f.parts or f.name in IDENTITE_LEGALE:
            continue
        if re.search(r"\bSandra [A-ZÉÈ][a-zéèêë]{2,}",
                     f.read_text("utf-8", errors="ignore")):
            fuite.append(str(f.relative_to(R)))
    if fuite:
        faux("nom de famille de Sandra hors document légal : "
             + ", ".join(fuite))
    else:
        juste("nom de famille de Sandra : nulle part hors document légal")

    for nom in ("mentions-legales", "cgv"):
        pages = [p for p in R.glob("%s.html" % nom)]
        if not pages:
            faux("page %s.html introuvable" % nom)
        elif re.search(r"SIRET", pages[0].read_text("utf-8"), re.I):
            juste("%s.html porte bien l'identité légale" % nom)
        else:
            faux("%s.html : SIRET absent, la loi l'exige" % nom)

    # Les sources clients ne se versionnent pas : le dépôt est public.
    suivis = subprocess.run(
        ["git", "-C", str(R), "ls-files", "reseaux/visuels/sources"],
        capture_output=True, text=True).stdout.strip()
    if suivis:
        faux("sources clients versionnées : " + suivis.replace("\n", ", "))
    else:
        juste("les sources clients ne sont pas versionnées")


def references():
    """Un chemin cité, un lien posé : les deux doivent mener quelque part."""
    gabarit = re.compile(r"AAAA|MM-JJ|<[^>]+>|\*")
    manquants = set()
    for f in R.rglob("*.md"):
        if ".git" in f.parts:
            continue
        for chemin in re.findall(r"`(reseaux/[A-Za-z0-9_\-./]+?)/?`",
                                 f.read_text("utf-8")):
            if gabarit.search(chemin) or (R / chemin).exists():
                continue
            manquants.add("%s → %s" % (f.relative_to(R), chemin))
    if manquants:
        faux("chemins cités introuvables : " + " ; ".join(sorted(manquants)[:6]))
    else:
        juste("tous les chemins cités dans les documents existent")

    casses = set()
    for f in sorted((R / "reseaux/blog").glob("*.md")):
        for lien in re.findall(r"\]\(([a-z0-9][a-z0-9\-]*\.html)\)",
                               f.read_text("utf-8")):
            if (R / lien).exists():
                continue
            if any(p.name.endswith(lien[:-5] + ".md")
                   for p in (R / "reseaux/blog").glob("*.md")):
                continue
            casses.add("%s → %s" % (f.name, lien))
    if casses:
        faux("liens d'articles cassés : " + " ; ".join(sorted(casses)[:5]))
    else:
        juste("les liens internes des articles mènent tous quelque part")

    for f in sorted((R / "reseaux/blog").glob("20*.md")):
        m = re.search(r"^date:\s*\"?(\d{4}-\d{2}-\d{2})", f.read_text("utf-8"),
                      re.M)
        if not m:
            faux("%s : pas de date dans l'en-tête" % f.name)
        elif m.group(1) != f.name[:10]:
            faux("%s : l'en-tête dit %s" % (f.name, m.group(1)))
    if not any(".md : " in e or "en-tête dit" in e for e in ecarts):
        juste("chaque article porte la date de son nom de fichier")


def reglementation():
    """Le Cerfa : le courant nommé, le périmé jamais donné pour bon."""
    t = " ".join(f.read_text("utf-8", errors="ignore")
                 for f in R.rglob("*.md") if ".git" not in f.parts)
    if "16308" in t and "14798" in t:
        juste("les deux Cerfa sont nommés, le courant et le périmé")
    else:
        faux("un des deux Cerfa manque dans les documents")
    mauvaises = [p for p in re.findall(r"14798[^.]{0,90}", t)
                 if re.search(r"\b(valable|en vigueur|à utiliser)", p)
                 and not re.search(r"n'est plus|plus valable|périmé|obsolète",
                                   p)]
    if mauvaises:
        faux("le Cerfa périmé est donné pour valable : " + mauvaises[0][:70])
    else:
        juste("le Cerfa périmé n'est jamais donné pour valable")


def cycle(rapport):
    """Ce que le moteur a signalé en produisant les visuels."""
    t = pathlib.Path(rapport).read_text(encoding="utf-8")
    for l in t.split("\n"):
        if "SANS IMAGE" in l:
            notes.append("fichier source manquant : " + l.strip())
    for mot in ("HORS CADRE", "CHEVAUCHE", "ORPHELIN", "DÉBORD"):
        n = t.count(mot)
        if n:
            faux("%d × %s dans les visuels" % (n, mot.lower()))
        else:
            juste("aucun %s" % mot.lower())
    m = re.search(r"(\d+) visuels produits", t)
    if m:
        notes.append("le moteur a produit %s visuels" % m.group(1))


def main():
    moteur()
    pubs = _publications()
    dates(pubs)
    comptes(pubs)
    prudence()
    references()
    reglementation()
    if len(sys.argv) > 1:
        cycle(sys.argv[1])
    else:
        notes.append("visuels non contrôlés : relancer avec le rapport du "
                     "cycle en argument")

    for n in notes:
        print("   ·", n)
    print("=" * 66)
    for t in ok:
        print("  OK   ", t)
    for t in ecarts:
        print("  ÉCART", t)
    print("=" * 66)
    print("%d contrôles passés, %d écart(s)." % (len(ok), len(ecarts)))
    return 1 if ecarts else 0


if __name__ == "__main__":
    raise SystemExit(main())
