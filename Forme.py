import pygame
import numpy as np

class Forme():
    def __init__(self, grille, Fenetre_util, Moteur_util, Interface_util,formes,positions):
        self.grille = grille
        self.Fenetre_util = Fenetre_util
        self.Moteur_util = Moteur_util
        self.Interface_util = Interface_util
        self.formes = formes
        self.positions = positions  

    def sauvegarder_formes(self, filename):
        formes = {
            'carre': np.array([[1, 1], [1, 1]]),
            'planeur': np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]]),
            'clignotant': np.array([[1, 1, 1]])
        }
        np.savez_compressed(filename, **formes)

    def charger_formes(self, filename):
        data = np.load(filename)
        return data

    def ajouter_forme(self, forme, x, y):
        if y + forme.shape[0] <= self.grille.grille.shape[0] and x + forme.shape[1] <= self.grille.grille.shape[1]:
            self.grille.grille[y:y+forme.shape[0], x:x+forme.shape[1]] = forme
        else:
            print(f"Erreur : La forme {forme} dépasse les limites de la grille.")


    def afficher_formes(self):
        print(self.positions)
        for forme_name, position in self.positions.items():
            if forme_name in self.formes:
                self.ajouter_forme(self.formes[forme_name], position[0], position[1])

    def menu_forme(self):
        rectangle = pygame.Rect(0, 0, self.Interface_util.fenetre.get_width(), self.Interface_util.fenetre.get_height())
        pygame.draw.rect(self.Interface_util.fenetre, (0, 0, 0), rectangle)
        texte = self.Interface_util.font.render('Veuillez choisir le nom de la forme :', True, (255, 255, 255))
        self.Interface_util.fenetre.blit(texte, (10, 10))
        texte_saisi = self.Interface_util.font.render(self.Moteur_util.input_text, True, (255, 255, 255))
        self.Interface_util.fenetre.blit(texte_saisi, (10, 50))

        # Afficher les formes disponibles
        y_offset = 100
        for forme_name, forme in self.formes.items():
            texte_forme = self.Interface_util.font.render(forme_name, True, (255, 255, 255))
            self.Interface_util.fenetre.blit(texte_forme, (10, y_offset))

            # Dessiner la forme à côté du nom
            forme_surface = pygame.Surface((50, 50))
            forme_surface.fill((0, 0, 0))  # Fond noir pour la forme
            for i in range(forme.shape[0]):
                for j in range(forme.shape[1]):
                    if forme[i, j] == 1:
                        rect = pygame.Rect(j * 10, i * 10, 10, 10)
                        pygame.draw.rect(forme_surface, (255, 255, 255), rect)
            self.Interface_util.fenetre.blit(forme_surface, (200, y_offset - 10))

            y_offset += 60
             
        pygame.display.flip()