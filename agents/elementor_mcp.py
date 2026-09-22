#!/usr/bin/env python3
"""Client minimal pour le serveur MCP Elementor de spn-net.fr (transport HTTP).

Gère l'initialisation, la session (Mcp-Session-Id) et l'appel d'outils.
Identifiants via l'environnement : WP_USER, WP_APP_PASSWORD.

Exemple :
    mcp = ElementorMCP()
    mcp.initialize()
    res = mcp.call("elementor-mcp-find-element",
                   {"pageId": 686, "widgetType": "heading"})
"""
from __future__ import annotations

import base64
import json
import os

import requests

ENDPOINT = "https://spn-net.fr/wp-json/mcp/elementor-mcp-server"


class ElementorMCP:
    def __init__(self):
        u, p = os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"]
        self._b64 = base64.b64encode(f"{u}:{p}".encode()).decode()
        self.session_id: str | None = None
        self._id = 0

    def _headers(self) -> dict:
        h = {
            "Authorization": f"Basic {self._b64}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session_id:
            h["Mcp-Session-Id"] = self.session_id
        return h

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    @staticmethod
    def _parse(text: str) -> dict:
        """Gère réponse JSON simple ou flux SSE (lignes 'data: ...')."""
        for line in reversed(text.strip().splitlines()):
            line = line.strip()
            if line.startswith("data:"):
                line = line[5:].strip()
            if line.startswith("{"):
                return json.loads(line)
        raise RuntimeError(f"Réponse MCP non parsable: {text[:200]}")

    def initialize(self) -> None:
        r = requests.post(ENDPOINT, headers=self._headers(), timeout=40, data=json.dumps({
            "jsonrpc": "2.0", "id": self._next_id(), "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                       "clientInfo": {"name": "spn-cli", "version": "1.0"}},
        }))
        r.raise_for_status()
        self.session_id = r.headers.get("Mcp-Session-Id")
        # notification initialisée
        requests.post(ENDPOINT, headers=self._headers(), timeout=30,
                      data=json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}))

    def call(self, tool: str, arguments: dict) -> dict:
        r = requests.post(ENDPOINT, headers=self._headers(), timeout=90, data=json.dumps({
            "jsonrpc": "2.0", "id": self._next_id(), "method": "tools/call",
            "params": {"name": tool, "arguments": arguments},
        }))
        r.raise_for_status()
        out = self._parse(r.text)
        if "error" in out:
            raise RuntimeError(f"MCP {tool} erreur: {out['error']}")
        result = out.get("result", {})
        # Les outils renvoient souvent un content[].text JSON.
        content = result.get("content")
        if content and isinstance(content, list):
            texts = [c.get("text", "") for c in content if c.get("type") == "text"]
            joined = "\n".join(texts)
            try:
                return {"parsed": json.loads(joined), "raw": result}
            except (json.JSONDecodeError, ValueError):
                return {"text": joined, "raw": result}
        return result


if __name__ == "__main__":
    import sys
    mcp = ElementorMCP()
    mcp.initialize()
    print(f"session={mcp.session_id}")
    if len(sys.argv) > 2:
        print(json.dumps(mcp.call(sys.argv[1], json.loads(sys.argv[2])),
                         ensure_ascii=False, indent=2)[:3000])
