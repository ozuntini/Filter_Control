# 🤝 Contributing Guidelines

Merci d'intéresser à contribuer au projet **Filter Control**! 

---

## 🎯 Comment contribuer

### 1. Signaler un bug 🐛

Si vous trouvez un bug, créez une issue avec:

- **Description claire** : Qu'est-ce qui ne fonctionne pas?
- **Étapes de reproduction** : Comment reproduire le problème?
- **Comportement attendu** : Que devrait-il se passer?
- **Logs** : Sortie avec `logging.basicConfig(level=logging.DEBUG)`
- **Environnement** : OS, version Python, port USB utilisé

**Exemple :**
```
**Titre:** Timeout lors de open_cover() sur Raspberry Pi 4

**Description:**
La méthode open_cover() expire systématiquement après 15 secondes.

**Étapes de reproduction:**
1. Connecter GeminiAutoFlatPanel sur /dev/ttyUSB0
2. Appeler panel.open_cover()
3. Attendre → Timeout

**Comportement attendu:**
Le couvercle devrait s'ouvrir

**Logs:**
[DEBUG] Command: >O# -> Response: *OOpened#
[WARNING] Timeout lors de la lecture (après 15s)

**Environnement:**
- OS: Raspberry Pi OS (32-bit)
- Python: 3.9
- pyserial: 3.5
```

### 2. Proposer une amélioration ✨

Pour proposer une nouvelle fonctionnalité:

1. Créez une issue avec le label `enhancement`
2. Décrivez le cas d'usage et les bénéfices
3. Proposez une API si possible
4. Discutez avant de coder!

**Exemple :**
```
**Titre:** Ajouter support du context manager

**Description:**
Permettre d'utiliser GeminiAutoFlatPanel avec `with` pour 
une meilleure gestion des ressources.

**Cas d'usage:**
```python
with GeminiAutoFlatPanel() as panel:
    panel.open_cover()
    # disconnect() automatiquement appelé
```

**Bénéfices:**
- Plus Pythonic
- Gestion automatique des erreurs
- Moins de boilerplate
```

### 3. Soumettre une Pull Request 🔄

**Workflow :**

1. **Fork** le repository
2. **Clone** votre fork
```bash
git clone https://github.com/YOUR_USERNAME/Filter_Control.git
cd Filter_Control
```

3. **Créer une branche** descriptive
```bash
git checkout -b fix/timeout-issue
# ou
git checkout -b feat/context-manager
```

4. **Commits** clairs et atomiques
```bash
git commit -m "🐛 fix: increase timeout for slow devices"
git commit -m "📚 docs: add example for context manager"
```

5. **Push** vers votre fork
```bash
git push origin fix/timeout-issue
```

6. **Créer une PR** vers `main` avec :
   - Description claire du changement
   - Référence à l'issue si applicable
   - Checklist complétée

---

## 📝 Standards de code

### Style

