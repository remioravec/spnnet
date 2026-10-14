#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hub du silo bureaux : /choisir-entreprise-nettoyage/

Slug tranche sur GSC (21/06 -> 18/09/2026) : "entreprise de nettoyage" pese
plusieurs milliers d'impressions (logistique 544, theatre 517, paris 8 429,
musee 414, IDF 263), "prestataire" 151 au total. Le mot "entreprise" gagne.

10 sections, 15 liens in-body poses dans le premier tiers de leur section,
ancres en exact match contigu qui tournent. Partis pris du CLAUDE.md respectes :
CTA du hero vers la grille (pas le formulaire), bloc de reponse sans lien,
devis uniquement en bas de page, grille sans echange d'e-mail.

Usage : python3 agents/landing/make_hub.py [--publish]
"""
from __future__ import annotations
import os, sys, json, pathlib, datetime, requests

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from make_article import ART_CSS, ART_JS, _faq_block, _faq_schema, strip_accents  # noqa: E402
import navboost as nb  # noqa: E402

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
PAGES = "https://spn-net.fr/wp-json/wp/v2/pages"
SLUG  = "choisir-entreprise-nettoyage"
URL   = f"https://spn-net.fr/{SLUG}/"

TITLE = "Comment choisir son entreprise de nettoyage : le guide en 10 points"
SEO_T = "Choisir son entreprise de nettoyage : le guide en 10 points | SPN NET"
DESC  = ("Choisir une entreprise de nettoyage sans se tromper : les 10 points à vérifier, "
         "du prix au m² à la conformité sociale, avec une grille de comparaison à remplir.")

# ---------------------------------------------------------------- CSS ----
HUB_CSS = """
.spn-art .hub-answer{background:var(--cream);border:1px solid var(--line);border-left:4px solid var(--orange-deep);border-radius:0 var(--r) var(--r) 0;padding:26px 28px;margin:28px 0}
.spn-art .hub-answer .tag{display:inline-block;font-size:.68rem;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--orange-deep);margin-bottom:10px}
.spn-art .hub-answer ol{margin:0;padding-left:20px}
.spn-art .hub-answer li{font-size:1.02rem;line-height:1.55;margin-bottom:5px;color:var(--ink)}
.spn-art .hub-answer li b{color:var(--orange-deep)}
.spn-art .hero-cta{display:inline-flex;align-items:center;gap:9px;background:var(--orange-deep);color:#fff;font-weight:700;font-size:.98rem;text-decoration:none;padding:13px 28px;border-radius:999px;margin-top:22px}
.spn-art .hero-cta:hover{background:var(--orange)}
.spn-art .sec-num{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:10px;background:var(--orange-soft);color:var(--orange-deep);font-family:'Fraunces',serif;font-weight:700;font-size:1.05rem;margin-right:11px;vertical-align:middle}
/* grille de comparaison */
.spn-art .cmp{width:100%;border-collapse:collapse;font-size:.9rem;min-width:620px}
.spn-art .cmp th,.spn-art .cmp td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}
.spn-art .cmp thead th{background:var(--cream);font-size:.76rem;text-transform:uppercase;letter-spacing:.05em;color:var(--grey);font-weight:800}
.spn-art .cmp thead th input{width:100%;border:1px solid var(--line);border-radius:8px;padding:7px 9px;font-family:inherit;font-size:.86rem;font-weight:700;color:var(--ink);background:#fff;text-transform:none;letter-spacing:0}
.spn-art .cmp td:first-child{font-weight:600;color:var(--ink);width:36%}
.spn-art .cmp td:first-child small{display:block;font-weight:400;color:var(--grey);font-size:.8rem;margin-top:3px}
.spn-art .cmp select{width:100%;border:1px solid var(--line);border-radius:8px;padding:7px 9px;font-family:inherit;font-size:.86rem;background:var(--cream);color:var(--ink);font-weight:600}
.spn-art .cmp tfoot td{background:var(--cream);font-weight:800}
.spn-art .cmp .sc{font-family:'Fraunces',serif;font-size:1.3rem;color:var(--orange-deep)}
.spn-art .cmp-wrap{overflow-x:auto;margin-top:18px}
.spn-art .cmp-act{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px;align-items:center}
.spn-art .cmp-act button{font-family:inherit;font-size:.88rem;font-weight:700;border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:999px;padding:10px 20px;cursor:pointer}
.spn-art .cmp-act button:hover{border-color:var(--orange-deep);color:var(--orange-deep)}
.spn-art .cmp-act .hint{font-size:.8rem;color:var(--grey)}

/* ---------- hero illustre ---------- */
.spn-art .art-hero .hero-in{grid-template-columns:1fr 360px}
.spn-art .hero-img{border-radius:20px;overflow:hidden;border:1px solid var(--line);box-shadow:var(--shadow);aspect-ratio:4/3;background:var(--cream)}
.spn-art .hero-img img{width:100%;height:100%;object-fit:cover;display:block}
/* ---------- infographies ---------- */
.spn-art .vz{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:24px 26px;margin:26px 0;box-shadow:var(--shadow-sm)}
.spn-art .vz .vz-t{font-size:.72rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--grey);margin-bottom:16px}
.spn-art .vz-2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.spn-art .vz-col{border:1px solid var(--line);border-radius:14px;padding:18px 18px 14px}
.spn-art .vz-col.win{border-color:rgba(216,67,31,.35);background:var(--orange-soft)}
.spn-art .vz-col h4{font-family:'Fraunces',serif;font-weight:600;font-size:1.04rem;margin:0 0 10px}
.spn-art .vz-col ul{list-style:none;margin:0;padding:0}
.spn-art .vz-col li{font-size:.88rem;color:var(--ink-2);padding:5px 0 5px 20px;position:relative}
.spn-art .vz-col li:before{content:"—";position:absolute;left:0;color:var(--grey)}
.spn-art .vz-col.win li:before{content:"✓";color:var(--orange-deep);font-weight:800}
/* barre empilee */
.spn-art .vz-bar{display:flex;height:42px;border-radius:10px;overflow:hidden;margin-bottom:10px}
.spn-art .vz-bar span{display:flex;align-items:center;justify-content:center;color:#fff;font-size:.8rem;font-weight:800}
.spn-art .vz-leg{display:flex;flex-wrap:wrap;gap:14px;font-size:.82rem;color:var(--ink-2)}
.spn-art .vz-leg i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px}
/* timeline */
.spn-art .vz-tl{display:flex;gap:0;flex-wrap:wrap}
.spn-art .vz-step{flex:1;min-width:130px;position:relative;padding:0 12px}
.spn-art .vz-step:before{content:"";position:absolute;top:15px;left:0;right:0;height:2px;background:var(--line)}
.spn-art .vz-step:first-child:before{left:50%}.spn-art .vz-step:last-child:before{right:50%}
.spn-art .vz-dot{position:relative;width:32px;height:32px;border-radius:50%;background:var(--orange-soft);color:var(--orange-deep);border:2px solid #fff;box-shadow:0 0 0 2px var(--orange-soft);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.82rem;margin:0 auto 12px}
.spn-art .vz-step b{display:block;text-align:center;font-size:.9rem;margin-bottom:3px}
.spn-art .vz-step span{display:block;text-align:center;font-size:.8rem;color:var(--grey);line-height:1.45}
/* niveaux empiles */
.spn-art .vz-lv{display:grid;gap:9px}
.spn-art .vz-lv div{border-radius:11px;padding:13px 16px;font-size:.9rem;display:flex;gap:12px;align-items:baseline}
.spn-art .vz-lv b{font-family:'Fraunces',serif;font-size:.96rem;min-width:92px;flex:0 0 auto}
.spn-art .vz-lv .l1{background:#16181D;color:#fff}.spn-art .vz-lv .l1 b{color:#fff}
.spn-art .vz-lv .l2{background:var(--orange-soft);color:var(--ink-2)}.spn-art .vz-lv .l2 b{color:var(--orange-deep)}
.spn-art .vz-lv .l3{background:var(--cream);color:var(--ink-2)}.spn-art .vz-lv .l3 b{color:var(--grey)}
/* zones d'acces */
.spn-art .vz-zn{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.spn-art .vz-zn div{border-radius:12px;padding:16px;text-align:center;border:1px solid var(--line)}
.spn-art .vz-zn .z-ok{background:#eaf6ec;border-color:#b7dcc0}
.spn-art .vz-zn .z-md{background:var(--orange-soft);border-color:rgba(216,67,31,.3)}
.spn-art .vz-zn .z-no{background:var(--cream)}
.spn-art .vz-zn b{display:block;font-size:.94rem;margin-bottom:5px}
.spn-art .vz-zn span{font-size:.8rem;color:var(--grey);line-height:1.45}
/* galerie 4 photos */
.spn-art .vz-g4{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.spn-art .vz-g4 figure{margin:0;border-radius:12px;overflow:hidden;border:1px solid var(--line);background:var(--cream)}
.spn-art .vz-g4 img{width:100%;height:100%;object-fit:cover;display:block;aspect-ratio:4/3}
.spn-art .vz-g4 figcaption{font-size:.78rem;font-weight:700;color:var(--ink-2);padding:8px 10px;text-align:center}
/* photo pleine largeur */
.spn-art .vz-photo{margin:0;border-radius:16px;overflow:hidden;border:1px solid var(--line)}
.spn-art .vz-photo img{width:100%;display:block;aspect-ratio:21/9;object-fit:cover}
.spn-art .vz-photo figcaption{font-size:.82rem;color:var(--grey);padding:10px 14px;background:#fff}
/* CTA intermediaire */
.spn-art .midcta{display:flex;align-items:center;gap:18px;flex-wrap:wrap;background:linear-gradient(120deg,var(--orange-soft),#fff);border:1px solid rgba(216,67,31,.28);border-radius:var(--r);padding:20px 24px;margin:28px 0}
.spn-art .midcta p{margin:0;flex:1;min-width:220px;font-size:.96rem;font-weight:600;color:var(--ink)}
.spn-art .midcta a{display:inline-flex;align-items:center;gap:8px;background:var(--orange-deep);color:#fff;font-weight:700;font-size:.92rem;text-decoration:none;padding:12px 24px;border-radius:999px;white-space:nowrap}
.spn-art .midcta a:hover{background:var(--orange)}
/* CTA final */
.spn-art .endcta{background:#16181D;color:#fff;border-radius:var(--r);padding:34px 34px 30px;margin:32px 0 0}
.spn-art .endcta h3{font-family:'Fraunces',serif;font-weight:600;font-size:1.5rem;color:#fff;margin:0 0 10px}
.spn-art .endcta p{color:rgba(255,255,255,.82);font-size:.98rem;margin:0 0 20px;max-width:56ch}
.spn-art .endcta .acts{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.spn-art .endcta .b1{background:var(--orange);color:#fff;font-weight:800;text-decoration:none;padding:14px 30px;border-radius:999px}
.spn-art .endcta .b2{color:#fff;font-weight:700;text-decoration:none;padding:14px 22px;border-radius:999px;border:1px solid rgba(255,255,255,.3)}
.spn-art .endcta .badges{margin-top:18px;font-size:.8rem;color:rgba(255,255,255,.6)}
@media(max-width:820px){.spn-art .vz-2,.spn-art .vz-zn{grid-template-columns:1fr}.spn-art .vz-g4{grid-template-columns:1fr 1fr}}
@media print{.spn-art .art-side,.spn-art .art-hero,.spn-art .cmp-act{display:none!important}}
"""

HUB_JS = """<script>(function(){
var r=document.querySelector('.spn-art');if(!r)return;
var t=r.querySelector('#cmpTable');if(!t)return;
var V={oui:2,partiel:1,non:0,'':0};
function calc(){
  var cols=[1,2,3];
  cols.forEach(function(c){
    var tot=0,max=0;
    t.querySelectorAll('tbody tr').forEach(function(tr){
      var s=tr.children[c]&&tr.children[c].querySelector('select');
      if(!s)return; max+=2; tot+=V[s.value]||0;
    });
    var cell=t.querySelector('tfoot tr').children[c];
    if(cell) cell.innerHTML='<span class="sc">'+tot+'</span> / '+max;
  });
}
t.addEventListener('change',calc);
var rz=r.querySelector('#cmpReset');
if(rz) rz.addEventListener('click',function(){
  t.querySelectorAll('select').forEach(function(s){s.value='';});
  t.querySelectorAll('thead input').forEach(function(i){i.value='';});
  calc();
});
var pr=r.querySelector('#cmpPrint');
if(pr) pr.addEventListener('click',function(){window.print();});
calc();
})();</script>"""

# ------------------------------------------------------------ SECTIONS ----
# (numero, titre, html du corps) — le lien vit dans le PREMIER TIERS de la section
SECTIONS = [
(1,"Généraliste ou spécialiste de vos locaux",
 """<p>La première question n'est pas le prix, c'est le périmètre : une entreprise qui entretient des plateaux de bureaux ne travaille pas comme celle qui nettoie des cuisines ou des blocs opératoires. Les protocoles, les produits et la formation des agents changent complètement. Si vos locaux sont des bureaux, cherchez une société dont le <a href="https://spn-net.fr/tertiaire/">nettoyage de bureaux à Paris</a> constitue le cœur de métier, pas une ligne parmi trente.</p>
<p>Le signe qui ne trompe pas : demandez combien de sites comparables au vôtre l'entreprise entretient aujourd'hui, en surface et en fréquence. Une réponse chiffrée et immédiate indique une spécialité réelle. Une réponse vague indique un catalogue.</p>
<p>Attention toutefois à l'excès inverse : un spécialiste trop étroit ne saura pas traiter vos à-côtés — vitrerie, sols techniques, parties communes. L'équilibre utile est une entreprise centrée sur votre typologie de locaux, capable d'absorber les prestations périphériques sans sous-traiter.</p>"""),

(2,"Lire un devis, et le prix au mètre carré",
 """<p>Un devis de propreté ne se juge pas sur son total. Il se juge sur le <b>temps d'intervention prévu</b>, exprimé en heures par passage : c'est cette ligne qui détermine la qualité que vous obtiendrez. Un prestataire moins cher qui prévoit deux heures là où il en faut trois vous livrera des sanitaires mal faits, et la différence se verra au troisième mois. Nous avons détaillé les fourchettes réelles dans notre guide du <a href="https://spn-net.fr/prix-nettoyage-bureaux-paris/">prix du nettoyage de bureaux à Paris</a>, avec un calculateur au m² et au poste.</p>
<p>Les cinq lignes à exiger sur tout devis : le temps prévu par passage, le périmètre exact espace par espace, la fréquence par espace (les sanitaires ne suivent pas le rythme des bureaux), ce qui est facturé en supplément (vitrerie, décapage, remise en état, consommables) et la clause de révision de prix.</p>
<p>Un devis clair sur ces cinq points vaut mieux qu'un devis moins cher de 8 % dont vous découvrirez le périmètre réel en cours de contrat.</p>"""),

(3,"Vérifier qu'elle est en règle",
 """<p>Ce point n'est pas une formalité : c'est une obligation légale qui vous engage. Dès qu'un contrat de nettoyage atteint 5 000 € HT, le donneur d'ordre doit obtenir l'attestation de vigilance URSSAF de son prestataire, puis la renouveler tous les six mois. À défaut, il peut être tenu solidairement responsable des cotisations impayées. La procédure complète et les six pièces à réunir figurent dans notre guide pour <a href="https://spn-net.fr/travail-dissimule-entreprise-nettoyage/">vérifier que votre entreprise de nettoyage est en règle</a>.</p>
<p>Le réflexe qui protège : ne pas se contenter de recevoir l'attestation, mais en vérifier l'authenticité en ligne sur urssaf.fr grâce au code de sécurité qu'elle porte. Une attestation reçue et non vérifiée ne vous exonère pas.</p>
<p>Demandez également par écrit si tout ou partie de la prestation est sous-traitée, et à qui. Votre obligation de vigilance s'étend à chaque sous-traitant direct.</p>"""),

(4,"Les certifications qui comptent vraiment",
 """<p>Les logos s'alignent vite sur les plaquettes. Encore faut-il savoir ce que chacun certifie : un diplôme qualifie un agent, une certification audite une organisation, un label porte sur un produit. Confondre les trois conduit à croire qu'une entreprise est « certifiée écologique » parce qu'elle emploie un produit écolabellisé. Le détail de chaque repère est dans notre guide des <a href="https://spn-net.fr/certifications-entreprise-nettoyage/">certifications d'une entreprise de nettoyage</a>.</p>
<p>Les questions qui tranchent : quelles certifications, sur quel périmètre exact, délivrées par quel organisme, et à quelle date remonte le dernier audit ? Une certification a une date de validité et fait l'objet d'audits de suivi.</p>
<p>Gardez en tête qu'une certification prouve le respect d'un référentiel à un instant donné. Elle ne dit rien, à elle seule, de la qualité que vous constaterez sur le terrain.</p>
<div class="twrap rv"><table class="art-table">
<thead><tr><th>Repère</th><th>Ce qu'il certifie</th><th>Portée</th></tr></thead>
<tbody>
<tr><td>CAP, CQP, TFP</td><td>La formation d'un agent</td><td>La personne</td></tr>
<tr><td>ISO 9001 / 14001 / 45001</td><td>Qualité, environnement, santé et sécurité au travail</td><td>L'entreprise</td></tr>
<tr><td>Qualipropre, Certipropre</td><td>Bonnes pratiques du secteur de la propreté</td><td>L'entreprise</td></tr>
<tr><td>Écolabel Européen</td><td>Critères environnementaux d'un produit</td><td>Le produit</td></tr>
</tbody></table></div>"""),

(5,"Qui entre réellement dans vos locaux",
 """<p>Le nettoyage de bureaux se fait le plus souvent hors présence de vos équipes, tôt le matin ou en soirée. Des personnes accèdent donc à vos postes de travail, vos documents et votre matériel sans témoin. Le risque ne se gère pas par la méfiance mais par le contrat : clause de confidentialité, agents nommés et stables, traçabilité des accès. Nous avons détaillé le cadre et la charte de discrétion dans notre guide sur la <a href="https://spn-net.fr/nettoyage-bureaux-confidentialite-securite/">confidentialité du nettoyage de bureaux</a>.</p>
<p>Quatre exigences à poser noir sur blanc : une clause de confidentialité engageant l'entreprise et chaque agent, des agents identifiés et fidélisés plutôt que des remplaçants au hasard, une traçabilité des clés et des badges, et une formation explicite à la discrétion.</p>
<div class="twrap rv"><table class="art-table">
<thead><tr><th>À exiger</th><th>Pourquoi c'est déterminant</th></tr></thead>
<tbody>
<tr><td>Clause de confidentialité</td><td>Engage l'entreprise et chaque agent individuellement.</td></tr>
<tr><td>Agents identifiés et stables</td><td>Les mêmes personnes, connues, formées à vos locaux.</td></tr>
<tr><td>Traçabilité des accès</td><td>Savoir qui intervient, quand, avec quelles clés.</td></tr>
<tr><td>Zones sensibles délimitées</td><td>Salle serveur, archives, direction : accès restreint ou exclu.</td></tr>
</tbody></table></div>"""),

(6,"Le suivi qualité, et le cap du troisième mois",
 """<p>C'est le point que presque personne ne vérifie à la signature, et celui qui décide de tout. Les premières semaines sont toujours impeccables : le prestataire met ses meilleures ressources sur une prise de marché. Le vrai sujet est ce qui se passe ensuite, quand l'attention retombe. Nous avons documenté les quatre causes réelles du relâchement et la grille de contrôle mensuelle dans notre analyse de <a href="https://spn-net.fr/qualite-nettoyage-baisse-apres-3-mois/">la qualité du nettoyage qui baisse après trois mois</a>.</p>
<p>Demandez donc, avant de signer : qui vient contrôler le travail sur site, à quelle fréquence, et sous quelle forme le constat vous est-il transmis ? Une réponse orale « on passe régulièrement » ne vaut rien. Un compte rendu de visite daté, si.</p>
<p>Le second garde-fou est la stabilité des équipes. Un turnover élevé annule tout : chaque nouvel agent redécouvre vos locaux, vos accès et vos exigences.</p>"""),

(7,"Proximité et capacité de remplacement",
 """<p>Une entreprise proche de vos locaux réagit plus vite sur les imprévus — un agent absent, une intervention d'urgence, un dégât des eaux un vendredi soir. Vérifiez qu'elle couvre réellement votre secteur avec des équipes basées à proximité, et pas depuis l'autre bout de la région : nos pages locales, du <a href="https://spn-net.fr/paris-8/">nettoyage de bureaux dans le 8e</a> à l'ensemble des <a href="https://spn-net.fr/92-hauts-de-seine/">Hauts-de-Seine</a>, décrivent cette couverture secteur par secteur.</p>
<p>La question décisive porte sur le remplacement : que se passe-t-il si votre agent habituel est absent ? Un prestataire sérieux a une réponse contractuelle — un remplaçant formé, prévenu, qui connaît le protocole du site. Un prestataire fragile vous annoncera l'absence le matin même.</p>"""),

(8,"Ce qui n'est pas dans le contrat d'entretien",
 """<p>Beaucoup de prestations courantes ne figurent pas dans un contrat de nettoyage standard et se découvrent en cours de route. Mieux vaut les identifier avant de comparer les devis, sans quoi vous comparez des périmètres différents. Selon vos locaux, pensez au <a href="https://spn-net.fr/ascenseurs-escalators/">nettoyage d'ascenseurs et escalators</a>, au <a href="https://spn-net.fr/portage/">portage</a> de charges, à la <a href="https://spn-net.fr/peinture/">peinture</a> de rafraîchissement ou au <a href="https://spn-net.fr/marquage-au-sol/">marquage au sol</a> des parkings.</p>
<p>Le bon réflexe est de demander à votre prestataire ce qu'il sait traiter en direct, et ce qu'il confierait à un tiers. Chaque intervenant supplémentaire est un interlocuteur de plus à piloter.</p>
<div class="twrap rv"><table class="art-table">
<thead><tr><th>Prestation</th><th>Rythme courant</th><th>Toujours en supplément ?</th></tr></thead>
<tbody>
<tr><td>Vitrerie intérieure et cloisons</td><td>Mensuel à trimestriel</td><td>Oui, chiffrée au m² de vitrage</td></tr>
<tr><td>Décapage et cristallisation des sols</td><td>Annuel</td><td>Oui</td></tr>
<tr><td>Ascenseurs et escalators</td><td>Selon fréquentation</td><td>Souvent</td></tr>
<tr><td>Marquage au sol des parkings</td><td>Ponctuel</td><td>Oui</td></tr>
<tr><td>Remise en état, fin de chantier</td><td>Ponctuel</td><td>Devis dédié</td></tr>
</tbody></table></div>"""),

(9,"Vous avez déjà un prestataire",
 """<p>Changer fait peur pour deux raisons : la paperasse et le sort des agents en place. Les deux sont encadrées, et moins lourdes qu'on ne le croit. Si votre contrat actuel s'essouffle, la marche à suivre complète figure sur notre page dédiée pour <a href="https://spn-net.fr/changer-de-prestataire-nettoyage/">changer de prestataire de nettoyage</a> — résiliation, transition, reprise des équipes.</p>
<p>Le point juridique à connaître est le transfert du personnel, organisé par l'<a href="https://spn-net.fr/annexe-7-changer-entreprise-nettoyage/">Annexe 7 de la convention collective de la propreté</a> : lorsqu'un marché change de prestataire, les agents remplissant les critères sont repris par l'entreprise entrante. C'est une protection, et pour vous une garantie de continuité.</p>
<p>Le seul élément vraiment contraignant est le préavis inscrit à votre contrat en cours — généralement d'un à trois mois. C'est lui qui fixe la date de bascule, pas la disponibilité du nouveau prestataire.</p>"""),
]

FAQ = [
 ("Comment choisir une entreprise de nettoyage pour des bureaux ?",
  "Vérifiez d'abord qu'elle est spécialisée dans votre typologie de locaux, puis le temps d'intervention prévu au devis, sa conformité sociale (attestation de vigilance URSSAF), la stabilité de ses agents et la réalité de son contrôle qualité. Le prix ne se compare qu'à périmètre et temps d'intervention identiques."),
 ("Quels documents demander à une entreprise de nettoyage ?",
  "L'attestation de vigilance URSSAF de moins de 6 mois, un extrait Kbis de moins de 3 mois, l'attestation d'assurance responsabilité civile professionnelle, la convention collective appliquée, la liste nominative des salariés étrangers le cas échéant, et la déclaration écrite de la chaîne de sous-traitance."),
 ("Quel est le prix d'un contrat de nettoyage de bureaux à Paris ?",
  "Les taux horaires relevés à Paris se situent entre 20 et 35 € HT de l'heure, soit environ 1,50 à 3,90 € HT par m² et par mois selon la fréquence. Un minimum de facturation d'environ 1 h 30 par semaine s'applique chez la plupart des prestataires."),
 ("Faut-il choisir un généraliste ou un spécialiste ?",
  "Une entreprise centrée sur votre typologie de locaux, mais capable d'absorber les prestations périphériques (vitrerie, sols, parties communes) sans sous-traiter. Un généraliste dilue ses protocoles, un spécialiste trop étroit multiplie les intervenants."),
 ("Comment savoir si la qualité va tenir dans la durée ?",
  "Posez trois questions avant de signer : qui contrôle le travail sur site, à quelle fréquence, et sous quelle forme le constat vous est transmis. Vérifiez aussi le taux de rotation des agents : c'est lui qui explique l'essentiel des baisses de qualité constatées passé le troisième mois."),
 ("Que se passe-t-il pour les agents si je change de prestataire ?",
  "L'Annexe 7 de la convention collective de la propreté organise leur transfert vers l'entreprise entrante dès lors qu'ils remplissent les critères d'ancienneté et de temps de travail sur le site. Pour vous, c'est une garantie de continuité : les mêmes personnes continuent d'entretenir vos locaux."),
 ("Suis-je responsable si mon prestataire emploie des travailleurs non déclarés ?",
  "Oui, si vous n'avez pas accompli votre obligation de vigilance. Dès 5 000 € HT de contrat, vous devez obtenir l'attestation de vigilance URSSAF à la signature puis tous les six mois. Sans cette traçabilité, vous pouvez être tenu solidairement responsable des cotisations dues."),
]

CRITERES = [
 ("Spécialiste de vos locaux","Entretient-elle des sites comparables, chiffres à l'appui ?"),
 ("Temps d'intervention au devis","Le devis indique-t-il les heures prévues par passage ?"),
 ("Attestation de vigilance URSSAF","Fournie, datée de moins de 6 mois, et vérifiée en ligne ?"),
 ("Certifications vérifiées","Périmètre, organisme et date du dernier audit connus ?"),
 ("Confidentialité contractualisée","Clause écrite, agents nommés, accès tracés ?"),
 ("Contrôle qualité tracé","Visites de site datées et compte rendu transmis ?"),
 ("Stabilité des agents","Même équipe annoncée, remplacement prévu au contrat ?"),
 ("Proximité et réactivité","Équipes basées dans votre secteur ?"),
 ("Prestations périphériques","Vitrerie, sols, ascenseurs traités en direct ?"),
]

IMG = "https://spn-net.fr/wp-content/uploads/2026/02/"
IMG1 = "https://spn-net.fr/wp-content/uploads/2026/01/"

def cta(txt, label="Ouvrir la grille de comparaison"):
    return (f'<div class="midcta rv"><p>{txt}</p>'
            f'<a href="#grille">{label} &#8594;</a></div>')

VISUELS = {
1: ('<div class="vz rv"><div class="vz-t">Ce qui change concrètement</div><div class="vz-2">'
    '<div class="vz-col"><h4>Le généraliste</h4><ul>'
    '<li>Un protocole unique adapté après coup</li><li>Agents polyvalents, tournés sur plusieurs typologies</li>'
    '<li>Réactif sur le devis, plus lent sur le terrain</li><li>Les à-côtés partent en sous-traitance</li></ul></div>'
    '<div class="vz-col win"><h4>Le spécialiste de vos locaux</h4><ul>'
    '<li>Un protocole écrit pour votre typologie</li><li>Agents formés à vos surfaces et contraintes</li>'
    '<li>Références chiffrées sur des sites comparables</li><li>Prestations périphériques traitées en direct</li></ul></div>'
    '</div></div>'),
2: ('<div class="vz rv"><div class="vz-t">Où part réellement votre budget</div>'
    '<div class="vz-bar">'
    '<span style="width:64%;background:#D8431F">Main-d\'œuvre 64 %</span>'
    '<span style="width:19%;background:#ED5D37">Encadrement 19 %</span>'
    '<span style="width:17%;background:#c9bdb2">Produits &amp; matériel 17 %</span></div>'
    '<div class="vz-leg"><span><i style="background:#D8431F"></i>Temps passé sur site</span>'
    '<span><i style="background:#ED5D37"></i>Contrôle qualité, remplacements</span>'
    '<span><i style="background:#c9bdb2"></i>Consommables, machines</span></div>'
    '<p style="font-size:.82rem;color:var(--grey);margin:14px 0 0">La main-d\'œuvre représentant près des deux tiers '
    'du prix, un devis nettement moins cher signifie presque toujours moins d\'heures sur site — rarement une meilleure organisation.</p></div>'),
3: ('<div class="vz rv"><div class="vz-t">Votre obligation de vigilance, dans le temps</div><div class="vz-tl">'
    '<div class="vz-step"><div class="vz-dot">1</div><b>À la signature</b><span>Dès 5 000 € HT de contrat : attestation URSSAF exigée</span></div>'
    '<div class="vz-step"><div class="vz-dot">2</div><b>+ 6 mois</b><span>Nouvelle attestation, vérifiée en ligne</span></div>'
    '<div class="vz-step"><div class="vz-dot">3</div><b>+ 12 mois</b><span>Et ainsi de suite jusqu\'au terme</span></div>'
    '<div class="vz-step"><div class="vz-dot">&#10003;</div><b>Archivage</b><span>C\'est la trace datée qui vous exonère</span></div>'
    '</div></div>'),
4: ('<div class="vz rv"><div class="vz-t">Trois niveaux qu\'on confond tout le temps</div><div class="vz-lv">'
    '<div class="l1"><b>L\'entreprise</b><span>ISO 9001, 14001, 45001, Qualipropre, Certipropre — une organisation auditée</span></div>'
    '<div class="l2"><b>La personne</b><span>CAP, CQP, TFP — la formation d\'un agent, pas de la société</span></div>'
    '<div class="l3"><b>Le produit</b><span>Écolabel Européen — une gamme, jamais l\'entreprise qui l\'emploie</span></div>'
    '</div></div>'),
5: ('<div class="vz rv"><div class="vz-t">Découper vos locaux en trois zones</div><div class="vz-zn">'
    '<div class="z-ok"><b>Accès libre</b><span>Bureaux ouverts, circulations, sanitaires, espaces de pause</span></div>'
    '<div class="z-md"><b>Accès encadré</b><span>Direction, salles de réunion, bureaux fermés — agents nommés</span></div>'
    '<div class="z-no"><b>Accès exclu</b><span>Salle serveur, archives, coffre — hors périmètre ou sous escorte</span></div>'
    '</div></div>'),
6: ('<div class="vz rv"><div class="vz-t">La qualité perçue, mois après mois</div>'
    '<svg viewBox="0 0 460 170" width="100%" height="170" role="img" aria-label="Courbe : la qualité d\'un prestataire moyen baisse après le 3e mois, celle d\'un contrat suivi reste stable">'
    '<line x1="38" y1="140" x2="450" y2="140" stroke="#E9E4DD"/><line x1="38" y1="16" x2="38" y2="140" stroke="#E9E4DD"/>'
    '<path d="M44,44 L130,44 L216,52 L302,92 L388,116 L446,126" fill="none" stroke="#9aa0a6" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="5 6"/>'
    '<path d="M44,48 L130,44 L216,42 L302,40 L388,39 L446,38" fill="none" stroke="#D8431F" stroke-width="3" stroke-linecap="round"/>'
    '<g font-size="10" fill="#9aa0a6" font-family="monospace"><text x="38" y="158">Mois 1</text><text x="196" y="158">Mois 3</text><text x="398" y="158">Mois 6</text></g></svg>'
    '<div class="vz-leg" style="margin-top:8px"><span><i style="background:#9aa0a6"></i>Sans contrôle qualité</span>'
    '<span><i style="background:#D8431F"></i>Avec visites de site datées</span></div></div>'),
7: (f'<figure class="vz-photo rv"><img src="{IMG}cleanzonejpg-0018.jpg" alt="Équipe SPN NET en intervention sur un site tertiaire à Paris" loading="lazy" decoding="async" width="1909" height="724">'
    '<figcaption>Des équipes basées en Île-de-France : c\'est la proximité qui rend le remplacement possible le jour même.</figcaption></figure>'),
8: (f'<div class="vz rv"><div class="vz-t">Les quatre prestations qu\'on oublie de chiffrer</div><div class="vz-g4">'
    f'<figure><img src="{IMG}Ascenseur-3.jpg" alt="Nettoyage d\'ascenseur" loading="lazy" decoding="async" width="1500" height="1000"><figcaption>Ascenseurs</figcaption></figure>'
    f'<figure><img src="{IMG}portage-1.jpg" alt="Portage de charges" loading="lazy" decoding="async" width="1500" height="1000"><figcaption>Portage</figcaption></figure>'
    f'<figure><img src="{IMG}peinture-2.jpg" alt="Peinture de rafraîchissement" loading="lazy" decoding="async" width="1500" height="1000"><figcaption>Peinture</figcaption></figure>'
    f'<figure><img src="{IMG}marquage-1.jpg" alt="Marquage au sol de parking" loading="lazy" decoding="async" width="1500" height="1000"><figcaption>Marquage au sol</figcaption></figure>'
    '</div></div>'),
9: ('<div class="vz rv"><div class="vz-t">Un changement de prestataire, étape par étape</div><div class="vz-tl">'
    '<div class="vz-step"><div class="vz-dot">1</div><b>Préavis</b><span>1 à 3 mois selon votre contrat : c\'est lui qui fixe la date</span></div>'
    '<div class="vz-step"><div class="vz-dot">2</div><b>Visite</b><span>Le nouveau prestataire chiffre sur vos locaux réels</span></div>'
    '<div class="vz-step"><div class="vz-dot">3</div><b>Annexe 7</b><span>Les agents éligibles sont repris par l\'entrant</span></div>'
    '<div class="vz-step"><div class="vz-dot">&#10003;</div><b>Bascule</b><span>Aucune journée sans entretien</span></div>'
    '</div></div>'),
}


def grille():
    head = ('<thead><tr><th>Critere</th>'
            + "".join(f'<th><input type="text" placeholder="Prestataire {c}" aria-label="Nom du prestataire {c}"></th>'
                      for c in "ABC") + '</tr></thead>')
    opts = ('<option value="">—</option><option value="oui">Oui (2)</option>'
            '<option value="partiel">Partiel (1)</option><option value="non">Non (0)</option>')
    rows = ""
    for i,(t,d) in enumerate(CRITERES):
        cells = "".join(f'<td><select aria-label="{t} — prestataire {c}">{opts}</select></td>' for c in "ABC")
        rows += f'<tr><td>{t}<small>{d}</small></td>{cells}</tr>'
    foot = '<tfoot><tr><td>Score</td><td>—</td><td>—</td><td>—</td></tr></tfoot>'
    return (
      '<div class="nb rv" id="grille">'
      f'<div class="nb-head"><span class="ic">{nb.IC_CHECK}</span><div>'
      '<h3>Votre grille de comparaison</h3>'
      '<p>Notez jusqu\'à trois entreprises sur les neuf points du guide. Le score se calcule tout seul. '
      'Rien à saisir d\'autre : ni e-mail, ni formulaire.</p></div></div>'
      f'<div class="cmp-wrap"><table class="cmp" id="cmpTable">{head}<tbody>{rows}</tbody>{foot}</table></div>'
      '<div class="cmp-act"><button type="button" id="cmpPrint">Imprimer la grille</button>'
      '<button type="button" id="cmpReset">Effacer</button>'
      '<span class="hint">Un écart de 4 points ou plus est rarement rattrapable par le prix.</span></div>'
      '</div>')


def body():
    h = ('<div class="hub-answer rv"><span class="tag">La reponse en 10 points</span><ol>'
         '<li>Choisir une entreprise <b>spécialisée dans votre typologie de locaux</b>.</li>'
         '<li>Comparer le <b>temps d\'intervention prévu</b>, pas le total du devis.</li>'
         '<li>Exiger l\'<b>attestation de vigilance URSSAF</b> et la vérifier en ligne.</li>'
         '<li>Distinguer diplôme d\'agent, certification d\'entreprise et label produit.</li>'
         '<li>Contractualiser la <b>confidentialité</b> et la traçabilité des accès.</li>'
         '<li>Vérifier <b>qui contrôle la qualité</b> sur site, et à quelle fréquence.</li>'
         '<li>Privilégier des <b>équipes stables</b> et un remplacement prévu au contrat.</li>'
         '<li>Identifier les <b>prestations hors contrat</b> avant de comparer les prix.</li>'
         '<li>Connaître l\'<b>Annexe 7</b> si vous changez de prestataire.</li>'
         '<li>Noter chaque candidat sur une <b>grille commune</b> avant de décider.</li>'
         '</ol></div>')
    h += '<div class="toc"><b>Au sommaire</b><ol>'
    for n,t,_ in SECTIONS:
        h += f'<li><a href="#s{n}">{t}</a></li>'
    h += '<li><a href="#grille">La grille de comparaison</a></li></ol></div>'
    CTA_APRES = {
        3: "Vous avez de quoi vérifier la conformité d'un candidat. Notez-le tout de suite.",
        6: "Trois points passés en revue : prix, conformité, suivi. Reportez-les sur la grille.",
        9: "Vous avez les neuf critères. Il ne reste qu'à les confronter, candidat par candidat.",
    }
    for n,t,c in SECTIONS:
        h += f'<h2 id="s{n}"><span class="sec-num">{n}</span>{t}</h2>\n{c}\n'
        if n in VISUELS: h += VISUELS[n] + "\n"
        if n in CTA_APRES: h += cta(CTA_APRES[n]) + "\n"
    h += '<h2 id="s10"><span class="sec-num">10</span>La grille de comparaison</h2>'
    h += ('<p>Un choix se défend d\'autant mieux qu\'il repose sur une notation commune. '
          'Remplissez la grille ci-dessous pour vos candidats : elle reprend les neuf points du guide, '
          'se calcule en direct et s\'imprime pour votre comité.</p>')
    h += grille()
    h += ('<h2 id="devis">Demander un devis à SPN NET</h2>'
          '<div class="endcta rv"><h3>Mettez-nous sur votre grille</h3>'
          '<p>SPN NET entretient des bureaux, commerces, copropriétés et établissements de santé à Paris '
          'et en Île-de-France depuis 30 ans. Équipes fidélisées, interlocuteur dédié, contrôle qualité '
          'tracé. Nous nous déplaçons pour chiffrer vos locaux réels et vous transmettons une proposition '
          'détaillée sous 24 heures ouvrées.</p>'
          '<div class="acts"><a class="b1" href="https://spn-net.fr/contact/">demander un devis</a>'
          '<a class="b2" href="tel:+33149462240">01 49 46 22 40</a></div>'
          '<div class="badges">ISO 45001 &#183; Médaille d\'argent EcoVadis 2025 &#183; 4,8/5 sur 48 avis Google</div>'
          '</div>')
    return h


def schema():
    art = {"@context":"https://schema.org","@type":"Article","headline":TITLE,"description":DESC,
           "datePublished":"2026-09-21","dateModified":"2026-09-21",
           "author":{"@type":"Organization","name":"SPN NET"},
           "publisher":{"@type":"Organization","name":"SPN NET"},
           "mainEntityOfPage":URL}
    bc = ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
          '{"@type":"ListItem","position":1,"name":"Accueil","item":"https://spn-net.fr/"},'
          '{"@type":"ListItem","position":2,"name":"Nettoyage de bureaux","item":"https://spn-net.fr/tertiaire/"},'
          f'{{"@type":"ListItem","position":3,"name":"{strip_accents("Choisir son entreprise de nettoyage")}"}}]}}')
    return (_faq_schema(FAQ)
            + '<script type="application/ld+json">' + json.dumps(art, ensure_ascii=False) + '</script>'
            + '<script type="application/ld+json">' + bc + '</script>')


def build():
    hero = ('<div class="art-hero"><div class="wrap hero-in"><div>'
            '<nav class="crumbs"><a href="https://spn-net.fr/">Accueil</a> &#8250; '
            '<a href="https://spn-net.fr/tertiaire/">Nettoyage de bureaux</a> &#8250; '
            '<span>Choisir son entreprise</span></nav>'
            '<span class="eyebrow">Guide d\'achat</span>'
            f'<h1>{TITLE}</h1>'
            '<p class="chapo">Dix points à vérifier avant de signer, du temps d\'intervention au devis '
            'jusqu\'à la conformité sociale — et une grille pour noter vos candidats.</p>'
            '<div class="art-meta"><span>&#128197; 21 septembre 2026</span>'
            '<span>&#9201; 12 min de lecture</span>'
            '<span class="rate"><span class="s">&#9733;</span> <b>4,8/5</b> &#183; 48 avis</span></div>'
            '<a class="hero-cta" href="#grille">Ouvrir la grille de comparaison &#8594;</a>'
            '</div>'
            f'<figure class="hero-img rv"><img src="{IMG1}tertiaire-1.jpg" '
            'alt="Entretien de bureaux par SPN NET à Paris" width="1500" height="1000" '
            'decoding="async"></figure>'
            '</div></div>')
    main = '<article class="art-main">' + body() + _faq_block(FAQ) + '</article>'
    side = ('<aside class="art-side"><div class="side-toc"><b>Au sommaire</b><ol>'
            + "".join(f'<li><a href="#s{n}">{t}</a></li>' for n,t,_ in SECTIONS)
            + '<li><a href="#grille">La grille de comparaison</a></li></ol></div></aside>')
    css = ART_CSS.replace("</style>", nb.NB_CSS + HUB_CSS + "</style>")
    return (css + '<div class="spn-art">' + hero
            + '<div class="art-body"><div class="wrap art-grid">' + main + side + '</div></div>'
            + schema() + ART_JS + nb.NB_JS + HUB_JS + '</div>')


def publish(html, status="draft"):
    ex = requests.get(PAGES, params={"slug":SLUG,"status":"publish,draft,future","_fields":"id"},
                      auth=AUTH, timeout=60).json()
    payload = {"title":"Comment choisir son entreprise de nettoyage","slug":SLUG,"status":status,
               "content":"<!-- wp:html -->\n"+html+"\n<!-- /wp:html -->",
               "template":"elementor_header_footer","excerpt":DESC,
               "meta":{"_elementor_edit_mode":"",
                       "slim_seo":{"title":SEO_T,"description":DESC,"noindex":status!="publish"}}}
    url = f"{PAGES}/{ex[0]['id']}" if ex else PAGES
    for _ in range(3):
        try:
            r = requests.post(url, auth=AUTH, timeout=120, json=payload); r.raise_for_status()
            return r.json()
        except Exception as e:
            err = e
    raise err


if __name__ == "__main__":
    html = build()
    (HERE / f"hub-{SLUG}.html").write_text(html)
    print(f"  HTML genere : {len(html):,} caracteres".replace(",", " "))
    st = "publish" if "--publish" in sys.argv else "draft"
    j = publish(html, st)
    print(f"  [{j.get('status')}] id={j.get('id')}")
    print(f"  apercu : https://spn-net.fr/?page_id={j.get('id')}&preview=true")
    print(f"  edition : https://spn-net.fr/wp-admin/post.php?post={j.get('id')}&action=edit")
