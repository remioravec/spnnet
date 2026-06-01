# Audit complet — spn-net.fr

**Date :** 1ᵉʳ juin 2026
**Périmètre :** 60 URL (toutes en HTTP 200), récupérées via le sitemap.
**Site :** SPN-NET — entreprise de nettoyage, Paris & Île-de-France.
**Méthode :** crawl automatisé (`audit/crawl.py`) + analyse (`audit/analyze.py`). Données brutes dans `audit/data/` et `audit/reports/`.

> ⚠️ **Accès en écriture WordPress bloqué.** Le serveur LiteSpeed ne transmet pas l'en-tête `Authorization` à WordPress : l'authentification via mot de passe d'application échoue (même des identifiants bidon renvoient `rest_not_logged_in`). Correctif `.htaccess` fourni en fin de document. L'audit ci-dessous repose sur le contenu public et ne nécessitait pas cet accès.

---

## 1. Synthèse — note globale

| Domaine | Note | Constat principal |
|---|---|---|
| Structure / maillage interne | 🟠 Moyen | Méga-menu omniprésent ; **12 articles de blog orphelins** |
| Boutons & CTA | 🟢 Bon | CTA présents, mais ancres répétitives |
| Surfeur raisonnable | 🔴 À corriger | **80,6 % des liens internes sont du boilerplate** (menu/footer) |
| Diversification des ancres | 🔴 À corriger | Ancres exactes répétées à ~100 % ; 179 ancres vides |
| Qualité / lisibilité | 🟠 Moyen | Lisibilité faible (Flesch ~25–45) ; contenu dense |
| SEO on-page | 🟠 Moyen | **18 pages sans H1** ; sinon titles/metas/alt corrects |

**Points forts :** aucune image sans attribut `alt` (60 pages), titles et meta-descriptions presque tous dans les bonnes longueurs, contenu volumineux sur les pages secteurs/locales, temps de réponse corrects.

---

## 2. Audit des boutons & liens

- **3 880 liens internes** au total sur 60 pages, soit ~65 liens/page.
- Répartition par zone :
  - `nav` (menu) : **2 655** (68,4 %)
  - `footer` : **354** (9,1 %)
  - `header` : **118** (3,0 %)
  - **`main` (contenu) : 753 (19,4 %)**
- **179 liens à ancre vide** (liens sur image/icône sans texte ni `aria-label` exploitable) et **124 liens à ancre générique** (« contact », « devis », « en savoir plus »…).
- La page d'accueil émet **95 liens sortants** (lourd ; à alléger).

**Recommandations boutons/liens**
1. Ajouter un `aria-label` explicite à chaque lien-image/icône (179 cas) — accessibilité + signal sémantique.
2. Réduire le nombre de liens du méga-menu visibles simultanément (sous-menus repliés) pour concentrer le « jus » sur les liens utiles.
3. Varier les libellés de CTA (voir §4).

---

## 3. Surfeur raisonnable (reasonable surfer)

Le modèle du surfeur raisonnable de Google pondère un lien selon sa **probabilité d'être cliqué** : un lien contextuel dans le corps du texte vaut bien plus qu'un lien de menu/footer répété sur tout le site.

**Constat : seuls 19,4 % des liens internes sont contextuels.** Le reste (80,6 %) est du boilerplate à faible poids. Pire, plusieurs pages à fort potentiel sont des **culs-de-sac** :

| Page | Mots | Liens contextuels entrants | Liens contextuels sortants |
|---|---|---|---|
| `/meilleure-entreprise-nettoyage-tertiaire-paris/` | 1 533 | **0** | 0 |
| `/meilleure-entreprise-nettoyage-sante-medical-paris/` | 1 776 | **0** | 0 |
| `/meilleure-entreprise-nettoyage-apres-sinistre-paris/` | 3 135 | **0** | 1 |
| …(les 12 articles de blog) | 1 393–3 614 | **0–1** | **0–1** |
| `/a-propos/` | 506 | — | 1 |

➡️ Ces 12 articles représentent **~24 000 mots de contenu** quasi invisibles pour le maillage interne. Ils ne reçoivent ni ne transmettent de jus contextuel.

**Recommandations surfeur raisonnable**
1. **Relier chaque article de blog à sa page secteur** correspondante, dans les deux sens, via un lien contextuel en plein corps de texte (ex. `/tertiaire/` ⇄ `/meilleure-entreprise-nettoyage-tertiaire-paris/`).
2. Ajouter dans le corps des pages secteurs/locales **2–4 liens contextuels** vers les pages connexes (secteur ↔ zone ↔ service), avec une ancre descriptive intégrée à une phrase.
3. Limiter le poids du menu : c'est un signal de structure, pas un canal de transmission de jus. Le maillage *éditorial* doit porter la hiérarchie thématique.

---

## 4. Diversification des ancres

**Constat : ancres internes massivement sur-optimisées (exact-match).** 34 cibles reçoivent ≥ 80 % de leurs liens avec une ancre identique :

