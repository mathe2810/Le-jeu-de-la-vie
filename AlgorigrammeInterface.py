from graphviz import *

# Create a new directed graph for the algorithm flowchart
flowchart = Digraph("GameOfLifeMenuFlowchart", format="png")
flowchart.attr(rankdir="TB", size="8,12")

# Add nodes for each function and decision
flowchart.node("Start", "Start", shape="oval", style="filled", color="lightgrey")
flowchart.node("Menu", "Menu (Affichage du menu et options utilisateur)", shape="box", style="rounded, filled", color="lightblue")
flowchart.node("AgrandirGrille", "agrandir_grille (Ajuster la taille de la grille)", shape="box", style="rounded, filled", color="lightgreen")
flowchart.node("CalculerColonnesLignes", "calculer_nombre_colonnes_lignes (Calcul des dimensions)", shape="box", style="rounded, filled", color="lightgreen")
flowchart.node("VerifierProportions", "verifier_proportions_grille (Valider proportions)", shape="box", style="rounded, filled", color="orange")
flowchart.node("DessinerGrille", "dessiner_grille (Affichage graphique de la grille)", shape="box", style="rounded, filled", color="pink")
flowchart.node("AfficherStats", "afficher_statistiques (Données de la simulation)", shape="box", style="rounded, filled", color="orange")
flowchart.node("AfficherFormes", "afficher_formes (Options des formes initiales)", shape="box", style="rounded, filled", color="pink")
flowchart.node("End", "End", shape="oval", style="filled", color="lightgrey")

# Add connections
flowchart.edge("Start", "Menu", label="Lancement de l'application")
flowchart.edge("Menu", "AgrandirGrille", label="Option: Démarrer simulation")
flowchart.edge("AgrandirGrille", "CalculerColonnesLignes", label="Calculer colonnes et lignes")
flowchart.edge("CalculerColonnesLignes", "VerifierProportions", label="Validation des dimensions")
flowchart.edge("VerifierProportions", "DessinerGrille", label="Dimensions valides")
flowchart.edge("DessinerGrille", "AfficherStats", label="Afficher infos statistiques")
flowchart.edge("AfficherStats", "AfficherFormes", label="Options supplémentaires")
flowchart.edge("AfficherFormes", "End", label="Fin ou boucle utilisateur")

# Render the flowchart
file_path = "FlowCharts/GameOfLifeInterfaceFlowchart"
flowchart.render(file_path, cleanup=True)
