#!/usr/bin/env python3
"""Déploie le modèle 'nettoyage de bureaux' (CRO + GEO + humain + maillage) sur
les pages locales EXISTANTES (arrondissements + départements), en INDEXABLE.

Mécanisme validé (réversible) : on écrit le modèle en post_content, on désactive
le builder Elementor (_elementor_edit_mode=""), template en-tête/pied de page.
La data Elementor d'origine est conservée (réactivable en remettant "builder").

Chaque page a un contenu local UNIQUE (cf. zones_data.py) → pas de duplicate.

Usage :
  python3 agents/landing/make_zone.py paris-3 paris-8      # zones ciblées
  python3 agents/landing/make_zone.py --all                # toutes les zones
  python3 agents/landing/make_zone.py --restore paris-3    # restaure la page Elementor
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

import requests

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from make_paris2 import CSS, PROMISE, PULL, TEAM, TEAMCUE, HEADFIX, _CK, _IMG  # noqa: E402
from zones_data import ALL_ZONES  # noqa: E402

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
BASE_HTML = (HERE / "lp.html").read_text()
API = "https://spn-net.fr/wp-json/wp/v2/pages"
BAK_DIR = pathlib.Path(os.environ.get("SPN_BAK", "/tmp/spn_bak"))
BAK_DIR.mkdir(parents=True, exist_ok=True)

NOINDEX_SCRIPT = ('<script>try{document.head.insertAdjacentHTML(\'beforeend\','
                  '\'<meta name="robots" content="noindex,nofollow,noarchive">\');}catch(e){}</script>')

# ---- anchors du modèle (identiques à make_paris2) ----
A_EYEBROW = '<span class="eyebrow">Entretien de bureaux · Paris & Île-de-France</span>'
A_H1 = "<h1>Entretien de <em>bureaux</em> à Paris, sans jamais gêner votre activité</h1>"
A_LEAD = ('<p class="lead">Sociétés, PME et startups : un nettoyage de bureaux régulier et fiable, '
          'réalisé <b>tôt le matin ou en soirée</b>. Un interlocuteur dédié, des équipes formées et '
          'certifiées ISO 45001 — devis sous 24h.</p>')
A_ZONEP = ("<p>Basés dans les Hauts-de-Seine, nous réagissons vite à Paris comme en proche couronne. "
           "Une présence locale et des équipes mobiles dans les 20 arrondissements et l'ensemble des "
           "départements franciliens.</p>")

# ---- Carrousel de réalisations dans le hero (home + pages mères) ----
_IMGB = "https://spn-net.fr/wp-content/uploads/2026/"
_CAR_SLIDES = [
    (_IMGB + "01/tertiaire-1-1024x683.jpg", "Bureaux & Tertiaire", "Entretien de bureaux · Paris"),
    (_IMGB + "01/hotel-1024x683.jpg", "Hôtellerie & Restauration", "Parties communes & cuisines"),
    (_IMGB + "01/sante-1024x683.jpg", "Santé & Médical", "Bionettoyage"),
    (_IMGB + "01/commerce-1024x683.jpg", "Commerce & Retail", "Surfaces de vente & vitrines"),
    (_IMGB + "01/copro-1024x683.jpg", "Copropriété & Habitat", "Parties communes d'immeubles"),
    (_IMGB + "03/ascenseurs-et-escalators-e1773133478487.webp", "Ascenseurs & Escalators", "Métal, inox & vitrage"),
]

CAROUSEL_CSS = (
    ".spn-lp .hero-carousel{position:relative;border-radius:22px;overflow:hidden;box-shadow:var(--shadow);aspect-ratio:4/3;background:var(--ink-2)}"
    ".spn-lp .hero-carousel .slide{position:absolute;inset:0;opacity:0;transition:opacity 1s ease}"
    ".spn-lp .hero-carousel .slide.on{opacity:1}"
    ".spn-lp .hero-carousel .slide img{width:100%;height:100%;object-fit:cover}"
    ".spn-lp .hero-carousel .slide::after{content:\"\";position:absolute;inset:0;background:linear-gradient(transparent 50%,rgba(20,22,27,.82))}"
    ".spn-lp .hero-carousel .cap{position:absolute;left:22px;right:22px;bottom:20px;z-index:2;color:#fff}"
    ".spn-lp .hero-carousel .cap b{font-family:'Fraunces',serif;font-weight:600;font-size:1.2rem;display:block;line-height:1.15}"
    ".spn-lp .hero-carousel .cap small{font-size:.85rem;color:rgba(255,255,255,.85)}"
    ".spn-lp .hero-carousel .cbadge{position:absolute;top:16px;left:16px;z-index:3;background:rgba(255,255,255,.94);color:var(--ink);font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:6px 13px;border-radius:999px}"
    ".spn-lp .hero-carousel .dots{position:absolute;top:18px;right:16px;z-index:3;display:flex;gap:6px}"
    ".spn-lp .hero-carousel .dots button{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.55);border:none;cursor:pointer;padding:0;transition:.25s}"
    ".spn-lp .hero-carousel .dots button.on{background:#fff;width:22px;border-radius:4px}"
    "@media(max-width:880px){.spn-lp .hero-carousel{aspect-ratio:16/10}}"
)

CAROUSEL_JS = ('<script>(function(){var r=document.querySelector(".spn-lp");if(!r)return;var c=r.querySelector("#heroCar");'
               'if(!c)return;var s=c.querySelectorAll(".slide"),d=c.querySelectorAll(".dots button"),i=0,t;'
               'function go(n){s[i].classList.remove("on");if(d[i])d[i].classList.remove("on");i=(n+s.length)%s.length;'
               's[i].classList.add("on");if(d[i])d[i].classList.add("on");}function play(){t=setInterval(function(){go(i+1);},4200);}'
               'function stop(){clearInterval(t);}for(var k=0;k<d.length;k++){(function(k){d[k].addEventListener("click",'
               'function(){go(k);stop();play();});})(k);}c.addEventListener("mouseenter",stop);c.addEventListener("mouseleave",play);'
               'document.addEventListener("visibilitychange",function(){document.hidden?stop():play();});play();})();</script>')


def carousel_html():
    slides = ""
    for k, (img, title, sub) in enumerate(_CAR_SLIDES):
        on = " on" if k == 0 else ""
        lazy = "" if k == 0 else 'loading="lazy" '
        slides += (f'<div class="slide{on}"><img src="{img}" alt="{title} — réalisation SPN NET" {lazy}/>'
                   f'<div class="cap"><b>{title}</b><small>{sub}</small></div></div>')
    dots = "".join(f'<button class="{"on" if k == 0 else ""}" aria-label="Vue {k + 1}"></button>' for k in range(len(_CAR_SLIDES)))
    return ('<div class="hero-carousel reveal" id="heroCar"><span class="cbadge">Nos réalisations</span>'
            + slides + '<div class="dots">' + dots + '</div></div>')


def apply_carousel(h):
    """Remplace le formulaire du hero par le carrousel ; déplace l'ancre #devis vers le CTA final."""
    s = h.index('<div class="lead-card reveal" id="devis">')
    e = h.index("<!-- ============ CLIENTS LOGOS")
    h = h[:s] + carousel_html() + "\n</div></div>\n\n" + h[e:]
    h = h.replace('<div class="cta-final">', '<div class="cta-final" id="devis">', 1)
    h = h.replace("</style>", CAROUSEL_CSS + "</style>", 1)
    return h


