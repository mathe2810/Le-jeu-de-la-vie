import numpy as np

# Fonction pour analyser la grille et retourner les statistiques
def analyser_grille(grille):
    n_vivants = np.sum(grille)
    n_morts = grille.size - n_vivants
    return {'vivants': n_vivants, 'morts': n_morts}

# Fonction pour analyser l'évolution de la grille
def analyser_evolution(grille_initiale, grille_finale):
    changement = np.sum(grille_initiale != grille_finale)
    return changement
