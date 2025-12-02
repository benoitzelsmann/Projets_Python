import tkinter as tk
from itertools import combinations
from math import sqrt, atan2, sin, cos, pi
from time import time
from typing import List, Optional, Tuple

from Boule import Boule
from Trace import Trace

class Altitude(tk.Toplevel):
    """
    Fenêtre secondaire (Toplevel) pour afficher la vue de côté (Altitude).
    Gérée par le même processus que Jeu pour éviter les erreurs de multiprocessing.
    """
    def __init__(self, master_game: 'Jeu'):
        super().__init__(master_game)
        self.master_game = master_game
        
        self.dim_graphe = [10, 2]  # longueur, hauteur en mètres
        self.metre = 60
        self.dim_fenetre = [x * self.metre for x in self.dim_graphe]
        
        self.title('Altitude (Vue de côté)')
        
        # Positionnement de la fenêtre
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) + int(self.master_game.dim_fentre[0] / 1.5)
        y = (screen_height // 2) - (self.dim_fenetre[1] // 2)
        self.geometry(f"{self.dim_fenetre[0]}x{self.dim_fenetre[1]}+{x}+{y}")

        self.canvas2 = tk.Canvas(self, bg='white')
        self.canvas2.pack(fill=tk.BOTH, expand=True)

        self.dessin_boule: Optional[int] = None
        self.boule_suivie: Optional[Boule] = None
        self.traj_dessin: List[int] = []
        self.coords_precedentes: Tuple[float, float] = (0.0, 0.0)

        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        # Lancement de la boucle locale
        self.update_view()

    def hide_window(self):
        """Au lieu de détruire, on cache ou on ignore le clic croix pour l'instant"""
        pass

    def reset_view(self):
        """Nettoie l'affichage quand on change de boule"""
        if self.dessin_boule:
            self.canvas2.delete(self.dessin_boule)
            self.dessin_boule = None
        
        for draw in self.traj_dessin:
            self.canvas2.delete(draw)
        self.traj_dessin = []

    def update_view(self):
        if not self.master_game.play: 
            return

        # On suit toujours la dernière boule lancée
        if self.master_game.boules:
            current_boule = self.master_game.boules[-1]
            
            # Si on a changé de boule (nouveau lancer)
            if current_boule != self.boule_suivie:
                self.reset_view()
                self.boule_suivie = current_boule
                
                # Initialisation graphique de la nouvelle boule
                boule_x_px = current_boule.ym * self.metre
                boule_y_px = self.dim_fenetre[1] - current_boule.zm * self.metre
                radius = current_boule.radius_m * self.metre
                
                self.dessin_boule = self.canvas2.create_oval(
                    boule_x_px - radius, boule_y_px - 2 * radius,
                    boule_x_px + radius, boule_y_px,
                    fill=current_boule.color, outline='black'
                )
                self.coords_precedentes = (boule_x_px, boule_y_px)

            # Mise à jour position
            if self.dessin_boule and self.boule_suivie:
                boule_x_px = self.boule_suivie.ym * self.metre
                boule_y_px = self.dim_fenetre[1] - self.boule_suivie.zm * self.metre
                radius = self.boule_suivie.radius_m * self.metre

                # Déplacer le cercle
                self.canvas2.coords(
                    self.dessin_boule,
                    boule_x_px - radius, boule_y_px - 2 * radius,
                    boule_x_px + radius, boule_y_px
                )
                
                # Tracer la traînée
                line = self.canvas2.create_line(
                    self.coords_precedentes[0], self.coords_precedentes[1] - radius,
                    boule_x_px, boule_y_px - radius,
                    fill='black'
                )
                self.traj_dessin.append(line)
                
                self.coords_precedentes = (boule_x_px, boule_y_px)

        self.after(20, self.update_view)


class Jeu(tk.Tk):

    def __init__(self):
        super().__init__()

        """definitions des parametres graphiques"""
        self.images_secondes = 100 # Plus standard
        self.delay = 1 / self.images_secondes
        self.inital_time = time()

        """Definir la taille du terrain"""
        self.dim_terrain = [5, 10]  # dimensions en metres du terrain
        self.metre = 80  # 1m = 80 pixels

        """Placer et titrer la fenetre au centre de l'écran"""
        self.dim_fentre = [self.metre * dim for dim in self.dim_terrain]
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - int(self.dim_fentre[0] / 1.5)
        y = (screen_height // 2) - (self.dim_fentre[1] // 2) - 20
        self.geometry(f"{self.dim_fentre[0]}x{self.dim_fentre[1]}+{x}+{y}")
        self.title('Pétanque - Vue de dessus')

        """Création du canvas dans lequel on va dessiner les boules"""
        self.canvas = tk.Canvas(self, bg='beige')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Légendes
        self.legend_team = self.canvas.create_text(150, self.dim_fentre[1] - 30, text="Equipe la plus proche : -")
        self.legend_dist = self.canvas.create_text(350, self.dim_fentre[1] - 30, text="Distance : -")

        """Gestion du Jeu"""
        self.play = True
        self.jouer_tour = True # Indique si on peut lancer
        self.len_boules = 0
        self.couples_a_tester = []
        
        self.equipe_plus_proche: Optional[int] = None
        self.dist_min: float = 0.0
        self.equipe_commence = 1

        # Liste des boules (commence avec le cochonnet)
        self.boules: List[Boule] = [Boule(self, 2.6, 8, 0, 'Cochonnet', None)]
        self.redefinir_combinaisons()

        self.time_avant_retest_collision = 0.1  # s

        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)

        """Paramètres physiques et lancer"""
        self.start_xm = 2.5  # position de lancer initiale
        self.start_ym = 1.0
        self.coeff = 2
        self.drop_angle = 30 / 180 * pi
        self.gravity = 9.81
        self.hauteur_bonhomme = 0.6  # m

        # Outil de tracé
        self.trace = Trace(self, self.coeff)
        
        # Fenêtre secondaire (Altitude)
        self.alt_window = Altitude(self)

        """Lancement de l'actualisation de la fenetre"""
        self.update_game()

    def update_legendes(self):
        txt_eq = str(self.equipe_plus_proche) if self.equipe_plus_proche else "-"
        self.canvas.itemconfig(self.legend_team, text=f"Equipe la plus proche : {txt_eq}")
        self.canvas.itemconfig(self.legend_dist, text=f"Distance : {self.dist_min} (m)")

    def redefinir_combinaisons(self):
        # On recalcule les paires seulement si le nombre de boules change
        if len(self.boules) != self.len_boules:
            # Liste d'indices : [0, 1, 2...]
            indices = list(range(len(self.boules)))
            self.couples_a_tester = list(combinations(indices, 2))
            self.len_boules = len(self.boules)

    def update_positions_boules(self):
        current_time = time()
        dt = current_time - self.inital_time
        # Limite dt pour éviter les sauts physiques si l'ordi lag
        if dt > 0.1: dt = 0.016 
        
        # On vérifie si tout le monde est à l'arrêt pour autoriser le prochain lancer
        all_stopped = True

        for boule in self.boules:
            # Mouvement au sol
            boule.xm += dt * boule.speed_xm
            boule.ym += dt * boule.speed_ym

            # Mouvement vertical
            boule.speed_zm -= dt * self.gravity
            
            # Gestion altitude
            # Si la boule est en l'air ou vient de rebondir
            if boule.zm > 0 or boule.speed_zm > 0: 
                boule.zm += dt * boule.speed_zm
                # Effet visuel : la boule grossit quand elle monte
                # Attention : zm est petit, factorisons pour voir l'effet
                scale_factor = 1 + boule.zm * 0.5
                boule.radius = boule.initial_radius * scale_factor
            else:
                # Au sol
                boule.zm = 0
                boule.radius = boule.initial_radius
                
                # Rebond très amorti ou nul
                if abs(boule.speed_zm) > 0.5: # Seuil de rebond
                     boule.speed_zm = -boule.speed_zm * 0.3 # Rebond faible
                else:
                    boule.speed_zm = 0

            # Frottements au sol uniquement si z=0
            if boule.zm <= 0.001: # Tolérance zéro
                boule.zm = 0
                speed = sqrt(boule.speed_xm ** 2 + boule.speed_ym ** 2)
                
                if speed > 0:
                    # Décélération (F = m.a -> a = F/m = mu.g)
                    decel = boule.mu * self.gravity * dt
                    new_speed = max(0, speed - decel)
                    
                    if speed > 0:
                        ratio = new_speed / speed
                        boule.speed_xm *= ratio
                        boule.speed_ym *= ratio
                    
                    # Arrêt complet si très lent
                    if new_speed < 0.05:
                        boule.speed_xm = 0
                        boule.speed_ym = 0
            
            # Vérification état mouvement
            if abs(boule.speed_xm) > 0.01 or abs(boule.speed_ym) > 0.01 or abs(boule.speed_zm) > 0.1:
                all_stopped = False

            boule.update_pos()

        self.jouer_tour = all_stopped
        self.inital_time = current_time

    def detecter_collisons_bord(self):
        boules_to_remove = []
        for boule in self.boules:
            # Pas besoin de rappeler metre_to_pixels ici, update_pos le fait
            
            # Bord Gauche
            if boule.xm - boule.radius_m <= 0:
                boule.xm = boule.radius_m + 0.01
                boule.speed_xm *= -0.8 # Rebond amorti

            # Bord Droit
            elif boule.xm + boule.radius_m >= self.dim_terrain[0]:
                boule.xm = self.dim_terrain[0] - boule.radius_m - 0.01
                boule.speed_xm *= -0.8

            # Bord Fond (Haut de l'écran) -> Sortie
            elif boule.ym + boule.radius_m >= self.dim_terrain[1]:
                # On ne supprime pas immédiatement pour ne pas casser la boucle
                boules_to_remove.append(boule)
            
            # Bord Bas (Ligne de départ)
            elif boule.ym - boule.radius_m <= 0:
                 boule.ym = boule.radius_m + 0.01
                 boule.speed_ym *= -0.8

        # Suppression propre
        for b in boules_to_remove:
            if b.dessin:
                self.canvas.delete(b.dessin)
            if b in self.boules:
                self.boules.remove(b)
        
        if boules_to_remove:
            self.redefinir_combinaisons()

    def detecter_collisions_entre_boules(self):
        for idx1, idx2 in self.couples_a_tester:
            # Sécurité si une boule a été supprimée entre temps
            if idx1 >= len(self.boules) or idx2 >= len(self.boules):
                continue
                
            boule1 = self.boules[idx1]
            boule2 = self.boules[idx2]
            
            # Si immunité temporaire, on passe
            if boule1.just_decal or boule2.just_decal:
                continue
            
            # Les boules ne se touchent que si elles sont à peu près à la même altitude
            if abs(boule1.zm - boule2.zm) > (boule1.radius_m + boule2.radius_m):
                continue

            dx = boule1.xm - boule2.xm
            dy = boule1.ym - boule2.ym # inversion repère pas nécessaire ici car diff relative
            distance = sqrt(dx ** 2 + dy ** 2)
            rayon_total = boule1.radius_m + boule2.radius_m

            # Collision détectée
            if distance < rayon_total:
                # Repousser les boules pour qu'elles ne se chevauchent plus
                overlap = rayon_total - distance
                angle = atan2(dy, dx)
                
                move_dist = overlap / 2 + 0.001
                
                boule1.xm += cos(angle) * move_dist
                boule1.ym += sin(angle) * move_dist
                boule2.xm -= cos(angle) * move_dist
                boule2.ym -= sin(angle) * move_dist
                
                # Activer immunité
                boule1.decale(self.time_avant_retest_collision)
                boule2.decale(self.time_avant_retest_collision)

                # --- Physique du choc élastique 2D ---
                
                # Vecteur normal unitaire
                nx = dx / distance
                ny = dy / distance
                
                # Vecteur tangent unitaire
                tx = -ny
                ty = nx
                
                # Projection des vitesses sur la normale et la tangente
                v1n = nx * boule1.speed_xm + ny * boule1.speed_ym
                v1t = tx * boule1.speed_xm + ty * boule1.speed_ym
                v2n = nx * boule2.speed_xm + ny * boule2.speed_ym
                v2t = tx * boule2.speed_xm + ty * boule2.speed_ym
                
                # Échange des vitesses normales (conservation quantité mvt + énergie cinétique)
                # Formule collision élastique 1D masses m1, m2
                m1 = boule1.mass
                m2 = boule2.mass
                
                v1n_final = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
                v2n_final = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)
                
                # Recomposition
                boule1.speed_xm = v1n_final * nx + v1t * tx
                boule1.speed_ym = v1n_final * ny + v1t * ty
                boule2.speed_xm = v2n_final * nx + v2t * tx
                boule2.speed_ym = v2n_final * ny + v2t * ty
                
                # Amortissement du choc
                loss = 0.9
                boule1.speed_xm *= loss
                boule1.speed_ym *= loss
                boule2.speed_xm *= loss
                boule2.speed_ym *= loss

    def lancer_boule(self, speed_x, speed_y, speed_z):
        equipe = 1
        if self.equipe_plus_proche is not None:
            # Si l'équipe 1 gagne, c'est à l'équipe 2 de jouer (pour reprendre le point)
            if self.equipe_plus_proche == 1:
                equipe = 2
            else:
                equipe = 1
        else:
            equipe = self.equipe_commence

        boule = Boule(self, self.start_xm, self.start_ym, self.hauteur_bonhomme, 'Boule', equipe)
        
        boule.speed_xm = speed_x
        boule.speed_ym = speed_y
        boule.speed_zm = speed_z

        self.boules.append(boule)
        self.redefinir_combinaisons()

    def update_game(self):
        if self.play:
            self.update_positions_boules()
            self.detecter_collisons_bord()
            self.detecter_collisions_entre_boules()
            self.calcul_plus_proche()

            if len(self.boules) > 1:
                self.update_legendes()

            self.after(20, self.update_game)

    def calcul_plus_proche(self):
        # La boule 0 est le cochonnet
        if len(self.boules) > 1:
            cochonnet = self.boules[0]
            mod_min = 999.0
            index_boule_min = -1

            for i in range(1, len(self.boules)):
                boule = self.boules[i]
                # Distance euclidienne simple 2D (on ignore z pour le point)
                dist = sqrt((cochonnet.xm - boule.xm) ** 2 + (cochonnet.ym - boule.ym) ** 2)
                
                if dist < mod_min:
                    mod_min = dist
                    index_boule_min = i

            if index_boule_min != -1:
                self.dist_min = round(mod_min, 2)
                self.equipe_plus_proche = self.boules[index_boule_min].equipe
        else:
            self.dist_min = 0.0
            self.equipe_plus_proche = None

    def safe_destroy(self):
        self.play = False
        # Fermer la fenêtre secondaire
        self.alt_window.destroy()
        # Fermer la principale
        self.destroy()

def main():
    game = Jeu()
    game.mainloop()

if __name__ == '__main__':
    main()