def facts(z):
    return ('<div class="facts reveal"><h3>' + _CK + ' SPN NET — l\'essentiel</h3><dl>'
            '<div class="row"><dt>Activité</dt><dd>Nettoyage &amp; entretien de bureaux</dd></div>'
            f'<div class="row"><dt>Zone desservie</dt><dd>{z["zone"]}</dd></div>'
            '<div class="row"><dt>Expérience</dt><dd>30 ans · +350 clients</dd></div>'
            '<div class="row"><dt>Certifications</dt><dd>ISO 45001 · EcoVadis Argent</dd></div>'
            '<div class="row"><dt>Note clients</dt><dd>4,8/5 — 48 avis Google</dd></div>'
            '<div class="row"><dt>Horaires d\'intervention</dt><dd>Avant 9h, après 18h, week-end</dd></div>'
            '<div class="row"><dt>Devis</dt><dd>Gratuit, transmis sous 24h</dd></div>'
            '<div class="row"><dt>Contact</dt><dd><a href="tel:+33149462240" data-tel>01 49 46 22 40</a> · Bagneux (92)</dd></div>'
            '</dl></div>')


SERVICES = (
    '  <div style="margin-top:40px" class="reveal">\n'
    '    <h3 style="font-family:\'Fraunces\',serif;font-weight:600;font-size:1.4rem;margin-bottom:14px">Nos prestations de nettoyage de bureaux</h3>\n'
    '    <div style="overflow-x:auto"><table class="tbl">\n'
    '      <thead><tr><th>Prestation</th><th>Ce que nous faisons</th><th>Fréquence type</th></tr></thead>\n'
    '      <tbody>\n'
    '        <tr><td>Entretien des bureaux</td><td>Dépoussiérage, surfaces, corbeilles, désinfection des points de contact</td><td>Quotidien / 3× sem.</td></tr>\n'
    '        <tr><td>Sanitaires</td><td>Nettoyage complet, désinfection et réassort des consommables</td><td>Quotidien</td></tr>\n'
    '        <tr><td>Sols</td><td>Aspiration, lavage, décapage et cristallisation selon le revêtement</td><td>Selon protocole</td></tr>\n'
    '        <tr><td>Vitrerie</td><td>Surfaces vitrées intérieures, cloisons, portes et vitrines</td><td>Mensuel / trimestriel</td></tr>\n'
    '        <tr><td>Salles de réunion &amp; communs</td><td>Remise en ordre, tisanerie/cuisine, espace d\'accueil</td><td>Quotidien</td></tr>\n'
    '        <tr><td>Remise en état</td><td>Grand nettoyage, fin de chantier, avant/après emménagement</td><td>Ponctuel</td></tr>\n'
    '      </tbody>\n    </table></div>\n  </div>\n')


