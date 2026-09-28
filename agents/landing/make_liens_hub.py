#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose les 16 liens entrants in-body vers le hub /choisir-entreprise-nettoyage/.

Le bandeau sitewide ne vaut rien en maillage : une ancre unique répétée sur
83 pages, tout en bas de l'échelle du surfeur raisonnable. Ce sont ces 16 liens
contextuels qui portent le hub.

Règles appliquées (CLAUDE.md §4) :
  - une phrase complète, dans le premier tiers du texte de sa section ;
  - jamais en « lire aussi », jamais dans une carte, jamais après le module visuel ;
  - 16 ancres distinctes, une par source, aucune répétition à l'échelle du site ;
  - jamais dans le bloc « réponse en une phrase » : il reste sans lien.

    python3 agents/landing/make_liens_hub.py            # simulation
    python3 agents/landing/make_liens_hub.py --apply
"""
import json, os, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import make_zone as mz

TARGET = "https://spn-net.fr/choisir-entreprise-nettoyage/"
MARK = "spn-lien-hub"

# slug -> (ancre, phrase gabarit avec {a}, emplacement)
#   emplacement "local"  : 1er <p> de la prose du bloc expertise (gabarit landing)
#   emplacement "art"    : 1er <p> du corps d'article, apres le bloc reponse
#   emplacement "head:X" : le <p> du chapeau de la section nommee X
LIENS = {
 # --- les 8 pages secteur -------------------------------------------------
 "tertiaire": ("choisir son entreprise de nettoyage",
   "Avant de comparer deux devis, notre guide en dix points pour {a} reprend les critères qui pèsent vraiment sur un contrat de bureaux.", "local"),
 "sante-et-medical": ("comment choisir une entreprise de nettoyage",
   "Un site de soins ne se compare pas comme des bureaux : notre guide explique {a} sur des critères de protocole et de traçabilité.", "local"),
 "commerce-et-retail": ("choisir une entreprise de nettoyage",
   "Pour une surface de vente, {a} revient à vérifier qu'elle sait intervenir hors horaires d'ouverture sans jamais gêner la clientèle.", "local"),
 "copropriete-et-habitat": ("bien choisir son entreprise de nettoyage",
   "Un syndic engage la copropriété sur plusieurs exercices : {a} évite d'avoir à rouvrir le sujet en assemblée générale.", "local"),
 "logistique-et-industrie": ("notre guide pour choisir une entreprise de nettoyage",
   "Sur un entrepôt, la sécurité prime sur le prix au m² : {a} détaille les certifications à exiger avant de signer.", "local"),
 "hotellerie-et-restauration": ("les critères pour choisir une entreprise de nettoyage",
   "En hôtellerie comme en restauration, {a} tiennent autant à l'hygiène réglementaire qu'à la discrétion des équipes.", "local"),
 "enseignement-et-petite-enfance": ("notre méthode pour choisir son entreprise de nettoyage",
   "Face à un public d'enfants, {a} insiste sur les produits employés et sur la stabilité des agents affectés au site.", "local"),
 "loisirs-culture-et-evenementiel": ("les dix points à vérifier avant de signer",
   "Un équipement recevant du public impose des passages courts et très encadrés : voici {a} un contrat d'entretien.", "local"),
 # --- le lien montant des 6 articles + l'annexe 7 --------------------------
 "prix-nettoyage-bureaux-paris": ("le guide pour choisir son entreprise de nettoyage",
   "Un prix ne se lit jamais seul : {a} replace ces fourchettes parmi les neuf autres critères d'un contrat.", "art"),
 "travail-dissimule-entreprise-nettoyage": ("choisir une entreprise de nettoyage en règle",
   "La vigilance ne s'arrête pas aux documents : {a} suppose aussi de regarder ses certifications et son taux de rotation.", "art"),
 "certifications-entreprise-nettoyage": ("notre guide d'achat pour choisir une entreprise de nettoyage",
   "Une certification ne décide de rien à elle seule : {a} la remet à sa place parmi dix critères.", "art"),
 "nettoyage-bureaux-confidentialite-securite": ("la grille de comparaison des prestataires",
   "La confidentialité se vérifie au contrat, pas à l'oral : {a} en fait un critère à cocher, au même titre que le prix.", "art"),
 "qualite-nettoyage-baisse-apres-3-mois": ("choisir la bonne entreprise de nettoyage",
   "La baisse du troisième mois se joue en amont : {a}, c'est vérifier son dispositif de contrôle qualité avant de signer.", "art"),
 "annexe-7-changer-entreprise-nettoyage": ("les dix points qui séparent deux offres d'entretien",
   "L'Annexe 7 règle la reprise des agents, pas le choix du repreneur : {a} sont traités à part.", "art"),
 # --- les deux pages a gabarit particulier ---------------------------------
 "changer-de-prestataire-nettoyage": ("comment choisir votre nouvelle entreprise de nettoyage",
   "Avant même de résilier, {a} mérite d'être tranché : c'est ce qui évite de reconduire le même contrat ailleurs.", "head:INFOS"),
 "blog": ("Comment choisir son entreprise de nettoyage : le guide en 10 points",
   "Parmi elles, {a} rassemble les critères que les autres traitent séparément.", "head:INDEX ARTICLES"),
}

WRAP_OPEN, WRAP_CLOSE = "<!-- wp:html -->", "<!-- /wp:html -->"


def phrase(slug):
    anchor, tpl, _ = LIENS[slug]
    a = f'<a href="{TARGET}" data-{MARK}>{anchor}</a>'
    return " " + tpl.format(a=a)


def target_paragraph(html, where):
    """Retourne (debut, fin) du <p> a enrichir, ou None."""
    if where == "local":
        m = re.search(r'<div class="sec local">[\s\S]*?<div class="grid">\s*'
                      r'<div class="reveal">\s*<p>([\s\S]*?)</p>', html)
        return m.span(1) if m else None
    if where == "art":
        i = html.find('<article class="art-main">')
        if i == -1:
            return None
        # le bloc « reponse en une phrase » ne porte aucun lien : on passe apres
        m = re.compile(r'<div class="nb-answer[^"]*"[^>]*>[\s\S]*?</div>').search(html, i)
        if m:
            i = m.end()
        m = re.compile(r'<p>([\s\S]{60,}?)</p>').search(html, i)
        return m.span(1) if m else None
    if where.startswith("head:"):
        sec = where[5:]
        i = html.find(f"============ {sec} ")
        if i == -1:
            return None
        m = re.compile(r'<div class="sec-head[^"]*"[^>]*>[\s\S]*?<p>([\s\S]*?)</p>').search(html, i)
        return m.span(1) if m else None
    return None


def place(html, slug):
    if f"data-{MARK}" in html:
        return None, "déjà posé"
    span = target_paragraph(html, LIENS[slug][2])
    if not span:
        return None, "PARAGRAPHE INTROUVABLE"
    s, e = span
    return html[:e] + phrase(slug) + html[e:], "posé"


def main():
    apply_ = "--apply" in sys.argv
    print(f"{'source':44} {'etat':22} ancre")
    ok = ko = 0
    for slug in LIENS:
        r = mz.requests.get(mz.API, params={"slug": slug, "context": "edit",
                                            "_fields": "id,content"},
                            auth=mz.AUTH, timeout=90).json()
        if not r:
            print(f"{slug:44} PAGE INTROUVABLE"); ko += 1; continue
        pid, raw = r[0]["id"], r[0]["content"]["raw"]
        new, why = place(raw, slug)
        anchor = LIENS[slug][0]
        print(f"{'' if apply_ else '[simu] '}{slug:44} {why:22} « {anchor} »")
        if new is None:
            ko += why == "PARAGRAPHE INTROUVABLE"
            continue
        ok += 1
        if apply_:
            body = new
            if WRAP_OPEN not in body:          # ne jamais poster sans le wrapper
                body = f"{WRAP_OPEN}\n{body}\n{WRAP_CLOSE}"
            resp = mz.requests.post(f"{mz.API}/{pid}", auth=mz.AUTH, timeout=180,
                                    json={"content": body})
            if resp.status_code != 200:
                print(f"    ECHEC {resp.status_code} {resp.text[:160]}"); ko += 1; ok -= 1
    print(f"\n{ok} lien(s) à poser · {ko} problème(s)")
    if not apply_:
        print("Simulation. Relancer avec --apply.")


if __name__ == "__main__":
    main()
