#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les 3 contenus GEO de septembre 2026 (SPN NET) — silo « changer de prestataire ».

Relevés SERP live du 29/09/2026 (DataForSEO, fr / France, depth 10). Les trois
sujets remplacent les lignes « Cartographie de la demande (Changer de
prestataire — 1/2/3) » de la feuille GEO. Chacun porte le module d'attention
choisi DANS le relevé, jamais par goût.

  11/09 · résilier un contrat de nettoyage professionnel
      SERP : AI Overview rang 1 — mais il part en B2C (CESU, Shiva, O2, aide à
      domicile) et finit par demander « entreprise prestataire ou emploi direct
      CESU ? ». Google ne tient pas l'intention B2B. cleany.fr 1er titre son
      étape 1 « Calculez votre date limite » sans outil pour la calculer.
      PAA : conditions de résiliation, lettre pour un contrat d'entreprise de
      nettoyage, mettre fin à un contrat. Related : « Loi Chatel résiliation
      contrat nettoyage ».
      → réponse encadrée B2B + CALCULATEUR de date limite + tableau Chatel
        (le piège) + lettre type + FAQ reprenant les PAA.

  18/09 · cahier des charges de nettoyage de bureaux
      SERP : aucun AI Overview. Deux PDF de vrais cahiers des charges rankent
      en page 1 (#7 Maison de l'Emploi de Bordeaux, #8 Électricité de
      Strasbourg). Related saturé de « modèle gratuit », « PDF », « Word ».
      La SERP récompense un document utilisable, pas un article.
      → réponse encadrée + CAHIER DES CHARGES À REMPLIR zone par zone
        (cochable, imprimable, sans e-mail demandé) + tableau des fréquences.

  25/09 · prestataire qui ne respecte pas le contrat
      SERP : AI Overview rang 1, cleany.fr 1er avec son article résiliation,
      deux cabinets d'avocats (adlitem, lebouardavocats). adlitem pointe le
      manque : « ne souhaite pas se contenter de photos ou de simples remarques
      internes ». Personne ne livre le document de preuve.
      → réponse encadrée + RELEVÉ DE NON-CONFORMITÉ cochable + tableau des
        recours gradués + modèle de mise en demeure.

Frontière tenue avec l'existant, pour ne pas cannibaliser :
  /changer-de-prestataire-nettoyage/  = la page mère, elle vend le changement
  /annexe-7-changer-entreprise-nettoyage/ = la reprise du personnel
  /choisir-entreprise-nettoyage/      = le choix du suivant
  A1 = le calendrier de sortie · A3 = la preuve du manquement. A1 ne traite pas
  la preuve, A3 ne refait pas la procédure : chacun renvoie à l'autre.

Aucune offre ni tarif SPN inventé. Les références juridiques sont citées avec
leur article ; le contrat du client prime et c'est écrit dans chaque module.

Usage : python3 agents/landing/make_septembre.py [--dry]
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import navboost as nb          # noqa: E402
import nb_resiliation as nbr   # noqa: E402

HUB = "https://spn-net.fr/choisir-entreprise-nettoyage/"
MERE = "https://spn-net.fr/changer-de-prestataire-nettoyage/"
A7 = "https://spn-net.fr/annexe-7-changer-entreprise-nettoyage/"
QUAL = "https://spn-net.fr/qualite-nettoyage-baisse-apres-3-mois/"
PRIX = "https://spn-net.fr/prix-nettoyage-bureaux-paris/"
TERT = "https://spn-net.fr/tertiaire/"
DISS = "https://spn-net.fr/travail-dissimule-entreprise-nettoyage/"
CERT = "https://spn-net.fr/certifications-entreprise-nettoyage/"

S_RESIL = "https://spn-net.fr/resilier-contrat-nettoyage/"
S_CDC = "https://spn-net.fr/cahier-des-charges-nettoyage-bureaux/"
S_LITIGE = "https://spn-net.fr/prestataire-nettoyage-ne-respecte-pas-contrat/"


def lettre(titre, corps):
    """Bloc « modèle de courrier » — sélectionnable, imprimable, sans échange."""
    return (
        '<div class="nb rv nb-lettre">'
        f'<div class="nb-head"><span class="ic">{nb.IC_BUILD}</span><div>'
        f"<h3>{titre}</h3>"
        "<p>À recopier sur votre papier à en-tête. Rien à télécharger, "
        "aucune adresse e-mail à laisser.</p></div></div>"
        f'<div class="lettre-body">{corps}</div>'
        "</div>"
    )


LETTRE_CSS = (
    "<style>"
    ".spn-art .nb-lettre .lettre-body{background:#fff;border:1px solid var(--line,#e9e4dd);"
    "border-radius:12px;padding:22px 24px;font-size:.94rem;line-height:1.7;color:#2a2d35}"
    ".spn-art .nb-lettre .lettre-body p{margin:0 0 12px}"
    ".spn-art .nb-lettre .v{background:#fff1ea;border-radius:4px;padding:1px 6px;"
    "font-weight:600;color:#9a3412}"
    "</style>"
)

# =========================================================== A1 — RÉSILIER ===

