from itertools import permutations


class Sudokusolver:

    def __init__(self):
        self.size = 9

        self.numero_grille = 1

        self.grille_initiale_1 = [[0, 0, 8, 1, 0, 0, 2, 9, 0],
                                  [0, 0, 0, 0, 4, 2, 0, 0, 0],
                                  [1, 0, 0, 3, 0, 0, 5, 0, 6],
                                  [0, 0, 0, 0, 0, 0, 6, 0, 0],
                                  [9, 3, 0, 0, 0, 0, 0, 1, 5],
                                  [0, 0, 1, 0, 0, 0, 0, 0, 0],
                                  [5, 0, 3, 0, 0, 6, 0, 0, 9],
                                  [0, 0, 0, 2, 8, 0, 0, 0, 0],
                                  [0, 8, 9, 0, 0, 5, 1, 0, 0]]

        self.grille_initiale_2 = [[0, 0, 0, 4, 0, 0, 8, 7, 0],
                                  [0, 4, 7, 0, 9, 2, 0, 5, 0],
                                  [2, 0, 0, 6, 0, 0, 0, 3, 0],
                                  [9, 7, 0, 5, 0, 0, 2, 0, 3],
                                  [5, 0, 8, 0, 2, 4, 7, 0, 6],
                                  [6, 0, 4, 0, 0, 7, 0, 8, 5],
                                  [0, 9, 0, 3, 0, 8, 0, 0, 7],
                                  [0, 0, 3, 2, 4, 0, 1, 6, 0],
                                  [0, 1, 2, 0, 0, 0, 0, 9, 0]]

        self.grille_initiale_3 = [[0 for i in range(9)] for j in range(9)]

        self.grille = [self.grille_initiale_1, self.grille_initiale_2, self.grille_initiale_3][self.numero_grille]

        self.grille_initiale = [[j for j in x] for x in self.grille]

        self.lignes_possibles = [[] for i in range(9)]
        self.combinaisons_testees = [[] for i in range(9)]

    def check_columns_2(self):
        for i in range(9):
            column = [self.grille[k][i] for k in range(9)]
            if len(column) != len(set(column)):
                return False
        return True

    @staticmethod
    def check_columns(grille):
        for i in range(9):
            column = [grille[k][i] for k in range(9)]
            if len(column) != len(set(column)):
                return False
        return True

    def calcul_possiblilites(self):

        for n, line in enumerate(self.grille):

            elements_in_line = [a for a in line if a != 0]

            elements = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            elements_a_placer = [x for x in elements if x not in elements_in_line]

            elements_possibles = [list(line_s) for line_s in permutations(elements_a_placer)]

            for elements in elements_possibles:
                new_line = []
                for i in range(9):
                    if line[i] == 0:
                        new_line.append(elements.pop())
                    else:
                        new_line.append(line[i])

                possible = True
                for k, element in enumerate(new_line):
                    if line[k] == 0:
                        if element in [self.grille[b][k] for b in range(9)]:
                            possible = False

                if possible:
                    self.lignes_possibles[n].append(new_line)

    def calcul_possibilites_2(self, index):

        lignes_possibles = []
        elements_in_line = [a for a in self.grille[index] if a != 0]
        elements = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        elements_a_placer = [x for x in elements if x not in elements_in_line]

        for elements_permutation in permutations(elements_a_placer):
            new_line = []
            element_iter = iter(elements_permutation)
            for i in range(9):
                if self.grille[index][i] == 0:
                    new_line.append(next(element_iter))
                else:
                    new_line.append(self.grille[index][i])

            possible = True
            for k, element in enumerate(new_line):
                if self.grille[index][k] == 0:
                    if element in [self.grille[b][k] for b in range(9)]:
                        possible = False

            if possible:
                lignes_possibles.append(new_line)

        return lignes_possibles

    def remplir_grille(self):

        grille = [[] for i in range(9)]
        indexes = [0 for i in range(9)]

        for a, line0 in enumerate(self.lignes_possibles[0]):
            grille[0] = line0

            for b, line1 in enumerate(self.lignes_possibles[1]):
                grille[1] = line1
                for c, line2 in enumerate(self.lignes_possibles[2]):
                    grille[2] = line2
                    for d, line3 in enumerate(self.lignes_possibles[3]):
                        grille[3] = line3
                        for e, line4 in enumerate(self.lignes_possibles[4]):
                            grille[4] = line4
                            for f, line5 in enumerate(self.lignes_possibles[5]):
                                grille[5] = line5
                                for g, line6 in enumerate(self.lignes_possibles[6]):
                                    grille[6] = line6
                                    for h, line7 in enumerate(self.lignes_possibles[7]):
                                        grille[7] = line7
                                        for i, line8 in enumerate(self.lignes_possibles[8]):
                                            grille[8] = line8
                                            var = self.check_columns(grille)

                                            if var:
                                                indexes = [a, b, c, d, e, f, g, h]

        for i, index in enumerate(indexes):
            print(self.lignes_possibles[i][index])

    def remplir_grille_recursif(self, index):

        if index == 9:
            if self.check_columns_2():
                return True
            else:
                return False

        calc = self.calcul_possibilites_2(index)

        if len(calc) > 0:

            for line in calc:

                self.grille[index] = line.copy()
                if self.remplir_grille_recursif(index + 1):
                    return True
                self.grille[index] = self.grille_initiale[index].copy()

        return False


def main():
    sudoku = Sudokusolver()

    sudoku.remplir_grille_recursif(0)
    for line in sudoku.grille:
        print(line)


if __name__ == "__main__":
    main()
