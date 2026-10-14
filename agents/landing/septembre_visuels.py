#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Infographies des contenus de septembre + /carrieres/.

Un visuel par H2 de fond, construit avec les briques de visuels.py.
Toutes les données proviennent du texte déjà publié sur la page : aucune
offre, aucun tarif, aucune certification ajoutés ici.
"""
import visuels as v

OR, OR2, GR, CR = "#D8431F", "#ED5D37", "#c9bdb2", "#9aa0a6"

HUB = "https://spn-net.fr/choisir-entreprise-nettoyage/"
CDC = "https://spn-net.fr/cahier-des-charges-nettoyage-bureaux/"
CONTACT = "https://spn-net.fr/contact/"
TERT = "https://spn-net.fr/tertiaire/"

# ------------------------------------------------------- A1 : RESILIER -----
V_RESIL = {

"calendrier": v.etapes(
  "Le compte à rebours, de la date anniversaire au courrier",
  [("1", "La date anniversaire", "Celle de la prise d'effet du contrat, pas celle de la signature ni celle de la première facture."),
   ("2", "Le préavis inscrit au contrat", "Trois mois dans la quasi-totalité des contrats de propreté B2B, un ou deux sur les petits contrats, six sur les marchés multi-sites."),
   ("3", "Votre date limite d'envoi", "Date anniversaire moins le préavis. Postez avant, jamais le jour même."),
   ("4", "La première présentation du recommandé", "C'est elle qui fait foi, pas la date de dépôt ni celle de lecture.")]),

"chatel": v.duo(
  "La loi Chatel, et pourquoi elle ne vous couvre pas",
  "Ce que l'article L215-1 protège",
  ["Le consommateur et le non-professionnel",
   "Un rappel écrit du prestataire entre trois et un mois avant la fin du préavis",
   "À défaut de rappel, la résiliation devient possible à tout moment",
   "C'est le régime des contrats d'aide à domicile et de ménage aux particuliers"],
  "Votre contrat de propreté B2B",
  ["Conclu dans le cadre de votre activité professionnelle",
   "Aucun rappel n'est dû par le prestataire",
   "Le préavis du contrat s'applique sans atténuation",
   "La date anniversaire reste la seule porte de sortie de droit commun"]),

"lettre": v.cartes(
  "Les quatre éléments qui rendent le courrier incontestable",
  [("1", "Vos références", "Numéro de contrat et adresse exacte du site concerné"),
   ("2", "Le fondement", "La clause de résiliation et la date anniversaire, rien d'autre"),
   ("3", "La date d'effet", "Le jour où la prestation s'arrête, écrit en toutes lettres"),
   ("4", "L'accusé de réception", "Demandé dans le corps du courrier, en plus du recommandé")]),

"apres": v.etapes(
  "Ce qui se joue pendant le préavis, mois par mois",
  [("1", "Dès l'envoi", "Le sortant reste tenu d'exécuter au même niveau. Ses manquements pendant le préavis sont des manquements comme les autres."),
   ("2", "Dans la foulee", "Réclamez par écrit la liste du personnel affecté au site, avec ancienneté et temps de travail. Elle conditionne la reprise."),
   ("3", "Dès le choix du suivant", "Transmettez-lui les coordonnées du sortant : la passation Annexe 7 se prépare entre eux, pas le dernier jour."),
   ("4", "Jusqu'au terme", "Vous restez tenu de payer. Le contrat court, la facture aussi.")]),

"faute": v.duo(
  "Deux voies de sortie, deux natures de travail",
  "À l'échéance : une affaire de calendrier",
  ["Aucun motif à donner, aucune preuve à produire",
   "Il suffit de respecter le préavis et la forme du courrier",
   "Le risque est la date manquée, pas la contestation",
   "C'est le chemin normal"],
  "Pour manquement : une affaire de preuve",
  ["Des manquements établis, datés et déjà signalés",
   "Une mise en demeure restée sans effet",
   "Une gravité appréciée par le juge si le prestataire conteste",
   "On y va quand la date anniversaire est trop loin"]),
}

CTA_RESIL = v.cta(
  "Votre date limite est passée ou votre préavis court déjà ? La question suivante est celle du remplaçant.",
  HUB, "Le guide pour choisir le suivant")

# ----------------------------------------------- A2 : CAHIER DES CHARGES ---
V_CDC = {

"pourquoi": v.duo(
  "Deux demandes, deux devis qui ne se comparent pas",
  "« 400 m² de bureaux, devis SVP »",
  ["Chaque prestataire pose son hypothèse de temps",
   "Chacun ajoute sa marge de sécurité pour les inconnues",
   "Vous comparez deux prix qui ne couvrent pas le même périmètre",
   "Le moins cher est le moins-disant sur le périmètre, pas sur le prix"],
  "Un périmètre écrit, zone par zone",
  ["Tous chiffrent exactement les mêmes tâches",
   "L'écart de prix devient un écart de productivité, lisible",
   "Ce qui n'est pas dedans est visible avant signature",
   "Les suppléments du troisième mois disparaissent"]),

"besoins": v.cartes(
  "Les quatre relevés à faire avant d'écrire une ligne",
  [("1", "Surfaces et sols", "Surface par zone et nature du revêtement : moquette, parquet, carrelage"),
   ("2", "Usage des locaux", "Disposition des espaces et fonction réelle de chaque local"),
   ("3", "Fréquentation", "Nombre de postes et jours de présence effective, pas l'effectif théorique"),
   ("4", "Accès", "Zones à accès restreint, horaires, badges, alarme, gardien")]),

"frequences": v.jauge(
  "Ce que la fréquence fait au coût, à surface identique",
  [("2 passages / semaine", 50, "base de comparaison", GR),
   ("3 passages / semaine", 75, "environ + 50 %", OR2),
   ("5 passages / semaine", 100, "près du double", OR)],
  "Ordres de grandeur déduits du temps d'intervention, pas des tarifs SPN NET. "
  "La fréquence se cale sur l'occupation réelle, pas sur les mètres carrés."),

"types": v.cartes(
  "Ce qui tient dans le forfait, ce qui se chiffre à part",
  [("Récurrent", "Surfaces et points de contact", "Dépoussiérage, désinfection, traitement des odeurs"),
   ("Récurrent", "Sols et sanitaires", "Aspiration ou lavage selon le revêtement, désinfection et réassort"),
   ("Périodique", "Vitrerie et luminaires", "Cloisons, portes vitrées et fenêtres accessibles, à une hauteur définie"),
   ("Ponctuel", "Remise en état", "Après travaux ou en fin de chantier, devis séparé")]),

"qualite": v.duo(
  "L'adjectif ne se contrôle pas, le critère si",
  "Ce qui ne vaut rien le jour du litige",
  ["« Locaux propres »",
   "« Prestation soignée »",
   "« Qualité irréprochable »",
   "« Entretien des locaux », seul, dans l'objet du contrat"],
  "Ce qui se constate par oui ou par non",
  ["Corbeilles vidées et sacs remplacés à chaque passage",
   "Sols sans salissure visible en lumière rasante",
   "Sanitaires approvisionnés en papier et savon à chaque passage",
   "Surfaces vitrées intérieures sans trace de doigt à hauteur d'homme"]),

"erreurs": v.etapes(
  "Les cinq erreurs, et ce qu'elles coûtent",
  [("1", "Copier un modèle sans l'adapter", "Les cahiers des charges publics décrivent des bâtiments qui ne sont pas les vôtres, et oublient vos locaux."),
   ("2", "Omettre les contraintes d'accès", "Horaires, badges, alarme, gardien, ascenseur réservé : non dits, ils reviennent en avenant."),
   ("3", "Ne rien ecrire sur les consommables", "Papier, savon, sacs : qui fournit, qui stocke, qui réassort. Première source de litige au quotidien."),
   ("4", "Oublier la continuité de service", "Remplacement en cas d'absence : systématique ou non, sous quel délai. Non écrit, il n'existe pas."),
   ("5", "Mélanger récurrent et périodique", "Vitrerie et remise en état des sols chiffrées dans le forfait : le prix mensuel devient incomparable.")]),
}

CTA_CDC = v.cta(
  "Votre périmètre est écrit. Reste à savoir qui peut le tenir, et comment le vérifier avant de signer.",
  HUB, "Les dix points à vérifier avant de signer")

# ------------------------------------------------------- A3 : LITIGE -------
V_LITIGE = {

"constater": v.cartes(
  "Les quatre caractères de ce qui fait preuve",
  [("1", "Comparé", "Le constat se lit face à une prestation écrite au contrat, pas face à une attente"),
   ("2", "Daté", "Jour et heure du passage constaté, relevé au même moment chaque semaine"),
   ("3", "Transmis", "Envoyé au prestataire le jour même : c'est l'envoi qui vaut signalement"),
   ("4", "Répété", "Un constat isolé n'est pas une dérive. La série, elle, s'oppose")]),

"demeure": v.cartes(
  "Les quatre mentions sans lesquelles la mise en demeure ne tient pas",
  [("1", "Les obligations", "Rappel précis des clauses contractuelles qui ne sont pas tenues"),
   ("2", "Les manquements", "Liste datée des constats déjà signalés, relevé par relevé"),
   ("3", "Le délai", "Quinze à trente jours selon la nature du manquement, écrit noir sur blanc"),
   ("4", "La sanction", "Mention expresse de ce qui se passera à défaut d'exécution")]),

"faute": v.duo(
  "Ce qu'un juge regarde quand le prestataire conteste",
  "Ce qui fragilise votre résiliation",
  ["Un manquement isolé, même réel",
   "Des photos et des remarques internes, sans relevé",
   "Aucune mise en demeure préalable, hors urgence",
   "Un contrat qui dit « entretien des locaux » et rien de plus"],
  "Ce qui la tient",
  ["Une dérive répétée, datée et signalée",
   "Des relevés transmis au prestataire à chaque constat",
   "Une mise en demeure avec délai, restée sans effet",
   "Un périmètre écrit auquel comparer le constat"]),

"eviter": v.etapes(
  "Les trois conditions qui évitent le litige, dans l'ordre",
  [("1", "Un périmètre écrit", "Sans cahier des charges, il n'y a pas de manquement possible : il n'y a que des attentes déçues."),
   ("2", "Un rituel de contrôle", "Un point mensuel de quinze minutes, consigné, détecte la dérive au premier mois au lieu du sixième."),
   ("3", "Un prestataire solide", "Un opérateur qui sous-traite en cascade ou dont les équipes tournent tous les deux mois ne tiendra aucun engagement, quel que soit son prix.")]),
}

CTA_LITIGE = v.cta(
  "Le périmètre écrit est ce qui transforme une attente déçue en manquement opposable.",
  CDC, "Remplir votre cahier des charges")

# ------------------------------------------------------- CARRIERES --------
V_CARR = {

"formulaire": v.duo(
  "Le formulaire du site n'est pas fait pour une candidature",
  "Ce que le formulaire demande",
  ["Un nom", "Un e-mail", "Un téléphone", "Et c'est tout"],
  "Ce qu'une candidature suppose",
  ["Un CV ou un parcours",
   "Une disponibilité et un secteur géographique",
   "Un destinataire côté ressources humaines",
   "Une conservation du dossier"]),

"postuler": v.etapes(
  "Où arrive votre message, selon la voie choisie",
  [("1", "Par le formulaire du site", "La demande rejoint la liste des prospects de l'équipe commerciale. Elle n'est ni lue comme une candidature, ni orientée, ni conservée."),
   ("2", "Par les coordonnées des mentions légales", "Le message arrive à l'entreprise. Précisez dès l'objet qu'il s'agit d'une candidature et non d'une demande de devis."),
   ("3", "Dans les deux cas", "Le temps que vous y passez mérite d'arriver au bon endroit. C'est la raison d'être de cette page.")]),

"devis": v.duo(
  "Vous êtes au bon endroit, mais peut-être pas sur la bonne page",
  "Vous cherchez un emploi",
  ["Cette page vous concerne",
   "Les coordonnées utiles sont dans les mentions légales",
   "Le formulaire des autres pages ne vous mène nulle part"],
  "Vous cherchez un prestataire",
  ["Entreprise, syndic ou commerçant : l'offre est détaillée sur les pages secteur",
   "Écrivez d'abord ce que vous attendez, zone par zone",
   "Le guide de choix réunit les dix points à vérifier avant de signer"]),
}

CTA_CARR = v.cta(
  "Vous cherchiez un prestataire de propreté pour vos locaux professionnels ?",
  TERT, "Notre offre pour les bureaux")
