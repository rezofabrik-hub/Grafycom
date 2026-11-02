# -*- coding: utf-8 -*-
"""Page Actualités : les publications de Sandra, chargées dans le navigateur.

Sandra programme ses publications depuis l'Espace Pro de Rezo Fabrik.
Celles dont la case « Site internet » est cochée apparaissent ici toutes
seules, le jour venu, sans régénérer ni redéployer le site : la page ne
contient que le cadre, et assets/actualites.js va chercher les
publications dans la base (lecture publique, limitée par la base elle-même
aux publications parues et destinées au site).

Sans publication, sans réseau ou sans JavaScript, la page reste correcte :
elle affiche un message discret au lieu d'un cadre vide.
"""
from gen import page, appel, page_jsonld, CSP_ACTUALITES

DESC = ("Les nouvelles de l'atelier Grafycom à Perpignan : projets en "
        "cours, réalisations récentes et coulisses du studio.")

corps = """<section class="heros">
  <div class="conteneur">
    <p class="eyebrow">Actualités</p>
    <h1>Les nouvelles de l'atelier</h1>
    <p class="chapeau">Projets qui sortent, travaux en cours, coulisses du
    studio&nbsp;: ce qui se passe chez Grafycom, au fil des semaines.</p>
  </div>
</section>

<section>
  <div class="conteneur actus" id="actualites" aria-live="polite">
    <p class="actus-vide">Bientôt les nouveautés de l'atelier.</p>
  </div>
</section>
"""

corps += appel("Un projet en préparation&nbsp;?",
               "Un premier échange est gratuit, et franc — y compris "
               "quand la réponse est que vous n'avez besoin de rien.")

corps += '<script src="assets/actualites.js" defer></script>\n'

page("actualites.html",
     "Actualités de l'atelier | Grafycom, graphiste à Perpignan",
     DESC, corps, ogtitle="Les actualités de Grafycom",
     csp=CSP_ACTUALITES,
     jsonld=page_jsonld("Actualités de l'atelier", "actualites.html", DESC,
                        typ="CollectionPage"))
