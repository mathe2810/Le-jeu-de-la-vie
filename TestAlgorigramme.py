from graphviz import *

# Create a new directed graph for the algorithm flowchart
flowchart = Digraph("GameOfLifeFlowchart", format="png")
flowchart.attr(rankdir="TB", size="8,10")

# Add nodes for each function and decision
flowchart.node("Start", "Start", shape="oval", style="filled", color="lightgrey")
flowchart.node("CreerGrille", "creer_grille (Générer une grille aléatoire)", shape="box", style="rounded, filled", color="lightblue")
flowchart.node("CreerGrilleVide", "creer_grille_vide (Créer une grille vide)", shape="box", style="rounded, filled", color="lightblue")
flowchart.node("CompterVoisinsToro", "compter_voisins_vivants_laisser_revenir (Toroïde)", shape="box", style="rounded, filled", color="lightgreen")
flowchart.node("CompterVoisinsBloque", "compter_voisins_vivants_bloquer (Décalages)", shape="box", style="rounded, filled", color="lightgreen")
flowchart.node("Evoluer", "evoluer (Appliquer les règles du jeu de la vie)", shape="box", style="rounded, filled", color="orange")
flowchart.node("GererSouris", "gerer_souris (Interaction utilisateur)", shape="box", style="rounded, filled", color="pink")
flowchart.node("End", "End", shape="oval", style="filled", color="lightgrey")

# Add connections
flowchart.edge("Start", "CreerGrille", label="Option: Génération aléatoire")
flowchart.edge("Start", "CreerGrilleVide", label="Option: Grille vide")
flowchart.edge("CreerGrille", "CompterVoisinsToro", label="Calcul des voisins")
flowchart.edge("CreerGrilleVide", "CompterVoisinsToro", label="Calcul des voisins")
flowchart.edge("CompterVoisinsToro", "Evoluer", label="Règles appliquées")
flowchart.edge("CompterVoisinsBloque", "Evoluer", label="Règles appliquées")
flowchart.edge("Evoluer", "GererSouris", label="Passage à l'étape suivante")
flowchart.edge("GererSouris", "End", label="Fin ou actions utilisateur")

# Render the flowchart
file_path = "FlowCharts/GameOfLifeMotorFlowchart"
flowchart.render(file_path, cleanup=True)

