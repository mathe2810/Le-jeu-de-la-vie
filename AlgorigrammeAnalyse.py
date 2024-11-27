from graphviz import Digraph

# Création d'un diagramme de flux pour les fonctions statistiques du Jeu de la Vie
flowchart = Digraph("GameOfLifeStatisticsFlowchart", format="png")
flowchart.attr(rankdir="TB", size="10,12")

# Ajout des nœuds pour chaque fonction et étape
flowchart.node("Start", "Start", shape="oval", style="filled", color="lightgrey")
flowchart.node("Analyser", "analyser_evolution\n(Calcul des changements entre grilles)", shape="box", style="rounded, filled", color="lightblue")
flowchart.node("Stocker", "stocker_statistiques_csv\n(Enregistrer les statistiques)", shape="box", style="rounded, filled", color="lightgreen")
flowchart.node("Charger", "charger_statistiques_csv\n(Charger statistiques depuis CSV)", shape="box", style="rounded, filled", color="orange")
flowchart.node("Supprimer", "supprimer_statistiques\n(Supprimer le fichier CSV)", shape="box", style="rounded, filled", color="red")
flowchart.node("Afficher", "afficher_courbe_statistiques\n(Afficher l'évolution en courbe)", shape="box", style="rounded, filled", color="pink")
flowchart.node("End", "End", shape="oval", style="filled", color="lightgrey")

# Ajout des connexions
flowchart.edge("Start", "Analyser", label="Début de l'analyse")
flowchart.edge("Analyser", "Stocker", label="Statistiques calculées")
flowchart.edge("Stocker", "Charger", label="Option: Lecture des données")
flowchart.edge("Stocker", "Supprimer", label="Option: Supprimer les données")
flowchart.edge("Charger", "Afficher", label="Données chargées")
flowchart.edge("Supprimer", "End", label="Nettoyage terminé")
flowchart.edge("Afficher", "End", label="Affichage terminé")

# Génération du fichier PNG
file_path = "FlowCharts/GameOfLifeStatisticsFlowchart"
flowchart.render(file_path, cleanup=True)
