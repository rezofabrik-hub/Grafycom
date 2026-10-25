# -*- coding: utf-8 -*-
"""La signature d'e-mail, et la page depuis laquelle on la copie.

Pourquoi un générateur plutôt qu'un fichier écrit à la main
-----------------------------------------------------------
Une signature porte le téléphone, le site et le compte Instagram.
Ces trois valeurs existent déjà dans `gen.py` et dans la charte, et
une signature recopiée à la main dérive comme tout le reste : le jour
où le numéro change, personne ne pense à la signature. Ici elle est
construite à partir des mêmes constantes que le site.

Ce qu'un client de messagerie accepte, et ce qu'il refuse
----------------------------------------------------------
Rien de ce qui est vrai sur le site ne l'est dans un e-mail. Ce fichier
suit donc cinq règles, et chacune vient d'un client qui casse :

1. **Des tableaux, pas de flex ni de grid.** Outlook pour Windows rend
   l'HTML avec le moteur de Word, qui ignore la mise en page moderne.
2. **Des styles en ligne.** Gmail retire la balise <style> d'un message.
3. **Pas de police web.** Playfair et Inter ne s'installent pas chez le
   destinataire. On prend Georgia pour le serif, Arial pour le reste :
   présentes partout, et Georgia est le serif qui approche le mieux
   Playfair.
4. **Pas de dégradé CSS.** Le filet de la charte est donc fabriqué en
   huit cellules de tableau, une par arrêt du dégradé. C'est le même
   dégradé, en huit marches, et il s'affiche partout — y compris quand
   les images sont bloquées.
5. **Le texte se suffit sans les images.** Beaucoup de clients bloquent
   les images par défaut. Le logo est un agrément ; si rien ne
   s'affiche, la signature reste entière et lisible.

Ce qui n'y figure pas, et pourquoi
-----------------------------------
**Le nom de famille et l'adresse.** Règle du dossier, sans exception
hors mentions légales et CGV.

**L'adresse e-mail.** Elle est déjà dans le champ « De : » du message.
La répéter dans la signature prend une ligne pour ne rien apprendre.

Usage
-----
    python3 generateurs/p_signature.py
"""
from gen import page, TEL, TEL_URI, SITE

INSTA = "grafycom.graphiste"
LOGO = SITE + "/assets/img/signature-logo.png"

# Les huit arrêts du dégradé de la charte, dans l'ordre. Lus à la main
# ici plutôt que par charte.py : la signature part chez des gens, elle
# ne doit pas dépendre d'un import qui pourrait manquer un jour.
DEGRADE = ("#2f7fc4", "#35a9dd", "#3ec2b3", "#a86cd0",
           "#e33d82", "#f2585c", "#f5883c", "#f9c33f")

ENCRE, TAUPE, BRUN, CREME, SABLE = ("#2f2723", "#a2897c", "#6d5a50",
                                    "#f7f1ef", "#e4d5cc")
SERIF = "Georgia,'Times New Roman',serif"
SANS = "Arial,Helvetica,sans-serif"


def filet():
    """Le dégradé de la charte, en huit marches de tableau."""
    return "".join(
        '<td width="12.5%%" height="3" bgcolor="%s" '
        'style="font-size:0;line-height:0;height:3px">&nbsp;</td>' % c
        for c in DEGRADE)


def ligne(etiquette, contenu, couleur):
    """Une ligne de contact : son étiquette en petites capitales.

    Les pictogrammes du modèle d'origine sont des caractères que
    beaucoup de polices n'ont pas — le destinataire voit alors un
    carré vide. Une étiquette courte, dans une couleur de la charte,
    dit la même chose et s'affiche partout.
    """
    return """
      <tr>
        <td style="padding:0 0 5px 0;font:11px/16px %(sans)s;
            color:%(coul)s;letter-spacing:.09em;white-space:nowrap;
            vertical-align:top;padding-right:14px"
            width="62">%(etiq)s</td>
        <td style="padding:0 0 5px 0;font:13px/16px %(sans)s;
            color:%(encre)s;vertical-align:top">%(cont)s</td>
      </tr>""" % {"sans": SANS, "coul": couleur, "etiq": etiquette,
                  "encre": ENCRE, "cont": contenu}


