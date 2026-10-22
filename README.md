# Pannier Fermier

Contexte du projet : "Le Panier Fermier" 

Le scénario : Vous venez d'être embouché(e) comme développeur(euse) / data analyste pour "Le Panier 
Fermier", une coopérative locale qui met en relation des producteurs bio et des consommateurs 
urbains. La coopérative a besoin d'auditer ses données, de suivre ses ventes, d'analyser le 
comportement de ses clients et d'optimiser sa chaîne logistique. 

Partie 1 : Les bases - Extraction et Filtrage  
Objectif : Maîtriser le SELECT, les filtres simples, le tri et la pagination. 

1) Liste des producteurs : Affichez tous les producteurs, triés par ordre alphabétique de leur nom. 
2) Recherche ciblée : Affichez les produits dont le prix unitaire est inférieur à 5,00 euros. 
3) Filtres multiples : Trouvez tous les clients habitant à "Lyon" et inscrits après le 1er janvier 2025. 
4) Limitation : Affichez les 5 produits les plus chers du catalogue.
   
Partie 2 : Fonctions d'agrégation et Regroupement  
Objectif : Calculer des métriques métier clés avec GROUP BY et HAVING. 

1) Comptage simple : Combien y a-t-il de clients inscrits au total ? 
2) Moyennes et Totaux : Quel est le prix moyen des produits proposés par la coopérative ? Quel est 
le stock total disponible ? 
3) Agrégation par producteur : Affichez l'identifiant de chaque producteur ainsi que le nombre de 
produits différents qu'il propose. 
4) Filtrage sur agrégat (HAVING) : Quels sont les producteurs qui proposent plus de 3 produits ? 
5) Chiffre d'affaires potentiel : Calculez la valeur totale du stock (quantité en stock multipliée par le 
prix unitaire) pour chaque produit.

Partie 3 : Les Jointures et Relations  
Objectif : Croiser les tables pour reconstituer l'information métier. 

1) Jointure simple : Affichez la liste de tous les produits avec le nom du producteur associé (Nom du 
produit, Prix, Nom du producteur, Ville du producteur). 
2) Commandes clients : Affichez les détails des commandes (ID de commande, date, statut) avec le 
nom et l'email du client correspondant. 
3) Jointure multi-tables (Le ticket de caisse) : Pour la commande dont l'ID est 1, affichez la liste 
des produits commandés, leur quantité, leur prix unitaire et le montant total pour chaque ligne. 
4) Clients sans commande (LEFT JOIN) : Identifiez les clients qui n'ont jamais passé de commande à 
ce jour.

Partie 4 : Modifications, Contraintes et Transactions  
Objectif : Savoir modifier les données en toute sécurité et respecter l'intégrité. 

1) Insertion : Ajoutez un nouveau client de votre choix dans la base de données. 
2) Mise à jour : Suite à une inflation, augmentez de 5% le prix de tous les produits du producteur 
"Ferme des Lilas". 
3) Gestion des stocks (Transaction) : Un client passe une commande. Simulez cette opération dans 
une transaction (BEGIN TRANSACTION, COMMIT) : 
a. Insérez une nouvelle commande pour ce client. 
b. Insérez la ligne de commande associée. 
c. Mettez à jour (décrémentez) le stock du produit concerné. 
(Si le stock devient négatif, la transaction doit être annulée avec ROLLBACK).

Partie 5 : Requêtes Complexes et Analyses Avancées  
Objectif : Résoudre des problématiques métier fines avec des sous-requêtes ou des CTE (Common 
Table Expressions). 

1) Sous-requête : Affichez-le ou les produits qui ont le prix unitaire le plus élevé de toute la base. 
2) Analyse avec WITH (CTE) : 
a. Créez une CTE calculant le chiffre d'affaires total généré par chaque client (Somme de 
quantite * prix_unitaire pour ses commandes livrées). 
b. Utilisez cette CTE pour afficher uniquement les clients dont le total des achats dépasse 100 
euros. 
3) Cas conditionnels (CASE WHEN) : Affichez la liste des produits avec leur nom, leur prix, et une 
colonne textuelle "Gamme" qui indique : 
a. "Économique" si le prix est $< 3\text{€}$ 
b. "Standard" si le prix est entre $3\text{€}$ et $10\text{€}$ 
c. "Premium" si le prix est $> 10\text{€}$

Partie 6 : Performance et Indexation 
Objectif : Comprendre l'impact des index sur les performances de recherche. 

1) Analyse de requête : Utilisez la commande EXPLAIN QUERY PLAN devant une requête de 
recherche de client par son email. Observez le plan d'exécution. 
2) Création d'index : Créez un index sur la colonne email de la table client. 
3) Vérification : Relancez le EXPLAIN QUERY PLAN et observez la différence (passage d'un parcours 
de table complet à une recherche par index).

Initialisation de la base de données 
Pour commencer, les apprenants exécutent le script de création de la structure et d'insertion des 
données de base. 
Pour cela : en mode console  
sqlite3 panier_fermier.db < init_db.sql 
ou utilisation de VSCode
