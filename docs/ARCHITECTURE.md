
# 📖 Architecture
## 💡 Propositions d'améliorations

### 1. **Améliorer la gestion d'erreurs**
- Créer des exceptions personnalisées (`ConnectionError`, `CommandError`, etc.)
- Implémenter des retry automatiques

```python
class GeminiError(Exception):
    """Exception de base pour Gemini"""
    pass

class ConnectionError(GeminiError):
    """Erreur de connexion"""
    pass
```

### 2. **Ajouter un context manager**
```python
class GeminiAutoFlatPanel:
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

# Utilisation
with GeminiAutoFlatPanel() as panel:
    panel.open_cover()
```

### 3. **Ajouter des tests unitaires**
```python
# tests/test_filter_controller.py
import unittest
from unittest.mock import Mock, patch

class TestGeminiAutoFlatPanel(unittest.TestCase):
    def setUp(self):
        self.panel = GeminiAutoFlatPanel()
    
    def test_connect_success(self):
        with patch('serial.Serial') as mock_serial:
            assert self.panel.connect() == True
```

### 4. **Créer une classe de configuration**
```python
from dataclasses import dataclass

@dataclass
class GeminiConfig:
    port: str = '/dev/ttyUSB0'
    baudrate: int = 9600
    timeout: float = 1.0
    
    # Paramètres temporels
    open_timeout: float = 15.0
    close_timeout: float = 15.0
```

### 5. **Enrichir le README avec des diagrammes**
- Diagramme de flux d'état du couvercle
- Architecture de communication série
- Exemple d'intégration dans une pipeline d'astrophotographie

### 6. **Ajouter du logging structuré**
```python
import json

def log_command(self, command, response, duration):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "response": response,
        "duration_ms": duration * 1000
    }
    self.logger.info(json.dumps(log_entry))
```

---

## 📊 Diagramme de flux proposé

```
┌─────────────────────────────────────┐
│   GeminiAutoFlatPanel.__init__()    │
│   (Initialiser les paramètres)      │
└────────────────┬────────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │   connect()     │  (Établir connexion)
        │   (+ stty conf) │
        └────────┬────────┘
                 │
        ┌────────▼─────────┐
        │  get_device_     │  (Vérifier l'état)
        │  status()        │
        └────────┬─────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
 open_cover() close_cover() other_commands()
    │            │            │
    └────────────┼────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │   disconnect()  │   (Fermer)
        └─────────────────┘
```
