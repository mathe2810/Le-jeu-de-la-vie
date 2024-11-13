import pandas as pd
import numpy as np

# Fonction pour sauvegarder la grille dans un fichier CSV
def sauvegarder_grille(grille, nom_fichier):
    df = pd.DataFrame(grille)
    df.to_csv(nom_fichier, index=False)

# Fonction pour charger une grille à partir d'un fichier CSV
def charger_grille(nom_fichier):
    df = pd.read_csv(nom_fichier)
    grille = df.values
    return grille
