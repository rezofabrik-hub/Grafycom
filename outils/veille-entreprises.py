#!/usr/bin/env python3
"""Veille des créations d'entreprises dans les Pyrénées-Orientales (66).

Source : BODACC, le Bulletin officiel des annonces civiles et commerciales.
Toute immatriculation au registre du commerce y est publiée — c'est la
raison d'être du bulletin. Les données sont ouvertes et interrogeables sans
clé d'API.

Ce que le script produit : une liste de prospects qualifiés, classés par
intérêt pour une activité de communication visuelle. Un restaurant qui
ouvre a besoin d'une carte, d'une enseigne et d'un logo ; une société
civile immobilière n'a besoin de rien. Le tri repose là-dessus.

Ce que le script ne produit pas : des adresses e-mail. Le BODACC n'en
publie aucune, et c'est très bien ainsi. La prise de contact se fait au
téléphone, par courrier ou sur place.

Usage :
    python3 outils/veille-entreprises.py                 # 7 derniers jours
    python3 outils/veille-entreprises.py --jours 30
    python3 outils/veille-entreprises.py --depuis 2026-09-01
    python3 outils/veille-entreprises.py --tout          # sans filtre d'intérêt
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

BODACC = ("https://bodacc-datadila.opendatasoft.com/api/explore/v2.1"
          "/catalog/datasets/annonces-commerciales/records")
DEPARTEMENT = "66"
PAR_PAGE = 100

RACINE = pathlib.Path(__file__).resolve().parent
SORTIE = RACINE / "prospects"
EXCLUSIONS = RACINE / "ne-pas-contacter.txt"

# Secteurs classés par intérêt réel pour Grafycom. L'ordre compte : le
# premier groupe dont un mot apparaît dans l'activité déclarée fixe la note.
SECTEURS = [
    (3, "Restauration & bouche", (
        "restaurant", "restauration", "brasserie", "pizzeria", "pizza",
        "traiteur", "snack", "crêperie", "creperie", "glacier", "glaces",
        "boulangerie", "pâtisserie", "patisserie", "boucherie", "charcuterie",
        "épicerie", "epicerie", "caviste", "vins", "chocolat", "salon de thé",
        "salon de the", "café", "cafe", "bar", "débit de boissons",
        "food truck", "burger", "sushi", "tapas", "primeur", "fromager",
        "poissonnerie", "biscuiterie", "torréfaction", "torrefaction",
        "fruits et légumes", "fruits et legumes", "produits régionaux",
        "produits regionaux", "terroir", "foie gras", "confit",
        "conserverie", "miel", "fromage", "crémerie", "cremerie",
    )),
    (3, "Commerce de détail", (
        "commerce de détail", "commerce de detail", "vente au détail",
        "vente au detail", "boutique", "prêt-à-porter", "pret-a-porter",
        "vêtements", "vetements", "fleuriste", "bijouterie", "maroquinerie",
        "décoration", "decoration", "ameublement", "librairie", "papeterie",
        "jouets", "chaussures", "lingerie", "parfumerie", "mercerie",
        "brocante", "concept store", "dépôt-vente", "depot-vente",
    )),
    (3, "Beauté & bien-être", (
        "coiffure", "coiffeur", "esthétique", "esthetique", "barbier",
        "onglerie", "manucure", "institut de beauté", "institut de beaute",
        "spa", "massage", "tatouage", "tatoueur", "épilation", "epilation",
        "soins du corps", "naturopath", "sophrolog", "réflexolog",
        "reflexolog", "bien-être", "bien-etre",
    )),
    (2, "Artisanat & bâtiment", (
        "plomberie", "électricité", "electricite", "maçonnerie", "maconnerie",
        "menuiserie", "peinture", "carrelage", "couverture", "charpente",
        "serrurerie", "chauffage", "climatisation", "isolation", "rénovation",
        "renovation", "bâtiment", "batiment", "travaux", "terrassement",
        "paysagiste", "jardin", "espaces verts", "piscine", "véranda",
        "veranda", "cuisiniste", "ébéniste", "ebeniste", "ferronnerie",
        "vitrerie", "ravalement", "étanchéité", "etancheite", "plâtrerie",
        "platrerie", "électricien", "electricien", "artisan",
    )),
    (2, "Tourisme & hébergement", (
        "hôtel", "hotel", "chambres d'hôtes", "chambres d'hotes", "camping",
        "gîte", "gite", "location saisonnière", "location saisonniere",
        "meublé de tourisme", "meuble de tourisme", "hébergement touristique",
        "hebergement touristique", "résidence de tourisme", "auberge",
        "activités de plein air", "nautique", "plongée", "plongee",
    )),
    (2, "Santé & soins", (
        "infirmier", "kinésithérap", "kinesitherap", "ostéopath", "osteopath",
        "dentaire", "orthodont", "podolog", "orthophon", "psycholog",
        "diététi", "dieteti", "opticien", "audioprothés", "audiiprothes",
        "pharmac", "vétérinaire", "veterinaire", "cabinet médical",
    )),
    (2, "Commerce en ligne", (
        "vente à distance", "vente a distance", "vente en ligne",
        "commerce électronique", "commerce electronique", "e-commerce",
        "boutique en ligne", "dropship", "drop ship", "sur internet",
        "par internet", "marketplace",
    )),
    (2, "Marchés & vente ambulante", (
        "ambulant", "au marché", "au marche", "sur les marchés",
        "sur les marches", "non sédentaire", "non sedentaire",
        "camion", "food truck", "étal", "forain",
    )),
    (2, "Services de proximité", (
        "conciergerie", "intendance", "laverie", "pressing", "retouche",
        "cordonnerie", "distributeur automatique", "distributeurs automatiques",
        "toilettage", "pension pour animaux", "animalerie", "fleurs",
        "réparation", "reparation", "dépannage", "depannage",
    )),
    (2, "Loisirs & événementiel", (
        "location de structures", "structures gonflables", "animation",
        "événement", "evenement", "loisirs", "escape game", "salle de sport",
        "fitness", "yoga", "danse", "équitation", "equitation", "club",
        "jeux", "paintball", "karting", "accrobranche",
    )),
    (1, "Services aux entreprises", (
        "conseil", "courtage", "courtier", "immobilier", "agence",
        "assurance", "comptab", "avocat", "juridique", "formation",
        "coaching", "coach", "recrutement", "communication", "marketing",
        "événementiel", "evenementiel", "photographe", "informatique",
        "web", "transport", "nettoyage", "sécurité", "securite",
        "aide à domicile", "aide a domicile", "garde d'enfants", "auto-école",
        "auto-ecole", "taxi", "déménagement", "demenagement",
    )),
]

# Ce qui n'a pas de vitrine, pas de clientèle de passage, pas d'enseigne :
# inutile de faire perdre son temps à qui que ce soit.
SANS_OBJET = (
    # Sociétés patrimoniales : pas de clientèle, pas d'enseigne, pas de carte.
    "société civile immobilière", "societe civile immobiliere", "sci",
    "holding", "sociétés holding", "societes holding",
    "location de terrains", "location de biens immobiliers",
    "location d'immeubles", "l'acquisition d'un immeuble",
    "acquisition et la gestion", "gestion de portefeuille",
    "marchand de biens", "gestion de participations", "cession de participations",
    "détention, la gestion", "detention, la gestion", "prise de participation",
    "souscription de parts", "placement de capitaux",
    # Coursiers des plateformes de livraison : ni vitrine, ni marque propre.
    # Ils travaillent sous l'enseigne d'un autre.
    "à vélo", "a velo", "coursier", "coursière", "coursiere", "livreur",
    "plateformes de livraison", "pour le compte de plateformes",
)

def lire_exclusions() -> set[str]:
    """SIREN et noms à ne jamais faire remonter, un par ligne."""
    if not EXCLUSIONS.exists():
        return set()
    lignes = EXCLUSIONS.read_text(encoding="utf-8").splitlines()
    return {
        l.strip().lower().replace(" ", "")
        for l in lignes
        if l.strip() and not l.lstrip().startswith("#")
    }


def appeler(params: dict) -> dict:
    url = BODACC + "?" + urllib.parse.urlencode(params)
    requete = urllib.request.Request(
        url, headers={"User-Agent": "veille-grafycom/1.0 (+https://www.grafycom.fr)"}
    )
    for essai in range(4):
        try:
            with urllib.request.urlopen(requete, timeout=40) as reponse:
                return json.loads(reponse.read().decode("utf-8"))
        except Exception as erreur:  # réseau, quota, 5xx
            if essai == 3:
                raise
            attente = 2 ** essai
            print(f"  … {erreur} — nouvelle tentative dans {attente} s",
                  file=sys.stderr)
            time.sleep(attente)
    return {}


def deplier(valeur):
    """Les champs imbriqués arrivent tantôt en dict, tantôt en texte JSON."""
    if isinstance(valeur, (dict, list)):
        return valeur
    if isinstance(valeur, str) and valeur.strip().startswith(("{", "[")):
        try:
            return json.loads(valeur)
        except json.JSONDecodeError:
            return None
    return None


def premier(valeur):
    """« etablissement » peut être un objet seul ou une liste d'objets."""
    if isinstance(valeur, list):
        return valeur[0] if valeur else {}
    return valeur or {}


