#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le gabarit d'article ne stylait pas ses tableaux.

Les tableaux de synthese des articles sortaient sans bordure ni en-tete :
le CSS .tbl du site est scope .spn-lp, pas .spn-art. Le correctif vit
desormais dans visuels.py ; ce script le pose sur les pages deja en ligne.

Idempotent : la presence de « .spn-art .tbl{ » suffit a ecarter la page.
Le CSS se pose DANS la balise style existante, et l'ecriture passe par
wp:html, sinon wpautop injecte des <p> dedans.

Usage : python3 agents/landing/poser_css_tableau.py [--dry]
"""
from __future__ import annotations

import base64
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
import visuels as vz   # noqa: E402

API = "https://spn-net.fr/wp-json/wp/v2"
AUTH = base64.b64encode(
    f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()

BLOC = re.search(r"(/\* tableaux du corps d'article.*?)\n\.spn-art \.vz-g4",
                 vz.EXTRA, re.S).group(1)


def call(url, data=None, method="GET"):
    r = urllib.request.Request(url, method=method,
                               data=json.dumps(data).encode() if data else None)
    r.add_header("Authorization", "Basic " + AUTH)
    if data:
        r.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(r, timeout=120) as f:
        return json.loads(f.read().decode())


def main():
    dry = "--dry" in sys.argv
    n = 0
    for ep in ("pages", "posts"):
        page = 1
        while True:
            items = call(f"{API}/{ep}?per_page=100&page={page}"
                         "&status=publish,draft,future,private&context=edit"
                         "&_fields=id,slug,content")
            if not items:
                break
            for it in items:
                html = it["content"]["raw"]
                if 'class="tbl"' not in html or 'class="spn-art"' not in html:
                    continue
                if ".spn-art .tbl{" in html:
                    print(f"  {it['slug']:46} deja pose")
                    continue
                if "</style>" not in html:
                    print(f"  {it['slug']:46} AUCUNE BALISE STYLE")
                    continue
                new = html.replace("</style>", BLOC + "</style>", 1)
                n += 1
                print(f"  {it['slug']:46} CSS tableau posé"
                      + ("  [simulation]" if dry else ""))
                if dry:
                    continue
                call(f"{API}/{ep}/{it['id']}",
                     {"content": "<!-- wp:html -->\n" + new + "\n<!-- /wp:html -->",
                      "template": "elementor_header_footer",
                      "meta": {"_elementor_edit_mode": ""}}, "POST")
            if len(items) < 100:
                break
            page += 1
    print(f"\n{n} pages corrigées")


if __name__ == "__main__":
    main()
