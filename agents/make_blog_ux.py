#!/usr/bin/env python3
"""Refonte UX/UI de lecture des articles de blog : injecte une feuille de style
'lecture' branded (typo Fraunces pour les titres, largeur de lecture confortable,
listes / citations / tableaux / images stylés, liens et accents orange).

Idempotent (marqueur spn-blog-ux). N'altère pas le contenu rédactionnel.
Usage : python3 agents/make_blog_ux.py
"""
from __future__ import annotations

import os
import requests

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
BASE = "https://spn-net.fr"
IDS = [2189, 2205, 2212, 2214, 2216, 2218, 2231, 2290, 2301, 2311, 2323, 2333]

W = ".elementor-widget-theme-post-content"
CSS = (
    "<!-- wp:html -->\n<!-- spn-blog-ux -->"
    '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">'
    "<style>"
    f"{W} .elementor-widget-container{{max-width:730px;margin-left:auto;margin-right:auto;font-family:'Plus Jakarta Sans',system-ui,sans-serif;font-size:1.08rem;line-height:1.75;color:#2A2D35}}"
    f"{W} p{{margin:0 0 1.15em}}"
    f"{W} h2,{W} h3,{W} h4{{font-family:'Fraunces',Georgia,serif;color:#16181D;letter-spacing:-.01em;line-height:1.18}}"
    f"{W} h2{{font-size:1.75rem;font-weight:600;margin:1.9em 0 .55em}}"
    f'{W} h2::before{{content:"";display:block;width:46px;height:4px;background:#ED5D37;border-radius:3px;margin-bottom:.55em}}'
    f"{W} h3{{font-size:1.32rem;font-weight:600;margin:1.6em 0 .45em}}"
    f"{W} a{{color:#D8431F;text-decoration:underline;text-underline-offset:2px;font-weight:600}}"
    f"{W} a:hover{{color:#16181D}}"
    f"{W} ul,{W} ol{{margin:0 0 1.25em;padding-left:0;list-style:none}}"
    f"{W} ul li{{position:relative;padding:.18em 0 .18em 1.7em}}"
    f'{W} ul li::before{{content:"";position:absolute;left:.1em;top:.72em;width:8px;height:8px;background:#ED5D37;border-radius:2px}}'
    f"{W} ol{{counter-reset:li}}"
    f"{W} ol li{{counter-increment:li;position:relative;padding:.18em 0 .18em 2.1em;margin-bottom:.2em}}"
    f'{W} ol li::before{{content:counter(li);position:absolute;left:0;top:.1em;width:1.5em;height:1.5em;background:#FFF1EA;color:#D8431F;border-radius:50%;font-weight:700;font-size:.82em;display:flex;align-items:center;justify-content:center}}'
    f"{W} blockquote{{margin:1.6em 0;padding:1.1em 1.4em;border-left:4px solid #ED5D37;background:#FAF8F5;border-radius:0 14px 14px 0;font-style:italic;color:#16181D}}"
    f"{W} blockquote p:last-child{{margin:0}}"
    f"{W} img{{border-radius:16px;height:auto}}"
    f"{W} table{{width:100%;border-collapse:collapse;margin:1.6em 0;font-size:.98rem}}"
    f"{W} th,{W} td{{padding:12px 15px;border-bottom:1px solid #E9E4DD;text-align:left;vertical-align:top}}"
    f"{W} th{{background:#FAF8F5;font-weight:700;color:#16181D}}"
    f"{W} strong,{W} b{{color:#16181D}}"
    f"{W} .elementor-widget-container > p:first-of-type{{font-size:1.24rem;line-height:1.6;color:#16181D;font-weight:500}}"
    "</style>\n<!-- /wp:html -->\n\n"
)


def main():
    for pid in IDS:
        try:
            r = requests.get(f"{BASE}/wp-json/wp/v2/posts/{pid}",
                             params={"context": "edit", "_fields": "content,slug"}, auth=AUTH, timeout=30).json()
            c = r["content"]["raw"]
            if "spn-blog-ux" in c:
                print(f"  ⏭ {pid} ({r['slug']}) déjà"); continue
            requests.post(f"{BASE}/wp-json/wp/v2/posts/{pid}", json={"content": CSS + c}, auth=AUTH, timeout=60).raise_for_status()
            print(f"  ✓ {pid} ({r['slug']})")
        except Exception as ex:  # noqa: BLE001
            print(f"  ✗ {pid}: {ex}")


if __name__ == "__main__":
    main()
