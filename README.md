# Système de Gestion d'Inventaire

## Introduction
Ce script permet de **gérer un inventaire de produits** via une interface en ligne de commande.  
Il offre plusieurs fonctionnalités comme **l'importation de fichiers CSV**, **la recherche de produits** et **la génération de rapports**.  

Ce projet est utile pour toute personne souhaitant suivre et analyser son stock de manière simple et efficace.

---

## Fonctionnalités

### Importation de produits
- Permet d'ajouter des produits à l'inventaire depuis un **fichier CSV**.
- Vérifie que les données sont bien formatées avant l'ajout.
- Enregistre les produits dans une **base de données SQLite**.

### Recherche et filtrage
- Recherche de produits par **nom**, **catégorie** ou **prix**.
- Affichage détaillé des produits trouvés.
- Permet de filtrer par **gamme de prix**.

### Génération de rapports
- Produit un **fichier de rapport** listant les stocks et leur valeur.
- Analyse l'inventaire par **catégorie** et **quantité disponible**.
- Donne une vue d’ensemble sur les stocks et leur évolution.

---

## Format des fichiers CSV

Les fichiers à importer doivent être sous le format suivant :

```csv
Product Name,Category,Price,Quantity
iPhone 14,Électronique,999.99,30
Chaise Gaming,Mobilier,199.99,15
Écran 4K,Électronique,599.99,10

## Installation et Lancement
### Prérequis

Avant de commencer, assure-toi d'avoir Python 3.x installé.
Tu peux vérifier avec la commande :

```bash
python --version
```

## Télécharger le projet

Si tu utilises Git :

```bash
git clone https://github.com/MonsieurLoki/My_new_script
cd votre-repo
```

## Lancer le programme

Une fois dans le dossier, exécute :

```bash
python inventory_cli.py
```

Un menu interactif s’affichera pour te guider.

