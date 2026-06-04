#!/usr/bin/env python3
"""Génère des variantes sectorielles (message-match Google Ads) de la landing page
de base (lp.html) et les publie en noindex / template Canvas.

Chaque variante ne change que le hero (eyebrow, H1, lead), le <select> (secteur
pré-sélectionné) et le <title>. Tout le reste (logos, avis, formulaire branché sur
l'Elementor ae4c659, etc.) est identique. Le formulaire reporte automatiquement
l'URL/titre de la variante dans l'e-mail (referer = location.href).

Met aussi à jour la LP de base (id 2594).
Usage : python3 agents/landing/make_variants.py
"""
from __future__ import annotations

import os
import pathlib

import requests

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
BASE_HTML = pathlib.Path(__file__).parent / "lp.html"
HERE = pathlib.Path(__file__).parent

EYEBROW_SRC = '<span class="eyebrow">Propreté professionnelle · Paris & Île-de-France</span>'
H1_SRC = "<h1>Nettoyage de <em>bureaux & d'immeubles</em> qui valorise vos espaces</h1>"
LEAD_SRC = '<p class="lead">Entreprise de propreté certifiée ISO 45001, 30 ans d\'expérience et +350 clients. Un interlocuteur dédié, des équipes formées et un résultat irréprochable, semaine après semaine.</p>'
SELECT_SRC = '<select name="type" required><option value="">Sélectionnez…</option><option>Bureaux / Tertiaire</option><option>Immeuble / Copropriété</option><option>Commerce / Retail</option><option>Santé / Médical</option><option>Logistique / Industrie</option><option>Autre</option></select>'


def select_with(sector_label: str) -> str:
    return ('<select name="type" required><option value="">Sélectionnez…</option>'
            f'<option selected>{sector_label}</option>'
            '<option>Bureaux / Tertiaire</option><option>Immeuble / Copropriété</option>'
            '<option>Commerce / Retail</option><option>Santé / Médical</option>'
            '<option>Logistique / Industrie</option><option>Autre</option></select>')


VARIANTS = {
    "nettoyage-musee-theatre-evenementiel-paris": {
        "title": "Nettoyage de musées, théâtres & événementiel – Paris & IDF",
        "ss_title": "Nettoyage culturel & événementiel – SPN NET",
        "ss_desc": "Nettoyage de musées, théâtres, cinémas, salles de concert et de sport à Paris et en Île-de-France. Devis gratuit sous 24h.",
        "eyebrow": '<span class="eyebrow">Propreté culturelle & événementielle · Paris & Île-de-France</span>',
        "h1": "<h1>Nettoyage de <em>musées, théâtres & salles de spectacle</em> à la hauteur de vos publics</h1>",
        "lead": '<p class="lead">Spécialiste des lieux culturels, sportifs et événementiels : musées, théâtres, cinémas, salles de concert et de sport. Interventions discrètes, en horaires décalés, avant l\'ouverture au public.</p>',
        "select": select_with("Loisirs / Culture / Événementiel"),
    },
    "nettoyage-hotel-restaurant-paris": {
        "title": "Nettoyage d'hôtels & restaurants – Paris & Île-de-France",
        "ss_title": "Nettoyage hôtellerie & restauration – SPN NET",
        "ss_desc": "Nettoyage d'hôtels, restaurants et brasseries à Paris : normes HACCP, dégraissage de cuisines, entretien des chambres. Devis 24h.",
        "eyebrow": '<span class="eyebrow">Propreté hôtelière & restauration · Paris & Île-de-France</span>',
        "h1": "<h1>Nettoyage d'<em>hôtels & de restaurants</em> qui protège votre réputation</h1>",
        "lead": '<p class="lead">Hôtels, restaurants, brasseries : un nettoyage rigoureux conforme aux normes HACCP, du dégraissage des cuisines à l\'entretien des chambres. Interventions de nuit pour ne jamais gêner vos clients.</p>',
        "select": select_with("Hôtellerie / Restauration"),
    },
    "nettoyage-medical-sante-paris": {
        "title": "Nettoyage médical & bionettoyage – Paris & Île-de-France",
        "ss_title": "Nettoyage médical & bionettoyage – SPN NET",
        "ss_desc": "Bionettoyage de cabinets, laboratoires, cliniques et EHPAD à Paris : protocoles HAS/ARS, traçabilité, gestion des DASRI. Devis 24h.",
        "eyebrow": '<span class="eyebrow">Bionettoyage & hygiène médicale · Paris & Île-de-France</span>',
        "h1": "<h1>Bionettoyage <em>médical & santé</em> conforme et rassurant</h1>",
        "lead": '<p class="lead">Cabinets, laboratoires, cliniques, EHPAD : protocoles de bionettoyage et de désinfection conformes aux exigences HAS et ARS. Code couleur, traçabilité et gestion des DASRI par des agents formés.</p>',
        "select": select_with("Santé / Médical"),
    },
}


def build(base: str, v: dict) -> str:
    h = base
    h = h.replace(EYEBROW_SRC, v["eyebrow"])
    h = h.replace(H1_SRC, v["h1"])
    h = h.replace(LEAD_SRC, v["lead"])
    h = h.replace(SELECT_SRC, v["select"])
    return h


def upsert(slug: str, title: str, html: str, ss_title: str, ss_desc: str) -> str:
    content = "<!-- wp:html -->\n" + html + "\n<!-- /wp:html -->"
    # existe déjà ?
    ex = requests.get("https://spn-net.fr/wp-json/wp/v2/pages",
                      params={"slug": slug, "_fields": "id"}, auth=AUTH, timeout=30).json()
    payload = {"title": title, "slug": slug, "status": "publish", "content": content,
               "template": "elementor_canvas",
               "meta": {"slim_seo": {"title": ss_title, "description": ss_desc, "noindex": True}}}
    if ex:
        pid = ex[0]["id"]
        r = requests.post(f"https://spn-net.fr/wp-json/wp/v2/pages/{pid}", auth=AUTH, timeout=60, json=payload)
    else:
        r = requests.post("https://spn-net.fr/wp-json/wp/v2/pages", auth=AUTH, timeout=60, json=payload)
    r.raise_for_status()
    return r.json().get("link")


def main() -> None:
    base = BASE_HTML.read_text()
    # 1) met à jour la LP de base (referer auto, etc.)
    requests.post("https://spn-net.fr/wp-json/wp/v2/pages/2594", auth=AUTH, timeout=60,
                  json={"content": "<!-- wp:html -->\n" + base + "\n<!-- /wp:html -->"}).raise_for_status()
    print("✓ LP de base mise à jour (referer auto)")
    # 2) variantes
    for slug, v in VARIANTS.items():
        html = build(base, v)
        (HERE / f"lp-{slug}.html").write_text(html)
        link = upsert(slug, v["title"], html, v["ss_title"], v["ss_desc"])
        print(f"✓ {link}")


if __name__ == "__main__":
    main()
