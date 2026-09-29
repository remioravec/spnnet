#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Brouillon de mise à jour de /paris-17/ (operationnel-contenu, brief du 25/08/2026).

Reprend le gabarit zone (make_zone.build) — sections conservées mot pour mot —
et applique les 5 modifications du brief + des infographies :
  1. Title/meta réécrits.
  2. Paragraphe d'ouverture prix dans « Le nettoyage de bureaux à Paris 17e ».
  3. Ligne « Budget indicatif 17e » dans l'encadré l'essentiel.
  4. 4e colonne « Fourchette indicative » au tableau des prestations.
  5. Nouveau H2 « Combien coûte le nettoyage de bureaux dans le 17e »
     (grille surface × fréquence + infographie « 3 variables » + 6 facteurs).
  6. Phrase d'ancrage local dans « Nos clients parlent pour nous ».
  7. FAQ : réponse prix réécrite + 2 questions (tarif horaire, consommables),
     répercutées dans le JSON-LD FAQPage.

Les cellules de prix restent des PLACEHOLDERS visibles ([A2]..[C5], [HORAIRE],
[MOIS ANNÉE]) : aucun tarif SPN n'est inventé. Un repère marché (France Clean,
relevé du 25/08/2026) est joint, étiqueté comme tel.

Publie en BROUILLON (status=draft, noindex) sur un slug dédié — la page live
/paris-17/ n'est jamais touchée.

