import tkinter as tk
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from main import Jeu

class Boule:
    """Les coordonnées d'entrée sont en mètres dans le terrain à partir d'en bas à gauche"""

    def __init__(self, master: 'Jeu', x: float, y: float, z: float, type_boule: str, equipe: Optional[int]):

        self.master = master
        self.equipe = equipe

        # Position en mètres
        self.xm = x
        self.ym = y
        self.zm = z

        # Position en pixels
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        self.speed_xm = 0.0
        self.speed_ym = 0.0
        self.speed_zm = 0.0

        self.just_decal = False

        # Valeurs par défaut pour satisfaire le linter
        self.mu = 0.4
        self.radius_m = 0.075
        self.mass = 0.650
        self.color = "grey"
        self.coeff_amorti = 1

        if type_boule == 'Boule':
            self.mu = 0.4
            """définition de la taille, masse et couleur d'une boule (7.5cm, 650g et gris)"""
            self.radius_m = 0.075
            self.mass = 0.650
            self.color = "grey"
            self.coeff_amorti = 1  # m/s²

        elif type_boule == 'Cochonnet':
            self.mu = 0.8
            """définition de la taille, masse et couleur du cochonnet (3cm, 15g et gris)"""
            self.radius_m = 0.03
            self.mass = 0.015
            self.color = "black"
            self.coeff_amorti = 5  # m/s²

        # Conversion du rayon en pixels
        self.radius = self.radius_m * self.master.metre
        self.initial_radius = self.radius

        # Couleur de l'équipe
        if equipe == 1:
            self.color = "red"
        elif equipe == 2:
            self.color = "blue"

        """Index de la boule dans le canvas"""
        self.dessin: Optional[int] = None
        
        self.metre_to_pixels()
        """initialisation de la boule"""
        self.draw()

    def metre_to_pixels(self):
        self.x = self.xm * self.master.metre
        # Inversion de l'axe Y pour correspondre au repère Tkinter (0 en haut)
        self.y = (self.master.dim_terrain[1] - self.ym) * self.master.metre
        self.z = self.zm * self.master.metre

    def draw(self):
        self.dessin = self.master.canvas.create_oval(
            self.x - self.radius, 
            self.y - self.radius, 
            self.x + self.radius,
            self.y + self.radius, 
            fill=self.color, 
            outline='black'
        )

    def update_pos(self):
        self.metre_to_pixels()
        if self.dessin:
            self.master.canvas.coords(
                self.dessin, 
                self.x - self.radius, 
                self.y - self.radius, 
                self.x + self.radius,
                self.y + self.radius
            )

    def decale(self, time_sec):
        """Active l'immunité aux collisions pour une courte durée via Tkinter.after"""
        self.just_decal = True
        # Conversion secondes -> millisecondes pour Tkinter
        ms = int(time_sec * 1000)
        self.master.after(ms, self.non_decale)

    def non_decale(self):
        self.just_decal = False