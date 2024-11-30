import numpy as np
import pygame
import math

class Grille:
    def __init__(self, n_lignes, n_colonnes,nb_survie, nb1_naissance, nb2_naissance):
        self.n_lignes = n_lignes
        self.n_colonnes = n_colonnes
        self.grille = np.zeros((n_lignes, n_colonnes), dtype=int)
        self.nb_survie = nb_survie
        self.nb1_naissance = nb1_naissance
        self.nb2_naissance = nb2_naissance

    # Fonction qui permet de créer une grille aléatoire de taille n_lignes x n_colonnes
    def creer_grille(self):
        self.grille = np.random.randint(0, 2, (self.n_lignes, self.n_colonnes))
    
    # Fonction qui permet de créer une grille vide de taille n_lignes x n_colonnes
    def creer_grille_vide(self):
        self.grille = np.zeros((self.n_lignes, self.n_colonnes), dtype=int)

    # Fonction qui permet de compter les voisins vivants dans une grille considérée comme un tore v1
    def compter_voisins_vivants_laisser_revenir(self, x, y):
        compteur = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                voisin_x = (x + i) % self.n_colonnes
                voisin_y = (y + j) % self.n_lignes
                compteur += self.grille[voisin_y, voisin_x]
        compteur -= self.grille[y, x]
        return compteur

    def evoluer(self):
        # Calculer la somme des voisins vivants directement avec des décalages
        voisins = (
            np.roll(self.grille, 1, axis=0) + 
            np.roll(self.grille, -1, axis=0) +
            np.roll(self.grille, 1, axis=1) + 
            np.roll(self.grille, -1, axis=1) +
            np.roll(np.roll(self.grille, 1, axis=0), 1, axis=1) +
            np.roll(np.roll(self.grille, 1, axis=0), -1, axis=1) +
            np.roll(np.roll(self.grille, -1, axis=0), 1, axis=1) +
            np.roll(np.roll(self.grille, -1, axis=0), -1, axis=1)
        )

        # Application des règles du jeu de la vie
        nouvelle_grille = (self.grille == 1) & ((voisins == self.nb1_naissance) | (voisins == self.nb2_naissance)) | (self.grille == 0) & (voisins == self.nb_survie)

        # Mise à jour de la grille
        self.grille = nouvelle_grille.astype(int)




    def agrandir_grille(self, Fenetre_util, Interface_util):
        largeur_fenetre, hauteur_fenetre = Interface_util.fenetre.get_size()
        self.n_colonnes = (largeur_fenetre - Fenetre_util.taille_statistiques) // Fenetre_util.taille_case
        self.n_lignes  = hauteur_fenetre // Fenetre_util.taille_case
        
        nouvelle_grille = np.zeros((self.n_lignes, self.n_colonnes), dtype=int)
        
        # Calculer les dimensions minimales pour éviter les erreurs de diffusion
        min_lignes = min(self.n_lignes, self.grille.shape[0])
        min_colonnes = min(self.n_colonnes, self.grille.shape[1])
        
        # Copier les valeurs de l'ancienne grille dans la nouvelle grille
        nouvelle_grille[:min_lignes, :min_colonnes] = self.grille[:min_lignes, :min_colonnes]
        
        self.grille = nouvelle_grille

    # Fonction qui verifie les bonnes proportions de la grille:
    def verifier_proportions_grille(self,Fenetre_util):
        if self.n_colonnes * Fenetre_util.taille_case + Fenetre_util.taille_statistiques > 1800:
            Fenetre_util.taille_case = 1800 // self.n_colonnes
        if self.n_lignes * Fenetre_util.taille_case > 800:
            Fenetre_util.taille_case = 800 // self.n_lignes
        if self.n_colonnes * Fenetre_util.taille_case + Fenetre_util.taille_statistiques < 250:
            Fenetre_util.taille_case = 250 // self.n_colonnes
        if self.n_lignes * Fenetre_util.taille_case < 800:
            Fenetre_util.taille_case = 800 // self.n_lignes
        

        Fenetre_util.taille_case_final = Fenetre_util.taille_case
    
    def sauvegarder_grille_npz(self, nom_fichier):
        np.savez(nom_fichier, grille=self.grille)

    def charger_grille_npz(self, nom_fichier):
        with np.load(nom_fichier) as data:
            self.grille = data['grille']
            self.n_lignes, self.n_colonnes = self.grille.shape