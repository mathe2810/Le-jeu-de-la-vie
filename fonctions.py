#                     ___                  ___          ___           ___                   _____          ___                                  ___                                             ___     
#                    /  /\                /  /\        /  /\         /__/\                 /  /::\        /  /\                                /  /\                   ___        ___          /  /\    
#                   /  /:/_              /  /:/       /  /:/_        \  \:\               /  /:/\:\      /  /:/_                              /  /::\                 /__/\      /  /\        /  /:/_   
#   ___     ___    /  /:/ /\            /__/::\      /  /:/ /\        \  \:\             /  /:/  \:\    /  /:/ /\             ___     ___    /  /:/\:\                \  \:\    /  /:/       /  /:/ /\  
#  /__/\   /  /\  /  /:/ /:/_           \__\/\:\    /  /:/ /:/_   ___  \  \:\           /__/:/ \__\:|  /  /:/ /:/_           /__/\   /  /\  /  /:/~/::\                \  \:\  /__/::\      /  /:/ /:/_ 
#  \  \:\ /  /:/ /__/:/ /:/ /\             \  \:\  /__/:/ /:/ /\ /__/\  \__\:\          \  \:\ /  /:/ /__/:/ /:/ /\          \  \:\ /  /:/ /__/:/ /:/\:\           ___  \__\:\ \__\/\:\__  /__/:/ /:/ /\
#   \  \:\  /:/  \  \:\/:/ /:/              \__\:\ \  \:\/:/ /:/ \  \:\ /  /:/           \  \:\  /:/  \  \:\/:/ /:/           \  \:\  /:/  \  \:\/:/__\/          /__/\ |  |:|    \  \:\/\ \  \:\/:/ /:/
#    \  \:\/:/    \  \::/ /:/               /  /:/  \  \::/ /:/   \  \:\  /:/             \  \:\/:/    \  \::/ /:/             \  \:\/:/    \  \::/               \  \:\|  |:|     \__\::/  \  \::/ /:/ 
#     \  \::/      \  \:\/:/               /__/:/    \  \:\/:/     \  \:\/:/               \  \::/      \  \:\/:/               \  \::/      \  \:\                \  \:\__|:|     /__/:/    \  \:\/:/  
#      \__\/        \  \::/                \__\/      \  \::/       \  \::/                 \__\/        \  \::/                 \__\/        \  \:\                \__\::::/      \__\/      \  \::/   
#                    \__\/                             \__\/         \__\/                                \__\/                                \__\/                    ~~~~                   \__\/    

# Description: Ce fichier contient les fonctions qui permettent de manipuler les données de la base de données

# Auteur: Matheo Leon
# Date: 13.11.2024

# Importation des librairies
import pygame
import numpy as np
import random
import time
import math
import pandas as pd

# Partie simulation

# Fonction qui permet de creer une grille aléatoire de taille n_lignes x n_colonnes:

def creer_grille(n_lignes, n_colonnes):
    return np.random.randint(0, 2, (n_lignes, n_colonnes))

# Partie interface graphique

# Fonction qui permet de dessiner les cellules de la grille:

def dessiner_grille(grille, fenetre, taille_case, couleur_vivant, couleur_mort):
    for y in range(0, grille.shape[0] * taille_case, taille_case):
        for x in range(0, grille.shape[1] * taille_case, taille_case):
            if grille[y // taille_case][x // taille_case] == 0:
                pygame.draw.rect(fenetre, couleur_mort, (x, y, taille_case, taille_case))
            else:
                pygame.draw.rect(fenetre, couleur_vivant, (x, y, taille_case, taille_case))

# Exemple d'utilisation de la fonction dessiner_grille :

# Initialisation de la grille
grille = creer_grille(50, 50)

# Initialisation de la fenêtre
pygame.init()
taille_case = 10
couleur_vivant = (255, 255, 255)
couleur_mort = (0, 0, 0)
n_lignes, n_colonnes = grille.shape
taille_fenetre = (n_colonnes * taille_case, n_lignes * taille_case)
fenetre = pygame.display.set_mode(taille_fenetre)

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dessin de la grille
    dessiner_grille(grille, fenetre, taille_case, couleur_vivant, couleur_mort)
    pygame.display.flip()

pygame.quit()



