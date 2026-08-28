#!/usr/bin/env python3
"""Analyse des données d'audit de spn-net.fr.

Produit des statistiques sur :
- le maillage interne (entrants/sortants, pages orphelines)
- la diversification des ancres (sur-optimisation, ancres génériques/vides)
- le modèle du « surfeur raisonnable » (position des liens : contenu vs boilerplate)
- la qualité/lisibilité du contenu (volume, lisibilité, SEO on-page)

Génère audit/reports/audit.md et plusieurs fichiers de données.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "pages.json"
REPORTS = ROOT / "reports"
BASE_HOST = "spn-net.fr"

GENERIC_ANCHORS = {
    "en savoir plus", "savoir plus", "cliquez ici", "cliquer ici", "ici",
    "lire la suite", "voir plus", "plus", "en savoir +", "découvrir",
    "decouvrir", "contactez-nous", "contact", "devis", "demander un devis",
    "nous contacter", "voir", "details", "détails", "lire plus",
}


def norm(u: str) -> str:
    p = urlparse(u)
    if not p.netloc.endswith(BASE_HOST):
        return u
    return (p.path or "/").rstrip("/") + "/"


def try_readability(text: str) -> float | None:
    try:
        import textstat
        textstat.set_lang("fr")
        return round(textstat.flesch_reading_ease(text), 1)
    except Exception:  # noqa: BLE001
        return None


def main() -> None:
    pages = json.loads(DATA.read_text())
    by_url = {norm(p["url"]): p for p in pages if p["status"] == 200}
    internal_urls = set(by_url)

    inbound: dict[str, list[tuple[str, str, str]]] = defaultdict(list)  # target -> (src, anchor, section)
    outbound: dict[str, int] = defaultdict(int)
    anchor_by_target: dict[str, Counter] = defaultdict(Counter)
    section_counter: Counter = Counter()
    generic_links = 0
    empty_anchor_links = 0
    total_internal_links = 0
    external_links: Counter = Counter()

    for src, p in by_url.items():
        seen_targets = set()
        for l in p["links"]:
            if l["is_internal"] and l["href"].startswith("http"):
                tgt = norm(l["href"])
                total_internal_links += 1
                section_counter[l["section"]] += 1
                anchor = (l["anchor"] or "").strip()
                anchor_low = anchor.lower()
                if not anchor:
                    empty_anchor_links += 1
                elif anchor_low in GENERIC_ANCHORS:
                    generic_links += 1
                # comptage entrants : 1 fois par couple (src,tgt,ancre) en contenu
                key = (tgt, anchor_low, l["section"])
                inbound[tgt].append((src, anchor, l["section"]))
                outbound[src] += 1
                if anchor:
                    anchor_by_target[tgt][anchor_low] += 1
                seen_targets.add(tgt)
            elif l["href"].startswith("http"):
                external_links[urlparse(l["href"]).netloc] += 1

    orphans = sorted(u for u in internal_urls if len(inbound.get(u, [])) == 0)

    # Liens "contextuels" (main) vs boilerplate (nav/header/footer)
    contextual = section_counter.get("main", 0)
    boilerplate = (section_counter.get("nav", 0) + section_counter.get("header", 0)
                   + section_counter.get("footer", 0))

    # Sur-optimisation d'ancre : même ancre exacte répétée massivement vers une cible
    over_optimized = []
    for tgt, counter in anchor_by_target.items():
        total = sum(counter.values())
        if total >= 5:
            top_anchor, top_n = counter.most_common(1)[0]
            ratio = top_n / total
            if ratio >= 0.8 and top_n >= 5:
                over_optimized.append((tgt, top_anchor, top_n, total, round(ratio, 2)))
    over_optimized.sort(key=lambda x: -x[2])

    # Diversité d'ancre par cible (nb d'ancres distinctes)
    anchor_diversity = sorted(
        ((tgt, len(c), sum(c.values())) for tgt, c in anchor_by_target.items()),
        key=lambda x: x[1])

    # ---- Qualité de contenu ----
    content_rows = []
    for u, p in sorted(by_url.items()):
        wc = p["word_count"]
        read = try_readability(p["text_sample"]) if p["text_sample"] else None
        content_rows.append({
            "url": u,
            "title": p["title"],
            "title_len": p["title_len"],
            "meta_desc_len": p["meta_desc_len"],
            "h1_count": len(p["h1"]),
            "h1": p["h1"][:1],
            "word_count": wc,
            "img": p["img_count"],
            "img_no_alt": p["img_without_alt"],
            "out_links": outbound.get(u, 0),
            "in_links": len(inbound.get(u, [])),
            "readability": read,
            "load_s": p["load_seconds"],
        })

    # ---- Anomalies SEO on-page ----
    issues = []
    for r in content_rows:
        if r["title_len"] == 0:
            issues.append((r["url"], "Title manquant"))
        elif r["title_len"] > 65:
            issues.append((r["url"], f"Title trop long ({r['title_len']} car.)"))
        elif r["title_len"] < 30:
            issues.append((r["url"], f"Title court ({r['title_len']} car.)"))
        if r["meta_desc_len"] == 0:
            issues.append((r["url"], "Meta description manquante"))
        elif r["meta_desc_len"] > 160:
            issues.append((r["url"], f"Meta description trop longue ({r['meta_desc_len']} car.)"))
        if r["h1_count"] == 0:
            issues.append((r["url"], "H1 manquant"))
        elif r["h1_count"] > 1:
            issues.append((r["url"], f"H1 multiples ({r['h1_count']})"))
        if r["word_count"] < 350:
            issues.append((r["url"], f"Contenu mince ({r['word_count']} mots)"))
        if r["img_no_alt"] > 0:
            issues.append((r["url"], f"{r['img_no_alt']} image(s) sans alt"))
        if r["out_links"] > 90:
            issues.append((r["url"], f"Trop de liens sortants ({r['out_links']})"))

    # Doublons de title / meta
    title_dups = Counter(r["title"] for r in content_rows if r["title"])
    title_dups = {t: n for t, n in title_dups.items() if n > 1}

    summary = {
        "pages_analysees": len(by_url),
        "total_liens_internes": total_internal_links,
        "liens_contextuels_main": contextual,
        "liens_boilerplate": boilerplate,
        "ratio_contextuel": round(contextual / max(total_internal_links, 1), 3),
        "liens_ancre_vide": empty_anchor_links,
        "liens_ancre_generique": generic_links,
        "pages_orphelines": orphans,
        "ancres_sur_optimisees": over_optimized,
        "sections": dict(section_counter),
        "top_domaines_externes": external_links.most_common(10),
        "titles_dupliques": title_dups,
    }

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    (REPORTS / "content.json").write_text(json.dumps(content_rows, ensure_ascii=False, indent=2))
    (REPORTS / "issues.json").write_text(json.dumps(issues, ensure_ascii=False, indent=2))
    (REPORTS / "anchor_diversity.json").write_text(
        json.dumps([{"target": t, "distinct_anchors": d, "total": tot}
                    for t, d, tot in anchor_diversity], ensure_ascii=False, indent=2))

    # Console résumé
    print("=== SYNTHÈSE ===")
    for k, v in summary.items():
        if isinstance(v, (list, dict)) and k not in ("sections",):
            print(f"{k}: {len(v)} éléments")
        else:
            print(f"{k}: {v}")
    print(f"\nIssues détectées: {len(issues)}")
    print(f"Pages orphelines: {orphans}")


if __name__ == "__main__":
    main()
