#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monte les reels à partir des écrans dessinés et du découpage écrit.

Pourquoi ce fichier existe
--------------------------
`visuels.py` produit les écrans des six reels, et le cahier des charges
porte leur découpage : le chrono de chaque plan et le texte de la voix
off. Il manquait le geste qui fait des deux un MP4. C'était la dernière
étape manuelle du cycle, et la seule qui se refaisait à l'identique six
fois.

Ce que ce fichier NE fait pas
-----------------------------
Il n'invente rien. Les durées viennent de la colonne « Chrono » du
découpage, le texte de la voix off de la dernière colonne du même
tableau, les images du dossier daté de `reseaux/visuels/`. Si une de ces
trois sources change, le montage change avec elle — et si elles se
contredisent (plus de lignes au tableau que d'écrans au dossier), il
s'arrête en le disant plutôt que de deviner.

C'est la même règle que pour la charte : une valeur recopiée dérive, une
valeur lue ne le peut pas. Les chronos ne sont donc écrits nulle part
ici.

La voix off
-----------
Sans clé de synthèse vocale, la vidéo sort muette — avec les bons
chronos, donc prête à recevoir une voix posée au montage. Le script de
la voix est toujours écrit à côté du MP4, en .txt, plan par plan : il se
colle tel quel dans n'importe quel outil.

Avec une clé, la voix est synthétisée et la vidéo sort montée. Les deux
réglages se lisent dans l'environnement, jamais dans le code :

    GRAFYCOM_TTS_CLE     la clé d'API du fournisseur
    GRAFYCOM_TTS_VOIX    l'identifiant de la voix choisie

Voir MISE-EN-LIGNE.md pour les poser. Ils ne se tapent jamais dans une
conversation.

Usage
-----
    python3 reseaux/reels.py --liste      # les reels trouvés
    python3 reseaux/reels.py 12           # un seul
    python3 reseaux/reels.py --tout
    python3 reseaux/reels.py 12 --voix    # avec la voix de synthèse
"""
import argparse
import os
import pathlib
import re
import subprocess
import sys
import unicodedata

RACINE = pathlib.Path(__file__).resolve().parent.parent
SOURCE = RACINE / "reseaux/propositions/a-valider/instagram-facebook.md"
VISUELS = RACINE / "reseaux/visuels"
SORTIE = RACINE / "reseaux/reels"

LARGE, HAUT = 1080, 1920
IPS = 30
FONDU = 0.35          # le fondu enchaîné entre deux écrans, en secondes

MOIS = {"janvier": 1, "février": 2, "mars": 3, "avril": 4, "mai": 5,
        "juin": 6, "juillet": 7, "août": 8, "septembre": 9,
        "octobre": 10, "novembre": 11, "décembre": 12}


def ffmpeg():
    """Le binaire ffmpeg : celui du système, sinon celui d'imageio.

    apt ne peut pas installer ffmpeg dans ce conteneur (dépôts partiels).
    imageio-ffmpeg embarque un binaire épinglé, ce qui vaut mieux de
    toute façon : la version est la même partout, et il s'installe sans
    les droits d'administration.
    """
    for essai in ("ffmpeg",):
        try:
            subprocess.run([essai, "-version"], capture_output=True, check=True)
            return essai
        except (OSError, subprocess.CalledProcessError):
            pass
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg introuvable. Installer :  pip install imageio-ffmpeg")


def _sans_accent(t):
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn").lower()


def _nettoyer(cellule):
    """Une cellule de tableau markdown, débarrassée de sa mise en forme."""
    t = cellule.strip()
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    t = re.sub(r"`(.+?)`", r"\1", t)
    return t.strip()


def decoupages():
    """Lit le cahier des charges et renvoie un découpage par reel.

    Cherche les titres de publication qui portent « REEL », puis le
    premier tableau qui suit, et n'en garde que deux colonnes : le
    chrono et la dernière, qui est la voix off. Le libellé de cette
    colonne varie — « Script voix off » ici, « Voix off » là — donc on
    prend la dernière plutôt que de chercher un intitulé exact.
    """
    if not SOURCE.exists():
        sys.exit("Introuvable : %s" % SOURCE)
    texte = SOURCE.read_text(encoding="utf-8")
    trouves = []

    titres = list(re.finditer(r"^## (\d+(?: bis)?) — (\w+) (\d{1,2}) (\w+).*$",
                              texte, re.M))
    for i, m in enumerate(titres):
        bloc = texte[m.end():titres[i + 1].start() if i + 1 < len(titres)
                     else len(texte)]
        if "REEL" not in m.group(0):
            continue
        numero = m.group(1)
        jour, mois = int(m.group(3)), MOIS.get(_sans_accent(m.group(4))
                                               .replace("aout", "août"))
        if mois is None:
            mois = MOIS.get(m.group(4).lower())
        annee = 2026

        plans = []
        for ligne in bloc.splitlines():
            if not ligne.startswith("|"):
                continue
            cols = [c for c in ligne.split("|")[1:-1]]
            if len(cols) < 4:
                continue
            chrono = _nettoyer(cols[0])
            c = re.match(r"^(\d+)\s*-\s*(\d+)\s*s$", chrono)
            if not c:
                continue                      # en-tête, séparateur, autre
            plans.append({"debut": int(c.group(1)), "fin": int(c.group(2)),
                          "voix": _nettoyer(cols[-1])})
        if plans:
            titre = re.sub(r"\s+", " ", m.group(0)[3:]).strip()
            trouves.append({"numero": numero, "titre": titre,
                            "date": (annee, mois, jour), "plans": plans})
    return trouves


def dossier_du_reel(r):
    """Le dossier d'écrans, trouvé par la DATE et non par un tableau.

    Les dossiers de `reseaux/visuels/` portent la date réelle de
    parution depuis le 14 octobre. C'est donc la date du titre qui les
    retrouve, sans qu'aucune correspondance soit recopiée ici — une
    correspondance recopiée se serait désynchronisée au prochain
    décalage de calendrier.
    """
    prefixe = "%04d-%02d-%02d-" % r["date"]
    for d in sorted(VISUELS.iterdir()):
        if d.is_dir() and d.name.startswith(prefixe):
            return d
    return None


def voix_de_synthese(textes, dossier):
    """Synthétise la voix off, si et seulement si une clé est posée."""
    cle = os.environ.get("GRAFYCOM_TTS_CLE")
    voix = os.environ.get("GRAFYCOM_TTS_VOIX")
    if not cle:
        return None
    if not voix:
        print("   GRAFYCOM_TTS_CLE est posée mais pas GRAFYCOM_TTS_VOIX : "
              "pas de voix.")
        return None
    import json
    import urllib.request
    faits = []
    for i, t in enumerate(textes, 1):
        if not t:
            faits.append(None)
            continue
        cible = dossier / ("voix%d.mp3" % i)
        req = urllib.request.Request(
            "https://api.elevenlabs.io/v1/text-to-speech/%s" % voix,
            data=json.dumps({"text": t, "model_id": "eleven_multilingual_v2"}
                            ).encode("utf-8"),
            headers={"xi-api-key": cle, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=90) as rep:
                cible.write_bytes(rep.read())
            faits.append(cible)
            print("   voix %d/%d" % (i, len(textes)))
        except Exception as e:
            print("   voix %d : échec (%s). La vidéo sortira muette." % (i, e))
            return None
    return faits


def monter(r, avec_voix=False):
    d = dossier_du_reel(r)
    if d is None:
        print("  n° %-4s dossier d'écrans introuvable pour le %04d-%02d-%02d"
              % (r["numero"], *r["date"]))
        return None
    ecrans = sorted(d.glob("*.png"))
    plans = r["plans"]
    if len(ecrans) != len(plans):
        print("  n° %-4s %d écrans dans %s mais %d plans au découpage — "
              "on ne devine pas." % (r["numero"], len(ecrans), d.name,
                                     len(plans)))
        return None

    SORTIE.mkdir(parents=True, exist_ok=True)
    travail = SORTIE / ("n%s-travail" % r["numero"])
    travail.mkdir(exist_ok=True)

    # Le script de la voix, toujours écrit : il se colle tel quel dans
    # n'importe quel outil, avec ou sans cle.
    script = SORTIE / ("n%s-voix-off.txt" % r["numero"])
    script.write_text(
        "%s\n\n" % r["titre"]
        + "\n\n".join("[%d-%d s]  %s" % (p["debut"], p["fin"], p["voix"])
                      for p in plans) + "\n", encoding="utf-8")

    pistes = voix_de_synthese([p["voix"] for p in plans], travail) \
        if avec_voix else None

    exe = ffmpeg()
    cible = SORTIE / ("reel-%s.mp4" % r["numero"])

    # Un fondu enchaine de 0,35 s entre chaque ecran. xfade raccourcit la
    # sortie d'un fondu a chaque transition : on allonge donc CHAQUE plan
    # du fondu, le dernier compris. Sans lui, la video rendait 23,67 s la
    # ou le decoupage en annonce 24 — l'ecart est invisible a l'oeil et
    # faux au chrono, ce qui est la pire combinaison.
    cmd = [exe, "-y", "-loglevel", "error"]
    for img, p in zip(ecrans, plans):
        duree = p["fin"] - p["debut"] + FONDU
        cmd += ["-loop", "1", "-t", "%.3f" % duree, "-i", str(img)]
    if pistes and any(pistes):
        for v in pistes:
            cmd += ["-i", str(v)] if v else ["-f", "lavfi", "-t", "1",
                                             "-i", "anullsrc"]

    filtres, dernier = [], None
    for i in range(len(ecrans)):
        filtres.append("[%d:v]scale=%d:%d:force_original_aspect_ratio="
                       "decrease,pad=%d:%d:(ow-iw)/2:(oh-ih)/2,setsar=1,"
                       "fps=%d[v%d]" % (i, LARGE, HAUT, LARGE, HAUT, IPS, i))
    dernier, decalage = "v0", 0.0
    for i in range(1, len(ecrans)):
        decalage += plans[i - 1]["fin"] - plans[i - 1]["debut"]
        filtres.append("[%s][v%d]xfade=transition=fade:duration=%.3f:"
                       "offset=%.3f[x%d]"
                       % (dernier, i, FONDU, decalage - FONDU, i))
        dernier = "x%d" % i

    if pistes and any(pistes):
        n = len(ecrans)
        for i, p in enumerate(plans):
            filtres.append("[%d:a]adelay=%d|%d[a%d]"
                           % (n + i, p["debut"] * 1000, p["debut"] * 1000, i))
        filtres.append("".join("[a%d]" % i for i in range(len(plans)))
                       + "amix=inputs=%d:normalize=0[son]" % len(plans))

    cmd += ["-filter_complex", ";".join(filtres), "-map", "[%s]" % dernier]
    if pistes and any(pistes):
        cmd += ["-map", "[son]", "-c:a", "aac", "-b:a", "128k"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium",
            "-crf", "20", "-movflags", "+faststart", str(cible)]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode:
        print("  n° %-4s ffmpeg a refusé :\n%s" % (r["numero"],
                                                   res.stderr[-900:]))
        return None
    duree = plans[-1]["fin"]
    print("  n° %-4s %-46s %2d s  %5.1f Mo  %s"
          % (r["numero"], d.name, duree, cible.stat().st_size / 1e6,
             "avec voix" if pistes and any(pistes) else "muet"))
    return cible


def main():
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("numero", nargs="?", help="le numéro du reel")
    a.add_argument("--liste", action="store_true")
    a.add_argument("--tout", action="store_true")
    a.add_argument("--voix", action="store_true",
                   help="synthétiser la voix off (demande GRAFYCOM_TTS_CLE)")
    args = a.parse_args()

    reels = decoupages()
    if args.liste:
        for r in reels:
            d = dossier_du_reel(r)
            print("  n° %-4s %-52s %s" % (r["numero"], r["titre"][:52],
                                          d.name if d else "— pas d'écrans"))
        return
    choisis = ([r for r in reels if r["numero"] == args.numero]
               if args.numero else reels if args.tout else None)
    if choisis is None:
        a.print_help()
        return
    if not choisis:
        sys.exit("Aucun reel n° %s." % args.numero)

    print("Montage dans %s" % SORTIE)
    faits = [c for c in (monter(r, args.voix) for r in choisis) if c]
    print("\n%d reel(s) monté(s)." % len(faits))
    if not os.environ.get("GRAFYCOM_TTS_CLE"):
        print("Muets : GRAFYCOM_TTS_CLE n'est pas posée. Le script de la "
              "voix est à côté de chaque MP4, en .txt.")


if __name__ == "__main__":
    main()
