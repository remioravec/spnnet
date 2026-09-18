#!/usr/bin/env python3
"""Met à jour le reviewCount du schema déjà déployé (ex. 33 -> 48) sur l'ensemble
des pages Elementor et des articles. Remplacement ciblé et idempotent.

Usage : python3 agents/update_schema_count.py 33 48
"""
from __future__ import annotations

import os
import sys

import requests

sys.path.insert(0, os.path.dirname(__file__))
from elementor_mcp import ElementorMCP  # noqa: E402

BASE = "https://spn-net.fr"
AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
MARK = "spn-schema"
EXCLUDE = {"devis-nettoyage-bureaux-paris", "nettoyage-musee-theatre-evenementiel-paris",
           "nettoyage-hotel-restaurant-paris", "nettoyage-medical-sante-paris", "sitemap-html"}
ARTICLE_IDS = [2189, 2205, 2212, 2214, 2216, 2218, 2231, 2290, 2301, 2311, 2323, 2333]


def old_new(argv):
    o = argv[1] if len(argv) > 1 else "33"
    n = argv[2] if len(argv) > 2 else "48"
    return f'"reviewCount":"{o}"', f'"reviewCount":"{n}"'


def all_pages():
    out, page = [], 1
    while True:
        r = requests.get(f"{BASE}/wp-json/wp/v2/pages",
                         params={"per_page": 100, "page": page, "_fields": "id,slug,status"},
                         auth=AUTH, timeout=30).json()
        if not isinstance(r, list) or not r:
            break
        out += [(p["id"], p["slug"]) for p in r if p.get("status") == "publish"]
        if len(r) < 100:
            break
        page += 1
    return out


def main():
    OLD, NEW = old_new(sys.argv)
    mcp = ElementorMCP(); mcp.initialize()
    print(f"=== PAGES ({OLD} -> {NEW}) ===")
    for pid, slug in all_pages():
        if slug in EXCLUDE:
            continue
        try:
            res = mcp.call("elementor-mcp-find-element", {"post_id": pid, "widgetType": "text-editor"})
            for w in res.get("parsed", res).get("matches", []):
                eid = w["element_id"]
                s = mcp.call("elementor-mcp-get-element-settings", {"post_id": pid, "element_id": eid})
                ed = (s.get("parsed", s).get("settings", {}) or {}).get("editor", "")
                if MARK in ed and OLD in ed:
                    mcp.call("elementor-mcp-update-element",
                             {"post_id": pid, "element_id": eid, "settings": {"editor": ed.replace(OLD, NEW)}})
                    print(f"  ✓ {slug}")
                    break
            else:
                continue
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ {slug}: {e}")
    print("=== ARTICLES ===")
    for pid in ARTICLE_IDS:
        try:
            r = requests.get(f"{BASE}/wp-json/wp/v2/posts/{pid}",
                             params={"context": "edit", "_fields": "content,slug"}, auth=AUTH, timeout=30).json()
            ed = r["content"]["raw"]
            if MARK in ed and OLD in ed:
                requests.post(f"{BASE}/wp-json/wp/v2/posts/{pid}",
                              json={"content": ed.replace(OLD, NEW)}, auth=AUTH, timeout=30).raise_for_status()
                print(f"  ✓ post {pid} ({r['slug']})")
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ post {pid}: {e}")


if __name__ == "__main__":
    main()
