#!/usr/bin/env python3
"""Maillage retour page→article : ajoute dans chaque page secteur/service un lien
contextuel (ancre diversifiée) vers l'article de blog correspondant.

Le lien est ajouté à la fin du 1ᵉʳ widget « text-editor » (paragraphe d'intro),
donc en plein contenu. Idempotent (marqueur HTML).

Identifiants via l'environnement : WP_USER, WP_APP_PASSWORD.
Usage : python3 agents/apply_reverse_links.py --slug tertiaire | --all
"""
from __future__ import annotations

import argparse
import os
import sys

import requests

sys.path.insert(0, os.path.dirname(__file__))
from elementor_mcp import ElementorMCP  # noqa: E402

BASE = "https://spn-net.fr"
AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
MARKER = "<!-- spn-maillage-retour -->"

A = "meilleure-entreprise-nettoyage"  # préfixe des slugs d'articles

# page_slug → fragment HTML (lien(s) contextuel(s) à ancres diversifiées)
LINKS: dict[str, str] = {
    "tertiaire":
        f'<p>{MARKER}Pour aller plus loin, consultez notre guide : '
        f'<a href="{BASE}/{A}-tertiaire-paris/">comment bien choisir votre entreprise de nettoyage tertiaire à Paris</a>.</p>',
    "logistique-et-industrie":
        f'<p>{MARKER}À lire aussi : <a href="{BASE}/{A}-logistique-industrie-paris/">'
        f'bien choisir une société de nettoyage logistique et industriel</a>.</p>',
    "sante-et-medical":
        f'<p>{MARKER}Notre guide dédié : <a href="{BASE}/{A}-sante-medical-paris/">'
        f'le nettoyage des établissements de santé et médicaux à Paris</a>.</p>',
    "commerce-et-retail":
        f'<p>{MARKER}Pour approfondir : <a href="{BASE}/{A}-commerce-retail-paris/">'
        f'choisir un prestataire de nettoyage pour commerces et surfaces de vente</a>.</p>',
    "copropriete-et-habitat":
        f'<p>{MARKER}Voir aussi : <a href="{BASE}/{A}-copropriete-habitat-paris/">'
        f'bien sélectionner une entreprise de nettoyage en copropriété</a>.</p>',
    "hotellerie-et-restauration":
        f'<p>{MARKER}À découvrir : <a href="{BASE}/{A}-hotellerie-restauration-paris/">'
        f'le nettoyage en hôtellerie et restauration</a>.</p>',
    "loisirs-culture-et-evenementiel":
        f'<p>{MARKER}Notre guide : <a href="{BASE}/{A}-loisirs-culture-evenementiel-paris/">'
        f'le nettoyage des lieux de loisirs, de culture et d\'événementiel</a>.</p>',
    "enseignement-et-petite-enfance":
        f'<p>{MARKER}Pour en savoir plus : <a href="{BASE}/{A}-enseignement-petite-enfance-paris/">'
        f'le nettoyage des écoles et établissements de petite enfance</a>.</p>',
    "proprete-des-locaux":
        f'<p>{MARKER}Nos guides spécialisés : '
        f'<a href="{BASE}/{A}-fin-de-chantier-paris/">nettoyage de fin de chantier</a>, '
        f'<a href="{BASE}/{A}-apres-sinistre-paris/">remise en état après sinistre</a>, '
        f'<a href="{BASE}/{A}-parkings-paris/">nettoyage de parkings</a> et '
        f'<a href="{BASE}/{A}-vitrines-paris/">nettoyage de vitrines</a>.</p>',
}


def page_id(slug: str) -> int | None:
    r = requests.get(f"{BASE}/wp-json/wp/v2/pages",
                     params={"slug": slug, "_fields": "id"}, auth=AUTH, timeout=30).json()
    return r[0]["id"] if r else None


def first_text_editor(mcp: ElementorMCP, post_id: int) -> tuple[str, str] | None:
    res = mcp.call("elementor-mcp-find-element", {"post_id": post_id, "widgetType": "text-editor"})
    d = res.get("parsed", res)
    te = [m for m in d.get("matches", []) if m.get("widgetType") == "text-editor"]
    if not te:
        return None
    eid = te[0]["element_id"]
    s = mcp.call("elementor-mcp-get-element-settings", {"post_id": post_id, "element_id": eid})
    sd = s.get("parsed", s)
    editor = (sd.get("settings", {}) if isinstance(sd, dict) else {}).get("editor", "")
    return eid, editor


def apply_one(mcp: ElementorMCP, slug: str) -> str:
    if slug not in LINKS:
        return f"  ✗ {slug}: pas de lien défini"
    pid = page_id(slug)
    if not pid:
        return f"  ✗ {slug}: introuvable"
    found = first_text_editor(mcp, pid)
    if not found:
        return f"  ✗ {slug}: aucun widget text-editor"
    eid, editor = found
    if MARKER in editor:
        return f"  ⏭  {slug}: déjà maillé"
    new_editor = editor + LINKS[slug]
    mcp.call("elementor-mcp-update-element",
             {"post_id": pid, "element_id": eid, "settings": {"editor": new_editor}})
    return f"  ✓ {slug} (id={pid}, el={eid}) — lien(s) retour ajouté(s)"


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--slug")
    g.add_argument("--all", action="store_true")
    args = ap.parse_args()
    mcp = ElementorMCP()
    mcp.initialize()
    slugs = list(LINKS) if args.all else [args.slug]
    for s in slugs:
        try:
            print(apply_one(mcp, s))
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ {s}: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
