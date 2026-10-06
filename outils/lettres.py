#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produit les courriers de félicitations, un par entreprise créée.

Pourquoi un courrier et pas un courriel
---------------------------------------
Parce qu'il n'existe aucune adresse e-mail à utiliser. Vérifié à la
source : ni le BODACC, ni Infogreffe, ni le répertoire Sirene de l'INSEE,
ni l'Annuaire des Entreprises de l'État ne collectent les courriels des
entreprises. Ils n'en ont pas. Les services qui en vendent les ont
aspirés ailleurs, ce qui pose un problème de qualité et un problème de
droit : la prospection B2B par courriel suppose une adresse obtenue
loyalement, ce qu'une adresse aspirée n'est pas.

L'adresse postale, elle, est vérifiée auprès de l'INSEE par la veille.
Et pour ce public précis, elle vaut mieux : un chef d'entreprise qui
vient d'ouvrir reçoit deux cents courriels par semaine et trois
courriers. Un courrier soigné de la part d'une graphiste est lui-même
l'argument — c'est le support qui démontre le métier.

Usage
-----
    python3 outils/lettres.py                 # la veille la plus récente
    python3 outils/lettres.py --note 3        # seulement le meilleur intérêt
    python3 outils/lettres.py --fichier ...csv

Produit un seul fichier HTML, une page par courrier, à imprimer en recto.
La sortie contient des noms et des adresses de personnes physiques : elle
reste dans outils/prospects/, exclu du dépôt.
"""
import argparse
import csv
import html
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent
SORTIE = RACINE / "prospects"

EXPEDITEUR = {
    "nom": "Sandra — Grafycom",
    "tel": "07 82 92 19 81",
    "mail": "sandra.grafycom@gmail.com",
    "site": "grafycom.fr",
}

# Une phrase par secteur. Un courrier qui parle du métier du destinataire
# se lit ; un courrier générique se jette. C'est toute la différence entre
# un publipostage et une lettre.
ACCROCHES = {
    "Restauration & bouche":
        "Pour un restaurant, tout se joue sur deux supports : la carte, "
        "qu'on lit en entier, et l'enseigne, qu'on lit de loin. Les deux "
        "méritent mieux qu'un modèle trouvé en ligne.",
    "Commerce de détail":
        "Pour un commerce, la devanture travaille vingt-quatre heures sur "
        "vingt-quatre, y compris quand vous êtes fermé. C'est le support "
        "qui mérite le plus d'attention, et souvent celui qu'on bâcle.",
    "Artisanat & bâtiment":
        "Pour un artisan, le véhicule est le premier support : il circule, "
        "il stationne devant les chantiers, il est vu cent fois par jour. "
        "Un marquage soigné vaut une campagne de publicité.",
    "Beauté & bien-être":
        "Dans votre métier, l'image est le premier soin : ce qu'on voit de "
        "la rue annonce ce qu'on ressentira à l'intérieur.",
    "Services de proximité":
        "Pour une activité de proximité, c'est la reconnaissance qui "
        "compte : être identifié du premier coup d'œil, à chaque fois.",
    "Loisirs & événementiel":
        "Dans l'événementiel, une affiche se lit en marchant, à trois "
        "mètres, parmi dix autres. Elle se conçoit pour ça.",
    "Tourisme & hébergement":
        "Pour un hébergement, la signalétique commence sur la route et se "
        "termine dans la chambre. Elle fait partie de l'accueil.",
}
DEFAUT = ("Une identité visuelle posée au départ, c'est un logo qui tient "
          "aussi bien sur une carte de visite que sur une enseigne.")

GABARIT = """<article class="lettre">
  <header>
    <p class="exp">%(exp_nom)s<br>%(tel)s · %(mail)s<br>%(site)s</p>
    <p class="dest">%(dest)s<br>%(adresse)s</p>
  </header>
  <p class="objet">Objet&nbsp;: félicitations pour votre immatriculation</p>
  <p>Bonjour%(civilite)s,</p>
  <p>J'ai vu la création de %(designation)s dans les annonces du BODACC, le
  bulletin où sont publiées toutes les immatriculations. Je me permets donc
  ce mot, en voisine.</p>
  <p>Je suis infographiste et chef de projet à Perpignan. Je construis
  l'identité visuelle des entreprises du département&nbsp;: le logo, la carte
  de visite, l'enseigne, la carte d'un restaurant, le marquage d'un
  véhicule. Tout ce qui fait qu'on vous reconnaît avant de vous
  connaître.</p>
  <p>%(accroche)s</p>
  <p>Les premières semaines sont le bon moment pour y penser&nbsp;: une
  identité posée au départ coûte moins cher qu'une identité refaite deux ans
  plus tard, quand les flyers sont imprimés et l'enseigne vissée.</p>
  <p>Si le sujet vous intéresse, je vous offre un premier échange, sans
  engagement&nbsp;: trente minutes pour comprendre votre métier et vous dire
  ce qui me semble utile — ou inutile.</p>
  <p>Très bonne installation à vous.</p>
  <p class="signature">%(exp_nom)s</p>
  <p class="mention">Vous recevez ce courrier parce que votre immatriculation
  a été publiée au BODACC. Dites-le-moi d'un mot et je retire votre
  entreprise de ma liste, définitivement.</p>
