#!/usr/bin/env python3
"""Génère une MAQUETTE d'accueil (noindex) proposant un nouveau visuel homepage,
avec maillage descendant vers les 8 pôles sectoriels et les zones (liens réels).

Publiée en NOINDEX (aperçu) sur /accueil-preview/. N'écrase pas la vraie home.
Usage : python3 agents/landing/make_home.py
"""
from __future__ import annotations

import os
import sys
import pathlib

import requests

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from make_paris2 import CSS, PROMISE, PULL, TEAM, TEAMCUE, HEADFIX, _CK  # noqa: E402
import make_zone as mz  # noqa: E402

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
SLUG = "accueil-preview"
SS_TITLE = "Entreprise de nettoyage à Paris & Île-de-France | SPN NET (aperçu)"
SS_DESC = ("Entreprise de propreté à Paris et en Île-de-France depuis 30 ans : bureaux, commerces, "
           "santé, hôtellerie, copropriétés. ISO 45001, 4,8/5. Devis 24h.")

HOME_CSS = """
.spn-lp .sectors{background:#fff}
.spn-lp .sectors .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.spn-lp .sectors a.card{display:block;background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px 20px;transition:transform .18s,box-shadow .18s;color:var(--ink)}
.spn-lp .sectors a.card:hover{transform:translateY(-4px);box-shadow:var(--shadow-sm);text-decoration:none}
.spn-lp .sectors a.card .ic{width:44px;height:44px;border-radius:12px;background:var(--orange-soft);display:flex;align-items:center;justify-content:center;color:var(--orange-deep);margin-bottom:12px}
.spn-lp .sectors a.card b{display:block;font-family:'Fraunces',serif;font-weight:600;font-size:1.08rem;margin-bottom:3px}
.spn-lp .sectors a.card small{color:var(--grey);font-size:.85rem;display:block}
.spn-lp .sectors a.card .go{color:var(--orange-deep);font-weight:700;font-size:.85rem;margin-top:10px;display:inline-block}
.spn-lp .arr a{font-size:.82rem;font-weight:600;color:#fff;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);padding:7px 13px;border-radius:9px;transition:background .15s,border .15s}
.spn-lp .arr a:hover{background:var(--orange);border-color:var(--orange);text-decoration:none}
.spn-lp .dep a{font-size:.82rem;font-weight:600;color:#fff;background:rgba(237,93,55,.16);border:1px solid rgba(237,93,55,.4);padding:7px 13px;border-radius:9px}
.spn-lp .dep a:hover{background:var(--orange);text-decoration:none}
@media(max-width:820px){.spn-lp .sectors .grid{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.spn-lp .sectors .grid{grid-template-columns:1fr}}
/* --- Deux expertises (branding) --- */
.spn-lp .pillars{background:var(--cream)}
.spn-lp .pillars .grid{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.spn-lp .pillar{position:relative;border-radius:22px;overflow:hidden;min-height:360px;display:flex;align-items:flex-end;color:#fff}
.spn-lp .pillar img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;transition:transform .6s}
.spn-lp .pillar:hover img{transform:scale(1.06)}
.spn-lp .pillar::after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 28%,rgba(20,22,27,.92));z-index:1}
.spn-lp .pillar .in{position:relative;z-index:2;padding:32px}
.spn-lp .pillar .tag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;background:var(--orange);color:#fff;padding:5px 12px;border-radius:999px;margin-bottom:12px}
.spn-lp .pillar h3{color:#fff;font-size:1.8rem;margin-bottom:8px}
.spn-lp .pillar p{color:rgba(255,255,255,.86);margin-bottom:18px;max-width:440px;font-size:1rem}
.spn-lp .pillar .lk{display:inline-flex;align-items:center;gap:8px;font-weight:700;color:#fff;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);padding:11px 20px;border-radius:999px}
.spn-lp .pillar:hover .lk{background:var(--orange);border-color:var(--orange)}
@media(max-width:820px){.spn-lp .pillars .grid{grid-template-columns:1fr}}
"""

