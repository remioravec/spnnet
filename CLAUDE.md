# CLAUDE.md — SPN NET

Contexte projet pour Claude Code. À poser à la racine du dossier de travail SPN NET.

---

## 1. Le client

**SPN NET** — `https://spn-net.fr` — société de nettoyage professionnel à Paris et en Île-de-France (bureaux, commerces, copropriétés, santé, logistique, hôtellerie, enseignement, ERP).

- Site **WordPress / Elementor**. Sitemap généré par le plugin *Google Sitemap Generator* 4.1.25.
- Contact client : Alexandra Guenantin (commerciale, responsable de secteurs).
- Axes prioritaires demandés : **CA, trafic, positionnement**. Carte blanche sur la méthode.
- Accent de marque `#d8431f`, fond `#faf8f5`, encre `#16181d`, lignes `#e9e4dd`, teinte `#fff1ea`.
- Polices du site : **Fraunces** (titres) + **Plus Jakarta Sans** (texte).

### Sources de données — ordre de priorité
1. **Search Console** — la mesure. Prime toujours sur l'estimation.
2. **Export Semrush** fourni par Rémi pour les positions. **DataForSEO sous-estime fortement ce domaine** (2 mots-clés remontés contre 61 chez Semrush) : ne jamais conclure sur la visibilité du site à partir de DataForSEO seul.
3. GA4 pour la conversion.

Un volume Google Ads nul n'écarte jamais une requête dès lors que la GSC mesure des affichages réels.

---

## 2. Accès et exécution

### Ce qui est branché
GSC · GA4 · Google Ads · Drive · Sheets · Gmail · GitHub.

**GSC** : propriété `https://spn-net.fr/` accessible en `siteOwner` (vérifié 11/09/2026).
**GA4** : propriété `properties/532410994` (vérifié 11/09/2026).

### Accès WordPress — EN ÉCRITURE, opérationnel
**Application Password actif** sur le compte administrateur, dans `.env` à la racine (gitignoré) :
`WP_USER` + `WP_APP_PASSWORD`. Capacités vérifiées le 21/09/2026 :
`edit_pages`, `publish_pages`, `manage_options` = `true`.

Publier directement via l'API REST, ne pas se contenter d'un livrable à coller :

```bash
set -a && . ./.env && set +a
curl -s -u "$WP_USER:$WP_APP_PASSWORD" https://spn-net.fr/wp-json/wp/v2/pages
```

Points appris à l'usage :
- Les pages du site sont rendues **hors Elementor** : `template=elementor_header_footer` + meta `_elementor_edit_mode=""`, le HTML vit dans `post_content`. C'est ce qui permet de maîtriser le gabarit.
- Les réglages d'un formulaire Elementor se modifient dans la meta `_elementor_data` (JSON), en `context=edit`.
- LiteSpeed sert des pages en cache ; la purge externe est refusée (405). Utiliser un paramètre d'URL pour vérifier une mise en ligne.
- Le proxy coupe parfois une requête en cours (`ws_closed_mid_exchange`) : **réessayer**, l'écriture a souvent abouti.

### Plugins maison déployés (code dans `wp-plugins/`)
| Plugin | Rôle |
|---|---|
| `spn-leads` | CRM des demandes. Table `wp_spn_leads`, capture Elementor + endpoint REST, backfill horaire, endpoints `/spn/v1/export`, `/import`, `/repair`. |
| `spn-redirects` | 301 des anciennes URL + exclusion du sitemap (`sm_b_exclude`) à l'activation. |
| `spn-smtp` | Envoi des e-mails via Google Workspace. Réglages dans *Réglages → Envoi e-mails*. |

### Envoi des e-mails
Compte SMTP : **`remi.oravec@seo-monkey.fr`** — avec un **point**.
⚠️ `remi-oravec@seo-monkey.fr` (tiret) **n'existe pas** : Google renvoie *Address not found*. Ne jamais l'utiliser comme destinataire. Elle reste le *login* WordPress, ce qui prête à confusion.
Destinataires des demandes : `a.guenantin@spn-net.fr`, `f.guenantin@spn-net.fr`, `remi.oravec@seo-monkey.fr`.

### Crawl du site
`web_fetch` est refusé par le robots.txt du site. Passer par `curl` avec un User-Agent navigateur, ce qui fonctionne :

```bash
curl -sL -A "Mozilla/5.0 Chrome/120.0" https://spn-net.fr/sitemap.xml -o sitemap.xml
# sous-sitemaps : sitemap-misc.xml · page-sitemap.xml · post-sitemap.xml
```

Pour séparer les liens du corps de ceux de la navigation, découper le HTML entre `</header>` et `<footer` — la structure est propre sur tous les gabarits.

