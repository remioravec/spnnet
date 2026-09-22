#!/usr/bin/env python3
"""Crawler d'audit pour spn-net.fr.

Récupère toutes les URL du sitemap, parse le HTML et extrait :
- métadonnées SEO (title, meta description, canonical, robots, og)
- structure des titres (h1..h3)
- volume et lisibilité du contenu
- liens internes/externes avec ancre, position et attributs
- boutons / call-to-action

Les données brutes sont écrites en JSON dans audit/data/ pour analyse.
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE = "https://spn-net.fr"
DATA_DIR = Path(__file__).parent / "data"
UA = "SPN-Audit-Bot/1.0 (+audit interne; respect robots)"
TIMEOUT = 30


def get_sitemap_urls() -> list[str]:
    """Récupère toutes les URL via l'index de sitemaps."""
    urls: list[str] = []
    index = requests.get(f"{BASE}/sitemap.xml", headers={"User-Agent": UA}, timeout=TIMEOUT)
    sub_sitemaps = re.findall(r"<loc>([^<]+)</loc>", index.text)
    for sm in sub_sitemaps:
        if sm.endswith(".xml"):
            r = requests.get(sm, headers={"User-Agent": UA}, timeout=TIMEOUT)
            urls += re.findall(r"<loc>([^<]+)</loc>", r.text)
    # homepage + dédoublonnage en gardant l'ordre
    urls = [BASE + "/"] + [u for u in urls if not u.endswith(".xml")]
    seen: dict[str, None] = {}
    for u in urls:
        seen.setdefault(u.rstrip("/") + "/", None)
    return list(seen)


@dataclass
class LinkInfo:
    href: str
    anchor: str
    is_internal: bool
    rel: str
    target_path: str
    section: str  # header / nav / main / footer / unknown
    is_button: bool
    nofollow: bool


@dataclass
class PageAudit:
    url: str
    status: int
    title: str = ""
    title_len: int = 0
    meta_description: str = ""
    meta_desc_len: int = 0
    canonical: str = ""
    meta_robots: str = ""
    h1: list[str] = field(default_factory=list)
    h2: list[str] = field(default_factory=list)
    h3: list[str] = field(default_factory=list)
    word_count: int = 0
    text_sample: str = ""
    img_count: int = 0
    img_without_alt: int = 0
    links: list[dict] = field(default_factory=list)
    buttons: list[str] = field(default_factory=list)
    lang: str = ""
    load_seconds: float = 0.0
    html_bytes: int = 0


def classify_section(tag) -> str:
    for parent in tag.parents:
        name = (parent.name or "").lower()
        cls = " ".join(parent.get("class", [])).lower()
        pid = (parent.get("id") or "").lower()
        blob = f"{name} {cls} {pid}"
        if name == "footer" or "footer" in blob:
            return "footer"
        if name == "header" or "header" in blob or "topbar" in blob:
            return "header"
        if name == "nav" or "menu" in blob or "nav" in blob:
            return "nav"
        if name == "main" or "content" in blob or "entry" in blob or "elementor-widget-container" in blob:
            return "main"
    return "unknown"


def looks_like_button(tag) -> bool:
    cls = " ".join(tag.get("class", [])).lower()
    if any(k in cls for k in ("btn", "button", "cta", "elementor-button")):
        return True
    if tag.name == "button":
        return True
    return False


def audit_page(url: str) -> PageAudit:
    t0 = time.time()
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
    except Exception as e:  # noqa: BLE001
        pa = PageAudit(url=url, status=-1)
        pa.text_sample = f"ERREUR: {e}"
        return pa
    load = time.time() - t0
    pa = PageAudit(url=url, status=r.status_code, load_seconds=round(load, 3),
                   html_bytes=len(r.content))
    if r.status_code != 200:
        return pa

    soup = BeautifulSoup(r.text, "lxml")
    if soup.html and soup.html.get("lang"):
        pa.lang = soup.html.get("lang")

    if soup.title and soup.title.string:
        pa.title = soup.title.string.strip()
        pa.title_len = len(pa.title)

    md = soup.find("meta", attrs={"name": "description"})
    if md and md.get("content"):
        pa.meta_description = md["content"].strip()
        pa.meta_desc_len = len(pa.meta_description)

    can = soup.find("link", attrs={"rel": "canonical"})
    if can and can.get("href"):
        pa.canonical = can["href"]
    mr = soup.find("meta", attrs={"name": "robots"})
    if mr and mr.get("content"):
        pa.meta_robots = mr["content"]

    pa.h1 = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
    pa.h2 = [h.get_text(" ", strip=True) for h in soup.find_all("h2")]
    pa.h3 = [h.get_text(" ", strip=True) for h in soup.find_all("h3")]

    # Texte visible (exclut scripts/styles/nav/footer pour estimer le corps)
    for bad in soup(["script", "style", "noscript"]):
        bad.decompose()
    body_text = soup.get_text(" ", strip=True)
    body_text = re.sub(r"\s+", " ", body_text)
    words = body_text.split()
    pa.word_count = len(words)
    pa.text_sample = body_text[:2000]

    imgs = soup.find_all("img")
    pa.img_count = len(imgs)
    pa.img_without_alt = sum(1 for i in imgs if not (i.get("alt") or "").strip())

    base_host = urlparse(BASE).netloc
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            full = href
            target_path = href
            internal = False
        else:
            full = urljoin(url, href)
            internal = urlparse(full).netloc.endswith(base_host)
            target_path = urlparse(full).path or "/"
        anchor = a.get_text(" ", strip=True)
        rel = " ".join(a.get("rel", [])) if a.get("rel") else ""
        li = LinkInfo(
            href=full,
            anchor=anchor,
            is_internal=internal,
            rel=rel,
            target_path=target_path,
            section=classify_section(a),
            is_button=looks_like_button(a),
            nofollow="nofollow" in rel.lower(),
        )
        pa.links.append(asdict(li))

    for b in soup.find_all(["button"]):
        txt = b.get_text(" ", strip=True)
        if txt:
            pa.buttons.append(txt)

    return pa


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    urls = get_sitemap_urls()
    print(f"{len(urls)} URL à auditer")
    results = []
    for i, u in enumerate(urls, 1):
        pa = audit_page(u)
        results.append(asdict(pa))
        print(f"[{i:>2}/{len(urls)}] {pa.status} {u}  ({pa.word_count} mots, {len(pa.links)} liens)")
        time.sleep(0.4)  # politesse
    out = DATA_DIR / "pages.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nÉcrit: {out}")


if __name__ == "__main__":
    main()