Suivez [PEP 8](https://www.python.org/dev/peps/pep-0008/) :

```python
# ✓ Bon
def open_cover(self) -> CoverState:
    """Ouvre le couvercle."""
    result = self.send_command(">O#")
    if result and result == "*OOpened#":
        return CoverState.OPEN
    return CoverState.UNKNOWN

# ✗ Mauvais
def open_cover(self):
    result=self.send_command(">O#")
    if result and result=="*OOpened#":return "Opened"
    return "Unknown"
```

### Type hints

Toutes les méthodes doivent avoir des type hints:

```python
# ✓ Bon
def send_command(self, command: str) -> str | None:
    """..."""

def get_device_status(self) -> dict | None:
    """..."""

# ✗ Mauvais
def send_command(self, command):
    """..."""

def get_device_status(self):
    """..."""
```

### Docstrings (NumPy style)

```python
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
```

### Noms de variables

```python
# ✓ Bon
device_id = "01"
motor_status = "0"
timeout_seconds = 15

# ✗ Mauvais
id = "01"           # Trop court
m_st = "0"          # Cryptique
to = 15             # Ambigü
```

---

## ✅ Checklist PR

Avant de soumettre:

- [ ] Code suit PEP 8
- [ ] Type hints sur toutes les méthodes
- [ ] Docstrings en format NumPy
- [ ] Tests écrits/mis à jour
- [ ] Tous les tests passent `pytest`
- [ ] Documentation mise à jour
- [ ] Messages de commit clairs
- [ ] Pas de code commenté ou de debug prints
- [ ] Pas de dépendances inutiles

```bash
# Tester avant de commit
python -m pytest
python -m pylint filter_controller.py
```

---

## 🧪 Tests

### Exécuter les tests

```bash
# Installer les dépendances de test
pip install pytest pytest-cov

# Exécuter tous les tests
pytest

# Avec coverage
pytest --cov=filter_controller tests/
```

### Écrire des tests

```python
# tests/test_filter_controller.py
import unittest
from unittest.mock import Mock, patch, MagicMock
from filter_controller import GeminiAutoFlatPanel, CoverState

class TestGeminiAutoFlatPanel(unittest.TestCase):
    def setUp(self):
        """Préparation avant chaque test."""
        self.panel = GeminiAutoFlatPanel()
    
def test_connect_success(self):
        """Test connexion réussie."""
        with patch('serial.Serial') as mock_serial:
            mock_instance = MagicMock()
            mock_serial.return_value = mock_instance
            
            result = self.panel.connect()
            
            self.assertTrue(result)
            mock_serial.assert_called_once()
    
def test_open_cover_success(self):
        """Test ouverture réussie du couvercle."""
        with patch.object(self.panel, 'send_command', return_value="*OOpened#"):
            result = self.panel.open_cover()
            self.assertEqual(result, CoverState.OPEN)
    
def test_open_cover_failure(self):
        """Test échec de l'ouverture."""
        with patch.object(self.panel, 'send_command', return_value=None):
            with patch.object(self.panel, 'receive_response', return_value=None):
                result = self.panel.open_cover()
                self.assertEqual(result, CoverState.UNKNOWN)
```

---

## 📋 Commits

Utilisez [Conventional Commits](https://www.conventionalcommits.org/) :

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types :**
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage (PEP 8, etc.)
- `refactor:` Refactorisation sans changement de comportement
- `perf:` Amélioration de performance
- `test:` Ajout/modification de tests
- `ci:` Configuration CI/CD

**Exemples :**
```bash
git commit -m "feat: add context manager support"
git commit -m "🐛 fix: increase timeout for slow devices"
git commit -m "📚 docs: add API reference guide"
git commit -m "🧪 test: add unit tests for CoverState"
```

---

## 🐛 Debugging

### Logs détaillés

```python
import logging

logging.basicConfig(level=logging.DEBUG)
panel = GeminiAutoFlatPanel()
```

### Inspecter les commandes

```python
# Voir exactement ce qui est envoyé/reçu
response = panel.send_command(">S#")
print(f"Raw response: {repr(response)}")
```

### Tester en isolation

```python
import unittest.mock as mock

with mock.patch('serial.Serial') as mock_serial:
    # Simuler des réponses du panneau
    mock_instance = mock.MagicMock()
    mock_instance.read_until.return_value = b"*OOpened#"
    mock_serial.return_value = mock_instance
    
    # Tester sans vrai hardware
    panel = GeminiAutoFlatPanel()
    result = panel.open_cover()
```

---

## 📚 Documentation

Avant de commiter une PR importante :

1. Mettre à jour les docstrings
2. Ajouter des exemples dans `docs/EXAMPLES.md`
3. Mettre à jour `docs/API.md` si changement d'API
4. Mettre à jour `README.md` si nécessaire

---

## ❓ Questions?

- Consultez les [Issues existantes](https://github.com/ozuntini/Filter_Control/issues)
- Lisez la [Documentation API](docs/API.md)
- Regardez les [Exemples](docs/EXAMPLES.md)
- Ouvrez une [Discussion](https://github.com/ozuntini/Filter_Control/discussions)

---

## 🎉 Merci!

Vos contributions rendent ce projet meilleur pour tous! 

