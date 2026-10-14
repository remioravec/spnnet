#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Page /carrieres/ — l'offre d'inspecteur propreté / responsable de secteur.

Demande d'Alexandra Guenantin du 13/10/2026 : retirer le contenu precedent
(« c'est un peu dur ») et publier le poste ouvert, candidatures adressees a
son e-mail.

Tout le contenu provient de la fiche de poste fournie par SPN NET. Aucune
mission, aucune condition, aucun avantage et aucune remuneration ajoutes.
La fiche indique contact@spn-net.fr ; Alexandra a demande que les
candidatures arrivent chez elle : c'est son adresse qui est publiee.

JSON-LD JobPosting a la place de l'Article du gabarit : c'est ce schema qui
rend l'offre eligible a Google Jobs. Adresse et telephone repris des
mentions legales, pas de la signature d'un e-mail.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import navboost as nb      # noqa: E402
import visuels as vz       # noqa: E402

RH = "a.guenantin@spn-net.fr"
OBJET = "Responsable de secteur propreté"
MAILTO = f"mailto:{RH}?subject={OBJET.replace(' ', '%20')}"
DATE = "2026-10-14"

OR, OR2, GR = "#D8431F", "#ED5D37", "#c9bdb2"

# ----------------------------------------------------------------- visuels --
V_BREF = vz.cartes(
    "Le poste en quatre lignes",
    [("CDI", "Temps plein", "Classification selon le profil et la convention collective des entreprises de propreté"),
     ("92220", "Rattaché à Bagneux", "52 avenue de Bourg-la-Reine, à quelques minutes de Paris"),
     ("IDF", "Paris et toute l'Île-de-France", "Un portefeuille de sites à piloter sur l'ensemble du secteur"),
     ("Permis B", "Indispensable", "Déplacements fréquents sur les sites clients")])

V_ROLE = vz.etapes(
    "Votre place dans l'organisation : quatre interlocuteurs quotidiens",
    [("1", "Les clients", "Vous êtes leur interlocuteur privilégié : demandes, réclamations, points de suivi et comptes rendus."),
     ("2", "Les agents et les chefs d'équipe", "Vous les encadrez avec une présence régulière sur le terrain, plannings et remplacements compris."),
     ("3", "Les fonctions support", "Vous transmettez les heures réalisées et les éléments utiles à la paie, et tenez les dossiers à jour."),
     ("4", "La direction de l'exploitation", "C'est votre rattachement hiérarchique, et votre appui sur les situations sensibles.")])

V_MISSIONS = vz.duo(
    "Deux faces du métier, et c'est le terrain qui commande",
    "Ce qui s'organise au bureau",
    ["Construction et mise à jour des plannings, organisation des remplacements",
     "Suivi des stocks, du matériel et des besoins d'approvisionnement",
     "Contrôle des heures réalisées et transmission des éléments de paie",
     "Comptes rendus de suivi client et propositions d'amélioration",
     "Participation aux devis et avenants avec la direction commerciale"],
    "Ce qui se joue sur les sites",
    ["Visites et contrôles qualité sur les sites confiés",
     "Vérification du respect des cahiers des charges, écart par écart",
     "Démarrage des nouveaux contrats : moyens humains, matériel, produits",
     "Encadrement direct des agents et des chefs d'équipe",
     "Application des consignes de sécurité et des protocoles propres à chaque site"])

V_PROFIL = vz.duo(
    "Ce que nous attendons, et ce qui fera la différence",
    "Indispensable",
    ["Une connaissance du secteur de la propreté",
     "Avoir déjà piloté plusieurs sites ou encadré des équipes de nettoyage",
     "Le permis B",
     "De l'aisance avec les clients, les outils bureautiques et le suivi administratif"],
    "Apprécié",
    ["La maîtrise du portugais, pour accompagner certaines équipes",
     "Le goût du terrain et l'autonomie dans l'organisation d'un secteur",
     "La capacité à gérer les imprévus et les situations sensibles avec calme",
     "Le sens des priorités quand plusieurs sites appellent le même matin"])

V_POURQUOI = vz.cartes(
    "Quatre raisons qui tiennent au fonctionnement de l'entreprise",
    [("30 ans", "Une entreprise locale", "Circuits de décision courts et contact direct avec la direction"),
     ("350", "clients professionnels", "Bureaux, commerces, santé, copropriétés, industrie, événementiel"),
     ("ISO 45001", "Santé et sécurité au travail", "Certification en vigueur, pas une déclaration d'intention"),
     ("EcoVadis", "Médaille d'argent", "Une démarche RSE évaluée par un tiers")])

TABLEAU = """<div class="tbl-wrap"><table class="tbl">
<caption>Les conditions, telles qu'elles figurent dans la fiche de poste</caption>
<thead><tr><th>Poste</th><th>Ce qui est fixé</th></tr></thead>
<tbody>
<tr><td>Contrat</td><td>CDI à temps plein</td></tr>
<tr><td>Rattachement</td><td>Bagneux, dans les Hauts-de-Seine</td></tr>
<tr><td>Secteur</td><td>Paris et toute l'Île-de-France</td></tr>
<tr><td>Déplacements</td><td>Fréquents sur les sites clients. Permis B indispensable</td></tr>
<tr><td>Rémunération</td><td>Selon l'expérience et le niveau de responsabilité confié</td></tr>
<tr><td>Classification</td><td>Selon le profil et la convention collective nationale des entreprises de propreté</td></tr>
<tr><td>Horaires</td><td>Souplesse nécessaire selon les interventions du matin, du soir et les urgences</td></tr>
<tr><td>Outils</td><td>Téléphone et outils professionnels fournis. Mobilité précisée en entretien</td></tr>
</tbody></table></div>"""

CTA = vz.cta(
    "Le poste vous parle ? Un CV suffit pour ouvrir la discussion.",
    MAILTO, "Envoyer ma candidature")

BODY = f"""<p class="lead">SPN NET recrute un inspecteur propreté et responsable de secteur, en CDI à temps plein. Le poste est rattaché à Bagneux, dans les Hauts-de-Seine, et couvre Paris et toute l'Île-de-France. Il s'adresse à une personne présente sur le terrain, organisée, et capable de décider vite.</p>

<h2 id="bref">Le poste en bref</h2>

<p>Vous pilotez un portefeuille de sites, vous accompagnez les équipes de terrain et vous garantissez la qualité des prestations auprès de nos clients. Le poste combine le contrôle qualité, l'encadrement et la relation client : les trois se tiennent, et c'est la même personne qui les porte.</p>

<p>SPN NET est une entreprise indépendante implantée à Bagneux. Depuis 30 ans, nos équipes accompagnent plus de 350 clients professionnels à Paris et en Île-de-France : bureaux, commerces, établissements de santé, copropriétés, sites industriels et lieux événementiels. L'entreprise est certifiée ISO 45001 et médaillée d'argent EcoVadis.</p>

{{V_BREF}}

<h2 id="role">Votre rôle au quotidien</h2>

<p>Rattaché à la direction de l'exploitation, vous êtes le lien quotidien entre les clients, les agents, les chefs d'équipe et les fonctions support. Vous veillez au respect des cahiers des charges, à la continuité des prestations et à la satisfaction des clients.</p>

<p>Concrètement, cela veut dire que vous passez une part importante de votre semaine sur les sites, et le reste à organiser ce que vous y avez constaté. Ce n'est pas un poste qui se tient depuis un bureau.</p>

{{V_ROLE}}

<h2 id="missions">Vos missions</h2>

<h3>Pilotage des sites et contrôle qualité</h3>

<p>Organiser les prestations sur les sites confiés et vérifier le respect des cahiers des charges. Réaliser des visites et des contrôles qualité, identifier les écarts et suivre les actions correctives. Préparer les démarrages de nouveaux contrats et mettre en place les moyens humains, matériels et produits nécessaires. Suivre les stocks, le matériel et les besoins d'approvisionnement des équipes.</p>

<h3>Management des équipes</h3>

<p>Encadrer les agents et les chefs d'équipe avec une présence régulière sur le terrain. Construire et actualiser les plannings, puis organiser les remplacements en cas d'absence ou d'urgence. Participer au recrutement, à l'intégration et à la formation des nouveaux collaborateurs. Faire appliquer les consignes de sécurité, les méthodes de travail et les protocoles propres à chaque site.</p>

<h3>Relation client et suivi administratif</h3>

<p>Être l'interlocuteur privilégié des clients, traiter leurs demandes et apporter une réponse rapide aux réclamations. Organiser les points de suivi, formaliser les comptes rendus et proposer des améliorations adaptées aux sites. Contrôler les heures réalisées, transmettre les éléments utiles à la paie et maintenir les dossiers à jour. Participer aux devis, avenants et ajustements de prestations en lien avec la direction commerciale.</p>

{{V_MISSIONS}}

<h2 id="profil">Le profil que nous cherchons</h2>

<p>Vous connaissez le secteur de la propreté et vous avez déjà piloté plusieurs sites ou encadré des équipes de nettoyage. Vous savez gérer les priorités, les imprévus et les situations sensibles avec calme et fermeté. Vous êtes à l'aise avec les clients, les outils bureautiques et le suivi administratif. Vous appréciez le terrain et vous travaillez avec autonomie, méthode et sens du service.</p>

<p>Le permis B est indispensable. La maîtrise du portugais constitue un plus pour accompagner certaines équipes.</p>

{{V_PROFIL}}

{{CTA}}

<h2 id="pourquoi">Pourquoi rejoindre SPN NET</h2>

<p>Une entreprise locale avec des circuits de décision courts et un contact direct avec la direction. Un portefeuille varié de sites professionnels et une véritable autonomie dans l'organisation du secteur. L'appui des équipes exploitation et ressources humaines pour le recrutement, le suivi et les situations urgentes. Une entreprise engagée dans la qualité, la santé et la sécurité au travail ainsi que dans une démarche RSE reconnue.</p>

{{V_POURQUOI}}

<h2 id="conditions">Les conditions du poste</h2>

<p>La rémunération se fixe selon l'expérience et le niveau de responsabilité confié ; elle se discute en entretien. La classification suit le profil et la convention collective nationale des entreprises de propreté.</p>

{TABLEAU}

<h2 id="postuler">Postuler</h2>

<p>Envoyez votre CV à <a href="{MAILTO}">{RH}</a>, avec pour objet <b>{OBJET}</b>. Votre candidature arrive directement chez Alexandra Guenantin, responsable de secteurs, qui vous répondra.</p>

<p>Les candidatures se font par e-mail et non par le formulaire de devis du site : celui-ci part vers l'équipe commerciale et ne comporte pas de champ pour un CV.</p>
"""

VISUELS = {"{V_BREF}": V_BREF, "{V_ROLE}": V_ROLE, "{V_MISSIONS}": V_MISSIONS,
           "{V_PROFIL}": V_PROFIL, "{V_POURQUOI}": V_POURQUOI, "{CTA}": CTA}

FAQ = [
 ("Quel est le poste ouvert chez SPN NET ?",
  "Un poste d'inspecteur propreté et responsable de secteur, en CDI à temps plein, rattaché à Bagneux dans les Hauts-de-Seine, sur un secteur qui couvre Paris et l'Île-de-France. Il consiste à piloter un portefeuille de sites, encadrer les équipes de terrain et assurer la relation avec les clients."),
 ("Comment postuler ?",
  f"Envoyez votre CV à {RH} avec pour objet « {OBJET} ». La candidature arrive directement chez la responsable de secteurs."),
 ("Le permis B est-il obligatoire ?",
  "Oui. Les déplacements sur les sites clients sont fréquents, à Paris et en Île-de-France, et le permis B est indispensable pour tenir le poste."),
 ("Quelle est la rémunération proposée ?",
  "Elle se fixe selon l'expérience et le niveau de responsabilité confié, et se discute en entretien. La classification suit la convention collective nationale des entreprises de propreté."),
 ("Faut-il parler portugais ?",
  "Ce n'est pas une condition. La maîtrise du portugais constitue un plus, pour accompagner certaines équipes."),
 ("Peut-on postuler via le formulaire du site ?",
  "Non. Le formulaire présent sur les pages du site part vers l'équipe commerciale et ne comporte pas de champ pour un CV. Les candidatures passent par l'adresse e-mail indiquée sur cette page."),
]

A = dict(
    slug="carrieres",
    # Le site est en UTC : une heure « ronde » du jour meme repasse la page en
    # « programmee » et la sort du site. On date au matin, en UTC.
    date=DATE + "T06:00:00",
    title="Inspecteur propreté et responsable de secteur — CDI, Paris et Île-de-France",
    seo_title="Recrutement — Inspecteur propreté / responsable de secteur | SPN NET",
    desc="SPN NET recrute un inspecteur propreté et responsable de secteur en CDI temps plein, rattaché à Bagneux (92), sur Paris et l'Île-de-France. Missions, profil, conditions et candidature.",
    hero_stats=[("CDI", "temps plein"), ("Bagneux", "Hauts-de-Seine"),
                ("Paris & IDF", "secteur couvert")],
    body=BODY, faq=FAQ,
)


def job_schema():
    node = {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "title": "Inspecteur propreté et responsable de secteur",
        "description": (
            "<p>SPN NET recrute un inspecteur propreté et responsable de secteur en CDI à temps plein. "
            "Vous pilotez un portefeuille de sites, accompagnez les équipes de terrain et garantissez la "
            "qualité des prestations auprès des clients.</p>"
            "<p>Missions : organisation des prestations et contrôle du respect des cahiers des charges, "
            "visites et contrôles qualité, préparation des démarrages de contrats, suivi des stocks et du "
            "matériel, encadrement des agents et des chefs d'équipe, plannings et remplacements, "
            "participation au recrutement et à la formation, application des consignes de sécurité, "
            "relation client et traitement des réclamations, comptes rendus de suivi, contrôle des heures "
            "et éléments de paie, participation aux devis et avenants.</p>"
            "<p>Profil : connaissance du secteur de la propreté, expérience du pilotage de plusieurs sites "
            "ou de l'encadrement d'équipes de nettoyage, aisance avec les clients et le suivi "
            "administratif, autonomie et sens du service. Permis B indispensable. La maîtrise du portugais "
            "est un plus.</p>"),
        "datePosted": DATE,
        "employmentType": "FULL_TIME",
        "industry": "Propreté et services aux entreprises",
        "hiringOrganization": {
            "@type": "Organization", "name": "SPN NET",
            "sameAs": "https://spn-net.fr/",
            "logo": "https://spn-net.fr/wp-content/uploads/elementor/thumbs/logo-rkamhcg62qbiqacow1pw230in940ue5954a7aysbu0.png",
        },
        "jobLocation": {
            "@type": "Place",
            "address": {"@type": "PostalAddress",
                        "streetAddress": "52 avenue de Bourg-la-Reine",
                        "addressLocality": "Bagneux",
                        "postalCode": "92220",
                        "addressRegion": "Île-de-France",
                        "addressCountry": "FR"},
        },
        "qualifications": "Permis B. Expérience du pilotage de plusieurs sites ou de l'encadrement d'équipes de nettoyage.",
        "skills": "Contrôle qualité, management d'équipes de propreté, relation client, planification",
        "applicantContact": {"@type": "ContactPoint", "email": RH},
        "url": "https://spn-net.fr/carrieres/",
    }
    return ('<script type="application/ld+json">'
            + json.dumps(node, ensure_ascii=False) + "</script>")


def main():
    import make_article as ma
    import make_septembre as msept
    ma.TAGS.update({"carrieres": "Recrutement"})

    a = dict(A)
    b = a["body"]
    for k, v in VISUELS.items():
        b = b.replace(k, v)
    reste = re.findall(r"\{V_[A-Z_]+\}|\{CTA\}", b)
    if reste:
        raise SystemExit(f"jetons non résolus : {set(reste)}")
    a["body"] = b

    html = ma.build_article(a)

    # NB_CSS est du CSS brut : il se pose DANS la balise style.
    if "</style>" in html:
        html = html.replace("</style>", nb.NB_CSS + "</style>", 1)
    else:
        html = "<style>" + nb.NB_CSS + "</style>" + html
    html += vz.CSS + vz.EXTRA

    # Le gabarit article pose un Article + un fil « Blog » : ni l'un ni
    # l'autre ne decrivent une offre d'emploi.
    html = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "Article".*?</script>',
                  job_schema(), html, count=1, flags=re.S)
    html = html.replace(
        '{"@type":"ListItem","position":2,"name":"Blog","item":"https://spn-net.fr/blog/"}',
        '{"@type":"ListItem","position":2,"name":"Carrieres","item":"https://spn-net.fr/carrieres/"}')
    html = html.replace(
        '<a href="https://spn-net.fr/blog/">Blog</a> › ', '')
    # la note Google n'a rien a faire sur une offre d'emploi
    html = re.sub(r'<span class="rate">.*?</span>\s*</span>', '', html, count=1, flags=re.S)
    html = re.sub(r'<span class="rate"><span class="s">★</span> <b>4,8/5</b> · 48 avis</span>',
                  '', html, count=1)

    html = html.rstrip()
    html = html[: html.rfind("</div>")] + nb.NB_JS + html[html.rfind("</div>"):]

    out = os.path.join(os.path.dirname(__file__), "article-carrieres.html")
    open(out, "w", encoding="utf-8").write(html)
    n = len(re.findall(r'<a\b[^>]*href="https://spn-net\.fr/', html))
    v = html.count('class="vz rv"')
    print(f"  carrieres  {len(html)} o · {v} visuels · {n} liens internes"
          + ("  [simulation]" if "--dry" in sys.argv else ""))
    if "--dry" not in sys.argv:
        print("   ", msept.deploy(a, html))


if __name__ == "__main__":
    main()
