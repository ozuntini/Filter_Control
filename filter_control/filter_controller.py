#!/usr/bin/env python3
"""
Module pour contrôler un GeminiAutoFlatPanel via USB/Serial.
Ce module fournit une classe `GeminiAutoFlatPanel`
avec des méthodes pour ouvrir/fermer le couvercle du panneau,récupérer l'état du périphérique et effectuer des vérifications de santé.
Les commandes et les réponses sont définies dans la classe `Commands`, 
et les états du couvercle sont représentés par l'énumération `CoverState`.

Usage:
    panel = GeminiAutoFlatPanel(port='/dev/ttyUSB0', baudrate=9600, timeout=1)
    if panel.connect():
        panel.open_cover()
        status = panel.get_device_status()
        panel.close_cover()
        panel.disconnect()
"""

from enum import Enum
import serial
import time
import logging
import subprocess

class CoverState(Enum):
    """Énumération pour l'état du couvercle."""
    OPENED = "opened"
    CLOSED = "closed"
    MOVING = "moving"
    UNKNOWN = "unknown"

class Commands:
    """Constantes pour les commandes et réponses du panneau."""
    OPEN = ">O#"
    CLOSE = ">C#"
    STATUS = ">S#"
    SETANGLE = ">M{}#"      # Commande pour régler l'angle du panneau (ex: >M45# pour 45 degrés)
    SETCLOSE = ">F#"        # Commande pour valider l'angle dea position fermée
    SETOPEN = ">E#"         # Commande pour valider l'angle de la position ouverte
    STATUS_ANGLE = ">A#"    # Commande pour récupérer l'angle actuel du panneau (réponse: *A{}Ready# 0=No 1=Ready)

    RESPONSES = {
        "OPENED": "*OOpened#",
        "CLOSED": "*CClosed#",
        "ANGLE": "*A{}Ready#"   # Réponse pour savoir si les position sont set ou pas (ex: *A1Ready# pour position ouverte validée, *A0Ready# pour non validée)
    }


