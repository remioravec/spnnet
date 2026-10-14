#!/usr/bin/env python3
"""Génère les fichiers d'import Google Ads Editor pour SPN NET :
- spn-ads-keywords.csv  : mots-clés par groupe d'annonces (+ URL finale = LP dédiée)
- spn-ads-negatives.csv : mots-clés à exclure (niveau campagne)

Priorisation fondée sur la Search Console (demande non-marque réelle).
Pas de campagne de marque (SPN-NET exclu, cf. négatifs).
"""
from __future__ import annotations

import csv
import pathlib

HERE = pathlib.Path(__file__).parent
CAMP = "Search – Nettoyage Paris IDF"

LP = {
    "culture": "https://spn-net.fr/nettoyage-musee-theatre-evenementiel-paris/",
    "hotel": "https://spn-net.fr/nettoyage-hotel-restaurant-paris/",
    "sante": "https://spn-net.fr/nettoyage-medical-sante-paris/",
    "bureaux": "https://spn-net.fr/devis-nettoyage-bureaux-paris/",
    "local": "https://spn-net.fr/devis-nettoyage-bureaux-paris/",
}

# groupe -> (lp, [(keyword, [match types])])  | "E"=Exact, "P"=Phrase
GROUPS = {
    "Culture & Événementiel": ("culture", [
        ("nettoyage musée", ["E", "P"]),
        ("nettoyage de musée", ["P"]),
        ("entreprise de nettoyage musée", ["P"]),
        ("société de nettoyage musée", ["P"]),
        ("nettoyage théâtre", ["P"]),
        ("nettoyage salle de spectacle", ["P"]),
        ("nettoyage cinéma", ["P"]),
        ("nettoyage salle de concert", ["P"]),
        ("nettoyage salle de sport", ["P"]),
        ("nettoyage salle de sport et fitness paris", ["P"]),
        ("nettoyage galerie d'art", ["P"]),
        ("nettoyage discothèque", ["P"]),
        ("désinfection salle de conférence paris", ["P"]),
        ("nettoyage événementiel paris", ["P"]),
        ("nettoyage après événement paris", ["P"]),
    ]),
    "Hôtellerie & Restauration": ("hotel", [
        ("nettoyage hôtel paris", ["E", "P"]),
        ("société de nettoyage hôtel", ["P"]),
        ("entreprise de nettoyage hôtel", ["P"]),
        ("nettoyage hôtelier paris", ["P"]),
        ("société de nettoyage hôtelier paris", ["P"]),
        ("nettoyage hôtel et restaurant", ["P"]),
        ("nettoyage restaurant paris", ["P"]),
        ("nettoyage restaurant et salle paris", ["P"]),
        ("nettoyage hôtels haut de gamme", ["P"]),
        ("nettoyage boulangerie et pâtisserie paris", ["P"]),
        ("dégraissage cuisine professionnelle paris", ["P"]),
    ]),
    "Santé & Médical": ("sante", [
        ("nettoyage médical", ["E", "P"]),
        ("société de nettoyage médical", ["P"]),
        ("agence de nettoyage médical", ["P"]),
        ("entreprise de nettoyage médical paris", ["P"]),
        ("nettoyage cabinet médical paris", ["P"]),
        ("nettoyage cabinet dentaire paris", ["P"]),
        ("nettoyage laboratoire d'analyses paris", ["P"]),
        ("bionettoyage paris", ["P"]),
        ("nettoyage pharmacie paris", ["P"]),
        ("nettoyage maison de retraite paris", ["P"]),
        ("désinfection médicale paris", ["P"]),
    ]),
    "Bureaux & Tertiaire": ("bureaux", [
        ("nettoyage bureaux paris", ["E", "P"]),
        ("entreprise de nettoyage bureaux paris", ["P"]),
        ("nettoyage tertiaire paris", ["P"]),
        ("nettoyage tertiaire ile de france", ["P"]),
        ("société de nettoyage bureaux paris", ["P"]),
        ("entretien de bureaux paris", ["P"]),
        ("nettoyage espace de coworking paris", ["P"]),
        ("entretien moquette bureau paris", ["P"]),
    ]),
    "Nettoyage Paris/IDF (local)": ("local", [
        ("entreprise de nettoyage paris", ["E", "P"]),
        ("société de nettoyage paris", ["P"]),
        ("entreprise de nettoyage ile de france", ["P"]),
        ("entreprise de nettoyage paris 2", ["P"]),
        ("nettoyage professionnel paris", ["P"]),
        ("devis nettoyage entreprise paris", ["P"]),
        ("entreprise de nettoyage de bureaux ile de france", ["P"]),
    ]),
}

MT = {"E": "Exact", "P": "Phrase"}

# Négatifs (niveau campagne) — emploi/B2C/hors-zone/infos
NEGATIVES = [
    # Emploi / formation
    "emploi", "recrutement", "offre d'emploi", "recrute", "salaire", "cdi", "cdd",
    "intérim", "interim", "stage", "alternance", "apprentissage", "formation", "diplôme",
    "cap", "métier", "fiche de poste", "devenir agent", "pole emploi", "indeed", "leboncoin",
    # B2C / particuliers / low-cost
    "femme de ménage", "aide ménagère", "ménage à domicile", "à domicile", "particulier",
    "auto-entrepreneur", "autoentrepreneur", "micro-entreprise", "pas cher", "gratuit",
    # Produits / matériel
    "produit", "produits", "matériel", "machine", "autolaveuse", "karcher", "location", "achat",
    # Infos / divers
    "définition", "c'est quoi", "wikipedia", "franchise",
    # Hors Île-de-France
    "lyon", "marseille", "lille", "bordeaux", "toulouse", "nantes", "nice", "strasbourg",
    "montpellier", "rennes", "marne",
]


def main() -> None:
    HERE.mkdir(exist_ok=True)
    # Mots-clés
    with open(HERE / "spn-ads-keywords.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Campaign", "Ad Group", "Keyword", "Match Type", "Final URL"])
        n = 0
        for grp, (lpk, kws) in GROUPS.items():
            for kw, mts in kws:
                for mt in mts:
                    w.writerow([CAMP, grp, kw, MT[mt], LP[lpk]])
                    n += 1
    # Négatifs
    with open(HERE / "spn-ads-negatives.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Campaign", "Keyword", "Match Type"])
        for kw in NEGATIVES:
            w.writerow([CAMP, kw, "Broad"])
    print(f"✓ spn-ads-keywords.csv : {n} mots-clés / {len(GROUPS)} groupes")
    print(f"✓ spn-ads-negatives.csv : {len(NEGATIVES)} négatifs")


if __name__ == "__main__":
    main()
