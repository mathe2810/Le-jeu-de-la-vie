import pygame
import numpy as np
import random
import time
import math
import pandas as pd


#Fonction pour afficher le Menu avec Pygame:

def Menu():
    pygame.init()
    taille_fenetre = (800, 600)
    fenetre = pygame.display.set_mode(taille_fenetre)
    pygame.display.set_caption('Menu')
    font = pygame.font.SysFont('Arial', 30)
    font_petit = pygame.font.SysFont('Arial', 20)
    couleur_fond = (255, 255, 255)
    couleur_texte = (0, 0, 0)
    couleur_bouton = (200, 200, 200)
    couleur_bouton_hover = (150, 150, 150)
    couleur_bouton_click = (100, 100, 100)
    couleur_bouton_texte = (0, 0, 0)
    couleur_bouton_texte_hover = (255, 255, 255)
    couleur_bouton_texte_click = (255, 255, 255)
    running = True
    while running:
        fenetre.fill(couleur_fond)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pos_souris = pygame.mouse.get_pos()
        if 300 <= pos_souris[0] <= 500 and 200 <= pos_souris[1] <= 250:
            couleur_bouton_actuelle = couleur_bouton_hover
            couleur_texte_actuelle = couleur_bouton_texte_hover
            if pygame.mouse.get_pressed()[0]:
                couleur_bouton_actuelle = couleur_bouton_click
                couleur_texte_actuelle = couleur_bouton_texte_click
                time.sleep(0.2)
                return True
        else:
            couleur_bouton_actuelle = couleur_bouton
            couleur_texte_actuelle = couleur_bouton_texte
        pygame.draw.rect(fenetre, couleur_bouton_actuelle, (300, 200, 200, 50))
        texte = font.render('Jouer', True, couleur_texte_actuelle)
        fenetre.blit(texte, (370, 210))
        pygame.display.flip()
    pygame.quit()
    return False

    

def agrandir_grille(grille, taille_case, taille_statistiques, taille_fenetre):
    n_colonnes, n_lignes = calculer_nombre_colonnes_lignes(taille_fenetre, taille_case, taille_statistiques)
    nouvelle_grille = np.zeros((n_lignes, n_colonnes), dtype=int)
    
    # Calculer les dimensions minimales pour éviter les erreurs de diffusion
    min_lignes = min(n_lignes, grille.shape[0])
    min_colonnes = min(n_colonnes, grille.shape[1])
    
    # Copier les valeurs de l'ancienne grille dans la nouvelle grille
    nouvelle_grille[:min_lignes, :min_colonnes] = grille[:min_lignes, :min_colonnes]
    
    return nouvelle_grille

def calculer_nombre_colonnes_lignes(taille_fenetre, taille_case, taille_statistiques):
    largeur_fenetre, hauteur_fenetre = taille_fenetre
    print(largeur_fenetre, hauteur_fenetre)
    nombre_colonnes = (largeur_fenetre - taille_statistiques) // taille_case
    nombre_lignes = hauteur_fenetre // taille_case
    print(nombre_colonnes, nombre_lignes)
    return nombre_colonnes, nombre_lignes
    



# Fonction qui verifie les bonnes proportions de la grille:
def verifier_proportions_grille(grille, taille_case, taille_statistiques):
    n_lignes, n_colonnes = grille.shape
    if n_colonnes * taille_case + taille_statistiques > 1920:
        taille_case = 1920 // n_colonnes
    if n_lignes * taille_case > 1080:
        taille_case = 1080 // n_lignes
    if n_colonnes * taille_case + taille_statistiques < 250:
        taille_case = 250 // n_colonnes
    if n_lignes * taille_case < 450:
        taille_case = 450 // n_lignes
    return taille_case


# Fonction qui permet de dessiner les cellules de la grille:
import pygame

def dessiner_grille(grille, fenetre, taille_case, couleur_vivant, couleur_mort, Bool_grille, taille_statistiques, scroll_x, scroll_y):
    n_lignes, n_colonnes = grille.shape

    # Créer une grille de rectangles
    x_coords, y_coords = np.meshgrid(np.arange(n_colonnes), np.arange(n_lignes))
    x_coords = (x_coords - scroll_x) * taille_case + taille_statistiques
    y_coords = (y_coords - scroll_y) * taille_case

    # Dessiner les cellules vivantes et mortes
    for y in range(n_lignes):
        for x in range(n_colonnes):
            rect = pygame.Rect(x_coords[y, x], y_coords[y, x], taille_case, taille_case)
            color = couleur_vivant if grille[y, x] else couleur_mort
            pygame.draw.rect(fenetre, color, rect)

            if Bool_grille:
                pygame.draw.rect(fenetre, (128, 128, 128), rect, 1)  # Dessiner les lignes de grille grises

# Fonction pour afficher les statistiques dans l'interface
def afficher_statistiques(fenetre, font, grille, Bool_pause, Bool_grille, Bool_reinit, Bool_forme, taille_case, taille_case_final, evolution_delay, clock):
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

    if Bool_forme == False:
        texte_forme = font.render(f'Forme', True, (255, 255, 255))
        pygame.draw.rect(fenetre, (0, 0, 0), (0, 340, 250, 30))
    else:
        texte_forme = font.render(f'Forme', True, (0, 0, 0))
        pygame.draw.rect(fenetre, (255, 255, 255), (0, 340, 250, 30))

    texte_fleche_gauche = font.render(f'←', True, (255, 255, 255))
    pygame.draw.rect(fenetre, (0, 0, 0), (70, 405, 20, 10))
    texte_fleche_droite = font.render(f'→', True, (255, 255, 255))
    pygame.draw.rect(fenetre, (0, 0, 0), (140, 405, 20, 10))
    texte_fleche_haut = font.render(f'↑', True, (255, 255, 255))
    pygame.draw.rect(fenetre, (0, 0, 0), (110, 370, 10, 30))
    texte_fleche_bas = font.render(f'↓', True, (255, 255, 255))
    pygame.draw.rect(fenetre, (0, 0, 0), (110, 420, 10, 30))


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
    fenetre.blit(texte_forme, (90, 340))
    fenetre.blit(texte_fleche_gauche, (70, 395))
    fenetre.blit(texte_fleche_droite, (140, 395))
    fenetre.blit(texte_fleche_haut, (110, 370))
    fenetre.blit(texte_fleche_bas, (110, 420))



# Fonction pour afficher les differentes formes dans l'interface:

def afficher_formes(fenetre, font, formes, couleur_vivant, couleur_mort, taille_case, taille_statistiques):
    n_formes = len(formes)
    for i, forme in enumerate(formes):
        n_lignes, n_colonnes = forme.shape
        for y in range(n_lignes):
            for x in range(n_colonnes):
                rect = pygame.Rect(x * taille_case + taille_statistiques + 250 * i, y * taille_case, taille_case, taille_case)
                if forme[y, x] == 1:
                    pygame.draw.rect(fenetre, couleur_vivant, rect)
                    
                pygame.draw.rect(fenetre, (128, 128, 128), rect, 1)  # Dessiner les lignes de grille grises
        texte = font.render(f'Forme {i + 1}', True, (0, 0, 0))
        fenetre.blit(texte, (250 * i + 10, n_lignes * taille_case + 10))

