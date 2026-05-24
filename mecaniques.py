# mecaniques.py
import random
import tkinter as tk
from tkinter import simpledialog

class LogiqueJeu:
    def __init__(self):
        self.mode = 1  # 1: Extrême, 2: Guerre, 3: Ville
        self.etape = "MENU_MODE"
        self.continents = []
        self.base_joueur = None
        self.code_partie = f"GEO-{random.randint(1000, 9999)}"
        
        # Système de tour strict
        self.tour_actuel = "Joueur"
        self.actions_restantes = 2
        self.argent = 100
        
        # Données de l'IA
        self.argent_ia = 100
        self.actions_ia = 2
        
        # Unités et inventions
        self.unites_placees = []
        self.custom_creations = []

    def generer_carte_aleatoire(self):
        self.continents = []
        for i in range(random.randint(4, 7)):
            x = random.randint(150, 600)
            y = random.randint(150, 600)
            rayon = random.randint(50, 95)
            self.continents.append({"id": i, "x": x, "y": y, "rayon": rayon})

    def fenetre_custom_creation(self):
        root = tk.Tk()
        root.withdraw()
        nom = simpledialog.askstring("Atelier d'Invention", "Nom de votre création :")
        if nom:
            description = simpledialog.askstring("Atelier d'Invention", f"Que fait '{nom}' ? Écrivez son effet :")
            if description:
                self.custom_creations.append({"nom": nom, "effet": description, "cout": 40})
                self.actions_restantes -= 1
                self.argent -= 40
        root.destroy()

    def verifier_fin_de_tour(self):
        if self.actions_restantes <= 0:
            self.tour_actuel = "IA"
            self.actions_ia = 2
            self.argent_ia += 30
            self.gerer_tour_ia()

    def gerer_tour_ia(self):
        if not self.continents: return
        
        # L'IA place une unité basique
        continent_cible = random.choice(self.continents)
        type_ia = random.choice(["Barrière", "Canon", "Tank"])
        self.unites_placees.append({
            "type": type_ia, "niveau": 1, 
            "x": continent_cible["x"] + random.randint(-20, 20), 
            "y": continent_cible["y"] + random.randint(-20, 20), 
            "camp": "IA"
        })
        
        # L'IA améliore une unité
        if self.unites_placees:
            unites_ia = [u for u in self.unites_placees if u["camp"] == "IA"]
            if unites_ia:
                random.choice(unites_ia)["niveau"] += 1

        # Retour au Joueur
        self.argent += 40
        self.actions_restantes = 2
        self.tour_actuel = "Joueur"
