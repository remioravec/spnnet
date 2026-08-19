#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gabarit d'article de blog branché (DA du site) — corps en 2 colonnes,
CTA en SIDEBAR sticky (pas dans le hero).

Les articles (contenu défini dans make_blog_aout.ARTICLES) sont rendus comme
les autres pages du site : template en-tête/pied, contenu custom (edit_mode="").
Pour maîtriser le rendu (le gabarit 'post' du thème impose sa propre sidebar),
chaque article POST est converti en PAGE au même slug.

Usage : python3 agents/landing/make_article.py            # gabarit + convert + index /blog/
        python3 agents/landing/make_article.py --blog      # reconstruit seulement /blog/
"""
from __future__ import annotations

import os
import re
import sys
import datetime
import unicodedata

import requests

sys.path.insert(0, os.path.dirname(__file__))
from make_blog_aout import ARTICLES, CSS as BLOGCSS, _faq_block, _faq_schema, BLOG_CARDS  # noqa: E402

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
POSTS = "https://spn-net.fr/wp-json/wp/v2/posts"
PAGES = "https://spn-net.fr/wp-json/wp/v2/pages"
NOW = datetime.datetime(2026, 8, 19, 12, 30)
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]

TAGS = {c[0]: c[1] for c in BLOG_CARDS}

ART_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,500&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
.spn-art{--orange:#ED5D37;--orange-deep:#D8431F;--orange-soft:#FFF1EA;--ink:#16181D;--ink-2:#2A2D35;--grey:#5b616b;--line:#E9E4DD;--cream:#FAF8F5;--r:18px;--shadow:0 18px 40px -22px rgba(22,24,29,.28);font-family:'Plus Jakarta Sans',system-ui,sans-serif;color:var(--ink);line-height:1.65}
.spn-art *{box-sizing:border-box}
.spn-art .wrap{max-width:1120px;margin:0 auto;padding:0 24px}
.spn-art a{color:var(--orange-deep)}
.spn-art .art-hero{background:linear-gradient(180deg,var(--cream),#fff);border-bottom:1px solid var(--line);padding:34px 0 30px}
.spn-art .crumbs{font-size:.82rem;color:var(--grey);margin-bottom:14px}
.spn-art .crumbs a{color:var(--grey);text-decoration:none}.spn-art .crumbs a:hover{color:var(--orange-deep)}
.spn-art .eyebrow{display:inline-block;font-size:.72rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--orange-deep);background:var(--orange-soft);padding:5px 13px;border-radius:999px}
.spn-art h1{font-family:'Fraunces',serif;font-weight:600;font-size:clamp(1.8rem,4vw,2.9rem);line-height:1.1;letter-spacing:-.015em;margin:14px 0 0;max-width:20ch}
.spn-art .art-meta{display:flex;flex-wrap:wrap;gap:16px;margin-top:16px;font-size:.86rem;color:var(--grey);font-weight:600}
.spn-art .art-meta .rate b{color:var(--ink)}.spn-art .art-meta .s{color:#FBBC05;letter-spacing:1px}
.spn-art .art-body{padding:40px 0 60px}
.spn-art .art-grid{display:grid;grid-template-columns:1fr 330px;gap:48px;align-items:start}
.spn-art .art-main{min-width:0}
/* sidebar */
.spn-art .art-side{position:sticky;top:86px;display:flex;flex-direction:column;gap:18px}
.spn-art .cta-card{background:var(--ink);color:#fff;border-radius:var(--r);padding:26px 24px;box-shadow:var(--shadow);position:relative;overflow:hidden}
.spn-art .cta-card::before{content:"";position:absolute;inset:0;background:radial-gradient(360px 180px at 100% -20%,rgba(237,93,55,.55),transparent 60%)}
.spn-art .cta-card>*{position:relative}
.spn-art .cta-card .rate{font-size:.82rem;font-weight:700;color:#fff}.spn-art .cta-card .rate .s{color:#FBBC05;letter-spacing:1px}
.spn-art .cta-card h3{font-family:'Fraunces',serif;font-weight:600;font-size:1.5rem;margin:12px 0 6px;line-height:1.15}
.spn-art .cta-card p{font-size:.9rem;color:rgba(255,255,255,.82);margin:0 0 16px}
.spn-art .cta-card .btn{display:block;text-align:center;background:linear-gradient(135deg,#F4794E,#D8431F);color:#fff;font-weight:700;text-decoration:none;padding:13px 18px;border-radius:999px}
.spn-art .cta-card .btn:hover{filter:brightness(1.06)}
.spn-art .cta-card .tel{display:block;text-align:center;color:#fff;font-weight:800;font-size:1.1rem;text-decoration:none;margin-top:14px}
.spn-art .cta-card .badges{margin-top:16px;padding-top:14px;border-top:1px solid rgba(255,255,255,.16);font-size:.75rem;font-weight:700;letter-spacing:.04em;color:rgba(255,255,255,.7);text-align:center}
.spn-art .side-toc{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:20px 22px}
.spn-art .side-toc b{display:block;font-size:.72rem;text-transform:uppercase;letter-spacing:.07em;color:var(--grey);margin-bottom:10px}
.spn-art .side-toc ol{margin:0;padding-left:18px}.spn-art .side-toc li{margin-bottom:7px}
.spn-art .side-toc a{color:var(--ink-2);text-decoration:none;font-size:.9rem;font-weight:600}.spn-art .side-toc a:hover{color:var(--orange-deep)}
@media(max-width:900px){.spn-art .art-grid{grid-template-columns:1fr;gap:28px}.spn-art .art-side{position:static;order:2}}
/* typo article (réutilise .spnblog mais scopée sous .spn-art) */
.spn-art .art-main .lead{font-size:1.12rem;color:var(--ink-2);font-weight:500;line-height:1.6}
.spn-art .art-main h2{font-family:'Fraunces',serif;font-weight:600;font-size:1.5rem;line-height:1.2;margin:34px 0 12px;letter-spacing:-.01em}
.spn-art .art-main h2:first-child{margin-top:0}
.spn-art .art-main p{margin:0 0 16px}
.spn-art .art-main ul{margin:0 0 18px;padding-left:22px}.spn-art .art-main li{margin-bottom:9px}
.spn-art .art-main strong{color:var(--ink)}
.spn-art .art-main .faq details{border:1px solid var(--line);border-radius:12px;padding:4px 18px;margin-bottom:10px;background:#fff}
.spn-art .art-main .faq summary{cursor:pointer;font-weight:700;padding:12px 0;list-style:none}
.spn-art .art-main .faq summary::-webkit-details-marker{display:none}
.spn-art .art-main .faq summary::after{content:"+";float:right;color:var(--orange-deep);font-weight:800}
.spn-art .art-main .faq details[open] summary::after{content:"–"}
</style>"""


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def fr_date(iso):
    d = datetime.datetime.fromisoformat(iso)
    return f"{d.day} {MOIS[d.month - 1]} {d.year}"


