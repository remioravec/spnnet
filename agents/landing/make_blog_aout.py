#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publie les 4 articles de blog du calendrier d'aout 2026 (demande cliente).

Contenu SEO reel, factuel (aucune offre/certif inventee : seules ISO 45001 +
EcoVadis Argent sont attribuees a SPN NET), maillage interne, FAQ + schema
FAQPage, CTA. Dates respectees : passees = publiees (datees), futures = programmees.

Usage : python3 agents/landing/make_blog_aout.py
        python3 agents/landing/make_blog_aout.py --restore   (repasse en brouillon)
"""
from __future__ import annotations

import os
import sys
import json
import datetime
import unicodedata

import requests

AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
API = "https://spn-net.fr/wp-json/wp/v2/posts"

CSS = (
    "<style>"
    ".spnblog{--o:#D8431F;--os:#FFF1EA;--ink:#16181D;--grey:#5b616b;--line:#ececec}"
    ".spnblog .toc{background:#faf8f5;border:1px solid var(--line);border-radius:14px;padding:18px 22px;margin:22px 0}"
    ".spnblog .toc b{display:block;font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;color:var(--grey);margin-bottom:8px}"
    ".spnblog .toc ol{margin:0;padding-left:20px}.spnblog .toc a{color:var(--ink);text-decoration:none}.spnblog .toc a:hover{color:var(--o)}"
    ".spnblog h2{margin-top:34px}"
    ".spnblog .faq{margin-top:16px}"
    ".spnblog .faq details{border:1px solid var(--line);border-radius:12px;padding:6px 16px;margin-bottom:10px;background:#fff}"
    ".spnblog .faq summary{cursor:pointer;font-weight:700;padding:10px 0;list-style:none}"
    ".spnblog .faq summary::-webkit-details-marker{display:none}"
    ".spnblog .cta{margin:34px 0 8px;background:linear-gradient(120deg,var(--os),transparent);border:1px solid rgba(216,67,31,.25);border-radius:16px;padding:24px 26px}"
    ".spnblog .cta h3{margin:0 0 6px}.spnblog .cta p{margin:0 0 14px;color:var(--grey)}"
    ".spnblog .cta a.btn{display:inline-block;background:var(--o);color:#fff;font-weight:700;text-decoration:none;padding:11px 22px;border-radius:999px}"
    "</style>"
)


def _faq_block(items):
    html = '<h2 id="faq">Questions fréquentes</h2>\n<div class="faq">\n'
    for q, a in items:
        html += f'  <details><summary>{q}</summary><p>{a}</p></details>\n'
    html += "</div>\n"
    return html


def _faq_schema(items):
    def s(t):
        return "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c)).replace('"', "'")
    q = ",".join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (s(a), s(b)) for a, b in items)
    return '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + q + "]}</script>"


def _cta(title, text, href, label):
    return (f'<div class="cta"><h3>{title}</h3><p>{text}</p>'
            f'<a class="btn" href="https://spn-net.fr{href}">{label}</a></div>')


def wrap(body, faq, cta):
    return (CSS + '<div class="spnblog">\n' + body + "\n" + _faq_block(faq) + _faq_schema(faq) + "\n" + cta + "\n</div>")


# ---------------------------------------------------------------- ARTICLES ----
A1_BODY = """<p class="lead">Changer d'entreprise de nettoyage inquiète surtout pour une raison : que deviennent les agents en place, et va-t-on se retrouver bloqué par des règles obscures ? La réponse tient en trois mots — <strong>l'Annexe 7</strong>. Voici ce que dit vraiment la loi, et pourquoi elle joue en votre faveur.</p>

<div class="toc"><b>Au sommaire</b><ol>
<li><a href="#definition">Qu'est-ce que l'Annexe 7 ?</a></li>
<li><a href="#conditions">Les conditions de reprise du personnel</a></li>
<li><a href="#donneur">Ce que ça change pour vous, donneur d'ordre</a></li>
<li><a href="#etapes">Changer sans friction : les étapes</a></li>
</ol></div>

