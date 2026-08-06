#!/usr/bin/env python3
"""Page 'Changer de prestataire de nettoyage' (BOFU/SEO), demandée par la cliente.

Réutilise le moteur de make_special (page sur-mesure branded, indexable,
formulaire double-écriture, FAQ + schema, fil d'Ariane).

Contenu = notes de la cliente, remaniées pour le SEO (aucune offre inventée) :
process en 4 étapes, rupture de contrat, reprise du personnel (Annexe 7),
formation des agents.

Usage : python3 agents/landing/make_switch.py
        python3 agents/landing/make_switch.py --restore changer-de-prestataire-nettoyage
"""
from __future__ import annotations

import os
import sys
import pathlib

import requests

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import make_zone as mz  # noqa: E402
import make_special as ms  # noqa: E402

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
API = "https://spn-net.fr/wp-json/wp/v2/pages"
SLUG = "changer-de-prestataire-nettoyage"

STEPS = [
    ("Prise de contact en moins de 4h",
     "Vous nous décrivez votre besoin ; nous vous rappelons en moins de 4 h ouvrées pour comprendre votre situation."),
    ("Visite de vos locaux",
     "Nous venons voir vos locaux pour cerner vos contraintes (accès, horaires, surfaces) et bâtir une proposition juste."),
    ("Proposition &amp; protocole sur mesure",
     "Vous recevez une proposition claire et, si nécessaire, un protocole de ménage adapté à vos espaces — sans forfait imposé."),
    ("Signature &amp; démarrage",
     "Nous organisons la transition avec votre ancien prestataire pour un démarrage sans coupure de service."),
]