---

## 3. État mesuré au 21/09/2026

Relevé sur les 87 URL du sitemap, dont 65 répondent 200.

| Mesure | Valeur | Seuil visé |
|---|---|---|
| Liens in-body / liens totaux d'une page | **9 %** (7 contre 71 en navigation) | ≥ 15 % |
| Ancres distinctes ÷ liens entrants sur `/tertiaire/` | **0,14** (112 liens, 16 ancres, dont 79 % sur 2 ancres) | ≥ 0,8 |
| Idem sur `/92-hauts-de-seine/` | **0,21** (62 liens, 13 ancres) | ≥ 0,8 |
| Liens vers une URL en 301 | **84** (19 in-body + 65 en pied de page) | 0 |
| URL du sitemap en 301 | **22 / 87** — dont les 19 du post-sitemap | 0 |
| Profondeur | 41 pages à 1 clic, 20 à 2 clics, **3 inatteignables** | ≤ 3 clics |

### Faits structurants
- Le pied de page pointe sitewide vers `/proprete-des-locaux/`, qui redirige en 301 vers `/tertiaire/`. **65 liens perdus en une ligne.**
- Les blocs de cartes mettent titre + sous-titre + « Découvrir → » dans un seul `<a>`. Ce ne sont pas des ancres, ce sont des cartes. Le mot-clé cible n'y est jamais contigu.
- `/portage/`, `/peinture/`, `/marquage-au-sol/` forment un **îlot fermé** : elles ne se lient qu'entre elles, ancre « Voir nos services », zéro lien entrant depuis le reste du site.
- Paris 18e et Paris 20e ne sont **pas au menu** et se classent 2e et 3e. Ce n'est pas le menu qui fait ranker.
- Cannibalisation `/meilleure-entreprise-nettoyage-{secteur}-paris/` résolue par 301 vers les pages secteur (25/08/2026). `/ascenseurs/` et `/escalators/` désormais en 301 vers `/ascenseurs-escalators/`. **Ne pas rouvrir ces gabarits d'URL.**

### Le silo modèle
`/changer-de-prestataire-nettoyage/` : 13 liens entrants, 11 ancres distinctes, ratio 0,85. C'est le seul silo conforme du site. Il sert de référence aux deux autres.

---

## 4. Méthode de maillage — les règles

Elles s'appliquent à tous les clients, pas seulement SPN.

### Surfeur raisonnable
- La valeur d'un lien suit la probabilité de clic : **corps de texte, premier tiers ≫ fin d'article ≫ bloc « articles liés » ≫ méga-menu ≫ pied de page**.
- Une carte de maillage qui ne mesure pas l'**emplacement** mesure le mauvais graphe. Toujours compter `liens in-body / liens totaux de la page`.
- Le premier lien du DOM gagne. Si le menu pointe vers une cible avant le lien contextuel, c'est l'ancre du menu qui est retenue. À vérifier une fois par gabarit.
- **Ne pas réciproquer par principe.** Un lien retour que personne ne clique ne transmet rien et divise le flux sortant de la page qui le reçoit. Réciproquer seulement quand la lecture le justifie.
- Un lien se pose dans une phrase complète, dans le premier tiers du texte de sa section. Jamais après le module visuel, jamais en « lire aussi », jamais sous forme de carte.

### Ancres internes
Exact match contigu obligatoire, jeu d'ancres qui tourne par cible. Distribution sur les liens in-body, par URL cible :

| Type | Part | Exemple vers `/tertiaire/` |
|---|---|---|
| Exact match contigu | 40 % | nettoyage de bureaux à Paris |
| Exact + mot outil | 35 % | notre offre de nettoyage de bureaux |
| Phrase porteuse | 20 % | une prestation de propreté tenue sur vos plateaux |
| Titre de la page | 5 % | Nettoyage de bureaux à Paris & de locaux tertiaires |

Contrôles : jamais deux liens de la même page source vers la même cible avec la même ancre · pas plus de 4 occurrences de l'ancre exacte à l'échelle du site pour 11 entrants · **ancres distinctes ÷ liens entrants ≥ 0,8**.

Bannies : « Voir nos services », « Découvrir → », « Secteur lié », « Notre guide sectoriel ». **Une flèche dans l'ancre signale un titre de carte, pas un lien de lecture.**

### Ancres externes (netlinking)
Règle inverse de l'interne, et dépendante du type de lien. Les 3 blogs SEO du mois prennent du **semi-optimisé** ; l'article invité prend l'**exact match**. Les blogs d'abord, l'article invité ensuite — l'ancre exacte n'arrive jamais en premier. Jamais d'ancre de marque.