def local(z):
    chips = "".join(f"<span>{q}</span>" for q in z["quartiers"])
    return (
        '\n<!-- ============ CONTENU LOCAL ============ -->\n'
        '<div class="sec local"><div class="wrap">\n'
        '  <div class="sec-head reveal" style="max-width:820px;text-align:left;margin:0 0 30px">'
        f'<span class="eyebrow">Expertise locale · {z["short"]}</span>'
        f'<h2>Le nettoyage de bureaux à {z["name"]}</h2></div>\n'
        + facts(z) +
        '\n  <div class="grid">\n    <div class="reveal">\n'
        f'      <p>{z["p1"]}</p>\n'
        f'      <p>{z["p2"]}</p>\n'
        '      <p>Sièges, PME, cabinets, studios et coworkings : nous adaptons la fréquence et le protocole à '
        'chaque type de locaux. Voir aussi notre <a href="https://spn-net.fr/tertiaire/">pôle nettoyage tertiaire &amp; bureaux</a>.</p>\n'
        f'      <div class="qtiers">{chips}</div>\n'
        '    </div>\n'
        '    <div class="side reveal">\n'
        f'      <h3>Pourquoi {z["name"]} nous choisit</h3>\n'
        '      <ul class="hero-points" style="margin:0">\n'
        '        <li>Intervention avant 9h ou après 18h</li>\n'
        '        <li>Équipes formées &amp; fidélisées</li>\n'
        '        <li>Un interlocuteur dédié, joignable</li>\n'
        '        <li>Devis sous 24h, sans engagement</li>\n'
        '      </ul>\n    </div>\n  </div>\n'
        + SERVICES +
        '</div></div>\n\n<!-- ============ WHY US ============ -->')


