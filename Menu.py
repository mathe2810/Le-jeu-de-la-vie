import pygame
def afficher_formulaire_dimensions(fenetre, font):
    input_text = ""
    input_active = None
    couleur_inactive = (255, 255, 255)
    couleur_texte = (0, 0, 0)
    couleur_bouton = (255, 0, 0)

    # Taille des rectangles
    rect_formulaire = pygame.Rect(0, 0, 300, 50)
    bouton_valider = pygame.Rect(0, 0, 300, 50)

    # Centrer les rectangles
    rect_formulaire.center = (fenetre.get_width() // 2, fenetre.get_height() // 2)
    bouton_valider.center = (fenetre.get_width() // 2, fenetre.get_height() // 2 + 60)

    while True:
        fenetre.fill((0, 0, 0))
        texte_largeur = font.render("Largeur:", True, couleur_texte)
        texte_hauteur = font.render("Hauteur:", True, couleur_texte)
        texte_valider = font.render("Valider", True, couleur_texte)

        # Centrer les textes
        fenetre.blit(texte_largeur, (rect_formulaire.x - texte_largeur.get_width() - 10, rect_formulaire.y + (rect_formulaire.height - texte_largeur.get_height()) // 2))
        fenetre.blit(texte_hauteur, (rect_formulaire.x - texte_hauteur.get_width() - 10, rect_formulaire.y + (rect_formulaire.height - texte_hauteur.get_height()) // 2))

        pygame.draw.rect(fenetre, couleur_inactive, rect_formulaire)
        pygame.draw.rect(fenetre, couleur_bouton, bouton_valider)

        texte_formulaire_saisi = font.render(input_text, True, couleur_texte)
        fenetre.blit(texte_formulaire_saisi, (rect_formulaire.x + 5, rect_formulaire.y + 5))
        fenetre.blit(texte_valider, (bouton_valider.x + (bouton_valider.width - texte_valider.get_width()) // 2, bouton_valider.y + (bouton_valider.height - texte_valider.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect_formulaire.collidepoint(event.pos):
                    input_active = "formulaire"
                elif bouton_valider.collidepoint(event.pos):
                    return int(input_text)
            elif event.type == pygame.KEYDOWN:
                if input_active == "formulaire":
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode


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