import numpy as np
import pygame

class Grille:
    def __init__(self, n_lignes, n_colonnes, taille_case):
        self.n_lignes = n_lignes
        self.n_colonnes = n_colonnes
        self.taille_case = taille_case
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

    # Fonction qui permet de faire évoluer la grille d'un pas de temps v2
    def evoluer(self):
        nouvelle_grille = np.copy(self.grille)

        # Comptage des voisins vivants en utilisant des décalages
        voisins = np.zeros((self.n_lignes, self.n_colonnes), dtype=int)
        voisins += np.roll(self.grille, 1, axis=0)  # Haut
        voisins += np.roll(self.grille, -1, axis=0)  # Bas
        voisins += np.roll(self.grille, 1, axis=1)  # Gauche
        voisins += np.roll(self.grille, -1, axis=1)  # Droite
        voisins += np.roll(np.roll(self.grille, 1, axis=0), 1, axis=1)  # Haut-Gauche
        voisins += np.roll(np.roll(self.grille, 1, axis=0), -1, axis=1)  # Haut-Droite
        voisins += np.roll(np.roll(self.grille, -1, axis=0), 1, axis=1)  # Bas-Gauche
        voisins += np.roll(np.roll(self.grille, -1, axis=0), -1, axis=1)  # Bas-Droite

        # Application des règles du jeu de la vie
        nouvelle_grille[(self.grille == 1) & ((voisins < 2) | (voisins > 3))] = 0
        nouvelle_grille[(self.grille == 0) & (voisins == 3)] = 1

        self.grille = nouvelle_grille

    def calculer_nombre_colonnes_lignes(self, Fenetre_util, Interface_util):
        largeur_fenetre, hauteur_fenetre = Fenetre_util.taille_fenetre
        nombre_colonnes = (largeur_fenetre - Fenetre_util.taille_statistiques) // self.taille_case
        nombre_lignes = hauteur_fenetre // self.taille_case
        return nombre_colonnes, nombre_lignes

    def agrandir_grille(self, Fenetre_util, Interface_util):
        self.n_colonnes, self.n_lignes = self.calculer_nombre_colonnes_lignes(Fenetre_util, Interface_util)
        nouvelle_grille = np.zeros((self.n_lignes, self.n_colonnes), dtype=int)
        
        # Calculer les dimensions minimales pour éviter les erreurs de diffusion
        min_lignes = min(self.n_lignes, self.grille.shape[0])
        min_colonnes = min(self.n_colonnes, self.grille.shape[1])
        
        # Copier les valeurs de l'ancienne grille dans la nouvelle grille
        nouvelle_grille[:min_lignes, :min_colonnes] = self.grille[:min_lignes, :min_colonnes]
        
        self.grille = nouvelle_grille

class Fenetre:
    def __init__(self, taille_statistiques, taille_case_final, grille, couleur_vivant, couleur_mort):
        self.taille_statistiques = taille_statistiques
        self.taille_case_final = taille_case_final
        self.taille_fenetre = (grille.n_colonnes * grille.taille_case + taille_statistiques, grille.n_lignes * grille.taille_case)
        self.couleur_vivant = couleur_vivant
        self.couleur_mort = couleur_mort

class Moteur:
    def __init__(self, Bool_pause, Bool_grille, Bool_reinit,Bool_form, last_click_time, iteration, scroll_x, scroll_y, clock, fps, evolution_delay, last_evolution_time):
        self.Bool_pause = Bool_pause
        self.Bool_grille = Bool_grille
        self.Bool_reinit = Bool_reinit
        self.Bool_form = Bool_form
        self.last_click_time = last_click_time
        self.iteration = iteration
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        self.clock = clock
        self.fps = fps
        self.evolution_delay = evolution_delay
        self.last_evolution_time = last_evolution_time

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
                    grille.taille_case += 1
                elif x > 220 and y > 190 and x < 240 and y < 220:
                    if grille.taille_case == Fenetre_util.taille_case_final:
                        Fenetre_util.taille_case_final -= 1
                        if Fenetre_util.taille_case_final == 0:
                            Fenetre_util.taille_case_final = 1
                        grille.grille = grille.agrandir_grille(Fenetre_util, Interface_util)
                        
                    else:
                        grille.taille_case -= 1

                # Gestion du scroll
                elif x > 70 and y > 405 and x < 90 and y < 415:
                    self.scroll_x += 1
                elif x > 140 and y > 405 and x < 160 and y < 415:
                    self.scroll_x -= 1
                elif x > 110 and y > 370 and x < 120 and y < 400:
                    self.scroll_y += 1
                elif x > 110 and y > 420 and x < 120 and y < 450:
                    self.scroll_y -= 1

                # Gestion de la réinitialisation
                elif x > 0 and y > 310 and x < 200 and y < 330:
                    self.Bool_reinit = not self.Bool_reinit

            # Gestion du clic sur la grille
            else:
                x -= Fenetre_util.taille_statistiques
                x = x // grille.taille_case
                y = y // grille.taille_case
                x += self.scroll_x
                y += self.scroll_y
                grille.grille[y, x] = 1 - grille.grille[y, x]
            self.last_click_time = current_time

        

class Interface:
    def __init__(self,fenetre,font):
        self.fenetre = fenetre
        self.font = font
    

    

    