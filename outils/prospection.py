# -*- coding: utf-8 -*-
"""Prospection ciblée B2B — entreprises établies des Pyrénées-Orientales.

POURQUOI CET OUTIL PLUTÔT QUE LA VEILLE DES CRÉATIONS
-----------------------------------------------------
Mesure faite le 6 octobre 2026 sur l'API officielle : 153 champs exposés,
AUCUN champ de contact. Ni courriel, ni téléphone, ni site, ni réseau social.
Une entreprise immatriculée la semaine dernière n'a donc aucun point de
contact atteignable — ni dans le registre, ni sur le web, où elle n'est pas
encore indexée.

Conclusion : la prospection « virtuelle » vers les créations est impossible.
Elle est en revanche possible vers les entreprises ÉTABLIES, parce que
celles-là ont publié elles-mêmes leurs coordonnées sur leur propre site. Cet
outil ne collecte que ça : ce que l'entreprise a rendu public de son plein
gré, sur son site, à destination de ses clients.

CADRE JURIDIQUE
---------------
Prospection B2B : la CNIL admet l'intérêt légitime, sans consentement
préalable, dès lors que la sollicitation est en rapport avec la profession du
destinataire, que l'origine des données est indiquée et qu'une opposition
simple et gratuite est offerte. Chaque message produit par lettres.py porte
ces trois mentions. Ne pas les retirer.

PROTECTION DES DONNÉES
----------------------
Les résultats contiennent des coordonnées professionnelles. Ils sont écrits
dans outils/prospects/, déjà exclu de git par le .gitignore du dépôt, pour
la même raison que les listes de veille. Ne jamais committer ce dossier. Le champ « dirigeants » de l'API, qui contient des noms
de personnes physiques, n'est jamais lu ni conservé.

USAGE
-----
    python3 prospection.py --cibler              construit la liste qualifiée
    python3 prospection.py --cibler --anciennete 5 --max 400
    python3 prospection.py --contacts            cherche les sites et courriels
    python3 prospection.py --rapport             tableau de synthèse
"""

import argparse
import csv
import json
import re
import sys
import time
import unicodedata
from datetime import date, timedelta
from pathlib import Path

ICI = Path(__file__).resolve().parent
SORTIE = ICI / "prospects"
CIBLES = SORTIE / "cibles.json"
CONTACTS = SORTIE / "contacts.csv"

API = "https://recherche-entreprises.api.gouv.fr/search"
AGENT = "grafycom-prospection/1.0 (+https://www.grafycom.fr)"

# Une seule session réutilisée pour toutes les requêtes. Mesuré : une
# connexion TLS neuve par requête échoue environ deux fois sur trois à
# travers le proxy, alors qu'une session réutilisée passe à chaque coup.
try:
    import requests
    _s = requests.Session()
    _s.headers["User-Agent"] = AGENT
except ImportError:
    requests = None
    _s = None


# --------------------------------------------------------------- secteurs
#
# Les activités dont le besoin en communication visuelle est structurel :
# une enseigne, une carte, une vitrine, un véhicule. Clé = préfixe NAF.

SECTEURS = {
    # commerce de bouche
    "10.71C": "Boulangerie, pâtisserie",
    "10.13B": "Charcuterie",
    "47.22Z": "Boucherie",
    "47.23Z": "Poissonnerie",
    "47.21Z": "Primeur",
    "47.25Z": "Caviste",
    # hôtellerie, restauration
    "56.10A": "Restauration traditionnelle",
    "56.10C": "Restauration rapide",
    "56.21Z": "Traiteur",
    "56.30Z": "Bar, débit de boissons",
    "55.10Z": "Hôtellerie",
    "55.20Z": "Hébergement touristique",
    "55.30Z": "Camping",
    # commerce de détail
    "47.71Z": "Prêt-à-porter",
    "47.72A": "Chaussures",
    "47.75Z": "Parfumerie, cosmétiques",
    "47.76Z": "Fleuriste, jardinerie",
    "47.77Z": "Bijouterie, horlogerie",
    "47.78A": "Opticien",
    "47.59A": "Meubles, décoration",
    "47.64Z": "Articles de sport",
    "47.62Z": "Papeterie, presse",
    # services de proximité
    "96.02A": "Coiffure",
    "96.02B": "Soins de beauté",
    "96.04Z": "Bien-être, spa",
    "93.13Z": "Salle de sport",
    "85.53Z": "Auto-école",
    "68.31Z": "Agence immobilière",
    "86.23Z": "Cabinet dentaire",
    # artisanat du bâtiment et extérieur
    "43.34Z": "Peinture, vitrerie",
    "43.32A": "Menuiserie",
    "43.22A": "Plomberie, chauffage",
    "43.21A": "Électricité",
    "45.20A": "Garage automobile",
    "81.30Z": "Paysagiste",
}

