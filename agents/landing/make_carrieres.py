#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Page /carrieres/ — SPN NET ne traite pas les candidatures via le site.

Le site est premier sur « société de nettoyage recrutement » : les candidats
arrivent et utilisent le formulaire de devis, faute d'autre porte. La page
capte cette requête et dit la chose clairement, au lieu de laisser le
formulaire commercial absorber des candidatures.

Aucune procédure de recrutement n'est inventée : la page dit ce qui ne se
fait pas. Le canal réel reste à fournir par SPN NET.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import navboost as nb

BODY = """<p class="lead">SPN NET ne reçoit pas les candidatures par ce site. Le formulaire que vous voyez sur nos pages est réservé aux demandes de devis des entreprises, des syndics et des commerces. Une candidature envoyée par ce formulaire n'est pas transmise au service concerné.</p>

<h2 id="pourquoi">Pourquoi le formulaire du site ne convient pas</h2>

<p>Le formulaire de nos pages alimente le suivi commercial : il ne demande qu'un nom, un e-mail et un téléphone, et part vers l'équipe qui établit les devis. Il n'a ni champ pour un CV, ni destinataire côté ressources humaines.</p>

<p>Concrètement, une candidature déposée par cette voie arrive dans une liste de prospects. Elle n'est ni lue comme une candidature, ni orientée, ni conservée. Ce n'est pas un choix de tri : c'est simplement le mauvais tuyau.</p>

<h2 id="postuler">Comment postuler chez SPN NET</h2>

<p>Les recrutements de SPN NET ne passent pas par ce site. Si vous souhaitez rejoindre nos équipes, adressez-vous directement à l'entreprise par les coordonnées figurant sur nos mentions légales, en précisant qu'il s'agit d'une candidature.</p>

<p>Nous préférons vous le dire plutôt que de laisser un formulaire absorber votre démarche sans suite. Le temps que vous y passez mérite d'arriver au bon endroit.</p>

<h2 id="devis">Vous cherchiez un devis ?</h2>

<p>Si vous êtes une entreprise, un syndic ou un commerçant et que vous cherchez un prestataire de propreté, vous êtes au bon endroit, mais pas sur la bonne page. Notre offre pour les locaux professionnels est détaillée sur notre page <a href="https://spn-net.fr/tertiaire/">nettoyage de bureaux à Paris</a>, et celle pour les immeubles sur notre page <a href="https://spn-net.fr/copropriete-et-habitat/">nettoyage de copropriété</a>.</p>

<p>Avant de consulter, il est utile d'écrire ce que vous attendez : notre <a href="https://spn-net.fr/cahier-des-charges-nettoyage-bureaux/">cahier des charges de nettoyage</a> se remplit zone par zone, et notre <a href="https://spn-net.fr/choisir-entreprise-nettoyage/">guide pour choisir une entreprise de nettoyage</a> réunit les dix points à vérifier avant de signer.</p>
"""

FAQ = [
 ("Peut-on postuler chez SPN NET via le site ?",
  "Non. Le formulaire présent sur les pages du site est réservé aux demandes de devis professionnelles. Il ne comporte aucun champ pour un CV et n'est pas transmis au service chargé des recrutements. Une candidature envoyée par cette voie n'est pas traitée."),
 ("Où envoyer sa candidature ?",
  "Directement à l'entreprise, par les coordonnées figurant sur nos mentions légales, en indiquant clairement qu'il s'agit d'une candidature et non d'une demande de devis."),
 ("Pourquoi le site apparaît-il sur les recherches d'emploi en nettoyage ?",
  "Parce que nos pages traitent du métier de la propreté et que les moteurs les remontent sur des requêtes voisines. Cette page existe précisément pour lever l'ambiguïté : le site de SPN NET est un site commercial, pas un site de recrutement."),
 ("Le formulaire de devis conserve-t-il les candidatures reçues ?",
  "Les demandes reçues par le formulaire sont enregistrées dans le suivi commercial. Une candidature qui y arrive n'est ni orientée vers les ressources humaines, ni conservée comme candidature. Il vaut mieux ne pas l'utiliser pour cela."),
]

A = dict(
    slug="carrieres",
    date="2026-10-07T09:00:00",
    title="Carrières : SPN NET ne reçoit pas les candidatures par le site",
    seo_title="Carrières — candidatures : SPN NET ne les reçoit pas par le site",
    desc="SPN NET ne traite pas les candidatures via le formulaire du site, réservé aux demandes de devis. Où adresser votre candidature, et ce que devient une candidature envoyée par erreur.",
    hero_stats=[("Devis", "ce que fait le formulaire"), ("Candidature", "ce qu'il ne fait pas"),
                ("3 champs", "ni CV, ni destinataire RH")],
    body=BODY, faq=FAQ,
)


def main():
    import make_article as ma
    import make_septembre as msept
    ma.TAGS.update({"carrieres": "Information"})
    html = ma.build_article(A)
    if "</style>" in html:
        html = html.replace("</style>", nb.NB_CSS + "</style>", 1)
    html = html.rstrip()
    html = html[: html.rfind("</div>")] + nb.NB_JS + html[html.rfind("</div>"):]
    open(os.path.join(os.path.dirname(__file__), "article-carrieres.html"), "w",
         encoding="utf-8").write(html)
    n = len(re.findall(r'<a\b[^>]*href="https://spn-net\.fr/', html))
    print(f"  carrieres  {len(html)} o · {n} liens internes")
    if "--dry" not in sys.argv:
        print("   ", msept.deploy(A, html))


if __name__ == "__main__":
    main()
