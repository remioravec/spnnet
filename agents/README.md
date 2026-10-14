# Agents IA — amélioration SEO/contenu de spn-net.fr

Système multi-agents (Anthropic SDK / Claude) qui transforme les conclusions de
l'audit (`audit/reports/`) en améliorations concrètes du site, avec une étape de
revue humaine (mode *propose*) avant toute publication (mode *apply*).

## Les 4 agents

| Agent | Fichier | Ce qu'il fait | Source d'audit |
|---|---|---|---|
| **H1** | `h1_agent.py` | Génère un H1 unique optimisé pour les 18 pages sans H1 | `issues.json` |
| **Maillage** | `internal_linking_agent.py` | Relie les 12 articles orphelins ↔ pages secteurs (liens contextuels) | `content.json` |
| **Ancres** | `anchor_agent.py` | Plan d'ancres diversifiées pour les ancres sur-optimisées | `summary.json` |
| **Lisibilité** | `readability_agent.py` | Réécrit les pages peu lisibles (Flesch < 35) | `content.json` |

## Architecture

```
audit/reports/*.json ─▶ Agent.analyze() ─▶ Claude (llm.py) ─▶ Proposal[]
                                                                  │
                          dry-run ─────────────────────────────▶ agents/proposals/*.json
                          apply  ──▶ WordPressClient.update_content() ─▶ API REST WP
```

- **`llm.py`** — wrapper Claude : modèle `claude-opus-4-8` (défaut), pensée
  adaptative, **prompt caching** du prompt système figé, sorties structurées
  (JSON schema) pour les agents qui en ont besoin.
- **`wp_client.py`** — client REST WordPress : lecture publique + écriture
  authentifiée (mot de passe d'application), avec mode `dry_run`.
- **`base.py`** — classe `Agent` + dataclass `Proposal` ; gère propose/apply et
  la sauvegarde des propositions.

## Utilisation

```bash
# 1. Variables d'environnement
export ANTHROPIC_API_KEY=sk-ant-...        # pour la génération par Claude
export WP_BASE_URL=https://spn-net.fr
export WP_USER="votre-login"               # pour --apply uniquement
export WP_APP_PASSWORD="xxxx xxxx xxxx ..."  # mot de passe d'application

# 2. Tester l'accès en écriture
python3 agents/run.py --verify-auth

# 3. Générer les propositions (aucune écriture)
python3 agents/run.py --dry-run                      # tous les agents
python3 agents/run.py --agents h1,links --dry-run    # sélection

# 4. Appliquer (après revue des propositions)
python3 agents/run.py --apply
```

Sans `ANTHROPIC_API_KEY`, les agents H1 / maillage / ancres basculent sur une
logique **déterministe de repli** (résultats plus simples) ; la lisibilité
nécessite la clé API.

## ⚠️ Pré-requis pour `--apply`

L'écriture via l'API REST échoue tant que le serveur **LiteSpeed ne transmet pas
l'en-tête `Authorization` à PHP**. Correctif `.htaccess` (racine du site) :

```apache
RewriteEngine On
RewriteCond %{HTTP:Authorization} ^(.*)
RewriteRule ^(.*) - [E=HTTP_AUTHORIZATION:%1]
```

Tant que ce n'est pas en place, `--verify-auth` renvoie `401` et `--apply` est
refusé : utilisez `--dry-run`, les propositions restent exploitables manuellement.

## Sécurité & bonnes pratiques

- **Revue humaine** : `--dry-run` est le défaut ; relisez `agents/proposals/`
  avant `--apply`.
- **Ne pas committer de secrets** : `ANTHROPIC_API_KEY` / `WP_APP_PASSWORD`
  passent par l'environnement, jamais dans le code.
- L'insertion H1 / liens se fait en tête/fin de contenu — un placement éditorial
  plus fin (au sein du corps) est recommandé en revue avant publication massive.
