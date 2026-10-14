#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pose les infographies dans le contenu LIVE d'une page, sans la regenerer.

Pourquoi ne pas repasser par le generateur : la page cahier des charges a recu
trois sections ecrites en direct apres sa mise en ligne. Un rebuild les perdrait.
On lit donc le contenu publie, on y insere les blocs, on reecrit.

Regles tenues :
  - un visuel par section de fond, pose a la fin de la prose, avant le module
    de la section et avant le H2 suivant ;
  - le CSS .vz est injecte DANS la balise <style> existante (sinon wpautop) ;
  - idempotent : le marqueur data-spn-vz empeche toute seconde pose ;
  - l'ecriture passe par le wrapper <!-- wp:html -->, sans quoi wpautop casse
    le CSS et le JS de la page.

Usage : python3 agents/landing/poser_visuels.py [--dry]
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
import base64

sys.path.insert(0, os.path.dirname(__file__))
import visuels as vz              # noqa: E402
import septembre_visuels as sv    # noqa: E402

API = "https://spn-net.fr/wp-json/wp/v2"
AUTH = base64.b64encode(
    f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()

MARQ = "data-spn-vz"

# page -> [(ancre du H2, bloc)] ; l'ancre est l'id du H2 ou un fragment du titre
PLAN = {
    3707: {"slug": "resilier-contrat-nettoyage",
           "blocs": [("calendrier", sv.V_RESIL["calendrier"]),
                     ("chatel",     sv.V_RESIL["chatel"]),
                     ("lettre",     sv.V_RESIL["lettre"]),
                     ("apres",      sv.V_RESIL["apres"]),
                     ("faute",      sv.V_RESIL["faute"] + sv.CTA_RESIL)]},
    3709: {"slug": "cahier-des-charges-nettoyage-bureaux",
           "blocs": [("pourquoi",   sv.V_CDC["pourquoi"]),
                     ("besoins",    sv.V_CDC["besoins"]),
                     ("frequences", sv.V_CDC["frequences"]),
                     ("types",      sv.V_CDC["types"]),
                     ("qualite",    sv.V_CDC["qualite"]),
                     ("erreurs",    sv.V_CDC["erreurs"] + sv.CTA_CDC)]},
    3711: {"slug": "prestataire-nettoyage-ne-respecte-pas-contrat",
           "blocs": [("constater",  sv.V_LITIGE["constater"]),
                     ("demeure",    sv.V_LITIGE["demeure"]),
                     ("faute",      sv.V_LITIGE["faute"]),
                     ("eviter",     sv.V_LITIGE["eviter"] + sv.CTA_LITIGE)]},
    3754: {"slug": "carrieres",
           "blocs": [("formulaire", sv.V_CARR["formulaire"]),
                     ("postuler",   sv.V_CARR["postuler"]),
                     ("devis",      sv.V_CARR["devis"] + sv.CTA_CARR)]},
}

# pour les pages dont les H2 n'ont pas d'id : fragment de titre -> rang
TITRES = {
    "formulaire": "formulaire du site ne convient pas",
    "postuler":   "Comment postuler",
    "devis":      "cherchiez un devis",
}


def call(url, data=None, method="GET"):
    r = urllib.request.Request(url, method=method,
                               data=json.dumps(data).encode() if data else None)
    r.add_header("Authorization", "Basic " + AUTH)
    if data:
        r.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(r, timeout=90) as f:
        return json.loads(f.read().decode())


def sections(html):
    """Decoupe le corps en (debut, fin) par H2, dans l'ordre du document."""
    hs = list(re.finditer(r"<h2\b[^>]*>.*?</h2>", html, re.S))
    out = []
    for i, m in enumerate(hs):
        fin = hs[i + 1].start() if i + 1 < len(hs) else len(html)
        out.append((m.group(0), m.end(), fin))
    return out


def point_insertion(html, deb, fin):
    """Fin de la prose : avant le premier module de la section, sur un </p>."""
    bloc = html[deb:fin]
    mod = re.search(r'<(?:div|section|form|table|figure)\b[^>]*class="[^"]*\b'
                    r'(?:nb-|tbl|lettre|midcta)', bloc)
    limite = mod.start() if mod else len(bloc)
    ps = [m.end() for m in re.finditer(r"</p>", bloc[:limite])]
    if not ps:
        return None
    return deb + ps[-1]


def poser(page_id, conf, dry):
    p = call(f"{API}/pages/{page_id}?context=edit&_fields=id,slug,status,content")
    html = p["content"]["raw"]
    if MARQ in html:
        return f"{conf['slug']:46} deja pose"

    secs = sections(html)
    index = {}
    for titre, deb, fin in secs:
        idm = re.search(r'id="([^"]+)"', titre)
        if idm:
            index[idm.group(1)] = (deb, fin)
        index.setdefault("__titre__" + re.sub("<[^>]+>", "", titre), (deb, fin))

    poses, manques = [], []
    for ancre, bloc in conf["blocs"]:
        cle = index.get(ancre)
        if cle is None and ancre in TITRES:
            frag = TITRES[ancre]
            for k, v in index.items():
                if k.startswith("__titre__") and frag in k:
                    cle = v
                    break
        if cle is None:
            manques.append(ancre)
            continue
        poses.append((cle, bloc))

    if manques:
        return f"{conf['slug']:46} ANCRES INTROUVABLES {manques}"

    # on insere de la fin vers le debut pour ne pas decaler les offsets
    poses.sort(key=lambda x: x[0][0], reverse=True)
    n = 0
    for (deb, fin), bloc in poses:
        pos = point_insertion(html, deb, fin)
        if pos is None:
            return f"{conf['slug']:46} PAS DE PARAGRAPHE section a {deb}"
        html = html[:pos] + bloc + html[pos:]
        n += 1

    # marqueur + CSS dans la balise style existante
    html = html.replace('<div class="vz rv">', f'<div class="vz rv" {MARQ}="1">')
    css = vz.CSS.replace("<style>", "").replace("</style>", "") + \
        vz.EXTRA.replace("<style>", "").replace("</style>", "")
    if "</style>" in html:
        html = html.replace("</style>", css + "</style>", 1)
    else:
        html = "<style>" + css + "</style>" + html

    if dry:
        open(os.path.join(os.path.dirname(__file__),
                          f"live-{conf['slug']}.html"), "w", encoding="utf-8").write(html)
        return f"{conf['slug']:46} {n} visuels · {len(html):7} o  [simulation]"

    body = {"content": "<!-- wp:html -->\n" + html + "\n<!-- /wp:html -->",
            "template": "elementor_header_footer",
            "meta": {"_elementor_edit_mode": ""}}
    call(f"{API}/pages/{page_id}", body, "POST")
    return f"{conf['slug']:46} {n} visuels · {len(html):7} o  publie"


def main():
    dry = "--dry" in sys.argv
    for pid, conf in PLAN.items():
        try:
            print("  " + poser(pid, conf, dry))
        except Exception as e:                       # noqa: BLE001
            print(f"  {conf['slug']:46} ERREUR {e}")


if __name__ == "__main__":
    main()
