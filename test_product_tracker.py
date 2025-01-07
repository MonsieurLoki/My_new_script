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


    def test_import_data(self):
        """Test de l'import des données"""
        self.tracker.import_data(self.csv_path)
        products = self.tracker.find_products()
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0]["name"], "Ordinateur Test")
        self.assertEqual(float(products[0]["current_price"]), 999.99)

    def test_search_by_name(self):
        """Test de la recherche par nom"""
        self.tracker.import_data(self.csv_path)
        results = self.tracker.find_products(name="Ordinateur")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Ordinateur Test")

    def test_search_by_category(self):
        """Test de la recherche par catégorie"""
        self.tracker.import_data(self.csv_path)
        results = self.tracker.find_products(category="Mobilier")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["category"], "Mobilier")

    def test_search_by_price_range(self):
        """Test de la recherche par plage de prix"""
        self.tracker.import_data(self.csv_path)
        results = self.tracker.find_products(min_price=200, max_price=500)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Bureau Test")

    def test_report_generation(self):
        """Test de la génération de rapport"""
        self.tracker.import_data(self.csv_path)
        report_fd, report_path = tempfile.mkstemp()
        os.close(report_fd)

        try:
            self.tracker.generate_inventory_report(report_path)

            # Vérifier le contenu du rapport
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("Rapport d'inventaire", content)
                self.assertIn("Produits distincts: 2", content)
                self.assertIn("Électronique", content)
                self.assertIn("Mobilier", content)
        finally:
            try:
                os.unlink(report_path)
            except PermissionError:
                pass

    def test_invalid_file_import(self):
        """Test de la gestion des erreurs lors de l'import"""
        with self.assertRaises(FileNotFoundError):
            self.tracker.import_data("fichier_inexistant.csv")

    def test_empty_search_results(self):
        """Test de recherche sans résultats"""
        self.tracker.import_data(self.csv_path)
        results = self.tracker.find_products(name="ProduitInexistant")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()