def activite(annonce: dict) -> str:
    bloc = deplier(annonce.get("listeetablissements")) or {}
    etab = premier(bloc.get("etablissement") if isinstance(bloc, dict) else bloc)
    if isinstance(etab, dict):
        for champ in ("activite", "qualiteEtablissement", "origineFonds"):
            if etab.get(champ):
                return " ".join(texte(etab[champ]).split())
    return ""


def texte(valeur) -> str:
    """Le BODACC renvoie parfois une liste là où on attend une chaîne —
    « prenom » en contient plusieurs quand la personne en a plusieurs."""
    if valeur is None:
        return ""
    if isinstance(valeur, (list, tuple)):
        return " ".join(texte(v) for v in valeur).strip()
    return str(valeur).strip()


def identite(annonce: dict) -> tuple[str, str, str]:
    """Renvoie (nom affichable, forme juridique, type pp/pm)."""
    bloc = deplier(annonce.get("listepersonnes")) or {}
    pers = premier(bloc.get("personne") if isinstance(bloc, dict) else bloc)
    if not isinstance(pers, dict):
        pers = {}
    forme = texte(pers.get("formeJuridique"))
    type_p = texte(pers.get("typePersonne"))
    nom = texte(pers.get("denomination"))
    if not nom:
        nom = f"{texte(pers.get('prenom'))} {texte(pers.get('nom'))}".strip()
    if not nom:
        nom = texte(annonce.get("commercant")) or "(nom non publié)"
    return " ".join(nom.split()), " ".join(forme.split()), type_p