# Formes juridiques et situations à écarter d'office.
EXCLUS_CATEGORIE = {"GE", "ETI"}


def secteur_de(naf):
    return SECTEURS.get(naf) if naf else None


# --------------------------------------------------------------- réseau

def interroger(params, essais=5):
    """GET sur l'API avec réessais. Renvoie le JSON ou lève."""
    if _s is None:
        raise SystemExit("le module requests est requis")
    dernier = None
    for n in range(essais):
        try:
            r = _s.get(API, params=params, timeout=60)
            if r.status_code == 429:
                time.sleep(2 + 2 * n)
                continue
            r.raise_for_status()
            return r.json()
        except Exception as e:          # réseau instable : on réessaie
            dernier = e
            time.sleep(1.5 * (n + 1))
    raise SystemExit(f"API injoignable après {essais} essais : {dernier}")


# --------------------------------------------------------------- ciblage

def cibler(anciennete, maximum, pages_par_secteur=6):
    """Construit la liste qualifiée, secteur par secteur.

    Deux mesures guident cette implémentation.

    1. Le paramètre date_creation_min de l'API est ACCEPTÉ MAIS IGNORÉ. Testé
       le 6 octobre 2026 : avec date_creation_min=2024-01-01, l'API renvoie
       des entreprises créées en 1991, 1955 et 1900 — résultat identique à
       celui d'un paramètre inexistant. L'ancienneté est donc calculée ici.

    2. Le tri par défaut de l'API place les grands comptes en tête : sur un
       échantillon de 1000 entreprises du 66 sans filtre d'activité, 0 cible
       exploitable (22 GE et 2 ETI sur les 25 premières). En revanche le
       paramètre activite_principale filtre réellement, et les pages
       profondes d'un même code NAF donnent les indépendants recherchés.
       On interroge donc code par code.
    """
    limite = (date.today() - timedelta(days=365 * anciennete)).isoformat()
    retenus, vus = [], set()
    examinees = 0

    for naf, libelle in SECTEURS.items():
        if len(retenus) >= maximum:
            break
        pris_ici = 0
        for page in range(1, pages_par_secteur + 1):
            if len(retenus) >= maximum:
                break
            d = interroger({
                "departement": "66",
                "etat_administratif": "A",
                "activite_principale": naf,
                "per_page": 25,
                "page": page,
            })
            lot = d.get("results", [])
            if not lot:
                break
            examinees += len(lot)

            for e in lot:
                siren = e.get("siren")
                if not siren or siren in vus:
                    continue
                vus.add(siren)

                siege = e.get("siege") or {}

                # Le filtre d'activité de l'API laisse passer quelques
                # intrus : on revérifie le code sur le siège.
                if (siege.get("activite_principale")
                        or e.get("activite_principale")) != naf:
                    continue

                # 1. ancienneté, calculée ici (cf. mesure 1 ci-dessus)
                creation = e.get("date_creation") or ""
                if not creation or creation > limite:
                    continue

                # 2. taille : on vise l'indépendant, pas le groupe
                if e.get("categorie_entreprise") in EXCLUS_CATEGORIE:
                    continue
                if (e.get("nombre_etablissements_ouverts") or 1) > 3:
                    continue

                # 3. le siège doit être DANS le 66.
                # Le paramètre departement de l'API retient une entreprise
                # dès qu'un de ses établissements s'y trouve : sans ce
                # contrôle, des sièges de la Meuse et du Finistère sont
                # entrés dans la liste lors du premier essai.
                cp = siege.get("code_postal") or ""
                if siege.get("departement") != "66" and not cp.startswith("66"):
                    continue

                # 4. diffusible : on respecte l'opposition INSEE
                if e.get("statut_diffusion") not in (None, "O", "diffusible"):
                    continue

                enseignes = siege.get("liste_enseignes") or []
                retenus.append({
                    "siren": siren,
                    "nom": e.get("nom_complet") or e.get("nom_raison_sociale") or "",
                    "enseigne": (siege.get("nom_commercial")
                                 or (enseignes[0] if enseignes else "")),
                    "secteur": libelle,
                    "naf": naf,
                    "creation": creation,
                    "anciennete_ans": (date.today()
                                       - date.fromisoformat(creation)).days // 365,
                    "commune": siege.get("libelle_commune") or "",
                    "code_postal": siege.get("code_postal") or "",
                    "effectif": e.get("tranche_effectif_salarie") or "",
                })
                pris_ici += 1
                if len(retenus) >= maximum:
                    break
        print(f"  {naf}  {libelle:30} {pris_ici:4}", file=sys.stderr)

    SORTIE.mkdir(parents=True, exist_ok=True)
    CIBLES.write_text(json.dumps(retenus, ensure_ascii=False, indent=1),
                      encoding="utf-8")
    print(f"\nexaminées : {examinees}")
    print(f"retenues  : {len(retenus)}  "
          f"(actives, {anciennete} ans et plus, indépendantes, "
          f"{len(SECTEURS)} secteurs ciblés)")
    print(f"écrit     : {CIBLES.relative_to(ICI.parent)}")
    return retenus