### Architecture d'un silo
```
Racine
└── Mère (elle vend)  ←→ Hub (guide d'achat, N sections numérotées)
     ├── Filles BOFU        ← une section du hub = une cible = un lien
     └── Articles de choix  → 2 liens montants : hub §N + mère
```
Un seul hub par silo. Deux hubs dans le même silo, c'est une cannibalisation.

---

## 5. Le chantier en cours : le hub de choix

### La page
`/choisir-entreprise-nettoyage/` — hub du silo bureaux. URL à re-trancher sur GSC (« entreprise » vs « prestataire ») avant publication.

Frontière à tenir : le guide traite le **choix**. Toute la procédure de résiliation reste sur `/changer-de-prestataire-nettoyage/`.

Conséquence : `/prix-nettoyage-bureaux-paris/` **cesse d'être un hub** et redevient l'article de choix du §2.

### Les 10 sections et leurs 15 liens sortants

| § | Section | Cible |
|---|---|---|
| 1 | Généraliste ou spécialiste de vos locaux | `/tertiaire/` |
| 2 | Lire un devis, et le prix au m² | `/prix-nettoyage-bureaux-paris/` |
| 3 | Vérifier qu'il est en règle | `/travail-dissimule-entreprise-nettoyage/` |
| 4 | Les certifications qui comptent | `/certifications-entreprise-nettoyage/` |
| 5 | Qui entre dans vos locaux | `/nettoyage-bureaux-confidentialite-securite/` |
| 6 | Le suivi qualité, et le 3e mois | `/qualite-nettoyage-baisse-apres-3-mois/` |
| 7 | Proximité et remplacement | `/paris-8/` + `/92-hauts-de-seine/` → `/paris/` après T9 |
| 8 | Ce qui n'est pas dans le contrat | `/ascenseurs-escalators/` `/portage/` `/peinture/` `/marquage-au-sol/` |
| 9 | Vous avez déjà un prestataire | `/changer-de-prestataire-nettoyage/` + `/annexe-7-changer-entreprise-nettoyage/` |
| 10 | La grille de comparaison | `/contact/` |

Réciprocité sur §1 à §6 et §9. **Allers simples sur §7, §8 et §10.**

### Les 16 liens entrants à poser
Les 8 pages secteur · le lien montant de chacun des 6 articles (§2 à §6 et §9) · `/blog/`. **16 ancres distinctes, une par source.**

### Partis pris à ne pas défaire sans arbitrage de Rémi
- Le CTA du hero ouvre la grille, **pas** le formulaire. La seule demande de devis est en bas de page.
- Le bloc de réponse en 10 lignes (cible AI Overview) ne porte **aucun lien**.
- §4, §5, §8, §9 n'ont aucune interaction : leur tableau se suffit.
- Le module §10 **n'échange rien contre le PDF** — pas d'e-mail, pas de formulaire. C'est ce qui le rend citable et linkable. Point encore ouvert côté client.

---

## 6. Roadmap technique de maillage

| # | Modification | Gain | Charge | Statut |
|---|---|---|---|---|
| T1 | Pied de page : `/proprete-des-locaux/` → `/tertiaire/` | 65 liens | 5 min | À FAIRE |
| T2 | Sortir sous-titre et flèche du `<a>` dans les blocs de cartes | ~180 ancres | 1 h | À FAIRE |
| T3 | Réécrire les 8 liens « Guide sectoriel » (301) | 8 liens | 20 min | À FAIRE |
| T4 | Câbler `/prix-nettoyage-bureaux-paris/` | +8 liens | 1 h | **Caduc** — le hub le fait mieux |
| T5 | Bloc « secteurs liés » de 8 cartes à 3 | −5 sortants/page | 2 h | À FAIRE |
| T6 | Casser l'îlot portage / peinture / marquage | +6 liens | 30 min | **Fait par le §8 du hub** |
| T7 | Corriger les liens in-body vers `/ascenseurs/` et `/escalators/` | 8 liens | 15 min | À FAIRE |
| T8 | Supprimer `post-sitemap.xml`, purger les 22 URL en 301 | −22 URL | 10 min | À FAIRE |
| T9 | Créer `/paris/`, alléger le menu de 33 à 21 URL | +21 pages câblées | 3 h | À FAIRE |
| T10 | Limiter les liens entre sœurs géo à 2 voisins | −44 liens boilerplate | 3 h | À FAIRE |

**20/80 :** T1 à T3 font 1 h 25 et récupèrent 81 liens. T9 est le seul levier qui agit sur les 65 pages en même temps (ratio in-body de 9 % à ~15 %).

---

## 7. Livrables produits

