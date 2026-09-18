#!/usr/bin/env python3
"""Wrapper Claude (Anthropic SDK) pour les agents d'amélioration.

- Modèle par défaut : claude-opus-4-8 (surchargeable via SPN_MODEL).
- Pensée adaptative (thinking adaptive) pour les tâches de raisonnement.
- Mise en cache de prompt (prompt caching) du prompt système figé pour
  réduire le coût sur les appels répétés (1 appel par page).
- Sorties structurées (output_config.format) quand un schéma est fourni.

Nécessite ANTHROPIC_API_KEY dans l'environnement.
"""
from __future__ import annotations

import json
import os

import anthropic

MODEL = os.environ.get("SPN_MODEL", "claude-opus-4-8")
_client: anthropic.Anthropic | None = None


def client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def complete(
    system: str,
    user: str,
    *,
    schema: dict | None = None,
    max_tokens: int = 8000,
    effort: str = "medium",
) -> str | dict:
    """Un appel Claude. Le prompt système est mis en cache (caching).

    Si `schema` est fourni, renvoie un dict validé contre le schéma JSON ;
    sinon renvoie le texte de la réponse.
    """
    kwargs: dict = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": effort},
        # Prompt système figé + cache_control → réutilisé d'un appel à l'autre.
        "system": [{
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"},
        }],
        "messages": [{"role": "user", "content": user}],
    }
    if schema is not None:
        kwargs["output_config"]["format"] = {"type": "json_schema", "schema": schema}

    resp = client().messages.create(**kwargs)
    text = next((b.text for b in resp.content if b.type == "text"), "")
    if schema is not None:
        return json.loads(text)
    return text
