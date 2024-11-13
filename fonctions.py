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

# Description: Ce fichier contient les fonctions qui permettent de simuler le jeu de la vie de Conway et de dessiner les cellules de la grille.
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

# Règles du jeu de la vie de Conway:
# - une cellule vivante survit si elle a 2 ou 3 voisins vivants,
# - une cellule vivante meurt de solitude ou de surpopulation.
# - une cellule morte peut devenir vivante si elle a exactement 3 voisins vivants.


# Fonction qui permet de creer une grille aléatoire de taille n_lignes x n_colonnes:

def creer_grille(n_lignes, n_colonnes):
    return np.random.randint(0, 2, (n_lignes, n_colonnes))

# Fonction qui permet de compter le nombre de voisins vivants d'une cellule:

def compter_voisins_vivants(grille, x, y):
    n_lignes, n_colonnes = grille.shape
    compteur = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            voisin_x = (x + i) % n_colonnes
            voisin_y = (y + j) % n_lignes
            compteur += grille[voisin_y, voisin_x]
    compteur -= grille[y, x]
    return compteur
    


# Fonction qui permet de faire évoluer la grille d'un pas de temps:

def evoluer(grille):
    n_lignes, n_colonnes = grille.shape
    nouvelle_grille = np.copy(grille)
    for y in range(n_lignes):
        for x in range(n_colonnes):
            n_voisins = compter_voisins_vivants(grille, x, y)
            if grille[y, x] == 1:
                # Règle 1 et 2
                if n_voisins < 2 or n_voisins > 3:
                    nouvelle_grille[y, x] = 0
            else:
                # Règle 3
                if n_voisins == 3:
                    nouvelle_grille[y, x] = 1
    return nouvelle_grille

    
# Partie interface graphique

# Fonction qui permet de dessiner les cellules de la grille:

def dessiner_grille(grille, fenetre, taille_case, couleur_vivant, couleur_mort):
    for y in range(0, grille.shape[0] * taille_case, taille_case):
        for x in range(0, grille.shape[1] * taille_case, taille_case):
            if grille[y // taille_case][x // taille_case] == 0:
                pygame.draw.rect(fenetre, couleur_mort, (x+taille_statistiques, y, taille_case, taille_case))
            else:
                pygame.draw.rect(fenetre, couleur_vivant, (x+taille_statistiques, y, taille_case, taille_case))

def afficher_statistiques(fenetre, font, grille):
    n_vivants = np.sum(grille)
    texte = font.render(f'Cellules vivantes: {n_vivants}', True, (0, 0, 0))
    fenetre.blit(texte, (10, 10))

# Exemple d'utilisation de la fonction dessiner_grille :

# Initialisation de la grille
grille = creer_grille(100, 100)

# Initialisation de la fenêtre
pygame.init()
taille_statistiques = 250
taille_case = 10
couleur_vivant = (255, 255, 255)
couleur_mort = (0, 0, 0)
n_lignes, n_colonnes = grille.shape
taille_fenetre = (n_colonnes * taille_case+taille_statistiques, n_lignes * taille_case)
fenetre = pygame.display.set_mode(taille_fenetre)

# Initialisation de la police de caractères
pygame.font.init()
font = pygame.font.SysFont('Arial', 20)

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Évolution de la grille
    grille = evoluer(grille)
    # Dessin de la grille
    dessiner_grille(grille, fenetre, taille_case, couleur_vivant, couleur_mort)
    # Affichage des statistiques
    pygame.draw.rect(fenetre, (250, 250, 250), (0, 0, 250, taille_fenetre[1]))
    afficher_statistiques(fenetre, font, grille)
    pygame.display.flip()

pygame.quit()