def lien(url, texte, couleur=ENCRE):
    return ('<a href="%s" style="color:%s;text-decoration:none">%s</a>'
            % (url, couleur, texte))


SIGNATURE = """
<table role="presentation" cellpadding="0" cellspacing="0" border="0"
       style="border-collapse:collapse;background:%(creme)s;
       max-width:470px">
  <tr>
    <td style="padding:16px 20px 14px 18px">
      <table role="presentation" cellpadding="0" cellspacing="0"
             border="0" style="border-collapse:collapse">
        <tr>
          <td width="76" style="vertical-align:middle;padding-right:16px">
            <img src="%(logo)s" width="72" height="72" alt="Grafycom"
                 style="display:block;width:72px;height:72px;border:0">
          </td>
          <td style="vertical-align:middle">
            <div style="font:400 21px/25px %(serif)s;color:%(encre)s;
                 letter-spacing:.055em">Sandra</div>
            <div style="font:11px/17px %(sans)s;color:%(taupe)s;
                 letter-spacing:.11em;padding-top:4px">
              &#8226;&nbsp; GRAFYCOM &nbsp;&#8226;&nbsp; COMMUNICATION
              VISUELLE &nbsp;&#8226;
            </div>
            <div style="font:italic 12px/17px %(serif)s;color:%(brun)s;
                 padding-top:2px">L'image qui vous ressemble</div>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td style="padding:0 20px 0 18px">
      <table role="presentation" cellpadding="0" cellspacing="0"
             border="0" width="100%%"
             style="border-collapse:collapse;width:100%%">
        <tr>%(filet)s</tr>
      </table>
    </td>
  </tr>
  <tr>
    <td style="padding:12px 20px 16px 18px">
      <table role="presentation" cellpadding="0" cellspacing="0"
             border="0" style="border-collapse:collapse">%(lignes)s
      </table>
    </td>
  </tr>
</table>""" % {
    "creme": CREME, "logo": LOGO, "serif": SERIF, "sans": SANS,
    "encre": ENCRE, "taupe": TAUPE, "brun": BRUN, "filet": filet(),
    "lignes": "".join([
        ligne("T&Eacute;L", lien("tel:" + TEL_URI, TEL), "#2f7fc4"),
        ligne("WEB", lien(SITE + "/", "grafycom.fr"), "#a86cd0"),
        ligne("INSTA", lien("https://www.instagram.com/%s/" % INSTA,
                            "@" + INSTA), "#e33d82"),
        ligne("ZONE",
              '<span style="color:%s">Perpignan et alentours</span>'
              % BRUN, "#f5883c"),
    ])}

TEXTE = """Sandra — Grafycom
Communication visuelle · L'image qui vous ressemble

Tél     %s
Web     grafycom.fr
Insta   @%s
Zone    Perpignan et alentours""" % (TEL, INSTA)