def reading_time(html):
    words = len(re.sub(r"<[^>]+>", " ", html).split())
    return max(2, round(words / 200))


def article_schema(a):
    node = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": a["title"], "description": a["desc"],
        "datePublished": a["date"], "dateModified": a["date"],
        "author": {"@type": "Organization", "name": "SPN NET"},
        "publisher": {"@type": "Organization", "name": "SPN NET",
                      "logo": {"@type": "ImageObject", "url": "https://spn-net.fr/wp-content/uploads/elementor/thumbs/logo-rkamhcg62qbiqacow1pw230in940ue5954a7aysbu0.png"}},
        "mainEntityOfPage": f"https://spn-net.fr/{a['slug']}/",
    }
    import json
    return '<script type="application/ld+json">' + json.dumps(node, ensure_ascii=False) + "</script>"


def breadcrumb(a):
    short = a["title"].split(":")[0].strip()
    return ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
            '{"@type":"ListItem","position":1,"name":"Accueil","item":"https://spn-net.fr/"},'
            '{"@type":"ListItem","position":2,"name":"Blog","item":"https://spn-net.fr/blog/"},'
            f'{{"@type":"ListItem","position":3,"name":"{strip_accents(short)}"}}]}}</script>')


CTA_CARD = (
    '<div class="cta-card">'
    '<div class="rate"><span class="s">★★★★★</span> 4,8/5 · 48 avis Google</div>'
    '<h3>Un projet de nettoyage&nbsp;?</h3>'
    '<p>Devis gratuit sous 24&nbsp;h, sans engagement. On vous répond en moins de 4&nbsp;h ouvrées.</p>'
    '<a class="btn" href="https://spn-net.fr/contact/">Demander un devis →</a>'
    '<a class="tel" href="tel:+33149462240">01 49 46 22 40</a>'
    '<div class="badges">ISO 45001 · EcoVadis Argent · 30 ans</div>'
    '</div>'
)