A1_BODY = """<p class="lead">Un contrat de nettoyage de locaux se résilie à sa date anniversaire, avec un préavis d'un à trois mois notifié par lettre recommandée. Rater cette fenêtre, c'est repartir pour un an. Voici comment calculer votre date limite, pourquoi la loi Chatel ne vous protège pas, et ce que doit contenir le courrier.</p>

<div class="toc"><b>Au sommaire</b><ol>
<li><a href="#calendrier">La seule date qui compte vraiment</a></li>
<li><a href="#chatel">Le piège : la loi Chatel ne s'applique pas à vous</a></li>
<li><a href="#lettre">Le courrier de résiliation, ligne par ligne</a></li>
<li><a href="#apres">Ce qui se passe entre l'envoi et la bascule</a></li>
<li><a href="#faute">Si vous ne pouvez pas attendre la date anniversaire</a></li>
</ol></div>

<h2 id="calendrier">La seule date qui compte vraiment</h2>

<p>La quasi-totalité des contrats d'entretien de locaux sont conclus pour un an, avec <strong>tacite reconduction</strong>. Concrètement : si personne ne dit rien, le contrat se renouvelle tout seul à sa date anniversaire. Pour en sortir, il faut le dénoncer <em>avant</em>, en respectant le préavis inscrit au contrat.</p>

<p>Ce préavis est presque toujours de <strong>trois mois</strong> en propreté B2B, parfois un ou deux pour les petits contrats, parfois six pour les marchés multi-sites. Il se compte à rebours depuis la date anniversaire, et c'est la <strong>date de première présentation du recommandé</strong> qui fait foi — pas la date à laquelle vous l'avez posté, ni celle où votre interlocuteur l'a lu.</p>

<p>Une erreur revient sans cesse : confondre la date de signature et la date de prise d'effet. C'est la seconde qui commande. Un contrat signé le 12 novembre pour une prise d'effet au 1<sup>er</sup> janvier a pour anniversaire le 1<sup>er</sup> janvier. Avec trois mois de préavis, votre dernier jour pour envoyer est le 30 septembre.</p>

__CALC_RESIL__

<p>Si la fenêtre est passée, ce n'est pas perdu pour autant : vous pouvez préparer le dossier sereinement, poser le cahier des charges du suivant et envoyer au bon moment l'an prochain. C'est même la meilleure façon de ne pas signer dans l'urgence avec le premier venu. Notre <a href="__HUB__">guide pour choisir une entreprise de nettoyage</a> détaille les dix points à instruire pendant ce délai.</p>

<h2 id="chatel">Le piège : la loi Chatel ne s'applique pas à vous</h2>

<p>C'est la confusion la plus coûteuse, et elle vient directement des résultats de recherche : tapez « résilier un contrat de nettoyage » et Google vous répond avec du CESU, de l'aide à domicile et des agences de ménage pour particuliers. Ce n'est pas votre situation.</p>

<p>La loi Chatel — l'article L215-1 du code de la consommation — oblige le prestataire à vous rappeler par écrit, entre trois et un mois avant la fin du préavis, que vous pouvez ne pas reconduire. S'il ne le fait pas, vous pouvez résilier à tout moment. Excellent dispositif. Il ne protège que les <strong>consommateurs</strong> et les <strong>non-professionnels</strong>.</p>

<p>Une société qui fait entretenir ses bureaux agit dans le cadre de son activité professionnelle. Elle n'est ni l'un ni l'autre. <strong>Aucun rappel d'échéance ne vous est dû</strong>, et l'oubli de votre prestataire ne vous ouvre aucun droit. La surveillance du calendrier est à votre charge, entièrement.</p>

<div class="tbl-wrap"><table class="tbl">
<caption>Ce qui s'applique, selon qui signe</caption>
<thead><tr><th>Situation</th><th>Rappel d'échéance dû&nbsp;?</th><th>Texte</th></tr></thead>
<tbody>
<tr><td>Particulier, contrat de ménage à domicile</td><td><b>Oui</b></td><td>Art. L215-1 c. consommation</td></tr>
<tr><td>Association hors activité professionnelle</td><td>Oui, si non-professionnelle</td><td>Art. liminaire c. consommation</td></tr>
<tr><td><b>Entreprise, entretien de ses locaux</b></td><td><b>Non</b></td><td>Hors champ Chatel</td></tr>
<tr><td><b>Syndicat de copropriétaires</b></td><td><b>Non</b> en principe</td><td>Agit pour la gestion de l'immeuble</td></tr>
</tbody></table></div>

<p>Une seule chose peut vous sauver : une clause du contrat qui prévoit elle-même un rappel. Certains prestataires l'écrivent, par confort commercial. Vérifiez — mais ne comptez pas dessus.</p>

<h2 id="lettre">Le courrier de résiliation, ligne par ligne</h2>

<p>Pas besoin d'avocat. Le courrier doit être <strong>identifiable, daté et sans ambiguïté</strong> : on doit pouvoir dire, à la seule lecture, quel contrat s'arrête et à quelle date. Quatre éléments suffisent : vos références de contrat, le fondement (la clause de résiliation), la date d'effet souhaitée, et la demande d'accusé de réception.</p>

<p>Deux précautions qui évitent les litiges. D'abord, n'invoquez <strong>aucun motif</strong> si vous résiliez à l'échéance : vous n'en devez aucun, et un motif mal formulé ouvre une discussion inutile. Ensuite, demandez dès ce courrier la liste du personnel affecté à votre site — c'est elle qui conditionnera la reprise des agents par le suivant.</p>

__LETTRE1__

<p>Envoyez en recommandé avec accusé de réception, et conservez l'avis de passage : c'est la date de première présentation qui compte, pas celle de la signature de l'accusé. Doublez d'un e-mail le jour même, pour l'horodatage.</p>

<h2 id="apres">Ce qui se passe entre l'envoi et la bascule</h2>

<p>Le préavis n'est pas une zone morte. Votre prestataire reste tenu d'exécuter le contrat jusqu'au dernier jour, au même niveau : les manquements pendant le préavis sont des manquements comme les autres. Et vous restez tenu de payer.</p>

<p>C'est aussi la période où se joue la <strong>reprise du personnel</strong>. En propreté, l'Annexe 7 de la convention collective impose au repreneur de reprendre les agents qui remplissent certains critères d'ancienneté et d'affectation. Ce n'est ni automatique ni optionnel : c'est conditionné. Le détail est dans notre article sur <a href="__A7__">l'Annexe 7 et la reprise du personnel de nettoyage</a>.</p>

<p>Pratiquement, trois choses à faire pendant le préavis : transmettre les coordonnées du sortant à l'entrant, organiser un état des lieux contradictoire des locaux et du matériel laissé sur site, et fixer la date exacte de bascule — idéalement un lundi, jamais un lendemain de jour férié.</p>

<h2 id="faute">Si vous ne pouvez pas attendre la date anniversaire</h2>

<p>La résiliation à l'échéance est le chemin normal. Il existe une autre voie, plus exigeante : la <strong>résiliation pour manquement</strong>, qui permet de sortir avant le terme quand le prestataire n'exécute pas ses obligations. Elle suppose des manquements établis, une mise en demeure restée sans effet, et un dossier qui tient.</p>

<p>Ce n'est pas le même travail : là où la résiliation à l'échéance est une affaire de calendrier, celle-ci est une affaire de preuve. Nous l'avons traitée à part, avec le relevé de non-conformité et le modèle de mise en demeure : <a href="__LITIGE__">que faire quand le prestataire de nettoyage ne respecte pas le contrat</a>.</p>

<p>Dans les deux cas, la question suivante est la même : par qui le remplacer. Prenez le temps d'écrire ce que vous attendez avant de consulter — c'est l'objet de notre <a href="__CDC__">cahier des charges de nettoyage de bureaux</a>, à remplir zone par zone.</p>
"""

