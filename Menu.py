import pygame
def afficher_formulaire_dimensions(fenetre, font):
    largeur = ""
    hauteur = ""
    input_active = None
    couleur_inactive = (255, 255, 255)
    couleur_texte = (0, 0, 0)
    couleur_bouton = (255, 0, 0)

    # Taille des rectangles
    rect_largeur = pygame.Rect(0, 0, 300, 50)
    rect_hauteur = pygame.Rect(0, 0, 300, 50)
    bouton_valider = pygame.Rect(0, 0, 300, 50)

    # Centrer les rectangles
    rect_largeur.center = (fenetre.get_width() // 2, fenetre.get_height() // 2 - 60)
    rect_hauteur.center = (fenetre.get_width() // 2, fenetre.get_height() // 2)
    bouton_valider.center = (fenetre.get_width() // 2, fenetre.get_height() // 2 + 60)

    while True:
        fenetre.fill((0, 0, 0))
        texte_largeur = font.render("Largeur:", True, couleur_texte)
        texte_hauteur = font.render("Hauteur:", True, couleur_texte)
        texte_valider = font.render("Valider", True, couleur_texte)

        # Centrer les textes
        fenetre.blit(texte_largeur, (rect_largeur.x - texte_largeur.get_width() - 10, rect_largeur.y + (rect_largeur.height - texte_largeur.get_height()) // 2))
        fenetre.blit(texte_hauteur, (rect_hauteur.x - texte_hauteur.get_width() - 10, rect_hauteur.y + (rect_hauteur.height - texte_hauteur.get_height()) // 2))

        pygame.draw.rect(fenetre, couleur_inactive, rect_largeur)
        pygame.draw.rect(fenetre, couleur_inactive, rect_hauteur)
        pygame.draw.rect(fenetre, couleur_bouton, bouton_valider)

        texte_largeur_saisi = font.render(largeur, True, couleur_texte)
        texte_hauteur_saisi = font.render(hauteur, True, couleur_texte)
        fenetre.blit(texte_largeur_saisi, (rect_largeur.x + 5, rect_largeur.y + 5))
        fenetre.blit(texte_hauteur_saisi, (rect_hauteur.x + 5, rect_hauteur.y + 5))
        fenetre.blit(texte_valider, (bouton_valider.x + (bouton_valider.width - texte_valider.get_width()) // 2, bouton_valider.y + (bouton_valider.height - texte_valider.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect_largeur.collidepoint(event.pos):
                    input_active = "largeur"
                elif rect_hauteur.collidepoint(event.pos):
                    input_active = "hauteur"
                elif bouton_valider.collidepoint(event.pos):
                    return int(largeur), int(hauteur)
            elif event.type == pygame.KEYDOWN:
                if input_active == "largeur":
                    if event.key == pygame.K_BACKSPACE:
                        largeur = largeur[:-1]
                    else:
                        largeur += event.unicode
                elif input_active == "hauteur":
                    if event.key == pygame.K_BACKSPACE:
                        hauteur = hauteur[:-1]
                    else:
                        hauteur += event.unicode
def afficher_menu(fenetre):
    pygame.init()
    font = pygame.font.SysFont('Arial', 40)
    couleur_fond = (0, 0, 0)
    couleur_texte = (255, 255, 255)
    couleur_bouton = (100, 100, 100)
    couleur_bouton_hover = (150, 150, 150)

    fenetre.fill(couleur_fond)

    texte_titre = font.render("Menu Principal", True, couleur_texte)
    fenetre.blit(texte_titre, (fenetre.get_width() // 2 - texte_titre.get_width() // 2, 50))

    boutons = [
        {"label": "Nouvelle Partie", "action": "nouvelle_partie"},
        {"label": "Charger Sauvegarde", "action": "charger_sauvegarde"},
        {"label": "Quitter", "action": "quitter"}
    ]

    bouton_rects = []
    for i, bouton in enumerate(boutons):
        largeur = 300
        hauteur = 60
        x = fenetre.get_width() // 2 - largeur // 2
        y = 150 + i * 100
        bouton_rect = pygame.Rect(x, y, largeur, hauteur)
        bouton_rects.append(bouton_rect)

        # Affichage du bouton
        pygame.draw.rect(fenetre, couleur_bouton, bouton_rect)
        texte_bouton = font.render(bouton["label"], True, couleur_texte)
        fenetre.blit(texte_bouton, (x + largeur // 2 - texte_bouton.get_width() // 2, y + hauteur // 2 - texte_bouton.get_height() // 2))

    pygame.display.flip()

    # Gestion des interactions
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, bouton in zip(bouton_rects, boutons):
                    if rect.collidepoint(event.pos):
                        return bouton["action"]

        # Mise Ã  jour des boutons (survol)
        for rect, bouton in zip(bouton_rects, boutons):
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(fenetre, couleur_bouton_hover, rect)
            else:
                pygame.draw.rect(fenetre, couleur_bouton, rect)

            texte_bouton = font.render(bouton["label"], True, couleur_texte)
            fenetre.blit(texte_bouton, (rect.x + rect.width // 2 - texte_bouton.get_width() // 2, rect.y + rect.height // 2 - texte_bouton.get_height() // 2))

        pygame.display.flip()