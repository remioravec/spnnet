#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remet les pages arrondissements et départements au gabarit du site.

Le 21/09/2026, ces 24 pages ont été repassées sur le gabarit « article » :
elles ont gardé un bon contenu local, mais perdu tous les modules d'interface
des pages secteur — hero, logos clients, chiffres, bande promesse, équipe,
réalisations, process, avis Google, barre mobile collante.

Ce script ne réécrit pas le contenu : il le reprend tel quel et le repose dans
le gabarit de `make_zone.build()`.

    python3 agents/landing/make_zone_relift.py paris-8            # fichier local
    python3 agents/landing/make_zone_relift.py --all              # les 24, en local
    python3 agents/landing/make_zone_relift.py paris-8 --deploy

Les sections du contenu en ligne sont réparties ainsi :
    1re section          -> chapeau du bloc « expertise locale »
    « Pourquoi… »        -> encadré latéral de ce bloc
    prestations, technique, autres -> sections pleine largeur en dessous
    « zone de couverture »-> paragraphe du module ZONE
    FAQ                  -> accordéon + JSON-LD FAQPage
    devis, aller plus loin, avis, CTA final -> écartés, le gabarit les fournit
"""
import json, os, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))

import make_zone as mz
from zones_data import ALL_ZONES

OUT = HERE
BAND = re.compile(r'<!-- spn-band v1 -->.*?<!-- /spn-band -->', re.S)

# Le bloc « reponse en une phrase » vient du gabarit article : le gabarit
# landing n'en porte pas le style, on l'apporte avec lui.
ANSWER_CSS = (
    ".spn-lp .nb-answer{background:#fff;border:1px solid var(--line,#e9e4dd);"
    "border-left:4px solid var(--o,#d8431f);border-radius:0 14px 14px 0;"
    "padding:18px 22px;margin:0 0 26px;max-width:820px}"
    ".spn-lp .nb-answer .tag{display:inline-block;font-size:.68rem;font-weight:800;"
    "letter-spacing:.09em;text-transform:uppercase;color:var(--o,#d8431f);margin-bottom:8px}"
    ".spn-lp .nb-answer p{margin:0;font-size:1rem;line-height:1.6;color:#2a2d35}")

TARGETS = [f"paris-{i}" for i in range(1, 21)] + [
    "77-seine-et-marne", "92-hauts-de-seine", "93-seine-saint-denis", "94-val-de-marne"]

# Ce que le gabarit fournit déjà : on ne le reprend pas du contenu en ligne.
# Le gabarit fournit deja ces blocs : les reprendre les ferait en double.
DROP = ("aller plus loin", "nos clients parlent", "des locaux impeccables")


# ---------------------------------------------------------------- extraction

WRAP = re.compile(r"<!--\s*/?wp:html\s*-->")


SRC_DIR = os.environ.get("SPN_RELIFT_SRC")  # repartir d'une sauvegarde plutot que du live


def live_content(slug):
    r = mz.requests.get(mz.API, params={"slug": slug, "context": "edit", "_fields": "id,content"},
                        auth=mz.AUTH, timeout=90).json()
    if not r:
        raise SystemExit(f"{slug} : page introuvable")
    pid = r[0]["id"]
    if SRC_DIR:
        # Le contenu en ligne peut deja etre une sortie de ce script : on
        # recolte alors depuis la sauvegarde d'origine, jamais depuis soi-meme.
        p = pathlib.Path(SRC_DIR) / f"{slug}.html"
        if not p.exists():
            raise SystemExit(f"{slug} : sauvegarde absente ({p})")
        return pid, WRAP.sub("", p.read_text(encoding="utf-8"))
    return pid, r[0]["content"]["raw"]


def sections(h):
    """Découpe le contenu en (titre H2, corps), styles et scripts retirés."""
    t = re.sub(r"<style[\s\S]*?</style>", "", h)
    t = re.sub(r"<script[\s\S]*?</script>", "", t)
    parts = re.split(r"<h2[^>]*>(.*?)</h2>", t, flags=re.S)
    out = []
    for i in range(1, len(parts), 2):
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", parts[i])).strip()
        out.append((title, parts[i + 1] if i + 1 < len(parts) else ""))
    return out


def kind(title):
    t = title.lower()
    if "question" in t:                                   return "FAQ"
    if any(d in t for d in DROP):                         return "DROP"
    if "zone" in t or "couverture" in t:                  return "ZONE"
    if "pourquoi" in t:                                   return "POURQUOI"
    return "CORPS"


def faq_items(body):
    items = []
    for m in re.finditer(r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>", body, re.S):
        q = clean(m.group(1))
        a = re.sub(r"\s+", " ", m.group(2)).strip()
        a = re.sub(r'^\s*<div class="body">(.*)</div>\s*$', r"\1", a, flags=re.S).strip()
        if q:
            items.append((q, a))
    if not items:
        hs = re.split(r"<h3[^>]*>(.*?)</h3>", body, flags=re.S)
        for i in range(1, len(hs), 2):
            q = clean(hs[i])
            a = re.sub(r"\s+", " ", hs[i + 1] if i + 1 < len(hs) else "").strip()
            if q:
                items.append((q, a))
    return items


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def tidy(body):
    """Nettoie un corps de section repris du gabarit article."""
    b = re.sub(r"<div class=\"(?:art-cta|toc|sidebar)[\s\S]*?</div>", "", body)
    b = re.sub(r"\s*<a[^>]*class=\"[^\"]*(?:btn|cta)[^\"]*\"[^>]*>.*?</a>\s*", "", b, flags=re.S)
    return b.strip()


ANSWER = re.compile(r'<div class="nb-answer[^"]*"[^>]*>[\s\S]*?</div>\s*(?=<h2)')
H1_RX  = re.compile(r"<h1[^>]*>([\s\S]*?)</h1>")
# Le chapeau du gabarit article : le <p> pose entre le H1 et la ligne de meta.
LEAD_RX = re.compile(r"</h1>\s*<p[^>]*>([\s\S]*?)</p>")


def harvest(slug):
    pid, h = live_content(slug)
    out = {"id": pid, "corps": [], "pourquoi": None, "zone": None, "faq": [],
           "answer": None, "h1": None, "lead": None}
    m = ANSWER.search(h)
    if m:
        out["answer"] = m.group(0).strip()
    # H1 et chapeau : on garde ceux de la page en ligne. Le H1 du generateur
    # vise « societe de nettoyage de bureaux », requete deja portee par la page
    # soeur /societe-nettoyage-bureaux-paris-N/ : le reprendre ici creerait une
    # cannibalisation.
    m = H1_RX.search(h)
    if m:
        out["h1"] = re.sub(r"\s+", " ", m.group(1)).strip()
    m = LEAD_RX.search(h)
    if m:
        lead = re.sub(r"\s+", " ", m.group(1)).strip()
        if 40 < len(lead) < 500:
            out["lead"] = lead
    for title, body in sections(h):
        k = kind(title)
        if k == "DROP":
            continue
        if k == "FAQ":
            out["faq"] = faq_items(body)
        elif k == "POURQUOI" and out["pourquoi"] is None:
            out["pourquoi"] = (title, tidy(body))
        elif k == "ZONE" and out["zone"] is None:
            out["zone"] = (title, tidy(body))
        else:
            out["corps"].append((title, tidy(body)))
    return out


# ---------------------------------------------------------------- re-gabarit

def local_block(z, x):
    """Le bloc « expertise locale » du gabarit, rempli du contenu de la page."""
    chips = "".join(f"<span>{q}</span>" for q in z["quartiers"])
    head_title, head_body = x["corps"][0]
    rest = x["corps"][1:]

    if x["pourquoi"]:
        ptitle, pbody = x["pourquoi"]
        side = f'      <h3>{ptitle}</h3>\n{pbody}\n'
    else:
        side = (f'      <h3>Pourquoi {z["name"]} nous choisit</h3>\n'
                '      <ul class="hero-points" style="margin:0">\n'
                '        <li>Intervention avant 9h ou après 18h</li>\n'
                '        <li>Équipes formées &amp; fidélisées</li>\n'
                '        <li>Un interlocuteur dédié, joignable</li>\n'
                '        <li>Devis sous 24h, sans engagement</li>\n'
                '      </ul>\n')

    more = ""
    for title, body in rest:
        more += (f'  <div style="margin-top:40px" class="reveal">\n'
                 f'    <h3 style="font-family:\'Fraunces\',serif;font-weight:600;'
                 f'font-size:1.4rem;margin-bottom:14px">{title}</h3>\n'
                 f'{body}\n  </div>\n')

    return (
        '\n<!-- ============ CONTENU LOCAL ============ -->\n'
        '<div class="sec local"><div class="wrap">\n'
        '  <div class="sec-head reveal" style="max-width:820px;text-align:left;margin:0 0 30px">'
        f'<span class="eyebrow">Expertise locale · {z["short"]}</span>'
        f'<h2>{head_title}</h2></div>\n'
        + (x["answer"] + "\n" if x["answer"] else "")
        + mz.facts(z) +
        '\n  <div class="grid">\n    <div class="reveal">\n'
        f'{head_body}\n'
        f'      <div class="qtiers">{chips}</div>\n'
        '    </div>\n'
        '    <div class="side reveal">\n' + side + '    </div>\n  </div>\n'
        + more +
        '</div></div>\n\n<!-- ============ WHY US ============ -->')


def build(slug):
    z = dict(ALL_ZONES[slug])
    x = harvest(slug)
    if x["h1"]:
        z["h1"] = x["h1"]
    if x["lead"]:
        z["lead"] = x["lead"]
    if not x["corps"]:
        raise SystemExit(f"{slug} : aucune section de contenu reperee")
    if len(x["faq"]) < 3:
        raise SystemExit(f"{slug} : FAQ trop courte ({len(x['faq'])})")

    orig_local, orig_faq, orig_zonep = mz.local, mz.faq_html, mz.A_ZONEP
    mz.local = lambda _z: local_block(_z, x)
    mz.faq_html = lambda _z: (
        "".join(f'    <details class="acc"><summary>{q}<span class="pl">+</span></summary>'
                f'<div class="body">{a}</div></details>\n' for q, a in x["faq"]).rstrip("\n"),
        [(q, clean(a)) for q, a in x["faq"]])
    try:
        h = mz.build(z)
    finally:
        mz.local, mz.faq_html = orig_local, orig_faq

    if x["zone"]:
        zp = re.sub(r"<h[23][^>]*>.*?</h[23]>", "", x["zone"][1], flags=re.S).strip()
        h = h.replace(
            f'<p>Notre base dans les Hauts-de-Seine nous rend très réactifs sur {z["name"]}. '
            f'Nous intervenons dans {z["zone"]} ({", ".join(z["quartiers"][:4])}…) et, plus largement, '
            "dans tout Paris et l'Île-de-France.</p>", zp, 1)

    if x["answer"] and ".nb-answer{" not in h:
        h = h.replace("</style>", ANSWER_CSS + "</style>", 1)

    # le bandeau du guide, pose a l'identique sur les autres pages
    i = h.find("<!-- ============ CLIENTS LOGOS")
    if i != -1 and "<!-- spn-band v1 -->" not in h:
        import make_bandeau as mb
        h = h[:i] + mb.BAND + "\n" + h[i:]
    return x["id"], h


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    deploy = "--deploy" in sys.argv
    slugs = TARGETS if "--all" in sys.argv else args
    if not slugs:
        raise SystemExit(__doc__)
    for s in slugs:
        pid, h = build(s)
        (OUT / f"relift-{s}.html").write_text(h, encoding="utf-8")
        n = len(re.findall(r'<div class="sec |<div class="hero"|<div class="clients"'
                           r'|<div class="stats"|<div class="promise"', h))
        print(f"  {s:22} id={pid:5} {len(h):7} o · {n} modules"
              + ("  -> deploye" if deploy else ""))
        if deploy:
            # Le wrapper wp:html est obligatoire : sans lui WordPress applique
            # wpautop au contenu et injecte des <p>/</p> a l'interieur du CSS
            # et du JS, ce qui casse la page. C'est ce que fait make_zone.deploy().
            payload = {"content": "<!-- wp:html -->\n" + h + "\n<!-- /wp:html -->",
                       "template": "elementor_header_footer",
                       "meta": {"_elementor_edit_mode": ""}}
            r = mz.requests.post(f"{mz.API}/{pid}", auth=mz.AUTH, timeout=180, json=payload)
            if r.status_code != 200:
                print(f"     ECHEC {r.status_code} {r.text[:160]}")


if __name__ == "__main__":
    main()