A1_FAQ = [
    ("Quelles sont les conditions pour résilier un contrat de nettoyage ?",
     "Trois conditions cumulatives dans le cas normal : résilier à la date anniversaire du contrat, respecter le préavis qu'il prévoit (un à trois mois le plus souvent), et notifier par lettre recommandée avec accusé de réception. Hors de ces conditions, il faut se placer sur le terrain du manquement contractuel, qui suppose des preuves et une mise en demeure préalable."),
    ("Comment rédiger une lettre de résiliation pour un contrat d'entreprise de nettoyage ?",
     "Quatre éléments suffisent : les références du contrat et du site concerné, le fondement (la clause de résiliation et la date anniversaire), la date d'effet souhaitée, et la demande d'accusé de réception. Si vous résiliez à l'échéance, n'indiquez aucun motif : vous n'en devez aucun. Ajoutez une demande de liste du personnel affecté au site, utile pour la reprise par le prestataire suivant."),
    ("Puis-je mettre fin à un contrat de nettoyage à tout moment ?",
     "Non, sauf si le contrat est à durée indéterminée ou prévoit expressément une résiliation libre. Un contrat d'un an à tacite reconduction ne peut être dénoncé qu'à son échéance, avec préavis. La seule autre porte de sortie est la résiliation pour manquement, qui exige des manquements établis et une mise en demeure restée sans effet."),
    ("La loi Chatel s'applique-t-elle aux contrats de nettoyage d'entreprise ?",
     "Non. La loi Chatel (article L215-1 du code de la consommation) protège les consommateurs et les non-professionnels. Une entreprise qui fait entretenir ses locaux agit à des fins professionnelles : elle est hors du champ. Aucun rappel d'échéance ne lui est dû, et l'absence de rappel ne rouvre aucun droit de résiliation."),
    ("Quel préavis pour résilier un contrat de nettoyage de bureaux ?",
     "Il est fixé par le contrat, pas par la loi. En propreté B2B, trois mois est de loin le plus fréquent ; un ou deux mois se rencontrent sur les petits contrats, six mois sur les marchés multi-sites. Vérifiez la clause « durée » ou « résiliation » : c'est elle qui commande, et elle seule."),
    ("Que devient le personnel de nettoyage quand je change de prestataire ?",
     "En propreté, l'Annexe 7 de la convention collective organise le transfert des contrats de travail des agents affectés au site vers l'entreprise entrante, sous conditions d'ancienneté et d'affectation. Ce n'est pas automatique pour tous les agents : les critères doivent être remplis, ce qui suppose que le sortant transmette la liste nominative."),
]

A1 = dict(
    slug="resilier-contrat-nettoyage",
    date="2026-09-11T09:00:00",
    title="Résilier un contrat de nettoyage : date limite, préavis et lettre type",
    seo_title="Résilier un contrat de nettoyage professionnel : préavis et lettre | SPN NET",
    desc="Résilier un contrat de nettoyage de locaux : calculez votre date limite d'envoi, pourquoi la loi Chatel ne vous protège pas, et le modèle de courrier à recopier.",
    hero_stats=[("3 mois", "préavis le plus courant"), ("Date anniv.", "la seule qui compte"),
                ("Chatel", "ne s'applique pas en B2B")],
    body=A1_BODY, faq=A1_FAQ,
)

# ==================================================== A2 — CAHIER DES CHARGES ===

