#!/usr/bin/env python3
"""Déploie le modèle sur les PAGES MÈRES sectorielles (pôles), en indexable.
Maillage descendant : chaque secteur pointe vers son article, des secteurs liés et
des pages locales. Contenu, prestations et FAQ propres au secteur (cf. sectors_data).

Mécanisme identique (réversible) à make_zone.

Usage :
  python3 agents/landing/make_sector.py tertiaire commerce-et-retail
  python3 agents/landing/make_sector.py --all
  python3 agents/landing/make_sector.py --restore tertiaire
"""
from __future__ import annotations

import os
import sys
import pathlib

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from make_paris2 import CSS, PROMISE, PULL, TEAM, TEAMCUE, HEADFIX, _CK  # noqa: E402
import make_zone as mz  # noqa: E402
from sectors_data import SECTORS  # noqa: E402


def facts(s):
    return ('<div class="facts reveal"><h3>' + _CK + ' SPN NET — l\'essentiel</h3><dl>'
            f'<div class="row"><dt>Spécialité</dt><dd>Nettoyage {s["short"].lower()}</dd></div>'
            '<div class="row"><dt>Zone desservie</dt><dd>Paris &amp; Île-de-France</dd></div>'
            '<div class="row"><dt>Expérience</dt><dd>30 ans · +350 clients</dd></div>'
            '<div class="row"><dt>Certifications</dt><dd>ISO 45001 · EcoVadis Argent</dd></div>'
            '<div class="row"><dt>Note clients</dt><dd>4,8/5 — 48 avis Google</dd></div>'
            '<div class="row"><dt>Horaires d\'intervention</dt><dd>Avant 9h, après 18h, week-end</dd></div>'
            '<div class="row"><dt>Devis</dt><dd>Gratuit, transmis sous 24h</dd></div>'
            '<div class="row"><dt>Contact</dt><dd><a href="tel:+33149462240" data-tel>01 49 46 22 40</a> · Bagneux (92)</dd></div>'
            '</dl></div>')


def services_table(s):
    rows = ""
    for presta, detail, freq in s["services"]:
        rows += f'        <tr><td>{presta}</td><td>{detail}</td><td>{freq}</td></tr>\n'
    return (
        '  <div style="margin-top:40px" class="reveal">\n'
        f'    <h3 style="font-family:\'Fraunces\',serif;font-weight:600;font-size:1.4rem;margin-bottom:14px">Nos prestations — {s["name"]}</h3>\n'
        '    <div style="overflow-x:auto"><table class="tbl">\n'
        '      <thead><tr><th>Prestation</th><th>Ce que nous faisons</th><th>Fréquence type</th></tr></thead>\n'
        f'      <tbody>\n{rows}      </tbody>\n    </table></div>\n  </div>\n')


def local(s):
    chips = "".join(f"<span>{a}</span>" for a in s["aspects"])
    return (
        '\n<!-- ============ EXPERTISE SECTORIELLE ============ -->\n'
        '<div class="sec local"><div class="wrap">\n'
        '  <div class="sec-head reveal" style="max-width:820px;text-align:left;margin:0 0 30px">'
        '<span class="eyebrow">Expertise sectorielle</span>'
        f'<h2>Notre expertise du nettoyage — {s["name"]}</h2></div>\n'
        + facts(s) +
        '\n  <div class="grid">\n    <div class="reveal">\n'
        f'      <p>{s["p1"]}</p>\n'
        f'      <p>{s["p2"]}</p>\n'
        '      <p>Interventions à Paris et dans toute l\'Île-de-France, en horaires décalés, avec un interlocuteur dédié. '
        'Voir aussi notre <a href="https://spn-net.fr/tertiaire/">pôle nettoyage tertiaire &amp; bureaux</a>.</p>\n'
        f'      <div class="qtiers">{chips}</div>\n'
        '    </div>\n'
        '    <div class="side reveal">\n'
        f'      <h3>Pourquoi nous confier ce secteur</h3>\n'
        '      <ul class="hero-points" style="margin:0">\n'
        '        <li>Protocole adapté à votre activité</li>\n'
        '        <li>Équipes formées &amp; fidélisées</li>\n'
        '        <li>Un interlocuteur dédié, joignable</li>\n'
        '        <li>Devis sous 24h, sans engagement</li>\n'
        '      </ul>\n    </div>\n  </div>\n'
        + services_table(s) +
        '</div></div>\n\n<!-- ============ WHY US ============ -->')


def links(s):
    cards = (f'    <a class="card" href="https://spn-net.fr/{s["article"][0]}/"><b>{s["article"][1]} <span class="ar">→</span></b>'
             '<small>Notre guide sectoriel</small></a>\n')
    for slug, label in s["related"]:
        cards += (f'    <a class="card" href="https://spn-net.fr/{slug}/"><b>{label} <span class="ar">→</span></b>'
                  '<small>Secteur lié</small></a>\n')
    for slug, label in s["zones"]:
        cards += (f'    <a class="card" href="https://spn-net.fr/{slug}/"><b>{label} <span class="ar">→</span></b>'
                  '<small>Nettoyage de bureaux localement</small></a>\n')
    return (
        '\n<!-- ============ MAILLAGE INTERNE ============ -->\n'
        '<div class="sec links"><div class="wrap">\n'
        '  <div class="sec-head reveal"><span class="eyebrow c">À explorer</span>'
        f'<h2>{s["name"]} — ressources &amp; zones liées</h2>'
        '<p>Notre guide sectoriel, les secteurs connexes et nos interventions locales.</p></div>\n'
        '  <div class="grid reveal">\n' + cards + '  </div>\n</div></div>\n\n<!-- ============ FINAL CTA ============ -->')


