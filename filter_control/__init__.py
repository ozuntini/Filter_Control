"""
Filter Controler - Open and Close Gemini Auto Flat Panel
========================================================

Module pour contrôler un GeminiAutoFlatPanel via USB/Serial.
Ce module fournit une classe `GeminiAutoFlatPanel`
avec des méthodes pour ouvrir/fermer le couvercle du panneau,récupérer l'état du périphérique et effectuer des vérifications de santé.
Les commandes et les réponses sont définies dans la classe `Commands`, 
et les états du couvercle sont représentés par l'énumération `CoverState`.
"""

__version__ = "0.1.0"
__author__ = "olivier.zuntini@gmail.com"