A2_BODY = """<p class="lead">Deux devis de nettoyage ne sont comparables que s'ils répondent à la même demande. Le cahier des charges est ce qui rend la comparaison possible : il décrit vos locaux zone par zone, ce qu'on y fait, à quelle fréquence, et comment on vérifie. Voici le modèle à remplir, et les erreurs qui font exploser les prix.</p>

<div class="toc"><b>Au sommaire</b><ol>
<li><a href="#pourquoi">Pourquoi c'est lui qui fixe le prix</a></li>
<li><a href="#zones">Découper vos locaux en zones</a></li>
<li><a href="#modele">Le cahier des charges à remplir</a></li>
<li><a href="#frequences">Les fréquences : ce qui se fait, ce qui se paie</a></li>
<li><a href="#qualite">Écrire des critères vérifiables, pas des adjectifs</a></li>
<li><a href="#erreurs">Cinq erreurs qui coûtent cher</a></li>
</ol></div>

<h2 id="pourquoi">Pourquoi c'est lui qui fixe le prix</h2>

<p>Un prestataire qui reçoit « 400 m² de bureaux, devis SVP » chiffre à l'aveugle. Il prend une hypothèse moyenne, ajoute une marge de sécurité pour les inconnues, et vous envoie un prix. Un autre prend une hypothèse plus basse et vous envoie un prix plus bas. Vous comparez deux chiffres qui ne recouvrent pas les mêmes prestations — et vous choisissez le moins cher, donc le moins-disant sur le périmètre.</p>

<p>Trois mois plus tard, les vitres ne sont pas faites, la tisanerie est « hors contrat », et vous payez des suppléments. Ce n'est pas de la mauvaise foi : c'est l'effet mécanique d'une demande imprécise. C'est d'ailleurs l'un des mécanismes de <a href="__QUAL__">la baisse de qualité au troisième mois</a>.</p>

<p>Le cahier des charges supprime cette zone grise. Il ne rend pas le nettoyage moins cher en lui-même : il rend les devis <strong>comparables</strong>, ce qui est la seule façon de savoir si un prix est bon. Pour situer vos chiffres, notre relevé des <a href="__PRIX__">prix du nettoyage de bureaux à Paris</a> donne les fourchettes de marché au m², à l'heure et au poste.</p>

<h2 id="zones">Découper vos locaux en zones</h2>

<p>Le découpage par zones est la colonne vertébrale du document. Il évite l'écueil du « tout partout tous les jours », qui n'est ni réaliste ni finançable, et celui de la liste de tâches sans localisation, impossible à contrôler.</p>

<p>Quatre familles couvrent la quasi-totalité des locaux tertiaires, et chacune appelle une logique différente : les <strong>espaces de travail</strong> (postes, plateaux, salles de réunion), les <strong>sanitaires</strong>, les <strong>circulations et espaces communs</strong> (accueil, couloirs, ascenseurs), et les <strong>locaux techniques et annexes</strong> (tisanerie, archives, local poubelles, parking).</p>

<div class="tbl-wrap"><table class="tbl">
<caption>Les quatre zones et ce qui les distingue</caption>
<thead><tr><th>Zone</th><th>Enjeu dominant</th><th>Fréquence typique</th><th>Ce qu'on oublie</th></tr></thead>
<tbody>
<tr><td>Espaces de travail</td><td>Poussière, points de contact</td><td>2 à 5 / semaine</td><td>Écrans, claviers, dessous de bureaux</td></tr>
<tr><td>Sanitaires</td><td>Hygiène, consommables</td><td>Quotidien</td><td>Réassort, traçabilité du passage</td></tr>
<tr><td>Circulations, accueil</td><td>Image, première impression</td><td>Quotidien</td><td>Vitrages intérieurs, traces de mains</td></tr>
<tr><td>Techniques, annexes</td><td>Sécurité, odeurs</td><td>Hebdo à mensuel</td><td>Local poubelles, tisanerie, archives</td></tr>
</tbody></table></div>

<p>Pour chaque zone, trois colonnes suffisent : la surface approximative, les tâches, la fréquence. Le reste est du détail.</p>

<h2 id="modele">Le cahier des charges à remplir</h2>

<p>Cochez ce que vous voulez voir figurer. Le document se lit dans l'ordre, section par section : à la fin, vous avez un périmètre écrit, que vous pouvez envoyer tel quel à trois prestataires en leur demandant de chiffrer <strong>la même chose</strong>.</p>

__CDC_CHECK__

<p>Ce document ne s'échange contre rien. Pas d'adresse e-mail à laisser, pas de formulaire : vous cochez, vous imprimez, vous l'envoyez à qui vous voulez — y compris à vos prestataires actuels.</p>

<h2 id="frequences">Les fréquences : ce qui se fait, ce qui se paie</h2>

<p>C'est la variable qui pèse le plus sur le devis, avant même la surface. Passer de deux à trois passages hebdomadaires augmente le coût d'environ la moitié ; passer à cinq le double presque. Autant le décider en connaissance de cause.</p>

<p>Une règle simple : la fréquence se cale sur <strong>l'occupation réelle</strong>, pas sur la surface. Un plateau de 300 m² occupé par huit personnes trois jours par semaine n'a pas besoin du même rythme qu'un plateau identique à trente personnes en présentiel complet. Comptez les occupants et les jours de présence, pas les mètres carrés.</p>

<p>Deuxième règle : séparez ce qui est <strong>récurrent</strong> de ce qui est <strong>périodique</strong>. Vitrerie, remise en état des sols, nettoyage des luminaires n'ont rien à faire dans le forfait hebdomadaire — ils se chiffrent au passage, deux à quatre fois par an. Les mélanger, c'est payer toute l'année une prestation trimestrielle.</p>

<h2 id="qualite">Écrire des critères vérifiables, pas des adjectifs</h2>

<p>« Locaux propres », « prestation soignée », « qualité irréprochable » : ces formules ne se contrôlent pas. Le jour où vous voudrez constater un manquement, elles ne vous serviront à rien, parce que personne ne peut trancher objectivement.</p>

<p>Un critère vérifiable est une phrase dont on peut dire « oui » ou « non » en regardant : corbeilles vidées et sacs remplacés, sols sans salissure visible en lumière rasante, sanitaires approvisionnés en papier et savon à chaque passage, surfaces vitrées intérieures sans trace de doigt à hauteur d'homme, absence de poussière sur les plans horizontaux à hauteur de main.</p>

<p>Ajoutez le <strong>rythme de contrôle</strong> : qui vérifie, à quelle fréquence, sur quel support. Un contrôle mensuel contradictoire, consigné sur un cahier de liaison ou une fiche signée des deux côtés, suffit — et change tout le jour où il faut objectiver une dérive.</p>

<h2 id="erreurs">Cinq erreurs qui coûtent cher</h2>

<p><strong>Copier un modèle sans l'adapter.</strong> Les cahiers des charges publics qu'on trouve en ligne sont écrits pour des bâtiments précis. Repris tels quels, ils décrivent des locaux que vous n'avez pas et oublient les vôtres.</p>

<p><strong>Omettre les contraintes d'accès.</strong> Horaires d'intervention, badges, alarme, présence d'un gardien, ascenseur réservé : ce sont des coûts. Non dites, elles reviennent en avenant.</p>

<p><strong>Ne rien écrire sur les consommables.</strong> Papier, savon, sacs : qui fournit, qui stocke, qui réassort. C'est la première source de litige au quotidien.</p>

<p><strong>Oublier la continuité de service.</strong> Que se passe-t-il en cas d'absence de l'agent ? Le remplacement est-il systématique, sous quel délai ? Écrivez-le, sinon il n'existe pas.</p>

<p><strong>Ne pas demander les pièces de conformité.</strong> Attestation de vigilance URSSAF, liste nominative des salariés étrangers : au-delà de 5 000 € HT, vous avez une obligation de vigilance, et c'est vous qui êtes exposé. Le détail est dans notre article sur <a href="__DISS__">la vérification du travail dissimulé chez votre prestataire</a>.</p>

<p>Une fois le document rempli, consultez trois prestataires, pas dix. Et comparez sur la grille complète : notre <a href="__HUB__">guide d'achat pour choisir une entreprise de nettoyage</a> reprend les dix critères qui séparent deux offres, prix compris. Pour vos bureaux, voyez aussi notre offre de <a href="__TERT__">nettoyage de bureaux à Paris</a>.</p>
"""

