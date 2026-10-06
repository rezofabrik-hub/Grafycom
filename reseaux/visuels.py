#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique les visuels des publications, sans quota et sans connecteur.

Pourquoi ce fichier existe
--------------------------
Les visuels ont d'abord été commandés à Canva. Trois défauts mesurés, tous
publics si on ne les attrape pas :

1. le format partait en 1080x1920 quand on demandait un post ;
2. le pseudo ressortait « @grafycom graphiste », sans le point ;
3. et surtout, la police choisie n'avait pas les accents français :
   « crédible » devenait « crıdible », « problème » devenait « problØme ».

S'y ajoute un quota de crédits qui s'épuise, et qui arrête la production
au milieu d'un cycle.

Ici, rien de tout ça. Le texte est écrit par Pillow avec Inter — la police
du site, extraite de assets/fonts et instanciée en graisse 800, 600 et 400,
accents compris. Le format est imposé en dur. Le pseudo est une constante.
Aucun appel réseau, aucun crédit, autant de visuels qu'on veut.

Ce que ce fichier NE fait pas : les photographies. Une devanture, une
matière, un plan de travail se photographient. C'est le métier de Sandra,
et une photo inventée sur le compte d'une graphiste se retourne contre elle.

Usage
-----
    python3 reseaux/visuels.py --exemple        # régénère le carrousel du 7
    python3 reseaux/visuels.py --liste          # les gabarits disponibles

Depuis un script :
    from visuels import Planche, LARGE, HAUT
