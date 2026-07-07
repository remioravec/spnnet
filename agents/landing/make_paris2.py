#!/usr/bin/env python3
"""Génère une page ORGANIQUE 'Société de nettoyage de bureaux à Paris 2e (75002)'
dérivée du design validé (lp.html), pensée pour battre le TOP 1 (NEOSIT) en UX/UI :
contenu local dense (quartiers du 2e), tableau de prestations, FAQ remplie et
localisée, avis Google réels, logos clients réels, formulaire inline.

Publiée en NOINDEX (aperçu) — template Canvas. On la bascule en indexable et en
page /paris-2/ bureaux si le rendu est validé.

Usage : python3 agents/landing/make_paris2.py
"""
from __future__ import annotations

import os
import pathlib

import requests

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
HERE = pathlib.Path(__file__).parent
BASE = (HERE / "lp.html").read_text()
SLUG = "nettoyage-bureaux-paris-2-preview"
SS_TITLE = "Société de nettoyage de bureaux à Paris 2e (75002) | SPN NET"
SS_DESC = ("Société de nettoyage de bureaux dans le 2e arrondissement de Paris (Bourse, "
           "Sentier, Montorgueil). Interventions soir & matin, avis 4,8/5, ISO 45001. Devis 24h.")

# --- 1) CSS additionnel (contenu local + tableau) injecté avant </style> ---
CSS = """
.spn-lp .local{background:#fff}
.spn-lp .local .grid{display:grid;grid-template-columns:1.15fr .85fr;gap:44px;align-items:start}
.spn-lp .local h2{font-size:clamp(1.7rem,3vw,2.3rem);margin-bottom:16px}
.spn-lp .local p{color:var(--ink-2);margin-bottom:14px}
.spn-lp .local .qtiers{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.spn-lp .local .qtiers span{font-size:.82rem;font-weight:600;background:var(--cream);border:1px solid var(--line);padding:7px 13px;border-radius:999px}
.spn-lp .local .side{background:var(--cream);border:1px solid var(--line);border-radius:var(--r);padding:26px;position:sticky;top:16px}
.spn-lp .local .side h3{font-size:1.15rem;margin-bottom:14px}
.spn-lp .tbl{width:100%;border-collapse:collapse;font-size:.92rem;margin-top:6px;background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden}
.spn-lp .tbl th,.spn-lp .tbl td{text-align:left;padding:12px 14px;border-bottom:1px solid var(--line);vertical-align:top}
.spn-lp .tbl th{background:var(--cream);font-family:'Plus Jakarta Sans',sans-serif;font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:var(--grey);font-weight:700}
.spn-lp .tbl tr:last-child td{border-bottom:none}
.spn-lp .tbl td:first-child{font-weight:700;color:var(--ink);white-space:nowrap}
@media(max-width:880px){.spn-lp .local .grid{grid-template-columns:1fr;gap:26px}.spn-lp .local .side{position:static}}
/* --- CRO / copywriting visuel --- */
.spn-lp .hl{background:linear-gradient(180deg,transparent 56%,#FFC49E 56%);padding:0 .06em;font-weight:800;color:var(--ink);white-space:nowrap}
.spn-lp .promise{position:relative;overflow:hidden;background:var(--ink);color:#fff;padding:78px 0;text-align:center}
.spn-lp .promise::before{content:"";position:absolute;inset:0;background:radial-gradient(720px 380px at 50% -12%,rgba(237,93,55,.34),transparent 66%)}
.spn-lp .promise .wrap{position:relative;z-index:1;max-width:900px}
.spn-lp .promise .k{font-family:'Fraunces',serif;font-weight:600;font-size:clamp(2rem,4.8vw,3.5rem);line-height:1.05;letter-spacing:-.015em;margin-bottom:18px}
.spn-lp .promise .k em{font-style:italic;color:var(--orange)}
.spn-lp .promise p{color:rgba(255,255,255,.82);font-size:1.12rem;max-width:640px;margin:0 auto 28px}
.spn-lp .promise .mini-row{display:flex;flex-wrap:wrap;gap:14px 30px;justify-content:center;font-weight:700;font-size:.98rem}
.spn-lp .promise .mini-row span{display:inline-flex;align-items:center;gap:9px;color:#fff}
.spn-lp .promise .mini-row svg{color:var(--orange);flex:none}
.spn-lp .pull{background:#fff;padding:66px 0}
.spn-lp .pull .wrap{max-width:960px;text-align:center}
.spn-lp .pull .mk{font-family:'Fraunces',serif;font-size:3.4rem;color:var(--orange-soft);line-height:.6;display:block}
.spn-lp .pull blockquote{font-family:'Fraunces',serif;font-weight:500;font-size:clamp(1.5rem,3.1vw,2.25rem);line-height:1.26;letter-spacing:-.01em;color:var(--ink);margin:0 0 20px}
.spn-lp .pull blockquote em{font-style:italic;color:var(--orange-deep)}
.spn-lp .pull .by{display:inline-flex;align-items:center;gap:11px;font-size:.92rem;color:var(--grey);font-weight:700}
.spn-lp .pull .by .stars{color:#FBBC05;letter-spacing:1px;font-weight:400}
.spn-lp .gains{display:flex;flex-wrap:wrap;gap:12px 24px;justify-content:center;margin-top:8px}
.spn-lp .gains span{display:inline-flex;align-items:center;gap:9px;font-weight:700;font-size:.96rem;color:var(--ink-2)}
.spn-lp .gains svg{color:var(--orange-deep);flex:none}
/* --- GEO factbox + maillage interne --- */
.spn-lp .facts{background:var(--cream);border:1px solid var(--line);border-radius:var(--r);padding:24px 26px;margin-bottom:34px}
.spn-lp .facts h3{font-size:1.12rem;margin-bottom:16px;display:flex;align-items:center;gap:9px}
.spn-lp .facts h3 svg{color:var(--orange-deep);flex:none}
.spn-lp .facts dl{display:grid;grid-template-columns:repeat(2,1fr);gap:14px 30px;margin:0}
.spn-lp .facts .row{display:flex;flex-direction:column;gap:2px}
.spn-lp .facts dt{font-size:.7rem;text-transform:uppercase;letter-spacing:.07em;color:var(--grey);font-weight:700}
.spn-lp .facts dd{margin:0;font-weight:700;color:var(--ink);font-size:.98rem}
.spn-lp .facts dd a{color:var(--orange-deep)}
@media(max-width:640px){.spn-lp .facts dl{grid-template-columns:1fr}}
.spn-lp .links{background:var(--cream)}
.spn-lp .links .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.spn-lp .links a.card{display:block;background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 20px;transition:transform .18s,box-shadow .18s;color:var(--ink)}
.spn-lp .links a.card:hover{transform:translateY(-3px);box-shadow:var(--shadow-sm);text-decoration:none}
.spn-lp .links a.card b{display:flex;align-items:center;justify-content:space-between;gap:10px;font-size:1.02rem;font-family:'Fraunces',serif;font-weight:600;margin-bottom:4px}
.spn-lp .links a.card small{color:var(--grey);font-size:.85rem}
.spn-lp .links a.card .ar{color:var(--orange-deep);font-weight:700}
@media(max-width:820px){.spn-lp .links .grid{grid-template-columns:1fr}}
/* --- Présence humaine (inspiration NEOSIT / Nikita) --- */
.spn-lp .team{background:#fff}
.spn-lp .team .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:6px}
.spn-lp .team figure{margin:0;border-radius:16px;overflow:hidden;position:relative;background:var(--ink-2);aspect-ratio:3/4}
.spn-lp .team figure img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.spn-lp .team figure:hover img{transform:scale(1.05)}
.spn-lp .team figure::after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 48%,rgba(20,22,27,.82));z-index:1}
.spn-lp .team figcaption{position:absolute;left:14px;right:14px;bottom:12px;z-index:2;color:#fff;font-size:.84rem;font-weight:700}
@media(max-width:820px){.spn-lp .team .grid{grid-template-columns:repeat(2,1fr)}}
.spn-lp .team-cue{display:flex;align-items:center;gap:13px;margin-top:20px}
.spn-lp .team-cue .avs{display:flex}
.spn-lp .team-cue .avs img{width:42px;height:42px;border-radius:50%;object-fit:cover;border:2px solid #fff;margin-left:-12px;box-shadow:var(--shadow-sm)}
.spn-lp .team-cue .avs img:first-child{margin-left:0}
.spn-lp .team-cue small{font-size:.86rem;color:var(--ink-2);font-weight:600;line-height:1.35;max-width:280px}
.spn-lp .team-cue small b{color:var(--ink)}
/* --- Intégration site : menu en overlay + allègement CTA mobile --- */
.spn-lp .hero{padding-top:104px}
@media(max-width:560px){.spn-lp .hero{padding-top:84px}.spn-lp .hero-cta{display:none}}
/* --- Supprime l'espace entre le contenu et le footer --- */
.elementor-widget-theme-post-content .elementor-widget-container{margin-bottom:0!important;padding-bottom:0!important}
.page-content,main.site-main,.site-main,.elementor-section-wrap{margin-bottom:0!important;padding-bottom:0!important}
.spn-lp{margin-bottom:0}
"""

