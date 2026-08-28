#!/usr/bin/env python3
"""Sauvegarde + affiche le contenu des widgets text-editor d'une page Elementor
(ou le post_content d'un article classique), pour préparer une réécriture.

Backup écrit dans agents/backups/. Réversible ensuite.

Usage :
  python3 agents/dump_page.py --page 413            # page Elementor (text-editors)
  python3 agents/dump_page.py --post 2189           # article classique (post_content)
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
BACKUPS = Path(__file__).parent / "backups"


def dump_page(post_id: int) -> None:
    mcp = ElementorMCP(); mcp.initialize()
    res = mcp.call("elementor-mcp-find-element", {"post_id": post_id, "widgetType": "text-editor"})
    d = res.get("parsed", res)
    te = [m for m in d.get("matches", []) if m.get("widgetType") == "text-editor"]
    backup = {}
    for m in te:
        eid = m["element_id"]
        s = mcp.call("elementor-mcp-get-element-settings", {"post_id": post_id, "element_id": eid})
        sd = s.get("parsed", s)
        ed = (sd.get("settings", {}) if isinstance(sd, dict) else {}).get("editor", "")
        backup[eid] = ed
    BACKUPS.mkdir(exist_ok=True)
    (BACKUPS / f"page_{post_id}_text_editors.json").write_text(
        json.dumps(backup, ensure_ascii=False, indent=2))
    print(f"[backup page {post_id}: {len(backup)} widgets]")
    for eid, ed in backup.items():
        print(f"\n===== {eid} ({len(ed)} car.) =====\n{ed}")


def dump_post(post_id: int) -> None:
    r = requests.get(f"{BASE}/wp-json/wp/v2/posts/{post_id}",
                     params={"context": "edit", "_fields": "id,slug,content"}, auth=AUTH, timeout=30).json()
    raw = r["content"]["raw"]
    BACKUPS.mkdir(exist_ok=True)
    (BACKUPS / f"post_{post_id}_content.json").write_text(
        json.dumps({"slug": r["slug"], "content": raw}, ensure_ascii=False, indent=2))
    print(f"[backup post {post_id} ({r['slug']}): {len(raw)} car.]\n")
    print(raw)


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--page", type=int)
    g.add_argument("--post", type=int)
    args = ap.parse_args()
    if args.page:
        dump_page(args.page)
    else:
        dump_post(args.post)
    return 0


if __name__ == "__main__":
    sys.exit(main())
