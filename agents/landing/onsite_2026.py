#!/usr/bin/env python3
"""Optimisations on-site 2026 (méthode 20/80) — appliquées sur spn-net.fr.

Deux chantiers « cœur » exécutés et réversibles :

1) Dédoublonnage (anti-cannibalisation)
   Les articles /societe-nettoyage-bureaux-paris-{2,12}/ ciblaient la même
   requête money que les pages zones /paris-{2,12}/. On pose un rel=canonical
   (Slim SEO) des articles vers les pages zones → consolidation du signal,
   sans 301 (pas de plugin de redirection installé). Réversible : retirer la
   clé 'canonical' de la meta slim_seo.

2) Schema Service + areaServed par page zone
   Chaque page /paris-N/ et /<dept>/ reçoit un noeud JSON-LD Service
   (serviceType « Nettoyage de bureaux ») rattaché à l'entité globale
   #business (provider @id), avec areaServed = la zone précise
   (City + code postal pour Paris, AdministrativeArea pour les départements).
   Idempotent (marqueur <!-- spn-zone-schema -->).

Usage :
    export WP_USER=... WP_APP_PASSWORD=...
    python3 agents/landing/onsite_2026.py canonical
    python3 agents/landing/onsite_2026.py schema
    python3 agents/landing/onsite_2026.py all
"""
from __future__ import annotations

import json
import os
import re
import sys

import requests

import zones_data as z

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
BASE = "https://spn-net.fr/wp-json/wp/v2"

# Doublons -> page zone canonique
CANONICALS = {
    "societe-nettoyage-bureaux-paris-2": "https://spn-net.fr/paris-2/",
    "societe-nettoyage-bureaux-paris-12": "https://spn-net.fr/paris-12/",
}

MARK = re.compile(r"<!-- spn-zone-schema -->.*?<!-- /spn-zone-schema -->\s*", re.S)


def set_canonicals() -> None:
    for slug, canon in CANONICALS.items():
        r = requests.get(f"{BASE}/posts", auth=AUTH,
                         params={"slug": slug, "context": "edit", "_fields": "id,meta"}, timeout=40)
        rows = r.json()
        if not rows:
            print(f"  ? {slug}: article introuvable"); continue
        pid = rows[0]["id"]
        ss = dict((rows[0].get("meta", {}) or {}).get("slim_seo", {}) or {})
        ss["canonical"] = canon
        w = requests.post(f"{BASE}/posts/{pid}", auth=AUTH, timeout=60, json={"meta": {"slim_seo": ss}})
        print(f"  {'✓' if w.status_code == 200 else '✗'} {slug} → canonical {canon}")


def _area_served(slug: str, name: str) -> dict:
    m = re.search(r"\((750\d\d)\)", z.ALL_ZONES[slug]["h1"])
    if m:  # arrondissement parisien
        return {"@type": "City", "name": name,
                "containedInPlace": {"@type": "City", "name": "Paris"},
                "address": {"@type": "PostalAddress", "postalCode": m.group(1),
                            "addressLocality": "Paris", "addressRegion": "Île-de-France",
                            "addressCountry": "FR"}}
    return {"@type": "AdministrativeArea", "name": name,
            "address": {"@type": "PostalAddress", "addressRegion": "Île-de-France",
                        "addressCountry": "FR"}}


def _service_block(slug: str, name: str, link: str) -> str:
    node = {
        "@context": "https://schema.org", "@type": "Service",
        "serviceType": "Nettoyage de bureaux", "name": f"Nettoyage de bureaux à {name}",
        "provider": {"@type": "CleaningService", "@id": "https://spn-net.fr/#business",
                     "name": "SPN NET", "telephone": "+33149462240", "url": "https://spn-net.fr/"},
        "areaServed": _area_served(slug, name), "url": link,
    }
    return ('<!-- spn-zone-schema -->\n<script type="application/ld+json">'
            + json.dumps(node, ensure_ascii=False) + "</script>\n<!-- /spn-zone-schema -->")


def inject_schema() -> None:
    for slug, v in z.ALL_ZONES.items():
        r = requests.get(f"{BASE}/pages", auth=AUTH,
                         params={"slug": slug, "context": "edit", "_fields": "id,link,content"}, timeout=40)
        rows = r.json()
        if not rows:
            print(f"  ? {slug}: page absente"); continue
        pg = rows[0]
        raw = pg["content"]["raw"]
        block = _service_block(slug, v["name"], pg["link"])
        out = MARK.sub("", raw)
        if "<!-- /wp:html -->" in out:
            out = out.replace("<!-- /wp:html -->", block + "\n<!-- /wp:html -->", 1)
        else:
            out = out + "\n" + block
        if out == raw:
            print(f"  = {slug}: inchangé"); continue
        w = requests.post(f"{BASE}/pages/{pg['id']}", auth=AUTH, timeout=90, json={"content": out})
        print(f"  {'✓' if w.status_code == 200 else '✗'} {slug}")


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd in ("canonical", "all"):
        print("— Dédoublonnage (canonical) —"); set_canonicals()
    if cmd in ("schema", "all"):
        print("— Schema Service + areaServed —"); inject_schema()
    if cmd not in ("canonical", "schema", "all"):
        print(__doc__)


if __name__ == "__main__":
    main()
