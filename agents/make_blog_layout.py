#!/usr/bin/env python3
"""Mise en page blog : hero d'article + colonne latérale STICKY (sommaire cliquable
généré depuis les H2, CTA devis, encart avis Google). Ancres ajoutées aux titres.

Idempotent (marqueur spn-blog-layout). À lancer APRÈS make_blog_ux / make_articles.
Usage : python3 agents/make_blog_layout.py [--restore]
"""
from __future__ import annotations

import os
import re
import unicodedata

import requests

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
BASE = "https://spn-net.fr"
GBP = "https://share.google/EHIcrr4rikijvXSJE"
IDS = [2189, 2205, 2212, 2214, 2216, 2218, 2231, 2290, 2301, 2311, 2323, 2333]

STYLE = """<style>
.elementor-widget-theme-post-content .elementor-widget-container{max-width:1140px!important;margin-left:auto;margin-right:auto}
.spn-blog-wrap{display:grid;grid-template-columns:minmax(0,1fr) 310px;gap:46px;align-items:start}
.spn-blog-main{min-width:0;max-width:760px}
.spn-blog-main h2{scroll-margin-top:100px}
.spn-blog-side{position:sticky;top:90px;display:flex;flex-direction:column;gap:16px;font-family:'Plus Jakarta Sans',system-ui,sans-serif}
.spn-toc{background:#fff;border:1px solid #E9E4DD;border-radius:16px;padding:20px}
.spn-toc .t{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:#9AA0A8;font-weight:700;margin:0 0 12px}
.spn-toc a{display:block;color:#2A2D35;text-decoration:none;font-weight:600;font-size:.9rem;padding:7px 0 7px 14px;border-left:2px solid #E9E4DD;transition:.15s;line-height:1.35}
.spn-toc a:hover,.spn-toc a.on{color:#D8431F;border-left-color:#ED5D37}
.spn-side-cta{background:#16181D;border-radius:16px;padding:22px}
.spn-side-cta h4{font-family:'Fraunces',Georgia,serif;font-size:1.25rem;margin:0 0 6px;color:#fff}
.spn-side-cta p{color:rgba(255,255,255,.7);font-size:.86rem;margin:0 0 14px}
.spn-side-cta a.b{display:block;text-align:center;background:linear-gradient(135deg,#F4794E,#D8431F);color:#fff;font-weight:700;padding:12px;border-radius:999px;text-decoration:none;margin-bottom:8px}
.spn-side-cta a.t{display:block;text-align:center;color:#fff;font-weight:700;text-decoration:none;font-size:1.05rem}
.spn-side-avis{background:#FAF8F5;border:1px solid #E9E4DD;border-radius:16px;padding:20px;text-align:center}
.spn-side-avis .n{font-size:1.7rem;font-weight:800;color:#16181D;font-family:'Fraunces',Georgia,serif;line-height:1}
.spn-side-avis .s{color:#FBBC05;letter-spacing:2px;font-size:1rem}
.spn-side-avis .p{font-size:.85rem;color:#6B7280;font-style:italic;margin:10px 0}
.spn-side-avis a{color:#D8431F;font-weight:700;text-decoration:none;font-size:.85rem}
.spn-blog-hero{border-bottom:1px solid #E9E4DD;padding-bottom:18px;margin-bottom:26px}
.spn-blog-hero .eb{display:inline-flex;align-items:center;gap:8px;font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#D8431F}
.spn-blog-hero .eb::before{content:"";width:24px;height:2px;background:#ED5D37;border-radius:2px}
.spn-blog-hero .meta{color:#9AA0A8;font-size:.85rem;margin-top:10px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.spn-blog-hero .pill{display:inline-flex;align-items:center;gap:6px;background:#FFF1EA;color:#D8431F;font-weight:700;padding:4px 11px;border-radius:999px}
@media(max-width:980px){.spn-blog-wrap{grid-template-columns:1fr}.spn-blog-side{position:static}.spn-toc{display:none}}
html{scroll-behavior:smooth}
</style>"""

