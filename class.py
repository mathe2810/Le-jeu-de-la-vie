import numpy as np
import pygame
import math
from scipy.signal import convolve2d

class Grille:
    def __init__(self, n_lignes, n_colonnes):
        self.n_lignes = n_lignes
        self.n_colonnes = n_colonnes
        self.grille = np.zeros((n_lignes, n_colonnes), dtype=int)

    # Fonction qui permet de créer une grille aléatoire de taille n_lignes x n_colonnes
    def creer_grille(self):
        self.grille = np.random.randint(0, 2, (self.n_lignes, self.n_colonnes))
    
    # Fonction qui permet de créer une grille vide de taille n_lignes x n_colonnes
    def creer_grille_vide(self):
        self.grille = np.zeros((self.n_lignes, self.n_colonnes), dtype=int)

    # Fonction qui permet de compter les voisins vivants dans une grille considérée comme un tore v1
    def compter_voisins_vivants_laisser_revenir(self, x, y):
        compteur = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                voisin_x = (x + i) % self.n_colonnes
                voisin_y = (y + j) % self.n_lignes
                compteur += self.grille[voisin_y, voisin_x]
        compteur -= self.grille[y, x]
        return compteur

    def evoluer(self):
        # Calculer la somme des voisins vivants directement avec des décalages
        voisins = (
            np.roll(self.grille, 1, axis=0) + np.roll(self.grille, -1, axis=0) +
            np.roll(self.grille, 1, axis=1) + np.roll(self.grille, -1, axis=1) +
            np.roll(np.roll(self.grille, 1, axis=0), 1, axis=1) +
            np.roll(np.roll(self.grille, 1, axis=0), -1, axis=1) +
            np.roll(np.roll(self.grille, -1, axis=0), 1, axis=1) +
            np.roll(np.roll(self.grille, -1, axis=0), -1, axis=1)
        )

        # Application des règles du jeu de la vie
        nouvelle_grille = (self.grille == 1) & ((voisins == 2) | (voisins == 3)) | (self.grille == 0) & (voisins == 3)

        # Mise à jour de la grille
        self.grille = nouvelle_grille.astype(int)




    def agrandir_grille(self, Fenetre_util, Interface_util):
        largeur_fenetre, hauteur_fenetre = Interface_util.fenetre.get_size()
        self.n_colonnes = (largeur_fenetre - Fenetre_util.taille_statistiques) // Fenetre_util.taille_case
        self.n_lignes  = hauteur_fenetre // Fenetre_util.taille_case
        
        nouvelle_grille = np.zeros((self.n_lignes, self.n_colonnes), dtype=int)
        
        # Calculer les dimensions minimales pour éviter les erreurs de diffusion
        min_lignes = min(self.n_lignes, self.grille.shape[0])
        min_colonnes = min(self.n_colonnes, self.grille.shape[1])
        
        # Copier les valeurs de l'ancienne grille dans la nouvelle grille
        nouvelle_grille[:min_lignes, :min_colonnes] = self.grille[:min_lignes, :min_colonnes]
        
        self.grille = nouvelle_grille

    # Fonction qui verifie les bonnes proportions de la grille:
    def verifier_proportions_grille(self,Fenetre_util):
        if self.n_colonnes * Fenetre_util.taille_case + Fenetre_util.taille_statistiques > 1800:
            Fenetre_util.taille_case = 1800 // self.n_colonnes
        if self.n_lignes * Fenetre_util.taille_case > 800:
            Fenetre_util.taille_case = 800 // self.n_lignes
        if self.n_colonnes * Fenetre_util.taille_case + Fenetre_util.taille_statistiques < 250:
            Fenetre_util.taille_case = 250 // self.n_colonnes
        if self.n_lignes * Fenetre_util.taille_case < 600:
            Fenetre_util.taille_case = 600 // self.n_lignes

        Fenetre_util.taille_case_final = Fenetre_util.taille_case
    
    def sauvegarder_grille_npz(self, nom_fichier):
        np.savez(nom_fichier, grille=self.grille)

    def charger_grille_npz(self, nom_fichier):
        with np.load(nom_fichier) as data:
            self.grille = data['grille']
            self.n_lignes, self.n_colonnes = self.grille.shape

