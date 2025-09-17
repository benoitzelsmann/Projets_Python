
from random import randint


class Boule:

    taille_terrain = 10  # m


    def __init__(self, master, x, y, z, radius, color):

        self.master = master

        self.x = x
        self.y = y
        self.z = z

        self.max_speed = 500

        self.speed_x = randint(-self.max_speed, self.max_speed)
        self.speed_y = randint(-self.max_speed, self.max_speed)
        self.speed_z = randint(-self.max_speed, self.max_speed)


        self.radius = radius

        self.color = color



        self.mass = 1

        """Index de la boule dans le canvas"""
        self.dessin = None

        """initialisation de la boule"""
        self.draw()

    def draw(self):
        self.dessin = self.master.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, fill=self.color, outline='black')

    def update_pos(self):
        self.master.canvas.coords(self.dessin,self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius,)



#
# self.move_boule()
#
#
#
#
#     def move_boule(self):
#         self.boule.x += 1
#         self.boule.update_pos()
#
#         if self.boule.x < 500:
#             self.after(10, self.move_boule)