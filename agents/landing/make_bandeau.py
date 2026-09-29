#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bandeau vers le hub d'achat, posé directement dans le post_content via l'API REST.

Le bloc est encadré de marqueurs : le script est donc rejouable. Il remplace le
bloc existant s'il le trouve, il l'insère sinon, et `--remove` le retire.

    python3 agents/landing/make_bandeau.py            # simulation
    python3 agents/landing/make_bandeau.py --apply
    python3 agents/landing/make_bandeau.py --remove --apply

Points d'insertion relevés sur les 93 pages le 21/09/2026 :
  - gabarit landing (60)  : avant le bandeau de logos clients, donc juste après le hero ;
  - gabarit article (24)  : avant le corps de l'article, donc juste après le hero ;
  - le reste              : en fin de contenu (aucun cas aujourd'hui).
Dans les trois cas le bandeau reste sous le H1, jamais au-dessus.
"""
import base64, json, os, re, sys, time, urllib.error, urllib.request

API    = "https://spn-net.fr/wp-json/wp/v2"
TARGET = "https://spn-net.fr/choisir-entreprise-nettoyage/"
IMG    = "https://spn-net.fr/wp-content/uploads/2026/02/tertiaire-2.jpg"

OPEN, CLOSE = "<!-- spn-band v1 -->", "<!-- /spn-band -->"
BLOCK = re.compile(re.escape(OPEN) + r".*?" + re.escape(CLOSE), re.S)

# La page cible, le formulaire et les mentions légales n'ont rien à y gagner.
# portage / peinture / marquage-au-sol sont de vraies pages Elementor
# (_elementor_edit_mode = builder) : leur rendu vient de _elementor_data, pas de
# post_content. Y écrire ne produirait que du balisage mort.
EXCLUDE = {"choisir-entreprise-nettoyage", "contact", "mention-legales", "sitemap.html",
           "portage", "peinture", "marquage-au-sol"}

ANCHORS = ["<!-- ============ CLIENTS LOGOS", '<div class="art-body"']

BAND = f"""{OPEN}
<div class="spn-band">
<style>
.spn-band{{--b-o:#d8431f;--b-os:#fff1ea;--b-ink:#16181d;--b-ink2:#41454f;--b-line:#e9e4dd;--b-cream:#faf8f5;
  font-family:'Plus Jakarta Sans',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  max-width:1120px;margin:34px auto;padding:0 24px;box-sizing:border-box}}
.spn-band *{{box-sizing:border-box}}
.spn-band .b-in{{display:grid;grid-template-columns:168px 1fr auto;gap:22px;align-items:center;
  background:linear-gradient(115deg,var(--b-os),var(--b-cream) 58%,#fff);
  border:1px solid var(--b-line);border-left:4px solid var(--b-o);border-radius:18px;padding:20px 24px}}
.spn-band .b-img{{width:168px;height:112px;border-radius:12px;overflow:hidden;background:var(--b-cream);flex:none}}
.spn-band .b-img img{{width:100%;height:100%;object-fit:cover;display:block}}
.spn-band .b-eye{{display:inline-block;font-size:.68rem;font-weight:800;letter-spacing:.09em;
  text-transform:uppercase;color:var(--b-o);margin-bottom:7px}}
.spn-band .b-t{{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.22;
  color:var(--b-ink);margin:0 0 6px}}
.spn-band .b-p{{font-size:.92rem;line-height:1.5;color:var(--b-ink2);margin:0}}
.spn-band .b-go{{display:inline-flex;align-items:center;gap:9px;background:var(--b-o);color:#fff;
  font-weight:700;font-size:.94rem;text-decoration:none;padding:14px 28px;border-radius:999px;white-space:nowrap}}
.spn-band .b-go:hover{{background:#ed5d37;color:#fff}}
@media(max-width:860px){{
  .spn-band .b-in{{grid-template-columns:120px 1fr;gap:16px;padding:18px}}
  .spn-band .b-img{{width:120px;height:96px}}
  .spn-band .b-go{{grid-column:1/-1;justify-content:center}}
}}
@media(max-width:520px){{
  .spn-band{{padding:0 16px;margin:26px auto}}
  .spn-band .b-in{{grid-template-columns:1fr}}
  .spn-band .b-img{{width:100%;height:150px}}
}}
</style>
  <div class="b-in">
    <div class="b-img">
      <img src="{IMG}" alt="" width="1500" height="1000" loading="lazy" decoding="async">
    </div>
    <div>
      <span class="b-eye">Guide d'achat</span>
      <p class="b-t">Comment choisir son entreprise de nettoyage</p>
      <p class="b-p">Les 10 points &agrave; v&eacute;rifier avant de signer, du temps d'intervention au devis
        jusqu'&agrave; la conformit&eacute; sociale &mdash; avec une grille de comparaison &agrave; remplir.</p>
    </div>
    <a class="b-go" href="{TARGET}">Lire le guide</a>
  </div>
</div>
{CLOSE}""".strip()


def redirected_slugs():
    """Les slugs servis en 301 par spn-redirects : inutile d'y poser un bandeau."""
    src = open(os.path.join(os.path.dirname(__file__), "..", "..",
                            "wp-plugins", "spn-redirects", "spn-redirects.php"),
               encoding="utf-8").read()
    return set(re.findall(r"'/([^']+)/'\s*=>", src))


def auth_header():
    env = {}
    for line in open(os.path.join(os.path.dirname(__file__), "..", "..", ".env"), encoding="utf-8"):
        m = re.match(r'\s*([A-Z_]+)\s*=\s*"?([^"\n]*)"?', line)
        if m:
            env[m.group(1)] = m.group(2)
    tok = base64.b64encode(f"{env['WP_USER']}:{env['WP_APP_PASSWORD']}".encode()).decode()
    return "Basic " + tok


def call(url, auth, data=None, tries=4):
    """Le proxy coupe parfois en cours d'échange : on réessaie."""
    for i in range(tries):
        req = urllib.request.Request(
            url, data=data,
            headers={"Authorization": auth, "User-Agent": "Mozilla/5.0 Chrome/120.0",
                     **({"Content-Type": "application/json"} if data else {})},
            method="POST" if data else "GET")
        try:
            return json.load(urllib.request.urlopen(req, timeout=180))
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"{e.code} {e.read()[:300]!r}")
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 ** (i + 1))


def place(content, remove=False):
    """Retourne (nouveau_contenu, raison) ou (None, raison) s'il n'y a rien à faire."""
    if BLOCK.search(content):
        if remove:
            return BLOCK.sub("", content).replace("\n\n\n", "\n\n"), "retiré"
        new = BLOCK.sub(lambda _: BAND, content)
        return (None, "inchangé") if new == content else (new, "remplacé")
    if remove:
        return None, "absent"
    for a in ANCHORS:
        i = content.find(a)
        if i != -1:
            return content[:i] + BAND + "\n" + content[i:], "posé/" + ("logos" if "LOGOS" in a else "article")
    return content + "\n" + BAND, "posé/fin"


def main():
    apply_ = "--apply" in sys.argv
    remove = "--remove" in sys.argv
    auth = auth_header()
    skip = redirected_slugs() | EXCLUDE

    pages = call(f"{API}/pages?per_page=100&status=publish&context=edit"
                 "&_fields=id,slug,content", auth)
    todo = [p for p in pages if p["slug"] not in skip]
    print(f"{len(pages)} pages publiées · {len(pages)-len(todo)} écartées (301 ou exclues) "
          f"· {len(todo)} candidates\n")

    stats, errs = {}, []
    for p in todo:
        new, why = place(p["content"]["raw"], remove)
        stats[why] = stats.get(why, 0) + 1
        if new is None:
            continue
        if apply_:
            try:
                call(f"{API}/pages/{p['id']}", auth,
                     json.dumps({"content": new}, ensure_ascii=False).encode())
            except Exception as e:
                errs.append((p["slug"], str(e)[:120]))
                print(f"  ÉCHEC {p['slug']}: {e}")
                continue
        print(f"  {'' if apply_ else '[simulation] '}{why:16} {p['slug']}")

    print("\n" + " · ".join(f"{k} : {v}" for k, v in sorted(stats.items())))
    if errs:
        print(f"\n{len(errs)} échec(s) : " + ", ".join(s for s, _ in errs))
    if not apply_:
        print("\nSimulation. Relancer avec --apply pour écrire.")


if __name__ == "__main__":
    main()
