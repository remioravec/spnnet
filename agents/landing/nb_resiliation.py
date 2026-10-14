#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module d'attention : calculateur de date limite de résiliation.

Justifié par le relevé SERP du 29/09/2026 sur « résilier un contrat de
nettoyage » : l'AI Overview part sur du B2C (CESU, aide à domicile, Shiva,
O2) et cleany.fr, 1er organique, titre son étape 1 « Calculez votre date
limite » sans donner d'outil pour la calculer. Personne dans le top 10 ne
pose la date à l'écran.

Complète navboost.py sans le modifier : le CSS et le JS sont autonomes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import navboost as nb

CSS = (
    "<style>"
    ".spn-art .nb-res{border-radius:12px;padding:16px 18px;margin:0}"
    ".spn-art .nb-res .nb-big{font-family:'Fraunces',Georgia,serif;font-size:1.55rem;"
    "font-weight:600;line-height:1.15;margin-bottom:6px}"
    ".spn-art .nb-res p{margin:4px 0;font-size:.93rem;line-height:1.5}"
    ".spn-art .nb-r-ok{background:#ecfdf5;border:1px solid #a7f3d0;color:#065f46}"
    ".spn-art .nb-r-soon{background:#fffbeb;border:1px solid #fde68a;color:#92400e}"
    ".spn-art .nb-r-late{background:#fff1ea;border:1px solid #fecaca;color:#9a3412}"
    "</style>"
)

JS = """<script>(function(){
var d=document.getElementById('crDate'),p=document.getElementById('crPre'),o=document.getElementById('crOut');
if(!d||!p||!o)return;
var M=['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'];
function fr(x){return x.getDate()+' '+M[x.getMonth()]+' '+x.getFullYear();}
function limite(anniv,mois){var l=new Date(anniv.getTime());l.setMonth(l.getMonth()-mois);l.setDate(l.getDate()-1);return l;}
function go(){
  var v=d.value; if(!v){o.innerHTML='';return;}
  var a=new Date(v+'T00:00:00'); if(isNaN(a.getTime())){o.innerHTML='';return;}
  var n=parseInt(p.value,10);
  var lim=limite(a,n);
  var now=new Date(); now.setHours(0,0,0,0);
  var j=Math.round((lim-now)/86400000), cls, msg;
  if(j>30){cls='nb-r-ok';msg='Il vous reste <b>'+j+' jours</b> pour envoyer le recommandé.';}
  else if(j>=0){cls='nb-r-soon';msg='Plus que <b>'+j+' jour'+(j>1?'s':'')+'</b>. Envoyez le recommandé cette semaine.';}
  else{
    var a2=new Date(a.getTime()); a2.setFullYear(a2.getFullYear()+1);
    var l2=limite(a2,n);
    cls='nb-r-late';
    msg='La date est passée : le contrat se reconduit jusqu’au <b>'+fr(a2)+'</b>. Prochaine fenêtre d’envoi : avant le <b>'+fr(l2)+'</b>.';
    lim=l2;
  }
  o.innerHTML='<div class="nb-res '+cls+'"><div class="nb-big">'+fr(lim)+'</div>'+
    '<p>Dernier jour pour envoyer votre lettre recommandée.</p><p>'+msg+'</p></div>';
}
d.addEventListener('input',go); p.addEventListener('change',go); go();
})();</script>"""

_EX = [
    ("1er janvier", "1 mois", "30 novembre"),
    ("1er janvier", "3 mois", "30 septembre"),
    ("1er avril", "3 mois", "31 décembre"),
    ("1er septembre", "3 mois", "31 mai"),
    ("1er septembre", "6 mois", "28 février"),
]


def calc_resiliation():
    rows = "".join(f"<tr><td>{a}</td><td>{p}</td><td><b>{d}</b></td></tr>" for a, p, d in _EX)
    return (
        '<div class="nb rv" id="calcResil">'
        f'<div class="nb-head"><span class="ic">{nb.IC_CALC}</span><div>'
        "<h3>Votre date limite d'envoi du recommandé</h3>"
        "<p>La date anniversaire de votre contrat, moins le préavis qu'il prévoit. "
        "Passé ce jour, le contrat repart pour un an.</p></div></div>"
        '<form class="nb-form" onsubmit="return false">'
        '<div class="nb-f"><label for="crDate">Date anniversaire du contrat</label>'
        '<input id="crDate" type="date" value="2027-01-01">'
        '<span class="hint">la date de prise d\'effet, pas celle de signature</span></div>'
        '<div class="nb-f"><label for="crPre">Préavis prévu au contrat</label>'
        '<select id="crPre"><option value="1">1 mois</option><option value="2">2 mois</option>'
        '<option value="3" selected>3 mois</option><option value="6">6 mois</option></select>'
        '<span class="hint">clause « durée » ou « résiliation »</span></div></form>'
        '<div class="nb-out" id="crOut" aria-live="polite">'
        '<p class="nb-nojs">Activez JavaScript pour le calcul instantané — '
        "les cas types restent lisibles juste en dessous.</p></div>"
        '<div class="nb-warn"><b>Le contrat prime toujours.</b> Ce calcul applique la règle la plus '
        "courante en propreté B2B : résiliation à la date anniversaire, préavis notifié par lettre "
        "recommandée. Relisez vos clauses « durée » et « résiliation » avant d'envoyer.</div>"
        '<div class="nb-grid"><table>'
        '<caption class="sr-only">Cas types de date limite d\'envoi</caption>'
        "<thead><tr><th>Date anniversaire</th><th>Préavis</th>"
        "<th>Dernier jour pour envoyer</th></tr></thead>"
        f"<tbody>{rows}</tbody></table></div>"
        "</div>"
    )