<h2 id="definition">Qu'est-ce que l'Annexe 7 ?</h2>
<p>L'<strong>Annexe 7</strong> est un texte de la <strong>convention collective nationale des entreprises de propreté</strong>. Elle organise la <em>continuité du contrat de travail</em> des agents de nettoyage lorsqu'un marché change de prestataire. Concrètement : quand une nouvelle société reprend l'entretien d'un site, elle a l'obligation de reprendre les salariés qui y travaillaient, dès lors que certains critères sont réunis.</p>
<p>L'objectif est double : <strong>protéger l'emploi</strong> des agents (ils ne perdent pas leur poste parce que vous changez de prestataire) et <strong>préserver la connaissance du site</strong> (les personnes qui connaissent vos locaux restent en place).</p>

<h2 id="conditions">Les conditions de reprise du personnel</h2>
<p>La reprise ne concerne pas tout le monde automatiquement. Les principaux critères, cumulatifs, sont :</p>
<ul>
<li>une <strong>ancienneté d'au moins 6 mois</strong> sur le site concerné ;</li>
<li>au moins <strong>30 % du temps de travail</strong> effectué sur ce site ;</li>
<li>un contrat en cours (CDI, ou CDD sous conditions) et une affectation effective au marché repris.</li>
</ul>
<p>Les salariés qui remplissent ces critères sont transférés à la société entrante <strong>avec leur ancienneté et les éléments essentiels de leur contrat</strong>. Ceux qui ne les remplissent pas restent salariés de l'entreprise sortante.</p>

