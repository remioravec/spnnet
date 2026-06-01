#!/usr/bin/env python3
"""Réécriture lisibilité d'une page Elementor (réécritures rédigées à la main,
fidèles aux faits). Idempotent (marqueur). Réversible via le backup JSON.

Sécurité : avant toute écriture, l'original de chaque widget est sauvegardé dans
agents/backups/page_<id>_text_editors.json (déjà fait pour la page 469).

Usage :
  python3 agents/apply_readability.py --page 469 --apply
  python3 agents/apply_readability.py --page 469 --restore   # rollback
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from elementor_mcp import ElementorMCP  # noqa: E402

BACKUPS = Path(__file__).parent / "backups"
MARK = "<!-- spn-readability -->"
KEEP_LINK = ('<p><!-- spn-maillage-retour -->À lire aussi : '
             '<a href="https://spn-net.fr/meilleure-entreprise-nettoyage-logistique-industrie-paris/">'
             'bien choisir une société de nettoyage logistique et industriel</a>.</p>')

# Réécritures par page → {element_id: nouveau HTML}. Phrases courtes, listes,
# balisage nettoyé, liens cassés google.com/search neutralisés (texte conservé),
# faits/titres/lien de maillage préservés.
REWRITES: dict[int, dict[str, str]] = {
    469: {
        "7ec8861f": MARK +
            "<p>Dans l'industrie lourde, la manufacture et la logistique, la propreté n'est pas un simple "
            "confort visuel. C'est un pilier de la productivité, de la prévention des risques et du bon "
            "fonctionnement de vos infrastructures. Poussières, résidus de production, traces de manutention : "
            "tout s'accumule vite. Mieux vaut confier ce travail à des spécialistes équipés.</p>"
            "<p><b>Entreprise de nettoyage logistique et industriel à Paris</b>, SPN NET accompagne les "
            "<b>usines et entrepôts</b> d'<b>Île-de-France</b>. Balayage mécanique des plateformes de stockage, "
            "dégraissage technique des lignes de production : nous mobilisons du matériel lourd et des équipes "
            "qualifiées, à la hauteur de vos exigences.</p>"
            "<p>En nous confiant vos infrastructures, vous sécurisez vos flux logistiques. Vous prolongez aussi "
            "la durée de vie de vos machines et garantissez un environnement de travail sain à vos opérateurs — "
            "sans jamais freiner votre rendement.</p>" + KEEP_LINK,
        "4d377353": MARK +
            "<h2><b>Les défis du nettoyage en milieu industriel et logistique (sécurité &amp; productivité)</b></h2>"
            "<p>Diriger un site de production ou une plateforme de distribution, c'est gérer des flux continus de "
            "marchandises et de personnes. Dans ces environnements, les risques professionnels sont partout : "
            "chutes, glissades, départs de feu.</p>"
            "<p>Notre intervention répond à deux priorités des directeurs de site et des responsables HSE "
            "(hygiène, sécurité, environnement) : la <b>sécurité au travail</b> et la <b>maintenance préventive</b>. "
            "Un nettoyage industriel rigoureux apporte des bénéfices concrets et mesurables :</p>"
            "<ul>"
            "<li><b>Moins d'accidents du travail.</b> Traiter les sols glissants (huile, hydrocarbures) et dégager "
            "les allées réduit fortement les chutes et les collisions avec les chariots élévateurs.</li>"
            "<li><b>Un outil de production qui dure.</b> Poussières, sciures et copeaux métalliques encrassent "
            "moteurs et rouages — première cause d'arrêt machine. Un dépoussiérage technique régulier agit comme "
            "une maintenance préventive contre les pannes coûteuses.</li>"
            "<li><b>Des audits et normes respectés.</b> Face aux inspections sanitaires et aux normes ISO, un site "
            "toujours propre facilite vos certifications et rassure vos clients lors des visites d'usine.</li>"
            "</ul>",
        "1207193": MARK +
            "<h2><b>Nos prestations de propreté pour les sites de production et de stockage</b></h2>"
            "<p>Dans l'industrie, le site ne s'arrête jamais : c'est l'une des plus grandes contraintes. SPN NET a "
            "développé une vraie expertise de la <b>co-activité</b>. Nos agents interviennent sur de grandes "
            "surfaces, en toute sécurité, pendant la préparation de commandes ou près des lignes en marche — sans "
            "gêner vos équipes.</p>"
            "<p>Nous bâtissons un cahier des charges sur-mesure pour chaque type d'infrastructure :</p>"
            "<h3><b>Usines, ateliers et lignes de production</b></h3>"
            "<p>Le nettoyage en usine demande de la technicité. Les résidus sont complexes : dégraissage, copeaux, "
            "poussières chimiques. Nous appliquons des protocoles dédiés au <b>nettoyage d'usines et de sites de "
            "production</b> : traitement des sols techniques (résine, béton poreux) et lavage des machines-outils, "
            "via notre service de <b>nettoyage industriel</b>.</p>"
            "<h3><b>Plateformes logistiques, entrepôts et quais</b></h3>"
            "<p>Chariots et transpalettes circulent sans cesse. Résultat : énormément de poussière de cartons et "
            "de traces de pneus. Pour traiter des milliers de mètres carrés en un temps record, nous déployons nos "
            "<b>auto-laveuses</b> autoportées et nos balayeuses mécaniques.</p>"
            "<p>Nous assurons le <b>nettoyage d'entrepôts logistiques</b> pour vos zones de stockage intérieures. "
            "Nous entretenons aussi vos extérieurs : <b>quais de chargement</b> et <b>centres de tri</b>, pour "
            "sécuriser les manœuvres des transporteurs.</p>"
            "<h3><b>Prestations complémentaires (vitrerie et sanitaires)</b></h3>"
            "<p>Pour une prestation globale de facility management, nous prenons aussi en charge :</p>"
            "<ul>"
            "<li>Le <b>nettoyage de vitrerie</b> : bureaux d'usine, postes de garde et verrières industrielles.</li>"
            "<li>La gestion et le réassort de vos <b>fournitures sanitaires</b> pour les vestiaires des opérateurs.</li>"
            "<li>Des interventions de <b>petite maintenance</b> sur site : relamping des entrepôts, réparation de "
            "petits éléments.</li>"
            "</ul>"
            "<h2><b>Matériel lourd et habilitations : l'expertise SPN NET</b></h2>"
            "<p>Le nettoyage industriel ne s'improvise pas avec un chariot de ménage. Il faut un parc de machines "
            "performant et des agents formés aux <b>normes d'hygiène</b> et de sécurité les plus strictes : ATEX, "
            "risques chimiques, travail en hauteur.</p>"
            "<p>La sécurité de nos équipes et des vôtres passe avant tout. Nos intervenants disposent d'"
            "<b>équipements de protection individuelle (EPI)</b> complets et des habilitations nécessaires "
            "(CACES, habilitations électriques) pour opérer sur votre site.</p>"
            "<p><b>Notre parc matériel comprend notamment :</b></p>"
            "<ul>"
            "<li><b>Auto-laveuses autoportées et balayeuses thermiques :</b> pour traiter des dizaines de milliers "
            "de m² de béton sans nuage de poussière.</li>"
            "<li><b>Monobrosses et aspirateurs à filtration absolue (HEPA) :</b> pour décaper les sols gras et "
            "aspirer les poussières fines, y compris en zone sensible.</li>"
            "<li><b>Nettoyeurs très haute pression (eau chaude et froide) :</b> pour dégraisser les bardages, laver "
            "les quais extérieurs et désincruster les huiles moteur.</li>"
            "<li><b>Nacelles élévatrices :</b> pour dépoussiérer en hauteur chemins de câbles, tuyauteries et "
            "luminaires.</li>"
            "</ul>"
            "<h2><b>Pourquoi confier votre site industriel à SPN NET ?</b></h2>"
            "<p>Externaliser l'entretien de votre chaîne logistique, c'est choisir un partenaire réactif, bien "
            "outillé et conscient de vos enjeux économiques. Nous définissons ensemble un cahier des charges strict : "
            "KPI clairs, horaires adaptés (3x8, week-end, nuit) et suivi qualité via des bons d'intervention "
            "dématérialisés.</p>",
    },
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", type=int, required=True)
    m = ap.add_mutually_exclusive_group(required=True)
    m.add_argument("--apply", action="store_true")
    m.add_argument("--restore", action="store_true")
    args = ap.parse_args()

    mcp = ElementorMCP()
    mcp.initialize()
    backup_file = BACKUPS / f"page_{args.page}_text_editors.json"

    if args.restore:
        original = json.loads(backup_file.read_text())
        for eid, html in original.items():
            mcp.call("elementor-mcp-update-element",
                     {"post_id": args.page, "element_id": eid, "settings": {"editor": html}})
            print(f"  ↩ restauré {eid}")
        return 0

    rewrites = REWRITES.get(args.page)
    if not rewrites:
        print(f"Pas de réécriture définie pour la page {args.page}")
        return 1
    for eid, html in rewrites.items():
        mcp.call("elementor-mcp-update-element",
                 {"post_id": args.page, "element_id": eid, "settings": {"editor": html}})
        print(f"  ✓ {eid} réécrit ({len(html)} car.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
