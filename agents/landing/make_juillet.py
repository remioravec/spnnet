#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les 3 contenus du calendrier de juillet 2026 (SPN NET).

Process /operationnel-contenu — relevés SERP live du 28/08/2026 (DataForSEO,
fr/France, depth 10). Chaque article porte les modules d'attention choisis DANS
le relevé, jamais par goût :

  13/07 · nettoyage copropriété
      SERP : AIO rang 1 + PAA rang 3 (9 questions, dont 5 sur le cadre légal).
      Un seul du top 5 donne un chiffre (lea-syndic, 150–350 € TTC/mois).
      → réponse encadrée + CALCULATEUR budget copro + tableau « qui décide quoi »
        + FAQ reprenant les questions PAA mot pour mot.

  20/07 · prix du nettoyage de bureaux à Paris
      SERP : AIO rang 1 + PAA rang 3 (9 questions, 5 sur le prix). Requête à
      variable, aucun outil dans le top 5, aucun résultat ne chiffre le coût
      AU POSTE de travail.
      → réponse encadrée + CALCULATEUR 3 unités (mois / m² / poste) + grille
        triable sourcée + FAQ PAA.

  27/07 · travail dissimulé
      SERP : AIO rang 1, france-clean 1er (15/08/2026), PAA rang 4. Le top 5
      est éclaté entre juridique généraliste et nettoyage ; personne ne livre
      de checklist opérationnelle des documents à exiger.
      → réponse encadrée (5 000 € HT / 6 mois) + CHECKLIST cochable des pièces
        + tableau des sanctions chiffrées + FAQ PAA.

Aucune offre ni tarif SPN inventé : les fourchettes sont des relevés de marché
datés et sourcés, signalés comme tels dans chaque module.

Usage : python3 agents/landing/make_juillet.py
"""
from __future__ import annotations

import os
import sys
import datetime

import requests

sys.path.insert(0, os.path.dirname(__file__))
import navboost as nb  # noqa: E402

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
POSTS = "https://spn-net.fr/wp-json/wp/v2/posts"
PAGES = "https://spn-net.fr/wp-json/wp/v2/pages"


# ============================================================ A1 — COPRO ====
A1_BODY = """<p class="lead">Halls, escaliers, local à poubelles : l'entretien des parties communes est la première chose que voient les résidents — et la ligne de charges la plus commentée en assemblée générale. Qui doit l'organiser, ce que dit la loi, et combien ça coûte réellement selon la taille de l'immeuble.</p>

<div class="toc"><b>Au sommaire</b><ol>
<li><a href="#loi">Ce que la loi impose vraiment</a></li>
<li><a href="#qui">Qui décide quoi : syndic, AG, copropriétaires</a></li>
<li><a href="#budget">Combien coûte le nettoyage d'une copropriété</a></li>
<li><a href="#perimetre">Le périmètre à écrire noir sur blanc</a></li>
<li><a href="#gardien">Gardien ou prestataire : comment trancher</a></li>
<li><a href="#choisir">Choisir son prestataire sans se tromper</a></li>
</ol></div>

""" + nb.answer(
    "La réponse en une phrase",
    "Le <strong>nettoyage des parties communes est une obligation du syndicat des copropriétaires</strong>, "
    "mise en œuvre par le syndic au titre de l'entretien de l'immeuble (loi n° 65-557 du 10 juillet 1965, "
    "article 18) et financée par le budget prévisionnel voté en assemblée générale. "
    "Budget observé : <strong>150 à 350 € TTC par mois</strong> pour une petite copropriété avec un passage "
    "hebdomadaire.",
    "Relevé du 28 août 2026 · source du chiffre : lea-syndic.fr, publication du 13 juin 2026") + """

<h2 id="loi">Ce que la loi impose vraiment</h2>
<p>Contrairement à une idée répandue, aucun texte ne fixe une fréquence de nettoyage obligatoire dans un immeuble d'habitation. Ce que la loi impose, c'est un <strong>résultat</strong> : la conservation de l'immeuble et l'entretien des parties communes.</p>
<div class="twrap rv"><table class="art-table">
<thead><tr><th>Texte</th><th>Ce qu'il dit</th><th>Ce que ça implique</th></tr></thead>
<tbody>
<tr><td>Loi du 10 juillet 1965, art. 14</td><td>Le syndicat des copropriétaires a pour objet la conservation de l'immeuble et l'administration des parties communes.</td><td>L'entretien n'est pas optionnel : c'est l'objet même du syndicat.</td></tr>
<tr><td>Loi du 10 juillet 1965, art. 18</td><td>Le syndic administre l'immeuble, pourvoit à sa conservation, à sa garde et à son entretien.</td><td>C'est au syndic d'organiser la prestation et de la faire exécuter.</td></tr>
<tr><td>Règlement de copropriété</td><td>Définit les parties communes et, souvent, les modalités d'entretien.</td><td>C'est lui qu'on lit en premier : le périmètre s'y trouve.</td></tr>
<tr><td>Code de la santé publique (RSD)</td><td>Le règlement sanitaire départemental impose la salubrité des locaux et la propreté des locaux à déchets.</td><td>Un local poubelles insalubre engage la responsabilité du syndicat.</td></tr>
</tbody></table></div>
<p>Autrement dit : la fréquence se décide, elle ne se subit pas. Une copropriété de six lots sans ascenseur n'a pas les mêmes besoins qu'un immeuble de cinquante lots avec parking souterrain — et c'est à l'assemblée générale de fixer le curseur.</p>

