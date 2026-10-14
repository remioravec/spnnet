#!/usr/bin/env python3
"""Nettoyage ciblé des pages locales Elementor (paris-X) : retire les éléments
parasites et corrige les défauts rédactionnels détectés, sans réécriture lourde.

Corrections appliquées aux widgets text-editor :
- liens cassés google.com/search neutralisés (texte conservé)
- verbes tronqués : « garantisson (garantissons) » -> « garantissons », idem proposon/assuron
- mentions parasites « voir le profil » et doublons « (ou X) » retirés/rephrasés
- noms de concurrents supprimés
- codes postaux non naturels supprimés (« Paris 1 75001 » -> « Paris 1er »)

Idempotent (les regex ne re-matchent pas une fois corrigées).
Usage : python3 agents/clean_pages.py --dry-run | --apply
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from elementor_mcp import ElementorMCP  # noqa: E402
import requests

BASE = "https://spn-net.fr"
AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])

PARIS = [f"paris-{n}" for n in range(1, 21)]
COMPETITORS = [
    "cleanolia france", "cleanolia", "nova clean", "ara nettoyage", "nikita nettoyage",
    "france clean", "vitri paul", "parc net", "net tout net", "ecocomplet",
    "samsic facility", "samsic", "onet", "somainnet", "avenir clean", "aeronet", "ara nettoyag",
]


def ordinal(n: int) -> str:
    return "1er" if n == 1 else f"{n}e"


# Séparateur tolérant aux balises (gras/italique/span) et espaces entre deux mots.
SEP = r"(?:\s|&nbsp;|</?(?:b|i|strong|em|span)[^>]*>)*"


def fix_flagrant(s: str) -> str:
    """Corrige les formulations sur-optimisées templatées des pages paris-X
    (retire le gras parasite, rend le texte naturel) + incohérences géo."""
    # « France, ce 75 service nettoyage » (en gras) -> « service de nettoyage »
    s = re.sub(rf"<b>{SEP}France,?{SEP}ce{SEP}75{SEP}service{SEP}nettoyage{SEP}</b>",
               "service de nettoyage", s, flags=re.I)
    s = re.sub(rf"\bEn{SEP}service de nettoyage{SEP}de haut vol",
               "Notre service de nettoyage de haut vol", s, flags=re.I)
    s = re.sub(rf"(?:france{SEP})?\b75{SEP}service{SEP}nettoyage\b", "service de nettoyage", s, flags=re.I)

    for n in range(1, 21):
        o = ordinal(n)
        # « Paris N nettoyage d'urgence » -> « nettoyage d'urgence à Paris Ne »
        s = re.sub(rf"<b>{SEP}Paris{SEP}{n}{SEP}nettoyage{SEP}</b>{SEP}d'urgence",
                   f"nettoyage d'urgence à Paris {o}", s, flags=re.I)
        s = re.sub(rf"<b>{SEP}Paris{SEP}{n}{SEP}nettoyage{SEP}</b>",
                   f"nettoyage à Paris {o}", s, flags=re.I)
        s = re.sub(rf"\bParis\s+{n}\s+nettoyage\b", f"nettoyage à Paris {o}", s, flags=re.I)
        # « Paris Ne arrondissement magasin de luxe » -> « magasin de luxe du Ne arrondissement »
        s = re.sub(rf"<b>{SEP}Paris{SEP}{o}{SEP}arrondissement{SEP}magasin{SEP}</b>{SEP}de luxe",
                   f"magasin de luxe du {o} arrondissement", s, flags=re.I)
        s = re.sub(rf"\bParis\s+{o}\s+arrondissement\s+magasin\b", f"magasin du {o} arrondissement", s, flags=re.I)
        # « du Paris N » (souvent en gras) -> « du Ne »  (mais on garde « du Paris historique »)
        s = re.sub(rf"\bdu{SEP}<b>{SEP}Paris{SEP}{n}{SEP}</b>", f"du {o}", s, flags=re.I)
        s = re.sub(rf"\bdu\s+Paris\s+{n}\b", f"du {o}", s, flags=re.I)
        s = re.sub(rf"\bdu\s+Paris\s+{o}\b", f"du {o}", s, flags=re.I)            # « du Paris 6e » -> « du 6e »
        s = re.sub(rf"\bdu\s+paris\s+{n}\s*(?:ème|eme|e|er)\b", f"du {o}", s, flags=re.I)

    # Géographie : on retire les villes hors Île-de-France et départements lointains,
    # mais on conserve « Gare de Lyon » (monument parisien), Seine-et-Marne, Neuilly…
    s = re.sub(rf"à{SEP}l'échelle nationale{SEP}à{SEP}Lyon{SEP},?{SEP}Bordeaux{SEP}ou{SEP}Marseille{SEP}",
               "à l'échelle nationale ", s, flags=re.I)
    s = re.sub(rf"à{SEP}Lyon{SEP}ou{SEP}Marseille", "ailleurs en France", s, flags=re.I)
    s = re.sub(rf"à{SEP}Marseille{SEP}ou{SEP}en province", "en province", s, flags=re.I)
    s = re.sub(rf",?{SEP}et même jusqu'à la{SEP}<b>{SEP}Marne{SEP}</b>", "", s, flags=re.I)
    s = re.sub(r",?\s*et même jusqu'à la Marne\b", "", s, flags=re.I)
    # « la marne nettoyage », « (mais aussi) dans la marne, la seine, » -> retirés
    s = re.sub(r"\bla\s+marne\s+nettoyage\b\s*,?\s*", "", s, flags=re.I)
    s = re.sub(r"(?:,?\s*mais aussi\s+)?dans\s+la\s+marne\s*,?\s*(?:la\s+seine\s*,?\s*)?", "", s, flags=re.I)
    s = re.sub(r"\bla\s+seine\s*,\s*", "", s, flags=re.I)
    return s


def clean_html(html: str) -> str:
    s = html
    s = fix_flagrant(s)

    # 1) Neutralise les liens google.com/search : garde le texte de l'ancre.
    s = re.sub(r'<a\b[^>]*href="[^"]*google\.com/search[^"]*"[^>]*>(.*?)</a>',
               r'\1', s, flags=re.I | re.S)
    # URL google.com/search collée en plein texte (artefact d'IA) :
    s = re.sub(r"7j\s*https?://www\.google\.com/search\?q=/7", "7j/7", s, flags=re.I)  # "7j/7"
    s = re.sub(r'\s*https?://www\.google\.com/search[^\s<"]*', " ", s, flags=re.I)

    # 2) Verbes tronqués + parenthèse de correction.
    for stem, ok in [("garantisson", "garantissons"), ("proposon", "proposons"),
                     ("assuron", "assurons"), ("réalison", "réalisons"),
                     ("realison", "réalisons"), ("disposon", "disposons"),
                     ("fournisson", "fournissons"), ("maitrison", "maîtrisons")]:
        s = re.sub(rf"\b{stem}\b\s*\(\s*{ok}\s*\)", ok, s, flags=re.I)   # "garantisson (garantissons)"
        s = re.sub(rf"\b{stem}\b(?!s)", ok, s)                             # "proposon" seul -> "proposons"
    # parenthèses de correction résiduelles "(garantissons)" / "(et proposons)".
    verbs_alt = r"(?:garantissons|proposons|assurons|réalisons|disposons|fournissons|maîtrisons)"
    s = re.sub(rf"\s*\(\s*{verbs_alt}\s*\)", "", s, flags=re.I)        # (garantissons)
    s = re.sub(r"\s*\(\s*et\s+[^)]{1,25}\)", "", s, flags=re.I)        # (et proposons)…
    # parenthèse vide ou orpheline laissée par un nettoyage
    s = re.sub(r"\(\s*\)", "", s)

    # 3) « voir le profil » et doublons « (ou X) ».
    s = re.sub(r"voir le profil approximatif", "approximatif", s, flags=re.I)
    s = re.sub(r"voir le profil", "consulter le profil", s, flags=re.I)
    # doublons synonymiques « (ou … ) » — tolérant aux balises à l'intérieur.
    s = re.sub(r"\s*\(\s*ou\b[^)]{1,70}\)", "", s, flags=re.I)

    # 4) Concurrents : parenthèses qui en contiennent, puis mentions en ligne, puis résidus.
    comp_alt = r"(?:cleanolia(?:\s+france)?|nova\s*clean|ara\s*nettoy\w*|avenir\s*clean|samsic(?:\s+facility)?|\bonet\b|somainnet|aeronet)"
    s = re.sub(rf"\s*\([^()]*{comp_alt}[^()]*\)", "", s, flags=re.I)
    s = re.sub(r"(?:à\s+)?samsic\s+facility\s+ou\s+aeronet", "à de grands groupes nationaux", s, flags=re.I)
    s = re.sub(r"\s*,?\s*comme\s+onet[^.<]*", "", s, flags=re.I)
    s = re.sub(rf"\s*,?\s*(?:comme|tels?\s+que)\s+{comp_alt}", "", s, flags=re.I)  # "comme cleanolia france"
    s = re.sub(rf"\s*{comp_alt}", "", s, flags=re.I)                                # résidus isolés
    s = re.sub(r"\(\s*comme\s*\)", "", s, flags=re.I)

    # 5) Codes postaux non naturels.
    for n in range(1, 21):
        cp = f"750{n:02d}"
        o = ordinal(n)
        s = re.sub(rf"\bParis\s+{n}\s*\(\s*{cp}\s*\)", f"Paris {o}", s)
        s = re.sub(rf"\bParis\s+{n}\s+{cp}\b", f"Paris {o}", s)
        s = re.sub(rf"\bparis\s+{n}\s*(?:ème|eme|e|er)?\s+{cp}\b", f"Paris {o}", s, flags=re.I)
        s = re.sub(rf"\b{cp}\s+paris\b", f"Paris {o}", s, flags=re.I)
        s = re.sub(rf"\bdu\s+{cp}\b", f"du {o} arrondissement", s)
        s = re.sub(rf"\(\s*{cp}\s*\)", f"({o})", s)
        s = re.sub(rf"\b{cp}\b", f"Paris {o}", s)
    # nettoyage des doublons "Paris Xe paris" / "Paris Xe Paris"
    s = re.sub(r"\b(Paris\s+\d+(?:er|e))\s+paris\b", r"\1", s, flags=re.I)
    # espaces résiduels : on NE touche PAS à l'espace avant : ; ? ! (typographie FR).
    s = re.sub(r"\s{2,}", " ", s)
    s = re.sub(r"\s+,", ",", s)           # pas d'espace avant la virgule
    s = re.sub(r",\s*,", ",", s)          # virgules orphelines
    s = re.sub(r"\(\s*,\s*", "(", s)
    s = re.sub(r"\s+\)", ")", s)
    return s


def main() -> int:
    ap = argparse.ArgumentParser()
    m = ap.add_mutually_exclusive_group(required=True)
    m.add_argument("--dry-run", action="store_true")
    m.add_argument("--apply", action="store_true")
    ap.add_argument("--slug", help="limiter à un slug")
    args = ap.parse_args()
    import json
    from pathlib import Path
    backups = Path(__file__).parent / "backups"
    backups.mkdir(exist_ok=True)
    mcp = ElementorMCP(); mcp.initialize()
    slugs = [args.slug] if args.slug else PARIS
    total_changes = 0
    for slug in slugs:
        r = requests.get(f"{BASE}/wp-json/wp/v2/pages", params={"slug": slug, "_fields": "id"},
                         auth=AUTH, timeout=30).json()
        if not r:
            continue
        pid = r[0]["id"]
        res = mcp.call("elementor-mcp-find-element", {"post_id": pid, "widgetType": "text-editor"})
        te = [x for x in res.get("parsed", res).get("matches", []) if x.get("widgetType") == "text-editor"]
        bkfile = backups / f"page_{pid}_text_editors.json"
        bk = json.loads(bkfile.read_text()) if bkfile.exists() else {}
        for w in te:
            eid = w["element_id"]
            cur = mcp.call("elementor-mcp-get-element-settings", {"post_id": pid, "element_id": eid})
            ed = (cur.get("parsed", cur).get("settings", {}) or {}).get("editor", "")
            new = clean_html(ed)
            if new != ed:
                total_changes += 1
                if args.dry_run:
                    import difflib
                    a = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", ed))
                    b = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", new))
                    sm = difflib.SequenceMatcher(a=a, b=b)
                    print(f"\n--- {slug} / {eid} ---")
                    for op, i1, i2, j1, j2 in sm.get_opcodes():
                        if op != "equal":
                            ctx_a = a[max(0, i1 - 25):i2 + 25]
                            ctx_b = b[max(0, j1 - 25):j2 + 25]
                            print(f"   AVANT …{ctx_a.strip()}…")
                            print(f"   APRÈS …{ctx_b.strip()}…")
                else:
                    if eid not in bk:               # sauvegarde l'original une seule fois
                        bk[eid] = ed
                        bkfile.write_text(json.dumps(bk, ensure_ascii=False, indent=2))
                    mcp.call("elementor-mcp-update-element",
                             {"post_id": pid, "element_id": eid, "settings": {"editor": new}})
                    print(f"  ✓ {slug} / {eid} nettoyé")
    print(f"\n{total_changes} widget(s) {'à modifier' if args.dry_run else 'modifiés'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
