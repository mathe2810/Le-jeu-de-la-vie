import pandas as pd
import numpy as np

# Fonction pour sauvegarder la grille dans un fichier .npz
def sauvegarder_grille_npz(grille, nom_fichier):
    np.savez_compressed(nom_fichier, grille=grille)

# Fonction pour charger une grille à partir d'un fichier .npz
def charger_grille_npz(nom_fichier):
    with np.load(nom_fichier) as data:
        grille = data['grille']
    return grille

