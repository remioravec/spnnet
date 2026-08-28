# Google Ads — SPN NET (structure prête à importer)

Fondé sur les données **Search Console** (demande non-marque réelle) — voir hiérarchie ci-dessous.
**Pas de campagne de marque** (« SPN-NET » exclu, présent dans les négatifs).

## Fichiers
- `spn-ads-keywords.csv` — mots-clés par groupe d'annonces + **URL finale = LP dédiée** (message-match).
- `spn-ads-negatives.csv` — mots-clés à exclure au **niveau campagne**.
- `build_ads.py` — régénère les CSV.

## Import dans Google Ads Editor
1. Ouvrir **Google Ads Editor** → compte → **Comptes › Importer › Depuis un fichier**.
2. Importer `spn-ads-keywords.csv` (colonnes : Campaign, Ad Group, Keyword, Match Type, Final URL).
3. Importer `spn-ads-negatives.csv` (mots-clés négatifs de campagne).
4. Vérifier, puis **Publier**.
> Les CSV créent la campagne « Search – Nettoyage Paris IDF » et ses 5 groupes si absents.

## Structure recommandée (1 campagne Search)
| Groupe d'annonces | Landing page (URL finale) | Priorité (data GSC) |
|---|---|---|
| Culture & Événementiel | `/nettoyage-musee-theatre-evenementiel-paris/` | 🥇 626 impressions |
| Hôtellerie & Restauration | `/nettoyage-hotel-restaurant-paris/` | 🥈 339 |
| Santé & Médical | `/nettoyage-medical-sante-paris/` | 🥉 211 |
| Bureaux & Tertiaire | `/devis-nettoyage-bureaux-paris/` | 125 |
| Nettoyage Paris/IDF (local) | `/devis-nettoyage-bureaux-paris/` | 81 |

> Commerce, Copropriété, Logistique, Enseignement : **0 demande prouvée** → non ouverts au lancement.

## Paramétrage de la campagne
- **Type** : Réseau de Recherche uniquement (décocher Display partenaires).
- **Zone géo** : Paris + communes IDF (cibler « présence » et non « intérêt »).
- **Langue** : français.
- **Correspondances** : Expression par défaut, Exact sur les têtes de série ; Large seulement après conversions + enchères auto.
- **Assets** : extensions de **lieu** (lier la fiche Google Business Profile), **appel** (01 49 46 22 40), **liens annexes** (Devis 24h, Secteurs, Avis, Zones), **accroches** (ISO 45001, EcoVadis Argent, 30 ans, Devis sous 24h).
- **Enchères** : démarrer *Maximiser les clics* (plafond CPC) ~2-3 sem., puis *Maximiser les conversions / CPA cible* dès 15-30 conversions.

## Conversions à configurer AVANT de scaler (priorité absolue)
La LP pousse déjà dans le `dataLayer` :
- `spn_lead_submit` (envoi formulaire)
- `spn_click_to_call` (clic téléphone)
→ Créer **2 conversions Google Ads** via GTM sur ces événements. Sans tracking, pas de Smart Bidding.

## Notes
- Les services transverses (vitrerie, fournitures sanitaires, petite maintenance) ne sont **pas** des mots-clés Ads (≈0 demande, up-sells) → réservés au SEO.
- Les leads des LP arrivent via votre **formulaire Elementor existant** (form `ae4c659`) → mêmes notifications e-mail. Le champ « referer » indique de quelle LP vient chaque lead.