A2_FAQ = [
    ("Comment faire un cahier des charges de nettoyage ?",
     "En six temps : décrire les locaux et le contexte, découper en zones (travail, sanitaires, circulations, annexes), lister les tâches par zone, fixer les fréquences en séparant le récurrent du périodique, écrire des critères de qualité vérifiables, puis préciser les conditions d'exécution (horaires, accès, consommables, continuité de service, pièces de conformité à fournir)."),
    ("Que doit contenir un cahier des charges de nettoyage de bureaux ?",
     "Les surfaces par zone, les tâches attendues zone par zone, les fréquences, les prestations périodiques chiffrées à part (vitrerie, sols, luminaires), les horaires et contraintes d'accès, la fourniture des consommables, les modalités de remplacement en cas d'absence, les critères de qualité contrôlables et le rythme des contrôles contradictoires."),
    ("Existe-t-il un modèle de cahier des charges de nettoyage gratuit ?",
     "Oui : celui de cette page se remplit directement à l'écran, section par section, et s'imprime. Il ne demande ni adresse e-mail ni création de compte. Méfiez-vous des modèles publics recopiés tels quels : ils décrivent des bâtiments précis et ne correspondront pas à vos locaux."),
    ("Faut-il un cahier des charges pour une petite surface ?",
     "Oui, et il est même plus rentable : sur un petit contrat, un supplément imprévu pèse proportionnellement plus lourd. Le document peut tenir sur deux pages. Ce qui compte n'est pas sa longueur, c'est que les trois prestataires consultés chiffrent exactement le même périmètre."),
    ("Comment comparer deux devis de nettoyage ?",
     "En vérifiant d'abord qu'ils répondent au même périmètre : mêmes zones, mêmes fréquences, mêmes prestations périodiques incluses ou exclues. Ensuite seulement, ramenez les deux prix à une unité commune — au m² et par mois, ou au passage. Un écart de prix sur des périmètres différents ne veut rien dire."),
    ("Combien de prestataires faut-il consulter ?",
     "Trois suffisent. Au-delà, le temps d'instruction augmente sans que la qualité de la décision progresse, et vous risquez d'attirer des offres d'appel non tenables. Trois devis sur un périmètre identique donnent déjà une fourchette de marché fiable."),
]

A2 = dict(
    slug="cahier-des-charges-nettoyage-bureaux",
    date="2026-09-18T09:00:00",
    title="Cahier des charges de nettoyage de bureaux : le modèle à remplir",
    seo_title="Cahier des charges nettoyage de bureaux : modèle à remplir | SPN NET",
    desc="Le cahier des charges de nettoyage de bureaux à remplir zone par zone, sans e-mail à laisser : tâches, fréquences, critères vérifiables et erreurs à éviter.",
    hero_stats=[("4 zones", "le découpage qui tient"), ("3 devis", "pas dix"),
                ("0 e-mail", "rien à échanger")],
    body=A2_BODY, faq=A2_FAQ,
)

# ========================================================= A3 — NON-RESPECT ===

A3_BODY = """<p class="lead">Les corbeilles ne sont pas vidées, les sanitaires sont à sec, l'agent n'est pas passé jeudi. Avant de parler de résiliation, il faut transformer ce constat en preuve : un relevé écrit, daté, contradictoire. Voici comment constater, tracer, mettre en demeure — et à quel moment vous pouvez sortir avant le terme.</p>

<div class="toc"><b>Au sommaire</b><ol>
<li><a href="#constater">Constater, c'est écrire</a></li>
<li><a href="#releve">Le relevé de non-conformité</a></li>
<li><a href="#graduation">Les quatre niveaux de recours</a></li>
<li><a href="#demeure">La mise en demeure</a></li>
<li><a href="#faute">Résilier pour manquement avant le terme</a></li>
<li><a href="#eviter">Ce qui aurait évité le litige</a></li>
</ol></div>

<h2 id="constater">Constater, c'est écrire</h2>

<p>Le réflexe naturel est le coup de fil, puis l'e-mail agacé, puis la photo prise sur le vif. Aucun des trois ne constitue, seul, un dossier. Un cabinet d'avocats résume bien le problème : l'entreprise cliente soupçonne que le prestataire ne respecte pas ses engagements, mais ne veut pas se contenter de photos ou de remarques internes.</p>

<p>Ce qui fait preuve, c'est un <strong>relevé régulier, daté et porté à la connaissance du prestataire</strong>. Trois caractéristiques : il compare la prestation constatée à une prestation <em>écrite</em> au contrat — d'où l'importance du <a href="__CDC__">cahier des charges</a> ; il est daté et horodaté ; il est transmis, de sorte que le prestataire ne puisse pas dire qu'il ignorait.</p>

<p>Un manquement signalé et non corrigé vaut dix manquements constatés en silence. C'est la répétition <em>après</em> signalement qui fait basculer un dossier.</p>

<h2 id="releve">Le relevé de non-conformité</h2>

<p>Le document ci-dessous se remplit sur place, en dix minutes, idéalement au même moment de la semaine. Cochez ce qui est conforme ; ce qui reste décoché est votre constat. Datez, signez, envoyez par e-mail le jour même — c'est cet envoi qui vaut signalement.</p>

__LITIGE_CHECK__

<p>Faites-le signer par l'agent ou le responsable de secteur quand c'est possible : un relevé contradictoire pèse infiniment plus qu'un relevé unilatéral. En cas de refus de signature, mentionnez-le sur le document et envoyez quand même.</p>

<h2 id="graduation">Les quatre niveaux de recours</h2>

<p>On ne passe pas du premier agacement au tribunal. La gradation compte, et elle compte juridiquement : un juge regarde si vous avez laissé au prestataire une chance de corriger.</p>

<div class="tbl-wrap"><table class="tbl">
<caption>La gradation des recours, du plus souple au plus lourd</caption>
<thead><tr><th>Niveau</th><th>Forme</th><th>Ce qu'il déclenche</th><th>Quand</th></tr></thead>
<tbody>
<tr><td>1. Signalement</td><td>E-mail avec relevé joint</td><td>Trace datée, obligation de corriger</td><td>Dès le premier constat</td></tr>
<tr><td>2. Réunion de recadrage</td><td>Réunion + compte rendu écrit</td><td>Plan d'action daté, engagements chiffrés</td><td>Après 2 à 3 signalements</td></tr>
<tr><td>3. Mise en demeure</td><td>Lettre recommandée AR</td><td>Délai d'exécution, point de départ des sanctions</td><td>Si le plan d'action échoue</td></tr>
<tr><td>4. Résiliation pour manquement</td><td>Lettre recommandée AR</td><td>Fin du contrat avant le terme</td><td>Mise en demeure restée sans effet</td></tr>
</tbody></table></div>

<p>Entre les niveaux 2 et 3, une question se pose : vos pénalités contractuelles. Beaucoup de contrats en prévoient et personne ne les applique jamais. Les activer, même symboliquement, est souvent plus efficace qu'un courrier de plus — et cela constitue une trace supplémentaire.</p>

<h2 id="demeure">La mise en demeure</h2>

<p>C'est le pivot du dossier. Le code civil, à l'article 1226, subordonne la résolution du contrat par notification à une mise en demeure préalable, sauf urgence. Autrement dit : sans mise en demeure, votre résiliation anticipée est fragile.</p>

<p>Elle doit contenir quatre choses : le rappel des obligations contractuelles précises qui ne sont pas tenues, la liste datée des manquements constatés et déjà signalés, un <strong>délai raisonnable</strong> pour y remédier — quinze à trente jours selon la nature du manquement — et la mention expresse de ce qui se passera à défaut.</p>

__LETTRE3__

<p>Envoyez en recommandé avec accusé de réception. Et tenez le délai que vous avez fixé : résilier avant son expiration retourne l'argument contre vous.</p>

<h2 id="faute">Résilier pour manquement avant le terme</h2>

<p>Si le délai expire sans correction réelle, vous pouvez notifier la résolution du contrat. Les articles 1224 à 1230 du code civil l'organisent : la résolution résulte soit d'une clause résolutoire prévue au contrat, soit d'une notification du créancier en cas d'inexécution suffisamment grave, soit d'une décision de justice.</p>

<p>Deux points de vigilance. D'abord, « suffisamment grave » s'apprécie : un manquement isolé ne suffit pas, une dérive répétée et signalée oui. Ensuite, vous agissez à vos risques : si le prestataire conteste et qu'un juge estime la gravité insuffisante, vous pouvez être condamné à des dommages. C'est précisément pour cela que le relevé compte.</p>

<p>Si la gravité ne vous paraît pas établie, la voie sûre reste la sortie à l'échéance. Nous l'avons détaillée, avec le calcul de la date limite et le modèle de courrier : <a href="__RESIL__">résilier un contrat de nettoyage à sa date anniversaire</a>.</p>

<h2 id="eviter">Ce qui aurait évité le litige</h2>

<p>Presque tous les litiges de propreté ont la même origine : un périmètre jamais écrit, donc jamais opposable. Quand le contrat dit « entretien des locaux » et rien de plus, il n'y a pas de manquement possible — il n'y a que des attentes déçues.</p>

<p>Le second facteur est l'absence de rituel de contrôle. Un point mensuel de quinze minutes, consigné, détecte la dérive au premier mois au lieu du sixième. C'est exactement le mécanisme décrit dans notre article sur <a href="__QUAL__">la qualité du nettoyage qui baisse après trois mois</a>.</p>

<p>Enfin, la solidité du prestataire compte plus que son prix. Un opérateur qui sous-traite en cascade ou dont les équipes tournent tous les deux mois ne tiendra aucun engagement, quel que soit le contrat signé. Les points à instruire avant de signer sont réunis dans notre <a href="__HUB__">guide pour bien choisir son entreprise de nettoyage</a>, et les <a href="__CERT__">certifications d'une entreprise de nettoyage</a> en disent long sur son organisation réelle. Si la décision est prise, voyez comment <a href="__MERE__">changer de prestataire de nettoyage</a> sans rupture de service.</p>
"""

