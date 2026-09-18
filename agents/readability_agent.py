#!/usr/bin/env python3
"""Agent 4 — réécriture pour la lisibilité et l'agréabilité.

Cible les pages dont la lisibilité (Flesch FR) est faible. Pour chacune,
récupère le contenu réel via l'API, et propose une réécriture : phrases plus
courtes, listes, ton plus humain — sans changer le sens ni les faits.
"""
from __future__ import annotations

from base import Agent, Proposal, load_audit
from llm import complete

SYSTEM = (
    "Tu es rédacteur web SEO francophone pour une entreprise de nettoyage en "
    "Île-de-France. On te donne le contenu HTML d'une page peu lisible. Tu le "
    "réécris pour : phrases courtes (< 20 mots en moyenne), paragraphes aérés, "
    "listes à puces quand c'est utile, ton clair et engageant orienté bénéfices "
    "client. NE CHANGE PAS les faits, chiffres, coordonnées, ni la structure des "
    "titres (Hn) ni les liens existants (<a>). Conserve le HTML valide. "
    "Réponds uniquement avec le HTML réécrit."
)

# Seuil de lisibilité Flesch FR en dessous duquel on propose une réécriture.
READABILITY_THRESHOLD = 35.0
# Plafond de pages traitées par exécution (coût/latence — ajustable).
MAX_PAGES = 12


class ReadabilityAgent(Agent):
    name = "readability_agent"
    kind = "readability"

    def analyze(self) -> list[Proposal]:
        rows = load_audit("content.json")
        candidates = sorted(
            (r for r in rows
             if r.get("readability") is not None
             and r["readability"] < READABILITY_THRESHOLD
             and r["word_count"] >= 400),
            key=lambda r: r["readability"],
        )[:MAX_PAGES]

        proposals: list[Proposal] = []
        for r in candidates:
            url = r["url"]
            content = self.wp.find_by_link(url)
            if not content:
                proposals.append(Proposal(
                    agent=self.name, url=url, kind=self.kind,
                    summary=f"Réécriture impossible (contenu introuvable via API) — lisibilité {r['readability']}",
                    details={"readability": r["readability"]}))
                continue
            user = (f"URL: {url}\nLisibilité actuelle (Flesch FR): {r['readability']}\n\n"
                    f"HTML à réécrire:\n{content.content_html[:12000]}")
            try:
                new_html = complete(SYSTEM, user, max_tokens=16000, effort="medium")
            except Exception as e:  # noqa: BLE001
                proposals.append(Proposal(
                    agent=self.name, url=url, kind=self.kind,
                    summary=f"Réécriture non générée (LLM indisponible) — lisibilité {r['readability']}",
                    details={"error": str(e), "readability": r["readability"]}))
                continue
            proposals.append(Proposal(
                agent=self.name, url=url, kind=self.kind,
                summary=f"Réécriture lisibilité (Flesch {r['readability']} → cible 50+)",
                details={"readability_before": r["readability"],
                         "wp_id": content.id, "new_html": new_html},
            ))
        return proposals

    def apply(self, proposal: Proposal) -> None:
        new_html = proposal.details.get("new_html")
        if not new_html:
            raise RuntimeError("Pas de réécriture disponible.")
        content = self.wp.find_by_link(proposal.url)
        if not content:
            raise RuntimeError(f"Contenu introuvable pour {proposal.url}")
        result = self.wp.update_content(content, new_html)
        proposal.details["wp_result"] = {"id": content.id, "dry_run": result.get("dry_run", False)}
