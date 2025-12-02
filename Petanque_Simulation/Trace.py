from math import sqrt, sin, atan2, cos, pi
import tkinter as tk
from typing import Optional, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from main import Jeu

class Trace:
    def __init__(self, master: 'Jeu', lancer_coeff: float):

        self.master = master
        
        # Position de départ du tracé (la position du joueur)
        self.start_x_px = self.master.start_xm * self.master.metre
        self.start_y_px = (self.master.dim_terrain[1] - self.master.start_ym) * self.master.metre
        
        self.line_id: Optional[int] = None
        self.contact_point_id: Optional[int] = None

        self.master.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.master.canvas.bind("<B1-Motion>", self.update_line)
        self.master.canvas.bind("<ButtonRelease-1>", self.end_draw)

        self.x_final_m: float = 0.0
        self.y_final_m: float = 0.0
        self.coeff_lancer = lancer_coeff

    def start_draw(self, event):
        # On ne peut tracer que si le jeu attend un lancer (self.master.jouer est True)
        # Note: dans votre logique 'jouer' semble dire "le jeu tourne", 
        # ici j'assume qu'on peut toujours tracer tant que le jeu n'est pas fini.
        if self.master.play: 
            self.line_id = self.master.canvas.create_line(
                self.start_x_px, self.start_y_px, event.x, event.y, fill="blue"
            )

    def calc_speeds(self, event) -> Tuple[float, float, float]:
        # Conversion position souris en mètres
        self.x_final_m = event.x / self.master.metre
        self.y_final_m = (self.master.dim_terrain[1] - event.y / self.master.metre)

        # Distance et Angle du vecteur tracé par la souris
        dx = self.x_final_m - self.master.start_xm
        dy = self.y_final_m - self.master.start_ym
        
        angle_principal = atan2(dx, dy)
        
        # La vitesse est proportionnelle à la longueur du trait
        dist_souris = sqrt(dx ** 2 + dy ** 2)
        speed = dist_souris * self.coeff_lancer

        # Projection 3D
        # speed_z est la composante verticale (cloche)
        # speed_x/y sont les composantes au sol
        speed_x = sin(angle_principal) * speed * cos(self.master.drop_angle)
        speed_y = cos(angle_principal) * speed * cos(self.master.drop_angle)
        speed_z = speed * sin(self.master.drop_angle)

        return speed_x, speed_y, speed_z

    def update_line(self, event):
        if not self.master.play: return

        if self.line_id is None:
            self.line_id = self.master.canvas.create_line(
                self.start_x_px, self.start_y_px, event.x, event.y, fill="blue"
            )
        else:
            self.master.canvas.coords(
                self.line_id, self.start_x_px, self.start_y_px, event.x, event.y
            )

        # Calcul prédictif de l'impact
        speed_x, speed_y, speed_z = self.calc_speeds(event)

        # Équation physique : z(t) = -0.5*g*t^2 + v_z*t + h
        # On cherche t quand z=0. Delta = b^2 - 4ac
        discriminant = speed_z ** 2 + 2 * self.master.gravity * self.master.hauteur_bonhomme
        
        if discriminant >= 0:
            t_impact = (speed_z + sqrt(discriminant)) / self.master.gravity

            x_impact_m = self.master.start_xm + speed_x * t_impact
            y_impact_m = self.master.start_ym + speed_y * t_impact

            x_impact_px = x_impact_m * self.master.metre
            y_impact_px = (self.master.dim_terrain[1] - y_impact_m) * self.master.metre

            point_radius = 5

            if self.contact_point_id is None:
                self.contact_point_id = self.master.canvas.create_oval(
                    x_impact_px - point_radius, y_impact_px - point_radius,
                    x_impact_px + point_radius, y_impact_px + point_radius,
                    fill='red', outline='red'
                )
            else:
                self.master.canvas.coords(
                    self.contact_point_id,
                    x_impact_px - point_radius, y_impact_px - point_radius,
                    x_impact_px + point_radius, y_impact_px + point_radius
                )

    def end_draw(self, event):
        if not self.master.play: return

        if self.line_id is not None:
            self.master.canvas.delete(self.line_id)
            self.line_id = None
        
        if self.contact_point_id is not None:
            self.master.canvas.delete(self.contact_point_id)
            self.contact_point_id = None

        speed_x, speed_y, speed_z = self.calc_speeds(event)
        self.master.lancer_boule(speed_x, speed_y, speed_z)