from Eval import Eval
from Fen import Fen
from Fuctions import case_to_index
from Movement import Movement
from Rules import cases_names, initial_position


class Engine:
    """
    Classe principale du moteur d'échecs qui gère la logique du jeu, l'évaluation des positions,
    et l'algorithme de recherche du meilleur coup.

    Cette classe intègre les modules d'évaluation, de gestion des mouvements et de notation FEN.
    Elle implémente l'algorithme Alpha-Beta avec recherche quiescente pour trouver les meilleurs coups.
    """
    def __init__(self):
        """
        Initialise le moteur d'échecs avec ses composants et paramètres par défaut.

        Initialise les modules d'évaluation, de mouvement et de notation FEN.
        Configure la profondeur de recherche, le plateau initial et les variables d'état du jeu.
        """

        self.Eval = Eval(self)
        self.Movement = Movement(self)

        self.depth = 4
        self.qs_depht = 0

        self.positions_transposition = {}

        """FEN"""
        self.Fen = Fen(self)

        self.fen_position = ("r6k/"
                             "8/"
                             "8/"
                             "8/"
                             "4PP2/"
                             "6PP/"
                             "r5BK/"
                             "8"
                             " w - - 1 41")

        self.fen_pos_test_mate = "k7/8/r3Q3/8/8/8/4PPP1/5K2 w - - 0 1"
        self.fen_pos_mate = "6K1/8/8/7q/7k/8/8/8 w - - 1 41"
        self.chek_board = "r1bqkbnr/pppp2pp/8/5P1Q/2Bp4/8/PPPP1PPP/RNB1K2R w KQkq - 0 7"
        self.fen_1 = "8/p6p/1k6/3r4/1P6/n6P/6P1/2R3K1 w - - 0 35"
        self.fen_2 = "4k3/8/5PP1/5K2/8/8/8/8 w - - 0 1"
        self.fen_knight_prom = "3n2nr/4Pqpp/2k5/8/8/8/2B3PP/6K1 w - - 0 1"

        self.board = [row[:] for row in initial_position]

        """Real"""
        self.wk_has_moved = False
        self.wrr_has_moved = False
        self.wrl_has_moved = False
        self.bk_has_moved = False
        self.brr_has_moved = False
        self.brl_has_moved = False
        self.wk_castle = False
        self.bk_castle = False



        self.last_move = None

        self.wk_pos = (7, 4)
        self.bk_pos = (0, 4)

        # self.Fen.get_board_from_fen(self.fen_1)

    def reset(self):
        """
        Réinitialise l'état du jeu à sa configuration de départ.

        Remet le plateau à sa position initiale, réinitialise les indicateurs de roque,
        les positions des rois et efface l'historique des coups.
        """
        self.board = [row[:] for row in initial_position]
        self.wk_has_moved = False
        self.wrr_has_moved = False
        self.wrl_has_moved = False
        self.bk_has_moved = False
        self.brr_has_moved = False
        self.brl_has_moved = False
        self.wk_castle = False
        self.bk_castle = False

        self.last_move = None

        self.wk_pos = (7, 4)
        self.bk_pos = (0, 4)

    def set_depth(self, depth):
        """
        Définit la profondeur de recherche pour l'algorithme Alpha-Beta.

        Args:
            depth (int): La profondeur de recherche à utiliser.
        """
        self.depth = depth


    def show_board(self):
        """
        Affiche l'état actuel du plateau d'échecs dans la console.

        Chaque ligne du plateau est affichée avec les pièces séparées par des espaces.
        """
        for row in self.board:
            print(' '.join(row))

    def test_move(self, color, move_case):
        """
        Teste si un mouvement est valide et retourne l'objet Move correspondant.

        Args:
            color (str): La couleur du joueur ('w' pour blanc, 'b' pour noir).
            move_case (str): Le mouvement au format algébrique (ex: "e2e4").

        Returns:
            Move ou list: L'objet Move si un seul mouvement est possible, 
                         ou une liste de mouvements possibles si plusieurs options existent.
        """
        index1 = case_to_index(move_case[0:2])
        index2 = case_to_index(move_case[2:4])


        moves_possibles = self.Movement.find_all_possible_moves(color, self.last_move)



        moves_playable = []
        for move_test in moves_possibles:
            if move_test.start == index1 and move_test.end == index2:
                moves_playable.append(move_test)

        if len(moves_playable) == 1:
            return moves_playable[0]
        else:
            return moves_playable

    def moves_possibles_case(self, case, player_color):
        """
        Détermine tous les mouvements possibles pour une pièce sur une case donnée.

        Args:
            case (str): La case en notation algébrique (ex: "e2").
            player_color (str): La couleur du joueur ('w' pour blanc, 'b' pour noir).

        Returns:
            list: Liste des cases cibles possibles avec leurs spécificités (capture, promotion, etc.).
                 Retourne une liste vide si la case est vide ou si aucun mouvement n'est possible.
        """
        pos = case_to_index(case)
        if self.board[pos[0]][pos[1]] == 0:
            return []

        moves_possibles = self.Movement.moves_possible_by_a_piece(pos, self.last_move, player_color)

        cases_possibles = []

        for move in moves_possibles:
            c, d = move.end
            typ = move.specificity
            case_target = cases_names[c][d]
            cases_possibles.append((case_target, typ))

        return cases_possibles

    def get_what_is_on_square(self, case):
        """
        Retourne la pièce présente sur une case donnée.

        Args:
            case (str): La case en notation algébrique (ex: "e2").

        Returns:
            int: Le caractère représentant la pièce sur la case ('.' pour une case vide).
        """
        (i, j) = case_to_index(case)
        return self.board[i][j]


    def ajust_depth(self):
        """
        Ajuste automatiquement la profondeur de recherche en fonction du nombre de pièces restantes sur le plateau.

        La profondeur augmente à mesure que le nombre de pièces diminue, permettant une recherche plus profonde
        dans les fins de partie où il y a moins de possibilités à explorer.
        """
        num_pieces = sum(1 for row in self.board for piece in row if piece != '.')


        if 33 > num_pieces > 7:  # Phase d'ouverture (beaucoup de pièces)
            self.depth = 5
        elif 7 >= num_pieces > 4:  # Phase médiane
            self.depth = 7
        else:
            self.depth = 9

    def find_best_move_cases(self, color):
        """
        Trouve le meilleur coup pour une couleur donnée et le retourne en notation algébrique.

        Args:
            color (str): La couleur du joueur ('w' pour blanc, 'b' pour noir).

        Returns:
            tuple: Un tuple contenant (coup_en_notation_algébrique, objet_move) ou (None, None) si aucun coup n'est possible.
        """
        # depth_mem = self.depth
        #
        # self.ajust_depth()
        #
        # if self.depth != depth_mem:
        #     print(f"profondeur = {self.depth}")

        best_move = self.find_best_move(color, self.depth)

        if best_move:

            a, b = best_move.start
            c, d = best_move.end

            case1 = cases_names[a][b]
            case2 = cases_names[c][d]

            return case1 + case2, best_move

        else:
            print("fin de partie")
            return None, None

    def get_board_string(self):
        # Représente l’état du plateau sous forme de chaîne, ex : FEN simplifiée
        board_rows = []
        for row in self.board:
            board_rows.append(''.join(str(p) for p in row))
        return '/'.join(board_rows)


    def find_best_move(self, color, depth):
        color_int = 1 if color == 'w' else -1

        """
        Trouve le meilleur coup pour une couleur donnée en utilisant l'algorithme Alpha-Beta.

        Implémente l'algorithme Alpha-Beta avec recherche quiescente pour trouver le meilleur coup
        à une profondeur donnée. Utilise l'évaluation de position pour déterminer la valeur des positions.

        Args:
            color (str): La couleur du joueur ('w' pour blanc, 'b' pour noir).
            depth (int): La profondeur de recherche.

        Returns:
            Move: L'objet Move représentant le meilleur coup trouvé, ou None si aucun coup n'est possible.
        """

        def quiescence(alpha, beta, maximizing_player, last_move, depht):
            """
            Recherche Quiescente : explore les positions calmes pour éviter les évaluations erronées.

            Cette fonction continue la recherche au-delà de la profondeur normale pour les positions
            instables (avec des captures possibles) afin d'obtenir une évaluation plus précise.

            Args:
                alpha (float): La meilleure valeur trouvée pour le joueur maximisant.
                beta (float): La meilleure valeur trouvée pour le joueur minimisant.
                maximizing_player (bool): True si c'est au tour du joueur maximisant (blanc).
                last_move (Move.py): Le dernier coup joué.
                depht (int): La profondeur restante pour la recherche quiescente.

            Returns:
                float: La valeur d'évaluation de la position.
            """

            # On commence par l'évaluation de la position à la profondeur actuelle
            stand_pat = self.Eval.total_adv(0)

            if depht == 0:
                return stand_pat

            if maximizing_player:
                # Recherche d'un meilleur coup pour le joueur maximisateur
                if stand_pat >= beta:
                    return stand_pat  # Coup déjà assez bon pour beta
                alpha = max(alpha, stand_pat)

                # Recherche de captures ou d'actions qui modifient la position
                moves = self.Movement.find_all_possible_moves('w' if maximizing_player else 'b', last_move)
                moves = [move for move in moves if move.specificity and "capture" in move.specificity]  # On ne considère que les captures

                for move in moves:
                    backup = self.Movement.do_move(move)
                    eval1 = quiescence(alpha, beta, False, move, depht - 1)  # Explore les captures
                    self.Movement.undo_move(backup)

                    if eval1 >= beta:
                        return eval1  # Prune
                    alpha = max(alpha, eval1)

                return alpha

            else:
                # Recherche d'un meilleur coup pour le joueur minimisateur
                if stand_pat <= alpha:
                    return stand_pat  # Coup déjà assez mauvais pour alpha
                beta = min(beta, stand_pat)

                # Recherche de captures ou d'actions qui modifient la position
                moves = self.Movement.find_all_possible_moves('w' if maximizing_player else 'b', last_move)
                moves = [move for move in moves if move.specificity and "capture" in move.specificity]

                for move in moves:
                    backup = self.Movement.do_move(move)
                    eval1 = quiescence(alpha, beta, True, move, depht - 1)  # Explore les captures
                    self.Movement.undo_move(backup)

                    if eval1 <= alpha:
                        return eval1  # Prune
                    beta = min(beta, eval1)

                return beta

        def alphabeta(depth_variable, alpha, beta, color, last_move):

            # current_color = 'w' if color == 1 else 'b'
            # key = f"{self.get_board_string()}_{current_color}"
            #
            # if key in self.positions_transposition:
            #     saved_eval, saved_move, saved_depth = self.positions_transposition[key]
            #     if saved_depth >= depth_variable:
            #         return saved_eval, saved_move

            if depth_variable == 0:
                return color * self.Eval.total_adv(), None

            best_score = float('-inf')
            best_move = None

            moves = self.Movement.find_all_possible_moves('w' if color == 1 else 'b', last_move)

            if not moves:
                if last_move is not None and last_move.gives_check != "":
                    return (-1000 - depth_variable) * color, None
                else:
                    return 0, None

            moves.sort(key=lambda m: self.Movement.move_score(m), reverse=True)

            for move in moves:
                backup = self.Movement.do_move(move)
                score, _ = alphabeta(depth_variable - 1, -beta, -alpha, -color, move)
                self.Movement.undo_move(backup)

                score = -score

                if score > best_score:
                    best_score = score
                    best_move = move

                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break

            # self.positions_transposition[key] = (best_score, best_move, depth_variable)
            return best_score, best_move

        _, move = alphabeta(depth, float('-inf'), float('inf'), color_int, self.last_move)

        return move


if __name__ == '__main__':
    pass