def links(z):
    cards = ""
    for slug, label, sub in z["neighbors"]:
        cards += (f'    <a class="card" href="https://spn-net.fr/{slug}/"><b>{label} <span class="ar">→</span></b>'
                  f'<small>{sub}</small></a>\n')
    cards += ('    <a class="card" href="https://spn-net.fr/tertiaire/"><b>Pôle Tertiaire &amp; bureaux <span class="ar">→</span></b><small>Notre expertise bureaux, tous secteurs</small></a>\n'
              '    <a class="card" href="https://spn-net.fr/92-hauts-de-seine/"><b>Hauts-de-Seine (92) <span class="ar">→</span></b><small>Notre base — proximité immédiate</small></a>\n')
    return (
        '\n<!-- ============ MAILLAGE INTERNE ============ -->\n'
        '<div class="sec links"><div class="wrap">\n'
        '  <div class="sec-head reveal"><span class="eyebrow c">Zones &amp; prestations liées</span>'
        f'<h2>Nettoyage de bureaux autour de {z["name"]}</h2>'
        '<p>Nous intervenons dans les secteurs voisins et sur toutes vos typologies de locaux.</p></div>\n'
        '  <div class="grid reveal">\n' + cards + '  </div>\n</div></div>\n\n<!-- ============ FINAL CTA ============ -->')


def faq_html(z):
    chips = ", ".join(z["quartiers"][:5])
    items = [
        (f"Intervenez-vous dans tout le secteur de {z['name']} ?",
         f"Oui, dans l'ensemble du secteur : {chips}… ainsi que dans tout Paris et l'Île-de-France."),
        ("Pouvez-vous nettoyer nos bureaux en dehors des heures d'ouverture ?",
         "Absolument. Nos équipes interviennent tôt le matin (avant 9h) ou en soirée (après 18h), et le week-end si besoin, pour ne pas perturber votre activité."),
        ("Combien coûte le nettoyage de bureaux ?",
         "Le tarif dépend de la surface, de la fréquence et des prestations retenues (entretien courant, sanitaires, vitrerie, sols, remise en état). Il n'y a pas de forfait standard imposé : le devis est gratuit et personnalisé, sous 24h."),
        (f"Quelle société de nettoyage de bureaux choisir à {z['name']} ?",
         "Regardez la proximité (réactivité), les certifications (ISO 45001), les avis clients réels et la capacité à intervenir en horaires décalés. SPN NET réunit ces critères : 4,8/5 sur 48 avis Google, ISO 45001, EcoVadis Argent, intervention soir et matin, interlocuteur dédié."),
        ("À quelle fréquence faut-il nettoyer des bureaux ?",
         "La fréquence dépend de votre surface, de votre effectif et de votre activité. Elle est définie avec vous lors du devis, d'un passage plusieurs fois par semaine à un entretien plus ponctuel."),
        ("Comment se déroule le nettoyage des bureaux ?",
         "Après un état des lieux, un protocole est défini pour vos locaux (postes de travail, sanitaires, sols, parties communes) puis réalisé par une équipe dédiée, aux horaires convenus. Les modalités précises figurent dans votre devis."),
        ("Vos prestations s'inscrivent-elles dans une démarche RSE ?",
         "Oui : SPN NET a obtenu la médaille d'argent EcoVadis 2025 (top 15 % RSE) et est certifiée ISO 45001. Les protocoles et produits adaptés à vos locaux sont définis lors de l'étude de votre besoin."),
        ("Proposez-vous la vitrerie et l'entretien des parties communes ?",
         "Oui : vitrerie, sols, sanitaires, salles de réunion et parties communes figurent parmi les prestations de nettoyage de bureaux, en complément de l'entretien courant."),
        ("Faites-vous les nettoyages ponctuels (remise en état, fin de chantier) ?",
         "Oui, nous réalisons aussi des interventions ponctuelles comme la remise en état ou le nettoyage de fin de chantier, en complément de l'entretien régulier."),
        ("Intervenez-vous pour plusieurs sites ?",
         "Pour un besoin sur plusieurs sites, précisez-le dans votre demande : nous étudions chaque situation et vous répondons sous 24h."),
        ("Le devis engage-t-il à quelque chose ?",
         "Non : le devis est gratuit et sans engagement. Les conditions du contrat d'entretien sont définies avec vous avant toute intervention."),
    ]
    html = ""
    for q, a in items:
        html += (f'    <details class="acc"><summary>{q}<span class="pl">+</span></summary>'
                 f'<div class="body">{a}</div></details>\n')
    return html.rstrip("\n"), items


