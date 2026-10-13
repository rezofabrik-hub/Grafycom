# Provenance des images du blog

| Fichier | Origine | Licence | Attribution |
|---|---|---|---|
| `enseigne.png` | `reseaux/illustrations.py` | — | aucune |
| `cmjn.png` | `reseaux/illustrations.py` | — | aucune |
| `droits.png` | `reseaux/illustrations.py` | — | aucune |
| `vitrine.png` | `reseaux/illustrations.py` | — | aucune |
| `retroplanning.png` | `reseaux/illustrations.py` | — | aucune |
| `trottoir.png` | `reseaux/illustrations.py` | — | aucune |
| `bilan.png` | `reseaux/illustrations.py` | — | aucune |

**Les sept articles ont leur illustration, et aucune ne dépend d'un tiers.**

## Pourquoi ce fichier

Une image dont on ne sait plus d'où elle vient est une image qu'on finit
par retirer en urgence. La ligne éditoriale l'exige d'ailleurs :
« jamais une image dont les droits ne sont pas clairs ».

## Deux photos retirées le 13 octobre 2026

`enseigne-photo.webp` et `pantone-photo.webp` venaient de Magnific
(ex-Freepik), via le compte d'un tiers. La question posée ici depuis
l'origine — « confirmer la formule du compte, et poser l'attribution dans
le pied de page si elle est due » — n'a jamais été tranchée. Elle n'a plus
lieu d'être : les deux articles concernés utilisent désormais le schéma
dessiné qui dormait dans ce dossier depuis le début, `enseigne.png` et
`cmjn.png`.

C'est mieux que du pareil au même. Un schéma qui porte l'argument de
l'article fait gagner du temps au lecteur ; une photo d'ambiance de banque
d'images n'apprend rien, se reconnaît, et pose une question de licence
chaque fois qu'on la regarde.

## En ajouter une

Écrire une fonction `illu_<sujet>()` dans `reseaux/illustrations.py`,
l'inscrire dans `ILLUSTRATIONS`, relancer le script, puis renseigner le
champ `illustration:` de l'article. Les couleurs viennent toutes de
`generateurs/charte.py` : une couleur hors charte arrête le programme.
