#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Infographies HTML du gabarit article — copywriting visuel.

Une page SPN NET ne se juge pas au nombre de mots : elle se juge a ce qu'on
comprend sans lire. Regle de production : UNE infographie entre chaque H2,
plus les modules d'attention NavBoost. Le texte vient apres, pas avant.

Blocs disponibles :
  duo(titre, gauche, droite)   comparaison deux colonnes, la droite gagnante
  barre(titre, parts, note)    barre empilee avec legende
  etapes(titre, steps)         frise horizontale numerotee
  cartes(titre, items)         grille de 4 cartes chiffrees
  jauge(titre, lignes, note)   barres horizontales comparees
  cta(texte, lien, libelle)    CTA intermediaire
"""

CSS = """<style>
.spn-art{--line:#e9e4dd;--r:16px;--shadow-sm:0 1px 2px rgba(15,23,42,.05);
  --grey:#7a7f8c;--ink:#16181d;--ink-2:#41454f;--orange:#ed5d37;--orange-deep:#d8431f;
  --orange-soft:#fff1ea;--cream:#faf8f5}
/* ---------- infographies ---------- */
.spn-art .vz{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:24px 26px;margin:26px 0;box-shadow:var(--shadow-sm)}
.spn-art .vz .vz-t{font-size:.72rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--grey);margin-bottom:16px}
.spn-art .vz-2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.spn-art .vz-col{border:1px solid var(--line);border-radius:14px;padding:18px 18px 14px}
.spn-art .vz-col.win{border-color:rgba(216,67,31,.35);background:var(--orange-soft)}
.spn-art .vz-col h4{font-family:'Fraunces',serif;font-weight:600;font-size:1.04rem;margin:0 0 10px}
.spn-art .vz-col ul{list-style:none;margin:0;padding:0}
.spn-art .vz-col li{font-size:.88rem;color:var(--ink-2);padding:5px 0 5px 20px;position:relative}
.spn-art .vz-col li:before{content:"—";position:absolute;left:0;color:var(--grey)}
.spn-art .vz-col.win li:before{content:"✓";color:var(--orange-deep);font-weight:800}
/* barre empilee */
.spn-art .vz-bar{display:flex;height:42px;border-radius:10px;overflow:hidden;margin-bottom:10px}
.spn-art .vz-bar span{display:flex;align-items:center;justify-content:center;color:#fff;font-size:.8rem;font-weight:800}
.spn-art .vz-leg{display:flex;flex-wrap:wrap;gap:14px;font-size:.82rem;color:var(--ink-2)}
.spn-art .vz-leg i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px}
/* timeline */
.spn-art .vz-tl{display:flex;gap:0;flex-wrap:wrap}
.spn-art .vz-step{flex:1;min-width:130px;position:relative;padding:0 12px}
.spn-art .vz-step:before{content:"";position:absolute;top:15px;left:0;right:0;height:2px;background:var(--line)}
.spn-art .vz-step:first-child:before{left:50%}.spn-art .vz-step:last-child:before{right:50%}
.spn-art .vz-dot{position:relative;width:32px;height:32px;border-radius:50%;background:var(--orange-soft);color:var(--orange-deep);border:2px solid #fff;box-shadow:0 0 0 2px var(--orange-soft);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.82rem;margin:0 auto 12px}
.spn-art .vz-step b{display:block;text-align:center;font-size:.9rem;margin-bottom:3px}
.spn-art .vz-step span{display:block;text-align:center;font-size:.8rem;color:var(--grey);line-height:1.45}
/* niveaux empiles */
.spn-art .vz-lv{display:grid;gap:9px}
.spn-art .vz-lv div{border-radius:11px;padding:13px 16px;font-size:.9rem;display:flex;gap:12px;align-items:baseline}
.spn-art .vz-lv b{font-family:'Fraunces',serif;font-size:.96rem;min-width:92px;flex:0 0 auto}
.spn-art .vz-lv .l1{background:#16181D;color:#fff}.spn-art .vz-lv .l1 b{color:#fff}
.spn-art .vz-lv .l2{background:var(--orange-soft);color:var(--ink-2)}.spn-art .vz-lv .l2 b{color:var(--orange-deep)}
.spn-art .vz-lv .l3{background:var(--cream);color:var(--ink-2)}.spn-art .vz-lv .l3 b{color:var(--grey)}
/* zones d'acces */
.spn-art .vz-zn{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.spn-art .vz-zn div{border-radius:12px;padding:16px;text-align:center;border:1px solid var(--line)}
.spn-art .vz-zn .z-ok{background:#eaf6ec;border-color:#b7dcc0}
.spn-art .vz-zn .z-md{background:var(--orange-soft);border-color:rgba(216,67,31,.3)}
.spn-art .vz-zn .z-no{background:var(--cream)}
.spn-art .vz-zn b{display:block;font-size:.94rem;margin-bottom:5px}
.spn-art .vz-zn span{font-size:.8rem;color:var(--grey);line-height:1.45}
/* galerie 4 photos */
.spn-art .vz-g4{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.spn-art .vz-g4 figure{margin:0;border-radius:12px;overflow:hidden;border:1px solid var(--line);background:var(--cream)}
.spn-art .vz-g4 img{width:100%;height:100%;object-fit:cover;display:block;aspect-ratio:4/3}
.spn-art .vz-g4 figcaption{font-size:.78rem;font-weight:700;color:var(--ink-2);padding:8px 10px;text-align:center}
/* photo pleine largeur */
.spn-art .vz-photo{margin:0;border-radius:16px;overflow:hidden;border:1px solid var(--line)}
.spn-art .vz-photo img{width:100%;display:block;aspect-ratio:21/9;object-fit:cover}
.spn-art .vz-photo figcaption{font-size:.82rem;color:var(--grey);padding:10px 14px;background:#fff}
/* CTA intermediaire */
.spn-art .midcta{display:flex;align-items:center;gap:18px;flex-wrap:wrap;background:linear-gradient(120deg,var(--orange-soft),#fff);border:1px solid rgba(216,67,31,.28);border-radius:var(--r);padding:20px 24px;margin:28px 0}
.spn-art .midcta p{margin:0;flex:1;min-width:220px;font-size:.96rem;font-weight:600;color:var(--ink)}
.spn-art .midcta a{display:inline-flex;align-items:center;gap:8px;background:var(--orange-deep);color:#fff;font-weight:700;font-size:.92rem;text-decoration:none;padding:12px 24px;border-radius:999px;white-space:nowrap}
.spn-art .midcta a:hover{background:var(--orange)}
/* CTA final */
.spn-art .endcta{background:#16181D;color:#fff;border-radius:var(--r);padding:34px 34px 30px;margin:32px 0 0}
.spn-art .endcta h3{font-family:'Fraunces',serif;font-weight:600;font-size:1.5rem;color:#fff;margin:0 0 10px}
.spn-art .endcta p{color:rgba(255,255,255,.82);font-size:.98rem;margin:0 0 20px;max-width:56ch}
.spn-art .endcta .acts{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.spn-art .endcta .b1{background:var(--orange);color:#fff;font-weight:800;text-decoration:none;padding:14px 30px;border-radius:999px}
.spn-art .endcta .b2{color:#fff;font-weight:700;text-decoration:none;padding:14px 22px;border-radius:999px;border:1px solid rgba(255,255,255,.3)}
.spn-art .endcta .badges{margin-top:18px;font-size:.8rem;color:rgba(255,255,255,.6)}
@media(max-width:820px){.spn-art .vz-2,.spn-art .vz-zn{grid-template-columns:1fr}.spn-art .vz-g4{grid-template-columns:1fr 1fr}}
@media print{.spn-art .art-side,.spn-art .art-hero,.spn-art .cmp-act{display:none!important}}
</style>"""


def _t(x):
    return '<div class="vz-t">%s</div>' % x


def duo(titre, g_titre, g_items, d_titre, d_items):
    gi = "".join("<li>%s</li>" % i for i in g_items)
    di = "".join("<li>%s</li>" % i for i in d_items)
    return ('<div class="vz rv">' + _t(titre) + '<div class="vz-2">'
            '<div class="vz-col"><h4>%s</h4><ul>%s</ul></div>'
            '<div class="vz-col win"><h4>%s</h4><ul>%s</ul></div>'
            '</div></div>' % (g_titre, gi, d_titre, di))


def barre(titre, parts, note=""):
    """parts : liste de (libelle, pourcentage, couleur, legende)"""
    bars = "".join('<span style="width:%d%%;background:%s">%s %d&nbsp;%%</span>' % (p, c, l, p)
                   for l, p, c, _ in parts)
    leg = "".join('<span><i style="background:%s"></i>%s</span>' % (c, lg) for _, _, c, lg in parts)
    n = ('<p style="font-size:.82rem;color:var(--grey);margin:14px 0 0">%s</p>' % note) if note else ""
    return ('<div class="vz rv">' + _t(titre) +
            '<div class="vz-bar">%s</div><div class="vz-leg">%s</div>%s</div>' % (bars, leg, n))


def etapes(titre, steps):
    """steps : liste de (numero, titre, detail)"""
    s = "".join('<div class="vz-step"><div class="vz-dot">%s</div>'
                '<div class="vz-h">%s</div><div class="vz-d">%s</div></div>' % (n, t, d)
                for n, t, d in steps)
    return '<div class="vz rv">' + _t(titre) + '<div class="vz-tl">%s</div></div>' % s


def cartes(titre, items):
    """items : liste de (chiffre, libelle, detail)"""
    c = "".join('<div class="vz-c"><b>%s</b><span>%s</span><small>%s</small></div>' % (a, b, d)
                for a, b, d in items)
    return '<div class="vz rv">' + _t(titre) + '<div class="vz-g4">%s</div></div>' % c


def jauge(titre, lignes, note=""):
    """lignes : liste de (libelle, pourcentage, valeur affichee, couleur)"""
    rows = "".join(
        '<div class="vz-j"><span class="vz-jl">%s</span>'
        '<span class="vz-jb"><i style="width:%d%%;background:%s"></i></span>'
        '<span class="vz-jv">%s</span></div>' % (l, p, c, v) for l, p, v, c in lignes)
    n = ('<p style="font-size:.82rem;color:var(--grey);margin:14px 0 0">%s</p>' % note) if note else ""
    return '<div class="vz rv">' + _t(titre) + rows + n + '</div>'


def cta(texte, lien, libelle):
    return ('<div class="midcta rv"><p>%s</p><a href="%s">%s &#8594;</a></div>'
            % (texte, lien, libelle))


EXTRA = """<style>
.spn-art .vz-g4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.spn-art .vz-c{border:1px solid var(--line);border-radius:14px;padding:16px 14px;background:var(--cream)}
.spn-art .vz-c b{display:block;font-family:'Fraunces',serif;font-size:1.5rem;font-weight:600;color:var(--orange-deep);line-height:1.1}
.spn-art .vz-c span{display:block;font-size:.84rem;font-weight:700;color:var(--ink);margin:6px 0 4px}
.spn-art .vz-c small{display:block;font-size:.76rem;color:var(--grey);line-height:1.4}
.spn-art .vz-j{display:flex;align-items:center;gap:12px;margin:9px 0}
.spn-art .vz-jl{flex:0 0 32%;font-size:.86rem;color:var(--ink-2)}
.spn-art .vz-jb{flex:1;height:14px;background:var(--cream);border-radius:7px;overflow:hidden}
.spn-art .vz-jb i{display:block;height:100%;border-radius:7px}
.spn-art .vz-jv{flex:0 0 124px;text-align:right;font-size:.86rem;font-weight:800;color:var(--ink)}
.spn-art .vz-dot{width:32px;height:32px;border-radius:50%;background:var(--orange-deep);color:#fff;
  display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.9rem;margin:0 auto 10px;position:relative;z-index:1}
.spn-art .vz-h{font-weight:700;font-size:.88rem;text-align:center;margin-bottom:4px;color:var(--ink)}
.spn-art .vz-d{font-size:.79rem;color:var(--grey);text-align:center;line-height:1.45}
@media(max-width:820px){.spn-art .vz-g4{grid-template-columns:1fr 1fr}.spn-art .vz-jl{flex:0 0 40%}.spn-art .vz-jv{flex:0 0 92px;font-size:.78rem}}
</style>"""