def strip_accents(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def faq_schema(items):
    q = []
    for name, ans in items:
        q.append('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
                 % (strip_accents(name).replace('"', "'"), strip_accents(ans).replace('"', "'")))
    return '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + ",".join(q) + ']}'


def build(z):
    h = BASE_HTML
    # indexable : retire l'injecteur noindex + la barre logo/tel
    h = h.replace(NOINDEX_SCRIPT, "", 1)
    s = h.index("<!-- ============ TOP STRIP ============ -->")
    e = h.index("<!-- ============ HERO ============ -->")
    h = h[:s] + h[e:]
    # CSS enrichi
    h = h.replace("</style>", CSS + "</style>", 1)
    # hero
    h = h.replace(A_EYEBROW, f'<span class="eyebrow">{z["eyebrow"]}</span>', 1)
    h = h.replace(A_H1, f'<h1>{z["h1"]}</h1>', 1)
    h = h.replace(A_LEAD, f'<p class="lead">{z["lead"]}</p>', 1)
    # zone paragraph
    zp = (f'<p>Notre base dans les Hauts-de-Seine nous rend très réactifs sur {z["name"]}. '
          f'Nous intervenons dans {z["zone"]} ({", ".join(z["quartiers"][:4])}…) et, plus largement, '
          "dans tout Paris et l'Île-de-France.</p>")
    h = h.replace(A_ZONEP, zp, 1)
    # promesse + local (avec facts + services) avant WHY
    h = h.replace("<!-- ============ WHY US ============ -->", PROMISE + local(z), 1)
    # citation avant avis
    h = h.replace("<!-- ============ AVIS GOOGLE", PULL + "\n<!-- ============ AVIS GOOGLE", 1)
    # équipe avant réalisations
    h = h.replace("<!-- ============ RÉALISATIONS ============ -->", TEAM, 1)
    # team-cue après trust-row
    tr = 'ISO 45001</b></span></div>\n    </div>'
    h = h.replace(tr, 'ISO 45001</b></span></div>\n      ' + TEAMCUE + '\n    </div>', 1)
    # maillage avant CTA final
    h = h.replace("<!-- ============ FINAL CTA ============ -->", links(z), 1)
    # WHY sec-head orienté bénéfice
    h = h.replace(
        '<span class="eyebrow c">Pourquoi SPN NET</span><h2>Propreté, rigueur et engagement depuis 30 ans</h2><p>Une entreprise à taille humaine, deux priorités : le client et le salarié.</p>',
        '<span class="eyebrow c">Ce que vous y gagnez</span><h2>Moins de tracas, des locaux toujours nickel</h2><p>Une entreprise à taille humaine qui traite vos bureaux comme les siens — et vos équipes avec le même soin.</p>'
        '<div class="gains" style="margin-top:18px">'
        '<span>' + _CK + ' Zéro relance à faire</span>'
        '<span>' + _CK + ' Même équipe, chaque semaine</span>'
        '<span>' + _CK + ' Contrôle qualité régulier</span></div>', 1)
    # FAQ : remplace le bloc générique de lp.html
    faq_start = h.index('    <details class="acc"><summary>Quelle est votre zone')
    faq_end = h.index("</details>", h.index("bien-être et à la sécurité de nos agents")) + len("</details>")
    fhtml, fitems = faq_html(z)
    h = h[:faq_start] + fhtml + h[faq_end:]
    # FAQ schema : remplace le FAQPage de lp.html
    ld_start = h.index('{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[')
    ld_end = h.index("]}", ld_start) + len("]}")
    h = h[:ld_start] + faq_schema(fitems) + h[ld_end:]
    # breadcrumb + headfix avant fermeture
    bc = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
          '"itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":"https://spn-net.fr/"},'
          '{"@type":"ListItem","position":2,"name":"Nettoyage de bureaux","item":"https://spn-net.fr/tertiaire/"},'
          f'{{"@type":"ListItem","position":3,"name":"{strip_accents(z["zone"])}"}}]}}</script>')
    h = h.rstrip()[:-len("</section>")] + bc + HEADFIX + "\n</section>\n"
    return h


