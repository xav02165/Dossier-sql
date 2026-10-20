"""
    ============================================================================
-- SCRIPT D'INITIALISATION DE LA BASE DE DONNÉES : "Le Panier Fermier"
-- Moteur : SQLite
-- ============================================================================
"""


import sqlite3
def connexion ():
    return sqlite3.connect("BDD.db")


try:
    # 1. Création d'un curseur pour exécuter les commandes SQL
    db = connexion()
    cursor = db.cursor()

    # 2. Activation du support des clés étrangères (bonne pratique)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 3. Liste des requêtes SQL dans l'ordre de suppression
    sql_queries = [
        "DROP TABLE IF EXISTS ligne_commande;",
        "DROP TABLE IF EXISTS commande;",
        "DROP TABLE IF EXISTS produit;",
        "DROP TABLE IF EXISTS producteur;",
        "DROP TABLE IF EXISTS client;"
    ]

    # 4. Exécution des requêtes
    for query in sql_queries:
        cursor.execute(query)
        
except sqlite3.Error as e:
    connexion.rollback()
    print(f"Erreur lors de l'effacement des tables : {e}")

"""
-- ----------------------------------------------------------------------------
-- 1. CRÉATION DE LA STRUCTURE DES TABLES
-- ----------------------------------------------------------------------------
"""

try:
    
    db = connexion()
    cursor = db.cursor()

    # 3. Liste des scripts de création
    queries = [
        """
        CREATE TABLE IF NOT EXISTS producteur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            ville TEXT NOT NULL,
            specialite TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS produit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prix_unitaire REAL NOT NULL CHECK(prix_unitaire > 0),
            stock INTEGER NOT NULL CHECK(stock >= 0),
            producteur_id INTEGER,
            FOREIGN KEY (producteur_id) REFERENCES producteur(id) ON DELETE SET NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS client (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            ville TEXT NOT NULL,
            date_inscription TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS commande (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            date_commande TEXT NOT NULL,
            statut TEXT CHECK(statut IN ('En attente', 'Expédiée', 'Livrée', 'Annulée')),
            FOREIGN KEY (client_id) REFERENCES client(id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS ligne_commande (
            commande_id INTEGER,
            produit_id INTEGER,
            quantite INTEGER NOT NULL CHECK(quantite > 0),
            PRIMARY KEY (commande_id, produit_id),
            FOREIGN KEY (commande_id) REFERENCES commande(id) ON DELETE CASCADE,
            FOREIGN KEY (produit_id) REFERENCES produit(id) ON DELETE RESTRICT
        );
        """
    ]

    # 4. Exécution de chaque bloc SQL
    for query in queries:
        cursor.execute(query)

    # 5. Validation définitive dans le fichier
    db.commit()
    print("Toutes les tables ont été créées avec succès !")

except sqlite3.Error as e:
    db.rollback()
    print(f"Erreur lors de la création des tables : {e}")


"""
-- ----------------------------------------------------------------------------
-- 2. INSERTION DES DONNÉES DE TEST (SEEDING)
-- ----------------------------------------------------------------------------
"""

