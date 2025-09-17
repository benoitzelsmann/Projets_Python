import threading


class Boule:
    """Les cooredonnées d'entree sont en metres dans le terrain à partir d'en bas à gauche"""

    def __init__(self, master, x, y, z, type_boule, equipe):

        self.master = master

        self.equipe = equipe

        self.xm = x
        self.ym = y
        self.zm = z

        self.x = 0
        self.y = 0
        self.z = 0

        self.speed_xm = 0
        self.speed_ym = 0
        self.speed_zm = 0

        self.just_decal = False

        self.metre_to_pixels()

        if type_boule == 'Boule':

            self.mu = 0.4

            """définition de la taille, masse et couleur d'une boule (7.5cm, 650g et gris)"""
            self.radius_m = 0.075

            self.radius = self.radius_m * self.master.metre
            self.initial_radius = self.radius

            self.mass = 0.650

            self.color = "grey"

            self.coeff_amorti = 1  # m/s²

        elif type_boule == 'Cochonnet':

            self.mu = 0.8

            """définition de la taille, masse et couleur du cochonnet (3cm, 15g et gris)"""
            self.radius_m = 0.03

            self.radius = self.radius_m * self.master.metre
            self.initial_radius = self.radius

            self.mass = 0.015

            self.color = "black"

            self.coeff_amorti = 5  # m/s²

        if equipe == 1:
            self.color = "red"
        else:
            self.color = "blue"

        """Index de la boule dans le canvas"""
        self.dessin = None

        """initialisation de la boule"""
        self.draw()

    def metre_to_pixels(self):
        self.x = self.xm * self.master.metre
        self.y = (self.master.dim_terrain[1] - self.ym) * self.master.metre
        self.z = self.zm * self.master.metre

    def draw(self):
        self.dessin = self.master.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius,
                                                     self.y + self.radius, fill=self.color, outline='black')

    def update_pos(self):
        self.metre_to_pixels()
        self.master.canvas.coords(self.dessin, self.x - self.radius, self.y - self.radius, self.x + self.radius,
                                  self.y + self.radius)

    def decale(self, time):
        self.just_decal = True
        timer = threading.Timer(time, self.non_decale)
        timer.start()

    def non_decale(self):
        self.just_decal = False
