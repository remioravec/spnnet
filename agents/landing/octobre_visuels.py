#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les infographies des 2 pages d'octobre — une entre chaque Hn."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import visuels as v

OR, OR2, GR, CR = "#D8431F", "#ED5D37", "#c9bdb2", "#9aa0a6"

# ------------------------------------------------ CONTRAT COPROPRIÉTÉ ------
V_COPRO = {
"QUI": v.duo(
  "Qui décide quoi, et ce qui arrive quand on se trompe",
  "Le syndic, seul", [
    "Signe les actes conservatoires urgents",
    "Exécute ce que l'assemblée a voté",
    "Ne choisit pas le prestataire d'entretien",
    "Un contrat signé sans mandat est contestable"],
  "L'assemblée générale", [
    "Choisit le prestataire et vote le contrat",
    "Vote le budget qui porte la dépense",
    "Décide à la majorité de l'article 24",
    "Peut donner mandat au conseil syndical pour instruire"]),

"CLAUSES": v.cartes(
  "Les quatre chiffres d'un contrat d'entretien",
  [("12 mois", "Durée ferme", "Au-delà, la reconduction tacite prend le relais"),
   ("3 mois", "Préavis courant", "Fixé par le contrat, jamais par la loi"),
   ("Art. 24", "Majorité du vote", "Majorité simple des voix exprimées"),
   ("6 mois", "Attestation URSSAF", "Validité maximale de la pièce à exiger")]),

"DUREE": v.jauge(
  "Les durées de préavis qu'on rencontre, et ce qu'elles impliquent",
  [("1 mois — petits contrats", 17, "sortie souple", OR2),
   ("2 mois", 33, "intermédiaire", OR2),
   ("3 mois — le plus fréquent", 50, "dénoncer en septembre", OR),
   ("6 mois — multi-sites", 100, "dénoncer en juin", GR)],
  "La longueur du préavis n'est pas un détail de forme : à six mois, la décision de changer se prend "
  "un semestre avant la fin du contrat, donc avant même d'avoir le recul d'une année complète."),

"CALENDRIER": v.etapes(
  "Le rétroplanning d'un contrat à échéance au 31 décembre",
  [("1", "Juin", "Bilan de l'année, relevés de contrôle à l'appui"),
   ("2", "Juil. – août", "Cahier des charges, consultation de trois prestataires"),
   ("3", "Sept.", "Question inscrite à l'ordre du jour de l'AG"),
   ("4", "30 sept.", "Envoi du recommandé de dénonciation"),
   ("5", "AG d'automne", "Vote du nouveau contrat, article 24"),
   ("6", "Décembre", "État des lieux, clés, reprise du personnel")]),

"HORS": v.duo(
  "Ce qui est presque toujours hors contrat",
  "Cru hors contrat, mais inclus", [
    "Le réassort des consommables sanitaires",
    "La remise en ordre après une réunion de copropriété",
    "Le signalement des ampoules grillées"],
  "Vraiment hors contrat", [
    "La vitrerie en hauteur et les parties vitrées extérieures",
    "Le décapage et la remise en état des sols",
    "Le nettoyage après sinistre ou après travaux",
    "La désinsectisation et la dératisation"]),

"ERREURS": v.cartes(
  "Les quatre oublis qui coûtent le plus cher",
  [("1", "Périmètre non écrit", "Aucun manquement n'est démontrable faute de référence"),
   ("2", "Bacs oubliés", "Première source de rappel à l'ordre en copropriété"),
   ("3", "Consommables non attribués", "Chacun attend que l'autre fournisse"),
   ("4", "Aucun contrôle", "La dérive s'installe au troisième mois, mécaniquement")]),
}

# ------------------------------------------------- CONTRÔLE QUALITÉ --------
V_CTRL = {
"POURQUOI": v.duo(
  "Deux façons de dire la même chose à son prestataire",
  "L'impression", [
    "« C'est moins bien qu'avant »",
    "Opinion contre opinion, la discussion tourne",
    "Aucune date, aucun poste identifié",
    "Le prestataire conteste, et il a beau jeu"],
  "La mesure", [
    "« Le poste sanitaires est passé de 2 à 1 sur trois relevés »",
    "Une série de faits, datés et transmis",
    "Le poste exact est nommé",
    "Le prestataire corrige, ou n'a plus d'argument"]),

"GRILLE": v.cartes(
  "Les quatre règles qui font tenir un relevé",
  [("1 ×/mois", "Toujours la même date", "Le lendemain d'un passage, jamais la veille"),
   ("1 personne", "Toujours la même", "La rotation des contrôleurs tue la comparabilité"),
   ("10 min", "Pas plus", "Un dispositif lourd est abandonné en six semaines"),
   ("Le jour même", "Transmis", "C'est l'envoi qui donne sa valeur au constat")]),

"SEUIL": v.jauge(
  "Lire le score mensuel sur 24 points",
  [("21 à 24 — conforme", 100, "on classe", "#16a34a"),
   ("17 à 20 — dérive naissante", 83, "on transmet", OR2),
   ("13 à 16 — écart installé", 66, "on recadre", OR),
   ("12 ou moins — manquement", 50, "mise en demeure", "#9a3412")],
  "Le seuil de décision utile n'est pas un chiffre isolé mais deux mois consécutifs sous 17. "
  "Un mauvais mois arrive ; deux de suite après signalement traduisent une organisation qui ne tient pas."),

"FAUX": v.duo(
  "Les indicateurs à ne pas suivre",
  "Ce qui ne mesure rien", [
    "Le nombre d'heures facturées — vous payez un résultat",
    "Les autocontrôles fournis par le prestataire",
    "La satisfaction déclarée en réunion",
    "Le nombre de passages, sans leur contenu"],
  "Ce qui se vérifie", [
    "L'état constaté poste par poste, noté",
    "Le respect du planning, comparé au contrat",
    "La stabilité de l'agent affecté au site",
    "Le délai de remplacement en cas d'absence"]),

"RITUEL": v.etapes(
  "Le cycle mensuel, de bout en bout",
  [("1", "Jour J", "Passage du prestataire"),
   ("2", "J + 1", "Relevé de dix minutes, toujours au même moment"),
   ("3", "J + 1", "Signature du responsable de secteur si présent"),
   ("4", "J + 1", "Envoi par courriel, sans commentaire"),
   ("5", "Mois + 12", "Point annuel sur les douze relevés")]),

"APRES": v.etapes(
  "La gradation des recours, et pourquoi l'ordre compte",
  [("1", "Signalement", "Courriel avec le relevé joint, dès le premier constat"),
   ("2", "Recadrage", "Réunion, compte rendu écrit, plan d'action daté"),
   ("3", "Pénalités", "Celles du contrat, même symboliques"),
   ("4", "Mise en demeure", "Recommandé, délai raisonnable, article 1226"),
   ("5", "Résolution", "Articles 1224 à 1230, si le délai expire sans correction")]),
}

CTA_COPRO = v.cta(
  "Vous préparez le renouvellement de votre contrat d'entretien ?",
  "https://spn-net.fr/contact/", "Demander un devis comparable")
CTA_CTRL = v.cta(
  "Vous voulez un prestataire qui accepte d'être contrôlé&nbsp;?",
  "https://spn-net.fr/contact/", "Demander un devis")
