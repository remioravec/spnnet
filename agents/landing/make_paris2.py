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
"""

# --- 2) Hero (message-match requête locale) ---
REPL = [
    ('<span class="eyebrow">Entretien de bureaux · Paris & Île-de-France</span>',
     '<span class="eyebrow">Nettoyage de bureaux · Paris 2ᵉ — 75002</span>'),
    ("<h1>Entretien de <em>bureaux</em> à Paris, sans jamais gêner votre activité</h1>",
     "<h1>Société de <em>nettoyage de bureaux</em> à Paris 2ᵉ (75002)</h1>"),
    ('<p class="lead">Sociétés, PME et startups : un nettoyage de bureaux régulier et fiable, réalisé <b>tôt le matin ou en soirée</b>. Un interlocuteur dédié, des équipes formées et certifiées ISO 45001 — devis sous 24h.</p>',
     '<p class="lead">De la <b>Bourse</b> au <b>Sentier</b>, nous entretenons les bureaux, sièges et espaces de coworking du 2ᵉ arrondissement. Interventions <b>tôt le matin ou en soirée</b>, sans gêner votre activité. Équipe dédiée certifiée ISO 45001 — devis sous 24h.</p>'),
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
      <p>Ces bureaux, souvent installés dans des <b>immeubles haussmanniens</b> aux accès contraints (pas toujours de monte-charge, horaires de gardiennage, plateaux occupés en continu), exigent un prestataire réactif et discret. Nos équipes interviennent <b>avant 9h ou après 18h</b>, avant l'arrivée ou après le départ de vos collaborateurs, pour un résultat impeccable sans perturber votre activité.</p>
      <p>Sièges sociaux, agences de communication, cabinets de conseil, studios et coworkings : nous adaptons la fréquence et le protocole à chaque type de locaux du 2ᵉ.</p>
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
    # CSS
    assert "</style>" in html
    html = html.replace("</style>", CSS + "</style>", 1)
    # Hero + zone
    for old, new in REPL:
        assert old in html, f"anchor introuvable: {old[:50]}"
        html = html.replace(old, new, 1)
    # Section locale avant WHY US
    assert "<!-- ============ WHY US ============ -->" in html
    html = html.replace("<!-- ============ WHY US ============ -->", LOCAL, 1)
    # FAQ : remplacer le bloc des 6 <details> par une FAQ locale
    start = html.index(FAQ_OLD_START)
    end = html.index("</details>", html.index("bien-être et à la sécurité de nos agents")) + len("</details>")
    faq_new = (
        '    <details class="acc"><summary>Intervenez-vous dans tout le 2ᵉ arrondissement (75002) ?<span class="pl">+</span></summary><div class="body">Oui, dans l\'ensemble du 2ᵉ : quartier de la Bourse, Sentier, Montorgueil, rue du Mail, Vivienne, Gaillon et les Grands Boulevards. Nous couvrons aussi tout Paris et l\'Île-de-France.</div></details>\n'
        '    <details class="acc"><summary>Pouvez-vous nettoyer nos bureaux en dehors des heures d\'ouverture ?<span class="pl">+</span></summary><div class="body">Absolument. Nos équipes interviennent tôt le matin (avant 9h) ou en soirée (après 18h), et le week-end si besoin, pour ne jamais perturber votre activité ni gêner vos collaborateurs.</div></details>\n'
        '    <details class="acc"><summary>Gérez-vous les immeubles haussmanniens et les accès difficiles ?<span class="pl">+</span></summary><div class="body">Oui. Beaucoup de bureaux du 2ᵉ sont dans des immeubles anciens, parfois sans monte-charge et avec gardiennage. Nos agents sont habitués à ces contraintes d\'accès et s\'organisent en conséquence.</div></details>\n'
        '    <details class="acc"><summary>Travaillez-vous avec les startups et coworkings du Sentier ?<span class="pl">+</span></summary><div class="body">Oui, c\'est un profil de client que nous connaissons bien : contrats souples, fréquences ajustables et interventions rapides adaptées aux espaces partagés et aux équipes en croissance.</div></details>\n'
        '    <details class="acc"><summary>Sous quel délai vais-je recevoir mon devis ?<span class="pl">+</span></summary><div class="body">Votre devis est gratuit, sans engagement, et transmis sous 24h ouvrées après l\'étude de votre besoin (souvent précédée d\'une courte visite sur site).</div></details>\n'
        '    <details class="acc"><summary>Êtes-vous une entreprise certifiée ?<span class="pl">+</span></summary><div class="body">SPN NET est certifiée ISO 45001 par DEKRA (santé-sécurité au travail) et a obtenu la médaille d\'argent EcoVadis 2025 (top 15 % RSE), fort de 30 ans d\'expérience et de +350 clients.</div></details>'
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
              '{"@type":"Question","name":"Etes-vous une entreprise certifiee ?","acceptedAnswer":{"@type":"Answer","text":"SPN NET est certifiee ISO 45001 (DEKRA) et medaille d\'argent EcoVadis 2025, avec 30 ans d\'experience."}}'
              ']}')
    html = html[:ld_start] + faq_ld + html[ld_end:]

    (HERE / "paris2.html").write_text(html)

    # Publier (noindex, canvas)
    content = "<!-- wp:html -->\n" + html + "\n<!-- /wp:html -->"
    ex = requests.get("https://spn-net.fr/wp-json/wp/v2/pages",
                      params={"slug": SLUG, "_fields": "id"}, auth=AUTH, timeout=30).json()
    payload = {"title": "Nettoyage bureaux Paris 2 (aperçu)", "slug": SLUG, "status": "publish",
               "content": content, "template": "elementor_canvas",
               "meta": {"slim_seo": {"title": SS_TITLE, "description": SS_DESC, "noindex": True}}}
    if ex:
        r = requests.post(f"https://spn-net.fr/wp-json/wp/v2/pages/{ex[0]['id']}", auth=AUTH, timeout=60, json=payload)
    else:
        r = requests.post("https://spn-net.fr/wp-json/wp/v2/pages", auth=AUTH, timeout=60, json=payload)
    r.raise_for_status()
    print("✓ Aperçu publié :", r.json().get("link"))


if __name__ == "__main__":
    main()