BODY = """
<section class="heros">
  <div class="conteneur" style="position:relative;z-index:1">
    <span class="eyebrow">Outil interne</span>
    <h1>La signature<br><span class="texte-degrade">d'e-mail</span></h1>
    <div class="trait"></div>
    <p class="chapeau">Cette page n'est pas destin&eacute;e aux visiteurs du site :
    elle sert &agrave; copier la signature dans Gmail, une fois, et &agrave; la
    retrouver le jour o&ugrave; il faut la remettre.</p>
  </div>
</section>

<section>
  <div class="conteneur">
    <h2>&Agrave; copier</h2>
    <div class="trait"></div>
    <p class="chapeau">S&eacute;lectionnez tout le bloc ci-dessous, du logo &agrave;
    la derni&egrave;re ligne, et copiez-le avec <code>Ctrl+C</code>.</p>
    <div style="margin:28px 0;padding:22px;background:#fff;
         border:1px solid #e4d5cc;border-radius:10px;overflow-x:auto">
%(signature)s
    </div>
  </div>
</section>

<section>
  <div class="conteneur">
    <h2>Dans Gmail</h2>
    <div class="trait"></div>
    <ol class="chapeau" style="text-align:left;max-width:640px;
        margin-left:auto;margin-right:auto">
      <li>Roue dent&eacute;e en haut &agrave; droite, puis
          <strong>Voir tous les param&egrave;tres</strong>.</li>
      <li>Onglet <strong>G&eacute;n&eacute;ral</strong>, descendre jusqu'&agrave;
          <strong>Signature</strong>.</li>
      <li><strong>Cr&eacute;er</strong>, la nommer <code>Grafycom</code>.</li>
      <li>Cliquer dans le cadre et coller avec <code>Ctrl+V</code>.</li>
      <li>Dessous, choisir cette signature pour les
          <strong>nouveaux messages</strong> et pour les
          <strong>r&eacute;ponses</strong>.</li>
      <li>Tout en bas de la page&nbsp;:
          <strong>Enregistrer les modifications</strong>.</li>
    </ol>
    <p class="chapeau" style="margin-top:24px">Le r&eacute;glage par d&eacute;faut de
    Gmail ins&egrave;re la signature <em>sous</em> le texte cit&eacute; quand vous
    r&eacute;pondez. La case <strong>&laquo;&nbsp;Ins&eacute;rer la signature avant le
    texte cit&eacute;&nbsp;&raquo;</strong>, juste en dessous, corrige &ccedil;a&nbsp;:
    sans elle, votre signature se retrouve en bas d'un fil de douze
    messages.</p>
  </div>
</section>

<section>
  <div class="conteneur">
    <h2>La version texte</h2>
    <div class="trait"></div>
    <p class="chapeau">Pour un formulaire, un devis, ou un client dont la
    messagerie refuse l'HTML.</p>
    <pre style="max-width:560px;margin:24px auto;padding:20px;
         background:#f7f1ef;border-left:3px solid #a86cd0;
         border-radius:6px;font:13px/1.7 ui-monospace,monospace;
         white-space:pre-wrap;text-align:left">%(texte)s</pre>
  </div>
</section>

<section>
  <div class="conteneur">
    <h2>Ce qu'il faut savoir</h2>
    <div class="trait"></div>
    <div class="grille g3" style="margin-top:40px">
      <div class="carte carte-creme">
        <h3>Le logo peut ne pas s'afficher</h3>
        <p>Beaucoup de messageries bloquent les images tant que le
        destinataire ne les autorise pas. C'est voulu&nbsp;: la signature
        reste enti&egrave;re sans lui, le texte ne d&eacute;pend d'aucune image.</p>
      </div>
      <div class="carte carte-creme">
        <h3>Le d&eacute;grad&eacute; n'est pas une image</h3>
        <p>Le filet est fait de huit cellules de tableau, une par
        couleur de la charte. Un vrai d&eacute;grad&eacute; CSS dispara&icirc;trait sous
        Outlook&nbsp;; celui-ci s'affiche partout.</p>
      </div>
      <div class="carte carte-creme">
        <h3>Les polices ne sont pas celles du site</h3>
        <p>Playfair et Inter ne s'installent pas chez le destinataire.
        Georgia et Arial les remplacent&nbsp;: pr&eacute;sentes partout, et
        Georgia est le serif qui approche le mieux Playfair.</p>
      </div>
    </div>
  </div>
</section>
""" % {"signature": SIGNATURE, "texte": TEXTE}

page("signature.html", "Signature d'e-mail — Grafycom",
     "Page interne : la signature d'e-mail de Grafycom, à copier dans "
     "Gmail.",
     BODY, ogtitle="Signature d'e-mail — Grafycom",
     robots="noindex, nofollow")