<h2 id="qui">Qui décide quoi : syndic, AG, copropriétaires</h2>
<p>C'est la source de la moitié des malentendus en AG. Trois niveaux, trois rôles distincts :</p>
<div class="twrap rv"><table class="art-table">
<thead><tr><th>Acteur</th><th>Son rôle sur le nettoyage</th><th>Ce qu'il ne peut pas faire seul</th></tr></thead>
<tbody>
<tr><td><b>L'assemblée générale</b></td><td>Vote le budget prévisionnel, qui contient la ligne « entretien des parties communes » (majorité de l'article 24).</td><td>Gérer le quotidien du prestataire.</td></tr>
<tr><td><b>Le syndic</b></td><td>Met en concurrence, signe le contrat dans la limite du budget voté, contrôle l'exécution et alerte en cas de dérive.</td><td>Engager une dépense hors budget sans vote.</td></tr>
<tr><td><b>Le conseil syndical</b></td><td>Assiste et contrôle le syndic, donne son avis sur les devis, remonte les manquements constatés.</td><td>Décider seul du choix du prestataire.</td></tr>
<tr><td><b>Le copropriétaire</b></td><td>Signale les manquements au syndic ou au conseil syndical.</td><td>Donner des consignes directes aux agents.</td></tr>
</tbody></table></div>
<div class="art-note rv"><b>Le réflexe qui évite les conflits :</b> un copropriétaire mécontent qui interpelle directement l'agent de nettoyage n'obtient rien de durable et met l'agent en porte-à-faux. Le circuit qui fonctionne est écrit : constat daté → conseil syndical ou syndic → point de suivi avec le prestataire.</div>

