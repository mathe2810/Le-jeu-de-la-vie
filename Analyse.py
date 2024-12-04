import numpy as np
import csv
import os
import matplotlib.pyplot as plt

class Analyse:
    def __init__(self):
        pass

    # Fonction pour analyser l'évolution de la grille
    def analyser_evolution(self,grille_initiale, grille_finale):
        changement = np.sum(grille_initiale != grille_finale)
        return changement

    # Fonction pour stocker les statistiques des cellules vivantes et mortes à chaque itération dans un fichier CSV
    def stocker_statistiques_csv(self,n_vivants, n_morts, iteration, nom_fichier='statistiques.csv'):
        existe = os.path.exists(nom_fichier)
        with open(nom_fichier, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not existe:
                writer.writerow(['Iteration', 'Vivants', 'Morts'])  # Écrire l'en-tête si le fichier n'existe pas
            writer.writerow([iteration, n_vivants, n_morts])

    # Fonction pour charger les statistiques depuis un fichier CSV
    def charger_statistiques_csv(self):
        fichier = 'statistiques.csv'
        statistiques = []
        if os.path.exists(fichier):
            with open(fichier, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    statistiques.append(row)
        return statistiques

    # Fonction pour supprimer les statistiques
    def supprimer_statistiques(self):
        if os.path.exists('statistiques.csv'):
            os.remove('statistiques.csv')

    # Fonction pour afficher les statistiques sous forme de courbe
    def afficher_courbe_statistiques(self,statistiques):
        iterations = [int(stat['Iteration']) for stat in statistiques]
        vivants = [int(stat['Vivants']) for stat in statistiques]
        morts = [int(stat['Morts']) for stat in statistiques]

        plt.figure(figsize=(10, 5))
        plt.plot(iterations, vivants, label='Cellules Vivantes', color='green')
        plt.plot(iterations, morts, label='Cellules Mortes', color='red')
        plt.xlabel('Itérations')
        plt.ylabel('Nombre de Cellules')
        plt.title('Évolution des Cellules Vivantes et Mortes')
        plt.legend()
        plt.grid(True)
        plt.show()
