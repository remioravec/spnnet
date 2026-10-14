#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chaque notification de demande s'annonce comme venant de Google Ads.

Le script d'envoi des formulaires a ete ecrit pour la landing Ads, puis
recopie sur tout le site. Resultat : le corps du message que recoit
Alexandra se termine par « Demande de devis via la landing page Google
Ads », et le referer_title commence par « Landing Ads — », y compris sur
les 55 pages qui ne sont pas des landings Ads. Le canal reel est donc
illisible dans l'e-mail, alors qu'il est juste dans l'outil Demandes.

Les 4 vraies landings Ads (noindex, hors sitemap) gardent leur etiquette :
  devis-nettoyage-bureaux-paris · nettoyage-hotel-restaurant-paris
  nettoyage-medical-sante-paris · nettoyage-musee-theatre-evenementiel-paris

Usage : python3 agents/landing/corriger_etiquette_source.py [--dry]
"""
from __future__ import annotations

import base64
import json
import os
import sys
import urllib.request

API = "https://spn-net.fr/wp-json/wp/v2"
AUTH = base64.b64encode(
    f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()

ADS = {"devis-nettoyage-bureaux-paris", "nettoyage-hotel-restaurant-paris",
       "nettoyage-medical-sante-paris", "nettoyage-musee-theatre-evenementiel-paris"}

SUBS = [
    ("'— Demande de devis via la landing page Google Ads (' + document.title + ').'",
     "'— Demande envoyée depuis la page ' + document.title + ' (' + location.pathname + ').'"),
    ("'Landing Ads — ' + document.title",
     "document.title"),
    ("'Landing Ads — ' + document.title",
     "document.title"),
]


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
        pg = 1
        while True:
            items = call(f"{API}/{ep}?per_page=100&page={pg}"
                         "&status=publish,draft,future,private&context=edit"
                         "&_fields=id,slug,content")
            if not items:
                break
            for it in items:
                html = it["content"]["raw"]
                if it["slug"] in ADS or "Google Ads" not in html:
                    continue
                new, k = html, 0
                for a, b in SUBS:
                    if a in new:
                        k += new.count(a)
                        new = new.replace(a, b)
                if not k:
                    continue
                n += 1
                print(f"  {it['slug']:46} {k} remplacement(s)"
                      + ("  [simulation]" if dry else ""))
                if dry:
                    continue
                call(f"{API}/{ep}/{it['id']}",
                     {"content": "<!-- wp:html -->\n" + new + "\n<!-- /wp:html -->",
                      "template": "elementor_header_footer",
                      "meta": {"_elementor_edit_mode": ""}}, "POST")
            if len(items) < 100:
                break
            pg += 1
    print(f"\n{n} pages corrigées · les 4 landings Ads conservent leur étiquette")


if __name__ == "__main__":
    main()