| Ancre | Cible | Exact-match |
|---|---|---|
| `blog` | `/blog/` | 119/120 (99 %) |
| `nos engagements` | `/a-propos/` | 118/118 (100 %) |
| `tertiaire` | `/tertiaire/` | 62/73 (85 %) |
| `paris 8`, `paris 9`… | pages locales | 100 % |

> ⚠️ Une grande part de cette répétition vient du **menu** (donc « normal » techniquement), mais cela révèle que **le maillage éditorial n'apporte aucune variété d'ancre** : il n'existe presque pas de liens contextuels avec des ancres riches et naturelles.

**Recommandations ancres**
1. Construire un **plan d'ancres diversifiées** par page cible : 1 ancre exacte tolérée, puis variantes partielles, sémantiques et naturelles.
   - Ex. pour `/tertiaire/` : « nettoyage de bureaux », « entretien de locaux tertiaires à Paris », « propreté des espaces de travail », « notre offre tertiaire »…
2. Remplacer les 124 ancres génériques (« en savoir plus », « devis ») par des ancres descriptives.
3. Donner un texte/`aria-label` aux 179 liens à ancre vide.

---

## 5. Qualité, lisibilité & agréabilité du contenu

- **Volume :** très bon globalement (médiane ~1 700 mots). Pages minces : `/contact/` (259), `/blog/` (342), `/sitemap.html/` (105 — page technique, non indexable de préférence).
- **Lisibilité (Flesch FR) :** **faible sur l'ensemble** — la majorité des pages se situent entre **25 et 48** (« difficile » à « assez difficile »). La page d'accueil ressort à ~0 (texte de menu mêlé au contenu). Cela traduit des **phrases longues et un vocabulaire dense**.
- **Agréabilité :** structure Hn présente et logique sur les pages secteurs/services, mais le ton est très « bloc SEO » (répétitif, formulations proches d'une page à l'autre sur les pages locales générées par gabarit).

**Recommandations contenu**
1. **Raccourcir les phrases** (cible : < 20 mots en moyenne) et aérer (listes à puces, intertitres) pour remonter le Flesch vers 50–60.
2. **Différencier les pages locales** (Paris 1–20, départements) : elles partagent un gabarit très similaire — ajouter des éléments réellement locaux (quartiers, références, exemples) pour éviter le contenu quasi-dupliqué.
3. Enrichir `/contact/` et `/blog/` (intro éditoriale, FAQ, réassurance).
4. Humaniser le ton : bénéfices client concrets, preuves (chiffres, certifications, avis).

---

## 6. SEO on-page — anomalies prioritaires

| Anomalie | Pages concernées | Priorité |
|---|---|---|
| **H1 manquant** | 18 pages : toutes les `paris-X` (sauf accueil), les 7 départements, `/a-propos/`, `/contact/`, `/proprete-des-locaux/`, `/ascenseurs-escalators/`, `/mention-legales/` | 🔴 Haute |
| Contenu mince | `/contact/`, `/blog/`, `/sitemap.html/` | 🟠 Moyenne |
| Trop de liens sortants | `/` (95) | 🟠 Moyenne |
| `/sitemap.html/` indexable (title 11 car., pas de meta) | 1 | 🟢 Basse |

> Les pages locales démarrent en **H2** (« Paris Centre »…) sans H1 : c'est l'anomalie la plus répétée. Chaque page doit avoir **exactement un H1** contenant le mot-clé principal (ex. « Entreprise de nettoyage — Paris 1 (75001) »).

**Bons points :** 0 image sans `alt`, titles 30–65 car. quasi partout, meta-descriptions 127–158 car., `lang` défini, canoniques présentes.

---

## 7. Plan d'action priorisé

| # | Action | Impact | Effort |
|---|---|---|---|
| 1 | Ajouter un **H1 unique** aux 18 pages sans H1 | 🔴🔴🔴 | Faible |
| 2 | **Relier les 12 articles** de blog à leurs pages secteurs (maillage bidirectionnel) | 🔴🔴🔴 | Moyen |
| 3 | Injecter **2–4 liens contextuels** à ancres diversifiées dans chaque page secteur/locale | 🔴🔴 | Moyen |
| 4 | Remplacer ancres génériques (124) et libeller les liens vides (179) | 🔴🔴 | Moyen |
| 5 | **Réécrire pour la lisibilité** (phrases courtes, listes) les pages denses | 🟠 | Élevé |
| 6 | **Différencier** les pages locales (anti-duplication) | 🟠 | Élevé |
| 7 | Corriger le `.htaccess` (en-tête Authorization) pour permettre l'automatisation via API | 🔴 | Faible |

---

## Annexe — correctif accès API WordPress

À placer **en haut** du `.htaccess` à la racine du site (LiteSpeed/Apache) :

```apache
# Transmettre l'en-tête Authorization à PHP
RewriteEngine On
RewriteCond %{HTTP:Authorization} ^(.*)
RewriteRule ^(.*) - [E=HTTP_AUTHORIZATION:%1]
```

Une fois en place, l'API REST acceptera le mot de passe d'application et les agents IA (§ dossier `agents/`) pourront appliquer automatiquement les corrections des actions 1 à 4.
