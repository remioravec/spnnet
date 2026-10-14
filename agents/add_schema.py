#!/usr/bin/env python3
"""Injecte le schema CleaningService + aggregateRating (JSON-LD) sur l'ensemble du
site : pages Elementor (ajout au 1er widget text-editor) et articles (bloc wp:html).

Idempotent (marqueur <!-- spn-schema -->). JSON-LD sur une seule ligne → insensible
à wpautop. Les 4 landing pages sont gérées à part (dans lp.html / make_variants.py).

Usage : python3 agents/add_schema.py
"""
from __future__ import annotations

import os
import pathlib
import sys

import requests

sys.path.insert(0, os.path.dirname(__file__))
from elementor_mcp import ElementorMCP  # noqa: E402

BASE = "https://spn-net.fr"
AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
SNIP = (pathlib.Path(__file__).parent / "schema" / "snippet.html").read_text()
MARK = "spn-schema"
LP_SLUGS = {"devis-nettoyage-bureaux-paris", "nettoyage-musee-theatre-evenementiel-paris",
            "nettoyage-hotel-restaurant-paris", "nettoyage-medical-sante-paris"}
EXCLUDE = LP_SLUGS | {"sitemap-html"}
ARTICLE_IDS = [2189, 2205, 2212, 2214, 2216, 2218, 2231, 2290, 2301, 2311, 2323, 2333]


def all_page_slugs() -> list[tuple[int, str]]:
    out = []
    page = 1
    while True:
        r = requests.get(f"{BASE}/wp-json/wp/v2/pages",
                         params={"per_page": 100, "page": page, "_fields": "id,slug,status"},
                         auth=AUTH, timeout=30)
        data = r.json()
        if not isinstance(data, list) or not data:
            break
        out += [(p["id"], p["slug"]) for p in data if p.get("status") == "publish"]
        if len(data) < 100:
            break
        page += 1
    return out


def inject_page(mcp: ElementorMCP, pid: int, slug: str) -> str:
    res = mcp.call("elementor-mcp-find-element", {"post_id": pid, "widgetType": "text-editor"})
    te = [w for w in res.get("parsed", res).get("matches", []) if w.get("widgetType") == "text-editor"]
    if not te:
        return f"  ⚠ {slug}: aucun widget text-editor (à traiter en widget HTML)"
    eid = te[0]["element_id"]
    s = mcp.call("elementor-mcp-get-element-settings", {"post_id": pid, "element_id": eid})
    ed = (s.get("parsed", s).get("settings", {}) or {}).get("editor", "")
    if MARK in ed:
        return f"  ⏭ {slug}: déjà présent"
    mcp.call("elementor-mcp-update-element",
             {"post_id": pid, "element_id": eid, "settings": {"editor": ed + SNIP}})
    return f"  ✓ {slug}"


def inject_post(pid: int) -> str:
    r = requests.get(f"{BASE}/wp-json/wp/v2/posts/{pid}",
                     params={"context": "edit", "_fields": "id,slug,content"}, auth=AUTH, timeout=30).json()
    ed = r["content"]["raw"]
    if MARK in ed:
        return f"  ⏭ post {pid}: déjà présent"
    block = "\n<!-- wp:html -->\n" + SNIP + "\n<!-- /wp:html -->"
    requests.post(f"{BASE}/wp-json/wp/v2/posts/{pid}", json={"content": ed + block}, auth=AUTH, timeout=30).raise_for_status()
    return f"  ✓ post {pid} ({r['slug']})"


def main() -> None:
    mcp = ElementorMCP(); mcp.initialize()
    print("=== PAGES ===")
    no_te = []
    for pid, slug in all_page_slugs():
        if slug in EXCLUDE:
            continue
        try:
            msg = inject_page(mcp, pid, slug)
            print(msg)
            if "aucun widget" in msg:
                no_te.append(slug)
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ {slug}: {e}")
    print("\n=== ARTICLES ===")
    for pid in ARTICLE_IDS:
        try:
            print(inject_post(pid))
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ post {pid}: {e}")
    if no_te:
        print(f"\n⚠ Pages sans text-editor (à traiter manuellement en widget HTML) : {no_te}")


if __name__ == "__main__":
    main()
