import unittest
import os
import tempfile
import csv
from datetime import datetime
from product_tracker import ProductTracker

class TestProductTracker(unittest.TestCase):
    def setUp(self):
        """Configuration avant chaque test"""
        # Créer une base de données temporaire
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.tracker = ProductTracker(self.db_path)

        # Créer un fichier CSV temporaire avec des données de test
        self.csv_fd, self.csv_path = tempfile.mkstemp()
        self.test_data = [
            {
                "Product Name": "Ordinateur Test",
                "Category": "Électronique",
                "Price": "999.99",
                "Quantity": "10"
            },
            {
                "Product Name": "Bureau Test",
                "Category": "Mobilier",
                "Price": "299.99",
                "Quantity": "5"
            }
        ]

        # Écrire les données de test dans le CSV
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["Product Name", "Category", "Price", "Quantity"]
            )
            writer.writeheader()
            writer.writerows(self.test_data)

    def tearDown(self):
        """Nettoyage après chaque test"""
        # Fermer la connexion à la base de données
        del self.tracker  # Force la fermeture de la connexion

        # Fermer et supprimer les fichiers temporaires
        os.close(self.db_fd)
        os.close(self.csv_fd)
        try:
            os.unlink(self.db_path)
        except PermissionError:
            pass  # Ignorer si le fichier est déjà supprimé
        try:
            os.unlink(self.csv_path)
        except PermissionError:
            pass  # Ignorer si le fichier est déjà supprimé


if __name__ == '__main__':
    unittest.main()