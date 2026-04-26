#!/bin/bash
# Script de test lancement test filter controller Python

set -e
# Définir une fonction d'erreur
on_error() {
    if [ -n "$VIRTUAL_ENV" ]; then
        # Désactivation de l'environnement virtuel et sortie avec code d'erreur
        echo "Désactivation de l'environnement virtuel et sortie sur erreur..."
        deactivate
    fi
    exit 1
}

# Capturer les erreurs
trap 'on_error' ERR

PARAM=""

echo "=== Lanceur test_filter_controller ==="

if [ "$1" == "" ] || [ -d "$1" ] || [ "$1" == "-h" ] || [ "$#" -lt 1 ] || [ "$#" -gt 1 ]; then
    echo "usage: "$0" [-o|--open ou -c|--close ou -s|--status ou -p|--position]"
    exit
else
    # Traiter les paramètres
    while [[ $# -gt 0 ]]; do
        case $1 in
        -o|--open)
            PARAM="Open"
            shift
            ;;
        -c|--close)
            PARAM="Close"
            shift
            ;;
        -s|--status)
            PARAM="Status"
            shift
            ;;
        -p|--position)
            PARAM="SetPosition"
            shift
            ;;
        *)
            echo "Option inconnue: $1"
            exit 1
            ;;
        esac
    done
fi

# Activation de l'environnement virtuel si disponible
if [ -f ~/eclipse_env/bin/activate ]; then
    echo "Activation de l'environnement virtuel..."
    source ~/eclipse_env/bin/activate
fi

# Lancement du script principal
echo "Lancement du script principal..."
echo "Command: python3 ./test_filter_controller.py $PARAM"
echo ""
echo "===================================="
sleep 1
python3 ./test_filter_controller.py $PARAM

# Désactivation de l'environnement virtuel
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Désactivation de l'environnement virtuel..."
    deactivate
fi

# Fin du script
