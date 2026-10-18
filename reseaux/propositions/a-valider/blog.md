# Blog — les articles à valider

Les textes complets sont dans `reseaux/blog/`, un fichier par article.
Ce document est l'index : il dit ce qui existe, à quelle date, et ce qu'il
reste à faire.

## Comment un article paraît

Il y a **deux verrous indépendants**, et c'est voulu.

1. L'en-tête doit porter **`statut: validé`**, le mot en toutes lettres.
   « rédigé », « à relire » ou « prêt » ne suffisent pas : ils décrivent
   l'état du texte, pas ton accord.
2. **La date de l'en-tête doit être arrivée.** Un article du 4 décembre ne
   sort pas le 13, même validé.

Tu peux donc **tout valider d'un coup** sans que tout sorte le même jour.
Chaque article paraîtra à sa date, tout seul.

## Les articles

| Date | Titre | Mots | Statut |
|---|---|---|---|
| vendredi 30 octobre | Enseigne de commerce : comment obtenir l'autorisation préalabl | 801 | ✅ validé |
| vendredi 6 novembre | Pourquoi vos couleurs imprimées ne ressemblent jamais à votre  | 647 | ✅ validé |
| jeudi 12 novembre | Habiller sa vitrine : dépoli, microperforé ou lettres découpée | 904 | ⚠️ à relire |
| vendredi 13 novembre | Qui possède votre logo ? | 687 | ✅ validé |
| vendredi 20 novembre | Cartes de vœux et emballages de fête : le rétroplanning à teni | 897 | ⚠️ à relire |
| vendredi 27 novembre | Vitrine de fin d'année : ce qui se lit vraiment depuis le trot | 854 | ⚠️ à relire |
| vendredi 4 décembre | Faut-il refaire son logo pour la nouvelle année ? Trois questi | 792 | ⚠️ à relire |

**4 articles sur 7 attendent ta validation.** Pour en
valider un : ouvrir son fichier dans `reseaux/blog/`, remplacer la ligne
`statut:` par `statut: validé`, et le pousser. Le reste est automatique.

## Ce qui manque

Aucun article ne déclare d'**illustration** — le champ est facultatif et
l'article s'affiche sans, mais une image d'en-tête vaut mieux. Elles se
fabriquent avec `reseaux/illustrations.py`, qui n'a pas encore de schéma
pour ces sujets.
