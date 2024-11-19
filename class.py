import numpy as np
import pygame
import math

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

    # Fonction qui verifie les bonnes proportions de la grille:
    def verifier_proportions_grille(self,Fenetre_util):
        if self.n_colonnes * self.taille_case + Fenetre_util.taille_statistiques > 1920:
            self.taille_case = 1920 // self.n_colonnes
        if self.n_lignes * self.taille_case > 1080:
            self.taille_case = 1080 // self.n_lignes
        if self.n_colonnes * self.taille_case + Fenetre_util.taille_statistiques < 250:
            self.taille_case = 250 // self.n_colonnes
        if self.n_lignes * self.taille_case < 450:
            self.taille_case = 450 // self.n_lignes

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
        texte_taille_case = self.font.render(f'Taille case: {grille.taille_case}', True, (0, 0, 0))
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

        texte_fleche_gauche = self.font.render(f'←', True, (255, 255, 255))
        pygame.draw.rect(self.fenetre, (0, 0, 0), (70, 405, 20, 10))
        texte_fleche_droite = self.font.render(f'→', True, (255, 255, 255))
        pygame.draw.rect(self.fenetre, (0, 0, 0), (140, 405, 20, 10))
        texte_fleche_haut = self.font.render(f'↑', True, (255, 255, 255))
        pygame.draw.rect(self.fenetre, (0, 0, 0), (110, 370, 10, 30))
        texte_fleche_bas = self.font.render(f'↓', True, (255, 255, 255))
        pygame.draw.rect(self.fenetre, (0, 0, 0), (110, 420, 10, 30))


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

    def dessiner_grille(self,grille,Fenetre_util,Moteur_util):
        # Créer une grille de rectangles
        x_coords, y_coords = np.meshgrid(np.arange(grille.n_colonnes), np.arange(grille.n_lignes))
        x_coords = (x_coords - Moteur_util.scroll_x) * grille.taille_case + Fenetre_util.taille_statistiques
        y_coords = (y_coords - Moteur_util.scroll_y) * grille.taille_case

        # Aplatir les coordonnées pour itérer facilement
        x_coords = x_coords.flatten()
        y_coords = y_coords.flatten()
        grille_flat = grille.grille.flatten()

        # Créer un tableau de rectangles
        rects = [pygame.Rect(x, y, grille.taille_case, grille.taille_case) for x, y in zip(x_coords, y_coords)]

        # Dessiner les cellules vivantes et mortes
        for rect, cell in zip(rects, grille_flat):
            color = Fenetre_util.couleur_vivant if cell else Fenetre_util.couleur_mort
            pygame.draw.rect(self.fenetre, color, rect)

        # Dessiner les lignes de grille si nécessaire
        if Moteur_util.Bool_grille:
            for rect in rects:
                pygame.draw.rect(self.fenetre, (128, 128, 128), rect, 1)  # Dessiner les lignes de grille grises
    

    