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
# Vide depuis le 23 octobre. La semaine du 23 novembre portait six
# publications — SOLAIRE 66 ajoutée « en plus » le 25. La n° 18 en est
# sortie le même jour, faute de vérification réglementaire : la semaine
# retombe à cinq toute seule, et la dérogation n'a plus lieu d'être.
DEROGATIONS = {}

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
    # Indexes par DATE, deux dossiers du meme jour s'ecrasaient dans le
    # dictionnaire et le residu passait inapercu — c'est exactement ce
    # qui est arrive a 2026-11-25-sweet-dream, cache derriere
    # 2026-11-25-solaire-66. On garde donc la liste.
    dossiers = collections.defaultdict(list)
    for d in (R / "reseaux/visuels").iterdir():
        if d.is_dir() and re.match(r"20\d\d-\d\d-\d\d", d.name):
            dossiers[d.name[:10]].append(d.name)
    doubles = {j: v for j, v in dossiers.items() if len(v) > 1}
    if doubles:
        faux("deux dossiers de visuels le même jour : %s"
             % "; ".join("%s → %s" % (j, ", ".join(sorted(v)))
                         for j, v in sorted(doubles.items())))
    else:
        juste("un seul dossier de visuels par date")
    sans = [n for n, (d, *_) in pubs.items() if d.isoformat() not in dossiers]
    if sans:
        faux("publications sans dossier de visuels : %s" % ", ".join(sans))
    else:
        juste("chaque publication a son dossier de visuels (%d)" % len(pubs))

    attendus = {d.isoformat() for d, *_ in pubs.values()}
    orphelins = sorted(n for o in set(dossiers) - attendus
                       for n in dossiers[o])
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
    # le total annoncé par le calendrier : il additionne quatre volumes
    # qu'on mesure déjà, et il était faux des deux côtés — 107 pour
    # 26 textes Google alors que 26 ne tombait pas juste non plus.
    goog = len(re.findall(r"\| Fiche Google \| post \|",
                          lire("reseaux/propositions/a-valider/calendrier.md")))
    regles = {
        "reseaux/propositions/a-valider/calendrier.md": [
            (r"\| \*\*Total à valider\*\* \| \*\*(\d+)\*\* \|",
             len(pubs) + goog + stories + arts),
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


def fiche_google():
    """Les textes de la fiche Google portent-ils la bonne date ?

    Le calendrier programme un texte par publication, au même créneau
    qu'elle. Les en-têtes du document, eux, étaient saisis à la main,
    et rien ne les relisait : le 23 octobre, quatre d'entre eux
    dataient d'un état antérieur du calendrier. Trois tenaient à des
    publications déplacées — le reel remonté au 9 novembre, la n° 9
    glissée au 14 — et le quatrième à une heure jamais corrigée.

    L'écart ne se voyait pas, parce que le contrôle de concordance
    d'au-dessus ne lit que le document Instagram. Celui-ci fait le
    même travail sur la fiche Google, dans les deux sens : un en-tête
    qui ne correspond à aucun créneau, et un créneau sans texte.
    """
    MOTIF_CAL = (r"\| (?:~~)?(\w+) (\d{1,2})(?:er)? (\w+)(?:~~)? \| "
                 r"\*{0,2}([\dh\s—-]+?)\*{0,2} \| Fiche Google \| post \| "
                 r"texte n° ([\w ]+?) \|")
    cal = {}
    for ligne in lire("reseaux/propositions/a-valider/calendrier.md").split("\n"):
        m = re.match(MOTIF_CAL, ligne)
        if m:
            _, j, mois, heure, num = m.groups()
            cal[num.strip()] = (datetime.date(2026, MOIS[mois], int(j)),
                                re.sub(r"\s+", " ", heure).strip())

    doc = {}
    for tete in re.findall(r"^## (?:~~)?(\d+(?: bis)?)(?:~~)? — (?:\w+) "
                           r"(\d{1,2})(?:er)? (\w+)(?: 2026)?, "
                           r"(\d+ h(?: \d+)?)",
                           lire("reseaux/propositions/a-valider/fiche-google.md"),
                           re.M):
        num, j, mois, heure = tete
        doc[num] = (datetime.date(2026, MOIS[mois], int(j)),
                    re.sub(r"\s+", " ", heure).strip())

    t = lire("reseaux/propositions/a-valider/fiche-google.md")
    m = re.search(r"les (\d+) textes à valider", t)
    if not m:
        faux("fiche Google : compteur de textes introuvable en tête")
    elif int(m.group(1)) != len(doc):
        faux("fiche Google : l'en-tête annonce %s textes, %d sont datés"
             % (m.group(1), len(doc)))
    else:
        juste("fiche Google : le compteur de tête vaut les textes datés (%d)"
              % len(doc))

    # le calendrier annonce aussi un volume, et personne ne le relisait :
    # il comptait 26 textes — la n° 18 suspendue comprise, alors que sa
    # ligne « publications » l'exclut — et un total de 107 qui ne tombait
    # juste ni avec 26 ni avec 25.
    kal = lire("reseaux/propositions/a-valider/calendrier.md")
    m = re.search(r"\| Textes de fiche Google \| \*\*(\d+)\*\* \|", kal)
    if not m:
        faux("calendrier : compteur de textes Google introuvable")
    elif int(m.group(1)) != len(cal):
        faux("calendrier : annonce %s textes Google, %d lignes datées"
             % (m.group(1), len(cal)))
    else:
        juste("calendrier : le volume de textes Google vaut ses lignes (%d)"
              % len(cal))

    sans_texte = sorted(set(cal) - set(doc))
    if sans_texte:
        faux("fiche Google : créneau au calendrier sans texte écrit : %s"
             % ", ".join("n° " + n for n in sans_texte))
    else:
        juste("fiche Google : chaque créneau du calendrier a son texte")

    divergent = ["n° %s : en-tête %s %s ≠ calendrier %s %s"
                 % (n, doc[n][0], doc[n][1], cal[n][0], cal[n][1])
                 for n in sorted(set(doc) & set(cal))
                 if doc[n] != cal[n]]
    if divergent:
        for d in divergent:
            faux("fiche Google — " + d)
    else:
        juste("fiche Google : les en-têtes concordent avec le calendrier")


def photos_a_prendre(pubs):
    """Le tableau des visuels livrés porte-t-il les bonnes dates ?

    Meme defaut que les en-tetes de la fiche Google, et trouve le meme
    jour : ce tableau datait chaque publication a la main, et cinq de
    ses lignes avaient vieilli — deux numeros intervertis, deux dates
    jamais reprises, et la n° 16 restee au 21 novembre alors qu'elle
    etait remontee au 9. Un tableau de dates qu'aucun programme ne
    relit finit toujours par mentir.
    """
    ABR = {"oct": 10, "nov": 11, "déc": 12}
    mauvais, inconnues = [], []
    for ligne in lire("reseaux/propositions/a-valider/photos-a-prendre.md")\
            .split("\n"):
        m = re.match(r"\| (\d+(?: bis)?) \| (\d{1,2})(?:er)? (oct|nov|déc) \|",
                     ligne)
        if not m:
            continue
        num = m.group(1)
        d = datetime.date(2026, ABR[m.group(3)], int(m.group(2)))
        if num not in pubs:
            inconnues.append(num)
        elif pubs[num][0] != d:
            mauvais.append("n° %s : tableau %s ≠ publication %s"
                           % (num, d, pubs[num][0]))
    for t in mauvais:
        faux("photos-a-prendre — " + t)
    if inconnues:
        faux("photos-a-prendre : numéros hors cycle, à barrer : %s"
             % ", ".join("n° " + n for n in inconnues))
    if not mauvais and not inconnues:
        juste("photos-a-prendre : les dates du tableau suivent le calendrier")


def pret_a_valider(pubs):
    """Le tableau de PRET-A-VALIDER porte-t-il les bonnes dates ?

    Quatrieme tableau de dates tenu a la main, quatrieme derive, et le
    plus genant des quatre : c'est celui que Laurent a sous les yeux
    quand il programme. Le 23 octobre il datait encore la n° 16 au
    28 novembre — elle etait remontee au 9 — la n° 9 au 9 novembre, la
    n° 22 au 24, et gardait la n° 18 comme si elle etait au calendrier.
    """
    ABR = {"oct": 10, "nov": 11, "déc": 12}
    mauvais, fantomes = [], []
    for ligne in lire("reseaux/propositions/a-valider/PRET-A-VALIDER.md").split("\n"):
        m = re.match(r"\| (\d+(?: bis)?) \| \w+ (\d{1,2})(?:er)? (oct|nov|déc) \|",
                     ligne)
        if not m:
            continue
        num = m.group(1)
        d = datetime.date(2026, ABR[m.group(3)], int(m.group(2)))
        if num not in pubs:
            fantomes.append(num)
        elif pubs[num][0] != d:
            mauvais.append("n° %s : tableau %s ≠ publication %s"
                           % (num, d, pubs[num][0]))
    for t in mauvais:
        faux("PRET-A-VALIDER — " + t)
    if fantomes:
        faux("PRET-A-VALIDER : numéros hors cycle, à barrer : %s"
             % ", ".join("n° " + n for n in fantomes))
    if not mauvais and not fantomes:
        juste("PRET-A-VALIDER : les dates du tableau suivent le calendrier")


def stories_dates():
    """La checklist des stories suit-elle le moteur et le calendrier ?

    Troisieme table de dates tenue a la main, troisieme derive — et la
    pire des trois. stories.md portait DEUX checklists qui employaient
    les memes codes pour des ecrans differents : S3-C etait la boite a
    questions dans l'une, le vote du jeudi dans l'autre, les lettres
    decalees d'un cran faute d'ecran Halloween. Dix-neuf ecrans
    divergeaient du calendrier, et sept en-tetes de section avec eux.

    Laurent a tranche le 23 octobre : la premiere lettre fait foi,
    celle que suivent deja visuels.py et le calendrier. Reste a ce que
    ca le reste. Le controle croise les trois sources — la liste du
    moteur, les lignes du calendrier, la table du document — et ne
    laisse passer que leur accord complet.
    """
    MOIS_N = {v: k for k, v in MOIS.items()}
    cal = {}
    for ligne in lire("reseaux/propositions/a-valider/calendrier.md").split("\n"):
        m = re.match(r"\| (?:~~)?(\w+) (\d{1,2})(?:er)? (\w+)(?:~~)? \| "
                     r"\*{0,2}([\dh\s]+?)\*{0,2} \| Story \| story \| "
                     r"(S\d-[A-Z])\s*(?:·|écran )?\s*(\d)?", ligne)
        if m:
            cal[m.group(5) + (m.group(6) or "")] = (
                datetime.date(2026, MOIS[m.group(3)], int(m.group(2))),
                re.sub(r"\s+", " ", m.group(4)).strip())

    doc = {}
    for m in re.finditer(r"^\| ☐ \| (S\d-[A-Z]\d?)\s*\| \w+\s*\| "
                         r"(\d{2})/(\d{2}) \| ([\dh\s]+?)\s*\|",
                         lire("reseaux/propositions/a-valider/stories.md"), re.M):
        doc[m.group(1)] = (datetime.date(2026, int(m.group(3)), int(m.group(2))),
                           re.sub(r"\s+", " ", m.group(4)).strip())

    moteur = set(re.findall(r'^     \("(S\d-[A-Z]\d?)"',
                            lire("reseaux/visuels.py"), re.M))

    sans_ligne = sorted((moteur & set(cal)) - set(doc))
    if sans_ligne:
        faux("stories : programmées au calendrier mais absentes de la "
             "checklist : %s" % ", ".join(sans_ligne))
    fantomes = sorted(set(doc) - moteur)
    if fantomes:
        faux("stories : en checklist mais pas dans le moteur : %s"
             % ", ".join(fantomes))
    divergent = ["%s : checklist %s %s ≠ calendrier %s %s"
                 % (c, doc[c][0], doc[c][1], cal[c][0], cal[c][1])
                 for c in sorted(set(doc) & set(cal)) if doc[c] != cal[c]]
    for d in divergent:
        faux("stories — " + d)
    if not sans_ligne and not fantomes and not divergent:
        juste("stories : checklist, moteur et calendrier concordent (%d)"
              % len(doc))


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
    for mot in ("HORS CADRE", "CHEVAUCHE", "ORPHELIN", "DÉBORD", "COUPE"):
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
    fiche_google()
    photos_a_prendre(pubs)
    stories_dates()
    pret_a_valider(pubs)
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
