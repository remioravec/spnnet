#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconstruit l'index /blog/ sur les articles reellement publies.

Fusionne les cartes des trois vagues (juillet, aout, septembre) et ne garde que
celles dont la page existe en ligne. Passe par make_zone.deploy(), qui pose le
wrapper wp:html : sans lui WordPress injecte des <p> dans le CSS et le JS.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import requests
import make_special as ms
import make_zone as mz
from make_blog_aout import BLOG_CARDS as CARDS_AOUT
from make_juillet import BLOG_CARDS_JUILLET as CARDS_JUIL
from make_septembre import BLOG_CARDS_SEPT as CARDS_SEPT
from make_octobre import BLOG_CARDS_OCT as CARDS_OCT

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
PAGES = "https://spn-net.fr/wp-json/wp/v2/pages"


def main():
    cards = list(CARDS_OCT) + list(CARDS_SEPT) + list(CARDS_AOUT) + list(CARDS_JUIL)
    seen, ordered = set(), []
    for c in cards:
        if c[0] not in seen:
            seen.add(c[0]); ordered.append(c)
    live = []
    for c in ordered:
        r = requests.get(PAGES, params={"slug": c[0], "status": "publish", "_fields": "id"},
                         auth=AUTH, timeout=40).json()
        if r:
            live.append(c)
        else:
            print(f"  absente, ecartee : {c[0]}")
    ms.POSTS[:] = live
    print(f"  index /blog/ : {len(live)} article(s) publie(s)")
    print(mz.deploy("blog", ms.CFG["blog"], builder=ms.build, prefix="special"))


if __name__ == "__main__":
    main()
