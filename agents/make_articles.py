#!/usr/bin/env python3
"""Refonte structurelle des articles de blog : ajoute un bloc de fin d'article
'Pour aller plus loin' (maillage vers la page mère du secteur + zones + CTA devis).
Idempotent (marqueur spn-art-more). N'altère pas le contenu rédactionnel existant.

Usage : python3 agents/make_articles.py
"""
from __future__ import annotations

import os
import requests

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
BASE = "https://spn-net.fr"

# id -> (secteur_slug, secteur_label, [(zone_slug, zone_label), ...])
ART = {
    2189: ("tertiaire", "bureaux & tertiaire", [("paris-8", "Paris 8e"), ("92-hauts-de-seine", "les Hauts-de-Seine")]),
    2205: ("logistique-et-industrie", "logistique & industrie", [("94-val-de-marne", "le Val-de-Marne"), ("77-seine-et-marne", "la Seine-et-Marne")]),
    2212: ("sante-et-medical", "médical & bionettoyage", [("paris-14", "Paris 14e"), ("94-val-de-marne", "le Val-de-Marne")]),
    2214: ("commerce-et-retail", "commerce & retail", [("paris-1", "Paris 1er"), ("paris-9", "Paris 9e")]),
    2216: ("copropriete-et-habitat", "copropriété & habitat", [("paris-15", "Paris 15e"), ("92-hauts-de-seine", "les Hauts-de-Seine")]),
    2218: ("hotellerie-et-restauration", "hôtellerie & restauration", [("paris-8", "Paris 8e"), ("paris-1", "Paris 1er")]),
    2231: ("loisirs-culture-et-evenementiel", "loisirs, culture & événementiel", [("paris-19", "Paris 19e"), ("paris-1", "Paris 1er")]),
    2290: ("enseignement-et-petite-enfance", "enseignement & petite enfance", [("paris-5", "Paris 5e"), ("94-val-de-marne", "le Val-de-Marne")]),
    2301: ("tertiaire", "bureaux & tertiaire", [("paris-2", "Paris 2e"), ("92-hauts-de-seine", "les Hauts-de-Seine")]),
    2311: ("tertiaire", "bureaux & tertiaire", [("paris-8", "Paris 8e"), ("94-val-de-marne", "le Val-de-Marne")]),
    2323: ("copropriete-et-habitat", "copropriété & habitat", [("94-val-de-marne", "le Val-de-Marne"), ("92-hauts-de-seine", "les Hauts-de-Seine")]),
    2333: ("commerce-et-retail", "commerce & retail", [("paris-1", "Paris 1er"), ("paris-8", "Paris 8e")]),
}

CARD = ('<a href="{href}" style="display:inline-flex;align-items:center;gap:6px;padding:10px 16px;'
        'background:#fff;border:1px solid #E9E4DD;border-radius:999px;color:#16181D;font-weight:600;'
        'text-decoration:none;font-size:.95rem">→ {label}</a>')


def block(sector, sector_label, zones):
    cards = CARD.format(href=f"{BASE}/{sector}/", label=f"Nettoyage {sector_label}")
    for s, l in zones:
        cards += CARD.format(href=f"{BASE}/{s}/", label=f"Nettoyage de bureaux à {l}")
    return (
        "\n<!-- wp:html -->\n"
        '<!-- spn-art-more --><div class="spn-art-more" style="margin:40px 0 8px;padding:28px;border:1px solid #E9E4DD;'
        'border-radius:18px;background:#FAF8F5;font-family:inherit">'
        '<div style="display:flex;align-items:center;gap:10px;font-size:1.25rem;font-weight:800;color:#16181D;margin:0 0 6px">'
        '<span style="width:16px;height:16px;background:#ED5D37;border-radius:4px;transform:rotate(45deg);display:inline-block"></span>'
        'Pour aller plus loin</div>'
        '<p style="color:#6B7280;margin:0 0 16px;font-size:.98rem">Nos pages dédiées et nos zones d\'intervention en Île-de-France.</p>'
        '<div style="display:flex;flex-wrap:wrap;gap:10px">' + cards + '</div>'
        '<div style="margin-top:20px;padding:20px 22px;background:#16181D;border-radius:14px;display:flex;flex-wrap:wrap;'
        'align-items:center;justify-content:space-between;gap:16px">'
        '<div style="color:#fff;font-weight:700;font-size:1.05rem">Un projet de nettoyage&nbsp;?<br>'
        '<span style="color:rgba(255,255,255,.7);font-weight:500;font-size:.9rem">Devis gratuit sous 24h · ISO 45001 · 4,8/5 sur 48 avis Google</span></div>'
        '<div style="display:flex;gap:10px;flex-wrap:wrap">'
        f'<a href="{BASE}/{sector}/" style="background:linear-gradient(135deg,#F4794E,#D8431F);color:#fff;font-weight:700;'
        'padding:13px 22px;border-radius:999px;text-decoration:none;font-size:.98rem">Demander un devis</a>'
        '<a href="tel:+33149462240" style="background:#fff;color:#16181D;font-weight:700;padding:13px 22px;'
        'border-radius:999px;text-decoration:none;font-size:.98rem">01 49 46 22 40</a>'
        '</div></div></div>\n'
        "<!-- /wp:html -->\n")


def main():
    for pid, (sector, label, zones) in ART.items():
        try:
            r = requests.get(f"{BASE}/wp-json/wp/v2/posts/{pid}",
                             params={"context": "edit", "_fields": "content,slug"}, auth=AUTH, timeout=30).json()
            c = r["content"]["raw"]
            if "spn-art-more" in c:
                print(f"  ⏭ {pid} ({r['slug']}) déjà"); continue
            blk = block(sector, label, zones)
            # insère avant le bloc schema s'il existe, sinon append
            marker = "\n<!-- wp:html -->\n<!-- spn-schema -->"
            if marker in c:
                c = c.replace(marker, blk + marker, 1)
            else:
                c = c + blk
            requests.post(f"{BASE}/wp-json/wp/v2/posts/{pid}", json={"content": c}, auth=AUTH, timeout=60).raise_for_status()
            print(f"  ✓ {pid} ({r['slug']})")
        except Exception as ex:  # noqa: BLE001
            print(f"  ✗ {pid}: {ex}")


if __name__ == "__main__":
    main()
