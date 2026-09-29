#!/usr/bin/env python3
"""Ajoute un tableau récapitulatif pertinent aux pages/articles qui n'en ont pas
(clarté & lisibilité). Idempotent (marqueur <!-- spn-table -->).

- Secteurs (Elementor) : tableau ajouté à la fin du widget « prestations ».
- Articles (classique)  : tableau inséré juste avant le lien de maillage final.

Usage : python3 agents/add_tables.py
"""
from __future__ import annotations

import os
import re
import sys

import requests

sys.path.insert(0, os.path.dirname(__file__))
from elementor_mcp import ElementorMCP  # noqa: E402

BASE = "https://spn-net.fr"
AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
M = "<!-- spn-table -->"


def table(rows: list[tuple[str, str]], headers: tuple[str, str]) -> str:
    head = f"<tr><td><b>{headers[0]}</b></td><td><b>{headers[1]}</b></td></tr>"
    body = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
    return f'{M}<figure class="wp-block-table"><table><tbody>{head}{body}</tbody></table></figure>'


# Secteur -> (page_id, widget prestations, tableau)
SECTORS = {
    "logistique-et-industrie": (469, "1207193", table([
        ("Entrepôts &amp; plateformes", "Balayage mécanique, auto-laveuses, racks, zones de picking"),
        ("Usines &amp; lignes de production", "Dégraissage technique, sols résine/béton, gestion de la co-activité"),
        ("Quais &amp; extérieurs", "Quais de chargement, parvis et bardages au nettoyeur haute pression"),
    ], ("Zone du site", "Prestations clés"))),
    "hotellerie-et-restauration": (515, "c40492c", table([
        ("Chambres &amp; hébergement", "Rotation, moquettes à la vapeur, salles d'eau, parties communes"),
        ("Cuisines professionnelles", "Dégraissage des hottes, normes HACCP, plonge et chambres froides"),
        ("Salles &amp; réception", "Sols, banquettes, vitrerie, désinfection des points de contact"),
    ], ("Espace", "Prestations clés"))),
    "enseignement-et-petite-enfance": (527, "c2d8b83", table([
        ("Crèches &amp; maternelles", "Bio-nettoyage vapeur, désinfection des jouets, dortoirs, tables à langer"),
        ("Écoles, collèges &amp; lycées", "Points de contact, blocs sanitaires, réfectoires (HACCP)"),
        ("Campus &amp; formation", "Amphithéâtres, bibliothèques, grandes surfaces de circulation"),
    ], ("Établissement", "Prestations clés"))),
}

# Article post_id -> tableau
ARTICLES = {
    2311: table([
        ("Dégât des eaux", "Pompage, assèchement technique, traitement anti-bactérien et fongicide"),
        ("Incendie", "Décontamination des suies, désodorisation à l'ozone, lessivage"),
        ("Vandalisme, Diogène, décès", "Débarras, désinfection lourde, remise en état"),
    ], ("Type de sinistre", "Notre intervention")),
    2323: table([
        ("Sols béton / résine", "Auto-laveuse autoportée, nettoyeur haute pression"),
        ("Taches d'huile incrustées", "Dégraissant industriel + monobrosse à disque abrasif"),
        ("Luminaires &amp; tuyauteries", "Dépoussiérage humide en hauteur"),
    ], ("Surface", "Traitement")),
    2333: table([
        ("Vitrines &amp; devantures", "Lavage à l'eau pure osmosée, séchage sans traces"),
        ("Vitres en hauteur", "Perches télescopiques, sans nacelle"),
        ("Vitrophanie &amp; stickers", "Nettoyage délicat, sans grattoir métallique"),
    ], ("Type de vitrage", "Prestation")),
}


def add_sector(mcp: ElementorMCP, slug: str, pid: int, eid: str, tbl: str) -> str:
    cur = mcp.call("elementor-mcp-get-element-settings", {"post_id": pid, "element_id": eid})
    ed = (cur.get("parsed", cur).get("settings", {}) or {}).get("editor", "")
    if M in ed:
        return f"  ⏭  {slug}: tableau déjà présent"
    # insère le tableau après le 1er paragraphe d'intro du widget prestations
    m = re.search(r"</p>", ed)
    new = (ed[:m.end()] + tbl + ed[m.end():]) if m else (ed + tbl)
    mcp.call("elementor-mcp-update-element", {"post_id": pid, "element_id": eid, "settings": {"editor": new}})
    return f"  ✓ {slug}: tableau ajouté (widget {eid})"


def add_article(pid: int, tbl: str) -> str:
    r = requests.get(f"{BASE}/wp-json/wp/v2/posts/{pid}",
                     params={"context": "edit", "_fields": "id,slug,content"}, auth=AUTH, timeout=30).json()
    ed = r["content"]["raw"]
    if M in ed:
        return f"  ⏭  post {pid}: tableau déjà présent"
    wrapped = f"<!-- wp:table -->{tbl}<!-- /wp:table -->"
    # insère juste avant le paragraphe de maillage final
    idx = ed.find("<!-- spn-maillage")
    if idx == -1:
        new = ed + wrapped
    else:
        pstart = ed.rfind("<!-- wp:paragraph -->", 0, idx)
        pos = pstart if pstart != -1 else idx
        new = ed[:pos] + wrapped + ed[pos:]
    requests.post(f"{BASE}/wp-json/wp/v2/posts/{pid}", json={"content": new}, auth=AUTH, timeout=30).raise_for_status()
    return f"  ✓ post {pid} ({r['slug']}): tableau ajouté"


def main() -> int:
    mcp = ElementorMCP(); mcp.initialize()
    for slug, (pid, eid, tbl) in SECTORS.items():
        try:
            print(add_sector(mcp, slug, pid, eid, tbl))
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ {slug}: {e}")
    for pid, tbl in ARTICLES.items():
        try:
            print(add_article(pid, tbl))
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ post {pid}: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
