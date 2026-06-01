#!/usr/bin/env python3
"""Applique le maillage interne sur les 12 articles de blog (éditeur classique).

Ajoute à chaque article un lien contextuel descriptif vers sa page secteur/service
correspondante, avec une ancre diversifiée. Idempotent (marqueur HTML).

Identifiants via l'environnement : WP_USER, WP_APP_PASSWORD.
Usage :
  python3 agents/apply_blog_links.py --slug <slug>   # un seul article
  python3 agents/apply_blog_links.py --all           # les 12 articles
"""
from __future__ import annotations

import argparse
import os
import sys

import requests

BASE = "https://spn-net.fr"
U = os.environ["WP_USER"]
P = os.environ["WP_APP_PASSWORD"]
AUTH = (U, P)
MARKER = "<!-- spn-maillage -->"

# slug d'article → (phrase HTML contextuelle avec lien + ancre descriptive diversifiée)
LINKS: dict[str, str] = {
    "meilleure-entreprise-nettoyage-tertiaire-paris":
        f'<p>{MARKER}Pour aller plus loin, découvrez notre offre complète de '
        f'<a href="{BASE}/tertiaire/">nettoyage de bureaux et de locaux tertiaires</a> '
        f'partout en Île-de-France.</p>',
    "meilleure-entreprise-nettoyage-logistique-industrie-paris":
        f'<p>{MARKER}Voir aussi nos prestations dédiées à l\'<a href="{BASE}/logistique-et-industrie/">'
        f'entretien des sites logistiques et industriels</a>.</p>',
    "meilleure-entreprise-nettoyage-sante-medical-paris":
        f'<p>{MARKER}Découvrez notre savoir-faire en <a href="{BASE}/sante-et-medical/">'
        f'nettoyage des établissements de santé et médicaux</a>, soumis à des protocoles d\'hygiène stricts.</p>',
    "meilleure-entreprise-nettoyage-commerce-retail-paris":
        f'<p>{MARKER}En savoir plus sur la <a href="{BASE}/commerce-et-retail/">'
        f'propreté des commerces et des surfaces de vente</a>.</p>',
    "meilleure-entreprise-nettoyage-copropriete-habitat-paris":
        f'<p>{MARKER}Consultez également notre offre d\'<a href="{BASE}/copropriete-et-habitat/">'
        f'entretien des copropriétés et de l\'habitat collectif</a>.</p>',
    "meilleure-entreprise-nettoyage-hotellerie-restauration-paris":
        f'<p>{MARKER}Découvrez nos services de <a href="{BASE}/hotellerie-et-restauration/">'
        f'nettoyage en hôtellerie et restauration</a>.</p>',
    "meilleure-entreprise-nettoyage-loisirs-culture-evenementiel-paris":
        f'<p>{MARKER}Voir notre expertise en <a href="{BASE}/loisirs-culture-et-evenementiel/">'
        f'propreté des lieux de loisirs, de culture et d\'événementiel</a>.</p>',
    "meilleure-entreprise-nettoyage-enseignement-petite-enfance-paris":
        f'<p>{MARKER}En complément, notre offre de <a href="{BASE}/enseignement-et-petite-enfance/">'
        f'nettoyage des établissements scolaires et de la petite enfance</a>.</p>',
    "meilleure-entreprise-nettoyage-fin-de-chantier-paris":
        f'<p>{MARKER}Retrouvez l\'ensemble de nos prestations de <a href="{BASE}/proprete-des-locaux/">'
        f'nettoyage de fin de chantier et de propreté des locaux</a>.</p>',
    "meilleure-entreprise-nettoyage-apres-sinistre-paris":
        f'<p>{MARKER}Découvrez aussi notre accompagnement pour la <a href="{BASE}/proprete-des-locaux/">'
        f'remise en état des locaux après sinistre</a>.</p>',
    "meilleure-entreprise-nettoyage-parkings-paris":
        f'<p>{MARKER}Voir également notre service de <a href="{BASE}/proprete-des-locaux/">'
        f'nettoyage des parkings et des parties communes</a>.</p>',
    "meilleure-entreprise-nettoyage-vitrines-paris":
        f'<p>{MARKER}En savoir plus sur le <a href="{BASE}/proprete-des-locaux/">'
        f'nettoyage des vitrines et des surfaces vitrées</a>.</p>',
}


def get_post(slug: str) -> dict | None:
    r = requests.get(f"{BASE}/wp-json/wp/v2/posts",
                     params={"slug": slug, "context": "edit", "_fields": "id,slug,content"},
                     auth=AUTH, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None


def apply_one(slug: str) -> str:
    if slug not in LINKS:
        return f"  ✗ {slug}: pas de lien défini"
    post = get_post(slug)
    if not post:
        return f"  ✗ {slug}: introuvable"
    raw = post["content"]["raw"]
    if MARKER in raw:
        return f"  ⏭  {slug}: déjà maillé (marqueur présent)"
    new_html = raw + "\n" + LINKS[slug]
    r = requests.post(f"{BASE}/wp-json/wp/v2/posts/{post['id']}",
                      json={"content": new_html}, auth=AUTH, timeout=30)
    if r.status_code not in (200, 201):
        return f"  ✗ {slug}: HTTP {r.status_code} {r.text[:120]}"
    return f"  ✓ {slug} (id={post['id']}) — lien contextuel ajouté"


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--slug")
    g.add_argument("--all", action="store_true")
    args = ap.parse_args()
    slugs = list(LINKS) if args.all else [args.slug]
    for s in slugs:
        print(apply_one(s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