Usage : python3 agents/landing/make_paris17_maj.py
"""
from __future__ import annotations

import os
import sys
import pathlib

import requests

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import make_zone as mz  # noqa: E402
from zones_data import ALL_ZONES  # noqa: E402

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
API = "https://spn-net.fr/wp-json/wp/v2/pages"
SRC_SLUG = "paris-17"
DRAFT_SLUG = "paris-17-brouillon-maj"

NEW_TITLE = "Nettoyage de bureaux Paris 17e — devis sous 24h | SPN NET"
NEW_DESC = ("Nettoyage de bureaux dans le 17e : Batignolles, Clichy, Palais des Congrès. "
            "Tarifs indicatifs par surface, intervention avant 9h ou après 18h. Devis sous 24h.")

_IMG = "https://spn-net.fr/wp-content/uploads/2026/01/tertiaire-1-1024x683.jpg"


def chip(t):
    return '<span class="tbc">' + t + '</span>'


# ---- 4) tableau des prestations : 4e colonne « Fourchette indicative » ----
SERVICES_4COL = (
    '  <div style="margin-top:40px" class="reveal">\n'
    '    <h3 style="font-family:\'Fraunces\',serif;font-weight:600;font-size:1.4rem;margin-bottom:14px">Nos prestations de nettoyage de bureaux</h3>\n'
    '    <div style="overflow-x:auto"><table class="tbl">\n'
    '      <thead><tr><th>Prestation</th><th>Ce que nous faisons</th><th>Fréquence type</th><th>Fourchette indicative</th></tr></thead>\n'
    '      <tbody>\n'
    '        <tr><td>Entretien des bureaux</td><td>Dépoussiérage, surfaces, corbeilles, désinfection des points de contact</td><td>Quotidien / 3× sem.</td><td>Inclus au forfait de base</td></tr>\n'
    '        <tr><td>Sanitaires</td><td>Nettoyage complet, désinfection et réassort des consommables</td><td>Quotidien</td><td>Inclus — consommables en option</td></tr>\n'
    '        <tr><td>Sols</td><td>Aspiration, lavage, décapage et cristallisation selon le revêtement</td><td>Selon protocole</td><td>Décapage et cristallisation en supplément</td></tr>\n'
    '        <tr><td>Vitrerie</td><td>Surfaces vitrées intérieures, cloisons, portes et vitrines</td><td>Mensuel / trimestriel</td><td>Chiffrée à part, selon la surface vitrée</td></tr>\n'
    '        <tr><td>Salles de réunion &amp; communs</td><td>Remise en ordre, tisanerie/cuisine, espace d\'accueil</td><td>Quotidien</td><td>Inclus au forfait de base</td></tr>\n'
    '        <tr><td>Remise en état</td><td>Grand nettoyage, fin de chantier, avant/après emménagement</td><td>Ponctuel</td><td>Devis dédié</td></tr>\n'
    '      </tbody>\n    </table></div>\n  </div>\n')


# ---- 7) FAQ custom paris-17 : Q3 réécrite + 2 questions ajoutées ----
_ORIG_FAQ = mz.faq_html  # référence avant monkeypatch


def faq_html_p17(z):
    _, base = _ORIG_FAQ(z)  # 11 items d'origine
    items = list(base)
    # Q3 = « Combien coûte le nettoyage de bureaux ? » → réponse chiffrée (placeholders)
    items[2] = (
        "Combien coûte le nettoyage de bureaux ?",
        "Pour un plateau de 100 à 300 m² dans le 17e, comptez autour de [B3] € par mois pour "
        "trois passages hebdomadaires. En dessous de 100 m², le budget démarre vers [A3] € mensuels ; "
        "au-delà de 300 m², comptez à partir de [C3] €. Ces montants varient selon les sols, la surface "
        "vitrée, les horaires d'intervention et les consommables retenus. Le devis est gratuit, "
        "personnalisé et transmis sous 24 heures.")
    items.append((
        "Quel est le tarif horaire d'un agent de nettoyage à Paris ?",
        "Le nettoyage de bureaux se chiffre rarement à l'heure : la prestation est établie au forfait "
        "mensuel, calculé sur la surface, la fréquence et le protocole. Ramené à l'heure d'intervention, "
        "cela représente [HORAIRE] € dans le 17e, encadrement, matériel et contrôle qualité compris. "
        "C'est ce qui distingue un contrat d'entretien d'une prestation facturée au temps passé."))
    items.append((
        "Les consommables sont-ils compris dans le tarif ?",
        "Au choix. Papier, savon, sacs et essuie-mains peuvent être intégrés au forfait mensuel — vous "
        "n'avez plus à les commander ni à surveiller les stocks — ou rester à votre charge si vous "
        "disposez déjà d'un fournisseur. Les deux options figurent sur le devis, chiffrées séparément."))
    html = ""
    for q, a in items:
        html += (f'    <details class="acc"><summary>{q}<span class="pl">+</span></summary>'
                 f'<div class="body">{a}</div></details>\n')
    return html.rstrip("\n"), items


# ---- 5) Nouveau H2 « Combien coûte le nettoyage de bureaux dans le 17e » ----
def _ic(p):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            'stroke-linecap="round" stroke-linejoin="round">' + p + '</svg>')

FACTORS = [
    (_ic('<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 3v18"/>'),
     "La nature des sols",
     "Une moquette s'aspire, un marbre se lave et se cristallise, un vinyle se décape. Le revêtement change le temps passé et le matériel mobilisé."),
    (_ic('<rect x="3" y="3" width="18" height="18" rx="1"/><path d="M3 12h18M12 3v18"/>'),
     "La surface vitrée",
     "Cloisons intérieures, verrières et façades de bureaux récents demandent une intervention distincte de l'entretien courant."),
    (_ic('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>'),
     "Les horaires",
     "Une intervention avant 9h ou après 18h relève d'une organisation différente d'un passage en journée. Le week-end également."),
    (_ic('<path d="M6 2h9l3 3v17H6z"/><path d="M9 7h6M9 11h6M9 15h4"/>'),
     "Les consommables",
     "Papier, savon, sacs : leur fourniture et leur réassort peuvent être intégrés au forfait ou facturés à part, selon ce que vous préférez."),
    (_ic('<path d="M3 21h18M6 21V7l6-4 6 4v14"/><path d="M10 21v-5h4v5"/>'),
     "L'accès aux locaux",
     "Étages sans ascenseur, contrôle d'accès, local technique éloigné : autant de minutes qui s'ajoutent à chaque passage."),
    (_ic('<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.2"/><path d="M3 20c0-3 2.7-5 6-5s6 2 6 5M15 20c0-2 1-3.5 3-3.5s3 1.5 3 3.5"/>'),
     "La densité d'occupation",
     "Un plateau de 200 m² occupé par 40 personnes ne se salit pas comme le même plateau occupé par 12."),
]


def price_section():
    factors = ""
    for ic, h, p in FACTORS:
        factors += f'    <div class="pf reveal"><span class="pf-ic">{ic}</span><b>{h}</b><span>{p}</span></div>\n'
    grid_head = ('<thead><tr><th>Surface des bureaux</th><th>2 passages / sem.</th>'
                 '<th>3 passages / sem.</th><th>5 passages / sem.</th></tr></thead>')
    def r(lbl, a, b, c):
        return (f'<tr><td><b>{lbl}</b></td><td>{a}</td><td>{b}</td><td>{c}</td></tr>')
    grid = (
        '<div style="overflow-x:auto"><table class="tbl ptable">' + grid_head + '<tbody>'
        + r("Moins de 100 m²", chip("[A2]") + " € / mois", chip("[A3]") + " € / mois", chip("[A5]") + " € / mois")
        + r("100 à 300 m²", chip("[B2]") + " € / mois", chip("[B3]") + " € / mois", chip("[B5]") + " € / mois")
        + r("300 à 600 m²", chip("[C2]") + " € / mois", chip("[C3]") + " € / mois", chip("[C5]") + " € / mois")
        + r("Plus de 600 m²", "Sur étude", "Sur étude", "Sur étude")
        + '</tbody></table></div>')
    return (
        '\n<!-- ============ PRIX (NOUVEAU H2) ============ -->\n'
        '<div class="sec price"><div class="wrap">\n'
        '  <div class="sec-head reveal" style="max-width:840px;text-align:left;margin:0 0 26px">'
        '<span class="eyebrow">Budget · Paris 17e</span>'
        '<h2>Combien coûte le nettoyage de bureaux dans le 17e</h2>'
        '<p>Il n\'existe pas de forfait standard en nettoyage de bureaux : le prix se calcule sur trois '
        'variables — la surface à traiter, le nombre de passages hebdomadaires et le protocole retenu. '
        'Voici les ordres de grandeur que nous constatons sur les bureaux du 17e arrondissement, mis à '
        'jour en ' + chip("[MOIS ANNÉE]") + '.</p></div>\n'
        # infographie 3 variables + photo
        '  <div class="pgrid2 reveal">\n'
        '    <div class="pvars">\n'
        '      <div class="pv"><span class="pv-n">1</span><b>Surface</b><small>m² à traiter</small></div>\n'
        '      <span class="pv-x">×</span>\n'
        '      <div class="pv"><span class="pv-n">2</span><b>Fréquence</b><small>passages / semaine</small></div>\n'
        '      <span class="pv-x">×</span>\n'
        '      <div class="pv"><span class="pv-n">3</span><b>Protocole</b><small>prestations retenues</small></div>\n'
        '      <span class="pv-eq">=</span>\n'
        '      <div class="pv pv-res"><b>Votre forfait</b><small>mensuel, sur mesure</small></div>\n'
        '    </div>\n'
        f'    <figure class="pphoto"><img src="{_IMG}" alt="Entretien de bureaux SPN NET — Paris" loading="lazy"/>'
        '<figcaption>Interventions avant 9h ou après 18h, sans gêner votre activité.</figcaption></figure>\n'
        '  </div>\n'
        # grille
        '  <h3 class="ph3">Grille indicative par surface et par fréquence</h3>\n'
        '  ' + grid + '\n'
        '  <p class="pnote">Montants hors taxes, entretien courant des bureaux, sanitaires et parties '
        'communes compris. Vitrerie, décapage des sols et remises en état sont chiffrés à part.</p>\n'
        '  <div class="tbc-legend reveal"><span class="tbc">[ ]</span> Valeurs à compléter par SPN NET '
        'avant mise en ligne — la page ne se publie pas tant que la grille n\'est pas renseignée.</div>\n'
        # 6 facteurs
        '  <h3 class="ph3" style="margin-top:34px">Ce qui fait varier le prix de votre devis</h3>\n'
        '  <p style="max-width:760px;color:var(--grey)">Deux bureaux de surface identique n\'aboutissent '
        'pas au même montant. Six éléments expliquent l\'essentiel de l\'écart :</p>\n'
        '  <div class="pfactors">\n' + factors + '  </div>\n'
        '  <p style="max-width:760px;margin-top:18px">Nous évaluons ces éléments lors d\'une visite sur '
        'site, puis vous transmettons une proposition détaillée sous 24 heures ouvrées. Le devis est '
        'gratuit et sans engagement.</p>\n'
        # repère marché (annexe, étiqueté)
        '  <details class="mkt reveal"><summary>Repère de marché — relevé du 25 août 2026 '
        '<span class="pl">+</span></summary><div class="mkt-b">'
        '<p><b>Ces montants ne sont pas ceux de SPN NET.</b> Ils sont relevés sur la page d\'un concurrent '
        'positionné sur la même requête (grille reprise mot pour mot par Google dans son extrait de '
        'résultat) et servent uniquement à situer les fourchettes à fixer.</p>'
        '<div style="overflow-x:auto"><table class="tbl"><thead><tr><th>Surface</th><th>Par passage</th>'
        '<th>Par mois</th></tr></thead><tbody>'
        '<tr><td>50 à 100 m²</td><td>35 à 50 €</td><td>750 à 1 100 €</td></tr>'
        '<tr><td>100 à 200 m²</td><td>45 à 75 €</td><td>990 à 1 650 €</td></tr>'
        '<tr><td>200 à 500 m²</td><td>70 à 140 €</td><td>1 540 à 3 080 €</td></tr>'
        '</tbody></table></div>'
        '<p class="src">Source : groupe-france-clean.fr, page « Nettoyage bureau à Paris 17ème », '
        '9ᵉ résultat organique sur « nettoyage de bureaux paris 17 » au 25/08/2026.</p>'
        '</div></details>\n'
        '</div></div>\n\n<!-- ============ WHY US ============ -->')


PRICE_CSS = (
    ".spn-lp .tbc{display:inline-block;background:#FFF1EA;color:#D8431F;border:1px dashed #D8431F;"
    "border-radius:6px;padding:0 7px;font-weight:700;font-size:.9em;font-family:'Roboto Mono',ui-monospace,monospace;letter-spacing:.02em}"
    ".spn-lp .sec.price{background:var(--cream,#FAF8F5)}"
    ".spn-lp .ph3{font-family:'Fraunces',serif;font-weight:600;font-size:1.3rem;margin:26px 0 14px}"
    ".spn-lp .pgrid2{display:grid;grid-template-columns:1.15fr .85fr;gap:22px;align-items:center;margin-bottom:8px}"
    ".spn-lp .pvars{display:flex;flex-wrap:wrap;align-items:center;gap:12px;background:#fff;border:1px solid var(--line,#E9E4DD);border-radius:20px;padding:22px}"
    ".spn-lp .pvars .pv{flex:1 1 90px;min-width:90px;text-align:center;padding:8px}"
    ".spn-lp .pvars .pv-n{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;background:#FFF1EA;color:#D8431F;font-family:'Fraunces',serif;font-weight:700;margin-bottom:8px}"
    ".spn-lp .pvars .pv b{display:block;font-size:1rem}.spn-lp .pvars .pv small{color:var(--grey,#5b616b);font-size:.8rem}"
    ".spn-lp .pvars .pv-x,.spn-lp .pvars .pv-eq{font-family:'Fraunces',serif;font-size:1.4rem;color:var(--orange,#ED5D37);font-weight:700}"
    ".spn-lp .pvars .pv-res{background:#16181D;color:#fff;border-radius:14px;padding:14px 10px;flex:1 1 120px}"
    ".spn-lp .pvars .pv-res small{color:rgba(255,255,255,.75)}"
    ".spn-lp .pphoto{margin:0;border-radius:20px;overflow:hidden;border:1px solid var(--line,#E9E4DD);background:#fff}"
    ".spn-lp .pphoto img{width:100%;height:100%;object-fit:cover;display:block;aspect-ratio:4/3}"
    ".spn-lp .pphoto figcaption{font-size:.82rem;color:var(--grey,#5b616b);padding:10px 14px}"
    ".spn-lp table.ptable td:first-child{white-space:nowrap}"
    ".spn-lp .pnote{font-size:.85rem;color:var(--grey,#5b616b);margin-top:10px;max-width:820px}"
    ".spn-lp .tbc-legend{margin-top:14px;font-size:.85rem;color:#D8431F;background:#fff;border:1px dashed #D8431F;border-radius:12px;padding:12px 16px;display:inline-block}"
    ".spn-lp .pfactors{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:8px}"
    ".spn-lp .pf{background:#fff;border:1px solid var(--line,#E9E4DD);border-radius:16px;padding:18px 18px}"
    ".spn-lp .pf-ic{display:inline-flex;width:38px;height:38px;color:var(--orange-deep,#D8431F);background:#FFF1EA;border-radius:10px;padding:8px;margin-bottom:10px}"
    ".spn-lp .pf-ic svg{width:100%;height:100%}"
    ".spn-lp .pf b{display:block;font-size:1rem;margin-bottom:4px}.spn-lp .pf span:last-child{color:var(--grey,#5b616b);font-size:.9rem}"
    ".spn-lp .mkt{margin-top:28px;background:#fff;border:1px solid var(--line,#E9E4DD);border-radius:14px;padding:4px 18px}"
    ".spn-lp .mkt summary{cursor:pointer;font-weight:600;padding:14px 0;list-style:none;display:flex;justify-content:space-between;align-items:center}"
    ".spn-lp .mkt summary::-webkit-details-marker{display:none}"
    ".spn-lp .mkt .mkt-b{padding-bottom:14px}.spn-lp .mkt .src{font-size:.78rem;color:var(--grey,#5b616b);margin-top:8px}"
    ".spn-lp .rev-local{max-width:760px;margin:6px auto 0;color:var(--grey,#5b616b);font-size:.96rem;text-align:center}"
    ".spn-lp .rev-local .tbc{border-style:solid}"
    "@media(max-width:880px){.spn-lp .pgrid2{grid-template-columns:1fr}.spn-lp .pfactors{grid-template-columns:1fr 1fr}}"
    "@media(max-width:560px){.spn-lp .pfactors{grid-template-columns:1fr}.spn-lp .pvars .pv-x,.spn-lp .pvars .pv-eq{display:none}}"
)


def build_draft():
    z = dict(ALL_ZONES[SRC_SLUG])
    # monkeypatch : tableau 4 colonnes + FAQ custom (schéma FAQPage synchronisé)
    mz.SERVICES = SERVICES_4COL
    mz.faq_html = faq_html_p17
    h = mz.build(z)

    # 2) paragraphe d'ouverture prix, avant le 1er paragraphe local
    open_p = (
        '<p>Dans le 17e arrondissement, l\'entretien d\'un plateau de bureaux de 100 à 300 m² nettoyé '
        'trois fois par semaine se situe autour de ' + chip("[B3]") + ' € par mois. En dessous de 100 m², '
        'le budget démarre autour de ' + chip("[A3]") + ' € mensuels, et un plateau de 300 à 600 m² se '
        'situe vers ' + chip("[C3]") + ' €. Le montant exact dépend de votre surface, de votre fréquence '
        'et des prestations retenues : la grille plus bas vous donne l\'ordre de grandeur avant même de '
        'demander un devis.</p>\n      ')
    anchor_p1 = '<p>' + z["p1"] + '</p>'
    assert anchor_p1 in h, "ancre p1 introuvable"
    h = h.replace(anchor_p1, open_p + anchor_p1, 1)

    # 3) ligne budget dans l'encadré l'essentiel (avant Contact)
    contact_row = '<div class="row"><dt>Contact</dt>'
    budget_row = ('<div class="row"><dt>Budget indicatif 17e</dt><dd>À partir de ' + chip("[A3]")
                  + ' € / mois — 100 m², 3 passages/sem.</dd></div>')
    h = h.replace(contact_row, budget_row + contact_row, 1)

    # 5) nouveau H2 prix, entre le tableau des prestations et « Moins de tracas »
    h = h.replace("<!-- ============ WHY US ============ -->", price_section(), 1)

    # 6) phrase d'ancrage local dans « Nos clients parlent pour nous »
    anchor_rev = ('<div class="rev-score">')
    local_line = (
        '<p class="rev-local">Nous entretenons les bureaux d\'entreprises installées dans le 17e et sur '
        'les communes limitrophes — Clichy, Levallois-Perret, Neuilly-sur-Seine. '
        + chip("[RÉFÉRENCE CLIENT À CONFIRMER]") + '</p>\n    ')
    h = h.replace(anchor_rev, local_line + anchor_rev, 1)

    # CSS des infographies
    h = h.replace("</style>", PRICE_CSS + "</style>", 1)
    return h


def deploy_draft(h):
    ex = requests.get(API, params={"slug": DRAFT_SLUG, "status": "publish,future,draft",
                                   "_fields": "id"}, auth=AUTH, timeout=30).json()
    payload = {
        "title": "BROUILLON — Nettoyage de bureaux Paris 17e (MAJ prix)",
        "slug": DRAFT_SLUG,
        "status": "draft",
        "content": "<!-- wp:html -->\n" + h + "\n<!-- /wp:html -->",
        "template": "elementor_header_footer",
        "meta": {"_elementor_edit_mode": "",
                 "slim_seo": {"title": NEW_TITLE, "description": NEW_DESC, "noindex": True}},
    }
    url = f"{API}/{ex[0]['id']}" if ex else API
    r = requests.post(url, auth=AUTH, timeout=90, json=payload)
    r.raise_for_status()
    j = r.json()
    return j


def main():
    h = build_draft()
    (HERE / f"draft-{DRAFT_SLUG}.html").write_text(h)
    j = deploy_draft(h)
    pid = j.get("id")
    prev = f"https://spn-net.fr/?page_id={pid}&preview=true"
    print(f"  ✓ brouillon [draft] id={pid}")
    print(f"    aperçu admin : {prev}")
    print(f"    lien édition : https://spn-net.fr/wp-admin/post.php?post={pid}&action=edit")
    print(f"    HTML : agents/landing/draft-{DRAFT_SLUG}.html ({len(h)} car.)")


if __name__ == "__main__":
    main()
