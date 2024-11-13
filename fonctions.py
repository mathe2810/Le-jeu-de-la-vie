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

# Fonction qui permet de creer une grille vide de taille n_lignes x n_colonnes:

def creer_grille_vide(n_lignes, n_colonnes):
    return np.zeros((n_lignes, n_colonnes), dtype=int)



# Fonction qui permet de compter le nombre de voisins vivants d'une cellule : permet de compter les voisins vivants d'une cellule en considérant que la grille est un tore.

def compter_voisins_vivants_laisser_revenir(grille, x, y):
    n_lignes, n_colonnes = grille.shape
    compteur = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            voisin_x = (x + i) % n_colonnes
            voisin_y = (y + j) % n_lignes
            compteur += grille[voisin_y, voisin_x]
    compteur -= grille[y, x]
    return compteur

# Fonction qui permet de compter le nombre de voisins vivants d'une cellule : permet de compter les voisins vivants d'une cellule en considérant que la grille n est pas un tore.

def compter_voisins_vivants_bloquer(grille, x, y):
    n_lignes, n_colonnes = grille.shape
    compteur = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            voisin_x = x + i
            voisin_y = y + j
            if 0 <= voisin_x < n_colonnes and 0 <= voisin_y < n_lignes:
                compteur += grille[voisin_y, voisin_x]
    return compteur
    


# Fonction qui permet de faire évoluer la grille d'un pas de temps:

def evoluer(grille):
    n_lignes, n_colonnes = grille.shape
    nouvelle_grille = np.copy(grille)
    for y in range(n_lignes):
        for x in range(n_colonnes):
            n_voisins = compter_voisins_vivants_laisser_revenir(grille, x, y)
            if grille[y, x] == 1:
                # Règle 1 et 2
                if n_voisins < 2 or n_voisins > 3:
                    nouvelle_grille[y, x] = 0
            else:
                # Règle 3
                if n_voisins == 3:
                    nouvelle_grille[y, x] = 1
    return nouvelle_grille

# Fonction qui permet d'agrandir la grille de n_lignes_ajout lignes et n_colonnes_ajout colonnes:

def agrandir_grille(grille, n_lignes_ajout, n_colonnes_ajout):
    n_lignes, n_colonnes = grille.shape
    nouvelle_grille = np.zeros((n_lignes + n_lignes_ajout, n_colonnes + n_colonnes_ajout), dtype=int)
    nouvelle_grille[:n_lignes, :n_colonnes] = grille
    return nouvelle_grille
    
# Partie interface graphique

# Fonction qui verifie les bonnes proportions de la grille:

def verifier_proportions_grille(grille, taille_case, taille_statistiques):
    n_lignes, n_colonnes = grille.shape
    if n_colonnes * taille_case+taille_statistiques > 1920:
        taille_case = 1920 // n_colonnes
    if n_lignes * taille_case > 1080:
        taille_case = 1080 // n_lignes

    if n_colonnes * taille_case+taille_statistiques < 250:
        taille_case = 250 // n_colonnes

    if n_lignes * taille_case < 350:
        taille_case = 350 // n_lignes

    return taille_case


# Fonction qui permet de dessiner les cellules de la grille:

def dessiner_grille(grille, fenetre, taille_case, couleur_vivant, couleur_mort, Bool_grille):
    n_lignes, n_colonnes = grille.shape
    for y in range(n_lignes):
        for x in range(n_colonnes):
            if Bool_grille == True:
                rect = pygame.Rect(x * taille_case + taille_statistiques, y * taille_case, taille_case, taille_case)
                if grille[y, x] == 0:
                    pygame.draw.rect(fenetre, couleur_mort, rect)
                else:
                    pygame.draw.rect(fenetre, couleur_vivant, rect)
                pygame.draw.rect(fenetre, (128, 128, 128), rect, 1)  # Dessiner les lignes de grille grises
            else:
                if grille[y][x] == 0:
                    pygame.draw.rect(fenetre, couleur_mort, (x * taille_case + taille_statistiques, y * taille_case, taille_case, taille_case))
                else:
                    pygame.draw.rect(fenetre, couleur_vivant, (x * taille_case + taille_statistiques, y * taille_case, taille_case, taille_case))