def build_article(a):
    body = a["body"]
    # extraire le sommaire du corps pour le passer en sidebar
    m = re.search(r'<div class="toc">.*?</div>\s*', body, re.S)
    toc_inner = ""
    if m:
        oo = re.search(r"<ol>.*?</ol>", m.group(0), re.S)
        toc_inner = oo.group(0) if oo else ""
        body = body.replace(m.group(0), "", 1)
    side_toc = f'<div class="side-toc"><b>Au sommaire</b>{toc_inner}</div>' if toc_inner else ""

    hero = (
        '<div class="art-hero"><div class="wrap">'
        '<nav class="crumbs"><a href="https://spn-net.fr/">Accueil</a> › '
        '<a href="https://spn-net.fr/blog/">Blog</a> › <span>' + strip_accents(a["title"].split(":")[0].strip()) + '</span></nav>'
        f'<span class="eyebrow">{TAGS.get(a["slug"], "Guide")}</span>'
        f'<h1>{a["title"]}</h1>'
        '<div class="art-meta">'
        f'<span>📅 {fr_date(a["date"])}</span>'
        f'<span>⏱ {reading_time(body)} min de lecture</span>'
        '<span class="rate"><span class="s">★</span> <b>4,8/5</b> · 48 avis</span>'
        '</div></div></div>'
    )
    main = '<article class="art-main">' + body + _faq_block(a["faq"]) + '</article>'
    side = '<aside class="art-side">' + CTA_CARD + side_toc + '</aside>'
    schema = _faq_schema(a["faq"]) + article_schema(a) + breadcrumb(a)
    return (ART_CSS + '<div class="spn-art">' + hero
            + '<div class="art-body"><div class="wrap art-grid">' + main + side + '</div></div>'
            + schema + '</div>')


def convert(a):
    """Supprime le POST éventuel et (ré)écrit une PAGE branchée au même slug."""
    status = "publish" if datetime.datetime.fromisoformat(a["date"]) <= NOW else "future"
    # 1) supprimer le post du même slug (libère le slug)
    p = requests.get(POSTS, params={"slug": a["slug"], "status": "publish,future,draft", "_fields": "id"}, auth=AUTH, timeout=30).json()
    for x in p:
        requests.delete(f"{POSTS}/{x['id']}", params={"force": "true"}, auth=AUTH, timeout=40)
    # 2) créer / mettre à jour la page
    html = build_article(a)
    content = "<!-- wp:html -->\n" + html + "\n<!-- /wp:html -->"
    payload = {"title": a["title"], "slug": a["slug"], "status": status, "date": a["date"],
               "content": content, "template": "elementor_header_footer", "excerpt": a["desc"],
               "meta": {"_elementor_edit_mode": "", "slim_seo": {"title": a["seo_title"], "description": a["desc"], "noindex": False}}}
    ex = requests.get(PAGES, params={"slug": a["slug"], "status": "publish,future,draft", "_fields": "id"}, auth=AUTH, timeout=30).json()
    url = f"{PAGES}/{ex[0]['id']}" if ex else PAGES
    r = requests.post(url, auth=AUTH, timeout=90, json=payload)
    r.raise_for_status()
    j = r.json()
    return f"  {'✓' if status == 'publish' else '⏳'} [{status}] {j.get('link')}"


def rebuild_blog():
    """Index /blog/ : liste les articles réellement publiés (pages)."""
    import make_special as ms
    import make_zone as mz
    live = []
    for c in BLOG_CARDS:
        r = requests.get(PAGES, params={"slug": c[0], "status": "publish", "_fields": "id"}, auth=AUTH, timeout=30).json()
        if r:
            live.append(c)
    ms.POSTS[:] = live
    print(f"  index /blog/ : {len(live)} article(s) publié(s)")
    print(mz.deploy("blog", ms.CFG["blog"], builder=ms.build, prefix="special"))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--blog":
        rebuild_blog()
        return
    for a in ARTICLES:
        try:
            print(convert(a))
        except Exception as ex:  # noqa: BLE001
            print(f"  ✗ {a['slug']}: {ex}")
    rebuild_blog()


if __name__ == "__main__":
    main()