# --------------------------------------------------------------- contacts
#
# ÉTAT DE CETTE ÉTAPE : NE PAS S'EN SERVIR POUR ENVOYER.
#
# La recherche de contacts procède par DEVINETTE DE DOMAINE : on fabrique
# des noms de domaine plausibles à partir de la raison sociale et de
# l'enseigne, puis on vérifie que la page parle bien de l'entreprise.
# Mesuré le 6 octobre 2026 sur 25 cibles du 66 :
#
#     sites trouvés   1 / 25   (4 %)
#     courriels       0 / 25   (0 %)
#
# Avant de resserrer les contrôles, la méthode rendait 9 sites sur 40, mais
# 4 sur 6 étaient faux : un domaine mis en vente (lecroquant.com), un jeu
# de stratégie (rulica.com), une page vide (cerezo.com), et l'adresse d'une
# autre structure relevée au passage (restaurant@esat-salernes.com). Les
# faux positifs ont disparu ; le rendement utile aussi.
#
# CONCLUSION : la devinette de domaine n'est pas une méthode viable. Pour
# que cette étape serve, il faut une vraie source — moteur de recherche
# avec API, annuaire professionnel, ou données de la fiche Google. Tant
# qu'une telle source n'est pas branchée ici, l'étape --cibler est la
# partie utilisable de cet outil, et la liste de contacts se complète à la
# main à partir d'elle.
#
# L'étape --cibler, elle, fonctionne : 120 cibles, toutes dans le 66,
# toutes actives, indépendantes et de plus de trois ans.

RE_MAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Adresses de plateformes ou de prestataires : jamais le contact de la cible.
# Adresses qui ne sont jamais celle de la cible : outils techniques,
# domaines parqués mis en vente, textes de remplissage de gabarits.
# Chacune de ces chaînes vient d'un faux positif réellement observé.
MAIL_REJETES = (
    "sentry", "wixpress", "jquery", "godaddy", "u003", "@2x",
    "example.", "yourdomain", "domain.com", "email.com", "votredomaine",
    "domaine.com", "utilisateur@", "nom@", "prenom.nom", "adresse@",
    "domainmarket", "sedo.com", "afternic", "hugedomains", "dan.com",
    "buydomains", "namecheap", "parking",
)

# Boîtes grand public : un commerce qui publie « contact@orange.fr » sur
# SON site publie bien sa propre adresse. Les accepter est indispensable —
# les exiger sur le domaine du site faisait tomber le rendement à zéro.
FOURNISSEURS = (
    "gmail.com", "orange.fr", "wanadoo.fr", "free.fr", "sfr.fr", "laposte.net",
    "hotmail.fr", "hotmail.com", "outlook.fr", "outlook.com", "live.fr",
    "yahoo.fr", "yahoo.com", "bbox.fr", "numericable.fr", "aliceadsl.fr",
    "icloud.com", "me.com", "protonmail.com", "proton.me",
)

# Signes qu'une page est un domaine parqué ou un gabarit non rempli.
# Chaque motif vient d'un faux positif observé. « lecroquant.com » servait
# « LeCroquant.com is for sale - Premium Domain » : le motif doit porter sur
# « is for sale », pas sur « domain is for sale ».
PAGE_REJETEE = ("is for sale", "à vendre", "buy this domain", "parked domain",
                "domainmarket", "hugedomains", "afternic", "sedoparking",
                "lorem ipsum", "site en construction", "under construction")