def siren(annonce: dict) -> str:
    registre = annonce.get("registre")
    if isinstance(registre, list) and registre:
        return str(registre[0]).replace(" ", "")
    if isinstance(registre, str):
        return registre.replace(" ", "").split(",")[0]
    return ""


def _motif(mots: tuple[str, ...]) -> re.Pattern:
    """Un motif ne vaut que s'il tombe sur un mot entier.

    Sans cette précaution, « spa » se reconnaît dans « espaces verts » et
    une entreprise de débarras se retrouve classée en institut de beauté.
    C'est arrivé. Le pluriel, lui, doit passer : « soins esthétiques »
    parle bien d'esthétique.
    """
    alternatives = "|".join(re.escape(m) for m in sorted(mots, key=len, reverse=True))
    return re.compile(rf"(?<!\w)(?:{alternatives})(?:s|es)?(?!\w)",
                      re.IGNORECASE)


MOTIFS_SECTEURS = [(note, libelle, _motif(mots)) for note, libelle, mots in SECTEURS]
MOTIF_SANS_OBJET = _motif(SANS_OBJET)

# Le BODACC publie souvent l'activité principale en premier, puis les
# activités accessoires. Un mot trouvé dans l'entame pèse donc double.
ENTAME = 120


def classer(texte_activite: str, forme: str) -> tuple[int, str]:
    """Renvoie (priorité 0-3, nom du secteur).

    3 — besoin immédiat et visible : carte, enseigne, vitrine, menu.
    2 — besoin réel : logo, identité, véhicule, supports imprimés.
    1 — besoin possible, à qualifier au téléphone.
    0 — rien à proposer ; écarté sauf si --tout est demandé.

    Un texte d'activité est souvent long et touche plusieurs secteurs à la
    fois. On ne retient pas le premier secteur rencontré — ce serait l'ordre
    de la liste qui décide — mais celui qui est le plus présent.
    """
    texte_complet = f"{texte_activite} {forme}"
    if MOTIF_SANS_OBJET.search(texte_complet):
        return 0, "Sans objet"
    if not texte_activite.strip():
        return 1, "Activité non publiée"

    entame = texte_activite[:ENTAME]
    classement = []
    for note, libelle, motif in MOTIFS_SECTEURS:
        poids = len(motif.findall(texte_complet)) + len(motif.findall(entame))
        if poids:
            classement.append((poids, note, libelle))
    if not classement:
        return 1, "À qualifier"
    classement.sort(reverse=True)
    _, note, libelle = classement[0]
    return note, libelle