# Ajuste dynamiquement le padding haut du hero à la hauteur réelle du menu (overlay absolu)
HEADFIX = ('<script>(function(){var r=document.querySelector(".spn-lp");if(!r)return;'
           'var hero=r.querySelector(".hero");function pad(){var h=document.querySelector("header.elementor-location-header");'
           'if(h&&hero&&h.offsetHeight){hero.style.paddingTop=(h.offsetHeight+24)+"px";}}'
           'pad();window.addEventListener("load",pad);window.addEventListener("resize",pad);'
           'if(document.readyState!=="loading")pad();else document.addEventListener("DOMContentLoaded",pad);})();</script>')

_IMG = "https://spn-net.fr/wp-content/uploads/2026/02/"

TEAMCUE = ('<div class="team-cue"><div class="avs">'
           '<img src="' + _IMG + 'Teams-01.jpg" alt=""><img src="' + _IMG + 'Teams-07.jpg" alt="">'
           '<img src="' + _IMG + 'Teams-03.jpg" alt=""></div>'
           '<small><b>Une équipe dédiée</b>, formée et fidèle — pas des remplaçants au hasard.</small></div>')

TEAM = ('\n<!-- ============ ÉQUIPE HUMAINE ============ -->\n'
        '<div class="sec team"><div class="wrap">\n'
        '  <div class="sec-head reveal"><span class="eyebrow c">Des visages, pas des remplaçants</span>'
        '<h2>L\'équipe qui prendra soin de vos bureaux</h2>'
        '<p>Des agents formés, en tenue et fidélisés — souvent les mêmes d\'une semaine à l\'autre. '
        'Ils connaissent vos locaux, vos accès et vos exigences.</p></div>\n'
        '  <div class="grid reveal">\n'
        '    <figure><img src="' + _IMG + 'Teams-01.jpg" alt="Agent de propreté de l\'équipe SPN NET à Paris 2" loading="lazy"><figcaption>Agent de propreté</figcaption></figure>\n'
        '    <figure><img src="' + _IMG + 'Teams-02.jpg" alt="Agent d\'entretien SPN NET préparé pour le bionettoyage" loading="lazy"><figcaption>Préparation du matériel</figcaption></figure>\n'
        '    <figure><img src="' + _IMG + 'Teams-03.jpg" alt="Agent de nettoyage professionnel équipé d\'un aspirateur" loading="lazy"><figcaption>Entretien des sols</figcaption></figure>\n'
        '    <figure><img src="' + _IMG + 'Teams-07.jpg" alt="Employée de l\'entreprise de propreté SPN NET en tenue" loading="lazy"><figcaption>En tenue SPN NET</figcaption></figure>\n'
        '  </div>\n</div></div>\n\n<!-- ============ RÉALISATIONS ============ -->')

