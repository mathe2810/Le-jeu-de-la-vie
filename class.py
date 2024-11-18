import numpy as np

class Grille:
    def __init__(self, n_lignes, n_colonnes, taille_case):
        self.n_lignes = n_lignes
        self.n_colonnes = n_colonnes
        self.taille_case = taille_case
        self.grille = np.zeros((n_lignes, n_colonnes), dtype=int)

    