ANNUAIRE = "https://recherche-entreprises.api.gouv.fr/search"


def adresse_postale(siren_recherche: str) -> tuple[str, str, str]:
    """Adresse, dirigeant, et statut de la vérification.

    Le BODACC ne publie que la commune. Pour écrire à quelqu'un — et un
    courrier soigné reste la meilleure carte de visite d'un graphiste — il
    faut la rue. L'annuaire des entreprises la donne, et il est ouvert.

    Le statut renvoyé compte autant que l'adresse. Un appel qui échoue ne
    doit jamais ressembler à un appel qui réussit et ne trouve rien :
    c'est de cette confusion qu'une entreprise non diffusible s'est
    retrouvée dans une liste de prospects, parce que l'erreur réseau
    était avalée en silence. Trois statuts, donc : « ok », « introuvable »
    et « non vérifié ».
    """
    if not siren_recherche:
        return "", "", "introuvable"
    params = {"q": siren_recherche, "minimal": "true",
              "include": "siege,dirigeants", "per_page": "1"}
    url = ANNUAIRE + "?" + urllib.parse.urlencode(params)
    requete = urllib.request.Request(
        url, headers={"User-Agent": "veille-grafycom/1.0 (+https://www.grafycom.fr)"}
    )
    data = None
    for essai in range(5):
        try:
            with urllib.request.urlopen(requete, timeout=25) as reponse:
                data = json.loads(reponse.read().decode("utf-8"))
            break
        except Exception:
            if essai < 4:
                time.sleep(1.5 * (essai + 1))
    if data is None:
        return "", "", "non vérifié"

    resultats = data.get("results") or []
    if not resultats:
        return "", "", "introuvable"
    fiche = resultats[0]
    siege = fiche.get("siege") or {}
    adresse = " ".join(texte(siege.get("adresse")).split())
    nom_dirigeant = ""
    for d in fiche.get("dirigeants") or []:
        if d.get("type_dirigeant") == "personne physique":
            nom_dirigeant = " ".join(
                x for x in (texte(d.get("prenoms")), texte(d.get("nom"))) if x
            )
            break
    return adresse, nom_dirigeant, "ok"


