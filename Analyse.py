import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import shutil




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
    def charger_statistiques_csv(self, chemin_fichier='statistiques.csv'):
        statistiques = []
        if os.path.exists(chemin_fichier):
            with open(chemin_fichier, mode='r') as file:
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

    def copier_fichier(self, source, destination):
        # Créer le fichier de destination s'il n'existe pas
        if not os.path.exists(destination):
            with open(destination, 'w') as file:
                pass  # Créer un fichier vide
            print(f"Le fichier de destination {destination} a été créé.")

        # Copier le contenu du fichier source vers le fichier de destination
        if os.path.exists(source):
            shutil.copyfile(source, destination)
            print(f"Le fichier {source} a été copié vers {destination}.")
        else:
            print(f"Le fichier source {source} n'existe pas.")
    
    def prendreDerniereIteration(self, chemin_fichier):
        derniere_iteration = None
        if os.path.exists(chemin_fichier):
            with open(chemin_fichier, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    derniere_iteration = row['Iteration']
            return derniere_iteration
        else:
            with open(chemin_fichier, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Iteration', 'Vivants', 'Morts'])  # Écrire l'en-tête si le fichier n'existe pas
                return 0
            
    def vider_fichier(self, chemin_fichier):
        with open(chemin_fichier, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Iteration', 'Vivants', 'Morts'])  # Écrire l'en-tête
        print(f"Le fichier {chemin_fichier} a été vidé.")

    def vider_fichier_temps(self, chemin_fichier):
        with open(chemin_fichier, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Temps', 'Taille', 'Nombre de cellule'])  # Écrire l'en-tête
        print(f"Le fichier {chemin_fichier} a été vidé.")

    def enregister_temps(self, temps, taille_grille, nombre_cellule_vivantes, chemin_fichier='./sauvegarde/temps/temps.csv'):
        existe = os.path.exists(chemin_fichier)
        with open(chemin_fichier, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not existe:
                writer.writerow(['Temps', 'Taille', 'Nombre de cellule'])  # Écrire l'en-tête si le fichier n'existe pas
            writer.writerow([temps,taille_grille,nombre_cellule_vivantes])

    def charger_temps(self, chemin_fichier='./sauvegarde/temps/temps.csv'):
        temps = []
        if os.path.exists(chemin_fichier):
            with open(chemin_fichier, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    temps.append(row)
        return temps
    
    def afficher_courbe_temps(self, temps):
        temps_execution = [float(temp['Temps']) for temp in temps]
        nombre_cellule = [int(temp['Nombre de cellule']) for temp in temps]
        a = []
        for i in range(len(temps_execution)):
            a.append(i)

        fig, ax1 = plt.subplots(figsize=(10, 5))

        color = 'tab:orange'
        ax1.set_xlabel('Nombre de cellules vivantes')
        ax1.set_ylabel('Temps d\'exécution (us)', color=color)
        ax1.plot(a, temps_execution, label='Temps d\'exécution', color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # Instancier un second axe qui partage le même axe x
        color = 'tab:blue'
        ax2.set_ylabel('Nombre de cellules vivantes', color=color)
        ax2.plot(a, nombre_cellule, label='Nombre de cellules vivantes', color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  # Pour éviter que les labels se chevauchent
        plt.title('Temps d\'exécution de l\'évolution en fonction du nombre de cellules vivantes')
        plt.show()

                
