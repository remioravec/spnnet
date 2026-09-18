#!/usr/bin/env python3
"""Redesign des pages menu 'Nos Engagements' (/a-propos/) et 'Blog' (/blog/),
en indexable, via le mécanisme réversible.

Usage : python3 agents/landing/make_special.py apropos blog
        python3 agents/landing/make_special.py --restore a-propos blog
"""
from __future__ import annotations

import sys
import pathlib

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from make_paris2 import CSS, PROMISE, PULL, TEAM, TEAMCUE, HEADFIX, _CK  # noqa: E402
import make_zone as mz  # noqa: E402

EXTRA_CSS = """
.spn-lp .engage .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.spn-lp .engage .grid.g4-fix{grid-template-columns:repeat(4,1fr)}
.spn-lp .eng p a{color:var(--orange-deep);font-weight:700}
@media(max-width:900px){.spn-lp .engage .grid.g4-fix{grid-template-columns:1fr 1fr}}
.spn-lp .eng{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:26px 24px;transition:transform .2s,box-shadow .2s}
.spn-lp .eng:hover{transform:translateY(-4px);box-shadow:var(--shadow-sm)}
.spn-lp .eng .ic{width:52px;height:52px;border-radius:14px;background:var(--orange-soft);display:flex;align-items:center;justify-content:center;color:var(--orange-deep);margin-bottom:15px}
.spn-lp .eng h3{font-size:1.18rem;margin-bottom:8px}
.spn-lp .eng p{font-size:.93rem;color:var(--grey)}
.spn-lp .posts .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.spn-lp .post{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px;color:var(--ink);transition:transform .2s,box-shadow .2s}
.spn-lp .post:hover{transform:translateY(-4px);box-shadow:var(--shadow-sm);text-decoration:none}
.spn-lp .post .tag{align-self:flex-start;font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--orange-deep);background:var(--orange-soft);padding:4px 11px;border-radius:999px;margin-bottom:12px}
.spn-lp .post h3{font-size:1.16rem;margin-bottom:8px;line-height:1.25}
.spn-lp .post p{font-size:.9rem;color:var(--grey);margin-bottom:14px;flex:1}
.spn-lp .post .go{color:var(--orange-deep);font-weight:700;font-size:.9rem}
@media(max-width:820px){.spn-lp .engage .grid,.spn-lp .posts .grid{grid-template-columns:1fr}}
"""


