#!/usr/bin/env python3
"""Agent 2 — maillage interne (surfeur raisonnable).

Relie les 12 articles de blog orphelins à leurs pages secteurs et services,
dans les deux sens, via des liens contextuels (dans le corps du texte).
Cible le problème : 80 % des liens sont du boilerplate, articles = culs-de-sac.
"""
from __future__ import annotations

from base import Agent, Proposal, load_audit
from llm import complete

# Correspondance article de blog → page(s) cible(s) sur le même thème.
BLOG_TO_TARGET = {
    "/meilleure-entreprise-nettoyage-tertiaire-paris/": "/tertiaire/",
    "/meilleure-entreprise-nettoyage-logistique-industrie-paris/": "/logistique-et-industrie/",
    "/meilleure-entreprise-nettoyage-sante-medical-paris/": "/sante-et-medical/",
    "/meilleure-entreprise-nettoyage-commerce-retail-paris/": "/commerce-et-retail/",
    "/meilleure-entreprise-nettoyage-copropriete-habitat-paris/": "/copropriete-et-habitat/",
    "/meilleure-entreprise-nettoyage-hotellerie-restauration-paris/": "/hotellerie-et-restauration/",
    "/meilleure-entreprise-nettoyage-loisirs-culture-evenementiel-paris/": "/loisirs-culture-et-evenementiel/",
    "/meilleure-entreprise-nettoyage-enseignement-petite-enfance-paris/": "/enseignement-et-petite-enfance/",
    "/meilleure-entreprise-nettoyage-fin-de-chantier-paris/": "/proprete-des-locaux/",
    "/meilleure-entreprise-nettoyage-apres-sinistre-paris/": "/proprete-des-locaux/",
    "/meilleure-entreprise-nettoyage-parkings-paris/": "/proprete-des-locaux/",
    "/meilleure-entreprise-nettoyage-vitrines-paris/": "/proprete-des-locaux/",
}

SYSTEM = (
    "Tu es expert SEO en maillage interne. On te donne une page source et une page "
    "cible du même site (entreprise de nettoyage en Île-de-France). Tu proposes UNE "
    "phrase en français à insérer dans le corps de la source, contenant un lien "
    "contextuel naturel vers la cible. L'ancre doit être descriptive et variée "
    "(évite « cliquez ici » / « en savoir plus » et l'ancre exacte sur-optimisée). "
    "Réponds au format JSON demandé."
)

LINK_SCHEMA = {
    "type": "object",
    "properties": {
        "anchor": {"type": "string"},
        "sentence_html": {"type": "string", "description": "Phrase complète avec la balise <a href=…>."},
    },
    "required": ["anchor", "sentence_html"],
    "additionalProperties": False,
}

BASE = "https://spn-net.fr"


class InternalLinkingAgent(Agent):
    name = "internal_linking_agent"
    kind = "internal_links"

    def analyze(self) -> list[Proposal]:
        content = {c["url"]: c for c in load_audit("content.json")}
        proposals: list[Proposal] = []
        for src, tgt in BLOG_TO_TARGET.items():
            # Lien article → page secteur (et réciproque).
            for a, b, direction in ((src, tgt, "article→secteur"),
                                    (tgt, src, "secteur→article")):
                a_title = content.get(a, {}).get("title", a)
                b_title = content.get(b, {}).get("title", b)
                user = (f"Page source: {a} (titre: {a_title})\n"
                        f"Page cible: {BASE}{b} (titre: {b_title})\n"
                        f"Sens: {direction}\n\nPropose la phrase avec le lien contextuel.")
                try:
                    res = complete(SYSTEM, user, schema=LINK_SCHEMA, max_tokens=800, effort="low")
                    anchor, sentence = res["anchor"], res["sentence_html"]
                except Exception as e:  # noqa: BLE001
                    anchor = b_title
                    sentence = f'<p>Voir aussi notre page <a href="{BASE}{b}">{b_title}</a>.</p>'
                    res = {"error": str(e)}
                proposals.append(Proposal(
                    agent=self.name, url=a, kind=self.kind,
                    summary=f'Lien contextuel {direction} → {b} (ancre: "{anchor}")',
                    details={"target": b, "anchor": anchor, "sentence_html": sentence,
                             "direction": direction},
                ))
        return proposals

    def apply(self, proposal: Proposal) -> None:
        content = self.wp.find_by_link(proposal.url)
        if not content:
            raise RuntimeError(f"Contenu introuvable pour {proposal.url}")
        # Insère la phrase-lien à la fin du contenu (revue humaine recommandée
        # avant un placement éditorial plus fin).
        new_html = f"{content.content_html}\n{proposal.details['sentence_html']}"
        result = self.wp.update_content(content, new_html)
        proposal.details["wp_result"] = {"id": content.id, "dry_run": result.get("dry_run", False)}
