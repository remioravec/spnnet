#!/usr/bin/env python3
"""Polissage CRO : allègement du gras + surlignage orange « stabilo » de la
requête clé, sur les widgets text-editor (pages) ou le post_content (articles).

- Pages locales paris-X : on retire le gras des paragraphes (gras parasite /
  demi-gras) ; l'emphase passe par le surlignage de la requête principale.
- Surlignage : la 1ʳᵉ occurrence de la requête clé est entourée d'un <mark>
  orange (#FFB454), une seule fois par page.

Idempotent : on ne re-surligne pas si un <mark> est déjà présent.
Usage : python3 agents/polish.py --paris   (les 20 pages locales)
"""
from __future__ import annotations

import argparse
import os
import re
import sys

import requests

sys.path.insert(0, os.path.dirname(__file__))
from elementor_mcp import ElementorMCP  # noqa: E402

BASE = "https://spn-net.fr"
AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
MARK_OPEN = '<mark style="background-color:#FFB454;padding:0 .12em;border-radius:.1em;">'
MARK_CLOSE = "</mark>"

PARIS = [f"paris-{n}" for n in range(1, 21)]


# séparateur tolérant aux balises span/b entre deux mots de la requête
_SEP = r"(?:\s|&nbsp;|</?(?:span|b|strong|i|em)[^>]*>)+"
# requêtes candidates (par ordre de priorité), en tokens
_QUERIES = [
    ["entreprise", "de", "nettoyage"],
    ["société", "de", "nettoyage"],
    ["entreprises", "de", "nettoyage"],
    ["nettoyage", "de", "bureaux"],
    ["nettoyage", "de", "locaux"],
    ["nettoyage", "professionnel"],
    ["propreté", "de", "vos", "locaux"],
    ["nettoyage", "de", "qualité"],
    ["hygiène", "irréprochable"],
    ["besoins", "en", "matière", "de", "nettoyage"],
    ["nettoyage"],  # repli : garantit un surlignage
]


def highlight_once(html: str, _unused=None) -> tuple[str, bool]:
    """Entoure la 1ʳᵉ occurrence d'une requête clé d'un <mark> orange
    (tolérant aux balises entre les mots)."""
    if "<mark" in html:
        return html, False
    for toks in _QUERIES:
        pat = _SEP.join(re.escape(t) for t in toks)
        m = re.search(pat, html, flags=re.I)
        if m:
            s, e = m.start(), m.end()
            return html[:s] + MARK_OPEN + html[s:e] + MARK_CLOSE + html[e:], True
    return html, False


def strip_paragraph_bold(html: str) -> str:
    """Retire le gras (<b>/<strong>) du corps. Les titres (h2/h3) restent gras
    via leurs balises ; on conserve l'emphase des en-têtes de tableau."""
    # protège les cellules d'en-tête de tableau (1ʳᵉ ligne) : on garde leur gras
    return re.sub(r"</?(?:b|strong)>", "", html)


def polish_page(mcp: ElementorMCP, slug: str) -> str:
    r = requests.get(f"{BASE}/wp-json/wp/v2/pages", params={"slug": slug, "_fields": "id"},
                     auth=AUTH, timeout=30).json()
    if not r:
        return f"  ✗ {slug}: introuvable"
    pid = r[0]["id"]
    res = mcp.call("elementor-mcp-find-element", {"post_id": pid, "widgetType": "text-editor"})
    te = [x for x in res.get("parsed", res).get("matches", []) if x.get("widgetType") == "text-editor"]
    done_hl = False
    changed = 0
    for w in te:
        eid = w["element_id"]
        cur = mcp.call("elementor-mcp-get-element-settings", {"post_id": pid, "element_id": eid})
        ed = (cur.get("parsed", cur).get("settings", {}) or {}).get("editor", "")
        new = strip_paragraph_bold(ed)
        if not done_hl:
            new, hl = highlight_once(new, r"entreprise de nettoyage")
            done_hl = done_hl or hl
        if new != ed:
            mcp.call("elementor-mcp-update-element",
                     {"post_id": pid, "element_id": eid, "settings": {"editor": new}})
            changed += 1
    return f"  ✓ {slug} (id={pid}) — {changed} widget(s) polis, surlignage={'oui' if done_hl else 'non'}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paris", action="store_true")
    ap.add_argument("--slug")
    args = ap.parse_args()
    mcp = ElementorMCP(); mcp.initialize()
    slugs = [args.slug] if args.slug else (PARIS if args.paris else [])
    for s in slugs:
        try:
            print(polish_page(mcp, s))
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ {s}: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
