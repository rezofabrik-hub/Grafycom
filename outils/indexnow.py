#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Signale les pages du site aux moteurs qui acceptent IndexNow.

IndexNow est un protocole ouvert : on prévient le moteur qu'une adresse a
changé, au lieu d'attendre que son robot repasse. Bing, Yandex, Seznam,
Naver et Ecosia le lisent ; Qwant s'appuie sur Bing. Google ne le lit pas :
pour Google, la seule voie reste le sitemap dans la Search Console.

Aucun compte, aucune clé d'API : l'authentification tient au fait que la
clé est publiée à la racine du site. Si le fichier n'y est pas, le moteur
refuse la soumission, et c'est tant mieux — n'importe qui pourrait sinon
soumettre les adresses de n'importe quel site.

    python3 outils/indexnow.py            # toutes les pages du sitemap
    python3 outils/indexnow.py --essai    # montre ce qui serait envoyé
    python3 outils/indexnow.py https://www.grafycom.fr/prestations.html

Le script refuse de travailler tant que le site est en construction : rien
ne sert à soumettre des pages que robots.txt interdit, et une soumission
de page interdite se retient contre le domaine.
"""
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

RACINE = pathlib.Path(__file__).resolve().parent.parent
HOTE = "www.grafycom.fr"
SITE = "https://" + HOTE
POINT = "https://api.indexnow.org/indexnow"


def cle():
    """La clé est le nom du fichier .txt de 32 caractères posé à la racine."""
    trouves = [
        f for f in RACINE.glob("*.txt")
        if re.fullmatch(r"[0-9a-f]{8,128}", f.stem)
    ]
    if not trouves:
        sortir("aucun fichier de clé IndexNow à la racine du dépôt.\n"
               "       En créer un : python3 -c \"import secrets; "
               "k=secrets.token_hex(16); open(k+'.txt','w').write(k)\"")
    if len(trouves) > 1:
        sortir("plusieurs fichiers de clé à la racine : %s.\n"
               "       N'en garder qu'un." % ", ".join(f.name for f in trouves))
    f = trouves[0]
    contenu = f.read_text(encoding="utf-8").strip()
    if contenu != f.stem:
        sortir("%s doit contenir exactement son propre nom sans l'extension "
               "(%s), il contient « %s »." % (f.name, f.stem, contenu))
    return f.stem


def sortir(message):
    sys.stderr.write("ERREUR : %s\n" % message)
    raise SystemExit(1)


def site_ouvert():
    """Vrai si le site est reellement indexable.

    On ne se fie pas a robots.txt : pendant les travaux il autorise
    deliberement l'exploration, pour que les robots puissent lire le
    noindex des pages. Le signal fiable est donc le noindex lui-meme, sur
    la page d'accueil, double de l'interrupteur des generateurs.
    """
    gen = RACINE / "generateurs" / "gen.py"
    if gen.exists() and re.search(r"^CONSTRUCTION = True\s*$",
                                  gen.read_text(encoding="utf-8"), re.M):
        return False
    accueil = RACINE / "index.html"
    if accueil.exists() and "noindex" in accueil.read_text(encoding="utf-8"):
        return False
    return True


def adresses_du_sitemap():
    s = RACINE / "sitemap.xml"
    if not s.exists():
        sortir("sitemap.xml introuvable.")
    return re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", s.read_text(encoding="utf-8"))


def soumettre(urls, k):
    corps = json.dumps({
        "host": HOTE,
        "key": k,
        "keyLocation": "%s/%s.txt" % (SITE, k),
        "urlList": urls,
    }).encode("utf-8")
    req = urllib.request.Request(
        POINT, data=corps,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as rep:
            return rep.status, rep.read().decode("utf-8", "replace")[:300]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:300]
    except urllib.error.URLError as e:
        sortir("réseau injoignable : %s" % e.reason)


EXPLICATIONS = {
    200: "accepté.",
    202: "accepté, clé en cours de validation.",
    400: "requête mal formée.",
    403: "clé refusée : le fichier n'est pas en ligne à la racine du site. "
         "Vérifier %s/<cle>.txt dans un navigateur." % SITE,
    422: "adresses refusées : elles ne correspondent pas au domaine déclaré.",
    429: "trop de soumissions, réessayer plus tard.",
}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    essai = "--essai" in sys.argv[1:]
    force = "--force" in sys.argv[1:]

    if not site_ouvert() and not force:
        sortir("le site est encore en construction : les pages portent « noindex ».\n"
               "       Soumettre maintenant n'aurait aucun effet utile.\n"
               "       Lancer ./ouvrir-le-site.sh d'abord, ou --force pour passer outre.")

    urls = args or adresses_du_sitemap()
    mauvaises = [u for u in urls if not u.startswith(SITE + "/") and u != SITE + "/"]
    if mauvaises:
        sortir("adresses hors du domaine %s : %s" % (HOTE, ", ".join(mauvaises)))

    k = cle()
    print("Clé       : %s" % k)
    print("Fichier   : %s/%s.txt" % (SITE, k))
    print("Adresses  : %d" % len(urls))
    for u in urls:
        print("            %s" % u)

    if essai:
        print("\n--essai : rien n'a été envoyé.")
        return

    code, corps = soumettre(urls, k)
    print("\nRéponse %s : %s" % (code, EXPLICATIONS.get(code, "réponse inattendue.")))
    if corps.strip():
        print("          %s" % corps.strip())
    if code not in (200, 202):
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # Arrive quand la sortie est tuyautee vers « head » : ce n'est pas
        # une erreur du script, et une trace Python donnerait a croire
        # le contraire.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        raise SystemExit(0)