class Fenetre:
    def __init__(self, taille_statistiques, taille_case, taille_case_final, grille, couleur_vivant, couleur_mort,):
        self.taille_statistiques = taille_statistiques
        self.taille_case = taille_case
        self.taille_case_final = taille_case_final
        grille.verifier_proportions_grille(self)
        self.taille_fenetre = (grille.n_colonnes * self.taille_case + taille_statistiques, grille.n_lignes * self.taille_case)
        self.couleur_vivant = couleur_vivant
        self.couleur_mort = couleur_mort


class Moteur:
    def __init__(self, Bool_pause, Bool_grille, Bool_reinit,Bool_form,Bool_sauvegarde, last_click_time, iteration, scroll_x, scroll_y,coordHG,coordBD, clock, fps, evolution_delay, last_evolution_time, vitesse_deplacement, input_text):
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

    def gerer_souris(self,grille,Fenetre_util,Interface_util, click_delay=200):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_click_time < click_delay:
            return 0

        x, y = pygame.mouse.get_pos()

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

                        0, 340, 250, 30

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

                # Gestion de la vitesse de déplacement
                elif x > 220 and y > 450 and x < 240 and y < 480:
                    self.vitesse_deplacement += 1
                elif x > 240 and y > 450 and x < 260 and y < 480:
                    self.vitesse_deplacement -= 1

                # Gestion de la sauvegarde
                elif x > 0 and y > 480 and x < 250 and y < 510:
                    self.Bool_sauvegarde = not self.Bool_sauvegarde
                

            # Gestion du clic sur la grille
            else:
                x -= Fenetre_util.taille_statistiques
                x = x // Fenetre_util.taille_case
                y = y // Fenetre_util.taille_case
                x += self.scroll_x
                y += self.scroll_y
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

        if self.vitesse_deplacement < 1:
            self.vitesse_deplacement = 1
        elif self.vitesse_deplacement > 5:
            self.vitesse_deplacement = 5

            
            

        

       


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
        self.fenetre.blit(texte_plus_deplacement, (220, 450))
        self.fenetre.blit(texte_moins_deplacement, (240, 450))
        self.fenetre.blit(texte_sauvegarde, (60, 480))

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
    

class Forme():
    def __init__(self, grille, Fenetre_util, Moteur_util, Interface_util):
        self.grille = grille
        self.Fenetre_util = Fenetre_util
        self.Moteur_util = Moteur_util
        self.Interface_util = Interface_util

    def carre(self, x, y, taille):
        self.grille.grille[y:y+taille, x:x+taille] = 1

    def planeur(self, x, y):
        planeur = np.array([[0, 1, 0],
                            [0, 0, 1],
                            [1, 1, 1]])
        self.grille.grille[y:y+3, x:x+3] = planeur

    def sauvegarder_formes(self, filename):
        formes = {
            'carre': np.array([[1, 1], [1, 1]]),
            'planeur': np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])
        }
        np.savez_compressed(filename, **formes)

    def charger_formes(self, filename):
        data = np.load(filename)
        return data

    def ajouter_forme(self, forme, x, y):
        self.grille.grille[y:y+forme.shape[0], x:x+forme.shape[1]] = forme

    def menu_forme(self):
        rectangle = pygame.Rect(0, 0, self.Interface_util.fenetre.get_width(), self.Interface_util.fenetre.get_height())
        pygame.draw.rect(self.Interface_util.fenetre, (0, 0, 0), rectangle)
        texte = self.Interface_util.font.render('Veuillez choisir le nom de la forme :', True, (255, 255, 255))
        self.Interface_util.fenetre.blit(texte, (10, 10))
        texte_saisi = self.Interface_util.font.render(self.Moteur_util.input_text, True, (255, 255, 255))
        self.Interface_util.fenetre.blit(texte_saisi, (10, 50))
        pygame.display.flip()