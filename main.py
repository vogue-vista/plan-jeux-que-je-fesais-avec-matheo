# main.py
import sys
import random
import pygame
from mecaniques import LogiqueJeu  # On lie le premier fichier ici !

# Initialisation
pygame.init()
LARGEUR, HAUTEUR = 1100, 750
ECRAN = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Projet Geo-Cartes")
HORLOGE = pygame.time.Clock()

# Couleurs
COULEUR_FOND = (245, 245, 240)
COULEUR_MER = (215, 230, 240)
COULEUR_CONTINENT = (185, 215, 175)
COULEUR_TEXTE = (35, 35, 35)
COULEUR_BOUTON = (210, 210, 205)
COULEUR_BASE = (230, 60, 60)
COULEUR_IA = (60, 60, 230)

POLICE = pygame.font.SysFont("Arial", 18)
POLICE_TITRE = pygame.font.SysFont("Arial", 26, bold=True)

class Interface:
    def __init__(self):
        self.jeu = LogiqueJeu()

    def dessiner_bouton(self, texte, x, y, l, h):
        rect = pygame.Rect(x, y, l, h)
        pygame.draw.rect(ECRAN, COULEUR_BOUTON, rect)
        pygame.draw.rect(ECRAN, COULEUR_TEXTE, rect, 1)
        txt = POLICE.render(texte, True, COULEUR_TEXTE)
        ECRAN.blit(txt, (x + (l - txt.get_width())//2, y + (h - txt.get_height())//2))
        return rect

    def afficher_texte(self, texte, x, y, police=POLICE):
        surface = police.render(texte, True, COULEUR_TEXTE)
        ECRAN.blit(surface, (x, y))

    def dessiner(self):
        ECRAN.fill(COULEUR_FOND)
        j = self.jeu

        if j.etape == "MENU_MODE":
            self.afficher_texte("PROJET GÉO-CARTES : STRATÉGIE", LARGEUR//2 - 200, 100, POLICE_TITRE)
            self.btn_m1 = self.dessiner_bouton("1. Mode Extrême (Guerre + Ville)", LARGEUR//2 - 200, 250, 400, 50)
            self.btn_m2 = self.dessiner_bouton("2. Mode Guerre Seule (Ville auto)", LARGEUR//2 - 200, 320, 400, 50)
            self.btn_m3 = self.dessiner_bouton("3. Mode Ville Seule (Gestion)", LARGEUR//2 - 200, 390, 400, 50)

        elif j.etape in ["SELECTION_BASE", "PARTIE"]:
            pygame.draw.rect(ECRAN, COULEUR_MER, (50, 50, 700, 650))
            pygame.draw.rect(ECRAN, COULEUR_TEXTE, (50, 50, 700, 650), 2)

            for c in j.continents:
                pygame.draw.circle(ECRAN, COULEUR_CONTINENT, (c["x"], c["y"]), c["rayon"])
                pygame.draw.circle(ECRAN, COULEUR_TEXTE, (c["x"], c["y"]), c["rayon"], 1)

            if j.base_joueur:
                pygame.draw.circle(ECRAN, COULEUR_BASE, (j.base_joueur["x"], j.base_joueur["y"]), 18)
                self.afficher_texte("BASE", j.base_joueur["x"] - 20, j.base_joueur["y"] - 35)

            for u in j.unites_placees:
                couleur = COULEUR_BASE if u["camp"] == "Joueur" else COULEUR_IA
                pygame.draw.rect(ECRAN, couleur, (u["x"]-10, u["y"]-10, 20, 20))
                self.afficher_texte(f"{u['type']}v{u['niveau']}", u["x"]-12, u["y"]-25)

            pygame.draw.line(ECRAN, COULEUR_TEXTE, (780, 0), (780, HAUTEUR), 2)
            self.afficher_texte(f"TOUR : {j.tour_actuel.upper()}", 800, 20, POLICE_TITRE)
            self.afficher_texte(f"Actions : {j.actions_restantes} / 2", 800, 60)
            self.afficher_texte(f"Votre Argent : {j.argent} Or", 800, 90)
            self.afficher_texte(f"Code : {j.code_partie} (Chill)", 800, 120)

            if j.etape == "SELECTION_BASE":
                self.afficher_texte("CLIQUEZ SUR UN CONTINENT", 800, 200, POLICE_TITRE)
            elif j.etape == "PARTIE":
                self.afficher_texte("--- UNITÉS BASIQUES ---", 800, 170)
                if j.mode in :
                    self.btn_barriere = self.dessiner_bouton("Barrière (15 Or)", 800, 200, 260, 35)
                    self.btn_canon = self.dessiner_bouton("Canon (30 Or)", 800, 245, 260, 35)
                    self.btn_mine = self.dessiner_bouton("Mine (20 Or)", 800, 290, 260, 35)
                    self.btn_tank = self.dessiner_bouton("Tank (45 Or)", 800, 335, 260, 35)
                
                if j.mode in :
                    self.btn_upgrade = self.dessiner_bouton("Améliorer (25 Or)", 800, 390, 260, 35)

                self.btn_craft = self.dessiner_bouton("Créer sur mesure (40 Or)", 800, 480, 260, 35)
                self.btn_passer = self.dessiner_bouton("Passer le tour", 800, 690, 260, 35)

                y_offset = 530
                for c in j.custom_creations[-2:]:
                    self.afficher_texte(f"*{c['nom']} : {c['effet'][:20]}...", 800, y_offset)
                    y_offset += 25

        pygame.display.flip()

    def lancer(self):
        while True:
            j = self.jeu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    if j.etape == "MENU_MODE":
                        if self.btn_m1.collidepoint(pos): j.mode = 1; j.generer_carte_aleatoire(); j.etape = "SELECTION_BASE"
                        elif self.btn_m2.collidepoint(pos): j.mode = 2; j.generer_carte_aleatoire(); j.etape = "SELECTION_BASE"
                        elif self.btn_m3.collidepoint(pos): j.mode = 3; j.generer_carte_aleatoire(); j.etape = "SELECTION_BASE"
                    elif j.etape == "SELECTION_BASE":
                        for c in j.continents:
                            if ((pos - c["x"])**2 + (pos - c["y"])**2)**0.5 <= c["rayon"]:
                                j.base_joueur = c; j.etape = "PARTIE"; break
                    elif j.etape == "PARTIE" and j.tour_actuel == "Joueur":
                        if j.mode in and self.btn_barriere.collidepoint(pos) and j.argent >= 15:
                            j.argent -= 15; j.actions_restantes -= 1
                            j.unites_placees.append({"type": "Barrière", "niveau": 1, "x": j.base_joueur["x"]+random.randint(-40,40), "y": j.base_joueur["y"]+random.randint(-40,40), "camp": "Joueur"})
                        elif j.mode in and self.btn_canon.collidepoint(pos) and j.argent >= 30:
                            j.argent -= 30; j.actions_restantes -= 1
                            j.unites_placees.append({"type": "Canon", "niveau": 1, "x": j.base_joueur["x"]+random.randint(-40,40), "y": j.base_joueur["y"]+random.randint(-40,40), "camp": "Joueur"})
                        elif j.mode in and self.btn_mine.collidepoint(pos) and j.argent >= 20:
                            j.argent -= 20; j.actions_restantes -= 1
                            j.unites_placees.append({"type": "Mine", "niveau": 1, "x": j.base_joueur["x"]+random.randint(-40,40), "y": j.base_joueur["y"]+random.randint(-40,40), "camp": "Joueur"})
                        elif j.mode in and self.btn_tank.collidepoint(pos) and j.argent >= 45:
                            j.argent -= 45; j.actions_restantes -= 1
                            j.unites_placees.append({"type": "Tank", "niveau": 1, "x": j.base_joueur["x"]+random.randint(-40,40), "y": j.base_joueur["y"]+random.randint(-40,40), "camp": "Joueur"})
                        elif j.mode in and self.btn_upgrade.collidepoint(pos) and j.argent >= 25:
                            uj = [u for u in j.unites_placees if u["camp"] == "Joueur"]
                            if uj: random.choice(uj)["niveau"] += 1; j.argent -= 25; j.actions_restantes -= 1
                        elif self.btn_craft.collidepoint(pos) and j.argent >= 40:
                            j.fenetre_custom_creation()
                        elif self.btn_passer.collidepoint(pos):
                            j.actions_restantes = 0
                        j.verifier_fin_de_tour()

            self.dessiner()
            HORLOGE.tick(30)

if __name__ == "__main__":
    ui = Interface()
    ui.lancer()
