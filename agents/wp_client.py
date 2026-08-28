#!/usr/bin/env python3
"""Client WordPress REST pour spn-net.fr.

Lecture publique (toujours possible) + écriture authentifiée (mot de passe
d'application). L'écriture nécessite que le serveur transmette l'en-tête
Authorization à PHP — voir audit/reports/AUDIT.md (correctif .htaccess).

Identifiants lus depuis l'environnement :
  WP_BASE_URL   (défaut https://spn-net.fr)
  WP_USER       login ou e-mail
  WP_APP_PASSWORD  mot de passe d'application (espaces tolérés)
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import requests

WP_BASE_URL = os.environ.get("WP_BASE_URL", "https://spn-net.fr").rstrip("/")
WP_USER = os.environ.get("WP_USER", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
TIMEOUT = 30
UA = "SPN-Agent/1.0"


class WordPressError(RuntimeError):
    pass


@dataclass
class WPContent:
    """Représente une page/article WordPress."""
    id: int
    type: str  # "posts" | "pages"
    slug: str
    link: str
    title: str
    content_html: str
    raw: dict


class WordPressClient:
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": UA})
        self._auth = None
        if WP_USER and WP_APP_PASSWORD:
            self._auth = (WP_USER, WP_APP_PASSWORD)

    # ---- lecture (publique) ----
    def get_by_slug(self, slug: str, post_type: str = "posts") -> WPContent | None:
        url = f"{WP_BASE_URL}/wp-json/wp/v2/{post_type}"
        r = self.session.get(url, params={"slug": slug, "context": "view"}, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        if not data:
            return None
        item = data[0]
        return self._to_content(item, post_type)

    def find_by_link(self, link: str) -> WPContent | None:
        """Résout une URL publique en page ou article."""
        slug = link.rstrip("/").rsplit("/", 1)[-1]
        for pt in ("pages", "posts"):
            try:
                c = self.get_by_slug(slug, pt)
                if c:
                    return c
            except requests.HTTPError:
                continue
        return None

    def _to_content(self, item: dict, post_type: str) -> WPContent:
        return WPContent(
            id=item["id"],
            type=post_type,
            slug=item.get("slug", ""),
            link=item.get("link", ""),
            title=item.get("title", {}).get("rendered", ""),
            content_html=item.get("content", {}).get("rendered", ""),
            raw=item,
        )

    # ---- écriture (authentifiée) ----
    def verify_auth(self) -> tuple[bool, str]:
        """Teste l'authentification. Retourne (ok, message)."""
        if not self._auth:
            return False, "WP_USER / WP_APP_PASSWORD non définis dans l'environnement."
        url = f"{WP_BASE_URL}/wp-json/wp/v2/users/me?context=edit"
        r = self.session.get(url, auth=self._auth, timeout=TIMEOUT)
        if r.status_code == 200:
            return True, f"Authentifié en tant que {r.json().get('name')}"
        if r.status_code == 401:
            return False, ("401 — le serveur ne transmet probablement pas l'en-tête "
                           "Authorization à PHP (voir correctif .htaccess dans l'audit).")
        return False, f"HTTP {r.status_code}: {r.text[:200]}"

    def update_content(self, content: WPContent, new_html: str) -> dict:
        """Met à jour le HTML d'une page/article. Respecte dry_run."""
        if self.dry_run:
            return {"dry_run": True, "id": content.id, "would_update": True}
        if not self._auth:
            raise WordPressError("Écriture impossible : identifiants manquants.")
        url = f"{WP_BASE_URL}/wp-json/wp/v2/{content.type}/{content.id}"
        r = self.session.post(url, auth=self._auth, json={"content": new_html}, timeout=TIMEOUT)
        if r.status_code not in (200, 201):
            raise WordPressError(f"Échec mise à jour {content.id}: HTTP {r.status_code} {r.text[:200]}")
        return r.json()
