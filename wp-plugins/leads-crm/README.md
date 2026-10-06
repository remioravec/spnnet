# Demandes — CRM des leads

CRM léger pour WordPress : capture toutes les demandes du site, les qualifie,
détecte le canal d'acquisition et les exporte. **Aucune valeur client en dur** :
le même fichier se pose sur n'importe quel WordPress.

## Installer sur un nouveau site

1. Extensions → Ajouter → Téléverser `leads-crm.zip` → Activer.
2. C'est tout. Les réglages sont déduits du site : nom de la marque, domaine,
   e-mail de l'administrateur. Le plugin est fonctionnel sans configuration.
3. Pour personnaliser : **Demandes → Réglages**.

## Ce qui se règle

| Réglage | Par défaut | À quoi ça sert |
|---|---|---|
| Nom de la marque | nom du site | objet de l'e-mail, nom du fichier exporté |
| Domaine affiché | domaine du site | sous-titre de l'e-mail |
| Couleur d'accent | `#2563eb` | e-mail et tableau de bord |
| Objet de l'e-mail | `Nouvelle demande - {marque} - Site internet` | jetons `{marque}` et `{domaine}` |
| Destinataires | e-mail admin | un par ligne ou séparés par des virgules |
| Adresses à ne jamais notifier | vide | boîtes inexistantes, identifiants qui ne sont pas des e-mails |
| Adresses de test à ignorer | vide | en plus de `@example.com` et des noms en `ZZ TEST` |
| Anciennes routes REST | vide | namespaces à conserver en plus de `leads/v1` |
| Envoyer l'e-mail | **décoché** | voir ci-dessous |

### L'interrupteur d'e-mail, le piège à connaître

Il est **décoché par défaut**, et c'est volontaire. Si votre formulaire
(Elementor, Gravity Forms…) envoie déjà son propre e-mail, activer celui du
plugin fait partir **deux** messages par demande. Ne l'activez que si le
formulaire n'envoie rien, ou si vous préférez la mise en page du plugin —
auquel cas coupez l'envoi côté formulaire.

## Comment les demandes arrivent

- **Elementor Pro** : automatique, via `elementor_pro/forms/new_record`.
- **Endpoint REST** : `POST /wp-json/leads/v1/lead`, JSON
  `{name, email, phone, company, message, source, form}`.
- **Filet horaire** : un cron relit les soumissions Elementor, pour que la
  table se resynchronise seule si la capture temps réel décroche.

Les doublons sont écartés sur 180 secondes (même e-mail ou même téléphone).

## Canal d'acquisition

Lu dans l'URL d'arrivée, sans traceur :

- **Google Ads** — `gclid`, `gbraid`, `wbraid`, `gad_source`, `gad_campaignid`,
  ou `utm_medium` à `cpc` / `ppc` / `paid`
- **IA** — `utm_source` contenant chatgpt, openai, perplexity, copilot, gemini, claude
- **Nom de la source** — tout autre `utm_source`
- **SEO / direct** — le reste

Ce dernier groupe n'est pas tranché à dessein : sans référent, une visite
organique et un accès direct sont indiscernables depuis la seule URL
d'atterrissage. Mieux vaut un libellé honnête qu'un SEO gonflé.

## Reprise d'un site déjà équipé

Le plugin remplace l'ancienne extension « CRM des demandes ». À l'activation :

- la table existante est **conservée telle quelle** — aucun historique perdu,
  aucun renommage ;
- les destinataires et le réglage d'envoi sont **repris** ;
- l'ancienne route REST est **maintenue en plus** de la nouvelle, pour que les
  formulaires déjà en ligne continuent de poster sans être modifiés ;
- l'ancienne tâche planifiée est retirée.

Désactivez l'ancienne extension **avant** d'activer celle-ci : tant que les deux
tournent, chaque demande serait enregistrée deux fois. Le plugin le détecte,
refuse de démarrer et l'affiche en clair.

## Désinstallation

La désactivation retire la tâche planifiée et **ne supprime rien** : la table et
les réglages restent en place.