_ARROW = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def pillars_section():
    return (
        '\n<!-- ============ DEUX EXPERTISES (branding) ============ -->\n'
        '<div class="sec pillars"><div class="wrap">\n'
        '  <div class="sec-head reveal"><span class="eyebrow c">Nos deux expertises</span>'
        '<h2>Le nettoyage… et bien plus</h2>'
        '<p>Une même exigence de propreté, du poste de travail à la cabine d\'ascenseur.</p></div>\n'
        '  <div class="grid reveal">\n'
        '    <a class="pillar" href="https://spn-net.fr/tertiaire/">'
        '<img src="https://spn-net.fr/wp-content/uploads/2026/01/tertiaire-1-1024x683.jpg" alt="Nettoyage de bureaux et locaux professionnels" loading="lazy">'
        '<div class="in"><span class="tag">Propreté</span><h3>Nettoyage professionnel</h3>'
        '<p>Bureaux, commerces, santé, hôtellerie, copropriétés… Tous secteurs, à Paris et en Île-de-France.</p>'
        f'<span class="lk">Voir nos secteurs {_ARROW}</span></div></a>\n'
        '    <a class="pillar" href="https://spn-net.fr/ascenseurs-escalators/">'
        '<img src="https://spn-net.fr/wp-content/uploads/2026/03/ascenseurs-et-escalators-e1773133478487.webp" alt="Nettoyage d\'ascenseurs et escalators" loading="lazy">'
        '<div class="in"><span class="tag">Spécialité</span><h3>Ascenseurs & Escalators</h3>'
        '<p>Notre expertise reconnue : le nettoyage des ascenseurs et escalators — la confiance des grands acteurs du secteur (OTIS, KONE, Schindler…).</p>'
        f'<span class="lk">Découvrir {_ARROW}</span></div></a>\n'
        '  </div>\n</div></div>')

_SEC_ICON = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>')

SECTORS = [
    ("tertiaire", "Bureaux & Tertiaire", "Sièges, plateaux, coworkings"),
    ("commerce-et-retail", "Commerce & Retail", "Boutiques, surfaces de vente"),
    ("sante-et-medical", "Santé & Médical", "Cabinets, labos, bionettoyage"),
    ("logistique-et-industrie", "Logistique & Industrie", "Entrepôts, sites industriels"),
    ("hotellerie-et-restauration", "Hôtellerie & Restauration", "Hôtels, restaurants"),
    ("copropriete-et-habitat", "Copropriété & Habitat", "Immeubles, parties communes"),
    ("loisirs-culture-et-evenementiel", "Loisirs & Événementiel", "Musées, salles, ERP"),
    ("enseignement-et-petite-enfance", "Enseignement & Petite Enfance", "Écoles, crèches"),
]

FACTS = ('<div class="facts reveal"><h3>' + _CK + ' SPN NET — l\'essentiel</h3><dl>'
         '<div class="row"><dt>Activité</dt><dd>Entreprise de propreté, tous secteurs</dd></div>'
         '<div class="row"><dt>Zone desservie</dt><dd>Paris &amp; Île-de-France</dd></div>'
         '<div class="row"><dt>Expérience</dt><dd>30 ans · +350 clients</dd></div>'
         '<div class="row"><dt>Certifications</dt><dd>ISO 45001 · EcoVadis Argent</dd></div>'
         '<div class="row"><dt>Note clients</dt><dd>4,8/5 — 48 avis Google</dd></div>'
         '<div class="row"><dt>Horaires d\'intervention</dt><dd>Avant 9h, après 18h, week-end</dd></div>'
         '<div class="row"><dt>Devis</dt><dd>Gratuit, transmis sous 24h</dd></div>'
         '<div class="row"><dt>Contact</dt><dd><a href="tel:+33149462240" data-tel>01 49 46 22 40</a> · Bagneux (92)</dd></div>'
         '</dl></div>')


