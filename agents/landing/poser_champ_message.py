#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Demandes d'Alexandra Guenantin du 13/10/2026, sur les formulaires du site.

1. « Peux-tu rajouter un encart non obligatoire pour qu'ils mettent des infos
   supp » — les formulaires des pages generees ne portent que 3 champs. Le
   JS d'envoi lit deja un champ `message` et le transmet au formulaire
   Elementor de /contact/ : il ne manque que le champ. Rien a changer cote JS.

2. L'encart sous le bouton affirme « nous ne recrutons pas actuellement ».
   C'est devenu faux : SPN NET ouvre un poste d'inspecteur. L'encart renvoie
   desormais vers /carrieres/.

Le champ est pose avec `data-optional`, que le validateur du site sait deja
lire : il n'est jamais bloquant.

Ecriture dans le contenu live, enveloppee dans wp:html (sinon wpautop casse
le CSS et le JS de la page). Idempotent : data-spn-msg.

Usage : python3 agents/landing/poser_champ_message.py [--dry]
"""
from __future__ import annotations

import base64
import json
import os
import re
import sys
import urllib.request

API = "https://spn-net.fr/wp-json/wp/v2"
AUTH = base64.b64encode(
    f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()

CHAMP = (
    '<div class="field" data-field data-optional data-spn-msg="1">'
    '<label>Informations complémentaires '
    '<span style="font-weight:600;color:var(--grey)">(facultatif)</span></label>'
    '<textarea name="message" rows="3" '
    'placeholder="Surfaces, nombre de passages souhaités, horaires d\'accès, '
    'contraintes du site…"></textarea></div>'
)

SVG = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" '
       'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
       'stroke-linejoin="round"><circle cx="12" cy="12" r="10"/>'
       '<path d="M12 16v-4M12 8h.01"/></svg>')

RECRUT = (
    '<div class="norecruit" data-spn-msg="1">' + SVG +
    '<span>Ce formulaire est réservé aux demandes de <b>devis</b>. '
    'Pour une candidature, nos offres sont sur la page '
    '<a href="https://spn-net.fr/carrieres/" style="color:inherit;'
    'text-decoration:underline">Carrières</a>.</span></div>'
)


def call(url, data=None, method="GET"):
    r = urllib.request.Request(url, method=method,
                               data=json.dumps(data).encode() if data else None)
    r.add_header("Authorization", "Basic " + AUTH)
    if data:
        r.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(r, timeout=120) as f:
        return json.loads(f.read().decode())


def patch(html):
    """Retourne (html, champs poses, encarts reecrits)."""
    champs = recrut = 0
    out, pos = [], 0
    for m in re.finditer(r'<form id="spn-form[^"]*"[^>]*>.*?</form>', html, re.S):
        f = m.group(0)
        out.append(html[pos:m.start()])
        pos = m.end()
        # 1. le champ, juste avant le bouton d'envoi
        if 'name="message"' not in f:
            b = re.search(r'<button[^>]*type="submit"', f) or re.search(r'<button', f)
            if b:
                f = f[:b.start()] + CHAMP + "\n      " + f[b.start():]
                champs += 1
        # 2. le sous-titre : 3 champs obligatoires, le 4e est facultatif
        f = f.replace("3 champs suffisent", "3 champs obligatoires")
        # 3. l'encart recrutement
        nf, n = re.subn(r'<div class="norecruit">.*?</div>\s*</div>\s*(?=</|$)',
                        RECRUT, f, flags=re.S)
        if n == 0:
            nf, n = re.subn(r'<div class="norecruit">.*?</span>\s*</div>',
                            RECRUT, f, flags=re.S)
        f, recrut = nf, recrut + n
        out.append(f)
    out.append(html[pos:])
    return "".join(out), champs, recrut


def pages():
    for ep in ("pages", "posts"):
        page = 1
        while True:
            items = call(f"{API}/{ep}?per_page=100&page={page}"
                         "&status=publish,draft,future,private&context=edit"
                         "&_fields=id,slug,content,type")
            if not items:
                return
            for it in items:
                yield ep, it
            if len(items) < 100:
                break
            page += 1


def main():
    dry = "--dry" in sys.argv
    tot = tc = tr = 0
    for ep, it in pages():
        html = it["content"]["raw"]
        if '<form id="spn-form' not in html:
            continue
        if 'data-spn-msg' in html:
            print(f"  {it['slug']:46} deja pose")
            continue
        new, c, r = patch(html)
        if c == 0 and r == 0:
            continue
        tot += 1
        tc += c
        tr += r
        print(f"  {it['slug']:46} {c} champ(s) · {r} encart(s)"
              + ("  [simulation]" if dry else ""))
        if dry:
            continue
        body = {"content": "<!-- wp:html -->\n" + new + "\n<!-- /wp:html -->",
                "template": "elementor_header_footer",
                "meta": {"_elementor_edit_mode": ""}}
        for essai in range(3):
            try:
                call(f"{API}/{ep}/{it['id']}", body, "POST")
                break
            except Exception as e:                       # noqa: BLE001
                if essai == 2:
                    print(f"    ERREUR {it['slug']} : {e}")
    print(f"\n{tot} pages · {tc} champs posés · {tr} encarts réécrits")


if __name__ == "__main__":
    main()
