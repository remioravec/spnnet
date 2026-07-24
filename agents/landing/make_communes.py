#!/usr/bin/env python3
"""Crée + déploie les 13 pages communes 92/94 (net-new) autour de Bagneux.

Réutilise le moteur de make_zone (build/deploy) avec les données locales réelles
de communes_data.COMMUNES. Chaque page : publiée, indexable, template
en-tête/pied, contenu local unique + schema Service/areaServed (City + CP).

Usage :
  python3 agents/landing/make_communes.py --all
  python3 agents/landing/make_communes.py montrouge bagneux
  python3 agents/landing/make_communes.py --restore montrouge
"""
from __future__ import annotations

import json
import os
import re
import sys
import pathlib

import requests

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import make_zone as mz  # noqa: E402
from communes_data import COMMUNES  # noqa: E402

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
API = "https://spn-net.fr/wp-json/wp/v2/pages"


def ensure_page(slug: str, c: dict) -> int:
    """Crée la page si elle n'existe pas encore ; renvoie son id."""
    pid = mz.get_page_id(slug)
    if pid:
        return pid
    payload = {"title": c["name"], "slug": slug, "status": "publish",
               "content": "…", "template": "elementor_header_footer",
               "meta": {"slim_seo": {"title": c["title"], "description": c["desc"], "noindex": False}}}
    r = requests.post(API, auth=AUTH, timeout=90, json=payload)
    r.raise_for_status()
    return r.json()["id"]


def service_schema(c: dict, link: str) -> str:
    dept = ("Hauts-de-Seine", "Île-de-France") if c["cp"].startswith("92") else ("Val-de-Marne", "Île-de-France")
    node = {
        "@context": "https://schema.org", "@type": "Service",
        "serviceType": "Nettoyage de bureaux", "name": f"Nettoyage de bureaux à {c['name']}",
        "provider": {"@type": "CleaningService", "@id": "https://spn-net.fr/#business",
                     "name": "SPN NET", "telephone": "+33149462240", "url": "https://spn-net.fr/"},
        "areaServed": {"@type": "City", "name": c["name"],
                       "containedInPlace": {"@type": "AdministrativeArea", "name": dept[0]},
                       "address": {"@type": "PostalAddress", "postalCode": c["cp"],
                                   "addressLocality": c["name"], "addressRegion": dept[1],
                                   "addressCountry": "FR"}},
        "url": link,
    }
    return ('<!-- spn-zone-schema -->\n<script type="application/ld+json">'
            + json.dumps(node, ensure_ascii=False) + "</script>\n<!-- /spn-zone-schema -->")


MARK = re.compile(r"<!-- spn-zone-schema -->.*?<!-- /spn-zone-schema -->\s*", re.S)


def inject_schema(slug: str, c: dict) -> str:
    r = requests.get(API, auth=AUTH, params={"slug": slug, "context": "edit", "_fields": "id,link,content"}, timeout=40)
    pg = r.json()[0]
    raw = pg["content"]["raw"]
    block = service_schema(c, pg["link"])
    out = MARK.sub("", raw)
    if "<!-- /wp:html -->" in out:
        out = out.replace("<!-- /wp:html -->", block + "\n<!-- /wp:html -->", 1)
    else:
        out = out + "\n" + block
    w = requests.post(f"{API}/{pg['id']}", auth=AUTH, timeout=90, json={"content": out})
    return "schema✓" if w.status_code == 200 else f"schema✗{w.status_code}"


def do(slug: str, c: dict) -> str:
    ensure_page(slug, c)
    msg = mz.deploy(slug, c, builder=mz.build, prefix="commune")
    sch = inject_schema(slug, c)
    return f"{msg}  [{sch}]"


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__); return
    if args[0] == "--restore":
        for slug in args[1:]:
            print(mz.restore(slug))
        return
    slugs = list(COMMUNES.keys()) if args[0] == "--all" else args
    for slug in slugs:
        c = COMMUNES.get(slug)
        if not c:
            print(f"  ? {slug}: pas de données"); continue
        try:
            print(do(slug, c))
        except Exception as ex:  # noqa: BLE001
            print(f"  ✗ {slug}: {ex}")


if __name__ == "__main__":
    main()
