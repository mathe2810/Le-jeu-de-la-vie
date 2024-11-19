import pygame
import numpy as np
import time
from Interface import *
from Moteur import *
from Sauvegarde import *
from Analyse import *
from Class import *

supprimer_statistiques()

# Menu()

# Création de la grilles
grille = creer_grille(250, 250)

# Initialisation de la fenêtre
pygame.init()
taille_statistiques = 250
taille_case = 3
couleur_vivant = (255, 255, 255)
couleur_mort = (0, 0, 0)
n_lignes, n_colonnes = grille.shape
taille_case = verifier_proportions_grille(grille, taille_case, taille_statistiques)

taille_case_final = taille_case

taille_fenetre = (n_colonnes * taille_case + taille_statistiques, n_lignes * taille_case)
fenetre = pygame.display.set_mode(taille_fenetre)

# Initialisation de la police de caractères
pygame.font.init()
font = pygame.font.SysFont('Arial', 20)

# Variables de contrôle
Bool_pause = False
Bool_grille = False
Bool_reinit = False
Bool_forme = False

last_click_time = 0
iteration = 0

scroll_x = 0
scroll_y = 0

# Initialisation de l'horloge
clock = pygame.time.Clock()
fps = 160  # Définir le nombre d'images par seconde

# Variables pour contrôler le délai entre les évolutions
evolution_delay = 20  # Délai en millisecondes
last_evolution_time = pygame.time.get_ticks()

# Boucle principale du jeu
running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if Bool_reinit:
        grille = creer_grille_vide(200, 200)
        Bool_reinit = False

    if not Bool_pause:
        # Évolution de la grille à intervalles réguliers
        if current_time - last_evolution_time >= evolution_delay:
            grille = evoluer(grille)
            last_evolution_time = current_time

        stocker_statistiques_csv(np.sum(grille), grille.size - np.sum(grille), iteration)
        sauvegarder_grille_npz(grille, 'grille.npz')
        iteration += 1

    # Gestion de la souris
    grille, Bool_pause, Bool_grille, Bool_reinit, last_click_time, evolution_delay, taille_case, taille_case_final, fenetre, scroll_x, scroll_y = gerer_souris(
        grille, taille_case, Bool_pause, Bool_grille, Bool_reinit , last_click_time, evolution_delay, taille_case_final, fenetre, taille_statistiques, scroll_x, scroll_y)  

    # Dessin de la grille
    dessiner_grille(grille, fenetre, taille_case, couleur_vivant, couleur_mort, Bool_grille,taille_statistiques,scroll_x,scroll_y)
    # Affichage des statistiques
    pygame.draw.rect(fenetre, (250, 250, 250), (0, 0, 250, taille_fenetre[1]))
    afficher_statistiques(fenetre, font, grille, Bool_pause, Bool_grille, Bool_reinit,Bool_forme, taille_case, taille_case_final, evolution_delay, clock)
    pygame.display.flip()

    # Contrôler le taux de rafraîchissement
    clock.tick(fps)

    

pygame.quit()
# statistiques = charger_statistiques_csv()
# afficher_courbe_statistiques(statistiques)
# grille_finale = charger_grille_npz('grille.npz')
# print(f'Nombre de changements: {analyser_evolution(grille, grille_finale)}')