A3_FAQ = [
    ("Que se passe-t-il en cas de non-respect d'un contrat de nettoyage ?",
     "Le client peut exiger l'exécution, appliquer les pénalités prévues au contrat, demander une réduction du prix, ou engager la résolution du contrat. Le code civil (articles 1217 et suivants) ouvre ces options. Dans tous les cas, une mise en demeure préalable est nécessaire pour résoudre le contrat par notification, sauf urgence."),
    ("Comment prouver qu'un prestataire de nettoyage ne fait pas son travail ?",
     "Par un relevé de non-conformité écrit, daté, comparant la prestation constatée à ce que le contrat prévoit, et transmis au prestataire le jour même. Des photos seules ou des remarques internes ne suffisent pas : c'est la répétition d'un manquement déjà signalé, et restée sans correction, qui constitue le dossier."),
    ("Puis-je résilier un contrat de nettoyage pour faute avant son terme ?",
     "Oui, si l'inexécution est suffisamment grave et après mise en demeure restée sans effet, conformément aux articles 1224 à 1230 du code civil. La gravité s'apprécie : un manquement isolé ne suffit pas. Vous agissez à vos risques, d'où l'importance d'un relevé régulier et signalé avant d'en arriver là."),
    ("Quel délai accorder dans une mise en demeure ?",
     "Un délai raisonnable au regard de la nature du manquement : quinze jours pour des manquements d'exécution courante (corbeilles, sanitaires, fréquences), trente jours quand la correction suppose un recrutement ou une réorganisation d'équipe. Le délai fixé doit être tenu : résilier avant son expiration fragilise votre position."),
    ("Quelles sont les obligations d'un prestataire de nettoyage ?",
     "Celles que le contrat met à sa charge, et elles seules : c'est pourquoi un périmètre écrit est décisif. S'y ajoutent des obligations légales indépendantes du contrat, notamment en matière de déclaration de ses salariés — le donneur d'ordre ayant lui-même une obligation de vigilance au-delà de 5 000 € HT."),
    ("Faut-il appliquer les pénalités prévues au contrat ?",
     "Oui, quand elles existent et qu'un manquement est établi. La plupart des contrats en prévoient et personne ne les applique, ce qui les rend inopérantes. Les activer, même pour un montant symbolique, produit souvent plus d'effet qu'un courrier supplémentaire et constitue une trace datée de plus au dossier."),
]

A3 = dict(
    slug="prestataire-nettoyage-ne-respecte-pas-contrat",
    date="2026-09-25T09:00:00",
    title="Prestataire de nettoyage qui ne respecte pas le contrat : quels recours",
    seo_title="Prestataire de nettoyage qui ne respecte pas le contrat : recours | SPN NET",
    desc="Constater, tracer et mettre en demeure un prestataire de nettoyage défaillant : le relevé de non-conformité, les quatre niveaux de recours et le modèle de courrier.",
    hero_stats=[("Art. 1226", "mise en demeure préalable"), ("15 à 30 j", "délai raisonnable"),
                ("4 niveaux", "la gradation des recours")],
    body=A3_BODY, faq=A3_FAQ,
)

ARTICLES = [A1, A2, A3]

BLOG_CARDS_SEPT = [
    ("resilier-contrat-nettoyage", "Contrat",
     "Résilier un contrat de nettoyage",
     "Date limite, préavis, loi Chatel et lettre type — avec le calculateur de date d'envoi."),
    ("cahier-des-charges-nettoyage-bureaux", "Méthode",
     "Cahier des charges de nettoyage",
     "Le modèle à remplir zone par zone, pour que trois devis chiffrent la même chose."),
    ("prestataire-nettoyage-ne-respecte-pas-contrat", "Litige",
     "Prestataire qui ne respecte pas le contrat",
     "Constater, tracer, mettre en demeure : le relevé de non-conformité et les recours."),
]