_CK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'

PROMISE = """
<!-- ============ PROMESSE (bande impact) ============ -->
<div class="promise"><div class="wrap">
  <div class="k reveal">Vos bureaux <em>impeccables chaque matin</em>,<br>sans jamais y penser.</div>
  <p class="reveal">Vous dirigez, nous veillons sur la propreté — en silence, avant l'ouverture, avec une équipe qui connaît vos locaux par cœur.</p>
  <div class="mini-row reveal">
    <span>%CK% Devis sous 24h</span>
    <span>%CK% Sans engagement</span>
    <span>%CK% Un interlocuteur dédié</span>
  </div>
</div></div>
""".replace("%CK%", _CK)

PULL = """
<!-- ============ CITATION IMPACT ============ -->
<div class="pull"><div class="wrap reveal">
  <span class="mk">&ldquo;</span>
  <blockquote>Je ne peux que recommander SPN : pro, efficace et d'une <em>très grande réactivité</em>. Le directeur lui-même se déplace pour le premier état des lieux.</blockquote>
  <span class="by">Valérie Mangin <span class="stars">★★★★★</span> · Avis Google</span>
</div></div>
"""

# --- GEO : encart "l'essentiel" (extractible par les LLM), inséré en tête de section locale ---
FACTS = ('<div class="facts reveal"><h3>' + _CK + ' SPN NET — l\'essentiel</h3><dl>'
         '<div class="row"><dt>Activité</dt><dd>Nettoyage &amp; entretien de bureaux</dd></div>'
         '<div class="row"><dt>Zone desservie</dt><dd>Paris 2ᵉ (75002) &amp; Île-de-France</dd></div>'
         '<div class="row"><dt>Expérience</dt><dd>30 ans · +350 clients</dd></div>'
         '<div class="row"><dt>Certifications</dt><dd>ISO 45001 · EcoVadis Argent</dd></div>'
         '<div class="row"><dt>Note clients</dt><dd>4,8/5 — 48 avis Google</dd></div>'
         '<div class="row"><dt>Horaires d\'intervention</dt><dd>Avant 9h, après 18h, week-end</dd></div>'
         '<div class="row"><dt>Devis</dt><dd>Gratuit, transmis sous 24h</dd></div>'
         '<div class="row"><dt>Contact</dt><dd><a href="tel:+33149462240" data-tel>01 49 46 22 40</a> · Bagneux (92)</dd></div>'
         '</dl></div>')