def sectors_section():
    cards = ""
    for slug, name, sub in SECTORS:
        cards += (f'    <a class="card" href="https://spn-net.fr/{slug}/"><div class="ic">{_SEC_ICON}</div>'
                  f'<b>{name}</b><small>{sub}</small><span class="go">Découvrir →</span></a>\n')
    return (
        '\n<!-- ============ SECTEURS (maillage) ============ -->\n'
        '<div class="sec sectors"><div class="wrap">\n'
        '  <div class="sec-head reveal"><span class="eyebrow c">Nos secteurs d\'expertise</span>'
        '<h2>Une propreté adaptée à chaque métier</h2>'
        '<p>Nous intervenons dans tous les environnements professionnels, avec des protocoles dédiés.</p></div>\n'
        + FACTS +
        '\n  <div class="grid reveal">\n' + cards + '  </div>\n</div></div>\n\n<!-- ============ WHY US ============ -->')


def faq_home():
    items = [
        ("Quels types de locaux nettoyez-vous ?",
         "Tous les environnements professionnels : bureaux et tertiaire, commerces, santé et médical, logistique et industrie, hôtellerie-restauration, copropriétés, lieux culturels et établissements scolaires."),
        ("Quelle est votre zone d'intervention ?",
         "Paris (les 20 arrondissements) et toute l'Île-de-France : 77, 78, 91, 92, 93, 94 et 95. Notre base est à Bagneux (92)."),
        ("Pouvez-vous intervenir en dehors des heures d'activité ?",
         "Oui, nos équipes interviennent tôt le matin, en soirée ou le week-end selon vos contraintes, pour ne pas perturber votre activité."),
        ("Combien coûte une prestation de nettoyage ?",
         "Le tarif dépend de la surface, de la fréquence et des prestations retenues. Il n'y a pas de forfait standard imposé : le devis est gratuit et personnalisé, sous 24h."),
        ("Vos prestations s'inscrivent-elles dans une démarche RSE ?",
         "Oui : SPN NET a obtenu la médaille d'argent EcoVadis 2025 et est certifiée ISO 45001. Les protocoles et produits adaptés sont définis lors de l'étude de votre besoin."),
        ("Le devis engage-t-il à quelque chose ?",
         "Non : le devis est gratuit et sans engagement. Les conditions du contrat sont définies avec vous avant toute intervention."),
    ]
    html = "".join(
        f'    <details class="acc"><summary>{q}<span class="pl">+</span></summary><div class="body">{a}</div></details>\n'
        for q, a in items)
    return html.rstrip("\n"), items


ARR = "".join(f'<a href="https://spn-net.fr/paris-{i}/">Paris {i}</a>' for i in range(1, 21))
DEP = "".join(f'<a href="https://spn-net.fr/{s}/">{lbl}</a>' for s, lbl in [
    ("77-seine-et-marne", "77 Seine-et-Marne"), ("78-yvelines", "78 Yvelines"),
    ("91-essonne", "91 Essonne"), ("92-hauts-de-seine", "92 Hauts-de-Seine"),
    ("93-seine-saint-denis", "93 Seine-Saint-Denis"), ("94-val-de-marne", "94 Val-de-Marne"),
    ("95-val-doise", "95 Val-d'Oise")])


