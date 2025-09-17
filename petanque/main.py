import tkinter as tk
from itertools import combinations
from math import sqrt, atan2, sin, cos, pi
from multiprocessing import Process
from time import time


from Boule import Boule
from Trace import Trace


class Jeu(tk.Tk):

    def __init__(self):
        super().__init__()

        self.alt = ...

        """definitions des parametres graphiques"""
        self.images_secondes = 100
        self.delay = 1 / self.images_secondes
        self.inital_time = time()

        """Definir la taille du terrain"""
        self.dim_terrain = [5, 10]  # dimensions en metres du terrain
        self.metre = 80  # 1m = 80 pixels

        """Placer et titrer la fenetre au centre de l'écran"""
        self.dim_fentre = [self.metre * dim for dim in self.dim_terrain]
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - 2 * (self.dim_fentre[0] // 2)
        y = (screen_height // 2) - (self.dim_fentre[1] // 2) - 20
        self.geometry(f"{self.dim_fentre[0]}x{self.dim_fentre[1]}+{x}+{y}")
        self.title('Pétanque')

        """Création du canvas dans lequel on va dessiner les boules"""
        self.canvas = tk.Canvas(self, bg='beige')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.legend_team = self.canvas.create_text(82, 784, text=f"Equipe la plus proche : ")
        self.legend_dist = self.canvas.create_text(350, 784, text=f"Distance : ")

        """Création des boules"""
        self.len_boules = 0
        self.couples_a_tester = None
        self.couples_a_tester_comb = None

        """Alternance des équipes"""

        self.jouer = True
        self.equipe_plus_proche = None
        self.dist_min = None
        self.equipe_commence = 1

        self.boules = [Boule(self, 2.6, 8, 0, 'Cochonnet', None)]

        self.redefinir_combinaisons()

        self.time_avant_retest_collision = 0.1  # s

        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)
        self.play = True

        """Definitions nécessaires à la création d'une ligne de lancement"""
        self.start_xm = 2.5  # potision de lancer initiale
        self.start_ym = 1
        self.coeff = 2
        self.trace = Trace(self, self.coeff)

        """définition de l'angle de lancement"""
        self.drop_angle = 30 / 180 * pi
        self.gravity = 9.81
        self.hauteur_bonhomme = 0.6  # m

        """Lancement de l'actualisation de la fenetre"""
        self.update_game()

    def update_legendes(self):
        self.canvas.itemconfig(self.legend_team, text=f"Equipe la plus proche : {self.equipe_plus_proche}")
        self.canvas.itemconfig(self.legend_dist, text=f"Distance : {self.dist_min} (m)")

    def redefinir_combinaisons(self):

        if len(self.boules) != self.len_boules:
            self.couples_a_tester_comb = combinations([i for i in range(len(self.boules))], 2)
            self.couples_a_tester = [comb for comb in self.couples_a_tester_comb]

            self.len_boules = len(self.boules)

    def update_positions_boules(self):
        delay = time() - self.inital_time
        if delay > self.delay:
            for boule in self.boules:

                boule.xm += delay * boule.speed_xm
                boule.ym += delay * boule.speed_ym

                boule.speed_zm -= delay * self.gravity

                if boule.z > 0:
                    boule.zm += delay * boule.speed_zm
                    boule.radius = boule.initial_radius * (1 + boule.zm)
                else:
                    boule.radius = boule.initial_radius
                    boule.speed_zm = 0
                    boule.zm = 0

                if boule.zm == 0:

                    speed = sqrt(boule.speed_xm ** 2 + boule.speed_ym ** 2)
                    angle = atan2(boule.speed_xm, boule.speed_ym)
                    speed -= boule.mu * self.gravity * delay
                    speed = max(speed, 0)

                    boule.speed_xm = speed * sin(angle)
                    boule.speed_ym = speed * cos(angle)

                    if boule.speed_ym < 0.05:
                        boule.speed_ym = 0

                boule.update_pos()

            self.inital_time = time()

    def detecter_collisons_bord(self):
        for boule in self.boules:
            boule.metre_to_pixels()

            if boule.xm - boule.radius_m <= 0:
                boule.xm = boule.radius_m + 0.01
                boule.speed_xm *= -1


            elif boule.xm + boule.radius_m >= self.dim_terrain[0]:
                boule.xm = self.dim_terrain[0] - boule.radius_m - 0.01
                boule.speed_xm *= -1

            elif boule.ym + boule.radius_m >= self.dim_terrain[1]:
                self.canvas.delete(boule.dessin)
                del boule

    def detecter_collisions_entre_boules(self):
        for couple in self.couples_a_tester:

            boule1 = self.boules[couple[0]]
            boule2 = self.boules[couple[1]]
            boule1.metre_to_pixels()
            boule2.metre_to_pixels()
            if boule1.just_decal is False and boule2.just_decal is False:

                """Calcul de la distance entre les boules"""
                dx = boule1.xm - boule2.xm
                dy = -boule1.ym + boule2.ym
                distance = sqrt(dx ** 2 + dy ** 2)
                rayon_total = boule1.radius_m + boule2.radius_m

                """Cas de la collision"""
                if distance < rayon_total and boule1.zm == 0 and boule2.zm == 0:
                    depassement = rayon_total - distance
                    angle = atan2(dy, dx)

                    tolerance = 0.01
                    boule1.xm += cos(angle) * (depassement / 2 + tolerance)
                    boule1.ym += sin(angle) * (depassement / 2 + tolerance)
                    boule2.xm -= cos(angle) * (depassement / 2 + tolerance)
                    boule2.ym -= sin(angle) * (depassement / 2 + tolerance)

                    boule1.decale(self.time_avant_retest_collision)
                    boule2.decale(self.time_avant_retest_collision)

                    # Conversion des vitesses initiales dans le référentiel parallèle à la collision
                    v1_initial = boule1.speed_xm * cos(angle) + boule1.speed_ym * sin(angle)
                    v2_initial = boule2.speed_xm * cos(angle) + boule2.speed_ym * sin(angle)

                    # Conservation des composantes perpendiculaires (non affectées par la collision)
                    v1_perp = -boule1.speed_xm * sin(angle) + boule1.speed_ym * cos(angle)
                    v2_perp = -boule2.speed_xm * sin(angle) + boule2.speed_ym * cos(angle)

                    # Calcul des vitesses finales sur l'axe de collision (équations de conservation)
                    masse1, masse2 = boule1.mass, boule2.mass
                    v1_final = (v1_initial * (masse1 - masse2) + 2 * masse2 * v2_initial) / (masse1 + masse2)
                    v2_final = (v2_initial * (masse2 - masse1) + 2 * masse1 * v1_initial) / (masse1 + masse2)

                    # Conversion des vitesses finales en composantes cartésiennes
                    boule1.speed_xm = - v1_final * cos(angle) + v1_perp * sin(angle)
                    boule1.speed_ym = v1_final * sin(angle) + v1_perp * cos(angle)
                    boule2.speed_xm = - v2_final * cos(angle) + v2_perp * sin(angle)
                    boule2.speed_ym = v2_final * sin(angle) + v2_perp * cos(angle)

    def lancer_boule(self, speed_x, speed_y, speed_z):

        if self.equipe_plus_proche is None:
            boule = Boule(self, self.start_xm, self.start_ym, self.hauteur_bonhomme, 'Boule', self.equipe_commence)

        else:
            if self.equipe_plus_proche == 1:
                boule = Boule(self, self.start_xm, self.start_ym, self.hauteur_bonhomme, 'Boule', 2)
            elif self.equipe_plus_proche == 2:
                boule = Boule(self, self.start_xm, self.start_ym, self.hauteur_bonhomme, 'Boule', 1)

        boule.speed_xm = speed_x
        boule.speed_ym = speed_y
        boule.speed_zm = speed_z

        self.boules.append(boule)

    def update_game(self):

        if self.play:

            self.update_positions_boules()
            self.detecter_collisons_bord()
            self.detecter_collisions_entre_boules()
            self.redefinir_combinaisons()
            self.calcul_plus_proche()

            self.jouer = True

            if len(self.boules) > 1:
                self.update_legendes()

            self.after(10, self.update_game)

    def calcul_plus_proche(self):

        if len(self.boules) != 0:
            mod_min = 100
            index_boule_min = 0

            pos_cochonnet = (self.boules[0].xm, self.boules[0].ym)

            for i, boule in enumerate(self.boules):
                if i != 0:
                    pos_boule = (boule.xm, boule.ym)
                    mod = sqrt((pos_cochonnet[0] - pos_boule[0]) ** 2 + (pos_cochonnet[1] - pos_boule[1]) ** 2)
                    if mod < mod_min:
                        mod_min = mod
                        index_boule_min = i

            self.dist_min = round(mod_min, 2)
            self.equipe_plus_proche = self.boules[index_boule_min].equipe


        else:
            self.dist_min = 0
            self.equipe_plus_proche = None

    def safe_destroy(self):
        self.play = False

        self.alt.safe_destroy()

        self.after(50, self.destroy)


class Altitude(tk.Tk):
    def __init__(self, master):
        super().__init__()

        self.master = master

        self.jouer = True

        self.dim_graphe = [10, 2]  # longueur, hauteur
        self.metre = 60
        self.dim_fenetre = [x * self.metre for x in self.dim_graphe]
        self.title('Altitude')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) + 50
        y = (screen_height // 2) - (self.dim_fenetre[1] // 2)
        self.geometry(f"{self.dim_fenetre[0]}x{self.dim_fenetre[1]}+{x}+{y}")

        self.dessin_boule = None
        self.boule_initiale = self.master.boules[-1]
        self.traj_dessin = []

        self.canvas2 = tk.Canvas(self, bg='white')
        self.canvas2.pack(fill=tk.BOTH, expand=True)

        self.coords = (0, 0)

        self.protocol("WM_DELETE_WINDOW", self.quitter)

        self.update_game()

    def creer_boule(self):
        boule = self.master.boules[-1]

        for draw in self.traj_dessin:
            self.canvas2.delete(draw)

        self.traj_dessin = []

        boule_x = boule.ym * self.metre
        boule_y = self.dim_fenetre[1] - boule.zm * self.metre

        self.coords = (boule_x, boule_y)

        radius = boule.radius_m * self.metre
        self.dessin_boule = self.canvas2.create_oval(boule_x - radius, boule_y - 2 * radius, boule_x + radius,
                                                     boule_y, fill=boule.color, outline='black')

    def move_boule(self):
        boule = self.master.boules[-1]

        boule_x = boule.ym * self.metre
        boule_y = self.dim_fenetre[1] - boule.zm * self.metre

        radius = boule.radius_m * self.metre

        self.canvas2.coords(self.dessin_boule, boule_x - radius, boule_y - 2 * radius - 3, boule_x + radius,
                            boule_y - 3)

        if len(self.master.boules) > 1:
            self.traj_dessin.append(
                self.canvas2.create_line(self.coords[0], self.coords[1] - 2 * radius + 3, boule_x, boule_y - 2 * radius + 3,
                                         fill='black'))

        self.coords = (boule_x, boule_y)

    def update_game(self):

        if self.jouer:
            if self.master.boules[-1] != self.boule_initiale:
                self.canvas2.delete(self.dessin_boule)
                self.creer_boule()

                self.boule_initiale = self.master.boules[-1]

            self.move_boule()
            self.after(10, self.update_game)

    def safe_destroy(self):
        self.jouer = False
        self.after(50, self.destroy)

    def quitter(self):
        self.master.safe_destroy()
        self.safe_destroy()


def main():
    game = Jeu()
    alt = Altitude(game)
    game.alt = alt

    p1 = Process(target=game.mainloop())
    p2 = Process(target=alt.mainloop())

    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == '__main__':
    main()
