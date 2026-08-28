#!/usr/bin/env python3
"""Applique des réécritures « lisibilité » (rédigées à la main, fidèles aux faits)
sur les pages Elementor (widgets text-editor) ou les articles classiques (post_content).

Les réécritures sont lues depuis :
  agents/rewrites/page_<id>.json   → {element_id: nouveau_html}   (page Elementor)
  agents/rewrites/post_<id>.json   → {"content": nouveau_html}    (article classique)

Réversible via les backups agents/backups/ (créés par dump_page.py).

Usage :
  python3 agents/apply_readability.py --page 413 --apply
  python3 agents/apply_readability.py --page 413 --restore
  python3 agents/apply_readability.py --post 2189 --apply
  python3 agents/apply_readability.py --post 2189 --restore
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, os.path.dirname(__file__))
from elementor_mcp import ElementorMCP  # noqa: E402

BASE = "https://spn-net.fr"
AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
HERE = Path(__file__).parent
REWRITES = HERE / "rewrites"
BACKUPS = HERE / "backups"


def apply_page(post_id: int, restore: bool) -> None:
    mcp = ElementorMCP(); mcp.initialize()
    if restore:
        data = json.loads((BACKUPS / f"page_{post_id}_text_editors.json").read_text())
    else:
        # Réécritures = un fichier HTML par widget : rewrites/page_<id>/<element_id>.html
        pdir = REWRITES / f"page_{post_id}"
        data = {f.stem: f.read_text() for f in sorted(pdir.glob("*.html"))}
    for eid, html in data.items():
        mcp.call("elementor-mcp-update-element",
                 {"post_id": post_id, "element_id": eid, "settings": {"editor": html}})
        print(f"  {'↩ restauré' if restore else '✓ réécrit'} {eid} ({len(html)} car.)")


def apply_post(post_id: int, restore: bool) -> None:
    if restore:
        html = json.loads((BACKUPS / f"post_{post_id}_content.json").read_text())["content"]
    else:
        html = (REWRITES / f"post_{post_id}.html").read_text()
    r = requests.post(f"{BASE}/wp-json/wp/v2/posts/{post_id}",
                      json={"content": html}, auth=AUTH, timeout=30)
    r.raise_for_status()
    print(f"  {'↩ restauré' if restore else '✓ réécrit'} post {post_id} ({len(html)} car.)")


def main() -> int:
    ap = argparse.ArgumentParser()
    sel = ap.add_mutually_exclusive_group(required=True)
    sel.add_argument("--page", type=int)
    sel.add_argument("--post", type=int)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--restore", action="store_true")
    args = ap.parse_args()
    if args.page:
        apply_page(args.page, args.restore)
    else:
        apply_post(args.post, args.restore)
    return 0


if __name__ == "__main__":
    sys.exit(main())
