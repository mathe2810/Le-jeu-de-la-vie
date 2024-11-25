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
grille = Grille(250, 250)
grille.creer_grille()

# Initialisation de pygame
pygame.init()
pygame.font.init()

# Initialisation de la fenêtre
Fenetre_util = Fenetre(250, 3,3, grille,(255, 255, 255),(0, 0, 0))

#Initialisation de l'interface graphique
Interface_util = Interface(pygame.display.set_mode(Fenetre_util.taille_fenetre), pygame.font.SysFont('Arial', 20))

#Initialisation du moteur
Moteur_util = Moteur(False, False, False,False, 0, 0, 0, 0, pygame.time.Clock(), 160, 20, pygame.time.get_ticks())


# Boucle principale du jeu
running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if Moteur_util.Bool_reinit:
        grille.creer_grille_vide()
        Moteur_util.Bool_reinit = False

    if not Moteur_util.Bool_pause:
        # Évolution de la grille à intervalles réguliers
        if current_time - Moteur_util.last_evolution_time >= Moteur_util.evolution_delay:
            grille.evoluer()
            Moteur_util.last_evolution_time = current_time

        stocker_statistiques_csv(np.sum(grille.grille), grille.grille.size - np.sum(grille.grille), Moteur_util.iteration)
        sauvegarder_grille_npz(grille.grille, 'grille.npz')
        Moteur_util.iteration += 1

    # Gestion de la souris
    Moteur_util.gerer_souris(grille, Fenetre_util, Interface_util) 

    # Dessin de la grille
    Interface_util.dessiner_grille(grille, Fenetre_util, Moteur_util)
    
    Interface_util.afficher_statistiques(grille,Fenetre_util, Moteur_util)
    pygame.display.flip()

    # Contrôler le taux de rafraîchissement
    Moteur_util.clock.tick(Moteur_util.fps)

    

pygame.quit()
# statistiques = charger_statistiques_csv()
# afficher_courbe_statistiques(statistiques)
# grille_finale = charger_grille_npz('grille.npz')
# print(f'Nombre de changements: {analyser_evolution(grille, grille_finale)}')