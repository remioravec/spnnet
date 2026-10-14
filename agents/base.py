#!/usr/bin/env python3
"""Classe de base des agents d'amélioration de contenu.

Chaque agent :
  1. consomme les données d'audit (audit/reports/*.json),
  2. génère des *propositions* via Claude (ou en déterministe),
  3. en mode dry-run : écrit les propositions dans agents/proposals/,
     en mode apply : applique via l'API WordPress.

La séparation propose/apply permet une revue humaine avant publication.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT_REPORTS = ROOT / "audit" / "reports"
PROPOSALS_DIR = ROOT / "agents" / "proposals"


def load_audit(name: str):
    return json.loads((AUDIT_REPORTS / name).read_text())


@dataclass
class Proposal:
    """Une modification proposée pour une URL donnée."""
    agent: str
    url: str
    kind: str            # "h1" | "internal_links" | "anchors" | "readability"
    summary: str
    details: dict = field(default_factory=dict)
    applied: bool = False


class Agent:
    name = "base"
    kind = "base"

    def __init__(self, wp_client, dry_run: bool = True):
        self.wp = wp_client
        self.dry_run = dry_run
        self.proposals: list[Proposal] = []

    def analyze(self) -> list[Proposal]:
        """À implémenter : produit la liste des propositions."""
        raise NotImplementedError

    def apply(self, proposal: Proposal) -> None:
        """À implémenter : applique une proposition via l'API WordPress."""
        raise NotImplementedError

    def run(self) -> list[Proposal]:
        self.proposals = self.analyze()
        if not self.dry_run:
            for p in self.proposals:
                try:
                    self.apply(p)
                    p.applied = True
                except Exception as e:  # noqa: BLE001
                    p.details["error"] = str(e)
        self._save()
        return self.proposals

    def _save(self) -> None:
        PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
        out = PROPOSALS_DIR / f"{self.name}.json"
        out.write_text(json.dumps([asdict(p) for p in self.proposals],
                                  ensure_ascii=False, indent=2))
