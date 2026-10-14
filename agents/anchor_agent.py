#!/usr/bin/env python3
"""Agent 3 — diversification des ancres.

Pour les cibles dont l'ancre exacte est sur-optimisée (≥80 % identique dans
l'audit), génère un plan d'ancres diversifiées : 1 ancre exacte + variantes
partielles, sémantiques et naturelles, à utiliser dans le maillage éditorial.
"""
from __future__ import annotations

from base import Agent, Proposal, load_audit
from llm import complete

SYSTEM = (
    "Tu es expert SEO. Pour une page cible d'un site d'entreprise de nettoyage en "
    "Île-de-France, on te donne l'ancre exacte sur-optimisée actuelle. Tu proposes un "
    "plan de 6 ancres diversifiées et naturelles en français : 1 exacte (tolérée), puis "
    "des variantes partielles, sémantiques, de marque et descriptives — toutes "
    "réellement utilisables dans une phrase. Réponds au format JSON demandé."
)

ANCHOR_SCHEMA = {
    "type": "object",
    "properties": {
        "anchors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "type": {"type": "string", "enum": [
                        "exacte", "partielle", "sémantique", "marque", "descriptive"]},
                },
                "required": ["text", "type"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["anchors"],
    "additionalProperties": False,
}

# Seuils : on ne traite que les ancres significatives hors purs liens de menu génériques.
MIN_OCCURRENCES = 5


class AnchorAgent(Agent):
    name = "anchor_agent"
    kind = "anchors"

    def analyze(self) -> list[Proposal]:
        summary = load_audit("summary.json")
        over = summary.get("ancres_sur_optimisees", [])
        proposals: list[Proposal] = []
        seen_targets: set[str] = set()
        for tgt, anchor, n, total, ratio in over:
            if n < MIN_OCCURRENCES or tgt in seen_targets:
                continue
            seen_targets.add(tgt)
            user = (f"Page cible: {tgt}\nAncre exacte actuelle: \"{anchor}\" "
                    f"({n}/{total} liens, {int(ratio*100)} %).\n\n"
                    "Propose le plan de 6 ancres diversifiées.")
            try:
                res = complete(SYSTEM, user, schema=ANCHOR_SCHEMA, max_tokens=1200, effort="low")
                anchors = res["anchors"]
            except Exception as e:  # noqa: BLE001
                anchors = [{"text": anchor, "type": "exacte"}]
                res = {"error": str(e)}
            proposals.append(Proposal(
                agent=self.name, url=tgt, kind=self.kind,
                summary=f'Diversifier l\'ancre "{anchor}" ({int(ratio*100)} % exact) → {len(anchors)} variantes',
                details={"current_anchor": anchor, "ratio": ratio,
                         "occurrences": n, "total": total, "anchors": anchors},
            ))
        return proposals

    def apply(self, proposal: Proposal) -> None:
        # La diversification d'ancres est un plan éditorial : il s'applique en
        # modifiant les liens dans les pages sources (porté par l'agent maillage),
        # pas par une écriture directe sur la cible. On ne pousse donc rien ici —
        # le livrable est le plan d'ancres, à revoir puis à câbler dans le maillage.
        proposal.details["note"] = (
            "Plan d'ancres — à appliquer via le maillage éditorial (pages sources), "
            "pas d'écriture directe sur la cible.")
