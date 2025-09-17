from stockfish import Stockfish
from random import choice

# stockfish = Stockfish(path="code_source_stockfish/stockfish-windows-x86-64-avx2.exe")
#
#
# stockfish.set_position(["e2e4", "e7e6"])
# win = stockfish.get_wdl_stats()
# visu = stockfish.get_board_visual()
# stockfish.is_move_correct('a2a3')
#
# coup = stockfish.get_top_moves(3)
#
# eval = stockfish.get_evaluation()
#
# stockfish.set_elo_rating(1350)


class Game (Stockfish):

    stockfish_path = "code_source_stockfish/stockfish-windows-x86-64-avx2.exe"

    def __init__(self, initial_difficulty):
        super().__init__(path=self.stockfish_path)

        self.win = None
        self.evaluation = None
        self.best_moves = None

        self.update_engine_parameters({"UCI_Elo": initial_difficulty})

        pos_to_promote = ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1c4', 'g8f6', 'd2d3', 'h7h6', 'b1c3', 'd7d6', 'c1e3', 'a7a6', 'e1g1', 'b7b5', 'c4b3', 'c6a5', 'a2a4', 'b5b4', 'c3d5', 'a5b3', 'c2b3', 'a6a5', 'd5f6', 'd8f6', 'd1c2', 'c7c5', 'd3d4', 'e5d4', 'f3d4', 'f8e7', 'd4c6', 'c8a6', 'c6e7', 'e8e7', 'f1e1', 'a8c8', 'a1d1', 'h8d8', 'f2f4', 'e7f8', 'e4e5', 'f6g6', 'c2g6', 'f7g6', 'e5d6', 'd8d7', 'e3c5', 'f8f7', 'e1e7', 'd7e7', 'd6e7', 'c8c5']

        self.make_moves_from_current_position([])

        self.get_board()


    def get_board(self):
        liste = list(self.get_board_visual())
        indexes = []
        for i, charachter in enumerate(liste):
            if charachter == '\n':
                indexes.append(i+1)

        liste = [liste[indexes[i]:indexes[i+1]] for i in range(len(indexes)-1)]
        liste.pop(-1)

        for sous_liste in liste:
            for element in ['-', '+', '\n', '|']:
                while element in sous_liste:
                    sous_liste.remove(element)
        while [] in liste:
            liste.remove([])

        for sous_liste in liste:
            sous_liste.pop(0)
            sous_liste.pop(-1)

        for sous_liste in liste:
            i = 1
            while i < len(sous_liste):
                sous_liste.pop(i)
                sous_liste.pop(i)
                i += 1

        for sous_liste in liste:
            for a, letter in enumerate(sous_liste):
                if letter == ' ':
                    sous_liste[a] = None
                else:
                    if letter.isupper():
                        sous_liste[a] = 'w' + letter.lower()
                    else:
                        sous_liste[a] = 'b' + letter
        return liste

    def calculs_win_eval(self):
        evalu = self.get_evaluation()
        if evalu['type'] == 'cp':
            return ['cp', evalu['value']/100]
        elif evalu['type'] == 'mate':
            return ['mate', evalu['value']]
        return evalu

    def get_niv_elo(self):
        return self.get_parameters()["UCI_Elo"]

    def __str__(self):
        return self.get_board_visual()

    def set_difficulty(self, difficulty):
        self.update_engine_parameters({"UCI_Elo": difficulty})

    def move_piece(self, move):
        if self.test_move(move):
            self.make_moves_from_current_position([move])
        else:
            print("coup impossible")

    def test_move(self, move):
        if self.is_move_correct(move):
            return True

    def test_capture(self, move):
        capture = str(self.will_move_be_a_capture(move))
        if "DIRECT_CAPTURE" in capture:
            return True
        else:
            return False

    def is_a_promotion(self, move):
        if move[-1] == "8" and move[1] == "7":
            if "PAWN" in str(self.get_what_is_on_square(move[:2])):
                return True
        return False


    def find_best_moves(self, n):
        return self.get_top_moves(n)

    def find_best_move(self):
        return self.get_best_move_time(100)


if __name__ == "__main__":
    game = Game(100)



