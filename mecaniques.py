# mecaniques.py
import random
import tkinter as tk
from tkinter import simpledialog

class LogiqueJeu:
    def __init__(self):
        # 1: Extrême, 2: Guerre, 3: Ville, 4: Planétaire TR, 5: Course Armée
        self.mode = 1  
        self.etape = "MENU_MODE"
        self.continents = []
        self.base_joueur = None
        self.code_partie = f"GEO-{random.randint(1000, 9999)}"
        
        # Ressources de base et avancées
        self.argent = 100
        self.plutonium = 0
        self.tour_actuel = "Joueur"
        self.actions_restantes = 2
        
        # Variables pour le Temps Réel (Mode 4)
        self.timer_action = 0
        
        # Progression des grands projets (Mode 5)
        self.construction_silo = 0     # Max 10 pour débloquer l'espace
        self.espace_debloque = False
        self.bombe_nucleaire_prete = False
        
        self.unites_placees = []
        self.custom_creations = []

    def charger_carte(self):
        """Génère la carte selon le mode choisi"""
        self.continents = []
        if self.mode in [4, 5]:
            # Mode Planétaire / Course Armée : Carte fixe mondiale simulée
            noms = ["Amérique du Nord", "Amérique du Sud", "Europe", "Afrique", "Asie", "Océanie"]
            positions = [(180, 250, 90), (250, 520, 80), (450, 220, 70), (480, 480, 85), (620, 280, 110), (680, 550, 65)]
            for i, (x, y, r) in enumerate(positions):
                self.continents.append({"id": i, "nom": noms[i], "x": x, "y": y, "rayon": r})
        else:
            # Modes classiques : Îles aléatoires
            for i in range(random.randint(4, 7)):
                self.continents.append({"id": i, "nom": f"Île {i+1}", "x": random.randint(150, 600), "y": random.randint(150, 600), "rayon": random.randint(50, 95)})

    def fenetre_custom_creation(self):
        root = tk.Tk()
        root.withdraw()
        nom = simpledialog.askstring("Atelier d'Invention", "Nom du projet d'État :")
        if nom:
            description = simpledialog.askstring("Atelier d'Invention", f"Décrivez la loi ou l'arme '{nom}' :")
            if description:
                self.custom_creations.append({"nom": nom, "effet": description, "cout": 40})
                self.actions_restantes -= 1
                self.argent -= 40
        root.destroy()

    def verifier_fin_de_tour(self):
        if self.actions_restantes <= 0:
            self.forcer_fin_tour()

    def forcer_fin_tour(self):
        """Déclenche le changement de tour (géré par le joueur ou par le timer)"""
        if self.tour_actuel == "Joueur":
            self.tour_actuel = "IA"
            self.gerer_tour_ia()

    def gerer_tour_ia(self):
        if not self.continents: return
        
        # Production passive de fin de tour
        self.argent += 40
        
        # En mode Course Armée, l'IA essaie aussi d'avoir du nucléaire
        if self.mode == 5 and random.random() > 0.7:
            self.unites_placees.append({"type": "Mine Plu.", "niveau": 1, "x": random.randint(300,600), "y": random.randint(300,600), "camp": "IA"})
            
        # L'IA place une unité militaire basique
        if self.mode in [1, 2, 4, 5]:
            cible = random.choice(self.continents)
            self.unites_placees.append({
                "type": random.choice(["Canon", "Tank"]), "niveau": 1,
                "x": cible["x"] + random.randint(-20, 20), "y": cible["y"] + random.randint(-20, 20), "camp": "IA"
            })

        # Retour au joueur
        self.actions_restantes = 2
        self.tour_actuel = "Joueur"
