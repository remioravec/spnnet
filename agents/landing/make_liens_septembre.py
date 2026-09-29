#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les 6 liens entrants in-body vers les 3 contenus de septembre.

Memes regles que pour le hub (CLAUDE.md §4) : une phrase complete, dans le
premier tiers du texte de sa section, jamais en « lire aussi », jamais dans une
carte, jamais dans le bloc « reponse en une phrase ». Six sources distinctes,
six ancres distinctes.

Les pages qui portent deja le lien du hub recoivent celui-ci dans un paragraphe
different, pour ne pas empiler deux liens dans la meme phrase.

    python3 agents/landing/make_liens_septembre.py [--apply]
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
import make_zone as mz

MARK = "spn-lien-sept"
RESIL = "https://spn-net.fr/resilier-contrat-nettoyage/"
CDC = "https://spn-net.fr/cahier-des-charges-nettoyage-bureaux/"
LITIGE = "https://spn-net.fr/prestataire-nettoyage-ne-respecte-pas-contrat/"

# source -> (cible, ancre, phrase, emplacement, index du paragraphe)
LIENS = {
    "changer-de-prestataire-nettoyage": (
        RESIL, "résilier votre contrat de nettoyage",
        "Tout commence par une date : {a} suppose de respecter le préavis prévu, faute de quoi le contrat repart pour un an.",
        "head:INFOS", 0),
    "annexe-7-changer-entreprise-nettoyage": (
        RESIL, "résilier un contrat de nettoyage",
        "La reprise des agents ne se pose qu'une fois la sortie engagée : {a} obéit à son propre calendrier, à traiter en premier.",
        "art", 4),
    "prix-nettoyage-bureaux-paris": (
        CDC, "cahier des charges de nettoyage",
        "Encore faut-il que les deux devis portent sur le même périmètre : c'est exactement le rôle d'un {a}.",
        "art", 2),
    "tertiaire": (
        CDC, "cahier des charges de nettoyage de bureaux",
        "Avant de consulter, écrivez ce que vous attendez : notre modèle de {a} se remplit zone par zone.",
        "local", 1),
    "qualite-nettoyage-baisse-apres-3-mois": (
        LITIGE, "quand le prestataire ne respecte pas le contrat",
        "Passé un certain stade, le constat ne suffit plus : voici quels recours vous avez {a}.",
        "art", 3),
    "travail-dissimule-entreprise-nettoyage": (
        LITIGE, "mettre en demeure un prestataire défaillant",
        "La conformité administrative n'est qu'une partie du sujet : savoir {a} relève d'une autre procédure, que nous détaillons à part.",
        "art", 1),
}


def paragraphs(html, where):
    """Liste des spans de <p> candidats dans la section visee."""
    if where == "local":
        m = re.search(r'<div class="sec local">[\s\S]*?<div class="grid">\s*<div class="reveal">',
                      html)
        if not m:
            return []
        start, end = m.end(), html.find("</div>", m.end())
        seg = html[start:end if end != -1 else len(html)]
        return [(start + x.start(1), start + x.end(1))
                for x in re.finditer(r"<p>([\s\S]{60,}?)</p>", seg)]
    if where == "art":
        i = html.find('<article class="art-main">')
        if i == -1:
            return []
        m = re.compile(r'<div class="nb-answer[^"]*"[^>]*>[\s\S]*?</div>').search(html, i)
        if m:
            i = m.end()
        out = []
        for x in re.finditer(r"<p>([\s\S]{60,}?)</p>", html[i:i + 12000]):
            out.append((i + x.start(1), i + x.end(1)))
        return out
    if where.startswith("head:"):
        j = html.find(f"============ {where[5:]} ")
        if j == -1:
            return []
        m = re.compile(r'<div class="sec-head[^"]*"[^>]*>[\s\S]*?<p>([\s\S]*?)</p>').search(html, j)
        return [m.span(1)] if m else []
    return []


def place(html, slug):
    if f"data-{MARK}" in html:
        return None, "déjà posé"
    url, anchor, tpl, where, idx = LIENS[slug]
    ps = paragraphs(html, where)
    if len(ps) <= idx:
        return None, f"PARAGRAPHE {idx} INTROUVABLE ({len(ps)} trouvé)"
    a = f'<a href="{url}" data-{MARK}>{anchor}</a>'
    e = ps[idx][1]
    return html[:e] + " " + tpl.format(a=a) + html[e:], "posé"


def main():
    apply_ = "--apply" in sys.argv
    ok = ko = 0
    print(f"{'source':46} {'etat':26} ancre")
    for slug in LIENS:
        r = mz.requests.get(mz.API, params={"slug": slug, "context": "edit",
                                            "_fields": "id,content"},
                            auth=mz.AUTH, timeout=90).json()
        if not r:
            print(f"{slug:46} PAGE INTROUVABLE"); ko += 1; continue
        pid, raw = r[0]["id"], r[0]["content"]["raw"]
        new, why = place(raw, slug)
        print(f"{'' if apply_ else '[simu] '}{slug:46} {why:26} « {LIENS[slug][1]} »")
        if new is None:
            ko += "INTROUVABLE" in why
            continue
        ok += 1
        if apply_:
            body = new if "<!-- wp:html -->" in new else f"<!-- wp:html -->\n{new}\n<!-- /wp:html -->"
            resp = mz.requests.post(f"{mz.API}/{pid}", auth=mz.AUTH, timeout=180,
                                    json={"content": body})
            if resp.status_code != 200:
                print(f"    ECHEC {resp.status_code} {resp.text[:160]}"); ko += 1; ok -= 1
    print(f"\n{ok} lien(s) · {ko} probleme(s)")
    if not apply_:
        print("Simulation. Relancer avec --apply.")


if __name__ == "__main__":
    main()
