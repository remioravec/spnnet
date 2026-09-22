#!/usr/bin/env python3
"""Correctif visuel de la mise en page blog : empêche les styles du corps d'article
de fuir dans la sidebar, rend la 2e colonne responsive au CONTENEUR (container query,
donc OK même si la colonne de contenu est étroite), évite les débordements.

Idempotent (marqueur spn-blog-fix). Usage : python3 agents/make_blog_fix.py
"""
from __future__ import annotations

import os
import requests

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
BASE = "https://spn-net.fr"
IDS = [2189, 2205, 2212, 2214, 2216, 2218, 2231, 2290, 2301, 2311, 2323, 2333]
W = ".elementor-widget-theme-post-content"

FIX = (
    "\n<!-- wp:html -->\n<!-- spn-blog-fix --><style>"
    f"{W} .elementor-widget-container{{container-type:inline-size}}"
    "@container (max-width:900px){.spn-blog-wrap{grid-template-columns:1fr!important;gap:26px!important}"
    ".spn-blog-side{position:static!important}.spn-toc{display:none!important}}"
    ".spn-blog-wrap{max-width:100%}.spn-blog-main{min-width:0}"
    ".spn-blog-side a{text-decoration:none!important}"
    ".spn-blog-side .spn-toc a{color:#2A2D35!important;font-weight:600!important;font-size:.9rem!important}"
    ".spn-blog-side .spn-toc a:hover,.spn-blog-side .spn-toc a.on{color:#D8431F!important}"
    ".spn-blog-side p{margin:0!important}.spn-blog-side ul li{padding:0!important}"
    ".spn-blog-side ul li::before{display:none!important}"
    ".spn-side-cta p{color:rgba(255,255,255,.7)!important}.spn-side-avis .p{font-style:italic!important}"
    "</style>\n<!-- /wp:html -->\n"
)


def main():
    for pid in IDS:
        try:
            r = requests.get(f"{BASE}/wp-json/wp/v2/posts/{pid}",
                             params={"context": "edit", "_fields": "content,slug"}, auth=AUTH, timeout=30).json()
            c = r["content"]["raw"]
            if "spn-blog-fix" in c:
                print(f"  ⏭ {pid} déjà"); continue
            requests.post(f"{BASE}/wp-json/wp/v2/posts/{pid}", json={"content": c + FIX}, auth=AUTH, timeout=60).raise_for_status()
            print(f"  ✓ {pid} ({r['slug']})")
        except Exception as ex:  # noqa: BLE001
            print(f"  ✗ {pid}: {ex}")


if __name__ == "__main__":
    main()
