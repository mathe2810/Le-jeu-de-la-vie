import numpy as np
import pygame
import math

class Moteur:
    def __init__(self, Bool_pause, Bool_grille, Bool_reinit,Bool_form,Bool_sauvegarde,Bool_form_placement, Bool_reinit_ale, last_click_time, iteration, scroll_x, scroll_y,coordHG,coordBD, clock, fps, evolution_delay, last_evolution_time, vitesse_deplacement, input_text, pos_souris_grille):
        self.Bool_pause = Bool_pause
        self.Bool_grille = Bool_grille
        self.Bool_reinit = Bool_reinit
        self.Bool_form = Bool_form
        self.last_click_time = last_click_time
        self.iteration = iteration
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        self.coordHG = coordHG
        self.coordBD = coordBD
        self.clock = clock
        self.fps = fps
        self.evolution_delay = evolution_delay
        self.last_evolution_time = last_evolution_time
        self.coordHG = coordHG
        self.vitesse_deplacement = vitesse_deplacement
        self.Bool_sauvegarde = Bool_sauvegarde
        self.input_text = input_text
        self.pos_souris_grille = pos_souris_grille
        self.Bool_form_placement = Bool_form_placement
        self.Bool_reinit_ale = Bool_reinit_ale

    def gerer_souris(self,grille,Fenetre_util,Interface_util,Forme_util, click_delay=200):
        current_time = pygame.time.get_ticks()
        

        if current_time - self.last_click_time < click_delay:
            return 0


        x, y = pygame.mouse.get_pos()

        if self.Bool_form_placement:
            if x < 250 and pygame.mouse.get_pressed()[0]:
                print('impossible de placer une forme dans le menu')
                return 0
            x -= Fenetre_util.taille_statistiques
            x = x // Fenetre_util.taille_case
            y = y // Fenetre_util.taille_case
            x += self.scroll_x
            y += self.scroll_y
            self.pos_souris_grille = (x,y)
            Forme_util.positions = {
                    self.input_text: (self.pos_souris_grille[0], self.pos_souris_grille[1])
                }
            
             # Afficher la prévisualisation de la forme en gris
            if self.input_text in Forme_util.formes:
                forme = Forme_util.formes[self.input_text]
                for i in range(forme.shape[0]):
                    for j in range(forme.shape[1]):
                        if forme[i, j] == 1:
                            rect = pygame.Rect(
                                (x + j - self.scroll_x) * Fenetre_util.taille_case + Fenetre_util.taille_statistiques,
                                (y + i - self.scroll_y) * Fenetre_util.taille_case,
                                Fenetre_util.taille_case,
                                Fenetre_util.taille_case
                            )
                            pygame.draw.rect(Interface_util.fenetre, (128, 128, 128), rect)


            if pygame.mouse.get_pressed()[0]:
                Forme_util.afficher_formes()
                pygame.time.wait(200)
                self.input_text = ""
                self.Bool_form_placement = False
        else:
            if pygame.mouse.get_pressed()[0]:
                if x < 250:
                    #Gestion de la Pause
                    if x < 250 and y < 100 and x > 0 and y > 70:
                        self.Bool_pause = not self.Bool_pause

                    #Gestion de l'évolution
                    elif x > 200 and y > 100 and x < 220 and y < 130:
                        self.evolution_delay += 10
                    elif x > 220 and y > 100 and x < 240 and y < 130:
                        self.evolution_delay -= 10
                    
                    #Gestion de la grille
                    elif x > 0 and y > 160 and x < 250 and y < 190:
                        self.Bool_grille = not self.Bool_grille

                    #Gestion du zoom
                    elif x > 200 and y > 190 and x < 220 and y < 220:
                        Fenetre_util.taille_case += 1
                    elif x > 220 and y > 190 and x < 240 and y < 220:
                        if Fenetre_util.taille_case == Fenetre_util.taille_case_final:
                            Fenetre_util.taille_case_final -= 1
                            Fenetre_util.taille_case -=1
                            if Fenetre_util.taille_case_final == 0:
                                Fenetre_util.taille_case_final = 1
                                Fenetre_util.taille_case = 1
                            grille.agrandir_grille(Fenetre_util, Interface_util)
                            
                        else:
                            Fenetre_util.taille_case -= 1


                    elif x > 0 and y > 340 and x < 250 and y < 370:
                            self.Bool_form = not self.Bool_form

                    # Gestion du scroll
                    elif x > 70 and y > 405 and x < 90 and y < 415:
                        self.scroll_x = self.scroll_x - self.vitesse_deplacement
                    elif x > 140 and y > 405 and x < 160 and y < 415:
                        self.scroll_x = self.scroll_x + self.vitesse_deplacement
                    elif x > 110 and y > 370 and x < 120 and y < 400:
                        self.scroll_y -= self.vitesse_deplacement
                    elif x > 110 and y > 420 and x < 120 and y < 450:
                        self.scroll_y += self.vitesse_deplacement


                    # Gestion de la réinitialisation
                    elif x > 0 and y > 310 and x < 200 and y < 330:
                        self.Bool_reinit = not self.Bool_reinit

                    # Gestion de la sauvegarde
                    elif x > 0 and y > 480 and x < 250 and y < 510:
                        self.Bool_sauvegarde = not self.Bool_sauvegarde

                    elif x > 0 and y > 510 and x < 250 and y < 540:
                        self.Bool_reinit_ale = not self.Bool_reinit_ale

                    elif x > 200 and y > 570 and x < 220 and y < 590:
                        grille.nb1_naissance += 1
                        grille.nb2_naissance += 1
                    
                    elif x > 220 and y > 570 and x < 240 and y < 590:
                        grille.nb1_naissance -= 1
                        grille.nb2_naissance -= 1
                    
                    elif x > 200 and y > 600 and x < 220 and y < 620:
                        grille.nb_survie += 1
                    elif x > 220 and y > 600 and x < 240 and y < 620:
                        grille.nb_survie -= 1
                    

                # Gestion du clic sur la grille
                else:
                    if self.Bool_form_placement:
                        Forme_util.positions = {
                                self.input_text: (self.pos_souris_grille[0], self.pos_souris_grille[1])
                            }
                    else:
                        x -= Fenetre_util.taille_statistiques
                        x = x // Fenetre_util.taille_case
                        y = y // Fenetre_util.taille_case
                        x += self.scroll_x
                        y += self.scroll_y
                        self.pos_souris_grille = (x,y)
                        grille.grille[y, x] = 1 - grille.grille[y, x]
                self.last_click_time = current_time
            
            if self.coordHG[0] + self.scroll_x < 0:
                self.scroll_x += self.vitesse_deplacement
            elif self.coordHG[1] + self.scroll_y < 0:
                self.scroll_y += self.vitesse_deplacement
            elif self.coordBD[0] + self.scroll_x > grille.n_colonnes-1:
                self.scroll_x -= self.vitesse_deplacement
            elif self.coordBD[1] + self.scroll_y > grille.n_lignes-1:
                self.scroll_y -= self.vitesse_deplacement