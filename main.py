import pygame
import numpy as np
from Grille import Grille
from Interface import Interface
from Moteur import Moteur
from Forme import Forme
from Fenetre import Fenetre
from Analyse import Analyse
from Menu import *
import os

Analyse_util = Analyse()

# Analyse.supprimer_statistiques()

# Menu()

# Création de la grilles
# grille = Grille(10, 10,3,2,3)
# grille.creer_grille()

grille = Grille(10, 10,3,2,3)
# grille.charger_grille_npz('./sauvegarde/grille/pluit_de_planeur.npz')

# Initialisation de pygame
pygame.init()
pygame.font.init()

# Initialisation de la fenêtre
Fenetre_util = Fenetre(250, 3,3, grille,(255, 255, 255),(0, 0, 0))

#Initialisation de l'interface graphique
Interface_util = Interface(pygame.display.set_mode(Fenetre_util.taille_fenetre), pygame.font.SysFont('Arial', 20))

#Initialisation du moteur
Moteur_util = Moteur(False, False, False,False,False,False,False, 0, 0, 0, 0, (0,0), (0,0), pygame.time.Clock(), 160, 20, pygame.time.get_ticks(),5,"",(0,0))

Forme_util = Forme(grille, Fenetre_util, Moteur_util, Interface_util,0,0)



nom_ouverture_fichier_form = "sauvegarde/form/"
nom_ouverture_fichier_grille = "sauvegarde/grille/"

Forme_util.sauvegarder_formes(nom_ouverture_fichier_form + 'form.npz')

Forme_util.formes = Forme_util.charger_formes(nom_ouverture_fichier_form + 'form.npz')

def lister_sauvegardes(dossier):
    fichiers = [f for f in os.listdir(dossier) if f.endswith('.npz')]
    return fichiers


def afficher_bouton_retour(fenetre, font):
    couleur_bouton = (200, 0, 0)
    couleur_texte = (255, 255, 255)
    rect = pygame.Rect(10, fenetre.get_height() - 60, 150, 50)
    pygame.draw.rect(fenetre, couleur_bouton, rect)
    texte = font.render('Retour au menu', True, couleur_texte)
    fenetre.blit(texte, (rect.x + 10, rect.y + 10))
    return rect

def afficher_menu_principal():
    while True:
        action = afficher_menu(Interface_util.fenetre)
        if action == "nouvelle_partie":
            return "nouvelle_partie"
        elif action == "charger_sauvegarde":
            return "charger_sauvegarde"
        elif action == "quitter":
            pygame.quit()
            exit()


while True:
    action = afficher_menu_principal()

    if action == "nouvelle_partie":
        grille.verifier_proportions_grille(Fenetre_util)
        running = True

    if action == "charger_sauvegarde":
        dossier_sauvegardes = "./sauvegarde/grille/"
        fichiers_sauvegardes = lister_sauvegardes(dossier_sauvegardes)

        if not fichiers_sauvegardes:
            print("Aucune sauvegarde disponible.")
            continue

        index_selection = 0
        EntrerDossierSauvegarde = True

        while EntrerDossierSauvegarde:
            rectangle = pygame.Rect(0, 0, Interface_util.fenetre.get_width(), Interface_util.fenetre.get_height())
            pygame.draw.rect(Interface_util.fenetre, (0, 0, 0), rectangle)

            texte = Interface_util.font.render('Utilisez les flèches pour naviguer, Entrée pour sélectionner.', True,
                                               (255, 255, 255))
            Interface_util.fenetre.blit(texte, (10, 10))

            for i, fichier in enumerate(fichiers_sauvegardes):
                couleur = (0, 255, 0) if i == index_selection else (255, 255, 255)
                texte_fichier = Interface_util.font.render(fichier, True, couleur)
                Interface_util.fenetre.blit(texte_fichier, (10, 50 + i * 30))

            couleur_bouton = (255, 0, 0) if index_selection == len(fichiers_sauvegardes) else (255, 255, 255)
            texte_retour = Interface_util.font.render("Retour au menu", True, couleur_bouton)
            Interface_util.fenetre.blit(texte_retour, (10, 50 + len(fichiers_sauvegardes) * 30))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        index_selection = (index_selection - 1) % (len(fichiers_sauvegardes) + 1)
                    elif event.key == pygame.K_DOWN:
                        index_selection = (index_selection + 1) % (len(fichiers_sauvegardes) + 1)
                    elif event.key == pygame.K_RETURN:
                        if index_selection == len(fichiers_sauvegardes):
                            print("Retour au menu principal.")
                            EntrerDossierSauvegarde = False
                        else:
                            sauvegarde_choisie = fichiers_sauvegardes[index_selection]
                            chemin_sauvegarde = os.path.join(dossier_sauvegardes, sauvegarde_choisie)
                            grille.charger_grille_npz(chemin_sauvegarde)
                            grille.verifier_proportions_grille(Fenetre_util)
                            print(f"Sauvegarde {sauvegarde_choisie} chargée.")
                            EntrerDossierSauvegarde = False
                            running = True
                    elif event.key == pygame.K_ESCAPE:
                        print("Chargement annulé.")
                        EntrerDossierSauvegarde = False

    while running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if Moteur_util.Bool_sauvegarde | Moteur_util.Bool_form:
                        if event.key == pygame.K_RETURN:
                            if Moteur_util.Bool_sauvegarde:
                                grille.sauvegarder_grille_npz(f"./sauvegarde/grille/{Moteur_util.input_text}.npz")
                                Moteur_util.Bool_sauvegarde = False
                                print(f'Grille sauvegardée sous le nom {Moteur_util.input_text}.npz')
                                Moteur_util.input_text = ""
                            else:
                                Moteur_util.Bool_form = False
                                print(f'Forme utilisé : {Moteur_util.input_text}')
                                Moteur_util.Bool_form_placement = True
                        elif event.key == pygame.K_BACKSPACE:
                            Moteur_util.input_text = Moteur_util.input_text[:-1]
                        else:
                            Moteur_util.input_text += event.unicode

            if Moteur_util.Bool_form:
                Forme_util.menu_forme()
            else:
                if Moteur_util.Bool_sauvegarde:
                    rectangle = pygame.Rect(0, 0, Interface_util.fenetre.get_width(), Interface_util.fenetre.get_height())
                    pygame.draw.rect(Interface_util.fenetre, (0, 0, 0), rectangle)
                    texte = Interface_util.font.render('Veuillez choisir le nom de la sauvegarde :', True, (255, 255, 255))
                    Interface_util.fenetre.blit(texte, (10, 10))
                    texte_saisi = Interface_util.font.render(Moteur_util.input_text, True, (255, 255, 255))
                    Interface_util.fenetre.blit(texte_saisi, (10, 50))
                    pygame.display.flip()
                else:
                    if Moteur_util.Bool_reinit:
                        grille.creer_grille_vide()
                        Moteur_util.Bool_reinit = False

                    if not Moteur_util.Bool_pause:
                        if current_time - Moteur_util.last_evolution_time >= Moteur_util.evolution_delay:
                            grille.evoluer()
                            Moteur_util.last_evolution_time = current_time

                        # stocker_statistiques_csv(np.sum(grille.grille), grille.grille.size - np.sum(grille.grille), Moteur_util.iteration)
                        Moteur_util.iteration += 1

                    Moteur_util.gerer_souris(grille, Fenetre_util, Interface_util, Forme_util)
                    Interface_util.dessiner_grille(grille, Fenetre_util, Moteur_util)
                    Interface_util.afficher_statistiques(grille, Fenetre_util, Moteur_util)

                    bouton_retour = afficher_bouton_retour(Interface_util.fenetre, Interface_util.font)
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if bouton_retour.collidepoint(event.pos):
                                grille.creer_grille_vide()
                                running = False
                                break

                    Moteur_util.clock.tick(Moteur_util.fps)



