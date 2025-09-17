import tkinter as tk
from itertools import combinations
from math import sqrt, atan2, sin, cos, pi
from time import time
from multiprocessing import Process

from Boule_simple import Boule


class Jeu(tk.Tk):

    def __init__(self):
        super().__init__()

        """definitions des parametres graphiques"""
        self.images_secondes = 200
        self.delay = 1 / self.images_secondes
        self.inital_time = time()

        """Definir la taille du terrain"""
        self.dim_terrain = [5, 10]  # dimensions en metres du terrain
        self.metre = 80  # 1m = 80 pixels

        """Placer et titrer la fenetre au centre de l'écran"""
        self.dim_fentre = [self.metre * dim for dim in self.dim_terrain]
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.dim_fentre[0] // 2)
        y = (screen_height // 2) - (self.dim_fentre[1] // 2) - 20
        self.geometry(f"{self.dim_fentre[0]}x{self.dim_fentre[1]}+{x}+{y}")
        self.title('Pétanque')

        """Création du canvas dans lequel on va dessiner les boules"""
        self.canvas = tk.Canvas(bg='beige')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        """Création des boules"""
        # self.boules = [Boule(self, 300, 100, 0, 20, 'white'),
        #                Boule(self, 300, 200, 0, 20, 'white'),
        #                Boule(self, 300, 300, 0, 20, 'white'),
        #                Boule(self, 300, 400, 0, 20, 'white'),
        #                Boule(self, 300, 500, 0, 20, 'white'),
        #                Boule(self, 300, 600, 0, 20, 'white'),]

        self.boules = [Boule(self, 300, i * 800 // 500, 0, 5, 'white') for i in range(1, 500)]

        self.couples_a_tester_comb = combinations([i for i in range(len(self.boules))], 2)
        self.couples_a_tester = [comb for comb in self.couples_a_tester_comb]

        """Lancement de l'actualisation de la fenetre"""
        self.update_game()

    def update_positions_boules(self):
        if time() - self.inital_time > self.delay:
            for boule in self.boules:
                boule.x += self.delay * boule.speed_x
                boule.y += self.delay * boule.speed_y
                boule.update_pos()
            self.inital_time = time()

    def detecter_collisons_bord(self):
        for boule in self.boules:
            if boule.x - boule.radius <= 0:
                boule.x = boule.radius + 1
                boule.speed_x *= -1
            elif boule.x + boule.radius >= self.dim_fentre[0]:
                boule.x = self.dim_fentre[0] - boule.radius - 1
                boule.speed_x *= -1
            if boule.y - boule.radius <= 0:
                boule.y = boule.radius + 1
                boule.speed_y *= -1
            elif boule.y + boule.radius >= self.dim_fentre[1]:
                boule.y = self.dim_fentre[1] - boule.radius - 1
                boule.speed_y *= -1

    def detecter_collisions_entre_boules(self):
        for couple in self.couples_a_tester:
            boule1 = self.boules[couple[0]]
            boule2 = self.boules[couple[1]]

            """calcul de la distance entre les boules"""
            dx = boule1.x - boule2.x
            dy = boule1.y - boule2.y
            distance = sqrt(dx ** 2 + dy ** 2)
            rayon_total = boule1.radius + boule2.radius

            """cas de la collision"""
            if distance < rayon_total:
                depassement = rayon_total - distance
                angle = atan2(dy, dx)

                boule1.x += cos(angle) * depassement / 2
                boule1.y += sin(angle) * depassement / 2
                boule2.x -= cos(angle) * depassement / 2
                boule2.y -= sin(angle) * depassement / 2

                # Vitesses initiales
                v1 = sqrt(boule1.speed_x ** 2 + boule1.speed_y ** 2)
                v2 = sqrt(boule2.speed_x ** 2 + boule2.speed_y ** 2)

                # Directions initiales
                dir1 = atan2(boule1.speed_y, boule1.speed_x)
                dir2 = atan2(boule2.speed_y, boule2.speed_x)

                # Calcul des nouvelles vitesses en fonction de l'angle de collision
                vx1 = v2 * cos(dir2 - angle)
                vy1 = v1 * sin(dir1 - angle)
                vx2 = v1 * cos(dir1 - angle)
                vy2 = v2 * sin(dir2 - angle)

                # Appliquer les nouvelles vitesses en prenant en compte l'angle de collision
                boule1.speed_x = vx1 * cos(angle) + vy1 * cos(angle + pi / 2)
                boule1.speed_y = vx1 * sin(angle) + vy1 * sin(angle + pi / 2)
                boule2.speed_x = vx2 * cos(angle) + vy2 * cos(angle + pi / 2)
                boule2.speed_y = vx2 * sin(angle) + vy2 * sin(angle + pi / 2)

    def update_game(self):

        self.update_positions_boules()
        self.detecter_collisons_bord()
        self.detecter_collisions_entre_boules()

        self.after(1, self.update_game)


def main():

    game = Jeu()

    p1 = Process(target=game.mainloop())

    p1.start()
    p1.join()


if __name__ == '__main__':
    main()