</article>
"""

PAGE = """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<title>Courriers — %(periode)s</title>
<style>
  @page { size: A4; margin: 22mm 20mm; }
  body { font: 11.5pt/1.55 Georgia, 'Times New Roman', serif; color: #2f2723;
         max-width: 170mm; margin: 0 auto; padding: 10mm; }
  .lettre { page-break-after: always; min-height: 240mm; }
  .lettre:last-child { page-break-after: auto; }
  header { display: flex; justify-content: space-between; gap: 20mm;
           margin-bottom: 18mm; }
  .exp { font-size: 10pt; line-height: 1.5; margin: 0; }
  .dest { text-align: right; margin: 0; font-size: 10.5pt; }
  .objet { font-weight: bold; margin: 0 0 8mm; }
  p { margin: 0 0 4.5mm; text-align: justify; }
  .signature { margin-top: 8mm; font-weight: bold; }
  .mention { margin-top: 12mm; font-size: 8.5pt; font-style: italic;
             color: #6d5a50; text-align: left; }
  .compte { font-family: system-ui, sans-serif; font-size: 10pt;
            color: #6d5a50; border-bottom: 1px solid #ddd;
            padding-bottom: 6mm; margin-bottom: 10mm; }
  @media print { .compte { display: none; } }
</style></head><body>
<p class="compte">%(nb)d courriers — veille du %(periode)s. Imprimer en recto,
une page par destinataire.</p>
%(lettres)s
</body></html>
"""


def plus_recent() -> pathlib.Path:
    f = sorted(SORTIE.glob("prospects-66-*.csv"))
    if not f:
        sys.exit("ERREUR : aucune veille. Lancer d'abord "
                 "outils/veille-entreprises.py --quotidien --adresses")
    return f[-1]


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--fichier")
    a.add_argument("--note", type=int, default=2,
                   help="intérêt minimal retenu (défaut : 2)")
    args = a.parse_args()

    chemin = pathlib.Path(args.fichier) if args.fichier else plus_recent()
    fiches = list(csv.DictReader(chemin.open(encoding="utf-8-sig")))

    lettres, ecartes = [], 0
    for f in fiches:
        if not f.get("adresse") or f.get("diffusion") == "non vérifié" \
                or int(f.get("note") or 0) < args.note:
            ecartes += 1
            continue
        enseigne = f.get("enseigne") or ""
        nom = f["nom"]
        # « votre entreprise CERISE & COCOTTE » se lit mieux que la raison
        # sociale administrative, quand les deux diffèrent.
        designation = ("votre entreprise %s" % enseigne) if enseigne \
            else ("votre entreprise %s" % nom if nom.isupper() else "votre entreprise")
        dirigeant = f.get("dirigeant") or ""
        lettres.append(GABARIT % {
            "exp_nom": html.escape(EXPEDITEUR["nom"]),
            "tel": EXPEDITEUR["tel"], "mail": EXPEDITEUR["mail"],
            "site": EXPEDITEUR["site"],
            "dest": html.escape(enseigne or nom),
            "adresse": html.escape(f["adresse"]),
            "civilite": "",   # jamais de « Monsieur » deviné sur un prénom
            "designation": html.escape(designation),
            "accroche": ACCROCHES.get(f["secteur"], DEFAUT),
        })

    if not lettres:
        sys.exit("Aucune fiche ne remplit les conditions.")

    periode = chemin.stem.replace("prospects-66-", "")
    cible = SORTIE / ("courriers-%s.html" % periode)
    cible.write_text(PAGE % {"periode": periode, "nb": len(lettres),
                             "lettres": "\n".join(lettres)}, encoding="utf-8")

    print("%d courriers, %d fiches écartées" % (len(lettres), ecartes))
    print("  %s" % cible)
    print("\nÀ relire avant impression. Le dernier paragraphe — le droit de")
    print("retrait — est le seul qui soit juridiquement obligatoire : il ne")
    print("se supprime pas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