try:
    
    db = connexion()
    cursor = db.cursor()
    
    # --- A. PRODUCTEURS ---
    producteurs = [
        (1, 'Ferme des Lilas', 'Villefranche', 'Maraîchage bio'),
        (2, 'Le Verger du Soleil', 'Trévoux', 'Fruits et jus'),
        (3, 'Maison Chèvre & Miel', 'Villefranche', 'Fromages et apiculture'),
        (4, 'Domaine du Pain de Mie', 'Anse', 'Boulangerie artisanale'),
        (5, 'Les Potagers du Val', 'Lyon', 'Légumes oubliés')
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO producteur (id, nom, ville, specialite) VALUES (?, ?, ?, ?);", 
        producteurs
    )

    # --- B. PRODUITS ---
    produits = [
        (1, 'Pommes Gala (1kg)', 2.80, 50, 2),
        (2, 'Miel de Lavarde (500g)', 8.50, 15, 3),
        (3, 'Fromage de Chèvre Frais', 3.20, 25, 3),
        (4, 'Jus de Pomme Bio (1L)', 3.50, 40, 2),
        (5, 'Pain au Levain (500g)', 2.50, 30, 4),
        (6, 'Carottes Bio (1kg)', 1.90, 80, 1),
        (7, 'Courgettes (1kg)', 2.20, 60, 1),
        (8, 'Tomates Anciennes (1kg)', 4.10, 35, 1),
        (9, 'Panier Légumes Oubliés (3kg)', 12.00, 10, 5),
        (10, 'Brioche Artisanale', 4.80, 0, 4)
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO produit (id, nom, prix_unitaire, stock, producteur_id) VALUES (?, ?, ?, ?, ?);", 
        produits
    )

    # --- C. CLIENTS ---
    clients = [
        (1, 'Alice Martin', 'alice.martin@email.fr', 'Lyon', '2024-11-15'),
        (2, 'Bernard Dubois', 'b.dubois@email.fr', 'Villefranche', '2025-01-10'),
        (3, 'Chantal Moreau', 'chantal.m@email.fr', 'Lyon', '2025-01-20'),
        (4, 'David Bernard', 'david.b@email.fr', 'Trévoux', '2025-02-01'),
        (5, 'Élodie Petit', 'elodie.petit@email.fr', 'Lyon', '2025-02-15'),
        (6, 'François Leroy', 'f.leroy@email.fr', 'Caluire', '2025-03-01')
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO client (id, nom, email, ville, date_inscription) VALUES (?, ?, ?, ?, ?);", 
        clients
    )

    # --- D. COMMANDES ---
    commandes = [
        (1, 1, '2025-02-10', 'Livrée'),
        (2, 2, '2025-02-12', 'Livrée'),
        (3, 3, '2025-02-18', 'Expédiée'),
        (4, 1, '2025-02-22', 'Livrée'),
        (5, 5, '2025-03-02', 'En attente'),
        (6, 4, '2025-03-03', 'Annulée')
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO commande (id, client_id, date_commande, statut) VALUES (?, ?, ?, ?);", 
        commandes
    )

    # --- E. LIGNES DE COMMANDE ---
    lignes = [
        (1, 1, 2), (1, 4, 1), (1, 5, 2),  # Commande 1
        (2, 2, 1), (2, 3, 3),              # Commande 2
        (3, 8, 2), (3, 6, 3),              # Commande 3
        (4, 9, 1), (4, 2, 2),              # Commande 4
        (5, 7, 2), (5, 5, 1),              # Commande 5
        (6, 1, 1)                          # Commande 6
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO ligne_commande (commande_id, produit_id, quantite) VALUES (?, ?, ?);", 
        lignes
    )

    # 3. Validation des insertions
    db.commit()
    print("Le jeu de données a été inséré avec succès !")

except sqlite3.Error as e:
    db.rollback()
    print(f"Erreur lors de l'insertion des données : {e}")

#---------------------------------EXERCICES partie 1------------------------------------------------
#1) Liste des producteurs : Affichez tous les producteurs, triés par ordre alphabétique de leur nom.

    # Requête de sélection triée par nom
cursor.execute("SELECT nom, ville, specialite FROM producteur ORDER BY nom ASC;")
    
    # Récupération des résultats
producteurs = cursor.fetchall()

print("\n--- LISTE DES PRODUCTEURS (Ordre Alphabétique) ---")
for p in producteurs:
        print(f"Nom : {p[0]} | Ville : {p[1]} | Spécialité : {p[2]}")



#2) Recherche ciblée : Affichez les produits dont le prix unitaire est inférieur à 5,00 euros.
    
    # Requête de sélection 
cursor.execute("SELECT nom, prix_unitaire FROM produit WHERE prix_unitaire < 5.00;")

    # Récupération des résultats
produits = cursor.fetchall()

