// Page du back-office. Elle vit dans le code du Worker, pas dans dist/ :
// un fichier du site serait servi a tout le monde, garde ou pas.
export const PAGE_ADMIN = String.raw`<!doctype html>
<html lang="fr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Publications — Grafycom</title>
<link rel="icon" href="/assets/img/logo-grafycom-carre.jpg">
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<style>
:root{
 --bleu:#2f7fc4;--turquoise:#3ec2b3;--violet:#a86cd0;--magenta:#e33d82;
 --corail:#f2585c;--orange:#f5883c;--jaune:#f9c33f;
 --creme:#f7f1ef;--sable:#efe4dd;--sable-fonce:#e4d5cc;
 --taupe:#a2897c;--brun:#6d5a50;--encre:#2f2723;--blanc:#fff;
 --fond:var(--creme);--texte:var(--brun);--titre:var(--encre);
 --carte:var(--blanc);--filet:var(--sable-fonce);
 --degrade:linear-gradient(120deg,#2f7fc4 0%,#35a9dd 18%,#3ec2b3 33%,
   #a86cd0 52%,#e33d82 70%,#f2585c 84%,#f5883c 94%,#f9c33f 100%);
}
@media(prefers-color-scheme:dark){:root{
 --fond:#221c19;--texte:#d6c8c0;--titre:#f3ece8;--carte:#2c2420;
 --filet:#473b34;--taupe:#b39b8e;color-scheme:dark;}}
*{box-sizing:border-box}
body{margin:0;background:var(--fond);color:var(--texte);
 font-family:'Inter',system-ui,sans-serif;font-size:15px;line-height:1.6}
.filet{height:6px;background:var(--degrade)}
header{padding:22px 16px 0;max-width:1180px;margin:0 auto}
h1{font-family:'Playfair Display',Georgia,serif;color:var(--titre);
 font-size:clamp(24px,4vw,34px);margin:0 0 4px;font-weight:700}
.oeil{font-size:11.5px;letter-spacing:2.2px;text-transform:uppercase;
 color:var(--taupe);font-weight:600}
main{max-width:1180px;margin:0 auto;padding:18px 16px 80px}
.barre{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:18px 0 6px}
button{font:inherit;cursor:pointer;border-radius:999px;border:1px solid var(--filet);
 background:var(--carte);color:var(--texte);padding:7px 15px;font-size:13.5px}
button:hover{border-color:var(--taupe)}
button.on{background:var(--encre);color:#fff;border-color:var(--encre)}
@media(prefers-color-scheme:dark){button.on{background:var(--violet);border-color:var(--violet)}}
.compte{margin-left:auto;font-size:13px;color:var(--taupe);font-variant-numeric:tabular-nums}
.jour{margin:26px 0 8px;font-family:'Playfair Display',Georgia,serif;
 color:var(--titre);font-size:18px;font-weight:700}
.ligne{background:var(--carte);border:1px solid var(--filet);border-radius:14px;
 margin-bottom:10px;overflow:hidden}
.tete{display:grid;grid-template-columns:62px 1fr auto;gap:12px;align-items:center;
 padding:13px 16px;cursor:pointer}
.tete:hover{background:rgba(162,137,124,.07)}
.h{font-variant-numeric:tabular-nums;font-size:13px;color:var(--taupe);font-weight:600}
.t{min-width:0}
.t b{display:block;color:var(--titre);font-weight:600;font-size:14.5px;
 overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.t span{font-size:12.5px;color:var(--taupe)}
.p{font-size:11px;font-weight:600;letter-spacing:.4px;text-transform:uppercase;
 padding:4px 10px;border-radius:999px;white-space:nowrap}
.p-propose{background:var(--sable);color:var(--brun)}
.p-valide{background:#d9f2ec;color:#15655a}
.p-refuse{background:#fadcdc;color:#8d2626}
.p-publie{background:#dcebf8;color:#1d4e75}
@media(prefers-color-scheme:dark){
 .p-propose{background:#3a302a;color:#d6c8c0}.p-valide{background:#14433b;color:#8fe0d0}
 .p-refuse{background:#4a2020;color:#f3b3b3}.p-publie{background:#17384f;color:#a8d3f0}}
.corps{display:none;padding:0 16px 18px;border-top:1px solid var(--filet)}
.ligne.ouvert .corps{display:block}
label{display:block;font-size:11.5px;letter-spacing:1.1px;text-transform:uppercase;
 color:var(--taupe);font-weight:600;margin:14px 0 5px}
textarea,input[type=text]{width:100%;font:inherit;font-size:14px;color:var(--texte);
 background:var(--fond);border:1px solid var(--filet);border-radius:10px;padding:10px 12px}
textarea{resize:vertical;min-height:120px;line-height:1.6}
.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px;align-items:center}
.ok{background:var(--turquoise);border-color:var(--turquoise);color:#08342d;font-weight:600}
.non{background:var(--corail);border-color:var(--corail);color:#fff;font-weight:600}
.fait{background:var(--bleu);border-color:var(--bleu);color:#fff;font-weight:600}
.etat{font-size:12.5px;color:var(--taupe);margin-left:auto}
.vide{text-align:center;padding:60px 20px;color:var(--taupe)}
.avis{border-left:4px solid var(--bleu);background:var(--carte);border-radius:0 10px 10px 0;
 padding:12px 16px;font-size:13.5px;margin:16px 0}
</style></head><body>
<div class="filet"></div>
<header><span class="oeil">Grafycom · back-office</span><h1>Publications à relire</h1></header>
<main>
<div class="avis">Rien ne part sans ton clic. Pour Instagram, Facebook et la
fiche Google, le texte est à recopier dans Meta Business Suite — marque
ensuite « publié » pour garder le fil. Le blog, lui, sort tout seul à sa date
une fois validé.</div>
<div class="barre" id="barre"></div>
<div id="liste"><div class="vide">Chargement…</div></div>
</main>
<script>
const E = (s) => String(s==null?"":s).replace(/[&<>"']/g,
  c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const LIB = {propose:"à relire", valide:"validé", refuse:"refusé", publie:"publié"};
let TOUT = [], filtre = "tous";

function jourFr(d){
  const [a,m,j] = d.split("-");
  const mois = ["janvier","février","mars","avril","mai","juin","juillet",
    "août","septembre","octobre","novembre","décembre"][+m-1];
  return j.replace(/^0/,"") + " " + mois + " " + a;
}
async function charger(){
  const r = await fetch("/admin/api/publications");
  if(!r.ok){ document.getElementById("liste").innerHTML =
    '<div class="vide">Lecture impossible ('+r.status+')</div>'; return; }
  const d = await r.json();
  TOUT = d.publications; dessiner();
}
function dessiner(){
  const b = document.getElementById("barre");
  const n = (s)=>TOUT.filter(p=>p.statut===s).length;
  b.innerHTML = [["tous","Tout ("+TOUT.length+")"],["propose","À relire ("+n("propose")+")"],
    ["valide","Validé ("+n("valide")+")"],["publie","Publié ("+n("publie")+")"],
    ["refuse","Refusé ("+n("refuse")+")"]]
    .map(([k,l])=>'<button data-f="'+k+'" class="'+(filtre===k?"on":"")+'">'+l+"</button>").join("");
  b.querySelectorAll("button").forEach(x=>x.onclick=()=>{filtre=x.dataset.f;dessiner();});

  const vus = filtre==="tous" ? TOUT : TOUT.filter(p=>p.statut===filtre);
  const L = document.getElementById("liste");
  if(!vus.length){ L.innerHTML='<div class="vide">Rien ici.</div>'; return; }
  let html="", jour="";
  for(const p of vus){
    if(p.jour!==jour){ jour=p.jour; html+='<div class="jour">'+E(jourFr(jour))+"</div>"; }
    html += '<div class="ligne" data-id="'+E(p.id)+'">'
      + '<div class="tete"><div class="h">'+E(p.heure||"—")+"</div>"
      + '<div class="t"><b>'+E(p.titre)+"</b><span>"+E(p.canal)
      + (p.pilier?" · "+E(p.pilier):"")+"</span></div>"
      + '<div class="p p-'+E(p.statut)+'">'+LIB[p.statut]+"</div></div>"
      + '<div class="corps">'
      + "<label>Texte de la publication</label><textarea data-c=texte>"+E(p.texte)+"</textarea>"
      + "<label>Hashtags</label><input type=text data-c=hashtags value=\""+E(p.hashtags)+"\">"
      + "<label>Visuel</label><input type=text data-c=visuel value=\""+E(p.visuel)+"\">"
      + "<label>Note interne</label><input type=text data-c=note value=\""+E(p.note)+"\">"
      + '<div class="actions">'
      + "<button class=ok data-a=valide>Valider</button>"
      + "<button class=non data-a=refuse>Refuser</button>"
      + "<button class=fait data-a=publie>Marqué publié</button>"
      + "<button data-a=copier>Copier le texte</button>"
      + "<button data-a=enregistrer>Enregistrer</button>"
      + '<span class="etat"></span></div></div></div>';
  }
  L.innerHTML = html;
  L.querySelectorAll(".tete").forEach(t=>t.onclick=()=>t.parentElement.classList.toggle("ouvert"));
  L.querySelectorAll(".actions button").forEach(x=>x.onclick=(e)=>agir(e.target));
}
async function agir(bouton){
  const ligne = bouton.closest(".ligne");
  const etat = ligne.querySelector(".etat");
  const id = ligne.dataset.id, a = bouton.dataset.a;
  const champ = (c)=>ligne.querySelector('[data-c='+c+']').value;

  if(a==="copier"){
    const t = champ("texte") + (champ("hashtags")?"\n\n"+champ("hashtags"):"");
    try{ await navigator.clipboard.writeText(t); etat.textContent="copié"; }
    catch{ ligne.querySelector("[data-c=texte]").select(); etat.textContent="sélectionné, Ctrl+C"; }
    return;
  }
  const corps = {id, texte:champ("texte"), hashtags:champ("hashtags"),
                 visuel:champ("visuel"), note:champ("note")};
  if(a!=="enregistrer") corps.statut = a;
  etat.textContent = "…";
  const r = await fetch("/admin/api/publication",
    {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(corps)});
  if(!r.ok){ etat.textContent = "échec ("+r.status+")"; return; }
  const d = await r.json();
  const i = TOUT.findIndex(p=>p.id===id);
  if(i>=0) TOUT[i] = d.publication;
  const ouvert = ligne.classList.contains("ouvert");
  dessiner();
  if(ouvert){ const n = document.querySelector('.ligne[data-id="'+CSS.escape(id)+'"]');
              if(n){ n.classList.add("ouvert"); n.querySelector(".etat").textContent="enregistré"; } }
}
charger();
</script></body></html>`;
