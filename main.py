# main.py (PARTIE 1)
import sys
import random
import pygame
from mecaniques import LogiqueJeu

pygame.init()
LARGEUR, HAUTEUR = 1150, 750
ECRAN = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Géo-Cartes: Empires & Conquête Mondiale")
HORLOGE = pygame.time.Clock()

COULEUR_FOND = (240, 240, 235)
COULEUR_MER = (205, 225, 235)
COULEUR_CONTINENT = (175, 205, 165)
COULEUR_TEXTE = (30, 30, 30)
COULEUR_BOUTON = (215, 215, 210)
COULEUR_BASE = (225, 50, 50)
COULEUR_IA = (50, 50, 225)
COULEUR_SPECIAL = (160, 80, 200) # Violet pour le plutonium / espace

POLICE = pygame.font.SysFont("Arial", 16)
POLICE_TITRE = pygame.font.SysFont("Arial", 24, bold=True)

class Interface:
    def __init__(self):
        self.jeu = LogiqueJeu()

    def dessiner_bouton(self, texte, x, y, l, h, couleur=COULEUR_BOUTON):
        rect = pygame.Rect(x, y, l, h)
        pygame.draw.rect(ECRAN, couleur, rect)
        pygame.draw.rect(ECRAN, COULEUR_TEXTE, rect, 1)
        txt = POLICE.render(texte, True, COULEUR_TEXTE)
        ECRAN.blit(txt, (x + (l - txt.get_width())//2, y + (h - txt.get_height())//2))
        return rect

    def afficher_texte(self, texte, x, y, police=POLICE, couleur=COULEUR_TEXTE):
        surface = police.render(texte, True, couleur)
        ECRAN.blit(surface, (x, y))

    def dessiner(self):
        ECRAN.fill(COULEUR_FOND)
        j = self.jeu

        if j.etape == "MENU_MODE":
            self.afficher_texte("DEVENEZ LE DIRIGEANT DU MONDE", LARGEUR//2 - 200, 60, POLICE_TITRE)
            self.btn_m1 = self.dessiner_bouton("1. Mode Extrême Classique", LARGEUR//2 - 200, 160, 400, 45)
            self.btn_m2 = self.dessiner_bouton("2. Mode Guerre Seule", LARGEUR//2 - 200, 220, 400, 45)
            self.btn_m3 = self.dessiner_bouton("3. Mode Ville Seule", LARGEUR//2 - 200, 280, 400, 45)
            self.btn_m4 = self.dessiner_bouton("4. MODE PLANÉTAIRE (Temps Réel - Map Fixe)", LARGEUR//2 - 200, 360, 400, 50, (240, 180, 180))
            self.btn_m5 = self.dessiner_bouton("5. COURSE ARMA-SPATIALE (Plutonium & Fusée)", LARGEUR//2 - 200, 430, 400, 50, (180, 220, 240))

        elif j.etape in ["SELECTION_BASE", "PARTIE"]:
            # Rendu Map
            pygame.draw.rect(ECRAN, COULEUR_MER, (30, 50, 740, 650))
            pygame.draw.rect(ECRAN, COULEUR_TEXTE, (30, 50, 740, 650), 2)

            for c in j.continents:
                pygame.draw.circle(ECRAN, COULEUR_CONTINENT, (c["x"], c["y"]), c["rayon"])
                pygame.draw.circle(ECRAN, COULEUR_TEXTE, (c["x"], c["y"]), c["rayon"], 1)
                if j.mode in [4, 5]:
                    self.afficher_texte(c["nom"], c["x"] - 40, c["y"] - 10, POLICE)

            if j.base_joueur:
                pygame.draw.circle(ECRAN, COULEUR_BASE, (j.base_joueur["x"], j.base_joueur["y"]), 18)
                self.afficher_texte("QG", j.base_joueur["x"] - 10, j.base_joueur["y"] - 30)

            for u in j.unites_placees:
                c_unite = COULEUR_BASE if u["camp"] == "Joueur" else COULEUR_IA
                if "Mine" in u["type"] or "Silo" in u["type"]: c_unite = COULEUR_SPECIAL
                pygame.draw.rect(ECRAN, c_unite, (u["x"]-10, u["y"]-10, 20, 20))
                self.afficher_texte(f"{u['type']}v{u['niveau']}", u["x"]-12, u["y"]-25)

            # PANNEAU LATÉRAL
            pygame.draw.line(ECRAN, COULEUR_TEXTE, (790, 0), (790, HAUTEUR), 2)
            
            titre_mode = "CONQUÊTE EN DIRECT" if j.mode == 4 else "COURSE ARME-SPATIALE" if j.mode == 5 else "STRATÉGIE"
            self.afficher_texte(titre_mode, 810, 20, POLICE_TITRE)
            self.afficher_texte(f"Trésor : {j.argent} Or", 810, 60)
            
            if j.mode == 5:
                self.afficher_texte(f"Plutonium : {j.plutonium} kg", 810, 85, POLICE, COULEUR_SPECIAL)
                self.afficher_texte(f"Silo spatial : {j.construction_silo}/10 tours", 810, 110)

            if j.mode == 4:
                barre_temps = int((j.timer_action / 180) * 180)
                pygame.draw.rect(ECRAN, (200, 50, 50), (810, 140, barre_temps, 10))
                self.afficher_texte("VITE ! Le tour défile en continu...", 810, 155)
            else:
                self.afficher_texte(f"Actions : {j.actions_restantes} / 2 (Tour: {j.tour_actuel})", 810, 140)

            if j.etape == "SELECTION_BASE":
                self.afficher_texte("CHOISISSEZ VOTRE PAYS DE DÉPART", 810, 200, POLICE_TITRE, COULEUR_BASE)
            elif j.etape == "PARTIE":
                self.afficher_texte("--- ACTIONS MILITAIRES ---", 810, 190)
                self.btn_barriere = self.dessiner_bouton("Barrière (15 Or)", 810, 220, 150, 30)
                self.btn_tank = self.dessiner_bouton("Tank (45 Or)", 970, 220, 150, 30)
# main.py (PARTIE 2 - À coller directement sous la Partie 1)
                if j.mode == 5:
                    self.afficher_texte("--- TECHNOLOGIES D'ÉTAT ---", 810, 270, POLICE, COULEUR_SPECIAL)
                    self.btn_mine_plu = self.dessiner_bouton("+ Mine Plutonium (60 Or)", 810, 295, 310, 35)
                    self.btn_const_silo = self.dessiner_bouton("+ Travailler sur le Silo (30 Or)", 810, 340, 310, 35)
                    
                    if j.construction_silo >= 10:
                        self.btn_lancer_sat = self.dessiner_bouton("LANCER FUSÉE / SAT (80 Or)", 810, 385, 310, 35, (180, 240, 180))
                    if j.plutonium >= 5:
                        self.btn_bombe = self.dessiner_bouton("☢️ BRULER UN CONTINENT (5 Plu)", 810, 430, 310, 35, (240, 100, 100))

                self.afficher_texte("--- RECHERCHE LIBRE ---", 810, 490)
                self.btn_craft = self.dessiner_bouton("Créer un décret sur mesure (40 Or)", 810, 520, 310, 35)
                
                if j.mode != 4:
                    self.btn_passer = self.dessiner_bouton("Forcer Fin du tour", 810, 690, 310, 35)

        pygame.display.flip()

    def lancer(self):
        while True:
            j = self.jeu
            
            if j.etape == "PARTIE" and j.mode == 4:
                j.timer_action += 1
                if j.timer_action >= 180:
                    j.timer_action = 0
                    j.forcer_fin_tour()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    if j.etape == "MENU_MODE":
                        if self.btn_m1.collidepoint(pos): j.mode = 1
                        elif self.btn_m2.collidepoint(pos): j.mode = 2
                        elif self.btn_m3.collidepoint(pos): j.mode = 3
                        elif self.btn_m4.collidepoint(pos): j.mode = 4
                        elif self.btn_m5.collidepoint(pos): j.mode = 5
                        j.charger_carte()
                        j.etape = "SELECTION_BASE"
                        
                    elif j.etape == "SELECTION_BASE":
                        for c in j.continents:
                            if ((pos - c["x"])**2 + (pos - c["y"])**2)**0.5 <= c["rayon"]:
                                j.base_joueur = c; j.etape = "PARTIE"; break
                                
                    elif j.etape == "PARTIE" and (j.tour_actuel == "Joueur" or j.mode == 4):
                        if self.btn_barriere.collidepoint(pos) and j.argent >= 15:
                            j.argent -= 15; j.actions_restantes -= 1
                            j.unites_placees.append({"type": "Barrière", "niveau": 1, "x": j.base_joueur["x"]+random.randint(-30,30), "y": j.base_joueur["y"]+random.randint(-30,30), "camp": "Joueur"})
                        elif self.btn_tank.collidepoint(pos) and j.argent >= 45:
                            j.argent -= 45; j.actions_restantes -= 1
                            j.unites_placees.append({"type": "Tank", "niveau": 1, "x": j.base_joueur["x"]+random.randint(-30,30), "y": j.base_joueur["y"]+random.randint(-30,30), "camp": "Joueur"})
                        elif self.btn_craft.collidepoint(pos) and j.argent >= 40:
                            j.fenetre_custom_creation()
                            
                        if j.mode == 5:
                            if self.btn_mine_plu.collidepoint(pos) and j.argent >= 60:
                                j.argent -= 60; j.actions_restantes -= 1
                                j.unites_placees.append({"type": "Mine Plu.", "niveau": 1, "x": j.base_joueur["x"]+random.randint(-40,40), "y": j.base_joueur["y"]+random.randint(-40,40), "camp": "Joueur"})
                            elif self.btn_const_silo.collidepoint(pos) and j.argent >= 30:
                                j.argent -= 30; j.actions_restantes -= 1; j.construction_silo += 1
                                if j.construction_silo == 1:
                                    j.unites_placees.append({"type": "Silo", "niveau": 1, "x": j.base_joueur["x"]+35, "y": j.base_joueur["y"]+35, "camp": "Joueur"})
                            elif j.construction_silo >= 10 and self.btn_lancer_sat.collidepoint(pos) and j.argent >= 80:
                                j.argent -= 80; j.actions_restantes -= 1; j.espace_debloque = True
                            elif j.plutonium >= 5 and self.btn_bombe.collidepoint(pos):
                                j.plutonium -= 5; j.actions_restantes -= 1
                                j.unites_placees = [u for u in j.unites_placees if u["camp"] == "Joueur"]

                        if j.mode != 4 and self.btn_passer.collidepoint(pos):
                            j.actions_restantes = 0
                            
                        if j.mode == 5:
                            mines = [u for u in j.unites_placees if u["type"] == "Mine Plu." and u["camp"] == "Joueur"]
                            if random.random() > 0.8: j.plutonium += len(mines)

                        if j.mode != 4:
                            j.verifier_fin_de_tour()

            self.dessiner()
            HORLOGE.tick(30)

if __name__ == "__main__":
    ui = Interface()
    ui.lancer()