# Une page sans titre ni texte n'identifie personne : cerezo.com répondait
# 200 avec un corps vide.
TAILLE_MINIMALE = 400

# Trois chemins suffisent : l'accueil porte souvent déjà le courriel, et
# les mentions légales sont obligatoires sur un site professionnel français.
# Au-delà, le coût en temps dépasse le gain mesuré.
PAGES_CONTACT = ("", "contact", "mentions-legales")

DELAI = 8  # secondes par requête. Un site qui ne répond pas en 8 s est
           # de toute façon un mauvais signal pour une prise de contact.


def domaine_resout(domaine):
    """Résolution DNS avant toute requête HTTP.

    C'est l'optimisation qui rend l'outil utilisable : la grande majorité
    des domaines devinés n'existent pas, et une résolution ratée coûte
    quelques millisecondes là où une requête HTTP coûte plusieurs secondes
    de délai d'attente.
    """
    import socket
    try:
        socket.setdefaulttimeout(4)
        socket.getaddrinfo(domaine, 443, proto=socket.IPPROTO_TCP)
        return True
    except Exception:
        return False


def ardoise(s):
    """Nom -> fragment de domaine plausible."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"\b(sarl|sas|sasu|eurl|sci|snc|earl|scop|societe|ets|"
               r"etablissements|monsieur|madame|mr|mme)\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s


def candidats_domaine(cible):
    base = []
    for champ in (cible.get("enseigne"), cible.get("nom")):
        if champ:
            a = ardoise(champ)
            if 3 <= len(a) <= 30:
                base.append(a)
    vus, sortie = set(), []
    for b in base:
        for tld in (".fr", ".com"):
            d = b + tld
            if d not in vus:
                vus.add(d)
                sortie.append(d)
    return sortie[:4]


def verifier_site(domaine, cible):
    """Le site existe-t-il, et parle-t-il bien de CETTE entreprise ?

    Sans cette vérification, une homonymie suffirait à attribuer à une cible
    le courriel d'une autre société. On exige donc que la page mentionne le
    nom (ou l'enseigne) ou la commune de l'entreprise.
    """
    marqueurs = [ardoise(cible.get("enseigne") or ""),
                 ardoise(cible.get("nom") or "")]
    marqueurs = [m for m in marqueurs if len(m) >= 4]
    if not domaine_resout(domaine):
        return None

    for chemin in PAGES_CONTACT:
        url = f"https://{domaine}/{chemin}".rstrip("/")
        try:
            r = _s.get(url, timeout=DELAI, allow_redirects=True)
        except Exception:
            continue
        if r.status_code != 200 or "text/html" not in r.headers.get(
                "content-type", ""):
            continue
        page = r.text[:400000]
        bas_page = page.lower()

        # Domaine parqué, gabarit vide, ou page sans contenu : on
        # abandonne ce domaine sans même regarder le nom.
        if any(x in bas_page for x in PAGE_REJETEE):
            return None
        sans_balises = re.sub(r"<[^>]+>", " ", page)
        if len(re.sub(r"\s+", " ", sans_balises).strip()) < TAILLE_MINIMALE:
            return None

        plat = ardoise(page)
        if not any(m in plat for m in marqueurs):
            continue

        # Ancre locale : la page porte-t-elle la commune de l'entreprise
        # ou un code postal du département ?
        #
        # Ce signal ne REJETTE pas, il NOTE. Mesuré : deux boulangeries
        # réellement identifiées n'affichaient ni leur commune ni leur code
        # postal sur la page d'accueil. En faire un filtre dur ramenait le
        # rendement de 9 sites à 0. En faire une note laisse à Sandra une
        # liste utilisable, où elle sait d'un coup d'œil ce qui est certain
        # et ce qui mérite un regard avant d'écrire.
        commune_plate = ardoise(cible.get("commune") or "")
        ancre_locale = (len(commune_plate) >= 4 and commune_plate in plat)
        if not ancre_locale:
            ancre_locale = bool(re.search(r"\b66[0-9]{3}\b", page))
        confiance = "haute" if ancre_locale else "moyenne"

        for m in RE_MAIL.findall(page):
            bas = m.lower()
            if any(x in bas for x in MAIL_REJETES):
                continue
            if bas.endswith((".png", ".jpg", ".gif", ".webp", ".svg")):
                continue
            # Troisième verrou : d'où vient cette adresse ?
            # Soit elle est sur le domaine du site, soit c'est une boîte
            # grand public publiée par le commerce lui-même. Tout le reste
            # est l'adresse d'un tiers citée au passage — un prestataire,
            # un partenaire, une autre structure. C'est ce cas qui avait
            # produit « restaurant@esat-salernes.com » sur le site d'un
            # commerce de Perpignan : écrire là, c'est écrire à côté.
            hote = bas.split("@")[1]
            racine = domaine.rsplit(".", 1)[0].split(".")[-1]
            if racine in hote:
                pass                      # adresse du domaine : la meilleure
            elif hote in FOURNISSEURS:
                pass                      # boîte grand public sur son site
            else:
                continue                  # adresse d'un tiers : on écarte
            return {"site": f"https://{domaine}", "courriel": m,
                    "page": url, "confiance": confiance}
        return {"site": f"https://{domaine}", "courriel": "",
                "page": url, "confiance": confiance}
    return None


def chercher_contacts(limite):
    if not CIBLES.exists():
        raise SystemExit("lancer d'abord --cibler")
    cibles = json.loads(CIBLES.read_text(encoding="utf-8"))[:limite]
    lignes, avec_site, avec_mail = [], 0, 0

    for i, c in enumerate(cibles, 1):
        trouve = None
        for d in candidats_domaine(c):
            trouve = verifier_site(d, c)
            if trouve:
                break
        if trouve:
            avec_site += 1
            if trouve["courriel"]:
                avec_mail += 1
        lignes.append({**c,
                       "site": (trouve or {}).get("site", ""),
                       "courriel": (trouve or {}).get("courriel", ""),
                       "confiance": (trouve or {}).get("confiance", ""),
                       "source": (trouve or {}).get("page", "")})
        if i % 5 == 0:
            print(f"  {i}/{len(cibles)} — sites {avec_site}, "
                  f"courriels {avec_mail}", file=sys.stderr)

    SORTIE.mkdir(parents=True, exist_ok=True)
    champs = ["siren", "nom", "enseigne", "secteur", "commune", "code_postal",
              "creation", "anciennete_ans", "site", "courriel", "confiance",
              "source"]
    with CONTACTS.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs, extrasaction="ignore")
        w.writeheader()
        w.writerows(lignes)

    n = len(lignes)
    print(f"\nexaminées        : {n}")
    print(f"site trouvé      : {avec_site}  ({100 * avec_site // max(1, n)} %)")
    print(f"courriel publié  : {avec_mail}  ({100 * avec_mail // max(1, n)} %)")
    hautes = sum(1 for l in lignes if l.get("confiance") == "haute")
    print(f"  dont confiance haute (commune ou CP 66 sur la page) : {hautes}")
    print(f"  confiance moyenne (nom seul) : {avec_site - hautes} — "
          "à vérifier d'un coup d'œil avant d'écrire")
    print(f"écrit            : {CONTACTS.relative_to(ICI.parent)}")
    print("\nCe fichier contient des coordonnées professionnelles : "
          "il ne doit jamais être committé.")
    return lignes


def rapport():
    if not CIBLES.exists():
        raise SystemExit("lancer d'abord --cibler")
    cibles = json.loads(CIBLES.read_text(encoding="utf-8"))
    par_secteur, par_commune = {}, {}
    for c in cibles:
        par_secteur[c["secteur"]] = par_secteur.get(c["secteur"], 0) + 1
        par_commune[c["commune"]] = par_commune.get(c["commune"], 0) + 1
    print(f"{len(cibles)} cibles\n")
    print("par secteur")
    for s, n in sorted(par_secteur.items(), key=lambda kv: -kv[1]):
        print(f"  {n:4}  {s}")
    print("\npar commune (10 premières)")
    for s, n in sorted(par_commune.items(), key=lambda kv: -kv[1])[:10]:
        print(f"  {n:4}  {s}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cibler", action="store_true")
    ap.add_argument("--contacts", action="store_true")
    ap.add_argument("--rapport", action="store_true")
    ap.add_argument("--anciennete", type=int, default=3,
                    help="ancienneté minimale en années (défaut 3)")
    ap.add_argument("--max", type=int, default=300)
    ap.add_argument("--limite", type=int, default=60,
                    help="nombre de cibles sondées par --contacts")
    a = ap.parse_args()

    if a.cibler:
        cibler(a.anciennete, a.max)
    elif a.contacts:
        chercher_contacts(a.limite)
    elif a.rapport:
        rapport()
    else:
        ap.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
