<hr style="height:8px; border:none; background-color:red;">

> [!CAUTION]
> ## ⚠️ DANGER CRITIQUE : RISQUE DE CÉCITÉ ⚠️
> **CE SYSTÈME EST EXCLUSIVEMENT RÉSERVÉ À L'ASTROPHOTOGRAPHIE.**
> 
> * **INTERDICTION FORMELLE** d'utiliser ce dispositif pour l'observation visuelle (œil à l'oculaire).
> * Une défaillance logicielle, un bug du script ou une coupure de courant peut entraîner le retrait imprévu du filtre.
> * L'observation directe du soleil sans filtre à travers un instrument optique provoque une **perte de vue immédiate et définitive**.
> 
> **L'utilisateur assume l'entière responsabilité de l'utilisation de ce code.**

![Danger](https://img.shields.io/badge/DANGER-EYE_SAFETY-red?style=for-the-badge)
![Photo Only](https://img.shields.io/badge/Usage-Astrophotography_Only-blue?style=for-the-badge)

<hr style="height:8px; border:none; background-color:red;">

<div style="background-color: black; height: 20px;"></div>

# 📟 Filter Control for Solar Eclipse 🌞
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-C51A4A?style=for-the-badge&logo=Raspberry-Pi&logoColor=white)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen?style=for-the-badge)

## 🔭 Projet
Mon objectif est d'automatiser complètement une séquence de photographie d'éclipse Solaire.  
La différence de luminosité entre la phase partielle C1 à C2 et C3 à C4 et la phase totale est énorme.  
Pendant la phase totale il est nécessaire de retirer le filtre solaire obligatoire pendant la phase partielle.  
Pour automatiser ça je m'appuie sur un Automatic FlatPanel de la marque
[Gemini Astro](https://gemini-astro.com). Dont j'ai remplacé l'écran de flat par un filtre solaire.  
Le code de ce dépôt vous permettra de piloter ce système branché en USB sur une Raspberry.

## 📋 Prérequis
### Installation des dépendances
```bash
sudo apt-get update
sudo apt-get install python3-pip
pip install pyserial  # A faire dans l'environnement virtuel
```
ou
```bash
# Installer les dépendances Python
pip install -r requirements.txt
````

### Virtual environment
```bash
python3 -m venv ~/filter_ctrl_env
source ~/filter_ctrl_env/bin/activate
```

## 🛠️ Dépannage
### Vérifier le port USB
```bash
ls /dev/ttyUSB*
dmesg | grep usb  # Voir les événements USB`
```
### Permissions
```bash
sudo usermod -a -G dialout $USER  # Ajouter l'utilisateur au groupe dialout
```
Puis se reconnecter 🔌

Si vous rencontrez quand même des problèmes de droits
1. Dans /etc/udev/rules.d
2. Créer un fichier 10-serial-usb.rules
3. Ajouter la ligne KERNEL=="ttyUSB0",SUBSYSTEM=="tty",MODE="0666"

### Modemanager
Il est possible que ModemManager interfère avec votre périphérique USB.  
Vous pouvez le désactiver ou le désinstaller si vous n'en avez pas besoin pour d'autres fonctions de votre système.
```bash
sudo systemctl stop ModemManager.service
sudo systemctl disable ModemManager.service

sudo apt-get remove modemmanager # Désinstaller complètement ModemManager si vous n'en avez pas besoin
```

### Tester la connexion
```bash
python3 -c "import serial; s = serial.Serial('/dev/ttyUSB0', 9600); print('OK')"
```

## ‼️ Points importants
1. **Consultez la documentation** de votre GeminiAutoFlatPanel GAFP_basic_commands.md.
2. Adaptez les commandes selon votre modèle spécifique si besoin.
3. Vous avez la possibilité de définir la position Open et Close pour l'adapter à votre besoin.  
Attention à bien gérer le timeout dans la fonction **def receive_response(self, timeout=1.0):** pour attendre la fin du mouvement.
4. Ajouter des logs facilite le débogage

Vous pouvez maintenant intégrer facilement cette classe dans votre programme plus général ! 🚀

## ⚠️ Rappel de sécurité
Il faut être extrêmement prudent avec ce type de système, surtout lorsqu'il s'agit de manipuler des filtres solaires.  
Tenez bien compte du retour d'état du couvercle (coverStatus) pour éviter toute situation dangereuse.  
c.f. tableau de correspondance des états du couvercle ci-dessous retourné par la fonction get_device_status().:
| Code | Signification | État de sécurité |
|------|--------------|------------------|
| 0    | SAFE - FILTER ENGAGED | ✅ Sécurisé pour l'instrument |
| 1    | TRANSITION | ⚠️ Ne pas regarder |
| 2    | DANGER - RETRACTED | 🔥 PHOTO UNIQUEMENT |
| 3    | ERROR | ❌ Position inconnue |

<hr style="height:8px; border:none; background-color:red;">

## 💡 Gestion plus spécifique du device
Il est possible de nommer le device dans les règles udev pour lui donner un nom plus explicite et éviter les problèmes de droits.  
Voici un exemple de règle udev à ajouter dans /etc/udev/rules.d/99-gflatpanel.rules :
### 1. Identification du device
Pour être certain que la règle ne s'applique qu'à votre adaptateur spécifique, récupérez ses identifiants (ID Vendor et ID Product) :
```bash
lsusb
```
Vous devriez voir une ligne similaire à celle-ci :
Bus 001 Device 020: ID 1a86:7523 QinHeng Electronics CH340 serial converter
>ID=1a86 (vendor) : 7523 (product)
### 2. Règle udev
Créez un fichier de règles udev par exemple : /etc/udev/rules.d/99-gflatpanel.rules  
Et ajoutez la ligne suivante en adaptant les ID Vendor et Product à votre cas :
>ACTION=="add", SUBSYSTEM=="tty", SUBSYSTEMS=="usb", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="gflatpanel", MODE="0666", RUN+="/usr/bin/stty -F /dev/%k -hupcl"
### 3. Recharger les règles udev
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```
### 4. Vérification
Brancher votre adaptateur et vérifiez que le lien symbolique /dev/gflatpanel est créé et accessible en écriture :
```bash
ls -l /dev/gflatpanel
```
Vous devriez voir quelque chose comme :
```bash
lrwxrwxrwx 1 root root 7 Mar 29 17:29 /dev/gflatpanel -> ttyUSB0
```
Vérifier le paramètre de stty :
```bash
stty -F /dev/ttyUSB0 -a | grep hupcl
```
Vous devriez voir que le hang-up on close est désactivé (hupcl = -hupcl).  
>-parenb -parodd -cmspar cs8 **-hupcl** -cstopb cread clocal -crtscts  

Maintenant vous pouvez utiliser /dev/gflatpanel dans votre code sans vous soucier des permissions ou du numéro de port qui peut changer.