CARDS = [
    (ms._ic('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M9 13h6M9 17h4"/>'),
     "La rupture de votre contrat actuel",
     "On vous aide à résilier proprement : nous lisons avec vous les conditions de résiliation de votre contrat en cours et nous rédigeons la lettre. Vous restez maître de la décision — nous sommes là en support et conseil."),
    (ms._ic('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
     "La reprise de vos agents (Annexe 7)",
     "La convention collective de la propreté (<b>Annexe 7</b>) prévoit le transfert des agents à la société entrante lorsque les conditions sont réunies : au moins <b>6 mois d'ancienneté</b> et <b>30 % du temps de travail</b> sur votre site. Nous nous occupons des démarches."),
    (ms._ic('<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/>'),
     "Des agents formés, produits écologiques",
     "Nos agents — y compris ceux que nous reprenons — sont formés à nos produits et protocoles écologiques. La transition se fait sans perte de qualité ni changement de repères pour vos équipes."),
]


def switch_section():
    css = (
        '<style>'
        '.spn-lp .swsteps{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:8px}'
        '.spn-lp .swstep{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px 20px;position:relative}'
        '.spn-lp .swstep .num{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:12px;'
        'background:var(--orange-soft);color:var(--orange-deep);font-family:\'Fraunces\',serif;font-weight:700;font-size:1.15rem;margin-bottom:12px}'
        '.spn-lp .swstep h3{font-size:1.06rem;margin-bottom:6px;line-height:1.25}'
        '.spn-lp .swstep p{font-size:.9rem;color:var(--grey)}'
        '@media(max-width:900px){.spn-lp .swsteps{grid-template-columns:1fr 1fr}}'
        '@media(max-width:560px){.spn-lp .swsteps{grid-template-columns:1fr}}'
        '</style>'
    )
    steps = ""
    for i, (h, p) in enumerate(STEPS, 1):
        steps += f'    <div class="swstep reveal"><span class="num">{i}</span><h3>{h}</h3><p>{p}</p></div>\n'
    cards = ""
    for ic, h, p in CARDS:
        cards += f'    <div class="eng reveal"><div class="ic">{ic}</div><h3>{h}</h3><p>{p}</p></div>\n'
    return (
        css +
        '\n<!-- ============ PROCESS ============ -->\n'
        '<div class="sec"><div class="wrap">\n'
        '  <div class="sec-head reveal" style="max-width:760px"><span class="eyebrow c">Le process</span>'
        '<h2>Changer de prestataire de nettoyage, étape par étape</h2>'
        '<p>Que vous fassiez appel à une société de nettoyage pour la première fois ou que vous souhaitiez '
        'en changer, on vous accompagne du premier contact au démarrage.</p></div>\n'
        '  <div class="swsteps">\n' + steps + '  </div>\n</div></div>\n'
        '\n<!-- ============ INFOS ============ -->\n'
        '<div class="sec engage"><div class="wrap">\n'
        '  <div class="sec-head reveal"><span class="eyebrow c">Ce qu\'il faut savoir</span>'
        '<h2>Résiliation, reprise du personnel : on gère</h2>'
        '<p>Changer de prestataire fait souvent peur à cause de la paperasse et du sort des agents. '
        'Voici ce qu\'il faut savoir — et ce dont nous nous chargeons.</p></div>\n'
        '  <div class="grid">\n' + cards + '  </div>\n</div></div>\n\n<!-- ============ WHY US ============ -->'
    )


CFG = dict(
    title="Changer de prestataire de nettoyage : mode d'emploi | SPN NET",
    desc="Changer de société de nettoyage sans stress : résiliation du contrat, reprise du personnel (Annexe 7), démarrage sans coupure. SPN NET vous accompagne à Paris & IDF. Devis 24h.",
    eyebrow="Changer de prestataire",
    h1="Changer de <em>prestataire de nettoyage</em>, sans stress",
    lead="Vous voulez confier vos locaux à une autre société de nettoyage — ou faire appel à un prestataire pour la première fois ? On vous accompagne à chaque étape : résiliation, reprise des agents (Annexe 7), démarrage sans coupure. Devis sous 24h.",
    section=switch_section,
    faq=[
        ("Comment changer de société de nettoyage ?",
         "En pratique : vous nous contactez, nous visitons vos locaux, nous vous envoyons une proposition, puis nous organisons la transition avec votre ancien prestataire. Nous vous accompagnons aussi pour la résiliation et la reprise des agents."),
        ("Dois-je résilier mon contrat actuel avant de vous contacter ?",
         "Non. Contactez-nous d'abord : nous lisons avec vous les conditions de résiliation de votre contrat en cours et nous vous aidons à rédiger la lettre, au bon moment, pour éviter toute coupure de service."),
        ("Qu'est-ce que la reprise du personnel (Annexe 7) ?",
         "L'Annexe 7 de la convention collective de la propreté organise le transfert des agents de nettoyage à l'entreprise entrante lorsqu'un marché change de prestataire. Elle protège l'emploi des salariés concernés."),
        ("Quels sont les critères de reprise des agents ?",
         "Les principaux critères sont une ancienneté d'au moins 6 mois sur le site et au moins 30 % du temps de travail effectué sur votre site. Nous nous chargeons des démarches liées à cette reprise."),
        ("Le changement crée-t-il une coupure de nettoyage ?",
         "Non : nous organisons la transition pour que la prestation se poursuive sans interruption. L'objectif est un passage de relais fluide, sans jour sans entretien."),
        ("Sous quel délai pouvez-vous démarrer ?",
         "Nous vous recontactons en moins de 4 h ouvrées, puis nous convenons d'une visite et d'un devis sous 24 h. Le démarrage effectif dépend de votre préavis de résiliation, que nous étudions avec vous."),
    ],
    bc="Changer de prestataire",
)


def ensure_page():
    pid = mz.get_page_id(SLUG)
    if pid:
        return pid
    r = requests.post(API, auth=AUTH, timeout=90, json={
        "title": "Changer de prestataire de nettoyage", "slug": SLUG, "status": "publish",
        "content": "…", "template": "elementor_header_footer",
        "meta": {"slim_seo": {"title": CFG["title"], "description": CFG["desc"], "noindex": False}}})
    r.raise_for_status()
    return r.json()["id"]


def main():
    args = sys.argv[1:]
    if args and args[0] == "--restore":
        for slug in args[1:]:
            print(mz.restore(slug))
        return
    ensure_page()
    print(mz.deploy(SLUG, CFG, builder=ms.build, prefix="special"))


if __name__ == "__main__":
    main()