# --- Maillage interne : arrondissements voisins + pôle tertiaire + département ---
LINKS = """
<!-- ============ MAILLAGE INTERNE ============ -->
<div class="sec links"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow c">Zones &amp; prestations liées</span><h2>Nettoyage de bureaux autour du 2ᵉ</h2><p>Nous intervenons dans les arrondissements voisins et sur toutes vos typologies de locaux.</p></div>
  <div class="grid reveal">
    <a class="card" href="https://spn-net.fr/paris-1/"><b>Paris 1ᵉʳ <span class="ar">→</span></b><small>Louvre, Halles — bureaux &amp; commerces</small></a>
    <a class="card" href="https://spn-net.fr/paris-9/"><b>Paris 9ᵉ <span class="ar">→</span></b><small>Opéra, Grands Boulevards</small></a>
    <a class="card" href="https://spn-net.fr/paris-3/"><b>Paris 3ᵉ <span class="ar">→</span></b><small>Marais — agences &amp; studios</small></a>
    <a class="card" href="https://spn-net.fr/paris-8/"><b>Paris 8ᵉ <span class="ar">→</span></b><small>Quartier d'affaires, sièges</small></a>
    <a class="card" href="https://spn-net.fr/tertiaire/"><b>Pôle Tertiaire &amp; bureaux <span class="ar">→</span></b><small>Notre expertise bureaux, tous secteurs</small></a>
    <a class="card" href="https://spn-net.fr/92-hauts-de-seine/"><b>Hauts-de-Seine (92) <span class="ar">→</span></b><small>Notre base — proximité immédiate</small></a>
  </div>
</div></div>

<!-- ============ FINAL CTA ============ -->"""

BREADCRUMB = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
              '"itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":"https://spn-net.fr/"},'
              '{"@type":"ListItem","position":2,"name":"Nettoyage de bureaux","item":"https://spn-net.fr/tertiaire/"},'
              '{"@type":"ListItem","position":3,"name":"Paris 2e (75002)"}]}</script>')

# --- 2) Hero (message-match requête locale) ---
REPL = [
    ('<span class="eyebrow">Entretien de bureaux · Paris & Île-de-France</span>',
     '<span class="eyebrow">Nettoyage de bureaux · Paris 2ᵉ — 75002</span>'),
    ("<h1>Entretien de <em>bureaux</em> à Paris, sans jamais gêner votre activité</h1>",
     "<h1>Société de <em>nettoyage de bureaux</em> à Paris 2ᵉ (75002)</h1>"),
    ('<p class="lead">Sociétés, PME et startups : un nettoyage de bureaux régulier et fiable, réalisé <b>tôt le matin ou en soirée</b>. Un interlocuteur dédié, des équipes formées et certifiées ISO 45001 — devis sous 24h.</p>',
     '<p class="lead">De la <b>Bourse</b> au <b>Sentier</b>, nous entretenons les bureaux, sièges et coworkings du 2ᵉ arrondissement. Interventions <span class="hl">avant 9h ou après 18h</span>, sans jamais gêner votre activité. Équipe dédiée, certifiée ISO 45001 — <span class="hl">devis sous 24h</span>.</p>'),
    # Titre WHY orienté bénéfice + micro-gains
    ('<span class="eyebrow c">Pourquoi SPN NET</span><h2>Propreté, rigueur et engagement depuis 30 ans</h2><p>Une entreprise à taille humaine, deux priorités : le client et le salarié.</p>',
     '<span class="eyebrow c">Ce que vous y gagnez</span><h2>Moins de tracas, des locaux toujours nickel</h2><p>Une entreprise à taille humaine qui traite vos bureaux comme les siens — et vos équipes avec le même soin.</p>'
     '<div class="gains" style="margin-top:18px">'
     '<span>' + _CK + ' Zéro relance à faire</span>'
     '<span>' + _CK + ' Même équipe, chaque semaine</span>'
     '<span>' + _CK + ' Contrôle qualité régulier</span></div>'),
    # Zone : recentrage Paris 2
    ("<p>Basés dans les Hauts-de-Seine, nous réagissons vite à Paris comme en proche couronne. Une présence locale et des équipes mobiles dans les 20 arrondissements et l'ensemble des départements franciliens.</p>",
     "<p>Notre base dans les Hauts-de-Seine nous place à quelques minutes du 2ᵉ arrondissement : nous intervenons chaque jour dans le 75002 (Bourse, Sentier, Montorgueil, Vivienne, Mail…) et, plus largement, dans tout Paris et l'Île-de-France.</p>"),
]

