import serial
import time
import logging
import subprocess

class GeminiAutoFlatPanel:
    """
    Classe pour contrôler un GeminiAutoFlatPanel via USB/Serial
    """
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=1):
        """
        Initialise la connexion avec le panneau
        
        Args:
            port: Port USB (ex: /dev/ttyUSB0)
            baudrate: Vitesse de communication (généralement 9600 ou 115200)
            timeout: Délai d'attente en secondes
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.logger = logging.getLogger(__name__)

    def connect(self):
        """Configuration système (équivalent propre de stty)"""
        try:
            subprocess.run(["stty", "-F", self.port, "-hupcl"], check=True)
            self.logger.info(f"Configuration du port {self.port} terminée")
        except subprocess.CalledProcessError as e:
            self.logger.info(f"Erreur lors de la configuration du port : {e}")
            return False
        
        """Établit la connexion avec le panneau"""
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
    
    def disconnect(self):
        """Ferme la connexion"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.logger.info("Déconnecté")
    
    def send_command(self, command):
        """
        Envoie une commande au panneau
        
        Args:
            command: Commande à envoyer (str)
            
        Returns:
            Réponse du panneau (str) ou None en cas d'erreur
        """
        if not self.ser or not self.ser.is_open:
            self.logger.error("Port série non connecté")
            return None
        
        try:
            # Ajoute les caractères de fin de ligne si nécessaire
            if not command.endswith('\r\n'):
                command += '\r\n'
            
            self.ser.write(command.encode('utf-8'))
            time.sleep(0.1)  # Petit délai pour que le panneau réponde
            
            # Lit la réponse
            response = self.ser.read_until(b'#').decode('utf-8').strip()
            self.logger.info(f"Commande: {command.strip()} -> Réponse: {response}")
            return response
        
        except Exception as e:
            self.logger.error(f"Erreur d'envoi: {e}")
            return None

    def receive_response(self, timeout=1.0):
        """Lit une réponse du panneau avec un timeout configurable
        
        Args:
            timeout (float): Délai d'attente en secondes avant abandon (par défaut: 1.0s)
        
        Returns:
            str: La réponse reçue ou None en cas d'erreur/timeout
        """
        if not self.ser or not self.ser.is_open:
            self.logger.error("Port série non connecté")
            return None
        
        try:
            # Définir le timeout sur le port série
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

    def open_cover(self):
        """
        Ouvre le couvercle
        Returns:
            str: "Opened" si le panneau est ouvert, "Unknown" si aucune confirmation n'est reçue
        """
        cover = self.send_command(">O#")
        if cover and cover == "*OOpened#":
            self.logger.info("Panneau déjà ouvert")
            return "Opened"
        else:
            cover = self.receive_response(15)  # Attendre jusqu'à 15 secondes pour la confirmation d'ouverture
            if cover and cover == "*OOpened#":
                self.logger.info("Panneau ouvert avec succès")
                return "Opened"
            else:
                self.logger.error("Pas de confirmation d'ouverture du panneau")
                return "Unknown"
    
    def close_cover(self):
        """
        Ferme le couvercle
        Returns:
            str: "Closed" si le panneau est fermé, "Unknown" si aucune confirmation n'est reçue
        """
        cover = self.send_command(">C#")
        if cover and cover == "*CClosed#":
            self.logger.info("Panneau déjà fermé")
            return "Closed"
        else:
            cover = self.receive_response(15)  # Attendre jusqu'à 15 secondes pour la confirmation de fermeture
            if cover and cover == "*CClosed#":
                self.logger.info("Panneau fermé avec succès")
                return "Closed"
            else:
                self.logger.error("Pas de confirmation de fermeture du panneau")
                return "Unknown"
    
    def get_device_status(self):
        """
        Récupère l'état du device sous la forme : *SidMLC#
        M = motor status (0=stopped, 1=moving)
        L = light status (0=off, 1=on)
        C = Cover status (0=moving, 1=closed, 2=open, 3=timed out)
        """
        device = self.send_command(">S#")
        if device and device.startswith("*S") and device.endswith("#"):
            status = device[2:-1]  # Extrait le statut entre *S et #
            deviceId = status[:-3]  # Les 2 premiers caractères sont l'ID du device
            motorStatus = status[2]  # M
            lightStatus = status[3]  # L
            coverStatus = status[4]  # C
            self.logger.info(f"Device id: {deviceId}, Motor: {motorStatus}, Light: {lightStatus}, Cover: {coverStatus}")
            return {
                "device_id": deviceId,
                "motor_status": motorStatus,
                "light_status": lightStatus,
                "cover_status": coverStatus
            }
        else:
            self.logger.error(f"Réponse de statut incorrecte: {device}")
            return None