def _ic(path):
    return (f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{path}</svg>')


ENGAGEMENTS = [
    (_ic('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'), "Sécurité certifiée ISO 45001",
     "Notre système de management santé-sécurité au travail est certifié ISO 45001 par DEKRA. La sécurité de nos agents et de vos sites est une priorité."),
    (_ic('<circle cx="12" cy="8" r="6"/><path d="M9 22l3-3 3 3"/>'), "Médaille d'argent EcoVadis 2025",
     "Notre démarche RSE est reconnue par la médaille d'argent EcoVadis, qui place SPN NET dans le top 15 % des entreprises évaluées."),
    (_ic('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/>'),
     "Des équipes formées & fidélisées", "Nous investissons dans la formation et la stabilité de nos agents — souvent les mêmes sur vos sites, semaine après semaine."),
    (_ic('<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/>'), "Qualité suivie dans le temps",
     "Un interlocuteur dédié, des contrôles qualité réguliers et une capacité à ajuster la prestation : la propreté reste constante, sans que vous ayez à relancer."),
    (_ic('<path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7z"/><circle cx="12" cy="9" r="2.5"/>'),
     "Une entreprise de proximité", "Basés à Bagneux (92), nous sommes réactifs sur Paris et toute l'Île-de-France — le dirigeant se déplace lui-même pour les premiers états des lieux."),
    (_ic('<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/>'),
     "Une démarche responsable", "Produits et protocoles adaptés à chaque environnement, dans une logique d'amélioration continue au service de la santé et du bien-être."),
]

POSTS = [
    ("meilleure-entreprise-nettoyage-tertiaire-paris", "Bureaux", "Nettoyage tertiaire à Paris", "Bien choisir son prestataire pour l'entretien de bureaux et de locaux tertiaires."),
    ("meilleure-entreprise-nettoyage-commerce-retail-paris", "Commerce", "Nettoyage de commerces & retail", "Vitrines, surfaces de vente, sanitaires : garder un point de vente impeccable."),
    ("meilleure-entreprise-nettoyage-sante-medical-paris", "Santé", "Nettoyage médical & bionettoyage", "Protocoles d'hygiène pour cabinets, laboratoires et établissements de santé."),
    ("meilleure-entreprise-nettoyage-logistique-industrie-paris", "Logistique", "Nettoyage logistique & industrie", "Entrepôts et sites industriels : moyens mécanisés et sécurité."),
    ("meilleure-entreprise-nettoyage-hotellerie-restauration-paris", "Hôtellerie", "Nettoyage d'hôtels & restaurants", "Parties communes, chambres, cuisines : protéger sa réputation."),
    ("meilleure-entreprise-nettoyage-copropriete-habitat-paris", "Copropriété", "Nettoyage de copropriétés", "Parties communes, locaux poubelles, sorties de bacs pour les immeubles."),
    ("meilleure-entreprise-nettoyage-loisirs-culture-evenementiel-paris", "Culture", "Nettoyage culturel & événementiel", "Musées, salles, sites recevant du public : avant et après le public."),
    ("meilleure-entreprise-nettoyage-enseignement-petite-enfance-paris", "Enseignement", "Nettoyage d'écoles & crèches", "Hygiène renforcée pour les établissements scolaires et la petite enfance."),
    ("meilleure-entreprise-nettoyage-fin-de-chantier-paris", "Remise en état", "Nettoyage de fin de chantier", "Livrer des locaux nets après travaux ou avant emménagement."),
    ("meilleure-entreprise-nettoyage-apres-sinistre-paris", "Remise en état", "Nettoyage après sinistre", "Remise en état après dégât des eaux, incendie ou autre sinistre."),
    ("meilleure-entreprise-nettoyage-parkings-paris", "Parkings", "Nettoyage de parkings", "Sols, murs et signalétique des parkings de copropriétés et d'entreprises."),
    ("meilleure-entreprise-nettoyage-vitrines-paris", "Vitrerie", "Nettoyage de vitrines", "Vitrines et surfaces vitrées : capter l'attention et soigner l'image."),
]


def engage_section():
    cards = ""
    for ic, h, p in ENGAGEMENTS:
        cards += f'    <div class="eng reveal"><div class="ic">{ic}</div><h3>{h}</h3><p>{p}</p></div>\n'
    return ('\n<!-- ============ ENGAGEMENTS ============ -->\n'
            '<div class="sec engage"><div class="wrap">\n'
            '  <div class="sec-head reveal"><span class="eyebrow c">Ce qui nous engage</span>'
            '<h2>Des certifications, pas des promesses</h2>'
            '<p>Notre exigence est vérifiée par des tiers indépendants et incarnée par nos équipes.</p></div>\n'
            '  <div class="grid">\n' + cards + '  </div>\n</div></div>\n\n<!-- ============ WHY US ============ -->')


def posts_section():
    cards = ""
    for slug, tag, title, desc in POSTS:
        cards += (f'    <a class="post reveal" href="https://spn-net.fr/{slug}/"><span class="tag">{tag}</span>'
                  f'<h3>{title}</h3><p>{desc}</p><span class="go">Lire le guide →</span></a>\n')
    return ('\n<!-- ============ INDEX ARTICLES ============ -->\n'
            '<div class="sec posts"><div class="wrap">\n'
            '  <div class="sec-head reveal"><span class="eyebrow c">Nos guides</span>'
            '<h2>Guides & conseils propreté</h2>'
            '<p>Nos ressources pour bien choisir et organiser le nettoyage de vos locaux.</p></div>\n'
            '  <div class="grid">\n' + cards + '  </div>\n</div></div>\n\n<!-- ============ WHY US ============ -->')


def contact_section():
    cards = [
        (_ic('<path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7z"/><circle cx="12" cy="9" r="2.5"/>'),
         "Adresse", "52 Avenue de Bourg-la-Reine<br>92220 Bagneux (92)"),
        (_ic('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.1 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.4 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7A2 2 0 0 1 22 16.9z"/>'),
         "Téléphone", '<a href="tel:+33149462240">01 49 46 22 40</a><br>Du lundi au vendredi'),
        (_ic('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>'),
         "E-mail", '<a href="mailto:contact@spn-net.fr">contact@spn-net.fr</a>'),
        (_ic('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
         "Réactivité", "Devis gratuit sous 24h<br>Interventions soir &amp; matin"),
    ]
    body = ""
    for ic, h, v in cards:
        body += f'    <div class="eng reveal"><div class="ic">{ic}</div><h3>{h}</h3><p>{v}</p></div>\n'
    return ('\n<!-- ============ COORDONNÉES ============ -->\n'
            '<div class="sec engage"><div class="wrap">\n'
            '  <div class="sec-head reveal"><span class="eyebrow c">Nous joindre</span>'
            '<h2>Une équipe joignable, une réponse rapide</h2>'
            '<p>Basés à Bagneux (92), nous intervenons à Paris et dans toute l\'Île-de-France. '
            'Écrivez-nous via le formulaire ou appelez-nous directement.</p></div>\n'
            '  <div class="grid g4-fix">\n' + body + '  </div>\n</div></div>\n\n<!-- ============ WHY US ============ -->')


CFG = {
    "contact": dict(
        title="Contact — Devis nettoyage à Paris & Île-de-France | SPN NET",
        desc="Contactez SPN NET, entreprise de propreté à Bagneux (92) : devis gratuit sous 24h pour le nettoyage de vos locaux à Paris et en Île-de-France. 01 49 46 22 40.",
        eyebrow="Contact", h1="Parlons de <em>vos locaux</em>",
        lead="Décrivez-nous votre besoin : nous revenons vers vous sous 24h avec un devis gratuit et sans engagement. Vous pouvez aussi nous appeler directement.",
        section=contact_section,
        faq=[("Sous quel délai recevrai-je une réponse ?",
              "Nous vous recontactons sous 24h ouvrées après réception de votre demande, avec un devis gratuit et sans engagement."),
             ("Quelles informations préparer pour un devis ?",
              "Le type de locaux, la surface approximative, la fréquence souhaitée et vos contraintes d'accès ou d'horaires suffisent pour un premier chiffrage."),
             ("Intervenez-vous dans ma zone ?",
              "Nous couvrons Paris (les 20 arrondissements) et toute l'Île-de-France (77, 78, 91, 92, 93, 94, 95). Notre base est à Bagneux (92)."),
             ("Le devis engage-t-il à quelque chose ?",
              "Non : le devis est gratuit et sans engagement. Les conditions du contrat sont définies avec vous avant toute intervention.")],
        bc="Contact",
    ),
    "a-propos": dict(
        title="Nos engagements : ISO 45001, EcoVadis, RSE | SPN NET",
        desc="Les engagements de SPN NET : certification ISO 45001, médaille d'argent EcoVadis, équipes formées, démarche responsable. 30 ans au service des professionnels d'Île-de-France.",
        eyebrow="Nos engagements", h1="Nos <em>engagements</em>, votre tranquillité",
        lead="Depuis 30 ans, SPN NET met la même énergie au service de ses clients et de ses salariés : qualité certifiée, démarche RSE reconnue, sécurité au travail. Voici ce sur quoi vous pouvez compter.",
        section=engage_section,
        faq=[("SPN NET est-elle une entreprise certifiée ?",
              "Oui : SPN NET est certifiée ISO 45001 (santé-sécurité au travail, par DEKRA) et a obtenu la médaille d'argent EcoVadis 2025, dans le top 15 % des entreprises évaluées."),
             ("Qu'est-ce que la démarche RSE d'EcoVadis change concrètement ?",
              "Elle traduit un engagement vérifié sur l'environnement, le social et l'éthique : produits et protocoles adaptés, attention portée à la sécurité et au bien-être de nos agents."),
             ("Où êtes-vous basés et quelle est votre zone ?",
              "Notre siège est à Bagneux (92). Nous intervenons dans tout Paris et l'Île-de-France, avec une forte réactivité en proche couronne."),
             ("Le devis engage-t-il à quelque chose ?",
              "Non : le devis est gratuit et sans engagement. Les conditions du contrat sont définies avec vous avant toute intervention.")],
        bc="Nos engagements",
    ),
    "blog": dict(
        title="Blog : guides & conseils nettoyage professionnel | SPN NET",
        desc="Les guides SPN NET pour bien choisir et organiser le nettoyage de vos locaux à Paris et en Île-de-France : bureaux, commerces, santé, hôtellerie, copropriétés…",
        eyebrow="Le blog SPN NET", h1="Guides & conseils <em>propreté</em>",
        lead="Nos guides sectoriels pour bien choisir votre prestataire et organiser l'entretien de vos locaux à Paris et en Île-de-France.",
        section=posts_section,
        faq=[("À qui s'adressent ces guides ?",
              "Aux professionnels — dirigeants, office managers, syndics, gestionnaires — qui cherchent à choisir et organiser le nettoyage de leurs locaux."),
             ("Proposez-vous un devis à partir de ces pages ?",
              "Oui, chaque guide renvoie vers nos pages dédiées et un devis gratuit sous 24h, sans engagement."),
             ("Dans quelles zones intervenez-vous ?",
              "Paris (les 20 arrondissements) et toute l'Île-de-France : 77, 78, 91, 92, 93, 94 et 95.")],
        bc="Blog",
    ),
}


def links_section(cfg_key):
    cards = ""
    for slug, label in [("tertiaire", "Bureaux & Tertiaire"), ("sante-et-medical", "Santé & Médical"),
                        ("hotellerie-et-restauration", "Hôtellerie & Restauration"), ("copropriete-et-habitat", "Copropriété & Habitat")]:
        cards += (f'    <a class="card" href="https://spn-net.fr/{slug}/"><b>{label} <span class="ar">→</span></b>'
                  '<small>Notre pôle dédié</small></a>\n')
    cards += ('    <a class="card" href="https://spn-net.fr/paris-8/"><b>Nettoyage Paris 8e <span class="ar">→</span></b><small>Nos pages locales</small></a>\n'
              '    <a class="card" href="https://spn-net.fr/92-hauts-de-seine/"><b>Hauts-de-Seine (92) <span class="ar">→</span></b><small>Notre base</small></a>\n')
    return ('\n<!-- ============ MAILLAGE ============ -->\n'
            '<div class="sec links"><div class="wrap">\n'
            '  <div class="sec-head reveal"><span class="eyebrow c">À explorer</span>'
            '<h2>Nos pôles &amp; zones d\'intervention</h2><p>Découvrez nos expertises par secteur et par zone.</p></div>\n'
            '  <div class="grid reveal">\n' + cards + '  </div>\n</div></div>\n\n<!-- ============ FINAL CTA ============ -->')


def build(cfg):
    h = mz.BASE_HTML
    h = h.replace(mz.NOINDEX_SCRIPT, "", 1)
    a = h.index("<!-- ============ TOP STRIP ============ -->")
    b = h.index("<!-- ============ HERO ============ -->")
    h = h[:a] + h[b:]
    h = h.replace("</style>", CSS + EXTRA_CSS + "</style>", 1)
    h = h.replace(mz.A_EYEBROW, f'<span class="eyebrow">{cfg["eyebrow"]}</span>', 1)
    h = h.replace(mz.A_H1, f'<h1>{cfg["h1"]}</h1>', 1)
    h = h.replace(mz.A_LEAD, f'<p class="lead">{cfg["lead"]}</p>', 1)
    zp = ("<p>Nous intervenons à Paris et dans toute l'Île-de-France, avec des équipes mobiles dans les "
          "20 arrondissements et l'ensemble des départements franciliens.</p>")
    h = h.replace(mz.A_ZONEP, zp, 1)
    h = h.replace("<!-- ============ WHY US ============ -->", PROMISE + cfg["section"](), 1)
    h = h.replace("<!-- ============ AVIS GOOGLE", PULL + "\n<!-- ============ AVIS GOOGLE", 1)
    h = h.replace("<!-- ============ RÉALISATIONS ============ -->", TEAM, 1)
    tr = 'ISO 45001</b></span></div>\n    </div>'
    h = h.replace(tr, 'ISO 45001</b></span></div>\n      ' + TEAMCUE + '\n    </div>', 1)
    h = h.replace("<!-- ============ FINAL CTA ============ -->", links_section(cfg), 1)
    h = h.replace(
        '<span class="eyebrow c">Pourquoi SPN NET</span><h2>Propreté, rigueur et engagement depuis 30 ans</h2><p>Une entreprise à taille humaine, deux priorités : le client et le salarié.</p>',
        '<span class="eyebrow c">Ce que vous y gagnez</span><h2>Moins de tracas, des locaux toujours nickel</h2><p>Une entreprise à taille humaine qui traite vos locaux comme les siens — et vos équipes avec le même soin.</p>'
        '<div class="gains" style="margin-top:18px">'
        '<span>' + _CK + ' Zéro relance à faire</span>'
        '<span>' + _CK + ' Même équipe, chaque semaine</span>'
        '<span>' + _CK + ' Contrôle qualité régulier</span></div>', 1)
    fs = h.index('    <details class="acc"><summary>Quelle est votre zone')
    fe = h.index("</details>", h.index("bien-être et à la sécurité de nos agents")) + len("</details>")
    fhtml = "".join(f'    <details class="acc"><summary>{q}<span class="pl">+</span></summary><div class="body">{a}</div></details>\n'
                    for q, a in cfg["faq"]).rstrip("\n")
    h = h[:fs] + fhtml + h[fe:]
    ls = h.index('{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[')
    le = h.index("]}", ls) + len("]}")
    q = ",".join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
                 % (mz.strip_accents(n).replace('"', "'"), mz.strip_accents(x).replace('"', "'")) for n, x in cfg["faq"])
    h = h[:ls] + '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + q + ']}' + h[le:]
    bc = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList",'
          '"itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":"https://spn-net.fr/"},'
          f'{{"@type":"ListItem","position":2,"name":"{mz.strip_accents(cfg["bc"])}"}}]}}</script>')
    h = h.rstrip()[:-len("</section>")] + bc + HEADFIX + "\n</section>\n"
    return h


def main():
    args = sys.argv[1:]
    if args and args[0] == "--restore":
        for slug in args[1:]:
            print(mz.restore(slug))
        return
    m = {"apropos": "a-propos", "a-propos": "a-propos", "blog": "blog", "contact": "contact"}
    for a in args:
        slug = m.get(a)
        if not slug:
            print(f"  ? {a}"); continue
        cfg = CFG[slug]
        try:
            print(mz.deploy(slug, cfg, builder=build, prefix="special"))
        except Exception as ex:  # noqa: BLE001
            print(f"  ✗ {slug}: {ex}")


if __name__ == "__main__":
    main()