# ================================================================ MODULES ===

CDC_ITEMS = [
    ("Surfaces et plan par zone",
     "Surface approximative de chaque zone, nombre de postes, nombre d'étages et présence d'ascenseur.", None),
    ("Espaces de travail",
     "Dépoussiérage des plans, corbeilles, points de contact, aspiration ou lavage des sols. Précisez si les bureaux sont dégagés le soir.", None),
    ("Sanitaires",
     "Nettoyage complet, désinfection, réassort papier, savon et essuie-mains. Indiquez qui fournit les consommables.", None),
    ("Circulations et accueil",
     "Sols, vitrages intérieurs, traces de mains sur portes et cloisons, banque d'accueil.", None),
    ("Tisanerie et espaces de pause",
     "Plans de travail, évier, extérieur des appareils, tables. Précisez si la vaisselle est exclue.", None),
    ("Locaux techniques et annexes",
     "Local poubelles, archives, parking, local ménage. Souvent oubliés, souvent facturés en supplément ensuite.", None),
    ("Frequences par zone",
     "Calées sur l'occupation réelle, pas sur la surface. Comptez les occupants et les jours de présence.", None),
    ("Prestations périodiques chiffrées à part",
     "Vitrerie, remise en état des sols, luminaires, moquettes. Deux à quatre passages par an, jamais dans le forfait hebdomadaire.", None),
    ("Horaires et contraintes d'accès",
     "Plages d'intervention, badges, alarme, gardien, ascenseur réservé. Non dites, elles reviennent en avenant.", None),
    ("Continuité de service",
     "Remplacement en cas d'absence : systématique ou non, sous quel délai, avec quel niveau d'information.", None),
    ("Critères de qualité vérifiables",
     "Des phrases auxquelles on répond par oui ou non, jamais des adjectifs. Plus le rythme des contrôles contradictoires.", None),
    ("Pièces de conformité à fournir",
     "Attestation de vigilance URSSAF de moins de six mois, liste nominative des salariés étrangers, attestation d'assurance.",
     "Art. L8222-1 c. travail"),
]

LITIGE_ITEMS = [
    ("Corbeilles vidées et sacs remplacés",
     "Dans toutes les zones prévues au contrat, pas seulement les bureaux individuels.", None),
    ("Sanitaires nettoyés et réapprovisionnés",
     "Papier, savon, essuie-mains présents à l'issue du passage.", None),
    ("Sols traités selon le protocole",
     "Aspiration ou lavage selon le revêtement, sans salissure visible en lumière rasante.", None),
    ("Points de contact désinfectés",
     "Poignées, interrupteurs, boutons d'ascenseur, rampes.", None),
    ("Vitrages intérieurs sans trace",
     "Cloisons et portes vitrées, à hauteur d'homme.", None),
    ("Passage effectué aux jours prévus",
     "Comparez au planning contractuel, pas à votre souvenir. Notez les jours manqués.", None),
    ("Horaire d'intervention respecté",
     "Le passage a-t-il eu lieu dans la plage prévue, hors présence des équipes si c'est ce qui est écrit.", None),
    ("Agent habituel présent",
     "Une rotation permanente d'agents est un signal, et souvent la cause du reste.", None),
    ("Consommables fournis conformément au contrat",
     "Qui fournit, qui stocke, qui réassort : première source de litige au quotidien.", None),
    ("Relevé daté, signé et transmis le jour même",
     "C'est l'envoi qui vaut signalement. Sans transmission, le constat ne vaut rien.",
     "Art. 1226 c. civil"),
]

LETTRE1 = (
    "<p>Objet&nbsp;: r&eacute;siliation du contrat d&rsquo;entretien "
    "n<sup>o</sup>&nbsp;<span class=\"v\">[r&eacute;f&eacute;rence]</span> &mdash; site "
    "<span class=\"v\">[adresse]</span><br>Lettre recommand&eacute;e avec accus&eacute; de r&eacute;ception</p>"
    "<p>Madame, Monsieur,</p>"
    "<p>Par la pr&eacute;sente, nous vous notifions notre d&eacute;cision de ne pas reconduire le contrat "
    "d&rsquo;entretien des locaux r&eacute;f&eacute;renc&eacute; ci-dessus, conclu le "
    "<span class=\"v\">[date de signature]</span> et ayant pris effet le "
    "<span class=\"v\">[date d&rsquo;effet]</span>.</p>"
    "<p>Conform&eacute;ment &agrave; l&rsquo;article <span class=\"v\">[num&eacute;ro]</span> du contrat, "
    "pr&eacute;voyant un pr&eacute;avis de <span class=\"v\">[dur&eacute;e]</span>, cette r&eacute;siliation "
    "prendra effet le <span class=\"v\">[date anniversaire]</span> au soir. Les prestations se poursuivront "
    "normalement jusqu&rsquo;&agrave; cette date, aux conditions en vigueur.</p>"
    "<p>Nous vous remercions de bien vouloir nous adresser, dans les meilleurs d&eacute;lais&nbsp;: "
    "la liste nominative des agents affect&eacute;s au site avec leur date d&rsquo;entr&eacute;e, leur "
    "qualification et leur temps de travail sur le site&nbsp;; ainsi qu&rsquo;un &eacute;tat du mat&eacute;riel "
    "et des consommables vous appartenant pr&eacute;sents dans nos locaux.</p>"
    "<p>Nous vous saurions gr&eacute; de nous confirmer la bonne r&eacute;ception de ce courrier et la date "
    "d&rsquo;effet retenue.</p>"
    "<p>Veuillez agr&eacute;er, Madame, Monsieur, l&rsquo;expression de nos salutations distingu&eacute;es.</p>"
)

