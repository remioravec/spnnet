#!/usr/bin/env python3
"""Orchestrateur des agents d'amélioration SEO/contenu pour spn-net.fr.

Usage :
  python3 agents/run.py --dry-run                 # propose tout (défaut), aucune écriture
  python3 agents/run.py --agents h1,links --dry-run
  python3 agents/run.py --apply                   # applique via l'API WordPress
  python3 agents/run.py --verify-auth             # teste l'accès en écriture

Modes :
  --dry-run (défaut) : génère les propositions dans agents/proposals/*.json
  --apply            : applique réellement (nécessite WP_USER/WP_APP_PASSWORD
                       + correctif .htaccess pour l'en-tête Authorization)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from wp_client import WordPressClient  # noqa: E402
from h1_agent import H1Agent  # noqa: E402
from internal_linking_agent import InternalLinkingAgent  # noqa: E402
from anchor_agent import AnchorAgent  # noqa: E402
from readability_agent import ReadabilityAgent  # noqa: E402

AGENTS = {
    "h1": H1Agent,
    "links": InternalLinkingAgent,
    "anchors": AnchorAgent,
    "readability": ReadabilityAgent,
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Agents IA d'amélioration spn-net.fr")
    ap.add_argument("--agents", default="all",
                    help="liste séparée par des virgules: h1,links,anchors,readability (défaut: all)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="propose sans appliquer (défaut)")
    mode.add_argument("--apply", action="store_true", help="applique via l'API WordPress")
    ap.add_argument("--verify-auth", action="store_true", help="teste l'authentification puis quitte")
    args = ap.parse_args()

    dry_run = not args.apply
    wp = WordPressClient(dry_run=dry_run)

    if args.verify_auth:
        ok, msg = wp.verify_auth()
        print(("✅ " if ok else "❌ ") + msg)
        return 0 if ok else 1

    selected = list(AGENTS) if args.agents == "all" else [a.strip() for a in args.agents.split(",")]
    unknown = [a for a in selected if a not in AGENTS]
    if unknown:
        ap.error(f"agents inconnus: {unknown}. Disponibles: {list(AGENTS)}")

    if args.apply:
        ok, msg = wp.verify_auth()
        if not ok:
            print(f"❌ Écriture impossible : {msg}")
            print("   Repassez en --dry-run, ou appliquez le correctif .htaccess (voir AUDIT.md).")
            return 1
        print(f"✅ {msg} — mode APPLY")
    else:
        print("Mode DRY-RUN — aucune écriture. Propositions dans agents/proposals/")

    total = 0
    for key in selected:
        agent = AGENTS[key](wp_client=wp, dry_run=dry_run)
        props = agent.run()
        applied = sum(1 for p in props if p.applied)
        total += len(props)
        suffix = f", {applied} appliquées" if args.apply else ""
        print(f"  [{key:11s}] {len(props)} propositions{suffix}")

    print(f"\nTotal : {total} propositions. Détail : agents/proposals/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
