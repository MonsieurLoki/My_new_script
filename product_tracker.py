import sqlite3
import csv
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from contextlib import contextmanager


@dataclass
class ProductEvent:
    product_id: int
    event_type: str  # 'add', 'remove', 'update'
    quantity_change: int
    price: float
    timestamp: datetime


@dataclass
class Product:
    name: str
    category: str
    price: float
    quantity: int


class ProductTracker:
    def __init__(self, db_path: str = "inventory.db"):
        self.db_path = db_path
        self._initialize_db()

    @contextmanager
    def _get_connection(self):
        """Gestionnaire de contexte pour la connexion à la base de données"""
        conn = sqlite3.connect(self.db_path, timeout=20)
        try:
            yield conn
        finally:
            conn.close()

    def _initialize_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT,
                    current_price REAL,
                    current_quantity INTEGER DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS inventory_events (
                    id INTEGER PRIMARY KEY,
                    product_id INTEGER,
                    event_type TEXT,
                    quantity_change INTEGER,
                    price REAL,
                    timestamp DATETIME,
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """)
            conn.commit()

    def import_data(self, filepath: str) -> None:
        products = []
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                products.append({
                    'name': row['Product Name'],
                    'category': row['Category'],
                    'price': float(row['Price']),
                    'quantity': int(row['Quantity'])
                })

        with self._get_connection() as conn:
            for product in products:
                cursor = conn.execute(
                    "INSERT INTO products (name, category, current_price, current_quantity) VALUES (?, ?, ?, ?)",
                    (product['name'], product['category'], product['price'], product['quantity'])
                )
                product_id = cursor.lastrowid
                conn.execute(
                    """
                    INSERT INTO inventory_events 
                    (product_id, event_type, quantity_change, price, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (product_id, 'add', product['quantity'],
                     product['price'], datetime.now())
                )
            conn.commit()

    def find_products(self,
                      name: Optional[str] = None,
                      category: Optional[str] = None,
                      min_price: Optional[float] = None,
                      max_price: Optional[float] = None) -> List[Dict]:
        query = "SELECT * FROM products WHERE 1=1"
        params = []

        if name:
            query += " AND name LIKE ?"
            params.append(f"%{name}%")
        if category:
            query += " AND category = ?"
            params.append(category)
        if min_price is not None:
            query += " AND current_price >= ?"
            params.append(min_price)
        if max_price is not None:
            query += " AND current_price <= ?"
            params.append(max_price)

        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def generate_inventory_report(self, output_file: str) -> None:
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row

            # Get general statistics
            stats = conn.execute("""
                SELECT 
                    COUNT(*) as total_products,
                    SUM(current_quantity) as total_quantity,
                    SUM(current_quantity * current_price) as total_value
                FROM products
            """).fetchone()

            # Get category statistics
            category_stats = conn.execute("""
                SELECT 
                    category,
                    COUNT(*) as product_count,
                    SUM(current_quantity) as total_quantity,
                    SUM(current_quantity * current_price) as total_value
                FROM products
                GROUP BY category
            """).fetchall()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== Rapport d'inventaire ===\n\n")
            f.write(f"Produits distincts: {stats['total_products']}\n")
            f.write(f"Quantité totale: {stats['total_quantity']}\n")
            f.write(f"Valeur totale: {stats['total_value']:.2f}€\n\n")

            f.write("=== Par catégorie ===\n")
            for cat_stat in category_stats:
                f.write(f"\n{cat_stat['category']}:\n")
                f.write(f"  Nombre de produits: {cat_stat['product_count']}\n")
                f.write(f"  Quantité totale: {cat_stat['total_quantity']}\n")
                f.write(f"  Valeur: {cat_stat['total_value']:.2f}€\n")