# --- 3) Section contenu local + tableau (insérée avant WHY US) ---
LOCAL = """
<!-- ============ CONTENU LOCAL PARIS 2 ============ -->
<div class="sec local"><div class="wrap">
  <div class="sec-head reveal" style="max-width:820px;text-align:left;margin:0 0 30px">
    <span class="eyebrow">Expertise locale · 75002</span>
    <h2>Le nettoyage de bureaux dans le 2ᵉ arrondissement de Paris</h2>
  </div>
  <div class="grid">
    <div class="reveal">
      <p>Le 2ᵉ arrondissement concentre une densité rare de bureaux : le quartier d'affaires de la <b>Bourse</b> et des Grands Boulevards, les sièges et agences du <b>Sentier</b> — devenu le « Silicon Sentier » des startups et de la tech —, ainsi que les espaces de coworking autour de <b>Montorgueil</b> et de la rue du Mail.</p>
      <p>Ces bureaux, souvent installés dans des <b>immeubles haussmanniens</b> aux accès contraints (pas toujours de monte-charge, horaires de gardiennage, plateaux occupés en continu), exigent un prestataire réactif et discret. Nos équipes interviennent <span class="hl">avant 9h ou après 18h</span>, avant l'arrivée ou après le départ de vos collaborateurs, pour un résultat impeccable sans perturber votre activité.</p>
      <p>Sièges sociaux, agences de communication, cabinets de conseil, studios et coworkings : nous adaptons la fréquence et le protocole à chaque type de locaux du 2ᵉ. Voir aussi notre <a href="https://spn-net.fr/tertiaire/">pôle nettoyage tertiaire &amp; bureaux</a>.</p>
      <div class="qtiers">
        <span>Quartier de la Bourse</span><span>Le Sentier</span><span>Montorgueil</span><span>Rue du Mail</span><span>Vivienne</span><span>Gaillon</span><span>Grands Boulevards</span>
      </div>
    </div>
    <div class="side reveal">
      <h3>Pourquoi le 2ᵉ nous choisit</h3>
      <ul class="hero-points" style="margin:0">
        <li>Intervention avant 9h ou après 18h</li>
        <li>Immeubles haussmanniens & accès difficiles</li>
        <li>Un interlocuteur dédié, joignable</li>
        <li>Devis sous 24h, sans engagement</li>
      </ul>
    </div>
  </div>
  <div style="margin-top:40px" class="reveal">
    <h3 style="font-family:'Fraunces',serif;font-weight:600;font-size:1.4rem;margin-bottom:14px">Nos prestations de nettoyage de bureaux à Paris 2ᵉ</h3>
    <div style="overflow-x:auto"><table class="tbl">
      <thead><tr><th>Prestation</th><th>Ce que nous faisons</th><th>Fréquence type</th></tr></thead>
      <tbody>
        <tr><td>Entretien des bureaux</td><td>Dépoussiérage, surfaces, corbeilles, désinfection des points de contact</td><td>Quotidien / 3× sem.</td></tr>
        <tr><td>Sanitaires</td><td>Nettoyage complet, désinfection et réassort des consommables</td><td>Quotidien</td></tr>
        <tr><td>Sols</td><td>Aspiration, lavage, décapage et cristallisation selon le revêtement</td><td>Selon protocole</td></tr>
        <tr><td>Vitrerie</td><td>Surfaces vitrées intérieures, cloisons, portes et vitrines</td><td>Mensuel / trimestriel</td></tr>
        <tr><td>Salles de réunion & communs</td><td>Remise en ordre, tisanerie/cuisine, espace d'accueil</td><td>Quotidien</td></tr>
        <tr><td>Remise en état</td><td>Grand nettoyage, fin de chantier, avant/après emménagement</td><td>Ponctuel</td></tr>
      </tbody>
    </table></div>
  </div>
</div></div>

<!-- ============ WHY US ============ -->"""

# --- 4) FAQ localisée (remplace les 6 questions génériques) ---
FAQ_OLD_START = '    <details class="acc"><summary>Quelle est votre zone d\'intervention ?'
FAQ_OLD = None  # rempli plus bas via slicing


