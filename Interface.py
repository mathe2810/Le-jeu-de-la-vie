import pygame
import numpy as np
import random
import time
import math
import pandas as pd

def agrandir_grille(grille, n_lignes_ajout, n_colonnes_ajout):
    n_lignes, n_colonnes = grille.shape
    nouvelle_grille = np.zeros((n_lignes + n_lignes_ajout, n_colonnes + n_colonnes_ajout), dtype=int)
    nouvelle_grille[:n_lignes, :n_colonnes] = grille
    return nouvelle_grille
# Fonction qui verifie les bonnes proportions de la grille:
def verifier_proportions_grille(grille, taille_case, taille_statistiques):
    n_lignes, n_colonnes = grille.shape
    if n_colonnes * taille_case + taille_statistiques > 1920:
        taille_case = 1920 // n_colonnes
    if n_lignes * taille_case > 1080:
        taille_case = 1080 // n_lignes
    if n_colonnes * taille_case + taille_statistiques < 250:
        taille_case = 250 // n_colonnes
    if n_lignes * taille_case < 350:
        taille_case = 350 // n_lignes
    return taille_case


# Fonction qui permet de dessiner les cellules de la grille:
def dessiner_grille(grille, fenetre, taille_case, couleur_vivant, couleur_mort, Bool_grille, taille_statistiques):
    n_lignes, n_colonnes = grille.shape
    for y in range(n_lignes):
        for x in range(n_colonnes):
            rect = pygame.Rect(x * taille_case + taille_statistiques, y * taille_case, taille_case, taille_case)
            if grille[y, x] == 0:
                pygame.draw.rect(fenetre, couleur_mort, rect)
            else:
                pygame.draw.rect(fenetre, couleur_vivant, rect)
            if Bool_grille:
                pygame.draw.rect(fenetre, (128, 128, 128), rect, 1)  # Dessiner les lignes de grille grises


# Fonction pour afficher les statistiques dans l'interface
def afficher_statistiques(fenetre, font, grille, Bool_pause, Bool_grille, Bool_reinit, taille_case, taille_case_final, evolution_delay, clock):
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

    if Bool_reinit == False:
        texte_reinitialiser = font.render(f'Reinitialiser', True, (255, 255, 255))
        pygame.draw.rect(fenetre, (0, 0, 0), (0, 310, 250, 30))
    else:
        texte_reinitialiser = font.render(f'Reinitialiser', True, (0, 0, 0))
        pygame.draw.rect(fenetre, (255, 255, 255), (0, 310, 250, 30))


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
    fenetre.blit(texte_reinitialiser, (60, 310))