"""
import argparse
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

RACINE = pathlib.Path(__file__).resolve().parent
POLICES = RACINE / "polices"
SORTIE = RACINE / "visuels"

LARGE, HAUT = 1080, 1350          # format 4:5, le post Instagram
LARGE_S, HAUT_S = 1080, 1920      # format 9:16, la story
MARGE = 86
PSEUDO = "@grafycom.graphiste"    # avec le point. C'est une constante
                                  # justement pour qu'il ne se perde plus.

# La charte, reprise des variables CSS du site.
C = {
    "creme":  "#f7f1ef",
    "blanc":  "#ffffff",
    "encre":  "#2f2723",
    "violet": "#a86cd0",
    "bleu":   "#2f7fc4",
    "corail": "#f2585c",
    "rose":   "#e75ba6",
    "vert":   "#3a6b4a",
    "jaune":  "#f5e6a8",
    "brun":   "#6d5a50",
}


def police(graisse: int, taille: int) -> ImageFont.FreeTypeFont:
    f = POLICES / ("Inter-%d.ttf" % graisse)
    if not f.exists():
        sys.exit("ERREUR : %s manquante. Voir le commentaire en tête de ce "
                 "fichier : les polices viennent de assets/fonts." % f)
    return ImageFont.truetype(str(f), taille)


def couper(texte: str, fonte, largeur: int) -> list[str]:
    """Découpe un texte à la largeur donnée, en respectant les retours forcés."""
    lignes = []
    for para in texte.split("\n"):
        mots, courante = para.split(), ""
        for mot in mots:
            essai = (courante + " " + mot).strip()
            if fonte.getlength(essai) <= largeur or not courante:
                courante = essai
            else:
                lignes.append(courante)
                courante = mot
        lignes.append(courante)
    return lignes


class Planche:
    """Une page de carrousel, ou un écran de story."""

    def __init__(self, fond="creme", large=LARGE, haut=HAUT):
        self.l, self.h = large, haut
        self.im = Image.new("RGB", (large, haut), C.get(fond, fond))
        self.d = ImageDraw.Draw(self.im)
        self.y = MARGE

    # -- fonds -------------------------------------------------------
    def bandeau_bas(self, couleur="violet", part=0.33):
        """Un aplat plein sur le bas de la planche."""
        haut = int(self.h * (1 - part))
        self.d.rectangle([0, haut, self.l, self.h], fill=C.get(couleur, couleur))
        return self

    # -- texte -------------------------------------------------------
    def titre(self, texte, taille=96, couleur="encre", interligne=1.06, y=None):
        f = police(800, taille)
        if y is not None:
            self.y = y
        for ligne in couper(texte, f, self.l - 2 * MARGE):
            self.d.text((MARGE, self.y), ligne, font=f, fill=C.get(couleur, couleur))
            self.y += int(taille * interligne)
        return self

    def texte(self, contenu, taille=38, couleur="brun", graisse=400,
              interligne=1.38, avant=22):
        f = police(graisse, taille)
        self.y += avant
        for ligne in couper(contenu, f, self.l - 2 * MARGE):
            self.d.text((MARGE, self.y), ligne, font=f, fill=C.get(couleur, couleur))
            self.y += int(taille * interligne)
        return self

    def signature(self, couleur="blanc"):
        """Le pseudo, en bas à gauche. Jamais saisi à la main ailleurs."""
        f = police(600, 26)
        self.d.text((MARGE, self.h - MARGE - 26), PSEUDO, font=f,
                    fill=C.get(couleur, couleur))
        return self

    def numero(self, n, total, couleur="brun"):
        f = police(600, 24)
        t = "%d/%d" % (n, total)
        self.d.text((self.l - MARGE - f.getlength(t), MARGE - 30), t,
                    font=f, fill=C.get(couleur, couleur))
        return self

    # -- formes ------------------------------------------------------
    def disques(self, couleurs, legendes=None, y=None, diam=230):
        """Trois pastilles de couleur, avec une légende facultative."""
        y = self.y if y is None else y
        n = len(couleurs)
        espace = (self.l - 2 * MARGE - n * diam) // max(n - 1, 1)
        x = MARGE
        for i, c in enumerate(couleurs):
            self.d.ellipse([x, y, x + diam, y + diam], fill=C.get(c, c))
            if legendes and legendes[i]:
                f = police(600, 25)
                for j, l in enumerate(legendes[i].split("\n")):
                    w = f.getlength(l)
                    self.d.text((x + (diam - w) / 2, y + diam + 22 + j * 32),
                                l, font=f, fill=C["brun"])
            x += diam + espace
        self.y = y + diam + (90 if legendes else 50)
        return self

    def deux_cartes(self, gauche, droite, texte="12 €", y=None,
                    larg=390, haut=470):
        """Deux aplats portant le même texte : la démonstration de contraste.

        Le texte est écrit dans la même couleur sur les deux : c'est tout
        l'intérêt. Si on trichait, la démonstration ne vaudrait rien.
        """
        y = self.y if y is None else y
        f = police(800, 118)
        ecart = self.l - 2 * MARGE - 2 * larg
        for i, fond in enumerate((gauche, droite)):
            x = MARGE + i * (larg + ecart)
            self.d.rectangle([x, y, x + larg, y + haut], fill=C.get(fond, fond))
            w = f.getlength(texte)
            self.d.text((x + (larg - w) / 2, y + haut / 2 - 75), texte,
                        font=f, fill=C["blanc"])
        self.y = y + haut + 40
        return self

    def fleche(self, couleur="corail", y=None, taille=54):
        y = self.y if y is None else y
        f = police(800, taille)
        self.d.text((MARGE, y), "→", font=f, fill=C.get(couleur, couleur))
        self.y = y + taille + 20
        return self

    # -- mesure et centrage ------------------------------------------
    #
    # Une planche dont le texte est collé en haut laisse un vide en bas qui
    # se voit tout de suite. On mesure donc le bloc avant de le dessiner,
    # et on le pose au centre optique : legerement au-dessus du milieu
    # geometrique, parce que l'oeil place le centre plus haut qu'il n'est.

    def h_titre(self, texte, taille=96, interligne=1.06):
        f = police(800, taille)
        return len(couper(texte, f, self.l - 2 * MARGE)) * int(taille * interligne)

    def h_texte(self, contenu, taille=38, interligne=1.38, avant=22, graisse=400):
        f = police(graisse, taille)
        n = len(couper(contenu, f, self.l - 2 * MARGE))
        return avant + n * int(taille * interligne)

    def centrer(self, hauteur_totale, remonte=0.46):
        self.y = int(self.h * remonte - hauteur_totale / 2)
        return self

    # -- formes supplementaires ----------------------------------------
    def devanture(self, x, y, larg, haut, mot, graisse, taille,
                  fond="#e8e2dc", bandeau="#2f2723", texte_couleur="#f7f1ef"):
        """Une facade schematique avec son enseigne, pour le test A/B."""
        self.d.rectangle([x, y, x + larg, y + haut], fill=fond)
        hb = int(haut * 0.26)
        self.d.rectangle([x, y, x + larg, y + hb], fill=bandeau)
        f = police(graisse, taille)
        w = f.getlength(mot)
        self.d.text((x + (larg - w) / 2, y + hb / 2 - taille * 0.62), mot,
                    font=f, fill=texte_couleur)
        # La vitrine, pour que ca ressemble a un commerce.
        self.d.rectangle([x + larg * .12, y + hb + haut * .18,
                          x + larg * .88, y + haut * .86], fill="#cfc6bd")
        return self

    def pastille(self, x, y, texte, fond, couleur="blanc", taille=30, pad=16):
        f = police(800, taille)
        w = f.getlength(texte)
        self.d.rounded_rectangle([x, y, x + w + pad * 2, y + taille + pad],
                                 radius=(taille + pad) // 2, fill=C.get(fond, fond))
        self.d.text((x + pad, y + pad / 2 - 2), texte, font=f,
                    fill=C.get(couleur, couleur))
        return w + pad * 2

    def flouter(self, rayon=14):
        from PIL import ImageFilter
        self.im = self.im.filter(ImageFilter.GaussianBlur(rayon))
        self.d = ImageDraw.Draw(self.im)
        return self

    def sticker(self, titre, lignes, y=None, fond="blanc"):
        """Le cartouche qui imite un sticker Instagram, pour les stories."""
        y = self.y if y is None else y
        ft, fl = police(600, 24), police(600, 30)
        haut = 30 + 34 + len(lignes) * 44 + 24
        self.d.rounded_rectangle([MARGE, y, self.l - MARGE, y + haut],
                                 radius=28, fill=C.get(fond, fond))
        self.d.text((MARGE + 30, y + 24), titre.upper(), font=ft, fill=C["brun"])
        for i, l in enumerate(lignes):
            self.d.text((MARGE + 30, y + 66 + i * 44), l, font=fl, fill=C["encre"])
        self.y = y + haut + 24
        return self

    # -- sortie ------------------------------------------------------
    def ecrire(self, chemin):
        p = pathlib.Path(chemin)
        p.parent.mkdir(parents=True, exist_ok=True)
        self.im.save(p, "PNG")
        return p


# ---------------------------------------------------------------------
# Le carrousel du 7 octobre, en exemple complet et reproductible.
# ---------------------------------------------------------------------
def carrousel_couleurs(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-10-07-couleurs"))
    faits = []

    p = Planche("creme").bandeau_bas("violet", 0.30)
    p.titre("Votre couleur dit déjà ce que vous vendez.", 104, y=230)
    p.signature("blanc")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("blanc")
    p.titre("Avant même de lire votre nom…", 62, y=170)
    p.disques(["vert", "bleu", "rose"], y=460)
    p.texte("Le client a déjà deviné votre secteur.", 42, "encre", 600, avant=90)
    faits.append(p.ecrire(d / "02.png"))

    p = Planche("blanc")
    p.disques(["vert", "bleu", "rose"],
              ["BIO\nSANTÉ", "BANQUE\nCONSEIL", "SOIN\nENFANCE"], y=250)
    p.titre("Ce ne sont pas des règles.\nCe sont des réflexes.", 66, y=820)
    faits.append(p.ecrire(d / "03.png"))

    p = Planche("violet")
    t = "Les suivre vous rend crédible.\nLes casser vous rend mémorable."
    st = "Le problème, c'est de le faire sans le savoir."
    p.centrer(p.h_titre(t, 78) + p.h_texte(st, 40, avant=60))
    p.titre(t, 78, "blanc")
    p.texte(st, 40, "blanc", 400, avant=60)
    faits.append(p.ecrire(d / "04.png"))

    p = Planche("creme")
    p.titre("Le même prix. Deux fonds.", 62, y=170)
    p.deux_cartes("jaune", "bleu", "12 €", y=330)
    p.titre("Le contraste se vérifie.\nIl ne se devine pas.", 62, y=900)
    faits.append(p.ecrire(d / "05.png"))

    p = Planche("blanc")
    p.titre("Votre secteur en commentaire.", 86, y=320)
    p.texte("Je vous propose trois couleurs pour vous démarquer de vos "
            "concurrents directs.", 40, "brun", 400, avant=40)
    p.fleche("corail", y=820)
    p.signature("brun")
    faits.append(p.ecrire(d / "06.png"))

    return faits


def dilemme_enseigne(dossier=None):
    """Le test A/B du 8 octobre. La seconde planche est la premiere, floutee.

    Le flou n'illustre pas, il demontre. Il est applique par le script a la
    planche nette : les deux images sont donc rigoureusement identiques
    sauf le flou, et on ne peut pas tricher.

    Le reglage du rayon est le coeur du visuel. Trop fort, les deux mots
    disparaissent et la demonstration ne prouve rien — c'etait le cas au
    premier essai, a 16 pixels. A 8, le lettrage fin se dissout et le
    lettrage gras tient : c'est precisement ce qu'on veut montrer.

    Les lettres A et B sont tracees APRES le flou. Ce sont des reperes de
    lecture, pas des elements de la scene : les flouter les rendrait
    inutiles.
    """
    d = pathlib.Path(dossier or (SORTIE / "2026-10-08-dilemme"))
    faits = []
    LARG, HAUTF, ECART = 420, 430, 60
    X0 = (LARGE - 2 * LARG - ECART) // 2
    Y0 = 500

    def facades(p):
        # Meme mot, meme corps. Seule la graisse change : c'est la variable
        # testee, et la seule.
        p.devanture(X0, Y0, LARG, HAUTF, "MAISON", 400, 62)
        p.devanture(X0 + LARG + ECART, Y0, LARG, HAUTF, "MAISON", 800, 62)
        return p

    def reperes(p):
        f = police(800, 62)
        for i, lettre in enumerate(("A", "B")):
            x = X0 + i * (LARG + ECART)
            w = f.getlength(lettre)
            p.d.text((x + (LARG - w) / 2, Y0 + HAUTF + 34), lettre,
                     font=f, fill=C["corail"])
        return p

    p = Planche("creme")
    p.titre("Laquelle se lit\ndepuis le trottoir d'en face ?", 72, y=190)
    facades(p); reperes(p)
    p.signature("brun")
    faits.append(p.ecrire(d / "01.png"))

    p = Planche("creme")
    facades(p)
    p.flouter(8)
    reperes(p)                      # nets : ce sont des reperes
    p.titre("À vingt mètres,\nce n'est plus une typo.", 72, y=190)
    p.titre("C'est une silhouette.", 76, "corail", y=1120)
    faits.append(p.ecrire(d / "02.png"))
    return faits


def carrousel_typographie(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-10-12-typographie"))
    f = []
    p = Planche("blanc")
    t = "Cette police est magnifique."
    p.centrer(p.h_titre(t, 92) + p.h_texte("Et elle va vous coûter des clients.", 44, avant=40))
    p.titre(t, 92)
    p.texte("Et elle va vous coûter des clients.", 44, "corail", 600, avant=40)
    p.signature("brun"); f.append(p.ecrire(d / "01.png"))

    p = Planche("creme")
    p.titre("Lisible sur une carte.\nIllisible sur une bâche.", 70, y=220)
    p.texte("La même police, quatre supports, quatre résultats.", 40, "brun", 400, avant=50)
    p.devanture(MARGE, 700, 400, 380, "MAISON", 400, 40)
    p.devanture(MARGE + 480, 700, 400, 380, "MAISON", 800, 48)
    f.append(p.ecrire(d / "02.png"))

    p = Planche("violet")
    t = "Trois questions\navant de choisir\nune police."
    p.centrer(p.h_titre(t, 86)); p.titre(t, 86, "blanc")
    f.append(p.ecrire(d / "03.png"))

    p = Planche("blanc")
    p.titre("1. À quelle distance\nsera-t-elle lue ?", 70, y=230)
    p.texte("Une carte de visite se lit à bout de bras.\n"
            "Un menu, à table, parfois le soir.\n"
            "Une enseigne, à vingt mètres.\n\n"
            "Ce ne sont pas les mêmes polices.", 42, "brun", 400, avant=60)
    f.append(p.ecrire(d / "04.png"))

    p = Planche("creme")
    p.titre("2. Tient-elle\nen tout petit ?", 70, y=200)
    p.texte("Vos mentions, votre numéro, votre adresse. Si c'est illisible "
            "à six points, le problème n'est pas l'imprimeur.", 40, "brun", 400, avant=40)
    p.titre("3. Avez-vous le droit\nde l'utiliser ?", 70, y=830)
    p.texte("Une police gratuite n'est pas forcément libre pour un usage "
            "commercial.", 40, "brun", 400, avant=30)
    f.append(p.ecrire(d / "05.png"))

    p = Planche("bleu")
    t = "Une identité,\nc'est deux polices."
    st = "Une pour les titres, une pour le texte. Pas cinq."
    p.centrer(p.h_titre(t, 88) + p.h_texte(st, 42, avant=50))
    p.titre(t, 88, "blanc"); p.texte(st, 42, "blanc", 400, avant=50)
    p.signature("blanc"); f.append(p.ecrire(d / "06.png"))
    return f


def carrousel_enseigne(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-10-13-enseigne"))
    f = []
    p = Planche("violet")
    t = "Votre enseigne a besoin\nd'une autorisation.\nPas d'une déclaration."
    p.centrer(p.h_titre(t, 80)); p.titre(t, 80, "blanc")
    p.signature("blanc"); f.append(p.ecrire(d / "01.png"))

    p = Planche("blanc")
    p.titre("La confusion\nla plus répandue", 76, y=200)
    p.d.line([MARGE, 620, MARGE + 620, 620], fill=C["corail"], width=6)
    p.texte("Déclaration préalable", 54, "brun", 600, avant=20)
    p.y = 700
    p.texte("Autorisation préalable", 54, "violet", 800, avant=60)
    f.append(p.ecrire(d / "02.png"))

    p = Planche("creme")
    t = "Cerfa n° 16308*01"
    p.centrer(p.h_titre(t, 92) + p.h_texte("À déposer en mairie,\nen trois exemplaires.", 46, avant=50))
    p.titre(t, 92); p.texte("À déposer en mairie,\nen trois exemplaires.", 46, "brun", 600, avant=50)
    f.append(p.ecrire(d / "03.png"))

    p = Planche("blanc")
    p.titre("Au-delà de trois\ndispositifs ?", 76, y=250)
    p.texte("Le formulaire se remplit une seconde fois.", 44, "brun", 400, avant=50)
    p.texte("Enseigne en bandeau · caisson en drapeau · lettrage de vitrine "
            "· adhésif de porte. Ça fait déjà quatre.", 38, "corail", 600, avant=70)
    f.append(p.ecrire(d / "04.png"))

    p = Planche("creme")
    p.titre("Ce qui change\nselon la commune", 74, y=200)
    for i, (n, txt) in enumerate((("1", "Le Règlement Local de Publicité"),
                                  ("2", "Le Plan Local d'Urbanisme"),
                                  ("3", "Le secteur patrimonial protégé"))):
        y = 620 + i * 150
        p.pastille(MARGE, y, n, "corail", "blanc", 34)
        p.d.text((MARGE + 110, y + 8), txt, font=police(600, 40), fill=C["encre"])
    f.append(p.ecrire(d / "05.png"))

    p = Planche("bleu")
    t = "À Perpignan, le centre ancien\nest en secteur protégé."
    st = ("L'avis des Architectes des Bâtiments de France s'ajoute au dossier. "
          "Il oriente le choix des matières bien avant celui du logo.")
    p.centrer(p.h_titre(t, 68) + p.h_texte(st, 40, avant=50))
    p.titre(t, 68, "blanc"); p.texte(st, 40, "blanc", 400, avant=50)
    f.append(p.ecrire(d / "06.png"))

    p = Planche("violet")
    t = "Une enseigne se pense\nen amont."
    p.centrer(p.h_titre(t, 86) + p.h_texte("Pas après le logo.", 50, avant=40))
    p.titre(t, 86, "blanc"); p.texte("Pas après le logo.", 50, "blanc", 600, avant=40)
    p.signature("blanc"); f.append(p.ecrire(d / "07.png"))
    return f


def quiz_idees_recues(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-10-15-quiz"))
    f = []
    p = Planche("violet")
    p.pastille(MARGE, 240, "QUIZ", "corail", "blanc", 30)
    t = "4 idées reçues\nsur l'impression\net les enseignes."
    p.y = 380; p.titre(t, 84, "blanc")
    p.texte("Combien allez-vous rater ?", 46, "blanc", 600, avant=40)
    p.signature("blanc"); f.append(p.ecrire(d / "01.png"))

    questions = [
        ("« Une enseigne se déclare\nen mairie. »", "FAUX", "Elle s'autorise. Cerfa 16308*01."),
        ("« Un logo doit rester lisible\nen noir et blanc. »", "VRAI", "Sinon il échoue sur un tampon, une gravure, une broderie."),
        ("« 300 DPI convient\nà toutes les bâches. »", "FAUX", "La résolution se calcule à la distance de lecture."),
        ("« Une police gratuite est libre\npour un usage commercial. »", "FAUX", "Presque jamais vérifié, et c'est celui qui coûte."),
    ]
    for i, (q, rep, expl) in enumerate(questions, start=2):
        fond = "blanc" if i % 2 == 0 else "creme"
        p = Planche(fond)
        p.titre(q, 64, y=240)
        x = p.pastille(MARGE, 700, "VRAI", "bleu", "blanc", 32)
        p.pastille(MARGE + x + 24, 700, "FAUX", "corail", "blanc", 32)
        p.y = 860
        p.titre(rep, 92, "violet" if rep == "VRAI" else "corail")
        p.texte(expl, 38, "brun", 400, avant=20)
        f.append(p.ecrire(d / ("%02d.png" % i)))
    return f


def carrousel_droits(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-10-20-droits"))
    f = []
    p = Planche("creme")
    t = "Qui possède\nvotre logo ?"
    p.centrer(p.h_titre(t, 110) + p.h_texte("La réponse surprend la plupart des chefs d'entreprise.", 42, avant=50))
    p.titre(t, 110); p.texte("La réponse surprend la plupart des chefs d'entreprise.", 42, "brun", 400, avant=50)
    p.signature("brun"); f.append(p.ecrire(d / "01.png"))

    p = Planche("bleu")
    t = "Vous l'avez payé.\nVous ne le possédez\npas forcément."
    st = "Payer une création ne transfère pas les droits d'auteur. Le transfert se fait par écrit, et seulement par écrit."
    p.centrer(p.h_titre(t, 80) + p.h_texte(st, 40, avant=50))
    p.titre(t, 80, "blanc"); p.texte(st, 40, "blanc", 400, avant=50)
    f.append(p.ecrire(d / "02.png"))

    p = Planche("blanc")
    p.titre("Ce qui se cède,\net ce qui ne se cède pas", 66, y=200)
    p.texte("Les droits patrimoniaux se cèdent : exploiter, reproduire, adapter.", 42, "encre", 600, avant=70)
    p.texte("Le droit moral, jamais. Il reste à l'auteur, à vie.", 42, "corail", 600, avant=40)
    f.append(p.ecrire(d / "03.png"))

    p = Planche("creme")
    p.titre("Une cession se précise", 74, y=240)
    for i, txt in enumerate(("Pour quels supports.", "Sur quel territoire.",
                             "Pour combien de temps.")):
        y = 560 + i * 140
        p.pastille(MARGE, y, str(i + 1), "violet", "blanc", 34)
        p.d.text((MARGE + 110, y + 8), txt, font=police(600, 44), fill=C["encre"])
    f.append(p.ecrire(d / "04.png"))

    p = Planche("blanc")
    p.titre("Pourquoi ça compte\nun jour", 74, y=200)
    p.texte("Le jour où vous vendez l'entreprise.\n"
            "Le jour où vous déposez votre marque.\n"
            "Le jour où vous changez de prestataire.", 44, "brun", 400, avant=70)
    f.append(p.ecrire(d / "05.png"))

    p = Planche("violet")
    t = "Demandez votre\ncontrat de cession."
    st = "S'il n'existe pas, c'est le moment de le faire."
    p.centrer(p.h_titre(t, 88) + p.h_texte(st, 44, avant=50))
    p.titre(t, 88, "blanc"); p.texte(st, 44, "blanc", 600, avant=50)
    p.signature("blanc"); f.append(p.ecrire(d / "06.png"))
    return f


def plans_reel_cmjn(dossier=None):
    """Les cinq plans du reel du 9 octobre, en 9:16, a enchainer au montage."""
    d = pathlib.Path(dossier or (SORTIE / "2026-10-09-reel-cmjn"))
    f = []
    plans = [
        ("creme", "encre", "Pourquoi ce n'est jamais\nla même couleur", ""),
        ("blanc", "encre", "RVB", "De la lumière.\nRouge, vert, bleu.\nPlus on en met, plus c'est clair."),
        ("encre", "blanc", "CMJN", "Quatre encres.\nCyan, magenta, jaune, noir.\nChaque couche retire de la lumière."),
        ("creme", "encre", "Le papier\nchange tout", "Un mat absorbe.\nUn couché renvoie."),
        ("violet", "blanc", "Demandez un BAT.\nToujours.", "C'est gratuit, et ça évite de tout refaire."),
    ]
    for i, (fond, enc, titre, sous) in enumerate(plans, 1):
        p = Planche(fond, LARGE_S, HAUT_S)
        h = p.h_titre(titre, 96) + (p.h_texte(sous, 46, avant=60) if sous else 0)
        p.centrer(h, 0.44)
        p.titre(titre, 96, enc)
        if sous:
            p.texte(sous, 46, enc, 400, avant=60)
        p.signature(enc)
        f.append(p.ecrire(d / ("plan%d.png" % i)))
    return f


def plans_reel_halloween(dossier=None):
    d = pathlib.Path(dossier or (SORTIE / "2026-10-16-reel-halloween"))
    f = []
    plans = [
        ("#111111", "#f5883c", "Pourquoi Halloween\nest orange et noir", ""),
        ("#f5883c", "#111111", "Le contraste\nmaximal", "On le repère avant de comprendre ce qu'on regarde."),
        ("#111111", "#f5883c", "La nature\nl'utilise déjà", "Guêpes, serpents, rubans de chantier.\nLe message : attention."),
        ("creme", "encre", "Et pour\nvotre vitrine ?", "Parfait en saisonnier.\nÉpuisant toute l'année."),
        ("violet", "blanc", "Une couleur\nn'est jamais neutre.", "Elle dit quelque chose avant vous."),
    ]
    for i, (fond, enc, titre, sous) in enumerate(plans, 1):
        p = Planche(fond, LARGE_S, HAUT_S)
        h = p.h_titre(titre, 96) + (p.h_texte(sous, 46, avant=60) if sous else 0)
        p.centrer(h, 0.44)
        p.titre(titre, 96, enc)
        if sous:
            p.texte(sous, 46, enc, 400, avant=60)
        p.signature(enc)
        f.append(p.ecrire(d / ("plan%d.png" % i)))
    return f


def stories(dossier=None):
    """Les dix ecrans de stories du cycle, en 9:16."""
    d = pathlib.Path(dossier or (SORTIE / "stories"))
    f = []
    ecrans = [
        ("07-teasing", "creme", "encre", "Nouveau post.\nVotre couleur parle avant vous.",
         "Sondage", ["Le bleu marine évoque plutôt…", "A : la confiance", "B : le luxe"]),
        ("13-quiz-1", "bleu", "blanc", "Enseigne :\ndéclaration ou autorisation ?",
         "Quiz", ["Déclaration préalable", "Autorisation préalable"]),
        ("13-quiz-2", "violet", "blanc", "Autorisation.\nCerfa 16308*01, en mairie,\nen trois exemplaires.",
         "Mention du post", ["Le détail est dans le post du jour"]),
        ("14-questions", "violet", "blanc",
         "Une question sur votre\nidentité visuelle ?",
         "Boîte à questions", ["Je réponds à tout.", "Même aux questions bêtes.", "Surtout à celles-là."]),
        ("08-vote-1", "blanc", "encre", "Laquelle se lit\nà vingt mètres ?",
         "Sondage", ["A", "B"]),
        ("08-vote-2", "creme", "encre", "Réponse : B.\nÀ vingt mètres, une typo\ndevient une silhouette.",
         "Curseur emoji", ["Vous aviez deviné ?"]),
        ("09-blog", "creme", "encre", "Nouvel article :\nl'autorisation d'enseigne,\nétape par étape.",
         "Sticker Lien", ["grafycom.fr/blog"]),
        ("12-teasing", "creme", "encre", "Cette police est magnifique.\nEt pourtant…",
         "Curseur emoji", ["Vous choisissez vos polices au feeling ?"]),
        ("20-teasing", "blanc", "encre", "Avez-vous un contrat de cession\npour votre logo ?",
         "Sondage", ["A : oui, je l'ai", "B : aucune idée"]),
        ("21-coulisses", "creme", "encre",
         "Trois pistes pour un même logo.\nDeux finiront à la corbeille.",
         "", ["C'est normal. C'est même le travail."]),
    ]
    for nom, fond, enc, titre, st, lignes in ecrans:
        p = Planche(fond, LARGE_S, HAUT_S)
        p.titre(titre, 72, enc, y=460)
        if st:
            p.sticker(st, lignes, y=HAUT_S - 700)
        else:
            p.texte(lignes[0], 44, enc, 400, avant=60)
        p.signature(enc)
        f.append(p.ecrire(d / ("%s.png" % nom)))
    return f


GABARITS = {
    "carrousel-couleurs": carrousel_couleurs,
    "dilemme-enseigne": dilemme_enseigne,
    "carrousel-typographie": carrousel_typographie,
    "carrousel-enseigne": carrousel_enseigne,
    "quiz-idees-recues": quiz_idees_recues,
    "carrousel-droits": carrousel_droits,
    "plans-reel-cmjn": plans_reel_cmjn,
    "plans-reel-halloween": plans_reel_halloween,
    "stories": stories,
}


def main():
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--exemple", action="store_true",
                   help="produire le carrousel du 7 octobre")
    a.add_argument("--liste", action="store_true", help="les gabarits connus")
    a.add_argument("--tout", action="store_true", help="produire tout le cycle")
    args = a.parse_args()

    if args.liste:
        for k in GABARITS:
            print(" ", k)
        return
    if args.tout:
        total = 0
        for nom, fn in GABARITS.items():
            faits = fn()
            total += len(faits)
            print("%-26s %2d planches" % (nom, len(faits)))
        print("\n%d visuels produits dans %s" % (total, SORTIE))
        return
    if args.exemple:
        for f in carrousel_couleurs():
            im = Image.open(f)
            print("%-52s %sx%s" % (f, im.size[0], im.size[1]))
        return
    a.print_help()


if __name__ == "__main__":
    main()