def main() -> None:
    html = BASE
    # Page intégrée au site (menu + footer) : on retire la barre logo/tel de la LP,
    # qui ferait doublon avec l'en-tête du site.
    s = html.index("<!-- ============ TOP STRIP ============ -->")
    e = html.index("<!-- ============ HERO ============ -->")
    html = html[:s] + html[e:]
    # CSS
    assert "</style>" in html
    html = html.replace("</style>", CSS + "</style>", 1)
    # Hero + zone
    for old, new in REPL:
        assert old in html, f"anchor introuvable: {old[:50]}"
        html = html.replace(old, new, 1)
    # Bande promesse + section locale, avant WHY US
    assert "<!-- ============ WHY US ============ -->" in html
    html = html.replace("<!-- ============ WHY US ============ -->", PROMISE + LOCAL, 1)
    # GEO factbox en tête de la section locale
    anchor = '<div class="grid">\n    <div class="reveal">\n      <p>Le 2ᵉ arrondissement'
    assert anchor in html, "anchor factbox introuvable"
    html = html.replace(anchor, FACTS + '\n  ' + anchor, 1)
    # Citation impact juste avant les avis
    assert "<!-- ============ AVIS GOOGLE" in html
    html = html.replace("<!-- ============ AVIS GOOGLE", PULL + "\n<!-- ============ AVIS GOOGLE", 1)
    # Maillage interne avant le CTA final
    assert "<!-- ============ FINAL CTA ============ -->" in html
    html = html.replace("<!-- ============ FINAL CTA ============ -->", LINKS, 1)
    # Présence humaine : section équipe avant les réalisations
    assert "<!-- ============ RÉALISATIONS ============ -->" in html
    html = html.replace("<!-- ============ RÉALISATIONS ============ -->", TEAM, 1)
    # Rappel visuel d'agents dans le hero (après la trust-row)
    tr_anchor = 'ISO 45001</b></span></div>\n    </div>'
    assert tr_anchor in html, "anchor trust-row introuvable"
    html = html.replace(tr_anchor, 'ISO 45001</b></span></div>\n      ' + TEAMCUE + '\n    </div>', 1)
    # FAQ : remplacer le bloc des 6 <details> par une FAQ locale
    start = html.index(FAQ_OLD_START)
    end = html.index("</details>", html.index("bien-être et à la sécurité de nos agents")) + len("</details>")
    faq_new = (
        '    <details class="acc"><summary>Intervenez-vous dans tout le 2ᵉ arrondissement (75002) ?<span class="pl">+</span></summary><div class="body">Oui, dans l\'ensemble du 2ᵉ : quartier de la Bourse, Sentier, Montorgueil, rue du Mail, Vivienne, Gaillon et les Grands Boulevards. Nous couvrons aussi tout Paris et l\'Île-de-France.</div></details>\n'
        '    <details class="acc"><summary>Pouvez-vous nettoyer nos bureaux en dehors des heures d\'ouverture ?<span class="pl">+</span></summary><div class="body">Absolument. Nos équipes interviennent tôt le matin (avant 9h) ou en soirée (après 18h), et le week-end si besoin, pour ne jamais perturber votre activité ni gêner vos collaborateurs.</div></details>\n'
        '    <details class="acc"><summary>Gérez-vous les immeubles haussmanniens et les accès difficiles ?<span class="pl">+</span></summary><div class="body">Oui. Beaucoup de bureaux du 2ᵉ sont dans des immeubles anciens, parfois sans monte-charge et avec gardiennage. Nos agents sont habitués à ces contraintes d\'accès et s\'organisent en conséquence.</div></details>\n'
        '    <details class="acc"><summary>Intervenez-vous pour les startups et coworkings du Sentier ?<span class="pl">+</span></summary><div class="body">Oui : le 2ᵉ compte de nombreuses jeunes entreprises et espaces partagés. La fréquence et l\'organisation de l\'entretien sont adaptées à ce type de locaux lors du devis.</div></details>\n'
        '    <details class="acc"><summary>Combien coûte le nettoyage de bureaux à Paris 2ᵉ ?<span class="pl">+</span></summary><div class="body">Le tarif dépend de la surface, de la fréquence et des prestations retenues (entretien courant, sanitaires, vitrerie, sols, remise en état). Il n\'y a pas de forfait standard imposé : nous établissons un devis gratuit et personnalisé sous 24h, adapté à vos locaux du 2ᵉ.</div></details>\n'
        '    <details class="acc"><summary>Quelle société de nettoyage de bureaux choisir dans le 2ᵉ ?<span class="pl">+</span></summary><div class="body">Regardez la proximité (réactivité), les certifications (ISO 45001), les avis clients réels et la capacité à intervenir en horaires décalés. SPN NET réunit ces critères : 4,8/5 sur 48 avis Google, certifiée ISO 45001 et EcoVadis Argent, intervention soir et matin, interlocuteur dédié.</div></details>\n'
        '    <details class="acc"><summary>Sous quel délai vais-je recevoir mon devis ?<span class="pl">+</span></summary><div class="body">Votre devis est gratuit, sans engagement, et transmis sous 24h ouvrées après l\'étude de votre besoin (souvent précédée d\'une courte visite sur site).</div></details>\n'
        '    <details class="acc"><summary>Êtes-vous une entreprise certifiée ?<span class="pl">+</span></summary><div class="body">SPN NET est certifiée ISO 45001 par DEKRA (santé-sécurité au travail) et a obtenu la médaille d\'argent EcoVadis 2025 (top 15 % RSE), fort de 30 ans d\'expérience et de +350 clients.</div></details>\n'
        '    <details class="acc"><summary>À quelle fréquence faut-il nettoyer des bureaux ?<span class="pl">+</span></summary><div class="body">La fréquence dépend de votre surface, de votre effectif et de votre activité. Elle est définie avec vous lors du devis, d\'un passage plusieurs fois par semaine à un entretien plus ponctuel.</div></details>\n'
        '    <details class="acc"><summary>Comment se déroule le nettoyage des bureaux ?<span class="pl">+</span></summary><div class="body">Après un état des lieux, un protocole est défini pour vos locaux (postes de travail, sanitaires, sols, parties communes) puis réalisé par une équipe dédiée, aux horaires convenus. Les modalités précises figurent dans votre devis.</div></details>\n'
        '    <details class="acc"><summary>Vos prestations s\'inscrivent-elles dans une démarche RSE ?<span class="pl">+</span></summary><div class="body">Oui : SPN NET a obtenu la médaille d\'argent EcoVadis 2025 (top 15 % RSE) et est certifiée ISO 45001. Les protocoles et produits adaptés à vos locaux sont définis lors de l\'étude de votre besoin.</div></details>\n'
        '    <details class="acc"><summary>Proposez-vous la vitrerie et l\'entretien des parties communes ?<span class="pl">+</span></summary><div class="body">Oui : vitrerie, sols, sanitaires, salles de réunion et parties communes figurent parmi les prestations de nettoyage de bureaux, en complément de l\'entretien courant.</div></details>\n'
        '    <details class="acc"><summary>Faites-vous les nettoyages ponctuels (remise en état, fin de chantier) ?<span class="pl">+</span></summary><div class="body">Oui, nous réalisons aussi des interventions ponctuelles comme la remise en état ou le nettoyage de fin de chantier, en complément de l\'entretien régulier.</div></details>\n'
        '    <details class="acc"><summary>Intervenez-vous pour plusieurs sites ?<span class="pl">+</span></summary><div class="body">Pour un besoin sur plusieurs sites, précisez-le dans votre demande : nous étudions chaque situation et vous répondons sous 24h.</div></details>\n'
        '    <details class="acc"><summary>Le devis engage-t-il à quelque chose ?<span class="pl">+</span></summary><div class="body">Non : le devis est gratuit et sans engagement. Les conditions du contrat d\'entretien sont définies avec vous avant toute intervention.</div></details>'
    )
    html = html[:start] + faq_new + html[end:]

    # FAQ schema (JSON-LD) localisé
    faq_ld_old_anchor = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
    assert faq_ld_old_anchor in html
    ld_start = html.index(faq_ld_old_anchor)
    ld_end = html.index("]}", ld_start) + len("]}")
    faq_ld = ('{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
              '{"@type":"Question","name":"Intervenez-vous dans tout le 2e arrondissement (75002) ?","acceptedAnswer":{"@type":"Answer","text":"Oui, dans tout le 2e : Bourse, Sentier, Montorgueil, rue du Mail, Vivienne, Gaillon et les Grands Boulevards, ainsi que tout Paris et l\'Ile-de-France."}},'
              '{"@type":"Question","name":"Pouvez-vous nettoyer nos bureaux en dehors des heures d\'ouverture ?","acceptedAnswer":{"@type":"Answer","text":"Oui, nos equipes interviennent avant 9h, apres 18h ou le week-end pour ne pas perturber votre activite."}},'
              '{"@type":"Question","name":"Gerez-vous les immeubles haussmanniens et les acces difficiles ?","acceptedAnswer":{"@type":"Answer","text":"Oui, nos agents sont habitues aux immeubles anciens du 2e, parfois sans monte-charge et avec gardiennage."}},'
              '{"@type":"Question","name":"Sous quel delai vais-je recevoir mon devis ?","acceptedAnswer":{"@type":"Answer","text":"Un devis gratuit et sans engagement sous 24h ouvrees apres etude de votre besoin."}},'
              '{"@type":"Question","name":"Etes-vous une entreprise certifiee ?","acceptedAnswer":{"@type":"Answer","text":"SPN NET est certifiee ISO 45001 (DEKRA) et medaille d\'argent EcoVadis 2025, avec 30 ans d\'experience."}},'
              '{"@type":"Question","name":"Combien coute le nettoyage de bureaux a Paris 2e ?","acceptedAnswer":{"@type":"Answer","text":"Le tarif depend de la surface, de la frequence et des prestations (entretien courant, sanitaires, vitrerie, sols, remise en etat). Pas de forfait standard : devis gratuit et personnalise sous 24h."}},'
              '{"@type":"Question","name":"Quelle societe de nettoyage de bureaux choisir dans le 2e ?","acceptedAnswer":{"@type":"Answer","text":"Regardez la proximite, les certifications (ISO 45001), les avis reels et l\'intervention en horaires decales. SPN NET : 4,8/5 sur 48 avis, ISO 45001, EcoVadis Argent, intervention soir et matin, interlocuteur dedie."}},'
              '{"@type":"Question","name":"A quelle frequence faut-il nettoyer des bureaux ?","acceptedAnswer":{"@type":"Answer","text":"La frequence depend de la surface, de l\'effectif et de l\'activite ; elle est definie avec vous au devis, d\'un passage plusieurs fois par semaine a un entretien plus ponctuel."}},'
              '{"@type":"Question","name":"Comment se deroule le nettoyage des bureaux ?","acceptedAnswer":{"@type":"Answer","text":"Apres un etat des lieux, un protocole est defini pour vos locaux puis realise par une equipe dediee aux horaires convenus. Les modalites precises figurent dans le devis."}},'
              '{"@type":"Question","name":"Vos prestations s\'inscrivent-elles dans une demarche RSE ?","acceptedAnswer":{"@type":"Answer","text":"Oui : SPN NET est medaille d\'argent EcoVadis 2025 et certifiee ISO 45001. Les protocoles et produits adaptes sont definis lors de l\'etude du besoin."}},'
              '{"@type":"Question","name":"Proposez-vous la vitrerie et les parties communes ?","acceptedAnswer":{"@type":"Answer","text":"Oui : vitrerie, sols, sanitaires, salles de reunion et parties communes figurent parmi les prestations, en complement de l\'entretien courant."}},'
              '{"@type":"Question","name":"Faites-vous les nettoyages ponctuels (remise en etat, fin de chantier) ?","acceptedAnswer":{"@type":"Answer","text":"Oui : interventions ponctuelles comme la remise en etat ou le nettoyage de fin de chantier, en complement de l\'entretien regulier."}},'
              '{"@type":"Question","name":"Intervenez-vous pour plusieurs sites ?","acceptedAnswer":{"@type":"Answer","text":"Pour un besoin multi-sites, precisez-le dans votre demande : nous etudions chaque situation et repondons sous 24h."}},'
              '{"@type":"Question","name":"Le devis engage-t-il a quelque chose ?","acceptedAnswer":{"@type":"Answer","text":"Non : le devis est gratuit et sans engagement. Les conditions du contrat sont definies avec vous avant toute intervention."}}'
              ']}')
    html = html[:ld_start] + faq_ld + html[ld_end:]

    # Breadcrumb JSON-LD (GEO / structure) avant la fermeture de section
    assert html.rstrip().endswith("</section>")
    html = html.rstrip()[:-len("</section>")] + BREADCRUMB + HEADFIX + "\n</section>\n"

    (HERE / "paris2.html").write_text(html)

    # Publier (noindex, canvas)
    content = "<!-- wp:html -->\n" + html + "\n<!-- /wp:html -->"
    ex = requests.get("https://spn-net.fr/wp-json/wp/v2/pages",
                      params={"slug": SLUG, "_fields": "id"}, auth=AUTH, timeout=30).json()
    payload = {"title": "Nettoyage bureaux Paris 2 (aperçu)", "slug": SLUG, "status": "publish",
               "content": content, "template": "elementor_header_footer",
               "meta": {"slim_seo": {"title": SS_TITLE, "description": SS_DESC, "noindex": True}}}
    if ex:
        r = requests.post(f"https://spn-net.fr/wp-json/wp/v2/pages/{ex[0]['id']}", auth=AUTH, timeout=60, json=payload)
    else:
        r = requests.post("https://spn-net.fr/wp-json/wp/v2/pages", auth=AUTH, timeout=60, json=payload)
    r.raise_for_status()
    print("✓ Aperçu publié :", r.json().get("link"))


if __name__ == "__main__":
    main()