def collecter(depuis: str, jusqu_a: str) -> list[dict]:
    ou = (f"numerodepartement='{DEPARTEMENT}' AND familleavis='creation' "
          f"AND dateparution>=date'{depuis}' AND dateparution<=date'{jusqu_a}'")
    lignes, offset = [], 0
    while True:
        lot = appeler({
            "where": ou,
            "limit": PAR_PAGE,
            "offset": offset,
            "order_by": "dateparution DESC",
        })
        total = lot.get("total_count", 0)
        resultats = lot.get("results", [])
        if offset == 0:
            print(f"BODACC : {total} créations publiées dans le 66 "
                  f"du {depuis} au {jusqu_a}.")
        lignes.extend(resultats)
        offset += PAR_PAGE
        if not resultats or offset >= min(total, 10_000):
            break
        time.sleep(0.2)
    return lignes


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--jours", type=int, default=7,
                   help="profondeur de la veille en jours (défaut : 7)")
    a.add_argument("--depuis", help="date de début AAAA-MM-JJ, prioritaire sur --jours")
    a.add_argument("--adresses", action="store_true",
                   help="compléter avec l'adresse postale et le dirigeant "
                        "(un appel par entreprise, comptez ~1 min pour 200)")
    a.add_argument("--tout", action="store_true",
                   help="garder aussi les créations sans intérêt apparent")
    args = a.parse_args()

    fin = dt.date.today()
    debut = (dt.date.fromisoformat(args.depuis) if args.depuis
             else fin - dt.timedelta(days=args.jours))

    annonces = collecter(debut.isoformat(), fin.isoformat())
    if not annonces:
        print("Aucune création sur la période.")
        return 0

    exclus = lire_exclusions()
    prospects, ecartes = [], 0
    for annonce in annonces:
        nom, forme, type_p = identite(annonce)
        act = activite(annonce)
        note, secteur = classer(act, forme)
        sir = siren(annonce)

        if sir.lower() in exclus or nom.lower().replace(" ", "") in exclus:
            ecartes += 1
            continue
        if note == 0 and not args.tout:
            ecartes += 1
            continue

        acte = deplier(annonce.get("acte")) or {}
        prospects.append({
            "note": note,
            "secteur": secteur,
            "nom": nom,
            "forme": forme or ("entrepreneur individuel" if type_p == "pp" else ""),
            "ville": annonce.get("ville") or "",
            "code_postal": str(annonce.get("cp") or ""),
            "activite": act,
            "siren": sir,
            "adresse": "",
            "dirigeant": "",
            "diffusion": "non vérifié",
            "debut_activite": (acte.get("dateCommencementActivite") or ""),
            "parution": annonce.get("dateparution") or "",
            "annonce": annonce.get("url_complete") or "",
        })

    # Une même immatriculation peut faire l'objet de plusieurs annonces
    # (avis initial, puis rectificatif). On garde la plus récente.
    uniques: dict[str, dict] = {}
    doublons = 0
    for p in prospects:
        cle = p["siren"] or f"{p['nom']}|{p['ville']}"
        if cle in uniques:
            doublons += 1
            if p["parution"] <= uniques[cle]["parution"]:
                continue
        uniques[cle] = p
    prospects = list(uniques.values())

    prospects.sort(key=lambda p: (-p["note"], p["ville"], p["nom"]))

    opposes = douteux = 0
    if args.adresses:
        print(f"Recherche des adresses ({len(prospects)} appels)…")
        retenus = []
        for n, prosp in enumerate(prospects, 1):
            adr, dir_, statut = adresse_postale(prosp["siren"])
            prosp["adresse"], prosp["dirigeant"] = adr, dir_
            prosp["diffusion"] = statut
            # « [NON-DIFFUSIBLE] » : l'INSEE ne publie pas les données de
            # cette entreprise. Pour une société c'est une demande expresse ;
            # pour un entrepreneur individuel c'est devenu le réglage par
            # défaut. Dans les deux cas il n'y a pas d'adresse, donc rien à
            # quoi adresser un courrier : la fiche sort de la liste.
            if "NON-DIFFUSIBLE" in (adr + dir_).upper():
                prosp["diffusion"] = "non diffusible"
                opposes += 1
                continue
            if statut == "non vérifié":
                douteux += 1
            retenus.append(prosp)
            if n % 25 == 0:
                print(f"  {n}/{len(prospects)}")
            time.sleep(0.6)
        prospects = retenus
        if opposes:
            print(f"  {opposes} retirées : non diffusibles chez l'INSEE, "
                  f"donc sans adresse postale exploitable.")
        if douteux:
            print(f"  {douteux} non vérifiées : l'annuaire n'a pas répondu. "
                  f"Ne rien leur envoyer avant de relancer.")

    SORTIE.mkdir(exist_ok=True)
    base = f"prospects-66-{debut:%Y%m%d}-{fin:%Y%m%d}"
    chemin_csv = SORTIE / f"{base}.csv"
    colonnes = ["note", "secteur", "nom", "forme", "ville", "code_postal",
                "adresse", "dirigeant", "diffusion", "activite", "siren",
                "debut_activite", "parution", "annonce"]
    with chemin_csv.open("w", encoding="utf-8-sig", newline="") as f:
        ecrivain = csv.DictWriter(f, fieldnames=colonnes)
        ecrivain.writeheader()
        ecrivain.writerows(prospects)

    par_secteur: dict[str, list[dict]] = {}
    for p in prospects:
        par_secteur.setdefault(p["secteur"], []).append(p)

    lignes = [
        f"# Nouvelles entreprises du 66 — du {debut:%d/%m/%Y} au {fin:%d/%m/%Y}",
        "",
        f"{len(annonces)} créations publiées au BODACC, "
        f"**{len(prospects)} à regarder**, {ecartes} écartées"
        + (f", {doublons} doublons retirés" if doublons else "")
        + (f", {opposes} sans adresse diffusible" if opposes else "")
        + (f", {douteux} non vérifiées" if douteux else "") + ".",
        "",
    ]
    if args.adresses:
        lignes += ["_Diffusibilité vérifiée auprès de l'INSEE : les entreprises "
                   "dont le dirigeant s'est opposé à la diffusion de ses données "
                   "ont été retirées._", ""]
    else:
        lignes += ["> **À faire avant tout envoi :** relancer avec `--adresses`. "
                   "Sans cette étape, ni l'adresse postale ni le droit "
                   "d'opposition déjà exercé auprès de l'INSEE ne sont connus.", ""]
    for secteur in sorted(par_secteur, key=lambda s: (-par_secteur[s][0]["note"], s)):
        groupe = par_secteur[secteur]
        lignes.append(f"## {secteur} — {len(groupe)}")
        lignes.append("")
        for p in groupe:
            lignes.append(f"**{p['nom']}** — {p['ville']} ({p['code_postal']})")
            if p["adresse"]:
                lignes.append(f"  {p['adresse']}")
            if p["dirigeant"] and p["dirigeant"].lower() not in p["nom"].lower():
                lignes.append(f"  à l'attention de {p['dirigeant']}")
            if p["diffusion"] == "non vérifié":
                lignes.append("  ⚠ diffusion non vérifiée — ne rien envoyer")
            detail = p["activite"][:180] + ("…" if len(p["activite"]) > 180 else "")
            lignes.append(f"  {detail}")
            repere = [x for x in (p["forme"], f"SIREN {p['siren']}" if p["siren"] else "",
                                  f"début {p['debut_activite']}" if p["debut_activite"] else "")
                      if x]
            lignes.append(f"  _{' · '.join(repere)}_")
            lignes.append("")
        lignes.append("")

    chemin_md = SORTIE / f"{base}.md"
    chemin_md.write_text("\n".join(lignes), encoding="utf-8")

    print(f"{len(prospects)} prospects retenus, {ecartes} écartés, "
          f"{doublons} doublons.")
    for secteur in sorted(par_secteur, key=lambda s: -len(par_secteur[s])):
        print(f"  {len(par_secteur[secteur]):3d}  {secteur}")
    print(f"\n  {chemin_csv}")
    print(f"  {chemin_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
