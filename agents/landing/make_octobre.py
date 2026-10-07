#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les 2 contenus d'octobre 2026 qui manquaient (SPN NET).

Relevés SERP live du 07/10/2026 (DataForSEO, fr / France, depth 10).

  /contrat-nettoyage-copropriete/
      SERP en friche : AI Overview rang 1, puis un cabinet d'avocats sur un
      arrêt de jurisprudence, une annonce leboncoin de vente de contrats (#2),
      un blog de 2012 (#3), un forum de 2014 (#5), de l'assainissement et des
      gouttières. Aucun acteur ne tient le sujet.
      PAA : tarif moyen, comment rédiger un contrat, comment facturer,
      quelle loi régit les parties communes.
      → réponse encadrée + CHECKLIST des clauses à exiger + tableau du
        calendrier de décision en AG.

  /controle-qualite-prestataire-nettoyage/
      SERP entièrement écrite du point de vue du PRESTATAIRE : comparatifs de
      logiciels (#3, #6, #7, #9), pages commerciales d'entreprises de propreté
      (#1, #2, #4), offres d'emploi de contrôleur qualité (#5). Le PAA demande
      « meilleur logiciel » et « salaire d'un contrôleur qualité ».
      Related : « Fiche de contrôle qualité nettoyage Excel », « Modèle fiche
      de contrôle qualité nettoyage » — l'intention utile est un document.
      → réponse encadrée + GRILLE DE CONTRÔLE NOTÉE à remplir, côté client.

Frontières tenues avec l'existant :
  /nettoyage-copropriete/                        = le sujet general, le budget
  /contrat-nettoyage-copropriete/                = le contrat et son vote en AG
  /qualite-nettoyage-baisse-apres-3-mois/        = pourquoi la qualite baisse
  /controle-qualite-prestataire-nettoyage/       = le dispositif de controle
  /prestataire-nettoyage-ne-respecte-pas-contrat/= le litige, apres l'echec

Usage : python3 agents/landing/make_octobre.py [--dry]
"""
from __future__ import annotations
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import navboost as nb

COPRO   = "https://spn-net.fr/nettoyage-copropriete/"
HABITAT = "https://spn-net.fr/copropriete-et-habitat/"
PRIX    = "https://spn-net.fr/prix-nettoyage-bureaux-paris/"
CDC     = "https://spn-net.fr/cahier-des-charges-nettoyage-bureaux/"
QUAL    = "https://spn-net.fr/qualite-nettoyage-baisse-apres-3-mois/"
LITIGE  = "https://spn-net.fr/prestataire-nettoyage-ne-respecte-pas-contrat/"
RESIL   = "https://spn-net.fr/resilier-contrat-nettoyage/"
HUB     = "https://spn-net.fr/choisir-entreprise-nettoyage/"
CHANGER = "https://spn-net.fr/changer-de-prestataire-nettoyage/"
CTRL    = "https://spn-net.fr/controle-qualite-prestataire-nettoyage/"
CONTRAT = "https://spn-net.fr/contrat-nettoyage-copropriete/"

# ===================================================== A1 — CONTRAT COPRO ===

A1_BODY = """<p class="lead">Un contrat d'entretien de parties communes se vote en assemblée générale, à la majorité simple, et se reconduit tout seul si personne ne le dénonce. Ce qu'il doit contenir, qui décide quoi, et le calendrier à tenir pour ne pas se retrouver lié une année de plus.</p>

<div class="toc"><b>Au sommaire</b><ol>
<li><a href="#qui">Qui signe, qui vote, qui paie</a></li>
<li><a href="#clauses">Les clauses à exiger</a></li>
<li><a href="#duree">Durée, reconduction et dénonciation</a></li>
<li><a href="#calendrier">Le calendrier à tenir</a></li>
<li><a href="#erreurs">Ce qui fait déraper un contrat de copropriété</a></li>
</ol></div>

<h2 id="qui">Qui signe, qui vote, qui paie</h2>

<p>Trois acteurs, trois rôles distincts, et c'est la confusion entre les trois qui produit l'essentiel des litiges.</p>

<p>Le <strong>syndicat des copropriétaires</strong> est le client : c'est lui, personne morale, qui est partie au contrat. Le <strong>syndic</strong> ne signe qu'en exécution d'une décision d'assemblée : la loi du 10 juillet 1965 lui donne mission d'exécuter les décisions de l'assemblée générale, pas de choisir seul son prestataire. L'<strong>assemblée générale</strong> décide, et vote le budget prévisionnel qui porte la dépense.</p>

<p>Conséquence pratique : un contrat d'entretien signé par le syndic sans mandat de l'assemblée est contestable. Et un conseil syndical qui veut changer de prestataire ne peut pas le faire par lui-même — il prépare, l'assemblée tranche.</p>

<p>La dépense, elle, se répartit en charges générales selon les tantièmes, sauf si le règlement de copropriété prévoit une clé particulière pour l'entretien. Les fourchettes de budget sont détaillées dans notre page sur le <a href="__COPRO__">nettoyage de copropriété</a>, avec un calculateur par nombre de lots.</p>

<h2 id="clauses">Les clauses à exiger</h2>

<p>Un contrat d'entretien tient en quatre pages. Ce qui compte n'est pas sa longueur mais sa précision : tout ce qui n'y figure pas sera facturé en supplément, ou ne sera pas fait. Cochez ce que vous voulez y voir.</p>

__CLAUSES__

<p>Deux clauses pèsent plus que les autres. La première est le <strong>périmètre écrit zone par zone</strong> : sans lui, aucun manquement n'est démontrable, parce qu'il n'y a rien à quoi comparer. La seconde est la <strong>continuité de service</strong> : que se passe-t-il quand l'agent est absent, sous quel délai il est remplacé, et avec quelle information au conseil syndical.</p>

<p>Pour la rédaction du périmètre lui-même, notre <a href="__CDC__">cahier des charges de nettoyage</a> se remplit zone par zone et s'annexe directement au contrat.</p>

<h2 id="duree">Durée, reconduction et dénonciation</h2>

<p>La quasi-totalité des contrats d'entretien de copropriété sont conclus pour un an, avec <strong>tacite reconduction</strong>. Si personne ne dit rien avant l'échéance, le contrat repart pour douze mois aux mêmes conditions.</p>

<p>Le préavis de dénonciation est fixé par le contrat, pas par la loi. Trois mois est de loin le plus courant. Il se compte à rebours depuis la date anniversaire, et c'est la date de première présentation du recommandé qui fait foi.</p>

<p>Un point que beaucoup de conseils syndicaux ignorent : la <strong>loi Chatel ne s'applique pas</strong>. Elle protège les consommateurs et les non-professionnels ; un syndicat de copropriétaires agit pour la gestion de l'immeuble et n'en bénéficie pas en principe. Aucun rappel d'échéance ne vous est dû. La surveillance du calendrier est à votre charge. La procédure complète est détaillée dans notre guide pour <a href="__RESIL__">résilier un contrat de nettoyage</a>.</p>

<h2 id="calendrier">Le calendrier à tenir</h2>

<p>C'est ici que se perdent la plupart des changements de prestataire : non pas sur le fond, mais sur les dates. Deux contraintes se superposent — le préavis du contrat, et la date de l'assemblée générale annuelle. Il faut que la seconde tombe avant la première.</p>

<div class="tbl-wrap"><table class="tbl">
<caption>Rétroplanning pour un contrat à échéance au 31 décembre, préavis de 3 mois</caption>
<thead><tr><th>Quand</th><th>Qui</th><th>Quoi</th></tr></thead>
<tbody>
<tr><td>Juin</td><td>Conseil syndical</td><td>Bilan de l'année, relevés de contrôle à l'appui</td></tr>
<tr><td>Juillet – août</td><td>Conseil syndical</td><td>Cahier des charges, consultation de trois prestataires</td></tr>
<tr><td>Début septembre</td><td>Syndic</td><td>Inscription de la question à l'ordre du jour de l'AG</td></tr>
<tr><td><b>Avant le 30 septembre</b></td><td>Syndic</td><td><b>Envoi du recommandé de dénonciation</b></td></tr>
<tr><td>AG d'automne</td><td>Assemblée</td><td>Vote du nouveau contrat, majorité de l'article 24</td></tr>
<tr><td>Décembre</td><td>Les deux prestataires</td><td>État des lieux, transfert des clés, reprise du personnel</td></tr>
<tr><td>1<sup>er</sup> janvier</td><td>Entrant</td><td>Première intervention</td></tr>
</tbody></table></div>

<p>L'ordre compte : on dénonce <em>avant</em> l'assemblée, pas après. Dénoncer sans avoir voté le remplaçant est inconfortable mais rattrapable ; voter un remplaçant sans avoir dénoncé à temps vous laisse avec deux contrats, dont un que vous payez pour rien.</p>

<p>Si l'assemblée ne peut pas se tenir à temps, la dénonciation reste la priorité : elle se révoque plus facilement qu'une reconduction ne s'annule. La suite du processus est décrite dans notre guide pour <a href="__CHANGER__">changer de prestataire de nettoyage</a>.</p>

<h2 id="erreurs">Ce qui fait déraper un contrat de copropriété</h2>

<p><strong>Le périmètre non écrit.</strong> « Entretien des parties communes » ne veut rien dire. Les caves, le local à poubelles, le parking, les vitrages de hall et la sortie des bacs doivent être nommés, ou ils ne seront pas faits.</p>

<p><strong>La sortie et la rentrée des bacs oubliées.</strong> C'est la première source de rappel à l'ordre en copropriété, et c'est presque toujours hors contrat. Précisez les jours, et qui agit en cas de jour férié.</p>

<p><strong>Les consommables non attribués.</strong> Ampoules, sacs, produits : qui fournit, qui stocke. À défaut, chacun attend l'autre.</p>

<p><strong>Aucun rituel de contrôle.</strong> Un contrat sans dispositif de suivi dérive au troisième mois, mécaniquement. Nous l'avons documenté dans notre article sur <a href="__QUAL__">la qualité qui baisse après trois mois</a>, et le dispositif à mettre en face est détaillé dans notre <a href="__CTRL__">grille de contrôle qualité d'un prestataire de nettoyage</a>.</p>

<p><strong>Le prix comparé hors périmètre.</strong> Deux devis ne se comparent que s'ils répondent à la même demande. Nos relevés de marché figurent dans l'article <a href="__PRIX__">prix du nettoyage</a>, et les dix critères qui séparent deux offres dans notre <a href="__HUB__">guide pour choisir une entreprise de nettoyage</a>. Pour nos prestations en immeuble, voyez notre pôle <a href="__HABITAT__">copropriété et habitat</a>.</p>
"""

A1_FAQ = [
 ("Qui signe le contrat de nettoyage d'une copropriété ?",
  "Le syndic signe, mais au nom du syndicat des copropriétaires et en exécution d'une décision d'assemblée générale. La loi du 10 juillet 1965 lui donne mission d'exécuter les décisions de l'assemblée, pas de choisir seul le prestataire. Un contrat signé sans mandat de l'assemblée est contestable."),
 ("Quelle majorité pour voter un contrat d'entretien en AG ?",
  "La majorité simple des voix exprimées des copropriétaires présents ou représentés, dite majorité de l'article 24, s'agissant d'un acte d'administration courante inscrit au budget prévisionnel. Le montant est voté avec le budget."),
 ("Comment rédiger un contrat de nettoyage de copropriété ?",
  "Quatre pages suffisent si elles sont précises : identification des parties, périmètre détaillé zone par zone avec fréquences, modalités d'exécution (horaires, accès, consommables, remplacement en cas d'absence), prix et révision, durée et préavis, dispositif de contrôle, et pièces de conformité à fournir annuellement."),
 ("Quelle est la durée d'un contrat de nettoyage de copropriété ?",
  "Un an avec tacite reconduction dans la très grande majorité des cas. Le préavis de dénonciation est fixé par le contrat, le plus souvent trois mois avant la date anniversaire, notifié par lettre recommandée avec accusé de réception."),
 ("La loi Chatel s'applique-t-elle à un syndicat de copropriétaires ?",
  "En principe non. La loi Chatel protège les consommateurs et les non-professionnels ; un syndicat de copropriétaires agit pour la gestion de l'immeuble. Aucun rappel d'échéance ne lui est dû, et son absence n'ouvre aucun droit de résiliation. La surveillance du calendrier incombe au syndic."),
 ("Quelle est la loi qui régit le nettoyage des parties communes ?",
  "La loi du 10 juillet 1965 sur le statut de la copropriété et son décret d'application du 17 mars 1967. Ils organisent la répartition des charges d'entretien, le rôle du syndic et les majorités de vote. Aucun texte n'impose une fréquence de nettoyage : elle relève du règlement de copropriété et de la décision d'assemblée."),
]

A1 = dict(
    slug="contrat-nettoyage-copropriete",
    date="2026-10-12T09:00:00",
    title="Contrat de nettoyage de copropriété : clauses, durée et vote en AG",
    seo_title="Contrat de nettoyage de copropriété : clauses, durée et vote | SPN NET",
    desc="Ce que doit contenir un contrat d'entretien de parties communes : clauses à exiger, durée et préavis, qui vote quoi en assemblée générale, et le rétroplanning à tenir.",
    hero_stats=[("Art. 24", "majorité du vote en AG"), ("3 mois", "préavis le plus courant"),
                ("10/07/1965", "la loi de référence")],
    body=A1_BODY, faq=A1_FAQ,
)

# ================================================== A2 — CONTRÔLE QUALITÉ ===

A2_BODY = """<p class="lead">Tout ce qui se publie sur le contrôle qualité en propreté est écrit pour les entreprises de nettoyage : des comparatifs de logiciels et des offres d'emploi. Voici la même chose vue du côté de celui qui paie — une grille à remplir, un score, et un seuil à partir duquel on agit.</p>

<div class="toc"><b>Au sommaire</b><ol>
<li><a href="#pourquoi">Pourquoi un contrôle noté, et pas une impression</a></li>
<li><a href="#grille">La grille de contrôle à remplir</a></li>
<li><a href="#seuil">Lire le score et fixer le seuil</a></li>
<li><a href="#rituel">Le rituel : qui, quand, combien de temps</a></li>
<li><a href="#apres">Ce qu'on fait d'un score qui baisse</a></li>
</ol></div>

<h2 id="pourquoi">Pourquoi un contrôle noté, et pas une impression</h2>

<p>« J'ai l'impression que c'est moins bien qu'avant » ne se défend pas. Face à un prestataire, c'est une opinion contre une autre, et la discussion tourne en rond jusqu'à ce que l'un des deux se lasse.</p>

<p>Un score mensuel change la nature de l'échange. Il transforme un ressenti en <strong>série de mesures</strong>, et une série se discute sur les faits : le poste « sanitaires » est passé de 2 à 1 sur les trois derniers relevés, voilà ce qu'on regarde. Le prestataire sérieux s'en saisit ; celui qui dérive n'a plus d'argument.</p>

<p>Le second effet est plus discret mais plus puissant : <strong>un contrôle annoncé et tenu modifie le comportement avant même d'être appliqué</strong>. C'est exactement le mécanisme décrit dans notre article sur <a href="__QUAL__">la qualité du nettoyage qui baisse après trois mois</a> — la dérive ne vient pas d'un manque de bonne volonté, mais de l'absence de retour.</p>

<h2 id="grille">La grille de contrôle à remplir</h2>

<p>Douze postes, notés de 0 à 2 : <strong>2</strong> conforme, <strong>1</strong> acceptable mais à reprendre, <strong>0</strong> non fait. Cochez les postes conformes ; ce qui reste décoché est votre constat. Comptez dix minutes, au même moment chaque mois.</p>

__GRILLE__

<p>Deux règles pour que la grille tienne dans le temps. Contrôlez <strong>toujours au même moment du cycle</strong> — le lendemain d'un passage, jamais la veille, sinon vous mesurez l'usure et non la prestation. Et <strong>faites signer</strong> par le responsable de secteur quand c'est possible : un relevé contradictoire pèse infiniment plus qu'un relevé unilatéral.</p>

<p>La grille se cale sur ce que le contrat prévoit, poste par poste. Si votre périmètre n'est pas écrit, commencez par là : notre <a href="__CDC__">cahier des charges de nettoyage</a> se remplit zone par zone et devient la référence du contrôle.</p>

<h2 id="seuil">Lire le score et fixer le seuil</h2>

<p>Douze postes à 2 points font 24. Le score brut compte moins que sa <strong>tendance</strong> : un 20 stable vaut mieux qu'un 23 qui descend depuis trois mois.</p>

<div class="tbl-wrap"><table class="tbl">
<caption>Lecture du score mensuel sur 24 points</caption>
<thead><tr><th>Score</th><th>Lecture</th><th>Ce que vous faites</th></tr></thead>
<tbody>
<tr><td><b>21 à 24</b></td><td>Prestation conforme</td><td>Rien. Vous classez le relevé.</td></tr>
<tr><td><b>17 à 20</b></td><td>Dérive naissante</td><td>Vous transmettez le relevé par courriel, sans commentaire. La trace suffit.</td></tr>
<tr><td><b>13 à 16</b></td><td>Écart installé</td><td>Réunion de recadrage, compte rendu écrit, plan d'action daté.</td></tr>
<tr><td><b>12 ou moins</b></td><td>Manquement caractérisé</td><td>Mise en demeure. Les pénalités du contrat s'appliquent.</td></tr>
</tbody></table></div>

<p>Le vrai seuil de décision n'est pas un chiffre isolé : c'est <strong>deux mois consécutifs sous 17</strong>. Un mauvais mois arrive — un arrêt maladie, un remplacement raté. Deux de suite après un signalement, c'est une organisation qui ne tient pas.</p>

<h2 id="rituel">Le rituel : qui, quand, combien de temps</h2>

<p>Un dispositif de contrôle ne survit que s'il coûte peu. Dix minutes par mois, une seule personne désignée, toujours la même : l'office manager pour des bureaux, un membre du conseil syndical pour un immeuble. La rotation des contrôleurs tue la comparabilité.</p>

<p>Trois documents suffisent : la grille remplie et datée, un cahier de liaison sur site pour les signalements du quotidien, et un point annuel qui reprend les douze relevés. Le reste est du confort.</p>

<p>Et il faut le <strong>dire au prestataire dès la signature</strong>. Un contrôle annoncé est accepté ; un contrôle découvert est vécu comme une inspection et braque l'encadrement. Les dix critères à instruire avant de signer, contrôle compris, sont réunis dans notre <a href="__HUB__">guide pour choisir une entreprise de nettoyage</a>.</p>

<h2 id="apres">Ce qu'on fait d'un score qui baisse</h2>

<p>La gradation est toujours la même, et elle compte juridiquement : un juge regarde si vous avez laissé au prestataire une chance de corriger. Signalement écrit, puis réunion de recadrage avec plan d'action daté, puis mise en demeure, puis résolution. Jamais l'inverse, jamais de saut d'étape.</p>

<p>Chaque relevé transmis est une pièce. Douze relevés mensuels forment un dossier que personne ne conteste — c'est la différence entre « ça ne va pas » et une inexécution démontrée. La procédure complète, avec le modèle de mise en demeure, est dans notre page sur <a href="__LITIGE__">le prestataire qui ne respecte pas le contrat</a>.</p>

<p>Si la décision de changer est prise, la sortie obéit à son propre calendrier : voyez comment <a href="__RESIL__">résilier un contrat de nettoyage</a> à sa date anniversaire. Et pour un immeuble, le contrat se vote en assemblée — les délais sont détaillés dans notre page sur le <a href="__CONTRAT__">contrat de nettoyage de copropriété</a>.</p>
"""

A2_FAQ = [
 ("Comment contrôler la qualité d'un prestataire de nettoyage ?",
  "Avec une grille notée, remplie au même moment chaque mois, poste par poste, sur la base de ce que le contrat prévoit. Douze postes notés de 0 à 2 donnent un score sur 24 dont on suit la tendance. Le relevé est daté, si possible signé par le responsable de secteur, et transmis le jour même : c'est cette transmission qui lui donne sa valeur."),
 ("Quels indicateurs suivre pour un contrat de nettoyage ?",
  "Les postes vérifiables à l'œil : corbeilles, sanitaires et réassort, sols, points de contact, vitrages intérieurs, parties communes, respect du planning et des horaires, stabilité de l'agent, fourniture des consommables, remplacement en cas d'absence. Évitez les indicateurs déclaratifs fournis par le prestataire lui-même."),
 ("À quelle fréquence contrôler son prestataire de nettoyage ?",
  "Une fois par mois suffit, à condition que ce soit toujours au même moment du cycle et par la même personne. Un contrôle hebdomadaire s'essouffle en six semaines ; un contrôle annuel ne détecte la dérive qu'une fois installée. Le cahier de liaison prend le relais au quotidien."),
 ("Que faire si la qualité du nettoyage baisse ?",
  "Respecter la gradation : signalement écrit avec le relevé joint, puis réunion de recadrage avec plan d'action daté, puis mise en demeure par recommandé si le plan échoue. Le seuil de décision utile est deux mois consécutifs sous 17 sur 24 : un mauvais mois arrive, deux de suite après signalement traduisent une organisation défaillante."),
 ("Faut-il un logiciel de contrôle qualité propreté ?",
  "Pas côté client. Les logiciels du marché sont conçus pour les entreprises de propreté, qui pilotent des dizaines de sites. Pour contrôler un prestataire sur un ou deux sites, une grille papier ou un tableur datés et transmis font exactement le même travail, et restent opposables."),
 ("Qui doit faire le contrôle qualité du nettoyage ?",
  "Le client, pas le prestataire. Un autocontrôle fourni par l'entreprise de nettoyage a sa valeur, mais il ne remplace pas le vôtre. Désignez une personne unique et stable : office manager pour des bureaux, membre du conseil syndical pour une copropriété. La rotation des contrôleurs rend les relevés incomparables."),
]

A2 = dict(
    slug="controle-qualite-prestataire-nettoyage",
    date="2026-10-12T09:30:00",
    title="Contrôle qualité d'un prestataire de nettoyage : la grille à remplir",
    seo_title="Contrôle qualité prestataire nettoyage : grille et score | SPN NET",
    desc="La grille de contrôle qualité d'un prestataire de nettoyage, côté client : douze postes notés, un score sur 24, un seuil de décision et le rituel qui tient dans le temps.",
    hero_stats=[("12 postes", "notés de 0 à 2"), ("2 mois", "sous 17 = on agit"),
                ("10 min", "par mois, une personne")],
    body=A2_BODY, faq=A2_FAQ,
)

ARTICLES = [A1, A2]

BLOG_CARDS_OCT = [
    ("contrat-nettoyage-copropriete", "Copropriété",
     "Contrat de nettoyage de copropriété",
     "Clauses à exiger, durée, préavis et rétroplanning du vote en assemblée générale."),
    ("controle-qualite-prestataire-nettoyage", "Qualité",
     "Contrôle qualité d'un prestataire",
     "La grille à remplir côté client, le score sur 24 et le seuil à partir duquel on agit."),
]

CLAUSES = [
 ("Identification des parties", "Le syndicat des copropriétaires comme client, représenté par le syndic, et non le syndic en son nom propre.", None),
 ("Périmètre zone par zone", "Halls, escaliers, paliers, ascenseurs, caves, local à poubelles, parking, abords. Ce qui n'est pas nommé ne sera pas fait.", None),
 ("Fréquences datées", "Quotidien, trois fois par semaine, hebdomadaire. Jamais « régulièrement ».", None),
 ("Sortie et rentrée des bacs", "Jours précis, et qui agit en cas de jour férié. Première source de litige en copropriété.", None),
 ("Prestations périodiques chiffrées à part", "Vitrerie, remise en état des sols, nettoyage des luminaires. Deux à quatre passages par an, hors forfait mensuel.", None),
 ("Horaires et accès", "Plages d'intervention, badges, codes, local technique mis à disposition.", None),
 ("Fourniture des consommables", "Ampoules, sacs, produits : qui fournit, qui stocke, qui réassort.", None),
 ("Continuité de service", "Remplacement en cas d'absence : systématique ou non, sous quel délai, avec quelle information au conseil syndical.", None),
 ("Critères de qualité vérifiables", "Des phrases auxquelles on répond par oui ou non, et le rythme des contrôles contradictoires.", None),
 ("Prix, révision et pénalités", "Montant annuel, indice et date de révision, pénalités applicables en cas de manquement constaté.", None),
 ("Durée, reconduction et préavis", "Durée ferme, tacite reconduction ou non, durée du préavis et forme de la dénonciation.", None),
 ("Pièces de conformité annuelles", "Attestation de vigilance URSSAF de moins de six mois, attestation d'assurance, liste nominative des salariés étrangers.",
  "Art. L8222-1 c. travail"),
]

GRILLE = [
 ("Halls et parties d'accueil", "Sols, vitrages, traces de mains sur portes et interphone.", None),
 ("Escaliers et paliers", "Marches, contremarches, rampes, plinthes.", None),
 ("Sanitaires", "Nettoyage complet, désinfection, réassort papier et savon à l'issue du passage.", None),
 ("Corbeilles et sacs", "Vidées et sacs remplacés dans toutes les zones prévues.", None),
 ("Sols", "Aspiration ou lavage selon le revêtement, sans salissure visible en lumière rasante.", None),
 ("Points de contact", "Poignées, interrupteurs, boutons d'ascenseur, rampes.", None),
 ("Vitrages intérieurs", "Cloisons et portes vitrées, à hauteur d'homme, sans trace.", None),
 ("Local à poubelles", "Sol lavé, bacs rentrés, absence d'odeur.", None),
 ("Respect du planning", "Passage effectué aux jours prévus. Comparez au contrat, pas à votre souvenir.", None),
 ("Respect des horaires", "Intervention dans la plage prévue, hors présence si c'est ce qui est écrit.", None),
 ("Stabilité de l'agent", "Agent habituel présent. Une rotation permanente est un signal, et souvent la cause du reste.", None),
 ("Consommables fournis", "Conformément à ce que le contrat met à la charge du prestataire.", None),
]

LINKS = {"__COPRO__": COPRO, "__HABITAT__": HABITAT, "__PRIX__": PRIX, "__CDC__": CDC,
         "__QUAL__": QUAL, "__LITIGE__": LITIGE, "__RESIL__": RESIL, "__HUB__": HUB,
         "__CHANGER__": CHANGER, "__CTRL__": CTRL, "__CONTRAT__": CONTRAT}

MODULES = {
 "__CLAUSES__": lambda: nb.checklist(
     "Les clauses à exiger dans le contrat",
     "Cochez ce que vous voulez y voir figurer. Ce qui reste décoché est à ajouter avant signature.",
     CLAUSES, nb.IC_BUILD),
 "__GRILLE__": lambda: nb.checklist(
     "Votre grille de contrôle mensuelle",
     "Douze postes. Cochez les postes conformes : ce qui reste décoché est votre constat. "
     "Datez, faites signer si possible, transmettez le jour même.",
     GRILLE),
}


def resolve(a):
    b = a["body"]
    for k, v in LINKS.items():
        b = b.replace(k, v)
    for k, f in MODULES.items():
        if k in b:
            b = b.replace(k, f())
    left = re.findall(r"__[A-Z0-9_]+__", b)
    if left:
        raise SystemExit(f"{a['slug']} : jetons non resolus {set(left)}")
    o = dict(a); o["body"] = b
    return o


def main():
    import make_article as ma
    import make_septembre as msept
    ma.TAGS.update({c[0]: c[1] for c in BLOG_CARDS_OCT})
    dry = "--dry" in sys.argv
    for a in ARTICLES:
        r = resolve(a)
        html = ma.build_article(r)
        # NB_CSS est du CSS brut : il se pose DEDANS la balise style.
        if "</style>" in html:
            html = html.replace("</style>", nb.NB_CSS + "</style>", 1)
        else:
            html = "<style>" + nb.NB_CSS + "</style>" + html
        html = html.rstrip()
        html = html[: html.rfind("</div>")] + nb.NB_JS + html[html.rfind("</div>"):]
        open(os.path.join(os.path.dirname(__file__), f"article-{a['slug']}.html"), "w",
             encoding="utf-8").write(html)
        n = len(re.findall(r'<a\b[^>]*href="https://spn-net\.fr/', html))
        print(f"  {a['slug']:42} {len(html):7} o · {n} liens internes" + ("  [simulation]" if dry else ""))
        if not dry:
            print("   ", msept.deploy(r, html))


if __name__ == "__main__":
    main()
