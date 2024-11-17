import numpy as np
import pygame
from Interface import *
# Fonction qui permet de créer une grille aléatoire de taille n_lignes x n_colonnes
def creer_grille(n_lignes, n_colonnes):
    return np.random.randint(0, 2, (n_lignes, n_colonnes))

# Fonction qui permet de créer une grille vide de taille n_lignes x n_colonnes
def creer_grille_vide(n_lignes, n_colonnes):
    return np.zeros((n_lignes, n_colonnes), dtype=int)

# Fonction qui permet de compter les voisins vivants dans une grille considérée comme un tore
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

def compter_voisins_vivants_bloquer(grille):
    n_lignes, n_colonnes = grille.shape
    voisins = np.zeros((n_lignes, n_colonnes), dtype=int)
    voisins += np.roll(grille, 1, axis=0)  # Haut
    voisins += np.roll(grille, -1, axis=0)  # Bas
    voisins += np.roll(grille, 1, axis=1)  # Gauche
    voisins += np.roll(grille, -1, axis=1)  # Droite
    voisins += np.roll(np.roll(grille, 1, axis=0), 1, axis=1)  # Haut-Gauche
    voisins += np.roll(np.roll(grille, 1, axis=0), -1, axis=1)  # Haut-Droite
    voisins += np.roll(np.roll(grille, -1, axis=0), 1, axis=1)  # Bas-Gauche
    voisins += np.roll(np.roll(grille, -1, axis=0), -1, axis=1)  # Bas-Droite
    return voisins

# Fonction qui permet de faire évoluer la grille d'un pas de temps
def evoluer(grille):
    n_lignes, n_colonnes = grille.shape
    nouvelle_grille = np.copy(grille)

    # Comptage des voisins vivants en utilisant des décalages
    voisins = np.zeros((n_lignes, n_colonnes), dtype=int)
    voisins += np.roll(grille, 1, axis=0)  # Haut
    voisins += np.roll(grille, -1, axis=0)  # Bas
    voisins += np.roll(grille, 1, axis=1)  # Gauche
    voisins += np.roll(grille, -1, axis=1)  # Droite
    voisins += np.roll(np.roll(grille, 1, axis=0), 1, axis=1)  # Haut-Gauche
    voisins += np.roll(np.roll(grille, 1, axis=0), -1, axis=1)  # Haut-Droite
    voisins += np.roll(np.roll(grille, -1, axis=0), 1, axis=1)  # Bas-Gauche
    voisins += np.roll(np.roll(grille, -1, axis=0), -1, axis=1)  # Bas-Droite

    # Application des règles du jeu de la vie
    nouvelle_grille[(grille == 1) & ((voisins < 2) | (voisins > 3))] = 0
    nouvelle_grille[(grille == 0) & (voisins == 3)] = 1

    return nouvelle_grille


def gerer_souris(grille, taille_case, Bool_pause, Bool_grille, Bool_reinit, last_click_time, evolution_delay, taille_case_final,
                 fenetre, taille_statistiques, scroll_x, scroll_y, click_delay=200):
    current_time = pygame.time.get_ticks()
    new_evolution_delay = evolution_delay
    if current_time - last_click_time < click_delay:
        return grille, Bool_pause, Bool_grille, Bool_reinit, last_click_time, new_evolution_delay, taille_case, taille_case_final, fenetre, scroll_x, scroll_y

    x, y = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:
        if x < 250:
            #Gestion de la Pause
            if x < 250 and y < 100 and x > 0 and y > 70:
                Bool_pause = not Bool_pause

            #Gestion de l'évolution
            elif x > 200 and y > 100 and x < 220 and y < 130:
                new_evolution_delay += 10
            elif x > 220 and y > 100 and x < 240 and y < 130:
                new_evolution_delay -= 10
            
            #Gestion de la grille
            elif x > 0 and y > 160 and x < 250 and y < 190:
                Bool_grille = not Bool_grille

            #Gestion du zoom
            elif x > 200 and y > 190 and x < 220 and y < 220:
                taille_case += 1
            elif x > 220 and y > 190 and x < 240 and y < 220:
                if taille_case == taille_case_final:
                    taille_case_final -= 1
                    if taille_case_final == 0:
                        taille_case_final = 1
                    grille = agrandir_grille(grille, taille_case_final, taille_statistiques, fenetre.get_size())
                    
                else:
                    taille_case -= 1

            # Gestion du scroll
            elif x > 70 and y > 405 and x < 90 and y < 415:
                scroll_x += 1
            elif x > 140 and y > 405 and x < 160 and y < 415:
                scroll_x -= 1
            elif x > 110 and y > 370 and x < 120 and y < 400:
                scroll_y += 1
            elif x > 110 and y > 420 and x < 120 and y < 450:
                scroll_y -= 1

            # Gestion de la réinitialisation
            elif x > 0 and y > 310 and x < 200 and y < 330:
                Bool_reinit = not Bool_reinit

        # Gestion du clic sur la grille
        else:
            x -= taille_statistiques
            x = x // taille_case
            y = y // taille_case
            x += scroll_x
            y += scroll_y
            grille[y, x] = 1 - grille[y, x]
        last_click_time = current_time

    return grille, Bool_pause, Bool_grille, Bool_reinit, last_click_time, new_evolution_delay, taille_case, taille_case_final, fenetre, scroll_x, scroll_y