def afficher_statistiques(fenetre, font, grille, Bool_pause,Bool_grille):
    n_vivants = np.sum(grille)
    pos_souris = pygame.mouse.get_pos()
    
    texte_vivants = font.render(f'Cellules vivantes: {n_vivants}', True, (0, 0, 0))
    texte_souris = font.render(f'Position souris: {pos_souris}', True, (0, 0, 0))
    if Bool_pause == False:
        texte_pause = font.render(f'Pause', True, (255, 255, 255))
        pygame.draw.rect(fenetre, (0, 0, 0), (0, 70, 250, 30))
    else:
        texte_pause = font.render(f'Pause', True, (0, 0, 0))
        pygame.draw.rect(fenetre, (255, 255, 255), (0, 70, 250, 30))

    texte_delai_evolutions = font.render(f'évolutions: {evolution_delay} ms', True, (0, 0, 0))
    texte_plus = font.render(f'+', True, (0, 0, 0))
    texte_moins = font.render(f'-', True, (0, 0, 0))

    texte_fps = font.render(f'FPS: {math.ceil(clock.get_fps())}', True, (0, 0, 0))

    if Bool_grille == False:
        texte_grille = font.render(f'Grille', True, (255, 255, 255))
        pygame.draw.rect(fenetre, (0, 0, 0), (0, 160, 250, 30))
    else:
        texte_grille = font.render(f'Grille', True, (0, 0, 0))
        pygame.draw.rect(fenetre, (255, 255, 255), (0, 160, 250, 30))

    texte_zoom = font.render(f'Zoom', True, (0, 0, 0))
    texte_plus = font.render(f'+', True, (0, 0, 0))
    texte_moins = font.render(f'-', True, (0, 0, 0))
    texte_taille_grille = font.render(f'Taille grille: {grille.shape}', True, (0, 0, 0))
    texte_taille_case = font.render(f'Taille case: {taille_case}', True, (0, 0, 0))
    texte_taille_finale_case = font.render(f'Taille finale case: {taille_case_final}', True, (0, 0, 0))


    
    fenetre.blit(texte_vivants, (10, 10))
    fenetre.blit(texte_souris, (10, 40))
    fenetre.blit(texte_pause, (90, 70))
    fenetre.blit(texte_delai_evolutions, (10, 100))
    fenetre.blit(texte_plus, (200, 100))
    fenetre.blit(texte_moins, (220, 100))
    fenetre.blit(texte_fps, (10, 130))
    fenetre.blit(texte_grille, (90, 160))
    fenetre.blit(texte_zoom, (10, 190))
    fenetre.blit(texte_plus, (200, 190))
    fenetre.blit(texte_moins, (220, 190))
    fenetre.blit(texte_taille_grille, (10, 220))
    fenetre.blit(texte_taille_case, (10, 250))
    fenetre.blit(texte_taille_finale_case, (10, 280))

# Partie utilisateur 

# Fonction qui permet de gerer la souris pour changer l'etat des cellules:

def gerer_souris(grille, taille_case, Bool_pause, Bool_grille, last_click_time, evolution_delay, taille_case_final, fenetre, click_delay=200):
    current_time = pygame.time.get_ticks()
    new_evolution_delay = evolution_delay
    if current_time - last_click_time < click_delay:
        return grille, Bool_pause, Bool_grille, last_click_time, new_evolution_delay, taille_case, taille_case_final, fenetre

    x, y = pygame.mouse.get_pos()
    
    if pygame.mouse.get_pressed()[0]:
        if x < 250 and y < 100 and x > 0 and y > 70:
            Bool_pause = not Bool_pause
        elif x > 200 and y > 100 and x < 220 and y < 130:
            new_evolution_delay += 10
        elif x > 220 and y > 100 and x < 240 and y < 130:
            new_evolution_delay -= 10
        elif x > 0 and y > 160 and x < 250 and y < 190:
            Bool_grille = not Bool_grille
        elif x > 200 and y > 190 and x < 220 and y < 220:
            taille_case += 1
        elif x > 220 and y > 190 and x < 240 and y < 220:
            if taille_case == taille_case_final:
                grille = agrandir_grille(grille, 1, 1)
                taille_case_final -= 1
                taille_case_final = verifier_proportions_grille(grille, taille_case, taille_statistiques)
                taille_fenetre = (n_colonnes * taille_case_final+taille_statistiques, n_lignes * taille_case_final)
                fenetre = pygame.display.set_mode(taille_fenetre)
            else:
                taille_case -= 1
        else :
            x -= taille_statistiques
            x = x // taille_case
            y = y // taille_case
            grille[y, x] = 1 - grille[y, x]
        last_click_time = current_time
        
    
    return grille, Bool_pause, Bool_grille, last_click_time, new_evolution_delay, taille_case, taille_case_final, fenetre



    
        




# Exemple d'utilisation de la fonction dessiner_grille :

# Initialisation de la grille
grille = creer_grille(90, 50)
# grille = creer_grille_vide(50, 50)

# Initialisation de la fenêtre
pygame.init()
taille_statistiques = 250
taille_case = 5
couleur_vivant = (255, 255, 255)
couleur_mort = (0, 0, 0)
n_lignes, n_colonnes = grille.shape
taille_case = verifier_proportions_grille(grille, taille_case, taille_statistiques)

taille_case_final = taille_case

taille_fenetre = (n_colonnes * taille_case+taille_statistiques, n_lignes * taille_case)
fenetre = pygame.display.set_mode(taille_fenetre)

# Initialisation de la police de caractères
pygame.font.init()
font = pygame.font.SysFont('Arial', 20)

# Variables de contrôle
Bool_pause = False
Bool_grille = False
last_click_time = 0

# Initialisation de l'horloge
clock = pygame.time.Clock()
fps = 160  # Définir le nombre d'images par seconde

# Variables pour contrôler le délai entre les évolutions
evolution_delay = 100  # Délai en millisecondes
last_evolution_time = pygame.time.get_ticks()

# Boucle principale du jeu
running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    if not Bool_pause :
        # Évolution de la grille à intervalles réguliers
        if current_time - last_evolution_time >= evolution_delay:
            grille = evoluer(grille)
            last_evolution_time = current_time


    # Gestion de la souris
    grille, Bool_pause, Bool_grille, last_click_time, evolution_delay, taille_case, taille_case_final, fenetre = gerer_souris(grille, taille_case, Bool_pause, Bool_grille, last_click_time, evolution_delay, taille_case_final, fenetre)

    
    # Dessin de la grille
    dessiner_grille(grille, fenetre, taille_case, couleur_vivant, couleur_mort,Bool_grille)
    # Affichage des statistiques
    pygame.draw.rect(fenetre, (250, 250, 250), (0, 0, 250, taille_fenetre[1]))
    afficher_statistiques(fenetre, font, grille, Bool_pause,Bool_grille)
    pygame.display.flip()

    # Contrôler le taux de rafraîchissement
    clock.tick(fps)

pygame.quit()