def faq(s):
    items = list(s["faq"]) + [
        ("Combien coûte le nettoyage pour ce secteur ?",
         "Le tarif dépend de la surface, de la fréquence et des prestations retenues. Il n'y a pas de forfait standard imposé : le devis est gratuit et personnalisé, sous 24h."),
        ("Pouvez-vous intervenir en dehors des heures d'activité ?",
         "Oui, nos équipes interviennent tôt le matin, en soirée ou le week-end selon vos contraintes, pour ne pas perturber votre activité."),
        ("Vos prestations s'inscrivent-elles dans une démarche RSE ?",
         "Oui : SPN NET est médaille d'argent EcoVadis 2025 et certifiée ISO 45001. Les protocoles et produits adaptés sont définis lors de l'étude de votre besoin."),
        ("Le devis engage-t-il à quelque chose ?",
         "Non : le devis est gratuit et sans engagement. Les conditions du contrat sont définies avec vous avant toute intervention."),
    ]
    html = ""
    for q, a in items:
        html += (f'    <details class="acc"><summary>{q}<span class="pl">+</span></summary>'
                 f'<div class="body">{a}</div></details>\n')
    return html.rstrip("\n"), items


def build(s):
    h = mz.BASE_HTML
    h = h.replace(mz.NOINDEX_SCRIPT, "", 1)
    a = h.index("<!-- ============ TOP STRIP ============ -->")
    b = h.index("<!-- ============ HERO ============ -->")
    h = h[:a] + h[b:]
    h = h.replace("</style>", CSS + "</style>", 1)
    h = h.replace(mz.A_EYEBROW, f'<span class="eyebrow">{s["eyebrow"]}</span>', 1)
    h = h.replace(mz.A_H1, f'<h1>{s["h1"]}</h1>', 1)
    h = h.replace(mz.A_LEAD, f'<p class="lead">{s["lead"]}</p>', 1)
    zp = ("<p>Nous intervenons à Paris et dans toute l'Île-de-France, avec des équipes mobiles dans les "
          "20 arrondissements et l'ensemble des départements franciliens.</p>")
    h = h.replace(mz.A_ZONEP, zp, 1)
    h = h.replace("<!-- ============ WHY US ============ -->", PROMISE + local(s), 1)
    h = h.replace("<!-- ============ AVIS GOOGLE", PULL + "\n<!-- ============ AVIS GOOGLE", 1)
    h = h.replace("<!-- ============ RÉALISATIONS ============ -->", TEAM, 1)
    tr = 'ISO 45001</b></span></div>\n    </div>'
    h = h.replace(tr, 'ISO 45001</b></span></div>\n      ' + TEAMCUE + '\n    </div>', 1)
    h = h.replace("<!-- ============ FINAL CTA ============ -->", links(s), 1)
    h = h.replace(
        '<span class="eyebrow c">Pourquoi SPN NET</span><h2>Propreté, rigueur et engagement depuis 30 ans</h2><p>Une entreprise à taille humaine, deux priorités : le client et le salarié.</p>',
        '<span class="eyebrow c">Ce que vous y gagnez</span><h2>Moins de tracas, des locaux toujours nickel</h2><p>Une entreprise à taille humaine qui traite vos locaux comme les siens — et vos équipes avec le même soin.</p>'
        '<div class="gains" style="margin-top:18px">'
        '<span>' + _CK + ' Zéro relance à faire</span>'
        '<span>' + _CK + ' Même équipe, chaque semaine</span>'
        '<span>' + _CK + ' Contrôle qualité régulier</span></div>', 1)
    fs = h.index('    <details class="acc"><summary>Quelle est votre zone')
    fe = h.index("</details>", h.index("bien-être et à la sécurité de nos agents")) + len("</details>")
    fhtml, fitems = faq(s)
    h = h[:fs] + fhtml + h[fe:]
    ls = h.index('{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[')
    le = h.index("]}", ls) + len("]}")
    q = ",".join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
                 % (mz.strip_accents(n).replace('"', "'"), mz.strip_accents(x).replace('"', "'")) for n, x in fitems)
    h = h[:ls] + '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + q + ']}' + h[le:]
    bc = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
          '"itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":"https://spn-net.fr/"},'
          f'{{"@type":"ListItem","position":2,"name":"{mz.strip_accents(s["name"])}"}}]}}</script>')
    h = h.rstrip()[:-len("</section>")] + bc + HEADFIX + "\n</section>\n"
    return h


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return
    if args[0] == "--restore":
        for slug in args[1:]:
            print(mz.restore(slug))
        return
    slugs = list(SECTORS.keys()) if args[0] == "--all" else args
    for slug in slugs:
        s = SECTORS.get(slug)
        if not s:
            print(f"  ? {slug}: pas de données"); continue
        try:
            print(mz.deploy(slug, s, builder=build, prefix="sector"))
        except Exception as ex:  # noqa: BLE001
            print(f"  ✗ {slug}: {ex}")


if __name__ == "__main__":
    main()
