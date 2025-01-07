import argparse
import cmd
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from product_tracker import ProductTracker

class InventoryShell(cmd.Cmd):
    intro = """
    ===========================================
    Système de Gestion d'Inventaire v1.0
    ===========================================
    Tapez 'help' ou '?' pour la liste des commandes
    Tapez 'quit' pour quitter
    """
    prompt = '(inventaire) '

    def __init__(self):
        super().__init__()
        # Configuration du logging
        logging.basicConfig(
            filename=f'inventory_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Initialisation du tracker
        self.tracker = ProductTracker("inventory.db")
        self.logger.info("Système de gestion d'inventaire initialisé")

def main():
    try:
        InventoryShell().cmdloop()
    except KeyboardInterrupt:
        print("\nAu revoir!")
    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")
        logging.error(f"Erreur fatale: {str(e)}")

if __name__ == '__main__':
    main()