print("\n--- LISTE DES PRODUITS AVEC UN PRIX INFÉRIEUR A 5 EUROS ---")
for p in produits:
    
    print(f"Produit : {p[0]} ({p[1]} €)")

#3)Trouvez tous les clients habitant à "Lyon" et inscrits après le 1er janvier 2025.

    #Requete de selection:
cursor.execute("SELECT nom, ville, date_inscription FROM client WHERE ville = 'Lyon' AND date_inscription > 2025-01-01;")

        # Récupération des résultats
produits = cursor.fetchall()

print("\n--- LISTE DES CLIENTS HABITANT A LYON ET INSCRITS APRES LE 1er JANVIER 2025---")

for p in produits:
    print(f"Clients : {p[0]} | Ville : {p[1]} | Inscription : {p[2]}")


#4) Affichez les 5 produits les plus chers du catalogue.

    #Requete de selection: 
cursor.execute("SELECT nom, prix_unitaire FROM produit ORDER BY prix_unitaire DESC LIMIT 5;")
    # Récupération des résultats
produits = cursor.fetchall()

print("\n--- LISTE DES 5 PRODUITS LES PLUS CHER---")

for p in produits:
    print(f"Nom: {p[0]} | Prix: {p[1]}")

#-----------------------------------EXERCICES partie 2---------------------------------------
    #1 Combien y a-t-il de clients inscrits au total ?

    #Requete de selection:
cursor.execute("SELECT COUNT (nom) FROM client ;")
    # Récupération des résultats
produits = cursor.fetchall()

print("\n---NOMBRE DE CLIENT INSCRIT---")

for p in produits:
    print(f"Nombre d'inscrit : {p[0]}")

#2 Quel est le prix moyen des produits proposés par la coopérative ? 
    #Quel est le stock total disponible ?

    #Requete de selection:
cursor.execute("SELECT AVG (prix_unitaire), SUM(stock) FROM produit;")
    # Récupération des résultats
produits = cursor.fetchall()

print("\n---PRIX MOYEN ET STOCK TOTAL---")

for p in produits:
    print(f"PRIX MOYEN : {p[0]} | STOCK TOTAL : {p[1]}")

#3 Affichez l'identifiant de chaque producteur ainsi  
    #que le nombre de produits différents qu'il propose.

    #Requete de selection:
    
cursor.execute("SELECT producteur_id, COUNT(id) FROM produit GROUP BY producteur_id;")


# Récupération des résultats
produits = cursor.fetchall()

print("\n--- NOMBRE DE PRODUITS DIFFÉRENTS PAR PRODUCTEUR ---")
for r in produits:
    
    print(f"ID Producteur : {r[0]} | Nombre de produits proposés : {r[1]}")



# 4 Quels sont les producteurs qui proposent plus de 3 produits ?
# Requête de sélection
cursor.execute("SELECT producteur_id, COUNT(id) AS total_produits FROM produit GROUP BY producteur_id HAVING COUNT(id) > 3;")

# Récupération des résultats
produits = cursor.fetchall()

print("\n--- LISTE DES PRODUCTEURS QUI PROPOSENT PLUS DE 3 PRODUITS ---")

# On vérifie si la liste contient des résultats
if len(produits) > 0:
    for r in produits:
        # r[0] est l'id du producteur, r[1] est le nombre de produits (qui est forcément > 3 grâce au SQL)
        print(f"ID Producteur : {r[0]} (Propose {r[1]} produits)")
else:
    print("Il n'existe pas de producteurs qui proposent plus de 3 produits.")

#5 Calculez la valeur totale du stock (quantité en stock multipliée 
    # par le prix unitaire) pour chaque produit.
cursor.execute("SELECT nom, stock, prix_unitaire, (stock * prix_unitaire) AS valeur_stock FROM produit;")

    # Récupération des résultats
produits = cursor.fetchall()

print("\n--- VALEUR TOTALE DU STOCK POUR CHAQUE PRODUIT ---")





    
    # 4. Fermeture de la connexion
db.close()

















