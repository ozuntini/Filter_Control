## Changelog 26/04/2026
- Modification du fichier log
- Adaptation pour un regroupement dans Eclipse Project
- Ajout dans le readme du lien pour télécharger les fichiers d'imprimante 3D.

## Création de la version v1.0.1
- Intégration de la gestion du setting

## Changelog 13/04/2026
- Ajout de la fonction de vérification du setting de position >A#
- Adaptation des programmes et de la documentation

## Création de la version v1.0.0
- Création du fichier VERSION
- Passage en md du changelog
- Mise à jour du README.md
- Création d'un requirements.txt
- Mise à jour du pyproject.toml

## Changelog 12/04/2026
- Modification de l'arborescence pour construire un module Python
- Création du répertoire filter_control
- Création du pyproject.toml
- Vérification du bon fonctionnement

## Changelog 11/04/2026
Modification des entêtes des .py
Correction du filter_controller.py
Tests de fonctionnement

## Changelog 29/03/2026
Amélioration de la gestion du port USB avec des messages d'erreur plus clairs.
Solution de nommage du port USB via udev pour mieux gérer les mutliples périphériques et la configuration.
Informations notées dans le README.md.

## Changelog 28/03/2026
Modifications suite aux conseils de Copilot
Ajouts de documentations
Tests unitaires pour les fonctions de base
Tests avec la présence d'un boitier photo connecté en USB
Ajout de la Class Commands pour centraliser les commandes et réponses du GAFP
Ajout d'un Health Check pour vérifier la connexion et l'état du GAFP
Amélioration du design du retour avec des emojis pour une meilleure lisibilité dans test_filter_controller.py
Création d'une fonction de mapping pour les statuts du moteur, de la lumière et du couvercle avec des labels plus explicites et des emojis pour une meilleure compréhension visuelle.
Création de la fonction get_telemetry pour centraliser la récupération et le mapping des statuts du GAFP.

## Changelog 24/03/2026
Création des programmes avec l'aide de Copilot - Merci à lui 🙏😁
Récupération des commandes basiques pour piloter le Gemini Astro Automatic FlatPanel v2
Adaptation et évolution du code pour piloter correctement le GAFP
Documentation & Tests unitaires