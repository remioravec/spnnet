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
    for n,t,c in SECTIONS:
        h += f'<h2 id="s{n}"><span class="sec-num">{n}</span>{t}</h2>\n{c}\n'
    h += '<h2 id="s10"><span class="sec-num">10</span>La grille de comparaison</h2>'
    h += ('<p>Un choix se défend d\'autant mieux qu\'il repose sur une notation commune. '
          'Remplissez la grille ci-dessous pour vos candidats : elle reprend les neuf points du guide, '
          'se calcule en direct et s\'imprime pour votre comité.</p>')
    h += grille()
    h += ('<h2 id="devis">Demander un devis à SPN NET</h2>'
          '<p>SPN NET entretient des bureaux, commerces, copropriétés et établissements de santé à Paris '
          'et en Île-de-France depuis 30 ans. Équipes fidélisées, interlocuteur dédié, certification '
          'ISO 45001 et médaille d\'argent EcoVadis 2025. Nous nous déplaçons pour chiffrer vos locaux '
          'et vous transmettons une proposition détaillée sous 24 heures ouvrées : '
          '<a href="https://spn-net.fr/contact/">demander un devis</a>.</p>')
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
    hero = ('<div class="art-hero"><div class="wrap hero-solo">'
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
