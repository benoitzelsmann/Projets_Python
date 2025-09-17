from window import Window, SummaryWindow
from random import choice
import json


class Workout:


    def __init__(self):

        self.recap_exos = json.load(open('recap_exos.json', 'r', encoding='utf-8'))
        self.exos_par_zone = json.load(open('exos_par_zone.json', 'r', encoding='utf-8'))

        self.window1 = Window()
        self.window1.mainloop()

        self.difficulty = self.window1.difficulty
        self.nb_zones = self.window1.nb_zones
        self.repetitions = self.window1.repetitions
        self.window1.destroy()

        self.nb_exos_par_zone = 3

        self.zones = []
        self.exos = []
        self.workout = {}
        self.generate_workout()

        self.afficher_workout()


    def generate_workout(self):
        self.find_zones()
        self.find_exos()
        self.calculate_repetitions()

    def find_zones(self):
        zones = list(self.exos_par_zone.keys())
        zones_travail = [choice(zones) for i in range(self.nb_zones)]
        while len(zones_travail) != len(set(zones_travail)):
            zones_travail = [choice(zones) for i in range(self.nb_zones)]
        self.zones = zones_travail

    def find_exos(self):
        for zone in self.zones:
            exos = [1 for i in range(self.nb_exos_par_zone)]
            while len(exos) != len(set(exos)):
                for i in range(len(exos)):
                    exos[i] = choice(self.exos_par_zone[zone])
            for exo in exos:
                self.exos.append(exo)

    def calculate_repetitions(self):
        for exo in self.exos:
            if self.difficulty == 'Difficile':
                if self.recap_exos[exo]["repetitions"][0] is None:
                    self.workout[exo] = str(self.recap_exos[exo]["duree (s)"][1]) + ' secondes'
                else:
                    self.workout[exo] = str(self.recap_exos[exo]["repetitions"][1]) + ' repetitions'

            elif self.difficulty == 'Facile':
                if self.recap_exos[exo]["repetitions"][0] is None:
                    self.workout[exo] = str(self.recap_exos[exo]["duree (s)"][0]) + ' secondes'
                else:
                    self.workout[exo] = str(self.recap_exos[exo]["repetitions"][0]) + ' repetitions'

            elif self.difficulty == 'Moyen':
                if self.recap_exos[exo]["repetitions"][0] is None:
                    self.workout[exo] = str((self.recap_exos[exo]["duree (s)"][0] +
                                             self.recap_exos[exo]["duree (s)"][1]) // 2) + ' secondes'
                else:
                    self.workout[exo] = str((self.recap_exos[exo]["repetitions"][0] +
                                             self.recap_exos[exo]["repetitions"][1]) // 2) + ' repetitions'

    def afficher_workout(self):
        affichage = SummaryWindow(self.workout, self.repetitions)
        affichage.update()
        affichage.mainloop()




def main():
    Workout()



if __name__ == '__main__':
    main()
