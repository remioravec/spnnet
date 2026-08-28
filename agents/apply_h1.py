#!/usr/bin/env python3
"""Corrige les H1 manquants des pages locales Elementor (stratégie « enrichir + promouvoir »).

Pour chaque page locale (paris-X, départements), le 2ᵉ titre (unique, en H3) est
promu en H1 et enrichi avec le mot-clé principal.
Ex. « Paris 1ᵉʳ » (H3) → « Entreprise de nettoyage – Paris 1er » (H1).

Identifiants via l'environnement : WP_USER, WP_APP_PASSWORD.
Usage :
  python3 agents/apply_h1.py --slug paris-1
  python3 agents/apply_h1.py --all
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

DEPTS = {
    "92-hauts-de-seine": "Hauts-de-Seine (92)",
    "93-seine-saint-denis": "Seine-Saint-Denis (93)",
    "94-val-de-marne": "Val-de-Marne (94)",
    "77-seine-et-marne": "Seine-et-Marne (77)",
    "78-yvelines": "Yvelines (78)",
    "91-essonne": "Essonne (91)",
    "95-val-doise": "Val-d'Oise (95)",
}


def arr(n: int) -> str:
    return "1er" if n == 1 else f"{n}e"


def h1_for(slug: str) -> str | None:
    if slug.startswith("paris-"):
        try:
            n = int(slug.split("-")[1])
        except ValueError:
            return None
        return f"Entreprise de nettoyage – Paris {arr(n)}"
    if slug in DEPTS:
        return f"Entreprise de nettoyage – {DEPTS[slug]}"
    return None


def all_local_slugs() -> list[str]:
    return [f"paris-{n}" for n in range(1, 21)] + list(DEPTS)


def page_id(slug: str) -> int | None:
    r = requests.get(f"{BASE}/wp-json/wp/v2/pages",
                     params={"slug": slug, "_fields": "id"}, auth=AUTH, timeout=30).json()
    return r[0]["id"] if r else None


def unique_heading_id(mcp: ElementorMCP, post_id: int) -> str | None:
    """Renvoie l'element_id du 2ᵉ titre (titre unique de la page)."""
    res = mcp.call("elementor-mcp-find-element", {"post_id": post_id, "widgetType": "heading"})
    d = res.get("parsed", res)
    headings = [m for m in d.get("matches", []) if m.get("widgetType") == "heading"]
    return headings[1]["element_id"] if len(headings) >= 2 else None


def apply_one(mcp: ElementorMCP, slug: str) -> str:
    new_h1 = h1_for(slug)
    if not new_h1:
        return f"  ✗ {slug}: pas de H1 défini"
    pid = page_id(slug)
    if not pid:
        return f"  ✗ {slug}: introuvable"
    eid = unique_heading_id(mcp, pid)
    if not eid:
        return f"  ✗ {slug}: titre unique introuvable"
    mcp.call("elementor-mcp-update-element",
             {"post_id": pid, "element_id": eid,
              "settings": {"header_size": "h1", "title": new_h1}})
    return f'  ✓ {slug} (id={pid}, el={eid}) → H1 « {new_h1} »'


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--slug")
    g.add_argument("--all", action="store_true")
    args = ap.parse_args()
    mcp = ElementorMCP()
    mcp.initialize()
    slugs = all_local_slugs() if args.all else [args.slug]
    for s in slugs:
        try:
            print(apply_one(mcp, s))
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ {s}: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