LETTRE3 = (
    "<p>Objet&nbsp;: mise en demeure d&rsquo;ex&eacute;cuter &mdash; contrat d&rsquo;entretien "
    "n<sup>o</sup>&nbsp;<span class=\"v\">[r&eacute;f&eacute;rence]</span><br>"
    "Lettre recommand&eacute;e avec accus&eacute; de r&eacute;ception</p>"
    "<p>Madame, Monsieur,</p>"
    "<p>Le contrat vis&eacute; en objet met &agrave; votre charge "
    "<span class=\"v\">[rappeler les obligations pr&eacute;cises&nbsp;: zones, t&acirc;ches, fr&eacute;quences]</span>.</p>"
    "<p>Or, nous avons constat&eacute; les manquements suivants, qui vous ont &eacute;t&eacute; signal&eacute;s "
    "par courriel les <span class=\"v\">[dates]</span> et dont les relev&eacute;s sont joints&nbsp;: "
    "<span class=\"v\">[liste dat&eacute;e des manquements]</span>. Ces manquements se sont r&eacute;p&eacute;t&eacute;s "
    "post&eacute;rieurement &agrave; nos signalements, sans correction durable.</p>"
    "<p>En cons&eacute;quence, nous vous mettons en demeure d&rsquo;ex&eacute;cuter vos obligations "
    "contractuelles dans un d&eacute;lai de <span class=\"v\">[15 ou 30]</span> jours &agrave; compter de la "
    "premi&egrave;re pr&eacute;sentation de la pr&eacute;sente.</p>"
    "<p>&Agrave; d&eacute;faut d&rsquo;ex&eacute;cution dans ce d&eacute;lai, nous nous r&eacute;servons "
    "d&rsquo;appliquer les p&eacute;nalit&eacute;s pr&eacute;vues &agrave; l&rsquo;article "
    "<span class=\"v\">[num&eacute;ro]</span> et de proc&eacute;der &agrave; la r&eacute;solution du contrat "
    "par notification, dans les conditions des articles 1224 et suivants du code civil.</p>"
    "<p>Veuillez agr&eacute;er, Madame, Monsieur, l&rsquo;expression de nos salutations distingu&eacute;es.</p>"
)

LINKS = {
    "__HUB__": HUB, "__MERE__": MERE, "__A7__": A7, "__QUAL__": QUAL, "__PRIX__": PRIX,
    "__TERT__": TERT, "__DISS__": DISS, "__CERT__": CERT,
    "__RESIL__": S_RESIL, "__CDC__": S_CDC, "__LITIGE__": S_LITIGE,
}

MODULES = {
    "__CALC_RESIL__": lambda: nbr.calc_resiliation(),
    "__LETTRE1__": lambda: lettre("Le courrier de résiliation à l'échéance", LETTRE1),
    "__LETTRE3__": lambda: lettre("La mise en demeure à adresser", LETTRE3),
    "__CDC_CHECK__": lambda: nb.checklist(
        "Votre cahier des charges, section par section",
        "Cochez ce que vous voulez voir figurer. À la fin, vous avez un périmètre écrit, "
        "que trois prestataires pourront chiffrer à l'identique.",
        CDC_ITEMS, nb.IC_BUILD),
    "__LITIGE_CHECK__": lambda: nb.checklist(
        "Relevé de non-conformité",
        "À remplir sur place, au même moment chaque semaine. Ce qui reste décoché est votre constat : "
        "datez, signez, envoyez le jour même.",
        LITIGE_ITEMS),
}


def resolve(a):
    """Remplace les jetons de liens et de modules dans le corps."""
    b = a["body"]
    for k, v in LINKS.items():
        b = b.replace(k, v)
    for k, f in MODULES.items():
        if k in b:
            b = b.replace(k, f())
    if "__" in re.sub(r"__[A-Z0-9_]+__", "", b) is None:
        pass
    left = re.findall(r"__[A-Z0-9_]+__", b)
    if left:
        raise SystemExit(f"{a['slug']} : jetons non resolus {set(left)}")
    out = dict(a)
    out["body"] = b
    return out


def extra_css():
    """CSS des modules propres a ces trois articles."""
    return nbr.CSS + LETTRE_CSS


def main():
    import make_article as ma
    ma.TAGS.update({c[0]: c[1] for c in BLOG_CARDS_SEPT})
    dry = "--dry" in sys.argv
    for a in ARTICLES:
        r = resolve(a)
        html = ma.build_article(r)
        html = html.replace("</style>", "</style>" + nb.NB_CSS + extra_css(), 1) \
            if "</style>" in html else nb.NB_CSS + extra_css() + html
        html = html.rstrip()
        # JS des modules, juste avant la fermeture du gabarit
        js = nb.NB_JS + (nbr.JS if 'id="calcResil"' in html else "")
        html = html[: html.rfind("</div>")] + js + html[html.rfind("</div>"):]
        path = os.path.join(os.path.dirname(__file__), f"article-{a['slug']}.html")
        open(path, "w", encoding="utf-8").write(html)
        nlink = len(re.findall(r'<a\b[^>]*href="https://spn-net\.fr/', html))
        print(f"  {a['slug']:46} {len(html):7} o · {nlink} liens internes"
              + ("  [simulation]" if dry else ""))
        if dry:
            continue
        r2 = dict(r)
        r2["body"] = r["body"]
        print("   ", ma.convert_html(r2, html) if hasattr(ma, "convert_html") else deploy(r2, html))


def deploy(a, html):
    import datetime
    import requests
    AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
    PAGES = "https://spn-net.fr/wp-json/wp/v2/pages"
    POSTS = "https://spn-net.fr/wp-json/wp/v2/posts"
    NOW = datetime.datetime.now()
    status = "publish" if datetime.datetime.fromisoformat(a["date"]) <= NOW else "future"
    for x in requests.get(POSTS, params={"slug": a["slug"], "status": "publish,future,draft",
                                         "_fields": "id"}, auth=AUTH, timeout=40).json():
        requests.delete(f"{POSTS}/{x['id']}", params={"force": "true"}, auth=AUTH, timeout=40)
    payload = {
        "title": a["title"], "slug": a["slug"], "status": status, "date": a["date"],
        "content": "<!-- wp:html -->\n" + html + "\n<!-- /wp:html -->",
        "template": "elementor_header_footer", "excerpt": a["desc"],
        "meta": {"_elementor_edit_mode": "",
                 "slim_seo": {"title": a["seo_title"], "description": a["desc"], "noindex": False}},
    }
    ex = requests.get(PAGES, params={"slug": a["slug"], "status": "publish,future,draft",
                                     "_fields": "id"}, auth=AUTH, timeout=40).json()
    url = f"{PAGES}/{ex[0]['id']}" if ex else PAGES
    r = requests.post(url, auth=AUTH, timeout=120, json=payload)
    r.raise_for_status()
    return f"→ {r.json().get('link')}"


if __name__ == "__main__":
    main()
