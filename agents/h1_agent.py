#!/usr/bin/env python3
"""Agent 1 — correction des H1 manquants.

Cible les pages signalées « H1 manquant » dans l'audit. Pour chacune, génère
un H1 unique, optimisé (mot-clé + zone/secteur), à partir du title et des H2.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from base import Agent, Proposal, load_audit, ROOT
from llm import complete

SYSTEM = (
    "Tu es expert SEO on-page pour un site d'entreprise de nettoyage en Île-de-France. "
    "On te donne le title et les sous-titres (H2) d'une page sans balise H1. "
    "Tu proposes UN H1 unique, en français, naturel, contenant le mot-clé principal "
    "et la zone/secteur quand c'est pertinent. 45-70 caractères. Pas de superlatif vide. "
    "Réponds au format JSON demandé."
)

H1_SCHEMA = {
    "type": "object",
    "properties": {
        "h1": {"type": "string"},
        "rationale": {"type": "string"},
    },
    "required": ["h1", "rationale"],
    "additionalProperties": False,
}


def _norm(u: str) -> str:
    return u.rstrip("/") + "/"


class H1Agent(Agent):
    name = "h1_agent"
    kind = "h1"

    def analyze(self) -> list[Proposal]:
        issues = load_audit("issues.json")
        pages = {p["url"]: p for p in load_audit("content.json")}
        # données brutes pour récupérer les H2
        raw = json.loads((ROOT / "audit" / "data" / "pages.json").read_text())
        from urllib.parse import urlparse
        h2_by_url = {
            (urlparse(p["url"]).path or "/").rstrip("/") + "/": p.get("h2", [])
            for p in raw
        }

        targets = [u for (u, msg) in issues if msg == "H1 manquant"]
        proposals: list[Proposal] = []
        for url in targets:
            page = pages.get(url, {})
            title = page.get("title", "")
            h2s = h2_by_url.get(url, [])[:6]
            user = (f"URL: {url}\nTitle: {title}\nSous-titres H2: {h2s}\n\n"
                    "Propose le H1 manquant.")
            try:
                res = complete(SYSTEM, user, schema=H1_SCHEMA, max_tokens=1000, effort="low")
                h1, rationale = res["h1"], res["rationale"]
            except Exception as e:  # noqa: BLE001 — fallback déterministe
                h1 = re.split(r"[|\-–—]", title)[0].strip() or "Entreprise de nettoyage"
                rationale = f"Fallback (LLM indisponible: {e})"
            proposals.append(Proposal(
                agent=self.name, url=url, kind=self.kind,
                summary=f'Ajouter H1 : "{h1}"',
                details={"h1": h1, "rationale": rationale, "title": title},
            ))
        return proposals

    def apply(self, proposal: Proposal) -> None:
        content = self.wp.find_by_link(proposal.url)
        if not content:
            raise RuntimeError(f"Contenu introuvable pour {proposal.url}")
        h1 = proposal.details["h1"]
        # Préfixe un bloc H1 en tête du contenu (Elementor : insertion sûre côté éditeur).
        new_html = f"<h1>{h1}</h1>\n{content.content_html}"
        result = self.wp.update_content(content, new_html)
        proposal.details["wp_result"] = {"id": content.id, "dry_run": result.get("dry_run", False)}
