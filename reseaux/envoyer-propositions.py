#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Envoie les propositions de publications en relecture.

Le dispositif tient en une phrase : l'agent ecrit, ce script envoie,
Sandra tranche, un humain publie. Rien ne part sur les reseaux sans
qu'une personne l'ait lu et valide.

    python3 reseaux/envoyer-propositions.py                        # la plus recente
    python3 reseaux/envoyer-propositions.py reseaux/propositions/2026-10-06.md
    python3 reseaux/envoyer-propositions.py --essai                # sans envoyer
    python3 reseaux/envoyer-propositions.py --a sandra@... --copie laurent@...

Les identifiants d'envoi sont lus dans l'environnement, jamais ecrits
ici : voir outils/VEILLE-QUOTIDIENNE.md.
"""
import argparse
import html as _html
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "outils"))
from courriel import envoyer, liste  # noqa: E402

PROPOSITIONS = RACINE / "reseaux" / "propositions"
A_DEFAUT = "sandra.grafycom@gmail.com"
COPIE_DEFAUT = "rezofabrik@gmail.com"


def sortir(message: str) -> None:
    sys.stderr.write("ERREUR : %s\n" % message)
    raise SystemExit(1)


def derniere() -> pathlib.Path:
    fichiers = sorted(PROPOSITIONS.glob("*.md"))
    if not fichiers:
        sortir("aucune proposition dans %s.\n"
               "       Lancer l'agent social-grafycom d'abord." % PROPOSITIONS)
    return fichiers[-1]


def en_html(markdown: str) -> str:
    """Un rendu volontairement simple : titres, gras, listes, paragraphes.

    Pas de bibliotheque : le besoin est de relire un texte sur telephone,
    pas de publier un document. Les styles sont en ligne, seule mise en
    forme que les clients de messagerie respectent encore.
    """
    lignes = markdown.splitlines()
    sortie, dans_liste, dans_code = [], False, False

    def ferme_liste():
        nonlocal dans_liste
        if dans_liste:
            sortie.append("</ul>")
            dans_liste = False

    for ligne in lignes:
        brute = ligne.rstrip()
        if brute.startswith("```"):
            ferme_liste()
            if dans_code:
                sortie.append("</pre>")
            else:
                sortie.append('<pre style="background:#f6f6f6;padding:10px;'
                              'border-radius:5px;overflow-x:auto;'
                              'font-size:13px">')
            dans_code = not dans_code
            continue
        if dans_code:
            sortie.append(_html.escape(brute))
            continue

        t = _html.escape(brute.strip())
        # Gras et italique, apres echappement pour ne pas casser le HTML.
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
        t = re.sub(r"`(.+?)`", r'<code style="background:#f0f0f0;'
                               r'padding:1px 4px;border-radius:3px">\1</code>', t)

        if not t:
            ferme_liste()
            continue
        if t.startswith("#"):
            ferme_liste()
            niveau = len(brute.strip()) - len(brute.strip().lstrip("#"))
            taille = {1: 20, 2: 17, 3: 15}.get(niveau, 14)
            marge = "22px 0 8px" if niveau > 1 else "0 0 10px"
            sortie.append('<h%d style="font-size:%dpx;margin:%s">%s</h%d>'
                          % (min(niveau, 4), taille, marge,
                             t.lstrip("#").strip(), min(niveau, 4)))
            continue
        if t.startswith("---"):
            ferme_liste()
            sortie.append('<hr style="border:0;border-top:1px solid #e0e0e0;'
                          'margin:20px 0">')
            continue
        if re.match(r"^(-|\d+\.)\s", brute.strip()):
            if not dans_liste:
                sortie.append('<ul style="margin:6px 0;padding-left:20px">')
                dans_liste = True
            sortie.append("<li style='margin:3px 0'>%s</li>"
                          % re.sub(r"^(-|\d+\.)\s*", "", t))
            continue
        ferme_liste()
        sortie.append('<p style="margin:8px 0">%s</p>' % t)

    ferme_liste()
    if dans_code:
        sortie.append("</pre>")

    return ('<div style="font-family:-apple-system,BlinkMacSystemFont,'
            'Segoe UI,Roboto,Helvetica,Arial,sans-serif;font-size:15px;'
            'line-height:1.55;color:#1a1a1a;max-width:640px;margin:0 auto;'
            'padding:16px">'
            '<p style="background:#eef6ff;padding:12px 14px;border-radius:6px;'
            'margin:0 0 20px;font-size:14px">Propositions de publications, '
            '<strong>à relire avant toute publication</strong>. Rien n\'a été '
            'publié et rien ne le sera automatiquement : la mise en ligne se '
            'fait à la main, depuis Meta Business Suite.</p>'
            + "\n".join(sortie) +
            '<hr style="border:0;border-top:1px solid #e0e0e0;margin:24px 0 12px">'
            '<p style="color:#888;font-size:12px;margin:0">Préparé par '
            'l\'agent social-grafycom. Pour demander une correction, répondre '
            'à ce message.</p></div>')


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("fichier", nargs="?", help="proposition à envoyer "
                                             "(défaut : la plus récente)")
    a.add_argument("--a", default=A_DEFAUT, help="destinataires, séparés par des virgules")
    a.add_argument("--copie", default=COPIE_DEFAUT, help="adresses en copie")
    a.add_argument("--essai", action="store_true",
                   help="montrer ce qui serait envoyé, sans envoyer")
    args = a.parse_args()

    chemin = pathlib.Path(args.fichier) if args.fichier else derniere()
    if not chemin.exists():
        sortir("%s introuvable." % chemin)

    markdown = chemin.read_text(encoding="utf-8")
    if not markdown.strip():
        sortir("%s est vide : rien à envoyer." % chemin.name)

    # Le premier titre du fichier sert d'objet : c'est l'agent qui le choisit.
    titre = next((l.lstrip("#").strip() for l in markdown.splitlines()
                  if l.startswith("#")), "Propositions de publications")
    sujet = "Grafycom — %s" % titre

    dests, copies = liste(args.a), liste(args.copie)
    print("Fichier      : %s" % chemin)
    print("Objet        : %s" % sujet)
    print("Destinataire : %s" % ", ".join(dests))
    if copies:
        print("Copie        : %s" % ", ".join(copies))

    if args.essai:
        apercu = RACINE / "reseaux" / "propositions" / (chemin.stem + "-apercu.html")
        apercu.write_text(en_html(markdown), encoding="utf-8")
        print("\n--essai : rien n'a été envoyé.")
        print("Aperçu   : %s" % apercu)
        return 0

    try:
        envoyer(dests, copies, sujet, en_html(markdown), markdown)
    except Exception as e:
        sortir(str(e))
    print("\nEnvoyé.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
