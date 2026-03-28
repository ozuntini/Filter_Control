# 📖 API Reference - Filter Control v2.0
## 📚 Documentation du code Python - Filter Control

### Vue d'ensemble du projet

Le projet **Filter Control** automatise le contrôle d'un panneau plat automatique Gemini (GeminiAutoFlatPanel) via une connexion USB/Serial. Il a été conçu pour gérer automatiquement un filtre solaire lors de la photographie d'éclipses solaires, notamment pour retirer le filtre pendant la phase totale.

---

## 📋 Structure du projet

Le projet est composé de 2 fichiers Python :

```
Filter_Control/
├── filter_controller.py        # Classe principale de contrôle
├── test_filter_controller.py   # Script de test CLI
├── README.md                   # Documentation utilisateur
└── GAFP_basic_commands.md      # Documentation des commandes
```

---

## 🔧 Module Principal : `filter_controller.py`

### Classe : `GeminiAutoFlatPanel`

Gère la communication avec le panneau plat automatique Gemini via USB/Serial.

```python
class GeminiAutoFlatPanel:
    """Classe pour contrôler un GeminiAutoFlatPanel via USB/Serial"""
```

#### **Attributs d'instance**
| Attribut | Type | Description |
|----------|------|-------------|
| `port` | str | Port USB (ex: `/dev/ttyUSB0`) |
| `baudrate` | int | Vitesse de communication en bauds (défaut: 9600) |
| `timeout` | float | Délai d'attente en secondes |
| `ser` | serial.Serial | Objet de connexion série |
| `logger` | logging.Logger | Logger pour les messages de débogage |

---

### Méthodes

#### **`__init__(port, baudrate, timeout)`**
Initialise la connexion avec le panneau.

**Paramètres :**
- `port` (str, défaut: `/dev/ttyUSB0`) : Port USB
- `baudrate` (int, défaut: 9600) : Vitesse de communication
- `timeout` (float, défaut: 1) : Délai d'attente en secondes

**Exemple :**
```python
panel = GeminiAutoFlatPanel(port='/dev/ttyUSB0', baudrate=9600, timeout=1)
```

---

#### **`connect() → bool`**
Établit la connexion avec le panneau après configuration du port.

**Étapes :**
1. Configure le port avec la commande `stty` (désactive le contrôle de débit matériel)
2. Crée une connexion série avec les paramètres spécifiés
3. Paramètres fixes : 8 bits de données, pas de parité, 1 bit d'arrêt

**Retour :** `True` si succès, `False` sinon

**Exemple :**
```python
if panel.connect():
    print("Connecté au panneau")
else:
    print("Erreur de connexion")
```

---

#### **`disconnect()`**
Ferme la connexion série.

**Exemple :**
```python
panel.disconnect()
```

---

#### **`send_command(command) → str | None`**
Envoie une commande au panneau et récupère la réponse.

**Paramètres :**
- `command` (str) : Commande à envoyer (ex: `">O#"` pour ouvrir)

**Comportement :**
- Ajoute automatiquement `\r\n` si absent
- Attend 0.1 secondes que le panneau réponde
- Lit la réponse jusqu'au caractère `#`

**Retour :** Réponse du panneau (str) ou `None` en cas d'erreur

**Exemple :**
```python
response = panel.send_command(">S#")  # Demande le statut
print(response)  # Ex: *S01011#
```

---

#### **`receive_response(timeout=1.0) → str | None`**
Lit une réponse du panneau avec un timeout configurable.

**Paramètres :**
- `timeout` (float, défaut: 1.0) : Délai d'attente en secondes

**Retour :** Réponse reçue (str) ou `None` en cas d'erreur/timeout

**Cas d'usage :** Attendre les confirmations longues (jusqu'à 15 secondes pour les mouvements physiques)

**Exemple :**
```python
response = panel.receive_response(timeout=15)  # Attendre 15 secondes
```

---

#### **`open_cover() → str`**
Ouvre le couvercle (retire le filtre).

**Comportement :**
1. Envoie la commande `">O#"`
2. Si `"*OOpened#"` est reçu immédiatement, le panneau était déjà ouvert
3. Sinon, attend jusqu'à 15 secondes la confirmation `"*OOpened#"`

**Retour :** 
- `"Opened"` si succès
- `"Unknown"` si pas de confirmation

**Exemple :**
```python
result = panel.open_cover()
if result == "Opened":
    print("Filtre retiré avec succès")
```

---

#### **`close_cover() → str`**
Ferme le couvercle (met en place le filtre).

**Comportement :** Identique à `open_cover()` avec la commande `">C#"`

**Retour :**
- `"Closed"` si succès
- `"Unknown"` si pas de confirmation

**Exemple :**
```python
result = panel.close_cover()
if result == "Closed":
    print("Filtre mise en place avec succès")
```

---

#### **`get_device_status() → dict | None`**
Récupère l'état actuel du périphérique.

**Format de réponse :** `*SidMLC#`

| Position | Clé | Valeurs |
|----------|-----|---------|
| id (2 car.) | `device_id` | Identifiant du device |
| M | `motor_status` | 0=arrêté, 1=en mouvement |
| L | `light_status` | 0=éteinte, 1=allumée |
| C | `cover_status` | 0=mouvement, 1=fermé, 2=ouvert, 3=timeout |

**Retour :** 
```python
{
    "device_id": "01",
    "motor_status": "0",
    "light_status": "1",
    "cover_status": "2"
}
```
Ou `None` en cas d'erreur

**Exemple :**
```python
status = panel.get_device_status()
if status:
    print(f"Couverture: {status['cover_status']} (2=ouvert)")
```

---

## 🧪 Script de Test : `test_filter_controller.py`

Interface en ligne de commande (CLI) pour tester les fonctionnalités.

### Usage

```bash
# Ouvrir le panneau
python test_filter_controller.py --port /dev/ttyUSB0 --baudrate 9600 Open

# Fermer le panneau
python test_filter_controller.py --port /dev/ttyUSB0 --baudrate 9600 Close

# Vérifier l'état
python test_filter_controller.py Status

# Avec paramètres personnalisés
python test_filter_controller.py --port /dev/ttyUSB1 --baudrate 115200 --timeout 2 Status
```

### Arguments
| Argument | Type | Défaut | Description |
|----------|------|--------|-------------|
| `--port` | str | `/dev/ttyUSB0` | Port USB du panneau |
| `--baudrate` | int | 9600 | Vitesse en bauds |
| `--timeout` | float | 1 | Timeout en secondes |
| `action` | choice | - | Action : `Open`, `Close`, `Status` |

---

## 🚀 Exemple d'utilisation complet

```python
from filter_controller import GeminiAutoFlatPanel
import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO)

# Créer une instance
panel = GeminiAutoFlatPanel(port='/dev/ttyUSB0', baudrate=9600, timeout=1)

try:
    # Se connecter
    if panel.connect():
        # Vérifier l'état
        status = panel.get_device_status()
        print(f"État: {status}")
        
        # Ouvrir le filtre
        result = panel.open_cover()
        print(f"Ouverture: {result}")
        
        # Fermer le filtre
        result = panel.close_cover()
        print(f"Fermeture: {result}")
    else:
        print("Connexion échouée")
finally:
    # Toujours fermer
    panel.disconnect()
```

---
