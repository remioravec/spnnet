#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Modules d'attention (NavBoost) pour les articles SPN NET.

Doctrine (skill operationnel-contenu, étape 3 bis) : deux leviers seulement —
gagner le clic dans la SERP, et terminer la session (last longest click).
Le module se choisit dans le relevé SERP, jamais par goût.

Six règles de construction respectées ici :
  1. aucune dépendance externe (vanilla JS, zéro lib) ;
  2. le module fonctionne SANS JavaScript (la grille de référence complète est
     affichée en dur sous chaque calculateur, les checklists sont de vraies
     <input type=checkbox>) ;
  3. aucun contenu qui compte n'est injecté au clic ;
  4. accessible : <button>, <label for>, aria-*, navigable au clavier ;
  5. aucun décalage de mise en page (les zones de résultat ont une hauteur
     réservée) ;
  6. données réelles et sourcées — fourchettes de marché relevées le 28/08/2026,
     jamais des valeurs d'exemple, et jamais présentées comme les tarifs SPN NET.
"""
from __future__ import annotations

# ---------------------------------------------------------------- CSS ----
NB_CSS = """
/* ===== Modules d'attention (NavBoost) ===== */
.spn-art .nb{background:#fff;border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow-sm);padding:26px 26px 22px;margin:30px 0}
.spn-art .nb-head{display:flex;align-items:flex-start;gap:12px;margin-bottom:18px}
.spn-art .nb-head .ic{flex:0 0 40px;height:40px;display:inline-flex;align-items:center;justify-content:center;background:var(--orange-soft);color:var(--orange-deep);border-radius:11px}
.spn-art .nb-head .ic svg{width:22px;height:22px}
.spn-art .nb-head h3{font-family:'Fraunces',serif;font-weight:600;font-size:1.24rem;margin:0;line-height:1.2}
.spn-art .nb-head p{margin:4px 0 0;font-size:.88rem;color:var(--grey)}
/* --- formulaire --- */
.spn-art .nb-form{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;align-items:end}
.spn-art .nb-f{display:flex;flex-direction:column;gap:6px}
.spn-art .nb-f label{font-size:.78rem;font-weight:700;color:var(--ink-2);letter-spacing:.01em}
.spn-art .nb-f input,.spn-art .nb-f select{font-family:inherit;font-size:.95rem;font-weight:600;color:var(--ink);padding:11px 13px;border:1px solid var(--line);border-radius:11px;background:var(--cream);width:100%}
.spn-art .nb-f input:focus,.spn-art .nb-f select:focus{outline:2px solid var(--orange);outline-offset:1px;background:#fff}
.spn-art .nb-f .hint{font-size:.72rem;color:var(--grey)}
/* --- résultat --- */
.spn-art .nb-out{margin-top:20px;background:linear-gradient(180deg,var(--orange-soft),#fff);border:1px solid rgba(216,67,31,.25);border-radius:14px;padding:20px 22px;min-height:112px}
.spn-art .nb-out .big{font-family:'Fraunces',serif;font-weight:600;font-size:clamp(1.7rem,4vw,2.3rem);color:var(--orange-deep);line-height:1.05}
.spn-art .nb-out .sub{font-size:.86rem;color:var(--ink-2);font-weight:600;margin-top:4px}
.spn-art .nb-splits{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.spn-art .nb-splits div{background:#fff;border:1px solid var(--line);border-radius:10px;padding:9px 13px;font-size:.84rem;color:var(--ink-2);font-weight:600}
.spn-art .nb-splits div b{color:var(--orange-deep);font-weight:800}
.spn-art .nb-nojs{font-size:.85rem;color:var(--ink-2)}
.spn-art.js .nb-nojs{display:none}
.spn-art .sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.spn-art .nb-src{font-size:.75rem;color:var(--grey);margin-top:14px;line-height:1.5}
.spn-art .nb-warn{margin-top:12px;background:var(--cream);border-left:3px solid var(--orange);border-radius:0 10px 10px 0;padding:11px 14px;font-size:.82rem;color:var(--ink-2)}
/* --- grille de référence (fallback sans JS + preuve) --- */
.spn-art .nb-grid{margin-top:20px;overflow-x:auto}
.spn-art .nb-grid table{width:100%;border-collapse:collapse;font-size:.88rem;min-width:460px}
.spn-art .nb-grid th,.spn-art .nb-grid td{padding:11px 13px;text-align:left;border-bottom:1px solid var(--line)}
.spn-art .nb-grid thead th{background:var(--cream);font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:var(--grey);font-weight:800;white-space:nowrap}
.spn-art .nb-grid tbody tr:hover{background:var(--cream)}
.spn-art .nb-grid td:first-child{font-weight:700}
.spn-art .nb-grid td{white-space:nowrap}
.spn-art .nb-grid .hi{background:var(--orange-soft)!important}
/* --- checklist --- */
.spn-art .nb-check{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.spn-art .nb-check li{background:var(--cream);border:1px solid var(--line);border-radius:12px;transition:background .18s,border-color .18s}
.spn-art .nb-check li:has(input:checked){background:#eaf6ec;border-color:#b7dcc0}
.spn-art .nb-check label{display:flex;gap:13px;align-items:flex-start;padding:14px 16px;cursor:pointer}
.spn-art .nb-check input{margin:2px 0 0;width:19px;height:19px;flex:0 0 19px;accent-color:#2e7d32;cursor:pointer}
.spn-art .nb-check label>span>b{display:block;font-size:.96rem;margin-bottom:2px;color:var(--ink)}
.spn-art .nb-check label>span>span b{color:var(--ink-2)}
.spn-art .nb-check span{display:block;font-size:.85rem;color:var(--grey);line-height:1.5}
.spn-art .nb-check .law{display:inline-block;margin-top:5px;font-size:.72rem;font-weight:700;color:var(--orange-deep);background:#fff;border:1px solid rgba(216,67,31,.25);border-radius:999px;padding:2px 9px}
.spn-art .nb-score{margin-top:16px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.spn-art .nb-bar{flex:1;min-width:180px;height:9px;background:var(--line);border-radius:999px;overflow:hidden}
.spn-art .nb-bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--orange),#2e7d32);border-radius:999px;transition:width .4s cubic-bezier(.65,0,.2,1)}
.spn-art .nb-score .txt{font-size:.88rem;font-weight:700;color:var(--ink-2)}
/* --- tableau triable --- */
.spn-art .nb-sort thead th{cursor:pointer;user-select:none;position:relative}
.spn-art .nb-sort thead th[data-s]:after{content:"↕";opacity:.35;margin-left:6px;font-size:.9em}
.spn-art .nb-sort thead th.asc:after{content:"↑";opacity:1;color:var(--orange-deep)}
.spn-art .nb-sort thead th.desc:after{content:"↓";opacity:1;color:var(--orange-deep)}
/* --- réponse encadrée (anti AI Overview) --- */
.spn-art .nb-answer{background:linear-gradient(135deg,var(--orange-soft),#fff);border:1px solid rgba(216,67,31,.3);border-left:4px solid var(--orange-deep);border-radius:0 var(--r) var(--r) 0;padding:22px 24px;margin:24px 0}
.spn-art .nb-answer .tag{display:inline-block;font-size:.68rem;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--orange-deep);margin-bottom:8px}
.spn-art .nb-answer p{margin:0;font-size:1.06rem;line-height:1.6;color:var(--ink)}
.spn-art .nb-answer p strong{color:var(--orange-deep)}
.spn-art .nb-answer .date{display:block;margin-top:10px;font-size:.76rem;color:var(--grey)}
@media(max-width:720px){
  .spn-art .nb{padding:20px 18px 18px}
  .spn-art .nb-form{grid-template-columns:1fr 1fr}
}
@media(max-width:480px){.spn-art .nb-form{grid-template-columns:1fr}}
"""

# ---------------------------------------------------------------- JS ----
# Un seul bloc, vanilla, sans dépendance. Chaque module est autonome : s'il
# n'est pas présent dans la page, la fonction sort immédiatement.
NB_JS = """<script>(function(){
var r=document.querySelector('.spn-art');if(!r)return;
function eur(n){return n.toLocaleString('fr-FR',{maximumFractionDigits:0})+' €';}
function eur2(n){return n.toLocaleString('fr-FR',{minimumFractionDigits:2,maximumFractionDigits:2})+' €';}

/* ---- 1. Calculateur bureaux : surface x frequence -> fourchette ---- */
(function(){
  var box=r.querySelector('#calcBureaux');if(!box)return;
  var S=box.querySelector('#cbSurf'),F=box.querySelector('#cbFreq'),P=box.querySelector('#cbPostes'),O=box.querySelector('#cbOut');
  /* €/m²/mois observés sur le marche parisien (bas, haut) par passages/semaine */
  var T={1:[1.00,1.80],2:[1.60,2.90],3:[2.20,3.90],5:[3.50,6.50]};
  var PLANCHER=130; /* minimum de facturation constate (1h30/sem au tarif bas) */
  function calc(){
    var s=Math.max(10,Math.min(3000,parseInt(S.value,10)||0));
    var f=F.value,t=T[f]||T[3];
    var lo=Math.max(PLANCHER,Math.round(s*t[0]/5)*5), hi=Math.max(PLANCHER+40,Math.round(s*t[1]/5)*5);
    var p=parseInt(P.value,10)||Math.max(1,Math.round(s/10));
    var m2lo=lo/s,m2hi=hi/s, plo=lo/p, phi=hi/p;
    O.innerHTML='<div class="big">'+eur(lo)+' &ndash; '+eur(hi)+' <span style="font-size:.42em;font-weight:700">HT / mois</span></div>'+
      '<div class="sub">'+s+' m&sup2; &middot; '+f+' passage'+(f>1?'s':'')+' par semaine &middot; '+p+' poste'+(p>1?'s':'')+' de travail</div>'+
      '<div class="nb-splits">'+
      '<div>Au m&sup2; : <b>'+eur2(m2lo)+' &ndash; '+eur2(m2hi)+'</b> /m&sup2;/mois</div>'+
      '<div>Au poste : <b>'+eur(plo)+' &ndash; '+eur(phi)+'</b> /poste/mois</div>'+
      '<div>Par passage : <b>'+eur(lo/(f*4.33))+' &ndash; '+eur(hi/(f*4.33))+'</b></div>'+
      '</div>';
    var rows=box.querySelectorAll('.nb-grid tbody tr');
    for(var i=0;i<rows.length;i++){rows[i].classList.toggle('hi',rows[i].getAttribute('data-f')===String(f));}
  }
  [S,F,P].forEach(function(el){if(el){el.addEventListener('input',calc);el.addEventListener('change',calc);}});
  calc();
})();

/* ---- 2. Calculateur copropriete : lots x etages x frequence ---- */
(function(){
  var box=r.querySelector('#calcCopro');if(!box)return;
  var L=box.querySelector('#ccLots'),E=box.querySelector('#ccEtages'),F=box.querySelector('#ccFreq'),O=box.querySelector('#ccOut');
  function calc(){
    var lots=Math.max(2,Math.min(400,parseInt(L.value,10)||0));
    var et=Math.max(1,Math.min(20,parseInt(E.value,10)||1));
    var f=parseFloat(F.value)||1;
    /* duree d'un passage : base hall/local poubelles + cage d'escalier par etage */
    var h=0.5+et*0.22+lots*0.012;              /* heures par passage */
    var lo=h*f*4.33*22, hi=h*f*4.33*34;        /* 22 a 34 € HT/h releves */
    lo=Math.max(140,Math.round(lo/10)*10); hi=Math.max(200,Math.round(hi/10)*10);
    O.innerHTML='<div class="big">'+eur(lo)+' &ndash; '+eur(hi)+' <span style="font-size:.42em;font-weight:700">HT / mois</span></div>'+
      '<div class="sub">'+lots+' lots &middot; '+et+' &eacute;tage'+(et>1?'s':'')+' &middot; '+f+' passage'+(f>1?'s':'')+' par semaine</div>'+
      '<div class="nb-splits">'+
      '<div>Par lot : <b>'+eur2(lo/lots)+' &ndash; '+eur2(hi/lots)+'</b> /lot/mois</div>'+
      '<div>Par passage : <b>'+eur(lo/(f*4.33))+' &ndash; '+eur(hi/(f*4.33))+'</b></div>'+
      '<div>Dur&eacute;e estim&eacute;e : <b>'+h.toFixed(1).replace('.',',')+' h</b> /passage</div>'+
      '</div>';
  }
  [L,E,F].forEach(function(el){if(el){el.addEventListener('input',calc);el.addEventListener('change',calc);}});
  calc();
})();

/* ---- 3. Checklists cochables + score ---- */
r.querySelectorAll('[data-checklist]').forEach(function(box){
  var items=box.querySelectorAll('input[type=checkbox]');
  var bar=box.querySelector('.nb-bar i'),txt=box.querySelector('.nb-score .txt');
  if(!items.length||!bar)return;
  function upd(){
    var n=0;items.forEach(function(i){if(i.checked)n++;});
    var pct=Math.round(n/items.length*100);
    bar.style.width=pct+'%';
    if(txt){
      txt.textContent=n+' / '+items.length+' v\\u00e9rifi\\u00e9'+(n>1?'s':'')+
        (n===items.length?' \\u2014 dossier complet \\u2713':(n===0?'':' \\u2014 '+pct+' %'));
    }
  }
  items.forEach(function(i){i.addEventListener('change',upd);});
  upd();
});

/* ---- 4. Tableaux triables ---- */
r.querySelectorAll('table.nb-sort').forEach(function(tb){
  var ths=tb.querySelectorAll('thead th[data-s]');
  ths.forEach(function(th,idx){
    th.setAttribute('tabindex','0');th.setAttribute('role','button');
    function sort(){
      var col=Array.prototype.indexOf.call(th.parentNode.children,th);
      var num=th.getAttribute('data-s')==='num';
      var dir=th.classList.contains('asc')?-1:1;
      ths.forEach(function(o){o.classList.remove('asc','desc');});
      th.classList.add(dir===1?'asc':'desc');
      var tb2=tb.querySelector('tbody');
      var rows=Array.prototype.slice.call(tb2.querySelectorAll('tr'));
      rows.sort(function(a,b){
        var x=a.children[col].getAttribute('data-v')||a.children[col].textContent;
        var y=b.children[col].getAttribute('data-v')||b.children[col].textContent;
        if(num){return (parseFloat(String(x).replace(',','.'))-parseFloat(String(y).replace(',','.')))*dir;}
        return String(x).localeCompare(String(y),'fr')*dir;
      });
      rows.forEach(function(rw){tb2.appendChild(rw);});
    }
    th.addEventListener('click',sort);
    th.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();sort();}});
  });
});
})();</script>"""


# ------------------------------------------------------------ builders ----
def _ic(path):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            'stroke-linecap="round" stroke-linejoin="round">' + path + '</svg>')


IC_CALC = _ic('<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 10h2M12 10h2M16 10h0M8 14h2M12 14h2M16 14h0M8 18h6"/>')
IC_CHECK = _ic('<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>')
IC_BUILD = _ic('<path d="M3 21h18M5 21V7l7-4 7 4v14"/><path d="M9 21v-6h6v6M9 11h.01M15 11h.01"/>')


def answer(tag, html, date_src):
    """Réponse encadrée en tête d'article — contre l'AI Overview.

    C'est le bloc que le modèle recopie : une définition en UNE phrase,
    un chiffre daté, une source.
    """
    return (f'<div class="nb-answer rv"><span class="tag">{tag}</span>'
            f'<p>{html}</p><span class="date">{date_src}</span></div>')


def calc_bureaux():
    """Calculateur prix nettoyage bureaux — surface × fréquence → €/mois, €/m², €/poste.

    Justifié par le relevé SERP du 28/08/2026 : requête à variable (prix, m²),
    5 pages de paragraphes, aucun outil dans le top 5.
    """
    grid = [
        ("1", "1 passage / semaine", "1,00 – 1,80 €", "50 m² : 130 – 150 €", "200 m² : 200 – 360 €"),
        ("2", "2 passages / semaine", "1,60 – 2,90 €", "50 m² : 130 – 145 €", "200 m² : 320 – 580 €"),
        ("3", "3 passages / semaine", "2,20 – 3,90 €", "50 m² : 130 – 195 €", "200 m² : 440 – 780 €"),
        ("5", "5 passages / semaine", "3,50 – 6,50 €", "50 m² : 175 – 325 €", "200 m² : 700 – 1 300 €"),
    ]
    rows = "".join(
        f'<tr data-f="{f}"><td>{lbl}</td><td data-v="{m2.split(chr(32))[0].replace(",", ".")}">{m2}</td>'
        f'<td>{c50}</td><td>{c200}</td></tr>'
        for f, lbl, m2, c50, c200 in grid)
    return (
        '<div class="nb rv" id="calcBureaux">'
        f'<div class="nb-head"><span class="ic">{IC_CALC}</span><div>'
        '<h3>Estimez le budget de vos bureaux</h3>'
        '<p>Renseignez votre surface et votre fréquence : vous obtenez la fourchette de marché '
        'au mois, au m² et au poste de travail.</p></div></div>'
        '<form class="nb-form" onsubmit="return false">'
        '<div class="nb-f"><label for="cbSurf">Surface des bureaux</label>'
        '<input id="cbSurf" type="number" inputmode="numeric" min="10" max="3000" step="10" value="150">'
        '<span class="hint">en m²</span></div>'
        '<div class="nb-f"><label for="cbFreq">Fréquence de passage</label>'
        '<select id="cbFreq">'
        '<option value="1">1 fois par semaine</option>'
        '<option value="2">2 fois par semaine</option>'
        '<option value="3" selected>3 fois par semaine</option>'
        '<option value="5">5 jours sur 7</option></select>'
        '<span class="hint">passages hebdomadaires</span></div>'
        '<div class="nb-f"><label for="cbPostes">Postes de travail</label>'
        '<input id="cbPostes" type="number" inputmode="numeric" min="1" max="400" step="1" value="15">'
        '<span class="hint">laissez vide = 1 poste / 10 m²</span></div>'
        '</form>'
        '<div class="nb-out" id="cbOut" aria-live="polite">'
        '<p class="nb-nojs">Activez JavaScript pour l\'estimation instantanée — '
        'la grille complète reste consultable juste en dessous.</p></div>'
        '<div class="nb-warn"><b>Ce sont des fourchettes de marché</b>, relevées le 28 août 2026 sur '
        'les prestataires positionnés à Paris — pas les tarifs de SPN NET. Votre devis dépend de vos '
        'sols, de votre surface vitrée et de vos horaires.</div>'
        '<div class="nb-grid"><table class="nb-sort">'
        '<caption class="sr-only">Grille de prix du nettoyage de bureaux à Paris</caption>'
        '<thead><tr><th>Fréquence</th><th data-s="num">Prix au m²/mois</th>'
        '<th>Bureaux 50 m²</th><th>Plateau 200 m²</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div>'
        '<p class="nb-src"><b>Sources du relevé (28/08/2026) :</b> travaux.com (20–35 €/h en bureaux) · '
        'plateya.fr (20–35 € HT/h) · entreprisenettoyageparis.fr (20–70 € HT/h à Paris) · '
        'galognese.fr (1,50–2,50 €/m²) · menageparfait.fr (26 € HT/h) · oxynet.fr (50 m² : 100–150 €/mois ; '
        '100 m² : 200–300 €/mois) · hoper.io (dès 20 €/h, minimum 1 h 30 par semaine).</p>'
        '</div>')


def calc_copro():
    """Calculateur budget copropriété — lots × étages × fréquence.

    Justifié par le relevé SERP du 28/08/2026 : le PAA ouvre sur « Quel est le
    tarif moyen pour le nettoyage d'une copropriété ? » et un seul résultat du
    top 5 donne un chiffre. Aucun n'a d'outil.
    """
    return (
        '<div class="nb rv" id="calcCopro">'
        f'<div class="nb-head"><span class="ic">{IC_BUILD}</span><div>'
        '<h3>Estimez le budget d\'entretien de votre copropriété</h3>'
        '<p>Le prix ne se lit pas au m² en copropriété, mais au nombre de lots, d\'étages et de '
        'passages. Vous obtenez le coût mensuel et le coût par lot.</p></div></div>'
        '<form class="nb-form" onsubmit="return false">'
        '<div class="nb-f"><label for="ccLots">Nombre de lots</label>'
        '<input id="ccLots" type="number" inputmode="numeric" min="2" max="400" step="1" value="24">'
        '<span class="hint">logements et commerces</span></div>'
        '<div class="nb-f"><label for="ccEtages">Nombre d\'étages</label>'
        '<input id="ccEtages" type="number" inputmode="numeric" min="1" max="20" step="1" value="5">'
        '<span class="hint">cages d\'escalier à traiter</span></div>'
        '<div class="nb-f"><label for="ccFreq">Fréquence de passage</label>'
        '<select id="ccFreq">'
        '<option value="1">1 fois par semaine</option>'
        '<option value="2" selected>2 fois par semaine</option>'
        '<option value="3">3 fois par semaine</option>'
        '<option value="5">5 jours sur 7</option></select>'
        '<span class="hint">passages hebdomadaires</span></div>'
        '</form>'
        '<div class="nb-out" id="ccOut" aria-live="polite">'
        '<p class="nb-nojs">Activez JavaScript pour l\'estimation instantanée — les repères de marché '
        'restent indiqués ci-dessous.</p></div>'
        '<div class="nb-warn"><b>Fourchettes de marché</b> relevées le 28 août 2026, calculées sur une base '
        'de 22 à 34 € HT de l\'heure et une durée d\'intervention proportionnelle au nombre d\'étages et '
        'de lots. Ce ne sont pas les tarifs de SPN NET : le devis se fait après visite.</div>'
        '<p class="nb-src"><b>Repère de marché :</b> pour une petite copropriété avec un passage '
        'hebdomadaire, le budget observé est de <b>150 à 350 € TTC par mois</b> '
        '(lea-syndic.fr, relevé du 13 juin 2026). Taux horaires du secteur : 20 à 35 € HT '
        '(travaux.com, plateya.fr — relevé du 28/08/2026).</p>'
        '</div>')


def checklist(title, intro, items, icon=None):
    """Checklist cochable avec score — vraie <input type=checkbox>, marche sans JS.

    items : liste de tuples (titre, description, référence légale ou None).
    """
    lis = ""
    for i, (t, d, law) in enumerate(items):
        tag = f'<span class="law">{law}</span>' if law else ""
        lis += (f'<li><label for="ck{i}"><input type="checkbox" id="ck{i}">'
                f'<span><b>{t}</b><span>{d}</span>{tag}</span></label></li>')
    return (
        '<div class="nb rv" data-checklist>'
        f'<div class="nb-head"><span class="ic">{icon or IC_CHECK}</span><div>'
        f'<h3>{title}</h3><p>{intro}</p></div></div>'
        f'<ul class="nb-check">{lis}</ul>'
        '<div class="nb-score"><div class="nb-bar"><i></i></div>'
        '<span class="txt">0 / ' + str(len(items)) + ' vérifié</span></div>'
        '</div>')