<h2 id="donneur">Ce que ça change pour vous, donneur d'ordre</h2>
<p>Bonne nouvelle : l'Annexe 7 <strong>simplifie votre changement</strong> plutôt qu'elle ne le complique.</p>
<ul>
<li><strong>Pas de rupture de service</strong> : les mêmes visages continuent d'entretenir vos locaux pendant la transition.</li>
<li><strong>Pas de perte de savoir-faire</strong> : les agents connaissent déjà vos accès, vos horaires et vos exigences.</li>
<li><strong>Un cadre clair</strong> : la reprise est encadrée par la convention, pas laissée au hasard des négociations.</li>
</ul>
<p>La partie administrative (échanges d'informations sur les salariés, formalités de transfert) relève des <strong>deux prestataires</strong>. Un bon prestataire entrant s'en charge pour vous.</p>

<h2 id="etapes">Changer sans friction : les étapes</h2>
<p>En pratique, un changement bien mené suit quatre temps : un premier contact rapide, une visite de vos locaux, une proposition adaptée, puis la signature et l'organisation de la transition avec l'ancien prestataire. La résiliation de votre contrat en cours peut, elle aussi, être accompagnée — lecture des conditions de préavis et rédaction de la lettre.</p>
<p>Nous avons détaillé tout le processus, étape par étape, sur notre page dédiée : <a href="https://spn-net.fr/changer-de-prestataire-nettoyage/"><strong>changer de prestataire de nettoyage</strong></a>.</p>"""

A1 = dict(
    slug="annexe-7-changer-entreprise-nettoyage",
    date="2026-08-07T09:00:00",
    title="Annexe 7 : changer d'entreprise de nettoyage sans friction, ce que dit la loi",
    seo_title="Annexe 7 : changer d'entreprise de nettoyage sans friction | SPN NET",
    desc="Annexe 7 de la convention propreté : reprise des agents, conditions (6 mois, 30 %), et comment changer de prestataire de nettoyage sans coupure. Le guide clair.",
    body=A1_BODY,
    faq=[
        ("L'Annexe 7 est-elle obligatoire ?",
         "Oui : c'est un texte de la convention collective des entreprises de propreté. Lorsque les critères sont réunis, la reprise des agents par la société entrante s'impose."),
        ("Quels agents sont repris lors d'un changement de prestataire ?",
         "Ceux qui ont au moins 6 mois d'ancienneté sur le site et y effectuent au moins 30 % de leur temps de travail, avec un contrat en cours affecté au marché."),
        ("Vais-je subir une coupure de nettoyage pendant le changement ?",
         "Non, si la transition est organisée : les agents repris assurent la continuité, et le passage de relais avec l'ancien prestataire se prépare en amont."),
        ("Qui gère les démarches de reprise du personnel ?",
         "Elles relèvent des deux prestataires (sortant et entrant). Un prestataire entrant sérieux s'occupe des formalités pour vous."),
    ],
    cta=_cta("Vous envisagez de changer de prestataire ?",
             "On vous accompagne du premier contact au démarrage : résiliation, reprise des agents (Annexe 7), transition sans coupure.",
             "/changer-de-prestataire-nettoyage/", "Voir comment ça se passe →"),
)

A2_BODY = """<p class="lead">C'est un grand classique : les premières semaines, tout est impeccable. Puis, passé le cap des trois mois, la propreté s'effrite. Poubelles oubliées, sols moins nets, sanitaires en retrait. Pourquoi ce relâchement — et surtout, comment l'éviter durablement ?</p>

<div class="toc"><b>Au sommaire</b><ol>
<li><a href="#lunedemiel">L'effet « lune de miel » du contrat</a></li>
<li><a href="#causes">Les 4 vraies causes du relâchement</a></li>
<li><a href="#signaux">Les signaux qui doivent vous alerter</a></li>
<li><a href="#eviter">Comment garder une qualité constante</a></li>
</ol></div>

<h2 id="lunedemiel">L'effet « lune de miel » du contrat</h2>
<p>Au démarrage, un prestataire met ses meilleures ressources sur votre site : il veut réussir sa prise de marché. Cette période flatteuse crée une référence élevée dans votre esprit. Le problème n'est pas tant que la qualité baisse « anormalement » — c'est qu'elle <strong>revient à la normale</strong> une fois l'attention retombée, et que rien n'a été mis en place pour la maintenir.</p>

<h2 id="causes">Les 4 vraies causes du relâchement</h2>
<ul>
<li><strong>Le turnover des agents.</strong> Un agent qui change tous les mois ne connaît jamais vos locaux. La qualité dépend directement de la stabilité des équipes.</li>
<li><strong>Un cahier des charges flou.</strong> Sans fréquences écrites et sans périmètre précis, chacun interprète — et l'interprétation se dégrade avec le temps.</li>
<li><strong>L'absence de contrôle qualité.</strong> Ce qui n'est pas contrôlé n'est pas tenu. Sans visite de suivi ni point régulier, personne ne corrige les dérives.</li>
<li><strong>La sous-traitance en cascade.</strong> Quand la prestation est refilée à un tiers, l'engagement initial se dilue à chaque maillon.</li>
</ul>

<h2 id="signaux">Les signaux qui doivent vous alerter</h2>
<ul>
<li>Vous ne reconnaissez plus les agents d'une semaine à l'autre.</li>
<li>Vous devez <strong>relancer</strong> pour des tâches censées être au contrat.</li>
<li>Personne ne vient jamais vérifier le travail sur place.</li>
<li>Votre interlocuteur change, ou devient injoignable.</li>
</ul>

<h2 id="eviter">Comment garder une qualité constante</h2>
<p>La régularité ne tient pas à la chance, mais à trois leviers concrets :</p>
<ul>
<li><strong>Une équipe fidélisée</strong> — souvent les mêmes agents, qui connaissent vos locaux par cœur.</li>
<li><strong>Un interlocuteur dédié</strong> et joignable, capable d'ajuster la prestation.</li>
<li><strong>Un contrôle qualité régulier</strong>, avec des points de suivi, pour corriger avant que vous n'ayez à relancer.</li>
</ul>
<p>Chez SPN NET, ces trois principes structurent chaque contrat. Découvrez <a href="https://spn-net.fr/a-propos/">nos engagements</a>. Et si votre prestataire actuel s'est essoufflé, sachez qu'<a href="https://spn-net.fr/changer-de-prestataire-nettoyage/">en changer se fait sans friction</a>.</p>"""

A2 = dict(
    slug="qualite-nettoyage-baisse-apres-3-mois",
    date="2026-08-14T09:00:00",
    title="Pourquoi la qualité de votre prestataire de nettoyage baisse après 3 mois",
    seo_title="Qualité du nettoyage qui baisse après 3 mois : causes & solutions | SPN NET",
    desc="Turnover, cahier des charges flou, absence de contrôle : pourquoi la qualité de votre prestataire de nettoyage baisse après 3 mois, et comment garder un niveau constant.",
    body=A2_BODY,
    faq=[
        ("Pourquoi la qualité du nettoyage baisse-t-elle avec le temps ?",
         "Le plus souvent à cause du turnover des agents, d'un cahier des charges imprécis, de l'absence de contrôle qualité et de la sous-traitance en cascade."),
        ("Comment garantir une qualité de nettoyage constante ?",
         "Avec une équipe fidélisée qui connaît vos locaux, un interlocuteur dédié et joignable, et un contrôle qualité régulier qui corrige les dérives avant qu'elles ne s'installent."),
        ("Faut-il changer de prestataire dès que la qualité baisse ?",
         "Pas nécessairement : un point de suivi peut suffire à remettre la prestation à niveau. Si le relâchement persiste malgré les relances, un changement — encadré et sans coupure — est justifié."),
    ],
    cta=_cta("Un prestataire qui s'essouffle ?",
             "Équipe fidélisée, interlocuteur dédié, contrôle qualité régulier : voyez comment nous tenons la propreté dans la durée.",
             "/changer-de-prestataire-nettoyage/", "Reprendre la main →"),
)

A3_BODY = """<p class="lead">Le nettoyage de bureaux se fait souvent tôt le matin ou en soirée, une fois vos équipes parties. Des personnes ont alors accès à vos locaux — postes de travail, documents, matériel — sans témoin. Comment garder la maîtrise ? Voici ce qu'il faut exiger d'un prestataire, et les bonnes pratiques à mettre en place de votre côté.</p>

<div class="toc"><b>Au sommaire</b><ol>
<li><a href="#risque">Le vrai risque : l'accès hors présence</a></li>
<li><a href="#exiger">Ce qu'il faut exiger du prestataire</a></li>
<li><a href="#pratiques">Vos bonnes pratiques internes</a></li>
<li><a href="#rgpd">Données personnelles : le rôle du prestataire</a></li>
</ol></div>

<h2 id="risque">Le vrai risque : l'accès hors présence</h2>
<p>La confidentialité en entreprise ne se joue pas qu'à l'informatique. Un bureau laissé ouvert, un dossier sur une imprimante, un badge d'accès : autant d'éléments exposés lorsqu'une intervention a lieu sans que personne de chez vous ne soit présent. Le risque n'est pas théorique — il se gère par <strong>l'organisation et le contrat</strong>, pas par la méfiance.</p>

<h2 id="exiger">Ce qu'il faut exiger du prestataire</h2>
<ul>
<li><strong>Une clause de confidentialité</strong> engageant l'entreprise et ses agents.</li>
<li><strong>Des agents identifiés et fidélisés</strong> — les mêmes personnes, connues et formées, plutôt que des remplaçants au hasard.</li>
<li><strong>Une traçabilité des accès</strong> : qui intervient, quand, avec quelles clés ou badges.</li>
<li><strong>Une formation aux règles de discrétion</strong> : ne pas déplacer les documents, ne pas ouvrir ce qui est fermé, signaler toute anomalie.</li>
</ul>

<h2 id="pratiques">Vos bonnes pratiques internes</h2>
<ul>
<li><strong>Politique « clean desk »</strong> : rien de sensible laissé à l'air libre en fin de journée.</li>
<li><strong>Zones sensibles délimitées</strong> (salle serveur, archives, direction) avec accès restreint, voire exclu du périmètre d'intervention.</li>
<li><strong>Gestion des accès</strong> : badges nominatifs, restitution des clés, changement des codes en cas de rotation.</li>
<li><strong>Un référent unique</strong> côté entreprise pour le prestataire.</li>
</ul>

<h2 id="rgpd">Données personnelles : le rôle du prestataire</h2>
<p>Même sans accès aux systèmes informatiques, un prestataire de nettoyage évolue dans un environnement où circulent des données personnelles (documents RH, dossiers clients). Un partenaire sérieux <strong>forme ses agents à la discrétion</strong> et intègre la confidentialité à ses engagements, en cohérence avec vos obligations RGPD.</p>
<p>Un nettoyage discret et maîtrisé fait partie d'une prestation professionnelle. C'est l'un des principes de notre approche du <a href="https://spn-net.fr/tertiaire/">nettoyage de bureaux</a>.</p>"""

A3 = dict(
    slug="nettoyage-bureaux-confidentialite-securite",
    date="2026-08-21T09:00:00",
    title="Confidentialité : sécuriser le nettoyage de vos bureaux hors présence des équipes",
    seo_title="Nettoyage de bureaux & confidentialité : sécuriser l'accès hors présence | SPN NET",
    desc="Nettoyage de bureaux hors présence : clause de confidentialité, agents identifiés, traçabilité des accès, clean desk. Comment sécuriser vos locaux et vos données.",
    body=A3_BODY,
    faq=[
        ("Comment sécuriser le nettoyage de bureaux réalisé hors présence des équipes ?",
         "En exigeant une clause de confidentialité, des agents identifiés et formés à la discrétion, une traçabilité des accès, et en appliquant en interne une politique clean desk et une gestion stricte des badges."),
        ("Un prestataire de nettoyage est-il concerné par le RGPD ?",
         "Il n'accède pas à vos systèmes, mais il évolue près de données personnelles. Un prestataire sérieux forme ses agents à la discrétion et intègre la confidentialité à ses engagements, en cohérence avec vos obligations."),
        ("Faut-il exclure certaines zones du périmètre de nettoyage ?",
         "Les zones très sensibles (salle serveur, archives, direction) peuvent être à accès restreint, voire exclues du périmètre, ou nettoyées en présence d'un référent."),
    ],
    cta=_cta("Un nettoyage discret et maîtrisé",
             "Agents fidélisés et formés, interventions en horaires décalés sans jamais gêner ni exposer votre activité.",
             "/contact/", "Demander un devis →"),
)

A4_BODY = """<p class="lead">Qualipropre, ISO 9001, Écolabel, ISO 45001, EcoVadis… Les certifications s'affichent partout sur les sites d'entreprises de nettoyage. Mais que garantissent-elles <em>vraiment</em> ? Voici un décryptage clair pour ne pas confondre un vrai repère de qualité avec un simple argument marketing.</p>

<div class="toc"><b>Au sommaire</b><ol>
<li><a href="#pourquoi">Pourquoi les certifications comptent</a></li>
<li><a href="#qualipropre">Qualipropre : le label métier</a></li>
<li><a href="#iso9001">ISO 9001 : le management de la qualité</a></li>
<li><a href="#ecolabel">Écolabel & produits écologiques</a></li>
<li><a href="#spn">Nos certifications : ISO 45001 & EcoVadis</a></li>
<li><a href="#lire">Bien lire une certification</a></li>
</ol></div>

<h2 id="pourquoi">Pourquoi les certifications comptent</h2>
<p>Une certification est un <strong>engagement vérifié par un tiers indépendant</strong>. Elle ne dit pas qu'une entreprise est « la meilleure », mais qu'elle respecte un référentiel précis, contrôlé par audit. C'est un repère objectif dans un secteur où les promesses commerciales se ressemblent.</p>

<h2 id="qualipropre">Qualipropre : le label métier</h2>
<p><strong>Qualipropre</strong> est un label propre au secteur de la propreté. Il atteste du respect de bonnes pratiques professionnelles (organisation, moyens, suivi client) spécifiques au métier du nettoyage. C'est un signe de sérieux <em>sectoriel</em>.</p>

<h2 id="iso9001">ISO 9001 : le management de la qualité</h2>
<p>La norme <strong>ISO 9001</strong> certifie un <em>système de management de la qualité</em> : процессus documentés, écoute client, amélioration continue. Elle n'est pas spécifique au nettoyage — on la retrouve dans tous les secteurs — mais elle garantit une organisation structurée et auditée.</p>

<h2 id="ecolabel">Écolabel & produits écologiques</h2>
<p>Un <strong>Écolabel</strong> (comme l'Écolabel Européen) certifie qu'un <em>produit</em> répond à des critères environnementaux stricts. Attention à la nuance : utiliser des produits écolabellisés est une bonne pratique, mais ce n'est pas la même chose qu'une certification de l'entreprise. Demandez ce qui est réellement labellisé.</p>

<h2 id="spn">Nos certifications : ISO 45001 & EcoVadis</h2>
<p>Chez SPN NET, nous avons choisi de faire vérifier deux engagements qui comptent pour nos clients et nos agents :</p>
<ul>
<li><strong>ISO 45001</strong> — la norme internationale de <em>santé et sécurité au travail</em>, certifiée par DEKRA. Elle protège nos agents… et vos sites.</li>
<li><strong>Médaille d'argent EcoVadis 2025</strong> — une évaluation RSE reconnue qui place SPN NET dans le top 15 % des entreprises évaluées (environnement, social, éthique).</li>
</ul>
<p>Nous préférons afficher ce que nous détenons réellement, plutôt que d'aligner des logos. Le détail est sur notre page <a href="https://spn-net.fr/a-propos/">nos engagements</a>.</p>

<h2 id="lire">Bien lire une certification</h2>
<ul>
<li><strong>Qui certifie ?</strong> Un organisme indépendant reconnu (et non l'entreprise elle-même).</li>
<li><strong>Quoi exactement ?</strong> L'entreprise, un site, un produit ? Le périmètre change tout.</li>
<li><strong>Est-elle à jour ?</strong> Une certification a une date de validité et fait l'objet d'audits de suivi.</li>
</ul>"""

A4 = dict(
    slug="certifications-entreprise-nettoyage",
    date="2026-08-28T09:00:00",
    title="Qualipropre, ISO 9001, Écolabel : ce que garantissent les certifications de nettoyage",
    seo_title="Certifications de nettoyage : Qualipropre, ISO 9001, Écolabel… le guide | SPN NET",
    desc="Qualipropre, ISO 9001, Écolabel, ISO 45001, EcoVadis : ce que garantissent vraiment les certifications d'une entreprise de nettoyage, et comment les lire sans se tromper.",
    body=A4_BODY.replace("процессus", "processus"),
    faq=[
        ("Quelle est la différence entre Qualipropre et ISO 9001 ?",
         "Qualipropre est un label propre au secteur de la propreté (bonnes pratiques métier). ISO 9001 est une norme générale de management de la qualité, applicable à tous les secteurs et vérifiée par audit."),
        ("Un Écolabel certifie-t-il l'entreprise de nettoyage ?",
         "Non : un Écolabel certifie un produit répondant à des critères environnementaux. Utiliser des produits écolabellisés est une bonne pratique, mais ce n'est pas une certification de l'entreprise elle-même."),
        ("Quelles certifications possède SPN NET ?",
         "SPN NET est certifiée ISO 45001 (santé et sécurité au travail, par DEKRA) et a obtenu la médaille d'argent EcoVadis 2025, dans le top 15 % des entreprises évaluées sur la RSE."),
        ("Comment vérifier qu'une certification est sérieuse ?",
         "Vérifiez qui certifie (un organisme indépendant reconnu), ce qui est certifié (entreprise, site ou produit) et la date de validité, une certification faisant l'objet d'audits de suivi."),
    ],
    cta=_cta("Une entreprise de nettoyage certifiée & responsable",
             "ISO 45001, médaille d'argent EcoVadis, équipes formées : découvrez des engagements vérifiés, pas des promesses.",
             "/a-propos/", "Voir nos engagements →"),
)

ARTICLES = [A1, A2, A3, A4]

# Cartes pour l'index /blog/ (tag, titre court, accroche) — clé = slug
BLOG_CARDS = [
    ("annexe-7-changer-entreprise-nettoyage", "Guide", "Annexe 7 : changer sans friction",
     "Ce que dit vraiment la loi sur la reprise des agents quand vous changez de prestataire."),
    ("qualite-nettoyage-baisse-apres-3-mois", "Conseil", "Qualité qui baisse après 3 mois",
     "Pourquoi la propreté s'essouffle passé le démarrage — et comment tenir un niveau constant."),
    ("nettoyage-bureaux-confidentialite-securite", "Sécurité B2B", "Confidentialité au bureau",
     "Sécuriser le nettoyage réalisé hors présence de vos équipes : accès, discrétion, RGPD."),
    ("certifications-entreprise-nettoyage", "Certifications", "Certifications de nettoyage",
     "Qualipropre, ISO 9001, Écolabel, ISO 45001 : ce qu'elles garantissent vraiment."),
]


def rebuild_blog():
    """Reconstruit l'index /blog/ avec les articles réellement PUBLIÉS (statut WP).

    Relançable à tout moment : les articles programmés apparaissent
    automatiquement une fois leur date de publication passée.
    """
    import make_special as ms
    import make_zone as mz
    live = []
    for c in BLOG_CARDS:
        r = requests.get(API, params={"slug": c[0], "status": "publish", "_fields": "id"},
                         auth=AUTH, timeout=30).json()
        if r:
            live.append(c)
    ms.POSTS[:] = live  # posts_section() lit ce global au moment du build
    print(f"  index /blog/ : {len(live)} article(s) publié(s) listé(s)")
    print(mz.deploy("blog", ms.CFG["blog"], builder=ms.build, prefix="special"))


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def get_id(slug):
    r = requests.get(API, params={"slug": slug, "_fields": "id", "status": "publish,future,draft"}, auth=AUTH, timeout=30).json()
    return r[0]["id"] if r else None


def deploy(a, now):
    content = "<!-- wp:html -->\n" + wrap(a["body"], a["faq"], a["cta"]) + "\n<!-- /wp:html -->"
    dt = datetime.datetime.fromisoformat(a["date"])
    status = "publish" if dt <= now else "future"
    payload = {
        "title": a["title"], "slug": a["slug"], "content": content,
        "status": status, "date": a["date"],
        "excerpt": a["desc"],
        "meta": {"slim_seo": {"title": a["seo_title"], "description": a["desc"], "noindex": False}},
    }
    pid = get_id(a["slug"])
    url = f"{API}/{pid}" if pid else API
    r = requests.post(url, auth=AUTH, timeout=90, json=payload)
    r.raise_for_status()
    j = r.json()
    return f"  {'✓' if status=='publish' else '⏳'} [{status}] {j.get('link')}  ({a['date'][:10]})"


def main():
    now = datetime.datetime(2026, 8, 19, 12, 30)
    if len(sys.argv) > 1 and sys.argv[1] == "--restore":
        for a in ARTICLES:
            pid = get_id(a["slug"])
            if pid:
                requests.post(f"{API}/{pid}", auth=AUTH, timeout=60, json={"status": "draft"})
                print("  ↩ brouillon:", a["slug"])
        return
    if len(sys.argv) > 1 and sys.argv[1] == "--blog":
        rebuild_blog()
        return
    for a in ARTICLES:
        try:
            print(deploy(a, now))
        except Exception as ex:  # noqa: BLE001
            print(f"  ✗ {a['slug']}: {ex}")


if __name__ == "__main__":
    main()