def build():
    h = mz.BASE_HTML
    # aperçu : garde le noindex injecteur (page témoin) ; retire la barre logo/tel
    a = h.index("<!-- ============ TOP STRIP ============ -->")
    b = h.index("<!-- ============ HERO ============ -->")
    h = h[:a] + h[b:]
    h = h.replace("</style>", CSS + HOME_CSS + "</style>", 1)
    # hero (positionnement entreprise, tous secteurs)
    h = h.replace(mz.A_EYEBROW, '<span class="eyebrow">Entreprise de propreté · Paris & Île-de-France</span>', 1)
    h = h.replace(mz.A_H1, "<h1>Votre entreprise de <em>propreté professionnelle</em> à Paris et en Île-de-France</h1>", 1)
    h = h.replace(mz.A_LEAD,
                  '<p class="lead">30 ans au service des professionnels franciliens. Le <b>nettoyage tous secteurs</b> '
                  'et notre spécialité, les <b>ascenseurs & escalators</b>. Équipes certifiées ISO 45001, un interlocuteur '
                  'dédié — <span class="hl">devis sous 24h</span>.</p>', 1)
    # deux expertises (branding) + secteurs avant WHY
    h = h.replace("<!-- ============ WHY US ============ -->", PROMISE + pillars_section() + sectors_section(), 1)
    # citation avant avis
    h = h.replace("<!-- ============ AVIS GOOGLE", PULL + "\n<!-- ============ AVIS GOOGLE", 1)
    # équipe avant réalisations
    h = h.replace("<!-- ============ RÉALISATIONS ============ -->", TEAM, 1)
    tr = 'ISO 45001</b></span></div>\n    </div>'
    h = h.replace(tr, 'ISO 45001</b></span></div>\n      ' + TEAMCUE + '\n    </div>', 1)
    # WHY sec-head bénéfice
    h = h.replace(
        '<span class="eyebrow c">Pourquoi SPN NET</span><h2>Propreté, rigueur et engagement depuis 30 ans</h2><p>Une entreprise à taille humaine, deux priorités : le client et le salarié.</p>',
        '<span class="eyebrow c">Ce que vous y gagnez</span><h2>Moins de tracas, des locaux toujours nickel</h2><p>Une entreprise à taille humaine qui traite vos locaux comme les siens — et vos équipes avec le même soin.</p>'
        '<div class="gains" style="margin-top:18px">'
        '<span>' + _CK + ' Zéro relance à faire</span>'
        '<span>' + _CK + ' Même équipe, chaque semaine</span>'
        '<span>' + _CK + ' Contrôle qualité régulier</span></div>', 1)
    # zone : boutons -> liens réels (maillage)
    zs = h.index('<div class="arr">')
    ze = h.index('</div>', zs) + len('</div>')
    h = h[:zs] + '<div class="arr">' + ARR + '</div>' + h[ze:]
    ds = h.index('<div class="dep">')
    de = h.index('</div>', ds) + len('</div>')
    h = h[:ds] + '<div class="dep">' + DEP + '</div>' + h[de:]
    # FAQ home
    fs = h.index('    <details class="acc"><summary>Quelle est votre zone')
    fe = h.index("</details>", h.index("bien-être et à la sécurité de nos agents")) + len("</details>")
    fhtml, fitems = faq_home()
    h = h[:fs] + fhtml + h[fe:]
    ls = h.index('{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[')
    le = h.index("]}", ls) + len("]}")
    q = ",".join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
                 % (mz.strip_accents(n).replace('"', "'"), mz.strip_accents(x).replace('"', "'")) for n, x in fitems)
    h = h[:ls] + '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + q + ']}' + h[le:]
    h = mz.apply_carousel(h)
    h = h.rstrip()[:-len("</section>")] + HEADFIX + mz.CAROUSEL_JS + "\n</section>\n"
    return h


def main():
    html = build()
    (HERE / "home.html").write_text(html)
    content = "<!-- wp:html -->\n" + html + "\n<!-- /wp:html -->"
    ex = requests.get("https://spn-net.fr/wp-json/wp/v2/pages",
                      params={"slug": SLUG, "_fields": "id"}, auth=AUTH, timeout=30).json()
    payload = {"title": "Accueil (aperçu)", "slug": SLUG, "status": "publish", "content": content,
               "template": "elementor_header_footer",
               "meta": {"slim_seo": {"title": SS_TITLE, "description": SS_DESC, "noindex": True}}}
    if ex:
        r = requests.post(f"https://spn-net.fr/wp-json/wp/v2/pages/{ex[0]['id']}", auth=AUTH, timeout=90, json=payload)
    else:
        r = requests.post("https://spn-net.fr/wp-json/wp/v2/pages", auth=AUTH, timeout=90, json=payload)
    r.raise_for_status()
    print("✓ Aperçu accueil publié :", r.json().get("link"))


if __name__ == "__main__":
    main()