| Fichier | Contenu |
|---|---|
| `spn-choisir-entreprise-nettoyage.html` | La page complète au gabarit du site, 10 sections, 15 liens in-body, grille interactive, FAQ, JSON-LD Article + FAQPage + BreadcrumbList |
| `spn-bandeau-ebook.html` | Bloc autonome pour widget HTML Elementor global — home + 21 pages du méga-menu |
| `spn-guide-ebook.webp` / `.png` | Couverture ebook 738 × 840, polices et couleurs du site |

Pose du bandeau : **après le premier bloc de contenu, jamais au-dessus du H1.** Conserver `width`, `height`, `loading="lazy"`, `decoding="async"` — c'est ce qui empêche le décalage de mise en page sur 22 pages.

### Générateurs en place (`agents/landing/`)
`make_zone.py` (pages arrondissements et départements) · `make_sector.py` · `make_communes.py` · `make_special.py` (a-propos, blog, contact) · `make_article.py` + `make_blog_aout.py` + `make_juillet.py` (articles) · `navboost.py` (modules d'attention : calculateurs, checklists, tableaux triables).

---

## 8. Charte de production — Rémi Oravec

### Forme
- Livrable **directement actionnable**, aucune étape intermédiaire.
- Sorties copiables : **TSV** pour Google Sheets. En fin de process, donner la roadmap en bloc TSV dans le chat même si le classeur a déjà été mis à jour.
- Classeurs de roadmap : uniquement les colonnes client, aucune ligne ni colonne morte, colonnes assez larges pour que le texte tienne sur une ligne, mois et semaines fusionnés par blocs, **couleur conditionnelle sur la ligne entière** selon le statut. Ligne 1 = cellule fusionnée sur toute la largeur, figée, qui explique quoi / pourquoi / comment.
- Statuts roadmap : `A FAIRE` · `EN COURS` · `TERMINE` · `BLOQUE`. Netlinking : **`Proposé` · `Intégré`** seulement.
- Mise à jour d'un document existant : **ne pas casser la forme.** Modifier uniquement les cellules ciblées.

### Contenu
- Contenu SEO : brief + rédaction en **`.docx` mis en page**, jamais en markdown brut, **plus** un rendu de la page en un seul fichier HTML/CSS/JS autonome, dans le gabarit du site du client.
- `.docx` : ne jamais faire un encart ou une étiquette en tableau à une cellule — Google Docs recalcule la largeur et le bloc s'effondre. Paragraphes bordés uniquement.
- Mise à jour d'une page existante : tableau « section actuelle → ce qu'elle devient → décision », étiquette CONSERVÉ / RÉÉCRIT / NOUVEAU sur chaque section, passages à valeur repris mot pour mot.
- Section d'un hub dont le contenu existe déjà → **brief de branchement** (RETIRER / AJOUTER / DÉPLACER / NE PAS BRANCHER), pas un brief de contenu.
- Modèles de pages : l'UX/UI et l'interaction priment sur le contenu. Construire dans cet ordre.
- **Ne jamais inventer une offre ni une certification.** SPN NET détient **ISO 45001** et la **médaille d'argent EcoVadis 2025**, rien d'autre. Les fourchettes de prix publiées sont des **relevés de marché datés et sourcés**, signalés comme tels, jamais présentés comme les tarifs de SPN.
- Tagline : « propreté professionnelle », pas « nettoyage professionnel ».

### Reporting
- Lecture **sur 3 mois**, jamais à la semaine. Le toggle pilote la comparaison, pas la période.
- Courbes de trafic **hors marque**.
- Graphiques de position : **axe inversé**, la position 1 en haut.
- Écarter le mois en cours / partiel des séries.
- Toute perte constatée est présentée **avec sa solution en face**, rattachée à un ticket de roadmap.

### Posture
- **Challenger systématiquement.** Donner le 20/80, expliquer pourquoi c'est pertinent, proposer par quoi remplacer les actions à faible impact.
- Adosser chaque décision à **un chiffre**. Si le sujet est confus, chercher le chiffre unique qui donne la clarté plutôt qu'ajouter du détail.
- Arbitrage technique : ne pas trancher sur les recommandations officielles Google — **regarder ce que fait la SERP**, relevé daté de ceux qui rankent sur la requête cible.
- Vérifier le sitemap du client avant de proposer des pages à créer. Beaucoup existent déjà.
- Exécuter directement via l'API ou Composio quand c'est possible, plutôt que livrer un script à lancer.
- Réponses en chat **courtes**. Le livrable porte le détail.
- Tutoiement avec Rémi. Vouvoiement dans les livrables et les mails adressés à des tiers.
