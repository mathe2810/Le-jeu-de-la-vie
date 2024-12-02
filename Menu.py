import pygame

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