import csv

# Premier fichier: produits électroniques
electronics_data = [
    {
        "Product Name": "Smartphone Galaxy S21",
        "Category": "Électronique",
        "Price": "899.99",
        "Quantity": "45"
    },
    {
        "Product Name": "MacBook Pro 14",
        "Category": "Électronique",
        "Price": "1599.99",
        "Quantity": "20"
    },
    {
        "Product Name": "Écran Dell 27\"",
        "Category": "Électronique",
        "Price": "349.99",
        "Quantity": "30"
    }
]

# Deuxième fichier: mobilier
furniture_data = [
    {
        "Product Name": "Bureau Ergonomique",
        "Category": "Mobilier",
        "Price": "299.99",
        "Quantity": "25"
    },
    {
        "Product Name": "Chaise Gaming",
        "Category": "Mobilier",
        "Price": "199.99",
        "Quantity": "40"
    },
    {
        "Product Name": "Armoire de Bureau",
        "Category": "Mobilier",
        "Price": "449.99",
        "Quantity": "15"
    }
]

# Création des fichiers CSV
def create_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Product Name", "Category", "Price", "Quantity"])
        writer.writeheader()
        writer.writerows(data)

# Créer les fichiers
create_csv('electronics.csv', electronics_data)
create_csv('furniture.csv', furniture_data)

print("Fichiers CSV créés avec succès!")