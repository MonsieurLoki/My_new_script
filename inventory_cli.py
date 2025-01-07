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

    def do_import(self, arg):
        """
        Importe un ou plusieurs fichiers CSV.
        Usage: import chemin/vers/fichier1.csv [chemin/vers/fichier2.csv ...]
        """
        files = arg.split()
        if not files:
            print("Erreur: Veuillez spécifier au moins un fichier CSV")
            return

        for file in files:
            path = Path(file)
            if not path.exists():
                print(f"Erreur: Le fichier {file} n'existe pas")
                self.logger.error(f"Tentative d'import d'un fichier inexistant: {file}")
                continue

            try:
                self.tracker.import_data(str(path))
                print(f"Importé avec succès: {file}")
                self.logger.info(f"Fichier importé avec succès: {file}")
            except Exception as e:
                print(f"Erreur lors de l'import de {file}: {str(e)}")
                self.logger.error(f"Erreur d'import: {file} - {str(e)}")

    def do_search(self, arg):
        """
        Recherche des produits selon différents critères.
        Usage: search [-n nom] [-c catégorie] [-min prix_min] [-max prix_max]
        """
        parser = argparse.ArgumentParser(description='Recherche de produits')
        parser.add_argument('-n', '--name', help='Nom du produit')
        parser.add_argument('-c', '--category', help='Catégorie')
        parser.add_argument('-min', '--min_price', type=float, help='Prix minimum')
        parser.add_argument('-max', '--max_price', type=float, help='Prix maximum')

        try:
            args = parser.parse_args(arg.split())

            results = self.tracker.find_products(
                name=args.name,
                category=args.category,
                min_price=args.min_price,
                max_price=args.max_price
            )

            if not results:
                print("Aucun résultat trouvé")
                return

            # Affichage des résultats
            print("\nRésultats de la recherche:")
            print("=" * 80)
            print(f"{'Nom':<30} {'Catégorie':<15} {'Prix':<10} {'Quantité':<10}")
            print("-" * 80)

            for product in results:
                print(f"{product['name']:<30} {product['category']:<15} "
                      f"{product['current_price']:>8.2f}€ {product['current_quantity']:>8}")

            self.logger.info(f"Recherche effectuée avec succès: {len(results)} résultats")

        except Exception as e:
            print(f"Erreur de recherche: {str(e)}")
            print("Utilisez 'help search' pour voir la syntaxe correcte")
            self.logger.error(f"Erreur lors de la recherche: {str(e)}")


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
