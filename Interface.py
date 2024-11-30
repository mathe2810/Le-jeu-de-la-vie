import numpy as np
import pygame
import math

class Interface:
    def __init__(self,fenetre,font):
        self.fenetre = fenetre
        self.font = font

    def afficher_statistiques(self, grille, Fenetre_util, Moteur_util):
        # Affichage des statistiques
        pygame.draw.rect(self.fenetre, (250, 250, 250), (0, 0, 250, Fenetre_util.taille_fenetre[1]))
        n_vivants = np.sum(grille.grille)
        pos_souris = pygame.mouse.get_pos()
        texte_vivants = self.font.render(f'Cellules vivantes: {n_vivants}', True, (0, 0, 0))
        texte_souris = self.font.render(f'Position souris: {pos_souris}', True, (0, 0, 0))
        if Moteur_util.Bool_pause == False:
            texte_pause = self.font.render(f'Pause', True, (255, 255, 255))
            pygame.draw.rect(self.fenetre, (0, 0, 0), (0, 70, 250, 30))
        else:
            texte_pause = self.font.render(f'Pause', True, (0, 0, 0))
            pygame.draw.rect(self.fenetre, (255, 255, 255), (0, 70, 250, 30))

        texte_delai_evolutions = self.font.render(f'évolutions: {Moteur_util.evolution_delay} ms', True, (0, 0, 0))
        texte_plus = self.font.render(f'+', True, (0, 0, 0))
        texte_moins = self.font.render(f'-', True, (0, 0, 0))

        texte_fps = self.font.render(f'FPS: {math.ceil(Moteur_util.clock.get_fps())}', True, (0, 0, 0))

        if Moteur_util.Bool_grille == False:
            texte_grille = self.font.render(f'Grille', True, (255, 255, 255))
            pygame.draw.rect(self.fenetre, (0, 0, 0), (0, 160, 250, 30))
        else:
            texte_grille = self.font.render(f'Grille', True, (0, 0, 0))
            pygame.draw.rect(self.fenetre, (255, 255, 255), (0, 160, 250, 30))

        texte_zoom = self.font.render(f'Zoom', True, (0, 0, 0))
        texte_plus = self.font.render(f'+', True, (0, 0, 0))
        texte_moins = self.font.render(f'-', True, (0, 0, 0))
        texte_taille_grille = self.font.render(f'Taille grille: {grille.grille.shape}', True, (0, 0, 0))
        texte_taille_case = self.font.render(f'Taille case: {Fenetre_util.taille_case}', True, (0, 0, 0))
        texte_taille_finale_case = self.font.render(f'Taille finale case: {Fenetre_util.taille_case_final}', True, (0, 0, 0))

        if Moteur_util.Bool_reinit == False:
            texte_reinitialiser = self.font.render(f'Reinitialiser', True, (255, 255, 255))
            pygame.draw.rect(self.fenetre, (0, 0, 0), (0, 310, 250, 30))
        else:
            texte_reinitialiser = self.font.render(f'Reinitialiser', True, (0, 0, 0))
            pygame.draw.rect(self.fenetre, (255, 255, 255), (0, 310, 250, 30))

        if Moteur_util.Bool_form == False:
            texte_forme = self.font.render(f'Forme', True, (255, 255, 255))
            pygame.draw.rect(self.fenetre, (0, 0, 0), (0, 340, 250, 30))
        else:
            texte_forme = self.font.render(f'Forme', True, (0, 0, 0))
            pygame.draw.rect(self.fenetre, (255, 255, 255), (0, 340, 250, 30))

        if Moteur_util.Bool_sauvegarde == False:
            texte_sauvegarde = self.font.render(f'Sauvegarde', True, (255, 255, 255))
            pygame.draw.rect(self.fenetre, (0, 0, 0), (0, 480, 250, 30))
        else:
            texte_sauvegarde = self.font.render(f'Sauvegarde', True, (0, 0, 0))
            pygame.draw.rect(self.fenetre, (255, 255, 255), (0, 480, 250, 30))

        texte_fleche_gauche = self.font.render(f'←', True, (255, 255, 255))
        pygame.draw.rect(self.fenetre, (0, 0, 0), (70, 405, 20, 10))
        texte_fleche_droite = self.font.render(f'→', True, (255, 255, 255))
        pygame.draw.rect(self.fenetre, (0, 0, 0), (140, 405, 20, 10))
        texte_fleche_haut = self.font.render(f'↑', True, (255, 255, 255))
        pygame.draw.rect(self.fenetre, (0, 0, 0), (110, 370, 10, 30))
        texte_fleche_bas = self.font.render(f'↓', True, (255, 255, 255))
        pygame.draw.rect(self.fenetre, (0, 0, 0), (110, 420, 10, 30))

        texte_deplacement_vitesse = self.font.render(f'Vitesse de déplacement: {Moteur_util.vitesse_deplacement}', True, (0, 0, 0))
        texte_plus_deplacement = self.font.render(f'+', True, (0, 0, 0))
        texte_moins_deplacement = self.font.render(f'-', True, (0, 0, 0))

        if Moteur_util.Bool_reinit_ale == False:
            texte_reinit_aleatoire = self.font.render(f'Réinitialiser aléatoirement', True, (255, 255, 255))
            pygame.draw.rect(self.fenetre, (0, 0, 0), (0, 510, 250, 30))
        else:
            texte_reinit_aleatoire = self.font.render(f'Réinitialiser aléatoirement', True, (0,0,0))
            pygame.draw.rect(self.fenetre, (255, 255, 255), (0, 510, 250, 30))

        texte_changement_regle = self.font.render(f'Changer les règles :', True, (0, 0, 0))
        texte_naissance = self.font.render(f'Naissance : {grille.nb1_naissance} | {grille.nb2_naissance}', True, (0, 0, 0))
        texte_naissance_plus = self.font.render(f'+', True, (0, 0, 0))
        texte_naissance_moins = self.font.render(f'-', True, (0, 0, 0))
        texte_survie = self.font.render(f'Survie : {grille.nb_survie}', True, (0, 0, 0))
        texte_survie_plus = self.font.render(f'+', True, (0, 0, 0))
        texte_survie_moins = self.font.render(f'-', True, (0, 0, 0))

        self.fenetre.blit(texte_vivants, (10, 10))
        self.fenetre.blit(texte_souris, (10, 40))
        self.fenetre.blit(texte_pause, (90, 70))
        self.fenetre.blit(texte_delai_evolutions, (10, 100))
        self.fenetre.blit(texte_plus, (200, 100))
        self.fenetre.blit(texte_moins, (220, 100))
        self.fenetre.blit(texte_fps, (10, 130))
        self.fenetre.blit(texte_grille, (90, 160))
        self.fenetre.blit(texte_zoom, (10, 190))
        self.fenetre.blit(texte_plus, (200, 190))
        self.fenetre.blit(texte_moins, (220, 190))
        self.fenetre.blit(texte_taille_grille, (10, 220))
        self.fenetre.blit(texte_taille_case, (10, 250))
        self.fenetre.blit(texte_taille_finale_case, (10, 280))
        self.fenetre.blit(texte_reinitialiser, (60, 310))
        self.fenetre.blit(texte_forme, (90, 340))
        self.fenetre.blit(texte_fleche_gauche, (70, 395))
        self.fenetre.blit(texte_fleche_droite, (140, 395))
        self.fenetre.blit(texte_fleche_haut, (110, 370))
        self.fenetre.blit(texte_fleche_bas, (110, 420))
        self.fenetre.blit(texte_deplacement_vitesse, (10, 450))
        # self.fenetre.blit(texte_plus_deplacement, (220, 450))
        # self.fenetre.blit(texte_moins_deplacement, (240, 450))
        self.fenetre.blit(texte_sauvegarde, (60, 480))
        self.fenetre.blit(texte_reinit_aleatoire, (10, 510))
        self.fenetre.blit(texte_changement_regle, (10, 540))
        self.fenetre.blit(texte_naissance, (10, 570))
        self.fenetre.blit(texte_naissance_plus, (200, 570))
        self.fenetre.blit(texte_naissance_moins, (220, 570))
        self.fenetre.blit(texte_survie, (10, 600))
        self.fenetre.blit(texte_survie_plus, (200, 600))
        self.fenetre.blit(texte_survie_moins, (220, 600))


    def dessiner_grille(self, grille, Fenetre_util, Moteur_util):
        n_lignes, n_colonnes = grille.grille.shape

        # Créer une grille de rectangles
        x_coords, y_coords = np.meshgrid(np.arange(n_colonnes), np.arange(n_lignes))
        x_coords = (x_coords - Moteur_util.scroll_x) * Fenetre_util.taille_case + Fenetre_util.taille_statistiques
        y_coords = (y_coords - Moteur_util.scroll_y) * Fenetre_util.taille_case

        int_x_coords = x_coords
        int_y_coords = y_coords

        #Filtrer les cellules en dehors de l'écran
        mask = (int_x_coords >= Fenetre_util.taille_statistiques) & (int_x_coords < self.fenetre.get_width())
        mask &= (int_y_coords >= 0) & (int_y_coords < self.fenetre.get_height())
        int_x_coords = int_x_coords[mask]
        int_y_coords = int_y_coords[mask]

        caclCoordHG =  ((int_x_coords[0]-Fenetre_util.taille_statistiques)//Fenetre_util.taille_case)+Moteur_util.scroll_x, (int_y_coords[0]//Fenetre_util.taille_case)+Moteur_util.scroll_y
        caclCoordBD =  ((int_x_coords[-1]-Fenetre_util.taille_statistiques)//Fenetre_util.taille_case)+Moteur_util.scroll_x, (int_y_coords[-1]//Fenetre_util.taille_case)+Moteur_util.scroll_y

        
        #Premier point de la grille
        Moteur_util.coordHG = caclCoordHG


        #Derneir point de la grille
        Moteur_util.coordBD = caclCoordBD
        

        # Filtrer les cellules vivantes
        vivant_mask = grille.grille == 1
        vivant_x_coords = x_coords[vivant_mask]
        vivant_y_coords = y_coords[vivant_mask]

        mask1 = (vivant_x_coords >= Fenetre_util.taille_statistiques) & (vivant_x_coords < self.fenetre.get_width())
        mask1 &= (vivant_y_coords >= 0) & (vivant_y_coords < self.fenetre.get_height())
        dessin_x_coords = vivant_x_coords[mask1]
        dessin_y_coords = vivant_y_coords[mask1]

    
        

        # Dessiner les cellules mortes en arrière-plan
        rect = pygame.Rect(Fenetre_util.taille_statistiques, 0, self.fenetre.get_width(), self.fenetre.get_height())
        pygame.draw.rect(self.fenetre, Fenetre_util.couleur_mort, rect)

        # Créer une surface temporaire pour les cellules vivantes
        temp_surface = pygame.Surface((self.fenetre.get_width(), self.fenetre.get_height()), pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0))  # Remplir avec une transparence totale

        # Dessiner les cellules vivantes sur la surface temporaire
        for x, y in zip(dessin_x_coords, dessin_y_coords):
            rect = pygame.Rect(x, y, Fenetre_util.taille_case, Fenetre_util.taille_case)
            pygame.draw.rect(temp_surface, Fenetre_util.couleur_vivant, rect)

        # Blit la surface temporaire sur la fenêtre principale
        self.fenetre.blit(temp_surface, (0, 0))

        # Dessiner les lignes de grille si nécessaire
        if Moteur_util.Bool_grille:
            # Dessiner les lignes horizontales
            for y in range(n_lignes + 1):
                start_pos = (Fenetre_util.taille_statistiques, y * Fenetre_util.taille_case)
                end_pos = (Fenetre_util.taille_statistiques + n_colonnes * Fenetre_util.taille_case, y * Fenetre_util.taille_case)
                pygame.draw.line(self.fenetre, (128, 128, 128), start_pos, end_pos)

            # Dessiner les lignes verticales
            for x in range(n_colonnes + 1):
                start_pos = (Fenetre_util.taille_statistiques + x * Fenetre_util.taille_case, 0)
                end_pos = (Fenetre_util.taille_statistiques + x * Fenetre_util.taille_case, n_lignes * Fenetre_util.taille_case)
                pygame.draw.line(self.fenetre, (128, 128, 128), start_pos, end_pos)