TOC_JS = ("<script>(function(){var ls=[].slice.call(document.querySelectorAll('.spn-toc a'));"
          "if(!ls.length)return;var hs=ls.map(function(a){return document.getElementById(a.getAttribute('href').slice(1));});"
          "function on(){var y=window.scrollY+120,i=hs.length-1;for(var k=0;k<hs.length;k++){if(hs[k]&&hs[k].offsetTop<=y)i=k;}"
          "ls.forEach(function(a,j){a.classList.toggle('on',j===i);});}"
          "window.addEventListener('scroll',on,{passive:true});on();})();</script>")


def rtime(html):
    txt = re.sub(r"<[^>]+>", " ", html)
    n = len(txt.split())
    return max(2, round(n / 200))


def hero(mins):
    return ('<div class="spn-blog-hero"><span class="eb">Guide SPN NET</span>'
            f'<div class="meta"><span>⏱ {mins} min de lecture</span>'
            '<span class="pill">★ 4,8/5 · 48 avis Google</span>'
            '<span>Nettoyage professionnel · Paris &amp; Île-de-France</span></div></div>')


def sidebar(toc_links):
    toc = ""
    if toc_links:
        toc = ('<nav class="spn-toc"><p class="t">Sommaire</p>'
               + "".join(f'<a href="#{i}">{t}</a>' for i, t in toc_links) + "</nav>")
    cta = ('<div class="spn-side-cta"><h4>Un projet de nettoyage&nbsp;?</h4>'
           '<p>Devis gratuit sous 24h · sans engagement · ISO 45001.</p>'
           f'<a class="b" href="{BASE}/contact/">Demander un devis</a>'
           '<a class="t" href="tel:+33149462240">01 49 46 22 40</a></div>')
    avis = ('<div class="spn-side-avis"><div class="n">4,8/5</div>'
            '<div class="s">★★★★★</div>'
            '<div class="p">« Service très professionnel et fiable. Les équipes sont ponctuelles, discrètes et la qualité est toujours au rendez-vous. »</div>'
            f'<a href="{GBP}" target="_blank" rel="nofollow noopener">Voir nos 48 avis Google →</a></div>')
    return '<aside class="spn-blog-side">' + toc + cta + avis + "</aside>"


def add_anchors(content):
    links = []
    idx = [0]

    def repl(m):
        idx[0] += 1
        aid = f"s{idx[0]}"
        inner = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if inner:
            links.append((aid, inner))
        return f'<h2 id="{aid}"{m.group(1)}>{m.group(2)}</h2>'

    content = re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, content, flags=re.S)
    return content, links


def main():
    import sys
    restore = "--restore" in sys.argv
    for pid in IDS:
        try:
            r = requests.get(f"{BASE}/wp-json/wp/v2/posts/{pid}",
                             params={"context": "edit", "_fields": "content,slug"}, auth=AUTH, timeout=30).json()
            c = r["content"]["raw"]
            if restore:
                print(f"  (restore non géré automatiquement pour {pid})"); continue
            if "spn-blog-layout" in c:
                print(f"  ⏭ {pid} ({r['slug']}) déjà"); continue
            mins = rtime(c)
            c, links = add_anchors(c)
            open_blk = ("<!-- wp:html -->\n<!-- spn-blog-layout -->" + STYLE +
                        '<div class="spn-blog-wrap"><div class="spn-blog-main">' + hero(mins) +
                        "\n<!-- /wp:html -->\n\n")
            close_blk = ("\n<!-- wp:html -->\n</div>" + sidebar(links) + "</div>" + TOC_JS + "\n<!-- /wp:html -->\n")
            requests.post(f"{BASE}/wp-json/wp/v2/posts/{pid}", json={"content": open_blk + c + close_blk},
                          auth=AUTH, timeout=60).raise_for_status()
            print(f"  ✓ {pid} ({r['slug']}) · {len(links)} sections · {mins} min")
        except Exception as ex:  # noqa: BLE001
            print(f"  ✗ {pid}: {ex}")


if __name__ == "__main__":
    main()