<h2 id="budget">Combien coûte le nettoyage d'une copropriété</h2>
<p>En copropriété, le prix ne se lit pas au mètre carré comme en bureaux : il se calcule sur le <strong>nombre d'étages à traiter</strong> (donc de cages d'escalier), le <strong>nombre de lots</strong> (qui détermine le volume de déchets et l'usage des communs) et la <strong>fréquence</strong> des passages.</p>

""" + nb.calc_copro() + """

<p>Trois éléments font monter la facture au-delà de ces fourchettes, et ils sont presque toujours les mêmes : la <b>sortie et rentrée des conteneurs</b> (une prestation à part entière, souvent quotidienne), le <b>nettoyage du parking souterrain</b> (surface importante, matériel spécifique) et la <b>vitrerie des halls</b> (chiffrée séparément, généralement en trimestriel).</p>

<h2 id="perimetre">Le périmètre à écrire noir sur blanc</h2>
<p>La quasi-totalité des litiges d'entretien en copropriété vient d'un périmètre flou, pas d'un manque de sérieux. Ce qui n'est pas écrit n'est pas dû. Un cahier des charges utile précise, espace par espace, la tâche, sa fréquence et le résultat attendu.</p>
<div class="twrap rv"><table class="art-table">
<thead><tr><th>Espace</th><th>Prestation type</th><th>Fréquence courante</th></tr></thead>
<tbody>
<tr><td>Hall d'entrée</td><td>Lavage du sol, dépoussiérage, traces sur les portes vitrées, boîtes aux lettres</td><td>2 à 5 × / semaine</td></tr>
<tr><td>Escaliers &amp; paliers</td><td>Balayage humide, lavage, rampes et interrupteurs</td><td>1 à 3 × / semaine</td></tr>
<tr><td>Ascenseur</td><td>Sol, parois, miroir, boutons d'appel</td><td>2 à 5 × / semaine</td></tr>
<tr><td>Local à poubelles</td><td>Lavage, désinfection, sortie et rentrée des conteneurs</td><td>Quotidien ou selon collecte</td></tr>
<tr><td>Parking &amp; caves</td><td>Balayage mécanique, désinfection des points sensibles</td><td>Mensuel à trimestriel</td></tr>
<tr><td>Abords &amp; cour</td><td>Ramassage, désherbage manuel, propreté des grilles</td><td>Hebdomadaire</td></tr>
<tr><td>Vitrerie des communs</td><td>Portes vitrées, imposte, fenêtres de cage</td><td>Trimestriel</td></tr>
</tbody></table></div>

<h2 id="gardien">Gardien ou prestataire : comment trancher</h2>
<p>Beaucoup de copropriétés se posent la question au moment d'un départ à la retraite. Les deux modèles ne s'opposent pas sur le prix seul — ils s'opposent sur la nature du service rendu.</p>
<div class="twrap rv"><table class="art-table">
<thead><tr><th>Critère</th><th>Gardien salarié du syndicat</th><th>Entreprise de propreté</th></tr></thead>
<tbody>
<tr><td>Présence</td><td>Quotidienne, avec une fonction de surveillance et de lien social</td><td>Sur créneaux définis au contrat</td></tr>
<tr><td>Gestion</td><td>Le syndicat devient employeur : paie, congés, remplacements, conflits</td><td>Le prestataire gère ses équipes et leurs remplacements</td></tr>
<tr><td>Continuité</td><td>À organiser en cas d'arrêt ou de congés</td><td>Contractuelle : le remplacement est dû</td></tr>
<tr><td>Souplesse</td><td>Faible : toute évolution passe par le contrat de travail</td><td>La fréquence et le périmètre s'ajustent par avenant</td></tr>
<tr><td>Décision</td><td>Créer ou supprimer un poste est une décision lourde en AG</td><td>Relève du budget prévisionnel voté à l'article 24</td></tr>
</tbody></table></div>
<div class="art-note rv"><b>À vérifier avant tout arbitrage :</b> la suppression d'un poste de gardien, la transformation ou la vente de la loge ne se votent pas à la même majorité que le choix d'un prestataire. C'est une décision à instruire avec votre syndic et à faire figurer distinctement à l'ordre du jour — pas un simple arbitrage budgétaire.</div>

<h2 id="choisir">Choisir son prestataire sans se tromper</h2>
<p>À budget comparable, ce sont toujours les mêmes points qui séparent un contrat qui tient d'un contrat qui s'essouffle au bout de trois mois :</p>
<ul>
<li><strong>La stabilité des agents.</strong> Le même agent qui connaît l'immeuble, ses accès et ses habitants vaut mieux qu'une rotation permanente.</li>
<li><strong>Un interlocuteur joignable</strong>, qui répond au syndic <em>et</em> au conseil syndical sans passer par un standard.</li>
<li><strong>Un contrôle qualité tracé</strong> : des visites de site consignées, pas une promesse orale.</li>
<li><strong>La conformité sociale</strong> — attestation de vigilance URSSAF à jour, agents déclarés. C'est une obligation légale pour le syndicat dès 5 000 € HT de contrat : nous l'avons détaillée dans notre guide sur <a href="https://spn-net.fr/travail-dissimule-entreprise-nettoyage/">la vérification d'une entreprise de nettoyage</a>.</li>
<li><strong>Pas de sous-traitance en cascade</strong> : demandez qui exécute réellement la prestation.</li>
</ul>
<p>SPN NET entretient les parties communes d'immeubles à Paris et en Île-de-France depuis 30 ans, avec des équipes fidélisées et un interlocuteur dédié pour votre syndic. Découvrez notre <a href="https://spn-net.fr/copropriete-et-habitat/">offre nettoyage de copropriété et d'habitat</a>.</p>

<h2 id="aller-plus-loin">Aller plus loin</h2>
<div class="art-links rv">
<a href="https://spn-net.fr/copropriete-et-habitat/">Nettoyage de copropriété &amp; habitat<span>Notre offre pour les syndics et conseils syndicaux</span></a>
<a href="https://spn-net.fr/travail-dissimule-entreprise-nettoyage/">Vérifier que votre prestataire est en règle<span>Obligation de vigilance : la checklist des documents</span></a>
<a href="https://spn-net.fr/changer-de-prestataire-nettoyage/">Changer de prestataire<span>Résiliation, reprise des agents, transition sans coupure</span></a>
<a href="https://spn-net.fr/contact/">Demander un devis<span>Réponse sous 24 h, après visite de l'immeuble</span></a>
</div>"""

A1 = dict(
    slug="nettoyage-copropriete",
    date="2026-07-13T09:00:00",
    title="Nettoyage de copropriété : obligations, budget et organisation",
    seo_title="Nettoyage de copropriété : obligations, tarifs et organisation | SPN NET",
    desc="Nettoyage de copropriété : ce que la loi impose au syndic, qui décide quoi en AG, "
         "le budget réel par lot et par étage (calculateur) et le périmètre à écrire au contrat.",
    body=A1_BODY,
    faq=[
        ("Quel est le tarif moyen pour le nettoyage d'une copropriété ?",
         "Pour une petite copropriété avec un passage hebdomadaire, le budget observé sur le marché est de 150 à 350 € TTC par mois (relevé de juin 2026). Le montant dépend surtout du nombre d'étages, du nombre de lots et de la fréquence : notre calculateur donne une fourchette au mois et par lot."),
        ("Qui doit nettoyer les parties communes d'un immeuble ?",
         "L'entretien des parties communes incombe au syndicat des copropriétaires. Le syndic l'organise concrètement au titre de l'article 18 de la loi du 10 juillet 1965, soit en employant un gardien, soit en confiant la prestation à une entreprise de propreté. Les locataires n'ont aucune obligation d'entretenir les communs."),
        ("Quelle est l'obligation d'entretien d'un immeuble en copropriété ?",
         "La loi impose un résultat — la conservation de l'immeuble et l'administration des parties communes (article 14 de la loi du 10 juillet 1965) — mais ne fixe aucune fréquence de nettoyage. C'est l'assemblée générale qui arbitre le niveau de service en votant le budget prévisionnel."),
        ("Le nettoyage se vote-t-il en assemblée générale ?",
         "Oui : la ligne « entretien des parties communes » figure au budget prévisionnel, voté à la majorité de l'article 24. Le syndic met ensuite en concurrence et signe le contrat dans la limite du budget voté."),
        ("À quelle fréquence faut-il nettoyer les parties communes ?",
         "Il n'existe pas de fréquence légale. En pratique, un hall d'entrée se traite 2 à 5 fois par semaine, les escaliers 1 à 3 fois, et le local à poubelles quotidiennement ou au rythme de la collecte. La fréquence se fixe selon le nombre de lots et le passage réel."),
        ("Faut-il choisir un gardien ou une entreprise de nettoyage ?",
         "Un gardien apporte une présence quotidienne et une fonction de surveillance, mais fait du syndicat un employeur (paie, congés, remplacements). Une entreprise de propreté gère ses équipes, contractualise la continuité de service et s'ajuste par avenant. La suppression d'un poste de gardien est une décision distincte, à instruire avec le syndic."),
        ("Que faire si le nettoyage des parties communes est mal fait ?",
         "Consignez des constats datés (photos, dates, espaces concernés), transmettez-les au syndic ou au conseil syndical, et demandez un point de suivi avec le prestataire en s'appuyant sur le cahier des charges. Si le manquement persiste malgré les relances, le changement de prestataire s'organise sans coupure de service."),
    ],
    hero_stats=[("150–350 €", "TTC/mois, petite copro"), ("Art. 18", "loi du 10/07/1965"), ("Art. 24", "vote du budget")],
)


# ============================================================= A2 — PRIX ====
A2_BODY = """<p class="lead">C'est la première question que pose tout dirigeant avant de lancer une consultation — et la seule à laquelle les sites du secteur répondent par « ça dépend ». Voici les fourchettes réellement pratiquées à Paris, exprimées dans les trois unités qui servent à décider : au mois, au mètre carré et au poste de travail.</p>

<div class="toc"><b>Au sommaire</b><ol>
<li><a href="#calculateur">Estimez votre budget en 10 secondes</a></li>
<li><a href="#m2">Le prix au mètre carré</a></li>
<li><a href="#heure">Le prix à l'heure</a></li>
<li><a href="#poste">Le prix au poste de travail</a></li>
<li><a href="#variables">Les 6 variables qui font bouger le devis</a></li>
<li><a href="#lire">Lire un devis de nettoyage sans se faire piéger</a></li>
</ol></div>

""" + nb.answer(
    "La réponse en une phrase",
    "À Paris, le nettoyage de bureaux se situe entre <strong>20 et 35 € HT de l'heure</strong>, soit "
    "<strong>1,50 à 3,90 € HT par m² et par mois</strong> pour un entretien courant de 2 à 3 passages "
    "hebdomadaires — soit environ <strong>25 à 45 € HT par poste de travail et par mois</strong>.",
    "Fourchettes relevées le 28 août 2026 sur les prestataires positionnés à Paris "
    "(travaux.com, plateya.fr, galognese.fr, menageparfait.fr, oxynet.fr, hoper.io)") + """

<h2 id="calculateur">Estimez votre budget en 10 secondes</h2>
<p>Renseignez votre surface, votre fréquence et votre nombre de postes : vous obtenez la fourchette de marché dans les trois unités, plus le coût par passage.</p>

""" + nb.calc_bureaux() + """

<h2 id="m2">Le prix au mètre carré</h2>
<p>C'est l'unité la plus utilisée dans les appels d'offres, parce qu'elle permet de comparer deux devis sur des surfaces différentes. Elle a un défaut : elle écrase les écarts de configuration. Un plateau ouvert de 300 m² se nettoie plus vite au m² qu'un étage de bureaux cloisonnés de même surface.</p>
<div class="twrap rv"><table class="art-table">
<thead><tr><th>Type de prestation</th><th>Prix observé au m²</th><th>Base</th></tr></thead>
<tbody>
<tr><td>Entretien courant de bureaux</td><td>1,50 à 2,50 € / m²</td><td>Mensuel, quotidien ou hebdomadaire</td></tr>
<tr><td>Nettoyage ponctuel (grand ménage)</td><td>À partir de 2,00 € / m²</td><td>À l'intervention</td></tr>
<tr><td>Vitrerie</td><td>3 à 7 € / m² de vitrage</td><td>À l'intervention</td></tr>
<tr><td>Remise en état après travaux</td><td>30 à 45 € / heure</td><td>Chiffrée au temps passé</td></tr>
</tbody></table></div>
<p class="nb-src">Sources : galognese.fr (1,50–2,50 €/m²), travaux.com (vitres 3–7 €/m², après travaux 30–45 €/h) — relevé du 28/08/2026.</p>

<h2 id="heure">Le prix à l'heure</h2>
<p>C'est l'unité de référence du secteur, celle sur laquelle le prestataire construit son devis avant de le convertir en forfait mensuel. À Paris, les relevés convergent nettement.</p>
<div class="twrap rv"><table class="art-table nb-sort">
<thead><tr><th>Source relevée</th><th data-s="num">Taux horaire HT</th><th>Périmètre annoncé</th></tr></thead>
<tbody>
<tr><td>travaux.com</td><td data-v="20">20 à 35 €</td><td>Nettoyage de bureaux</td></tr>
<tr><td>plateya.fr</td><td data-v="20">20 à 35 €</td><td>Nettoyage standard de bureaux</td></tr>
<tr><td>entreprisenettoyageparis.fr</td><td data-v="20">20 à 70 €</td><td>Locaux professionnels à Paris</td></tr>
<tr><td>menageparfait.fr</td><td data-v="26">26 €</td><td>Bureaux, Paris</td></tr>
<tr><td>hoper.io</td><td data-v="20">dès 20 €</td><td>Minimum 1 h 30 par semaine</td></tr>
<tr><td>plateya.fr (locaux sensibles)</td><td data-v="60">jusqu'à 60 €</td><td>Laboratoires, santé, restauration</td></tr>
</tbody></table></div>
<p class="nb-src">Tableau triable — cliquez sur une colonne. Relevé du 28 août 2026.</p>
<div class="art-note rv"><b>Le piège du taux horaire seul :</b> un prestataire à 22 € HT/h qui prévoit 2 heures là où il en faut 3 revient plus cher qu'un prestataire à 28 € HT/h correctement dimensionné — et vous récupérez des sanitaires mal faits. Comparez toujours le <b>temps prévu</b> autant que le taux.</div>

<h2 id="poste">Le prix au poste de travail</h2>
<p>C'est l'unité que presque personne ne publie, et pourtant la seule qui parle à un directeur financier : elle se compare directement aux autres coûts d'occupation, par salarié et par mois.</p>
<p>La conversion est simple. En bureaux, la <strong>norme AFNOR NF X35-102</strong> retient un minimum de <strong>10 m² par personne</strong> ; c'est le ratio couramment utilisé pour dimensionner un plateau. Avec les fourchettes ci-dessus, on obtient :</p>
<div class="twrap rv"><table class="art-table">
<thead><tr><th>Fréquence</th><th>Coût par poste / mois</th><th>Exemple : 15 postes (150 m²)</th></tr></thead>
<tbody>
<tr><td>1 passage / semaine</td><td>10 à 18 € HT</td><td>150 à 270 € HT / mois</td></tr>
<tr><td>2 passages / semaine</td><td>16 à 29 € HT</td><td>240 à 435 € HT / mois</td></tr>
<tr><td>3 passages / semaine</td><td>22 à 39 € HT</td><td>330 à 585 € HT / mois</td></tr>
<tr><td>5 jours sur 7</td><td>35 à 65 € HT</td><td>525 à 975 € HT / mois</td></tr>
</tbody></table></div>
<p>Ramené à l'échelle d'un salarié, l'entretien courant d'un bureau représente donc l'équivalent de quelques euros par jour travaillé — un ordre de grandeur utile quand la ligne « propreté » passe en arbitrage budgétaire.</p>

<h2 id="variables">Les 6 variables qui font bouger le devis</h2>
<p>Deux locaux de surface identique n'aboutissent jamais au même montant. Six éléments expliquent l'essentiel de l'écart :</p>
<div class="art-steps rv">
<div class="stp"><b>La nature des sols</b><span>Une moquette s'aspire, un marbre se lave et se cristallise, un vinyle se décape.</span></div>
<div class="stp"><b>La surface vitrée</b><span>Cloisons, verrières et façades relèvent d'une prestation distincte, chiffrée au m² de vitrage.</span></div>
<div class="stp"><b>Les horaires</b><span>Avant 9 h, après 18 h ou le week-end : l'organisation et la majoration diffèrent.</span></div>
<div class="stp"><b>Les consommables</b><span>Papier, savon, sacs : intégrés au forfait ou facturés à part, au choix.</span></div>
<div class="stp"><b>L'accès aux locaux</b><span>Étage sans ascenseur, contrôle d'accès, local technique éloigné : des minutes à chaque passage.</span></div>
<div class="stp"><b>La densité d'occupation</b><span>200 m² occupés par 40 personnes ne se salissent pas comme les mêmes 200 m² à 12.</span></div>
</div>

<h2 id="lire">Lire un devis de nettoyage sans se faire piéger</h2>
<p>Un devis de propreté se juge sur cinq lignes, et rarement sur le total :</p>
<ul>
<li><strong>Le temps d'intervention prévu</strong>, en heures par passage. C'est la donnée qui conditionne la qualité — un devis qui ne l'indique pas est incomparable.</li>
<li><strong>Le périmètre exact</strong> : quels espaces, quelles tâches, avec quelles exclusions écrites.</li>
<li><strong>La fréquence par espace</strong>, pas une fréquence globale : les sanitaires ne suivent pas le rythme des bureaux.</li>
<li><strong>Ce qui est en supplément</strong> : vitrerie, décapage, cristallisation, remise en état, consommables.</li>
<li><strong>La clause de révision de prix</strong> et la durée d'engagement.</li>
</ul>
<p>Un devis clair sur ces cinq points vaut mieux qu'un devis moins cher de 8 % dont vous découvrirez le périmètre réel au troisième mois. Nous détaillons ailleurs pourquoi <a href="https://spn-net.fr/qualite-nettoyage-baisse-apres-3-mois/">la qualité s'essouffle souvent passé trois mois</a> — le flou contractuel en est la première cause.</p>
<p>Pour un chiffrage sur vos locaux réels, SPN NET se déplace et vous transmet une proposition détaillée sous 24 heures ouvrées. Voir notre <a href="https://spn-net.fr/tertiaire/">offre de nettoyage de bureaux à Paris et en Île-de-France</a>.</p>

<h2 id="aller-plus-loin">Aller plus loin</h2>
<div class="art-links rv">
<a href="https://spn-net.fr/tertiaire/">Nettoyage de bureaux à Paris<span>Notre offre tertiaire, tous secteurs</span></a>
<a href="https://spn-net.fr/qualite-nettoyage-baisse-apres-3-mois/">Quand la qualité baisse après 3 mois<span>Les 4 causes réelles et la grille de contrôle</span></a>
<a href="https://spn-net.fr/changer-de-prestataire-nettoyage/">Changer de prestataire<span>Sans coupure, reprise des agents incluse</span></a>
<a href="https://spn-net.fr/contact/">Demander un devis chiffré<span>Visite sur site, réponse sous 24 h</span></a>
</div>"""

A2 = dict(
    slug="prix-nettoyage-bureaux-paris",
    date="2026-07-20T09:00:00",
    title="Combien coûte le nettoyage de bureaux à Paris ? Les vraies fourchettes au m² et au poste",
    seo_title="Prix nettoyage bureaux Paris : tarifs au m², à l'heure et au poste | SPN NET",
    desc="Prix du nettoyage de bureaux à Paris : 20 à 35 € HT/h, 1,50 à 3,90 € HT/m²/mois. "
         "Calculateur, grille par surface et fréquence, coût par poste de travail. Relevé daté.",
    body=A2_BODY,
    faq=[
        ("Quel est le prix moyen d'un nettoyage de bureau par m² ?",
         "Pour un entretien courant, les prix relevés à Paris se situent entre 1,50 et 2,50 € HT par m² et par mois en fréquence standard, et montent jusqu'à 3,90 € HT/m²/mois pour trois passages hebdomadaires. La vitrerie se chiffre à part, entre 3 et 7 € HT du m² de vitrage."),
        ("Quel est le taux horaire moyen pour le nettoyage d'un bureau ?",
         "Le taux horaire relevé à Paris en août 2026 se situe entre 20 et 35 € HT de l'heure pour du nettoyage de bureaux standard. Les locaux sensibles (laboratoires, santé, restauration) peuvent atteindre 60 € HT de l'heure."),
        ("Quel est le tarif moyen d'une entreprise de nettoyage par heure ?",
         "Entre 20 et 35 € HT de l'heure pour des bureaux, 25 à 40 € pour du nettoyage à domicile et 30 à 45 € pour une remise en état après travaux. À Paris, certaines sources relèvent jusqu'à 70 € HT de l'heure sur des prestations très spécifiques."),
        ("Combien coûte le nettoyage de bureaux par salarié ?",
         "Sur la base de 10 m² par poste (norme AFNOR NF X35-102), l'entretien courant représente 16 à 29 € HT par poste et par mois pour deux passages hebdomadaires, et 22 à 39 € HT pour trois passages."),
        ("Y a-t-il un minimum de facturation en nettoyage de bureaux ?",
         "Oui, la plupart des prestataires appliquent un minimum d'intervention, généralement 1 h 30 par semaine. En pratique, le budget mensuel démarre autour de 130 à 150 € HT, même pour une petite surface."),
        ("Pourquoi deux devis pour la même surface peuvent-ils varier du simple au double ?",
         "Parce que le prix dépend du temps prévu, pas de la surface seule. La nature des sols, la surface vitrée, les horaires d'intervention, les consommables, l'accès aux locaux et la densité d'occupation font varier le temps nécessaire, donc le montant."),
        ("Les consommables sont-ils compris dans le tarif ?",
         "Au choix. Papier, savon, sacs et essuie-mains peuvent être intégrés au forfait mensuel ou rester à votre charge si vous avez déjà un fournisseur. Les deux options doivent figurer séparément sur le devis."),
    ],
    hero_stats=[("20–35 €", "HT / heure à Paris"), ("1,50–3,90 €", "HT / m² / mois"), ("10 m²", "par poste — NF X35-102")],
)


# =================================================== A3 — TRAVAIL DISSIMULÉ ==
CHECK_ITEMS = [
    ("L'attestation de vigilance URSSAF",
     "Le document central. Il prouve que le prestataire est à jour de ses déclarations et du paiement de ses cotisations. "
     "À exiger à la signature, puis <b>tous les 6 mois</b> jusqu'à la fin du contrat. Son authenticité se vérifie en ligne "
     "sur urssaf.fr avec le code de sécurité qui y figure — une attestation non vérifiée ne vous protège pas.",
     "Art. L8222-1 et D8222-5"),
    ("La preuve d'immatriculation",
     "Extrait Kbis de moins de 3 mois, ou carte d'identification pour les artisans. Vérifiez que l'objet social correspond "
     "bien à une activité de propreté et que l'entreprise n'est pas en cessation.",
     "Art. D8222-5"),
    ("La liste nominative des salariés étrangers",
     "Si le prestataire emploie des salariés étrangers soumis à autorisation de travail, il doit vous remettre la liste "
     "nominative correspondante, avec la date d'embauche et le type de titre.",
     "Art. D8254-2"),
    ("L'attestation d'assurance responsabilité civile professionnelle",
     "En cours de validité, couvrant l'activité exercée sur votre site. C'est elle qui joue en cas de dégât matériel "
     "pendant l'intervention.", None),
    ("La convention collective appliquée",
     "Le prestataire doit relever de la convention collective nationale des entreprises de propreté. C'est ce qui encadre "
     "les classifications, les rémunérations minimales et la reprise du personnel en cas de changement de prestataire.", None),
    ("La chaîne de sous-traitance",
     "Demandez par écrit si tout ou partie de la prestation est sous-traitée, et à qui. Votre obligation de vigilance "
     "s'étend à chaque sous-traitant direct : un maillon non vérifié est un maillon qui vous expose.",
     "Art. L8222-1"),
]

A3_BODY = """<p class="lead">Confier l'entretien de vos locaux à un prestataire ne transfère pas votre responsabilité. Si votre entreprise de nettoyage emploie des agents non déclarés, c'est vous, donneur d'ordre, qui pouvez être appelé à payer ses cotisations. Voici les documents à exiger, à quelle fréquence, et ce que vous risquez concrètement.</p>

<div class="toc"><b>Au sommaire</b><ol>
<li><a href="#pourquoi">Pourquoi c'est votre problème, pas seulement le sien</a></li>
<li><a href="#checklist">La checklist des documents à exiger</a></li>
<li><a href="#verifier">Comment vérifier une attestation de vigilance</a></li>
<li><a href="#risques">Ce que vous risquez, chiffré</a></li>
<li><a href="#signaux">Les signaux qui doivent vous alerter</a></li>
<li><a href="#faire">Que faire en cas de doute</a></li>
</ol></div>

""" + nb.answer(
    "La réponse en une phrase",
    "Dès qu'un contrat de nettoyage atteint <strong>5 000 € HT</strong>, le donneur d'ordre a une "
    "<strong>obligation de vigilance</strong> : il doit obtenir l'attestation de vigilance URSSAF de son "
    "prestataire à la signature, puis <strong>tous les 6 mois</strong> jusqu'à la fin du contrat — faute de "
    "quoi il peut être tenu <strong>solidairement responsable</strong> des cotisations, impôts et "
    "rémunérations impayés.",
    "Articles L8222-1 et D8222-5 du Code du travail · relevé du 28 août 2026") + """

<h2 id="pourquoi">Pourquoi c'est votre problème, pas seulement le sien</h2>
<p>Le raisonnement intuitif — « j'ai signé un contrat, le reste le regarde » — est précisément celui que la loi écarte. Le législateur a créé une <strong>solidarité financière</strong> du donneur d'ordre pour éviter que la sous-traitance ne serve de paravent au travail dissimulé.</p>
<p>Concrètement : si l'URSSAF constate du travail dissimulé chez votre prestataire de nettoyage et que vous ne pouvez pas prouver avoir accompli vos vérifications, l'administration peut se retourner vers vous pour le paiement des cotisations sociales, des majorations et pénalités, et, le cas échéant, des rémunérations dues aux salariés concernés.</p>
<div class="art-note rv"><b>Le point que tout le monde rate :</b> l'obligation n'est pas ponctuelle. Une attestation obtenue à la signature et jamais renouvelée ne vous protège pas au bout de huit mois. La vérification est <b>semestrielle</b>, et c'est la trace de ces vérifications qui vous exonère.</div>

<h2 id="checklist">La checklist des documents à exiger</h2>
<p>Cochez au fur et à mesure : ces six pièces constituent le dossier de conformité que vous devez pouvoir présenter en cas de contrôle. Conservez-les datées, pour toute la durée du contrat.</p>

""" + nb.checklist(
    "Votre dossier de conformité prestataire",
    "Les 6 pièces à réunir et à tenir à jour. Cochez ce que vous détenez déjà.",
    CHECK_ITEMS) + """

<h2 id="verifier">Comment vérifier une attestation de vigilance</h2>
<p>Recevoir le document ne suffit pas : la loi vous demande de vous assurer de son <strong>authenticité</strong>. C'est une démarche de deux minutes, et c'est elle qui fait la différence en cas de contrôle.</p>
<div class="art-steps rv">
<div class="stp"><b>Demandez le document</b><span>L'attestation de vigilance datant de moins de 6 mois, délivrée par l'URSSAF au prestataire.</span></div>
<div class="stp"><b>Relevez le code de sécurité</b><span>Chaque attestation authentique porte un code alphanumérique unique.</span></div>
<div class="stp"><b>Vérifiez en ligne</b><span>Sur urssaf.fr, l'espace de vérification confirme la validité du document à partir de ce code.</span></div>
<div class="stp"><b>Archivez avec la date</b><span>Conservez l'attestation et la preuve de vérification : c'est votre exonération.</span></div>
</div>
<p>Programmez un rappel semestriel dès la signature du contrat. C'est le seul moyen fiable de ne pas laisser passer l'échéance — l'oubli est la cause la plus fréquente de non-conformité, loin devant la fraude délibérée du prestataire.</p>

<h2 id="risques">Ce que vous risquez, chiffré</h2>
<p>Les sanctions du travail dissimulé frappent d'abord l'employeur fautif, mais le donneur d'ordre négligent est exposé sur le plan financier.</p>
<div class="twrap rv"><table class="art-table">
<thead><tr><th>Qui</th><th>Sanction</th><th>Montant</th><th>Référence</th></tr></thead>
<tbody>
<tr><td>Le prestataire (personne physique)</td><td>Emprisonnement et amende</td><td><b>3 ans</b> et <b>45 000 €</b></td><td>Art. L8224-1</td></tr>
<tr><td>Le prestataire (personne morale)</td><td>Amende</td><td>Jusqu'à <b>225 000 €</b></td><td>Art. L8224-5</td></tr>
<tr><td>Le donneur d'ordre négligent</td><td>Solidarité financière</td><td>Cotisations, majorations, pénalités et impôts dus</td><td>Art. L8222-2</td></tr>
<tr><td>Le donneur d'ordre négligent</td><td>Perte des exonérations</td><td>Annulation des réductions de cotisations sur la période</td><td>Art. L8222-2</td></tr>
<tr><td>Le prestataire</td><td>Peines complémentaires</td><td>Interdiction d'exercer, exclusion des marchés publics, affichage</td><td>Art. L8224-3</td></tr>
</tbody></table></div>
<p class="nb-src">Sanctions confirmées par les publications juridiques relevées le 28/08/2026 (cms.law, weblex.fr, service-public.fr).</p>

<h2 id="signaux">Les signaux qui doivent vous alerter</h2>
<p>Aucun de ces éléments ne prouve à lui seul une irrégularité, mais leur accumulation justifie une vérification approfondie :</p>
<ul>
<li><strong>Un prix anormalement bas.</strong> En dessous de 18–20 € HT de l'heure à Paris, la question du respect des minima conventionnels se pose mécaniquement — nous détaillons les fourchettes réelles dans notre <a href="https://spn-net.fr/prix-nettoyage-bureaux-paris/">guide des prix du nettoyage de bureaux</a>.</li>
<li><strong>Une rotation permanente des agents</strong>, sans que vous sachiez jamais qui intervient.</li>
<li><strong>Des agents qui ne connaissent pas le nom de leur employeur</strong> ou qui déclarent travailler pour une autre société.</li>
<li><strong>Un refus ou un report répété</strong> de fournir l'attestation de vigilance.</li>
<li><strong>Une sous-traitance non déclarée</strong>, découverte au détour d'une conversation.</li>
<li><strong>Des documents sans code de sécurité</strong> ou qui ne passent pas la vérification en ligne.</li>
</ul>

<h2 id="faire">Que faire en cas de doute</h2>
<p>La démarche est graduée, et il vaut mieux l'engager tôt :</p>
<ol>
<li><strong>Écrivez.</strong> Demandez formellement les pièces manquantes, par courriel ou lettre recommandée, en fixant un délai. La trace écrite compte autant que la réponse.</li>
<li><strong>Vérifiez l'attestation en ligne</strong> plutôt que de vous fier au document reçu.</li>
<li><strong>Mettez en demeure</strong> si les pièces ne viennent pas : c'est la condition pour dénoncer utilement le contrat.</li>
<li><strong>Changez de prestataire</strong> si le doute persiste. Le cadre légal organise la transition, y compris la reprise des agents : voir notre page <a href="https://spn-net.fr/changer-de-prestataire-nettoyage/">changer de prestataire de nettoyage</a>.</li>
</ol>
<p>Chez SPN NET, l'attestation de vigilance, le Kbis et l'attestation d'assurance sont transmis à la signature puis à chaque échéance semestrielle, sans que vous ayez à les réclamer. Nos agents sont salariés en direct, sans sous-traitance en cascade, et l'entreprise est certifiée <b>ISO 45001</b> (santé et sécurité au travail) et titulaire de la <b>médaille d'argent EcoVadis 2025</b>. Voir <a href="https://spn-net.fr/a-propos/">nos engagements</a>.</p>

<h2 id="aller-plus-loin">Aller plus loin</h2>
<div class="art-links rv">
<a href="https://spn-net.fr/a-propos/">Nos engagements<span>ISO 45001, EcoVadis Argent, agents salariés en direct</span></a>
<a href="https://spn-net.fr/prix-nettoyage-bureaux-paris/">Le prix du nettoyage de bureaux<span>Les fourchettes réelles — et le seuil qui doit alerter</span></a>
<a href="https://spn-net.fr/changer-de-prestataire-nettoyage/">Changer de prestataire<span>Résiliation, Annexe 7, transition sans coupure</span></a>
<a href="https://spn-net.fr/contact/">Demander un devis<span>Dossier de conformité fourni d'office</span></a>
</div>"""

A3 = dict(
    slug="travail-dissimule-entreprise-nettoyage",
    date="2026-07-27T09:00:00",
    title="Travail dissimulé : comment vérifier que votre entreprise de nettoyage est en règle",
    seo_title="Travail dissimulé : vérifier son entreprise de nettoyage | SPN NET",
    desc="Obligation de vigilance dès 5 000 € HT : attestation URSSAF tous les 6 mois, "
         "checklist des 6 documents à exiger, sanctions chiffrées et solidarité financière du donneur d'ordre.",
    body=A3_BODY,
    faq=[
        ("Qui est responsable en cas de travail dissimulé chez un prestataire ?",
         "L'employeur fautif est sanctionné pénalement, mais le donneur d'ordre qui n'a pas accompli son obligation de vigilance peut être tenu solidairement responsable du paiement des cotisations sociales, des majorations, pénalités et impôts dus par le prestataire (article L8222-2 du Code du travail)."),
        ("À partir de quel montant faut-il vérifier son prestataire de nettoyage ?",
         "Dès 5 000 € HT pour l'ensemble du contrat. Au-delà de ce seuil, vous devez obtenir l'attestation de vigilance URSSAF à la conclusion du contrat, puis tous les 6 mois jusqu'à son terme (article L8222-1)."),
        ("Quels documents demander à une entreprise de nettoyage ?",
         "Six pièces : l'attestation de vigilance URSSAF de moins de 6 mois, un extrait Kbis de moins de 3 mois, le cas échéant la liste nominative des salariés étrangers, l'attestation d'assurance responsabilité civile professionnelle, la convention collective appliquée et la déclaration écrite de la chaîne de sous-traitance."),
        ("Comment vérifier une attestation de vigilance URSSAF ?",
         "Chaque attestation authentique porte un code de sécurité. Il suffit de le saisir dans l'espace de vérification du site urssaf.fr pour confirmer la validité du document. Recevoir l'attestation sans la vérifier ne suffit pas à vous exonérer."),
        ("Quelles sont les sanctions du travail dissimulé ?",
         "Pour une personne physique, jusqu'à 3 ans d'emprisonnement et 45 000 € d'amende (article L8224-1). Pour une personne morale, l'amende peut atteindre 225 000 € (article L8224-5), avec des peines complémentaires comme l'interdiction d'exercer ou l'exclusion des marchés publics."),
        ("Comment prouver que j'ai fait mes vérifications ?",
         "En conservant, datées, les attestations obtenues et la preuve de leur vérification en ligne, pour toute la durée du contrat. C'est cette traçabilité qui vous exonère de la solidarité financière en cas de contrôle."),
        ("Un prix de nettoyage très bas est-il un signe de travail dissimulé ?",
         "Ce n'est pas une preuve, mais un signal. En dessous de 18 à 20 € HT de l'heure à Paris, la question du respect des minima de la convention collective de la propreté se pose. Croisez ce signal avec les autres : rotation des agents, refus de fournir les attestations, sous-traitance non déclarée."),
    ],
    hero_stats=[("5 000 €", "HT — seuil de vigilance"), ("6 mois", "périodicité du contrôle"), ("225 000 €", "amende max. personne morale")],
)


ARTICLES_JUILLET = [A1, A2, A3]

BLOG_CARDS_JUILLET = [
    ("nettoyage-copropriete", "Copropriété", "Nettoyage de copropriété",
     "Obligations du syndic, budget par lot et périmètre à écrire au contrat."),
    ("prix-nettoyage-bureaux-paris", "Prix", "Prix du nettoyage de bureaux à Paris",
     "Les fourchettes réelles au m², à l'heure et au poste — avec calculateur."),
    ("travail-dissimule-entreprise-nettoyage", "Conformité", "Travail dissimulé : vérifier son prestataire",
     "Obligation de vigilance, les 6 documents à exiger et les sanctions encourues."),
]


# ------------------------------------------------------------- moteur ----
def build(a):
    """Gabarit article du site + injection des modules d'attention."""
    import make_article as ma
    html = ma.build_article(a)
    # CSS des modules, avant la fermeture du <style> du gabarit
    html = html.replace("</style>", nb.NB_CSS + "</style>", 1)
    # JS des modules, juste avant la fermeture du conteneur
    if html.rstrip().endswith("</div>"):
        html = html.rstrip()[: -len("</div>")] + nb.NB_JS + "</div>"
    return html


def convert(a, now):
    status = "publish" if datetime.datetime.fromisoformat(a["date"]) <= now else "future"
    # libère le slug si un POST existe
    p = requests.get(POSTS, params={"slug": a["slug"], "status": "publish,future,draft",
                                    "_fields": "id"}, auth=AUTH, timeout=30).json()
    for x in p:
        requests.delete(f"{POSTS}/{x['id']}", params={"force": "true"}, auth=AUTH, timeout=40)
    html = build(a)
    payload = {
        "title": a["title"], "slug": a["slug"], "status": status, "date": a["date"],
        "content": "<!-- wp:html -->\n" + html + "\n<!-- /wp:html -->",
        "template": "elementor_header_footer", "excerpt": a["desc"],
        "meta": {"_elementor_edit_mode": "",
                 "slim_seo": {"title": a["seo_title"], "description": a["desc"], "noindex": False}},
    }
    ex = requests.get(PAGES, params={"slug": a["slug"], "status": "publish,future,draft",
                                     "_fields": "id"}, auth=AUTH, timeout=30).json()
    url = f"{PAGES}/{ex[0]['id']}" if ex else PAGES
    r = requests.post(url, auth=AUTH, timeout=90, json=payload)
    r.raise_for_status()
    j = r.json()
    return f"  ✓ [{status}] {j.get('link')}", len(html)


def rebuild_blog():
    """Index /blog/ — les 7 articles (4 d'août + 3 de juillet), publiés seulement."""
    import make_special as ms
    import make_zone as mz
    from make_blog_aout import BLOG_CARDS as CARDS_AOUT
    cards = BLOG_CARDS_JUILLET + list(CARDS_AOUT)
    live = []
    for c in cards:
        r = requests.get(PAGES, params={"slug": c[0], "status": "publish", "_fields": "id"},
                         auth=AUTH, timeout=30).json()
        if r:
            live.append(c)
    ms.POSTS[:] = live
    print(f"  index /blog/ : {len(live)} article(s) publié(s)")
    print(mz.deploy("blog", ms.CFG["blog"], builder=ms.build, prefix="special"))


def main():
    now = datetime.datetime.now()
    # les cartes de juillet doivent être connues du gabarit (eyebrow de l'article)
    import make_article as ma
    ma.TAGS.update({c[0]: c[1] for c in BLOG_CARDS_JUILLET})
    for a in ARTICLES_JUILLET:
        try:
            line, size = convert(a, now)
            print(f"{line}  ({size:,} car.)".replace(",", " "))
        except Exception as ex:  # noqa: BLE001
            print(f"  ✗ {a['slug']}: {ex}")
    rebuild_blog()


if __name__ == "__main__":
    main()
