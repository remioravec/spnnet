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
    # pages de services spécialisés
    ["nettoyage", "des", "ascenseurs"], ["ascenseurs", "et", "escalators"],
    ["marquage", "au", "sol"], ["mise", "en", "peinture"], ["portage", "de", "repas"],
    ["ascenseurs"], ["escalators"], ["peinture"], ["marquage"], ["portage"],
    ["propreté"], ["entretien"],
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
    """Retire tout le gras du corps (pages paris-X très chargées)."""
    return re.sub(r"</?(?:b|strong)>", "", html)


def reduce_bold_light(html: str) -> str:
    """Allègement léger : dans chaque <p>, on garde le 1ᵉʳ <b> et on dégras se
    les suivants. Le gras des listes, tableaux et titres est conservé."""
    def fix_p(m: re.Match) -> str:
        p = m.group(0)
        first = [True]

        def repl(bm: re.Match) -> str:
            if first[0]:
                first[0] = False
                return bm.group(0)
            return bm.group(1)
        return re.sub(r"<b>(.*?)</b>", repl, p, flags=re.S)
    return re.sub(r"<p\b[^>]*>.*?</p>", fix_p, html, flags=re.S)


def polish_page(mcp: ElementorMCP, slug: str, mode: str = "strip") -> str:
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
        if mode == "strip":
            new = strip_paragraph_bold(ed)
        elif mode == "light":
            new = reduce_bold_light(ed)
        else:  # "none" : surlignage uniquement, on ne touche pas au gras
            new = ed
        if not done_hl:
            new, hl = highlight_once(new)
            done_hl = done_hl or hl
        if new != ed:
            mcp.call("elementor-mcp-update-element",
                     {"post_id": pid, "element_id": eid, "settings": {"editor": new}})
            changed += 1
    return f"  ✓ {slug} (id={pid}) — {changed} widget(s) polis, surlignage={'oui' if done_hl else 'non'}"


def polish_post(post_id: int) -> str:
    """Articles classiques : allègement léger + surlignage dans le post_content."""
    r = requests.get(f"{BASE}/wp-json/wp/v2/posts/{post_id}",
                     params={"context": "edit", "_fields": "id,slug,content"}, auth=AUTH, timeout=30).json()
    ed = r["content"]["raw"]
    new = reduce_bold_light(ed)
    new, hl = highlight_once(new)
    if new != ed:
        requests.post(f"{BASE}/wp-json/wp/v2/posts/{post_id}", json={"content": new}, auth=AUTH, timeout=30).raise_for_status()
    return f"  ✓ post {post_id} ({r['slug']}) — surlignage={'oui' if hl else 'non'}"


SECTORS = ["tertiaire", "logistique-et-industrie", "sante-et-medical", "commerce-et-retail",
           "copropriete-et-habitat", "hotellerie-et-restauration", "loisirs-culture-et-evenementiel",
           "enseignement-et-petite-enfance"]
ARTICLE_IDS = [2189, 2205, 2212, 2214, 2216, 2218, 2231, 2290, 2301, 2311, 2323, 2333]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paris", action="store_true")
    ap.add_argument("--sectors", action="store_true")
    ap.add_argument("--articles", action="store_true")
    ap.add_argument("--slug")
    args = ap.parse_args()
    mcp = ElementorMCP(); mcp.initialize()
    if args.articles:
        for pid in ARTICLE_IDS:
            try:
                print(polish_post(pid))
            except Exception as e:  # noqa: BLE001
                print(f"  ✗ post {pid}: {e}")
        return 0
    if args.sectors:
        for s in SECTORS:
            try:
                print(polish_page(mcp, s, mode="light"))
            except Exception as e:  # noqa: BLE001
                print(f"  ✗ {s}: {e}")
        return 0
    slugs = [args.slug] if args.slug else (PARIS if args.paris else [])
    for s in slugs:
        try:
            print(polish_page(mcp, s, mode="strip" if args.paris or args.slug else "light"))
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ {s}: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
