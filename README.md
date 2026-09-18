# spnnet — audit & agents IA pour spn-net.fr

Audit SEO/contenu du site [spn-net.fr](https://spn-net.fr) (entreprise de
nettoyage, Île-de-France) et système d'agents IA pour l'améliorer.

## Contenu

| Dossier | Rôle |
|---|---|
| `audit/` | Crawler (`crawl.py`) + analyse (`analyze.py`) → rapport `reports/AUDIT.md` |
| `agents/` | Système multi-agents (Claude) : H1, maillage interne, ancres, lisibilité |

## Démarrage rapide

```bash
pip install -r requirements.txt

# 1) Auditer le site
python3 audit/crawl.py        # récupère toutes les URL du sitemap
python3 audit/analyze.py      # produit audit/reports/

# 2) Générer des propositions d'amélioration (sans rien publier)
export ANTHROPIC_API_KEY=sk-ant-...
python3 agents/run.py --dry-run
```

## Le rapport d'audit

➡️ **[`audit/reports/AUDIT.md`](audit/reports/AUDIT.md)** — synthèse, maillage
interne / surfeur raisonnable, diversification des ancres, qualité & lisibilité,
SEO on-page, et plan d'action priorisé.

## Les agents IA

➡️ **[`agents/README.md`](agents/README.md)** — architecture, usage,
modes *dry-run* / *apply*, et pré-requis d'accès à l'API WordPress.

> **Note d'accès** : l'application automatique (`--apply`) nécessite que le
> serveur transmette l'en-tête `Authorization` à PHP. Correctif `.htaccess`
> documenté dans l'audit (annexe).
