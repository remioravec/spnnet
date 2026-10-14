# -*- coding: utf-8 -*-
"""Données locales RÉELLES des 13 communes 92/94 autour de Bagneux (siège SPN NET).

Contenu unique par commune (anti-doorway) : tissu tertiaire, quartiers/zones
d'activité, accès, maillage croisé. Aucune offre inventée — on décrit le terrain
et les attributs réels de SPN NET (base à Bagneux, ISO 45001, horaires décalés,
devis 24h). Schéma identique à zones_data.ALL_ZONES + champ 'cp' pour areaServed.
"""

def _e(name, cp, lead, p1, p2, quartiers, neighbors):
    return {
        "name": name, "short": cp, "zone": f"{name} ({cp})", "cp": cp,
        "title": f"Société de nettoyage de bureaux à {name} ({cp}) | SPN NET",
        "desc": (f"Société de nettoyage de bureaux à {name} ({cp}) : {', '.join(quartiers[:3])}. "
                 f"Basée à Bagneux, proximité immédiate. Interventions soir & matin, ISO 45001, 4,8/5. Devis 24h."),
        "eyebrow": f"Nettoyage de bureaux · {name} ({cp})",
        "h1": f"Société de <em>nettoyage de bureaux</em> à {name} ({cp})",
        "lead": lead, "p1": p1, "p2": p2,
        "quartiers": quartiers, "neighbors": neighbors,
    }