# # Boucle principale du jeu
# running = True
# while running:
#     current_time = pygame.time.get_ticks()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if Moteur_util.Bool_sauvegarde | Moteur_util.Bool_form:
#                 if event.key == pygame.K_RETURN:
#                     # Sauvegarder la grille avec le nom de fichier saisi
#                     if Moteur_util.Bool_sauvegarde:
#                         grille.sauvegarder_grille_npz(f"./sauvegarde/grille/{Moteur_util.input_text}.npz")
#                         Moteur_util.Bool_sauvegarde = False
#                         print(f'Grille sauvegardée sous le nom {Moteur_util.input_text}.npz')
#                         Moteur_util.input_text = ""
#                     else:
#                         Moteur_util.Bool_form = False
#                         print(f'Forme utilisé : {Moteur_util.input_text}')
#                         Moteur_util.Bool_form_placement = True
                        
                    
#                 elif event.key == pygame.K_BACKSPACE:
#                     Moteur_util.input_text = Moteur_util.input_text[:-1]
#                 else:
#                     Moteur_util.input_text += event.unicode   

    
#     if Moteur_util.Bool_form:
#         Forme_util.menu_forme()
#     else :
#         if Moteur_util.Bool_sauvegarde:
        
#             rectangle = pygame.Rect(0, 0, Interface_util.fenetre.get_width(), Interface_util.fenetre.get_height())
#             pygame.draw.rect(Interface_util.fenetre, (0, 0, 0), rectangle)
#             texte = Interface_util.font.render('Veuillez choisir le nom de la sauvegarde :', True, (255, 255, 255))
#             Interface_util.fenetre.blit(texte, (10, 10))
#             texte_saisi = Interface_util.font.render(Moteur_util.input_text, True, (255, 255, 255))
#             Interface_util.fenetre.blit(texte_saisi, (10, 50))
#             pygame.display.flip()

#         else :
#             if Moteur_util.Bool_reinit:
#                 grille.creer_grille_vide()
#                 Moteur_util.Bool_reinit = False
            
#             if Moteur_util.Bool_reinit_ale:
#                 grille.creer_grille()
#                 Moteur_util.Bool_reinit_ale = False

#             if not Moteur_util.Bool_pause:
#                 # Évolution de la grille à intervalles réguliers
#                 if current_time - Moteur_util.last_evolution_time >= Moteur_util.evolution_delay:
#                     grille.evoluer()
#                     Moteur_util.last_evolution_time = current_time

#                 # Analyse_util.stocker_statistiques_csv(np.sum(grille.grille), grille.grille.size - np.sum(grille.grille), Moteur_util.iteration)
#                 Moteur_util.iteration += 1

#             # Gestion de la souris
#             Moteur_util.gerer_souris(grille, Fenetre_util, Interface_util, Forme_util) 

#             # Dessin de la grille
#             Interface_util.dessiner_grille(grille, Fenetre_util, Moteur_util)
            
#             Interface_util.afficher_statistiques(grille,Fenetre_util, Moteur_util)
#             pygame.display.flip()

#             # Contrôler le taux de rafraîchissement
#             Moteur_util.clock.tick(Moteur_util.fps)

    

pygame.quit()
# statistiques = charger_statistiques_csv()
# afficher_courbe_statistiques(statistiques)
# grille_finale = charger_grille_npz('grille.npz')
# print(f'Nombre de changements: {analyser_evolution(grille, grille_finale)}')