def get_page_id(slug):
    r = requests.get(API, params={"slug": slug, "_fields": "id"}, auth=AUTH, timeout=30).json()
    return r[0]["id"] if r else None


def deploy(slug, z, builder=build, prefix="zone"):
    pid = get_page_id(slug)
    if not pid:
        return f"  ✗ {slug}: page introuvable"
    # sauvegarde (réversible)
    bakf = BAK_DIR / f"{slug}.json"
    if not bakf.exists():  # ne jamais écraser la sauvegarde d'origine
        try:
            o = requests.get(f"{API}/{pid}", params={"context": "edit", "_fields": "content,template,meta"},
                             auth=AUTH, timeout=30).json()
            content, template = o["content"]["raw"], o.get("template", "")
            em = o["meta"].get("_elementor_edit_mode")
        except Exception:  # noqa: BLE001  (certaines pages 500 en edit avec content)
            o = requests.get(f"{API}/{pid}", params={"context": "edit", "_fields": "template,meta"},
                             auth=AUTH, timeout=30).json()
            content, template = "", o.get("template", "")
            em = o.get("meta", {}).get("_elementor_edit_mode")
        bakf.write_text(json.dumps({"id": pid, "content": content, "template": template, "edit_mode": em}))
    html = builder(z)
    (HERE / f"{prefix}-{slug}.html").write_text(html)
    payload = {"content": "<!-- wp:html -->\n" + html + "\n<!-- /wp:html -->",
               "template": "elementor_header_footer",
               "meta": {"_elementor_edit_mode": "", "slim_seo": {"title": z["title"], "description": z["desc"], "noindex": False}}}
    r = requests.post(f"{API}/{pid}", auth=AUTH, timeout=90, json=payload)
    r.raise_for_status()
    return f"  ✓ {slug} → {r.json().get('link')}"


def restore(slug):
    f = BAK_DIR / f"{slug}.json"
    if not f.exists():
        return f"  ✗ {slug}: pas de sauvegarde"
    b = json.loads(f.read_text())
    r = requests.post(f"{API}/{b['id']}", auth=AUTH, timeout=90, json={
        "content": b["content"], "template": b["template"],
        "meta": {"_elementor_edit_mode": b["edit_mode"] or "builder"}})
    r.raise_for_status()
    return f"  ↩ {slug} restauré"


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return
    if args[0] == "--restore":
        for slug in args[1:]:
            print(restore(slug))
        return
    slugs = list(ALL_ZONES.keys()) if args[0] == "--all" else args
    for slug in slugs:
        z = ALL_ZONES.get(slug)
        if not z:
            print(f"  ? {slug}: pas de données"); continue
        try:
            print(deploy(slug, z))
        except Exception as ex:  # noqa: BLE001
            print(f"  ✗ {slug}: {ex}")


if __name__ == "__main__":
    main()