class GeminiAutoFlatPanel:
    """Classe pour contrôler un GeminiAutoFlatPanel via USB/Serial.

    Parameters
    ----------
    port : str, optional
        Port USB (default '/dev/ttyUSB0').
    baudrate : int, optional
        Vitesse de communication en bauds (default 9600).
    timeout : float, optional
        Délai d'attente en secondes (default 1.0).
    """
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.logger = logging.getLogger(__name__)

    def connect(self) -> bool:
        """Établit la connexion avec le panneau.

        Returns
        -------
        bool
            True si la connexion a réussi, False sinon.
        """
        try:
            subprocess.run(["stty", "-F", self.port, "-hupcl"], check=True)
            self.logger.info(f"Configuration du port {self.port} terminée")
        except subprocess.CalledProcessError as e:
            self.logger.info(f"Erreur lors de la configuration du port : {e}")
            return False
        
        try:
            self.ser = serial.Serial(
                self.port,
                self.baudrate,
                timeout=self.timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
    
            self.logger.info(f"Connecté au port {self.port}")
            return True
        except serial.SerialException as e:
            self.logger.error(f"Erreur de connexion: {e}")
            return False
    
    def disconnect(self) -> None:
        """Ferme la connexion série avec le panneau."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.logger.info("Déconnecté")
    
    def send_command(self, command: str) -> str | None:
        """Envoie une commande texte au panneau.

        Parameters
        ----------
        command : str
            Commande à envoyer (ex: '>O#').

        Returns
        -------
        str or None
            Réponse brute du panneau, ou None en cas d'erreur.
        """
        if not self.ser or not self.ser.is_open:
            self.logger.error("Port série non connecté")
            return None
        
        try:
            if not command.endswith('\r\n'):
                command += '\r\n'
            
            self.ser.write(command.encode('utf-8'))
            time.sleep(0.1)
            
            response = self.ser.read_until(b'#').decode('utf-8').strip()
            self.logger.info(f"Commande: {command.strip()} -> Réponse: {response}")
            return response
        
        except Exception as e:
            self.logger.error(f"Erreur d'envoi: {e}")
            return None

    def receive_response(self, timeout: float = 1.0) -> str | None:
        """Lit une réponse du panneau avec un timeout configurable.

        Parameters
        ----------
        timeout : float, optional
            Délai d'attente en secondes (default 1.0).

        Returns
        -------
        str or None
            La réponse reçue ou None en cas d'erreur/timeout.
        """
        if not self.ser or not self.ser.is_open:
            self.logger.error("Port série non connecté")
            return None
        
        try:
            self.ser.timeout = timeout
            response = self.ser.read_until(b'#').decode('utf-8').strip()
            self.logger.info(f"Réponse reçue: {response}")
            return response
        except serial.SerialTimeoutException:
            self.logger.warning(f"Timeout lors de la lecture (après {timeout}s)")
            return None
        except Exception as e:
            self.logger.error(f"Erreur de lecture: {e}")
            return None

    def open_cover(self) -> CoverState:
        """Ouvre le couvercle (retire le filtre solaire).

        Returns
        -------
        CoverState
            Etat du couvercle après commande (OPEN ou UNKNOWN).
        """
        cover = self.send_command(Commands.OPEN)
        if cover and cover == Commands.RESPONSES["OPENED"]:
            self.logger.info("Panneau déjà ouvert")
            return CoverState.OPENED
        else:
            cover = self.receive_response(15)
            if cover and cover == Commands.RESPONSES["OPENED"]:
                self.logger.info("Panneau ouvert avec succès")
                return CoverState.OPENED
            else:
                self.logger.error("Pas de confirmation d'ouverture du panneau")
                return CoverState.UNKNOWN
    
    def close_cover(self) -> CoverState:
        """Ferme le couvercle (remet le filtre solaire).

        Returns
        -------
        CoverState
            Etat du couvercle après commande (CLOSED ou UNKNOWN).
        """
        cover = self.send_command(Commands.CLOSE)
        if cover and cover == Commands.RESPONSES["CLOSED"]:
            self.logger.info("Panneau déjà fermé")
            return CoverState.CLOSED
        else:
            cover = self.receive_response(15)
            if cover and cover == Commands.RESPONSES["CLOSED"]:
                self.logger.info("Panneau fermé avec succès")
                return CoverState.CLOSED
            else:
                self.logger.error("Pas de confirmation de fermeture du panneau")
                return CoverState.UNKNOWN
    
    def get_device_status(self) -> dict | None:
        """Récupère l'état actuel du périphérique.
    
        Returns:
            dict: Dictionnaire contenant :
                - device_id (str): device ID (ex: "99")
                - motor_status (str): Motor status (0 stopped, 1 running)
                - light_status (str): Light status (0 off, 1 on)
                - cover_status (str): Cover status (0 moving, 1 closed, 2 open, 3 timed out)
        
            None: En cas d'erreur
        """
        device = self.send_command(Commands.STATUS)
        if device and device.startswith("*S") and device.endswith("#"):
            status = device[2:-1]
            deviceId = status[:-3]
            motorStatus = status[2]
            lightStatus = status[3]
            coverStatus = status[4]
            self.logger.info(f"Device id: {deviceId}, Motor: {motorStatus}, Light: {lightStatus}, Cover: {coverStatus}")
            return {
                "device_id": deviceId,          # ID du device (ex: "12345")
                "motor_status": motorStatus,    # État du moteur (ex: "0" pour arrêté, "1" pour en mouvement)
                "light_status": lightStatus,    # État de la lumière (ex: "0" pour éteinte, "1" pour allumée)
                "cover_status": coverStatus     # État du couvercle (ex: "0" pour fermé, "1" pour ouvert)
            }
        else:
            self.logger.error(f"Réponse de statut incorrecte: {device}")
            return None
    
    def health_check(self):
        """Vérifie si le panneau répond 
    
        Returns:
            None: En cas d'erreur
        """
        status = self.send_command(Commands.STATUS)
        return status is not None
    
    def move_to_position(self, position: int) -> str | bool:
        """Déplace le panneau d'un angle spécifique.

        Parameters
        ----------
        position : int
            Position cible en ° de -45 (closing) à 45 (opening).

        Returns
        -------
        bool
            True si la commande a été envoyée avec succès, False sinon.
        """
        if -45 <= position <= 45:
            command = Commands.SETANGLE.format(position)
            response = self.send_command(command)
            if response and response.startswith("*M") and response.endswith("#"):
                self.logger.info(f"Déplacement vers {position}° confirmé -> Commande: {command}, Réponse: {response}")
                return response is not None
            else:
                response = self.receive_response(30)
                if response and response.startswith("*M") and response.endswith("#"):
                    self.logger.info(f"Déplacement vers {position}° confirmé -> Commande: {command}, Réponse: {response}")
                    return response is not None
                else:
                    self.logger.info(f"Pas de confirmation de déplacement vers {position}° -> Commande: {command}, Réponse: {response}")
                    return False
        else:
            self.logger.error("Position doit être entre -45 et 45 degrés")
            return False
    
    def set_closed_position(self) -> str | bool:
        """Valide l'angle de la position fermée.

        Returns
        -------
        bool
            True si la commande a été envoyée avec succès, False sinon.
        """
        response = self.send_command(Commands.SETCLOSE)
        return response is not None
    
    def set_open_position(self) -> str | bool:
        """Valide l'angle de la position ouverte.

        Returns
        -------
        bool
            True si la commande a été envoyée avec succès, False sinon.
        """
        response = self.send_command(Commands.SETOPEN)
        return response is not None
    
    def get_angle_set(self) -> dict | None:
        """Vérifie le setting de l'angle.
        *A0Ready#
        Returns
        -------
            dict: Dictionnaire contenant :
                - position_setting (str) : Setting 0 ou 1
                - position_status" (str) : Ready
        
            None: En cas d'erreur  
        """
        device = self.send_command(Commands.STATUS_ANGLE)
        if device and device.startswith("*A") and device.endswith("#"):
            position_setting = device[2]
            position_status = device[3:-1]
            self.logger.info(f"Position Setting: {position_setting}, Position Status: {position_status}")
            return {
                "position_setting": position_setting,          # 0 = No et 1 = Ready
                "position_status": position_status             # Toujours Ready
            }
        else:
            self.logger.error(f"Réponse de setting angle incorrecte: {device}")
            return None