COMMUNES = {
    "bagneux": _e(
        "Bagneux", "92220",
        "<b>Bagneux, c'est chez nous</b> : notre siège s'y trouve, avenue de Bourg-la-Reine. "
        "Nous entretenons les bureaux, PME et locaux tertiaires de la commune avec la réactivité d'un "
        "prestataire installé sur place. Interventions <span class=\"hl\">avant 9h ou après 18h</span> — "
        "<span class=\"hl\">devis sous 24h</span>.",
        "Bagneux connaît une forte mutation tertiaire autour de l'<b>écoquartier Victor Hugo</b> et de la "
        "nouvelle station <b>Bagneux – Lucie Aubrac</b> (M4), qui attire bureaux, sièges de PME et activités "
        "de services. Le tissu économique mêle petites et moyennes entreprises, artisans et locaux mixtes.",
        "Notre siège social est <b>à Bagneux même</b> : aucune commune ne bénéficie d'une réactivité "
        "équivalente. Équipes mobiles à quelques minutes, interventions en horaires décalés sur tous types "
        "de locaux, du plateau de bureaux à la PME de quartier.",
        ["Écoquartier Victor Hugo", "Centre-ville", "Pierre Plate", "Les Blagis", "Fort de Bagneux", "M4 Lucie Aubrac"],
        [["montrouge", "Montrouge", "limitrophe nord"], ["malakoff", "Malakoff", "à proximité"],
         ["chatillon", "Châtillon", "limitrophe ouest"], ["paris-14", "Paris 14e", "porte d'Orléans"]],
    ),
    "montrouge": _e(
        "Montrouge", "92120",
        "Aux portes de Paris 14e, <b>Montrouge</b> concentre sièges et bureaux : nous y entretenons vos "
        "locaux tertiaires avec des équipes basées juste à côté, à Bagneux. Interventions "
        "<span class=\"hl\">avant 9h ou après 18h</span> — <span class=\"hl\">devis sous 24h</span>.",
        "Montrouge est l'une des communes les plus tertiaires de la petite couronne : on y trouve de grands "
        "<b>sièges sociaux</b> (dont celui du Crédit Agricole), des immeubles de bureaux autour de la "
        "<b>Mairie de Montrouge</b> (M4) et de l'avenue Aristide Briand, et un tissu dense de PME et cabinets.",
        "À la frontière immédiate du 14e, Montrouge combine immeubles récents et bâti mixte aux accès "
        "parfois contraints. Notre base voisine à <b>Bagneux</b> nous permet d'intervenir tôt le matin ou "
        "en soirée sans perturber l'activité des entreprises.",
        ["Mairie de Montrouge", "Aristide Briand", "Jean Jaurès", "Portes de Montrouge", "Cimetière", "M4 / M13"],
        [["paris-14", "Paris 14e", "porte de Montrouge"], ["malakoff", "Malakoff", "limitrophe ouest"],
         ["bagneux", "Bagneux", "limitrophe sud — notre siège"], ["arcueil", "Arcueil", "limitrophe est"]],
    ),
    "malakoff": _e(
        "Malakoff", "92240",
        "<b>Malakoff</b>, entre Paris 14e/15e et Montrouge : PME, agences et studios y côtoient un tissu "
        "artisanal actif. Nous entretenons vos bureaux depuis notre base toute proche de Bagneux. "
        "Interventions <span class=\"hl\">soir et matin</span> — <span class=\"hl\">devis sous 24h</span>.",
        "Desservie par la ligne 13 (<b>Malakoff – Plateau de Vanves</b>, <b>Malakoff – Rue Étienne Dolet</b>), "
        "la commune accueille agences de communication, studios, PME de services et ateliers, souvent dans "
        "des <b>immeubles mixtes</b> et anciens locaux d'activité réhabilités.",
        "Ce bâti mixte, aux horaires d'occupation variés, demande un prestataire souple et réactif. Depuis "
        "<b>Bagneux</b>, nos équipes interviennent en horaires décalés et adaptent la fréquence à chaque type "
        "de local.",
        ["Centre-ville", "Plateau de Vanves", "Étienne Dolet", "Barrouge", "Stade Marcel Cerdan", "M13"],
        [["paris-14", "Paris 14e", "limitrophe"], ["montrouge", "Montrouge", "limitrophe est"],
         ["chatillon", "Châtillon", "limitrophe sud"], ["bagneux", "Bagneux", "à proximité — notre siège"]],
    ),
    "chatillon": _e(
        "Châtillon", "92320",
        "<b>Châtillon</b> mêle zones d'activité, bureaux et PME autour du pôle Châtillon-Montrouge. Nous y "
        "assurons l'entretien de vos locaux depuis notre siège voisin de Bagneux. Interventions "
        "<span class=\"hl\">avant 9h ou après 18h</span> — <span class=\"hl\">devis sous 24h</span>.",
        "Autour de la station <b>Châtillon – Montrouge</b> (terminus M13) et des zones d'activité de la "
        "commune se concentrent bureaux, PME industrielles et locaux de services. Le <b>tramway T6</b> et "
        "la densification renforcent ce tissu tertiaire.",
        "Des plateaux de bureaux aux locaux d'activité, chaque site a ses contraintes. Notre proximité "
        "depuis <b>Bagneux</b> (commune limitrophe) garantit une intervention rapide, en horaires décalés, "
        "avec un interlocuteur dédié.",
        ["Châtillon-Montrouge", "Centre-ville", "Parc Robespierre", "Zones d'activité", "Val de Bièvre", "M13 / T6"],
        [["montrouge", "Montrouge", "limitrophe"], ["malakoff", "Malakoff", "limitrophe nord"],
         ["bagneux", "Bagneux", "limitrophe est — notre siège"], ["clamart", "Clamart", "limitrophe ouest"]],
    ),
    "clamart": _e(
        "Clamart", "92140",
        "<b>Clamart</b>, de la gare du Grand Paris aux zones d'activité : bureaux, PME et sièges y trouvent "
        "un cadre en plein essor. Nous entretenons vos locaux depuis notre base proche de Bagneux. "
        "Interventions <span class=\"hl\">soir et matin</span> — <span class=\"hl\">devis sous 24h</span>.",
        "Clamart se transforme avec l'arrivée du <b>Grand Paris Express</b> (gare Clamart) et développe des "
        "programmes tertiaires et des zones d'activité (secteur <b>Novéos</b>). PME, sièges et locaux mixtes "
        "y côtoient un habitat dense autour du centre et du Petit-Clamart.",
        "Cette diversité de locaux appelle des protocoles adaptés. Depuis <b>Bagneux</b>, nos équipes "
        "interviennent en horaires décalés et ajustent fréquence et prestations à chaque site.",
        ["Gare de Clamart", "Novéos", "Centre-ville", "Petit-Clamart", "Jardin Parisien", "Trivaux"],
        [["chatillon", "Châtillon", "limitrophe est"], ["fontenay-aux-roses", "Fontenay-aux-Roses", "limitrophe sud"],
         ["malakoff", "Malakoff", "à proximité"], ["92-hauts-de-seine", "Hauts-de-Seine (92)", "le département"]],
    ),
    "fontenay-aux-roses": _e(
        "Fontenay-aux-Roses", "92260",
        "<b>Fontenay-aux-Roses</b> associe PME, professions libérales et pôle de recherche. Nous entretenons "
        "vos bureaux avec la réactivité d'une équipe basée juste à côté, à Bagneux. Interventions "
        "<span class=\"hl\">avant 9h ou après 18h</span> — <span class=\"hl\">devis sous 24h</span>.",
        "Desservie par le RER B, la commune accueille un tissu de PME, cabinets et professions libérales, "
        "ainsi que le centre de recherche du <b>CEA</b>. Le centre-ville et les quartiers des Blagis et "
        "Scarron mêlent locaux de services et habitat.",
        "Ces locaux, souvent de taille moyenne, demandent un entretien régulier et discret. Notre siège "
        "limitrophe de <b>Bagneux</b> assure une intervention rapide, en horaires décalés, avec un "
        "interlocuteur unique.",
        ["Centre-ville", "Les Blagis", "Scarron", "Pervenches", "Val Content", "RER B"],
        [["bagneux", "Bagneux", "limitrophe est — notre siège"], ["chatillon", "Châtillon", "limitrophe nord"],
         ["clamart", "Clamart", "limitrophe ouest"], ["sceaux", "Sceaux", "limitrophe sud"]],
    ),
    "bourg-la-reine": _e(
        "Bourg-la-Reine", "92340",
        "<b>Bourg-la-Reine</b>, carrefour du sud 92 : commerces, PME et cabinets y animent un centre dense "
        "autour du RER B. Nous entretenons vos bureaux depuis notre base voisine de Bagneux. Interventions "
        "<span class=\"hl\">soir et matin</span> — <span class=\"hl\">devis sous 24h</span>.",
        "Autour de la gare <b>RER B</b> et de l'avenue du Général Leclerc (RD920), Bourg-la-Reine concentre "
        "commerces, cabinets, professions libérales et PME de services, dans un bâti de centre-ville et "
        "d'immeubles mixtes.",
        "Ces locaux au cœur d'un secteur passant exigent un entretien soigné et régulier. Depuis "
        "<b>Bagneux</b>, commune voisine, nous intervenons tôt le matin ou en soirée, avec un interlocuteur "
        "dédié et un devis sous 24h.",
        ["Centre-ville", "Gare RER B", "Général Leclerc (RD920)", "Le Chai", "Les Bas Coquarts", "Faïencerie"],
        [["sceaux", "Sceaux", "limitrophe sud"], ["cachan", "Cachan", "limitrophe est"],
         ["bagneux", "Bagneux", "limitrophe nord — notre siège"], ["antony", "Antony", "à proximité"]],
    ),
    "sceaux": _e(
        "Sceaux", "92330",
        "<b>Sceaux</b>, ville universitaire et résidentielle : cabinets, PME et pôle d'enseignement y "
        "cohabitent. Nous entretenons vos bureaux avec des équipes basées tout près, à Bagneux. Interventions "
        "<span class=\"hl\">avant 9h ou après 18h</span> — <span class=\"hl\">devis sous 24h</span>.",
        "Autour du <b>Parc de Sceaux</b>, du centre historique et de la <b>Faculté Jean Monnet</b> "
        "(droit-économie), la commune accueille cabinets, professions libérales, PME de services et "
        "établissements d'enseignement, desservis par le RER B (Sceaux, Robinson).",
        "Ces locaux, du cabinet au petit siège, demandent un entretien méticuleux et discret. Notre "
        "proximité depuis <b>Bagneux</b> permet des interventions réactives en horaires décalés.",
        ["Centre historique", "Parc de Sceaux", "Robinson", "Faculté Jean Monnet", "Les Blagis", "RER B"],
        [["bourg-la-reine", "Bourg-la-Reine", "limitrophe nord"], ["fontenay-aux-roses", "Fontenay-aux-Roses", "limitrophe"],
         ["antony", "Antony", "limitrophe sud"], ["92-hauts-de-seine", "Hauts-de-Seine (92)", "le département"]],
    ),
    "antony": _e(
        "Antony", "92160",
        "<b>Antony</b>, principal pôle du sud 92 : pôle tertiaire de la Croix de Berny, PME et zones "
        "d'activité. Nous entretenons vos bureaux depuis notre base des Hauts-de-Seine, à Bagneux. "
        "Interventions <span class=\"hl\">soir et matin</span> — <span class=\"hl\">devis sous 24h</span>.",
        "Antony accueille le pôle tertiaire de la <b>Croix de Berny</b> (bureaux, sièges, le long de l'A86 "
        "et de la RD920), des zones d'activité et un centre-ville dynamique, desservis par le RER B et le "
        "tramway <b>T10</b>. Le tissu mêle sièges, PME et services.",
        "Des plateaux de bureaux de la Croix de Berny aux PME du centre, chaque site a ses exigences. Nos "
        "équipes, basées à <b>Bagneux</b>, interviennent en horaires décalés avec un interlocuteur dédié.",
        ["Croix de Berny", "Centre-ville", "La Fontaine", "Le Noyer Doré", "Pajeaud", "RER B / T10"],
        [["sceaux", "Sceaux", "limitrophe nord"], ["bourg-la-reine", "Bourg-la-Reine", "limitrophe"],
         ["fontenay-aux-roses", "Fontenay-aux-Roses", "à proximité"], ["92-hauts-de-seine", "Hauts-de-Seine (92)", "le département"]],
    ),
    "arcueil": _e(
        "Arcueil", "94110",
        "<b>Arcueil</b> concentre un pôle de bureaux majeur le long de l'A6 et du RER B. Nous entretenons "
        "vos locaux tertiaires avec des équipes basées tout près, à Bagneux. Interventions "
        "<span class=\"hl\">avant 9h ou après 18h</span> — <span class=\"hl\">devis sous 24h</span>.",
        "Le secteur <b>La Vache Noire</b> / <b>Laplace</b> et les abords de l'A6 forment l'un des pôles "
        "tertiaires les plus denses du Val-de-Marne : immeubles de bureaux, sièges et campus d'entreprises, "
        "desservis par le RER B (Laplace, Arcueil-Cachan).",
        "Ces grands plateaux de bureaux, occupés en continu, exigent des interventions en horaires décalés. "
        "Notre base proche de <b>Bagneux</b> (commune voisine) garantit réactivité et suivi par un "
        "interlocuteur unique.",
        ["La Vache Noire", "Laplace", "Chaperon Vert", "Centre-ville", "Bords de Bièvre", "RER B / A6"],
        [["paris-14", "Paris 14e", "à proximité"], ["gentilly", "Gentilly", "limitrophe est"],
         ["cachan", "Cachan", "limitrophe sud"], ["94-val-de-marne", "Val-de-Marne (94)", "le département"]],
    ),
    "cachan": _e(
        "Cachan", "94230",
        "<b>Cachan</b>, ville d'enseignement et de PME au sud du 94 : nous entretenons vos bureaux et locaux "
        "avec la réactivité d'une équipe basée tout près, à Bagneux. Interventions "
        "<span class=\"hl\">soir et matin</span> — <span class=\"hl\">devis sous 24h</span>.",
        "Traversée par le RER B (Arcueil-Cachan, Bagneux), Cachan accueille un tissu de PME, de laboratoires "
        "et d'établissements d'enseignement supérieur (campus historique de l'<b>ENS</b>), ainsi que des "
        "locaux de services autour du Coteau et de la Plaine.",
        "Du laboratoire au bureau de PME, chaque local a son protocole. Depuis <b>Bagneux</b>, commune "
        "limitrophe, nos équipes interviennent rapidement, en horaires décalés, sans gêner votre activité.",
        ["Le Coteau", "La Plaine", "Centre-ville", "Camp de Cachan", "Bords de Bièvre", "RER B"],
        [["arcueil", "Arcueil", "limitrophe nord"], ["bagneux", "Bagneux", "limitrophe ouest — notre siège"],
         ["bourg-la-reine", "Bourg-la-Reine", "limitrophe"], ["94-val-de-marne", "Val-de-Marne (94)", "le département"]],
    ),
    "gentilly": _e(
        "Gentilly", "94250",
        "<b>Gentilly</b>, aux portes de Paris 13e/14e : sièges et bureaux de la vallée de la Bièvre. Nous "
        "entretenons vos locaux depuis notre base des Hauts-de-Seine, à Bagneux. Interventions "
        "<span class=\"hl\">avant 9h ou après 18h</span> — <span class=\"hl\">devis sous 24h</span>.",
        "Le long du <b>Val de Bièvre</b> et de l'A6a, Gentilly accueille des sièges et immeubles de bureaux, "
        "des PME et des locaux de services, aux portes immédiates de Paris et du RER B.",
        "Ces immeubles tertiaires, souvent de belle superficie, demandent des interventions en horaires "
        "décalés. Notre proximité depuis <b>Bagneux</b> assure réactivité et régularité.",
        ["Val de Bièvre", "Centre-ville", "Reine Blanche", "Le Chaperon Vert", "Bords de Bièvre", "RER B"],
        [["paris-13", "Paris 13e", "limitrophe nord"], ["le-kremlin-bicetre", "Le Kremlin-Bicêtre", "limitrophe est"],
         ["arcueil", "Arcueil", "limitrophe sud"], ["94-val-de-marne", "Val-de-Marne (94)", "le département"]],
    ),
    "le-kremlin-bicetre": _e(
        "Le Kremlin-Bicêtre", "94270",
        "<b>Le Kremlin-Bicêtre</b>, porte d'Italie : pôle hospitalier majeur, PME et cabinets. Nous "
        "entretenons vos bureaux et locaux depuis notre base de Bagneux. Interventions "
        "<span class=\"hl\">soir et matin</span> — <span class=\"hl\">devis sous 24h</span>.",
        "Marquée par l'<b>hôpital Bicêtre</b> (AP-HP) et desservie par la ligne 7 (<b>Le Kremlin-Bicêtre</b>), "
        "la commune concentre professions médicales, cabinets, PME et locaux de services dans un centre "
        "dense aux portes de Paris 13e.",
        "Cabinets, bureaux et locaux professionnels y demandent un entretien rigoureux et régulier. Depuis "
        "<b>Bagneux</b>, nos équipes interviennent en horaires décalés, avec des protocoles adaptés à chaque "
        "type de local.",
        ["Centre-ville", "Hôpital Bicêtre", "Porte d'Italie", "Convention", "Fort de Bicêtre", "M7"],
        [["paris-13", "Paris 13e", "porte d'Italie"], ["gentilly", "Gentilly", "limitrophe ouest"],
         ["arcueil", "Arcueil", "à proximité"], ["94-val-de-marne", "Val-de-Marne (94)", "le département"]],
    ),
}
