class Fenetre:
    def __init__(self, taille_statistiques, taille_case, taille_case_final, grille, couleur_vivant, couleur_mort):
        self.taille_statistiques = taille_statistiques
        self.taille_case = taille_case
        self.taille_case_final = taille_case_final
        grille.verifier_proportions_grille(self)
        self.taille_fenetre = (grille.n_colonnes * self.taille_case + taille_statistiques, grille.n_lignes * self.taille_case)
        self.couleur_vivant = couleur_vivant
        self.couleur_mort = couleur_mort