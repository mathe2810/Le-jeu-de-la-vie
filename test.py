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
grille = Grille(250, 250, 3)
grille.creer_grille()

# Initialisation de pygame
pygame.init()
pygame.font.init()

# Initialisation de la fenêtre
Fenetre_util = Fenetre(250, 3, grille,(255, 255, 255),(0, 0, 0))
grille.taille_case = verifier_proportions_grille(grille.grille, grille.taille_case, Fenetre_util.taille_statistiques)

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
    dessiner_grille(grille.grille, Interface_util.fenetre, grille.taille_case, Fenetre_util.couleur_vivant, Fenetre_util.couleur_mort, Moteur_util.Bool_grille,Fenetre_util.taille_statistiques, Moteur_util.scroll_x,Moteur_util.scroll_y)
    # Affichage des statistiques
    pygame.draw.rect(Interface_util.fenetre, (250, 250, 250), (0, 0, 250, Fenetre_util.taille_fenetre[1]))
    afficher_statistiques(Interface_util.fenetre, Interface_util.font, grille.grille, Moteur_util.Bool_pause, Moteur_util.Bool_grille, Moteur_util.Bool_reinit,Moteur_util.Bool_form, grille.taille_case, Fenetre_util.taille_case_final, Moteur_util.evolution_delay, Moteur_util.clock)
    pygame.display.flip()

    # Contrôler le taux de rafraîchissement
    Moteur_util.clock.tick(Moteur_util.fps)

    

pygame.quit()
# statistiques = charger_statistiques_csv()
# afficher_courbe_statistiques(statistiques)
# grille_finale = charger_grille_npz('grille.npz')
# print(f'Nombre de changements: {analyser_evolution(grille, grille_finale)}')