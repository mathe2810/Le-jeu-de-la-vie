import numpy as np

class Grille:
    def __init__(self, n_lignes, n_colonnes, taille_case):
        self.n_lignes = n_lignes
        self.n_colonnes = n_colonnes
        self.taille_case = taille_case
        self.grille = np.zeros((n_lignes, n_colonnes), dtype=int)

    # Fonction qui permet de créer une grille aléatoire de taille n_lignes x n_colonnes
    def creer_grille(self):
        self.grille = np.random.randint(0, 2, (self.n_lignes, self.n_colonnes))
    
    # Fonction qui permet de créer une grille vide de taille n_lignes x n_colonnes
    def creer_grille_vide(self):
        self.grille = np.zeros((self.n_lignes, self.n_colonnes), dtype=int)

    # Fonction qui permet de compter les voisins vivants dans une grille considérée comme un tore
    def compter_voisins_vivants_laisser_revenir(self, x, y):
        compteur = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                voisin_x = (x + i) % self.n_colonnes
                voisin_y = (y + j) % self.n_lignes
                compteur += self.grille[voisin_y, voisin_x]
        compteur -= self.grille[y, x]
        return compteur

    # Fonction qui permet de faire évoluer la grille d'un pas de temps
def evoluer(self):
    nouvelle_grille = np.copy(self.grille)

    # Comptage des voisins vivants en utilisant des décalages
    voisins = np.zeros((self.n_lignes, self.n_colonnes), dtype=int)
    voisins += np.roll(self.grille, 1, axis=0)  # Haut
    voisins += np.roll(self.grille, -1, axis=0)  # Bas
    voisins += np.roll(self.grille, 1, axis=1)  # Gauche
    voisins += np.roll(self.grille, -1, axis=1)  # Droite
    voisins += np.roll(np.roll(self.grille, 1, axis=0), 1, axis=1)  # Haut-Gauche
    voisins += np.roll(np.roll(self.grille, 1, axis=0), -1, axis=1)  # Haut-Droite
    voisins += np.roll(np.roll(self.grille, -1, axis=0), 1, axis=1)  # Bas-Gauche
    voisins += np.roll(np.roll(self.grille, -1, axis=0), -1, axis=1)  # Bas-Droite

    # Application des règles du jeu de la vie
    nouvelle_grille[(self.grille == 1) & ((voisins < 2) | (voisins > 3))] = 0
    nouvelle_grille[(self.grille == 0) & (voisins == 3)] = 1

    self.grille = nouvelle_grille
    
    def compter_voisins_vivants_bloquer(self):
        voisins = np.zeros((self.n_lignes, self.n_colonnes), dtype=int)
        voisins += np.roll(self.grille, 1, axis=0)  # Haut
        voisins += np.roll(self.grille, -1, axis=0)  # Bas
        voisins += np.roll(self.grille, 1, axis=1)  # Gauche
        voisins += np.roll(self.grille, -1, axis=1)  # Droite
        voisins += np.roll(np.roll(self.grille, 1, axis=0), 1, axis=1)  # Haut-Gauche
        voisins += np.roll(np.roll(self.grille, 1, axis=0), -1, axis=1)  # Haut-Droite
        voisins += np.roll(np.roll(self.grille, -1, axis=0), 1, axis=1)  # Bas-Gauche
        voisins += np.roll(np.roll(self.grille, -1, axis=0), -1, axis=1)  # Bas-Droite
        return voisins

class Fenetre:
    def __init__(self, n_lignes, n_colonnes, taille_statistiques, taille_case):
        self.n_lignes = n_lignes
        self.n_colonnes = n_colonnes
        self.taille_statistiques = taille_statistiques
        self.taille_case = taille_case
        self.taille_case_final = taille_case
        self.taille_fenetre = (n_colonnes * taille_case + taille_statistiques, n_lignes * taille_case)

    

    