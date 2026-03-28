from filter_controller import GeminiAutoFlatPanel, CoverState
import logging
import argparse


parser = argparse.ArgumentParser(
    description='Contrôler un GeminiAutoFlatPanel',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Exemples:
  python test_filter_controller.py Open
  python test_filter_controller.py Close
  python test_filter_controller.py Status
  python test_filter_controller.py --port /dev/ttyUSB1 --baudrate 115200 Open
"""
)
parser.add_argument('--port', default='/dev/ttyUSB0', help='Port USB (par défaut: /dev/ttyUSB0)')
parser.add_argument('--baudrate', type=int, default=9600, help='Vitesse de communication (par défaut: 9600)')
parser.add_argument('--timeout', type=float, default=1, help='Délai d\'attente en secondes (par défaut: 1)')
parser.add_argument('action', choices=['Open', 'Close', 'Status'], help='Action à effectuer')

args = parser.parse_args()


# Configurer le logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Créer une instance
panel = GeminiAutoFlatPanel(port=args.port, baudrate=args.baudrate, timeout=args.timeout)

try:
    # Se connecter
    if panel.connect():
        if args.action == 'Open':
            print("🔓 Ouverture du panneau...")
            cover = panel.open_cover()
            if cover == CoverState.OPEN:
                print("✅ Panneau ouvert avec succès")
            else:
                print("❌ Échec de l'ouverture du panneau")
        elif args.action == 'Close':
            print("🔒 Fermeture du panneau...")
            cover = panel.close_cover()
            if cover == CoverState.CLOSED:
                print("✅ Panneau fermé avec succès")
            else:
                print("❌ Échec de la fermeture du panneau")
        elif args.action == 'Status':
            print("🔍 Vérification de l'état du panneau...")
            status = panel.get_device_status()
            if status:
                print(f"✅ État du device:")
                print(f"   ID: {status['device_id']}")
                print(f"   Moteur: {status['motor_status']}")
                print(f"   Lumière: {status['light_status']}")
                print(f"   Couvercle: {status['cover_status']}")
            else:
                print("❌ Impossible de lire l'état")
    else:
        print("❌ Échec de la connexion au panneau")
        
finally:
    # Toujours fermer la connexion
    panel.disconnect()