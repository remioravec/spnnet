#!/usr/bin/env python3
"""Corrige le bug de mise en page des articles : le thème single-post a DÉJÀ une
sidebar (Contactez-nous), donc la grille/sidebar injectée créait des colonnes
imbriquées cassées. On retire la grille/sidebar (blocs spn-blog-layout / -side /
-fix) et on remet un SOMMAIRE cliquable + avis Google propre en haut d'article.

Conserve : typographie (spn-blog-ux), bloc 'Pour aller plus loin', schema, ancres.
Idempotent (spn-blog-clean). Usage : python3 agents/make_blog_clean.py
"""
from __future__ import annotations

import os
import re

import requests

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
BASE = "https://spn-net.fr"
GBP = "https://share.google/EHIcrr4rikijvXSJE"
IDS = [2189, 2205, 2212, 2214, 2216, 2218, 2231, 2290, 2301, 2311, 2323, 2333]
MARK = ("spn-blog-layout", "spn-blog-side", "spn-blog-fix")

STYLE = ("<style>"
         ".spn-sum{background:#FAF8F5;border:1px solid #E9E4DD;border-radius:16px;padding:20px 24px;margin:0 0 30px;font-family:'Plus Jakarta Sans',system-ui,sans-serif}"
         ".spn-sum .hd{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid #E9E4DD}"
         ".spn-sum .t{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:#9AA0A8;font-weight:700}"
         ".spn-sum .avis{display:inline-flex;align-items:center;gap:8px;font-weight:700;color:#16181D;font-size:.9rem}"
         ".spn-sum .avis .s{color:#FBBC05;letter-spacing:1px}"
         ".spn-sum .avis a{color:#D8431F;text-decoration:none}"
         ".spn-sum ol{list-style:none;counter-reset:s;margin:0;padding:0;columns:2;column-gap:26px}"
         ".spn-sum li{counter-increment:s;padding:5px 0;break-inside:avoid}"
         ".spn-sum a{color:#2A2D35;text-decoration:none;font-weight:600;font-size:.93rem;line-height:1.4}"
         ".spn-sum a:hover{color:#D8431F}"
         ".spn-sum ol a::before{content:counter(s) '. ';color:#ED5D37;font-weight:800}"
         "@media(max-width:600px){.spn-sum ol{columns:1}}"
         "html{scroll-behavior:smooth}"
         ".elementor-widget-theme-post-content h2{scroll-margin-top:100px}"
         "</style>")


def strip_my_blocks(content):
    parts = re.split(r"(<!-- wp:html -->.*?<!-- /wp:html -->)", content, flags=re.S)
    kept = []
    for p in parts:
        if p.startswith("<!-- wp:html -->") and any(m in p for m in MARK):
            continue
        kept.append(p)
    return "".join(kept)


def toc(content):
    links = re.findall(r'<h2[^>]*\bid="(s\d+)"[^>]*>(.*?)</h2>', content, flags=re.S)
    items = ""
    for aid, inner in links:
        txt = re.sub(r"<[^>]+>", "", inner).strip()
        if txt:
            items += f'<li><a href="#{aid}">{txt}</a></li>'
    if not items:
        return ""
    return ("<!-- wp:html -->\n<!-- spn-blog-clean -->" + STYLE +
            '<div class="spn-sum"><div class="hd"><span class="t">Au sommaire</span>'
            f'<span class="avis"><span class="s">★★★★★</span> 4,8/5 · <a href="{GBP}" target="_blank" rel="nofollow noopener">48 avis Google</a></span></div>'
            f'<ol>{items}</ol></div>\n<!-- /wp:html -->\n\n')


def main():
    for pid in IDS:
        try:
            r = requests.get(f"{BASE}/wp-json/wp/v2/posts/{pid}",
                             params={"context": "edit", "_fields": "content,slug"}, auth=AUTH, timeout=30).json()
            c = r["content"]["raw"]
            if "spn-blog-clean" in c:
                print(f"  ⏭ {pid} déjà"); continue
            c2 = strip_my_blocks(c)
            block = toc(c2)
            c2 = block + c2
            requests.post(f"{BASE}/wp-json/wp/v2/posts/{pid}", json={"content": c2}, auth=AUTH, timeout=60).raise_for_status()
            print(f"  ✓ {pid} ({r['slug']})")
        except Exception as ex:  # noqa: BLE001
            print(f"  ✗ {pid}: {ex}")


if __name__ == "__main__":
    main()
