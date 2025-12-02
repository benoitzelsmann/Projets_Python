from Fuctions import is_opponent_piece
from Move import Move
from Rules import pieces_moves


class Movement:
    """
    Class responsible for handling all aspects of chess piece movement.

    This class manages the movement of chess pieces, including finding legal moves,
    checking for checks, pins, and other chess rules, and executing moves on the board.
    """

    def __init__(self, engine):
        """
        Initialize the Movement class with a reference to the chess engine.

        Args:
            engine: The chess engine that contains the board state and game information.
        """
        self.engine = engine
        pass

    def is_castling_valid(self, name, side):
        """
        Check if castling is valid for a given king and side.

        Args:
            name (int): The piece name (e.g., 'K' for white king, 'k' for black king).
            side (str): The side to castle on ('kingside' or 'queenside').

        Returns:
            bool: True if castling is valid, False otherwise.
        """
        color = 'w' if name > 0 else 'b'

        row = 7 if color == 'w' else 0
        enemy_color = 'w' if color == 'b' else 'b'

        # Vérifie si roi ou tour ont bougé
        if color == 'w':
            if self.engine.wk_has_moved or (self.engine.wrr_has_moved if side == 'kingside' else self.engine.wrl_has_moved):
                return False

        elif color == 'b':
            if self.engine.bk_has_moved or (self.engine.brr_has_moved if side == 'kingside' else self.engine.brl_has_moved):
                return False

        # Vérifie que les cases entre roi et tour sont vides
        if side == 'kingside' and not (self.engine.board[row][5] == self.engine.board[row][6] == 0):
            return False
        if side == 'queenside' and not (self.engine.board[row][1] == self.engine.board[row][2] == self.engine.board[row][3] == 0):
            return False

        # Vérifie que le roi ne passe pas par une case attaquée
        occupied_cases = self.find_all_occupated_cases(enemy_color)
        king_positions = [(row, 4), (row, 5), (row, 6)] if side == 'kingside' else [(row, 4), (row, 3), (row, 2)]

        if any(pos in occupied_cases for pos in king_positions):
            return False

        return True

    def find_all_possible_moves(self, color, last_move):
        """
        Find all possible legal moves for a given color.

        Args:
            color (str): The color to find moves for ('w' for white, 'b' for black).
            last_move (Move): The last move made in the game, or None if it's the first move.

        Returns:
            list: A list of all possible legal moves for the given color.
        """
        possible_moves = []

        if color == "w":
            for i in range(8):
                for j in range(8):
                    name = self.engine.board[i][j]
                    if name != 0 and name > 0:
                        possible_moves.extend(self.moves_possible_by_a_piece((i, j), last_move, color))

        if color == "b":
            for i in range(8):
                for j in range(8):
                    name = self.engine.board[i][j]
                    if name != 0 and name < 0:
                        possible_moves.extend(self.moves_possible_by_a_piece((i, j), last_move, color))
        return possible_moves

    def find_all_occupated_cases(self, color):
        """
        Find all squares that are threatened or controlled by pieces of a given color.

        Args:
            color (str): The color to find threatened squares for ('w' for white, 'b' for black).

        Returns:
            set: A set of tuples (row, col) representing all squares threatened by the given color.
        """
        occupated_cases = set()
        if color == "w":
            for i in range(8):
                for j in range(8):
                    name = self.engine.board[i][j]
                    if name != 0 and name > 0:
                        for case in self.cases_taken_by_a_piece((i, j)):
                            occupated_cases.add(case)
        elif color == "b":
            for i in range(8):
                for j in range(8):
                    name = self.engine.board[i][j]
                    if name != 0 and name < 0:
                        for case in self.cases_taken_by_a_piece((i, j)):
                            occupated_cases.add(case)
        return occupated_cases


    def is_in_check(self, color):
        """
        Check if the king of a given color is in check.

        Args:
            color (str): The color of the king to check ('w' for white, 'b' for black).

        Returns:
            bool: True if the king is in check, False otherwise.
        """
        enemy_color = "w" if color == "b" else "b"

        king_pos = self.engine.wk_pos if color == "w" else self.engine.bk_pos

        if color == "w":
            for i in range(8):
                for j in range(8):
                    name = self.engine.board[i][j]
                    if name != 0 and name > 0:
                        if king_pos in self.cases_taken_by_a_piece((i, j)):
                            return True
        if color == "b":
            for i in range(8):
                for j in range(8):
                    name = self.engine.board[i][j]
                    if name != 0 and name < 0:
                        if king_pos in self.cases_taken_by_a_piece((i, j)):
                            return True

        threatened_cases = self.find_all_occupated_cases(enemy_color)

        return king_pos in threatened_cases

    def cases_taken_by_a_piece(self, position):
        """
        Find all squares that a piece can attack or control from its position.

        Args:
            position (tuple): The position (row, col) of the piece.

        Returns:
            set: A set of tuples (row, col) representing all squares the piece can attack.
        """
        board = self.engine.board
        i, j = position
        name = board[i][j]
        if name == 0:
            return set()


        moves = pieces_moves[name]

        cases_taken = set()

        if abs(name) in (300, 1):
            for dx, dy in moves:
                x, y = i + dx, j + dy
                if 0 <= x < 8 and 0 <= y < 8:
                    cases_taken.add((x, y))

        elif abs(name) == 100:
            for dx, dy in moves:
                if dy:
                    x, y = i + dx, j + dy
                    if 0 <= x < 8 and 0 <= y < 8:
                        cases_taken.add((x, y))

        elif abs(name) in (900, 325, 500):
            for dx, dy in moves:
                x, y = i, j
                while True:
                    x += dx
                    y += dy
                    if not (0 <= x < 8 and 0 <= y < 8):
                        break
                    cases_taken.add((x, y))
                    if abs(board[x][y]) == 1 and is_opponent_piece(name, board[x][y]):
                        continue
                    if board[x][y] != 0:
                        break

        return cases_taken

    def is_pinned(self, start, name, end=None):
        """
        Check if a piece is pinned (can't move because it would expose the king to check).

        Args:
            start (tuple): The starting position (row, col) of the piece.
            name (int): The name of the piece.
            end (tuple, optional): The ending position if a specific move is being checked.

        Returns:
            bool: True if the piece is pinned, False otherwise.
        """
        king_pos = self.engine.bk_pos if name < 0 else self.engine.wk_pos
        x0, y0 = start
        xk, yk = king_pos

        dx = x0 - xk
        dy = y0 - yk

        if not (dx == 0 or dy == 0 or abs(dx) == abs(dy)):
            return False

        dir_x = dx // abs(dx) if dx != 0 else 0
        dir_y = dy // abs(dy) if dy != 0 else 0

        # Vérifier qu'il n'y a rien entre le roi et la pièce
        x, y = xk + dir_x, yk + dir_y
        while (x, y) != (x0, y0):
            if not (0 <= x < 8 and 0 <= y < 8):
                return False
            if self.engine.board[x][y] != 0:
                return False
            x += dir_x
            y += dir_y

        # Depuis la pièce, chercher une menace dans la même direction
        x, y = x0 + dir_x, y0 + dir_y
        while 0 <= x < 8 and 0 <= y < 8:
            piece = self.engine.board[x][y]
            if piece == 0:
                x += dir_x
                y += dir_y
                continue
            if is_opponent_piece(name, piece):
                if abs(piece) == 900 or \
                        (abs(piece) == 500 and (dir_x == 0 or dir_y == 0)) or \
                        (abs(piece) == 325 and abs(dir_x) == abs(dir_y)):

                    # Si un déplacement est proposé, vérifier s'il reste sur la ligne
                    if end:
                        dx_move = end[0] - xk
                        dy_move = end[1] - yk
                        if dx_move == 0 and dir_x == 0:
                            return False  # reste sur la colonne
                        if dy_move == 0 and dir_y == 0:
                            return False  # reste sur la ligne
                        if abs(dx_move) == abs(dy_move) and dir_x != 0 and dir_y != 0:
                            return False  # reste sur la diagonale
                    return True  # clouage confirmé
            break  # autre pièce bloque
        return False

    def is_discovered_check(self, name, old_pos, new_pos):
        """
        Check if moving a piece would reveal a check (discovered check).

        Args:
            name (int): The name of the piece being moved.
            old_pos (tuple): The starting position (row, col) of the piece.
            new_pos (tuple): The ending position (row, col) of the piece.

        Returns:
            tuple or None: The position of the attacking piece if a discovered check is found, None otherwise.
        """
        def same_line(a, b, c):
            """Renvoie True si c est sur la même ligne droite que a → b"""
            xa, ya = a
            xb, yb = b
            xc, yc = c
            return (xa - xc) * (yb - yc) == (ya - yc) * (xb - xc)

        opponent_king_pos = self.engine.wk_pos if name < 0 else self.engine.bk_pos
        xk, yk = opponent_king_pos
        xo, yo = old_pos
        xn, yn = new_pos

        dx = xo - xk
        dy = yo - yk

        # Vérifie que la pièce est alignée avec le roi adverse
        if not (dx == 0 or dy == 0 or abs(dx) == abs(dy)):
            return None

        dir_x = dx // abs(dx) if dx != 0 else 0
        dir_y = dy // abs(dy) if dy != 0 else 0

        # Étape 1 : toutes les cases entre roi et ancienne position doivent être vides
        for i in range(1, max(abs(dx), abs(dy))):
            xi = xk + i * dir_x
            yi = yk + i * dir_y
            if (xi, yi) == old_pos:
                break
            if self.engine.board[xi][yi] != 0:
                return False  # Quelque chose bloque entre le roi et l’ancienne position

        # Étape 2 : vérifier qu’un attaquant est derrière la pièce
        for i in range(1, 8):
            x = xo + i * dir_x
            y = yo + i * dir_y

            if not (0 <= x < 8 and 0 <= y < 8):
                break

            piece = self.engine.board[x][y]
            if piece == 0:
                continue

            # Vérifier si la pièce peut attaquer dans cette direction
            if abs(piece) == 900 and not is_opponent_piece(name, piece):

                # --- Nouvelle vérification : la pièce reste-t-elle sur la ligne ?
                if same_line((xk, yk), (x, y), (xn, yn)):
                    return None
                return x, y
            elif abs(piece) == 500 and (dir_x == 0 or dir_y == 0) and not is_opponent_piece(name, piece):
                if same_line((xk, yk), (x, y), (xn, yn)):
                    return None
                return x, y
            elif abs(piece) == 325 and abs(dir_x) == abs(dir_y) and not is_opponent_piece(name, piece):
                if same_line((xk, yk), (x, y), (xn, yn)):
                    return None
                return x, y
            break  # autre pièce

        return None

    def move_gives_check(self, name, end_pos):
        """
        Check if a move would put the opponent's king in check.

        Args:
            name (int): The name of the piece being moved.
            end_pos (tuple): The ending position (row, col) of the piece.

        Returns:
            bool: True if the move gives check, False otherwise.
        """
        x0, y0 = end_pos

        opponent_king_pos = self.engine.bk_pos if name > 0 else self.engine.wk_pos

        moves = pieces_moves[name]

        if abs(name) == 1:
            return False

        elif abs(name) == 300:

            for dx, dy in moves:
                x, y = x0 + dx, y0 + dy

                if (x, y) == opponent_king_pos:

                    return True

        elif abs(name) == 100:
            direction = -1 if name > 0 else 1
            if ((x0 + direction, y0 + 1) == opponent_king_pos) or ((x0 + direction, y0 - 1) == opponent_king_pos):

                return True

        elif abs(name) == 900:

            check_x = opponent_king_pos[0] - x0
            check_y = opponent_king_pos[1] - y0

            dir_x = check_x // abs(check_x) if check_x != 0 else 0
            dir_y = check_y // abs(check_y) if check_y != 0 else 0

            if dir_x == 0 or dir_y == 0 or abs(dir_x) == abs(dir_y):
                kx, ky = x0 + dir_x, y0 + dir_y
                while 0 <= kx < 8 and 0 <= ky < 8:
                    piece = self.engine.board[kx][ky]
                    if piece == 0:
                        kx += dir_x
                        ky += dir_y
                        continue
                    elif (kx, ky) == opponent_king_pos:
                        return True
                    break  # une pièce bloque ou le roi est atteint

        elif abs(name) == 500:

            check_x = opponent_king_pos[0] - x0
            check_y = opponent_king_pos[1] - y0

            dir_x = check_x // abs(check_x) if check_x != 0 else 0
            dir_y = check_y // abs(check_y) if check_y != 0 else 0

            if dir_x == 0 or dir_y == 0:
                kx, ky = x0 + dir_x, y0 + dir_y
                while 0 <= kx < 8 and 0 <= ky < 8:
                    piece = self.engine.board[kx][ky]
                    if piece == 0:
                        kx += dir_x
                        ky += dir_y
                        continue
                    elif (kx, ky) == opponent_king_pos:
                        return True
                    break  # une pièce bloque ou le roi est atteint

        elif abs(name) == 325:
            check_x = opponent_king_pos[0] - x0
            check_y = opponent_king_pos[1] - y0

            dir_x = check_x // abs(check_x) if check_x != 0 else 0
            dir_y = check_y // abs(check_y) if check_y != 0 else 0

            if abs(dir_x) == abs(dir_y):
                kx, ky = x0 + dir_x, y0 + dir_y
                while 0 <= kx < 8 and 0 <= ky < 8:
                    piece = self.engine.board[kx][ky]
                    if piece == 0:
                        kx += dir_x
                        ky += dir_y
                        continue
                    elif (kx, ky) == opponent_king_pos:
                        return True
                    break  # une pièce bloque ou le roi est atteint

        return False

    def handle_simple_check(self, name, pos, color, last_move):

        possible_moves = set()

        attacking_piece_pos = last_move.attacking_piece_pos
        attacking_piece_name = self.engine.board[attacking_piece_pos[0]][attacking_piece_pos[1]]

        if self.is_pinned(pos, name, attacking_piece_pos):
            return possible_moves

        # Mouvement du roi
        elif abs(name) == 1:

            occuped_cases = self.find_all_occupated_cases('b' if color == 'w' else 'w')

            for dx, dy in pieces_moves[name]:
                xk, yk = pos[0] + dx, pos[1] + dy
                if 0 <= xk < 8 and 0 <= yk < 8:

                    # case vide ou pièce adverse
                    if (xk, yk) not in occuped_cases:
                        target_piece = self.engine.board[xk][yk]

                        if target_piece == 0:

                            attaking = self.is_discovered_check(name, pos, (xk, yk))
                            gives_check = 'simplecheck' if attaking else ''

                            possible_moves.add(Move(pos, (xk, yk), None, gives_check, attaking))

                        elif is_opponent_piece(name, target_piece):

                            attaking = self.is_discovered_check(name, pos, (xk, yk))
                            gives_check = 'simplecheck' if attaking else ''

                            possible_moves.add(Move(pos, (xk, yk), 'capture', gives_check, attaking))


        # capture directe
        elif abs(name) != 1 and self.piece_can_go_to_pos(name, pos, attacking_piece_pos):

            # pion
            if abs(name) == 100:
                promotion_row = 0 if name > 0 else 7

                if attacking_piece_pos[0] == promotion_row:

                    for piece in [900, 500, 325, 300]:
                        gives_check, check_pos = self.find_move_specificity(piece if color == "w" else -piece, pos, attacking_piece_pos)
                        possible_moves.add(Move(pos, attacking_piece_pos, str(piece) + "promotioncapture", gives_check, check_pos))

                else:
                    gives_check, check_pos = self.find_move_specificity(name, pos, attacking_piece_pos)
                    possible_moves.add(Move(pos, attacking_piece_pos, "capture", gives_check, check_pos))

            # autres pieces
            else:
                gives_check, check_pos = self.find_move_specificity(name, pos, attacking_piece_pos)
                possible_moves.add(Move(pos, attacking_piece_pos, "capture", gives_check, check_pos))

        # interception
        if abs(attacking_piece_name) in (900, 500, 325):

            king_pos = self.engine.bk_pos if name < 0 else self.engine.wk_pos

            xk, yk = king_pos
            xa, ya = attacking_piece_pos

            dx = xa - xk
            dy = ya - yk

            step_x = dx // abs(dx) if dx != 0 else 0
            step_y = dy // abs(dy) if dy != 0 else 0

            for i in range(1, 8):

                x, y = xk + step_x * i, yk + step_y * i

                if not (0 <= x < 8 and 0 <= y < 8):
                    break

                if (x, y) == attacking_piece_pos:
                    break

                if abs(name) != 1 and self.piece_can_go_to_pos(name, pos, (x, y)):

                    if abs(name) == 100:
                        promotion_row = 0 if name > 0 else 7
                        if x == promotion_row:
                            for piece in [900, 500, 325, 300]:
                                gives_check, check_pos = self.find_move_specificity(piece if color == "w" else -piece, pos, (x, y))
                                possible_moves.add(Move(pos, (x, y), str(piece) + "promotion", gives_check, check_pos))
                        else:
                            gives_check, check_pos = self.find_move_specificity(name, pos, (x, y))
                            possible_moves.add(Move(pos, (x, y), None, gives_check, check_pos))

                    else:
                        gives_check, check_pos = self.find_move_specificity(name, pos, (x, y))
                        possible_moves.add(Move(pos, (x, y), None, gives_check, check_pos))

        return possible_moves

    def handle_double_check(self, name, pos, color):

        possible_moves = set()

        occuped_cases = self.find_all_occupated_cases('b' if color == 'w' else 'w')

        for dx, dy in pieces_moves[name]:
            xk, yk = pos[0] + dx, pos[1] + dy
            if 0 <= xk < 8 and 0 <= yk < 8:
                target_piece = self.engine.board[xk][yk]
                # case vide ou pièce adverse
                if (xk, yk) not in occuped_cases:

                    attacking_pos = self.is_discovered_check(name, pos, (xk, yk))
                    gives_check = 'simplecheck' if attacking_pos else ''

                    if target_piece == 0:
                        possible_moves.add(Move(pos, (xk, yk), None, gives_check, attacking_pos))

                    elif is_opponent_piece(name, target_piece):
                        possible_moves.add(Move(pos, (xk, yk), 'capture', gives_check, attacking_pos))

        return possible_moves

    def moves_possible_by_a_piece(self, pos, last_move, color_player):
        """
        Find all possible legal moves for a specific piece.

        This method handles all the complex rules of chess, including checks, pins,
        castling, en passant, and promotions.

        Args:
            pos (tuple): The position (row, col) of the piece.
            last_move (Move): The last move made in the game, or None if it's the first move.
            color_player (str): The color of the player ('w' for white, 'b' for black).

        Returns:
            set: A set of all possible legal moves for the piece.
        """
        x0, y0 = pos
        name = self.engine.board[x0][y0]
        color = 'w' if name > 0 else 'b'
        if color != color_player:
            return set()

        if last_move is not None:

            if last_move.gives_check == 'simplecheck':
                return self.handle_simple_check(name, pos, color_player, last_move)

            if last_move.gives_check == 'doublecheck' and abs(name) == 1:
                return self.handle_double_check(name, pos, color)

        if not last_move or last_move.gives_check == '':

            match abs(name):
                case 300: return self.get_knight_moves(name, pos)
                case 100: return self.get_pawn_moves(name, pos, last_move, color)
                case 1: return self.get_king_moves(name, pos, color)
                case 900: return self.get_queen_moves(name, pos)
                case 500 | 325: return self.get_rookorbishop_moves(name, pos)
        return set()

    def get_knight_moves(self, name, pos):

        possible_moves = set()
        x0, y0 = pos
        moves = pieces_moves[name]
        if not self.is_pinned(pos, name):
            for dx, dy in moves:
                x, y = x0 + dx, y0 + dy
                if 0 <= x < 8 and 0 <= y < 8:
                    target = self.engine.board[x][y]
                    if target == 0:
                        move_specificity = None
                    elif is_opponent_piece(name, target):
                        move_specificity = "capture"
                    else:
                        continue

                    gives_check, check_pos = self.find_move_specificity(name, pos, (x, y))
                    possible_moves.add(Move(pos, (x, y), move_specificity, gives_check, check_pos))
        return possible_moves

    def get_pawn_moves(self, name, pos, last_move, color):
        possible_moves = set()
        x0, y0 = pos

        is_white = name > 0
        direction = -1 if is_white else 1
        start_row = 6 if is_white else 1
        promotion_row = 0 if is_white else 7

        x1, y = x0 + direction, y0

        # One or two square forward
        if 8 > x1 >= 0 == self.engine.board[x1][y]:
            if not self.is_pinned(pos, name, (x1, y)):

                if x1 == promotion_row:
                    for piece in [900, 500, 325, 300]:
                        gives_check, check_pos = self.find_move_specificity(piece if color == "w" else -piece, pos, (x1, y))
                        possible_moves.add(Move(pos, (x1, y), str(piece) + "promotion", gives_check, check_pos))

                else:
                    gives_check, check_pos = self.find_move_specificity(name, pos, (x1, y))
                    possible_moves.add(Move(pos, (x1, y), None, gives_check, check_pos))

            # Two squares forward
            x2 = x0 + 2 * direction
            if x0 == start_row and 8 > x2 >= 0 == self.engine.board[x2][y]:
                if not self.is_pinned(pos, name, (x2, y)):
                    gives_check, check_pos = self.find_move_specificity(name, pos, (x2, y))
                    possible_moves.add(Move(pos, (x2, y), "doublepush", gives_check, check_pos))

        # Diagonal captures
        for dy in [-1, 1]:
            y_diag = y0 + dy
            if 0 <= y_diag < 8:
                x_diag = x0 + direction
                if not self.is_pinned(pos, name, (x_diag, y_diag)):
                    target = self.engine.board[x_diag][y_diag]
                    if target != '.' and is_opponent_piece(name, target):

                        # promotion
                        if x_diag == promotion_row:
                            for piece in [900, 500, 325, 300]:
                                gives_check, check_pos = self.find_move_specificity(piece if color == "w" else -piece, pos, (x_diag, y_diag))
                                possible_moves.add(Move(pos, (x_diag, y_diag), str(piece) + "promotioncapture", gives_check, check_pos))
                        # capture simple
                        else:
                            gives_check, check_pos = self.find_move_specificity(name, pos, (x_diag, y_diag))
                            possible_moves.add(Move(pos, (x_diag, y_diag), "capture", gives_check, check_pos))

        # En passant
        if last_move and last_move.specificity == "doublepush":

            to_pos = last_move.end
            if to_pos[0] == (3 if is_white else 4) and x0 == to_pos[0]:
                if abs(y0 - to_pos[1]) == 1:
                    x_ep, y_ep = x0 + direction, to_pos[1]
                    if 8 > x_ep >= 0 == self.engine.board[x_ep][y_ep]:
                        gives_check, check_pos = self.find_move_specificity(name, pos, (x_ep, y_ep))
                        possible_moves.add(Move(pos, (x_ep, y_ep), "enpassantcapture", gives_check, check_pos))
        return possible_moves

    def get_king_moves(self, name, pos, color):

        possible_moves = set()
        x0, y0 = pos
        occuped_cases = self.find_all_occupated_cases('b' if color == 'w' else 'w')
        moves = pieces_moves[name]

        for dx, dy in moves:
            x, y = x0 + dx, y0 + dy
            if 0 <= x < 8 and 0 <= y < 8:
                if (x, y) not in occuped_cases:
                    target = self.engine.board[x][y]

                    discover_pos = self.is_discovered_check(name, pos, (x, y))

                    if discover_pos:
                        gives_check = 'simplecheck'
                        check_pos = discover_pos
                    else:
                        gives_check = ''
                        check_pos = None

                    if target == 0:
                        possible_moves.add(Move(pos, (x, y), None, gives_check, check_pos))
                    elif is_opponent_piece(name, target):
                        possible_moves.add(Move(pos, (x, y), "capture", gives_check, check_pos))

        for castle in ['queenside', 'kingside']:
            if self.is_castling_valid(name, castle):

                if castle == 'kingside':
                    gives_check = 'simplecheck' if self.move_gives_check(500 if name > 0 else -500, (x0, 5)) else ''
                    possible_moves.add(Move(pos, (x0, 6), "castlekingside", gives_check, (x0, 5)))
                else:  # queenside
                    gives_check = 'simplecheck' if self.move_gives_check(500 if name > 0 else -500, (x0, 3)) else ''
                    possible_moves.add(Move(pos, (x0, 2), "castlequeenside", gives_check, (x0, 3)))

        return possible_moves

    def get_queen_moves(self, name, pos):
        possible_moves = set()
        x0, y0 = pos
        moves = pieces_moves[name]

        for dx, dy in moves:
            for i in range(1, 8):
                x, y = x0 + dx * i, y0 + dy * i
                if not (0 <= x < 8 and 0 <= y < 8):
                    break

                target = self.engine.board[x][y]

                if not self.is_pinned(pos, name, (x, y)):

                    gives_check = 'simplecheck' if self.move_gives_check(name, (x, y)) else ''

                    if target == 0:

                        possible_moves.add(Move(pos, (x, y), None, gives_check, (x, y) if gives_check else None))

                    elif is_opponent_piece(name, target):
                        possible_moves.add(Move(pos, (x, y), "capture", gives_check, (x, y) if gives_check else None))
                        break
                    else:
                        break  # friendly piece blocks
        return possible_moves

    def get_rookorbishop_moves(self, name, pos):

        x0, y0 = pos
        moves = pieces_moves[name]
        possible_moves = set()

        for dx, dy in moves:

            for i in range(1, 8):
                x, y = x0 + dx * i, y0 + dy * i
                if not (0 <= x < 8 and 0 <= y < 8):
                    break
                if self.is_pinned(pos, name, (x, y)):
                    break
                target = self.engine.board[x][y]
                gives_check, check_pos = self.find_move_specificity(name, pos, (x, y))

                specificity = None
                if target != 0:
                    if is_opponent_piece(name, target):
                        specificity = "capture"
                    else:
                        break  # friendly piece blocks

                possible_moves.add(Move(pos, (x, y), specificity, gives_check, check_pos))

                if specificity == "capture":
                    break  # stop after capture
        return possible_moves

    def find_move_specificity(self, name, pos_from, pos_to):
        check = self.move_gives_check(name, pos_to)
        discover_pos = self.is_discovered_check(name, pos_from, pos_to)

        if check and discover_pos:
            gives_check = 'doublecheck'
            check_pos = None
        elif check:
            gives_check = 'simplecheck'
            check_pos = pos_to
        elif discover_pos:
            gives_check = 'simplecheck'
            check_pos = discover_pos
        else:
            gives_check = ''
            check_pos = None
        return gives_check, check_pos

    def piece_can_go_to_pos(self, name, from_pos, to_pos):
        """
        Check if a piece can move from one position to another, ignoring checks.

        This is a simpler version of the movement logic that only checks if the piece
        can physically reach the target position, without considering checks or other complex rules.

        Args:
            name (int): The name of the piece.
            from_pos (tuple): The starting position (row, col) of the piece.
            to_pos (tuple): The target position (row, col).

        Returns:
            bool: True if the piece can move to the target position, False otherwise.
        """
        x0, y0 = from_pos

        for dx, dy in pieces_moves[name]:
            if abs(name) in (300, 1):
                x, y = x0 + dx, y0 + dy
                if (x, y) == to_pos:
                    return True

            elif abs(name) in (900, 500, 325):
                for i in range(1, 8):
                    x, y = x0 + dx * i, y0 + dy * i
                    if not (0 <= x < 8 and 0 <= y < 8):
                        break
                    if (x, y) == to_pos:
                        return True

                    if self.engine.board[x][y] != 0:
                        break  # Une pièce bloque

        if abs(name) == 100:
            direction = -1 if name > 0 else 1
            if (x0 + direction, y0) == to_pos and self.engine.board[to_pos[0]][to_pos[1]] == 0:
                return True
            if ((x0 + direction, y0 + 1) == to_pos or (x0 + direction, y0 - 1) == to_pos) and self.engine.board[to_pos[0]][to_pos[1]] != 0:
                return True

        return False

    def do_move(self, move):
        """
        Execute a move on the board.

        This method updates the board state to reflect the move, handling special moves
        like castling, en passant, and promotions.

        Args:
            move (Move): The move to execute.

        Returns:
            dict: A backup of the board state before the move, which can be used to undo the move.
        """
        a, b = move.start
        c, d = move.end
        move_type = move.specificity


        piece = self.engine.board[a][b]

        backup2 = {
            "move": move,
            "captured_piece": self.engine.board[c][d]
        }

        iswhite = piece > 0

        # --- Appliquer le move ---
        self.engine.board[c][d] = piece
        self.engine.board[a][b] = 0

        if piece == 1:
            backup2["wk_has_moved"] = self.engine.wk_has_moved
            self.engine.wk_has_moved = True
            backup2["wk_pos"] = (a, b)
            self.engine.wk_pos = (c, d)

        elif piece == -1:
            backup2["bk_has_moved"] = self.engine.bk_has_moved
            self.engine.bk_has_moved = True
            backup2["bk_pos"] = (a, b)
            self.engine.bk_pos = (c, d)

        elif piece == 500:
            if (a, b) == (7, 0):
                backup2["wrl_has_moved"] = self.engine.wrl_has_moved
                self.engine.wrl_has_moved = True

            elif (a, b) == (7, 7):
                backup2["wrr_has_moved"] = self.engine.wrr_has_moved
                self.engine.wrr_has_moved = True

        elif piece == -500:
            if (a, b) == (0, 0):
                backup2["brl_has_moved"] = self.engine.brl_has_moved
                self.engine.brl_has_moved = True

            elif (a, b) == (0, 7):
                backup2["brr_has_moved"] = self.engine.brr_has_moved
                self.engine.brr_has_moved = True

        if move_type:
            if move_type == "castlekingside":
                row = 7 if iswhite else 0

                self.engine.board[row][5] = self.engine.board[row][7]
                self.engine.board[row][7] = 0
                if iswhite:
                    backup2["wk_castle"] = self.engine.wk_castle
                    self.engine.wk_castle = True
                else:
                    backup2["bk_castle"] = self.engine.bk_castle
                    self.engine.bk_castle = True

            elif move_type == "castlequeenside":
                row = 7 if iswhite else 0
                self.engine.board[row][3] = self.engine.board[row][0]
                self.engine.board[row][0] = 0
                if iswhite:
                    backup2["wk_castle"] = self.engine.wk_castle
                    self.engine.wk_castle = True
                else:
                    backup2["bk_castle"] = self.engine.bk_castle
                    self.engine.bk_castle = True

            elif move_type == "enpassantcapture":
                direction = -1 if iswhite else 1
                captured_row = c - direction
                backup2["enpassant_captured_pos"] = (captured_row, d)
                backup2["captured_piece"] = self.engine.board[captured_row][d]
                self.engine.board[captured_row][d] = 0

            elif "promotion" in move_type:
                promoted_piece = int(move_type[0:3])
                backup2["promoted_from"] = piece
                self.engine.board[c][d] = promoted_piece if iswhite else -promoted_piece

        return backup2

    def undo_move(self, backup):
        """
        Undo a move and restore the board to its previous state.

        This method uses the backup created by do_move to restore the board state,
        handling special moves like castling, en passant, and promotions.

        Args:
            backup (dict): The backup of the board state before the move.
        """
        move = backup["move"]
        a, b = move.start
        c, d = move.end
        move_type = move.specificity

        # --- Déterminer la couleur à partir de la pièce d'origine
        piece = backup.get("promoted_from", self.engine.board[c][d])
        iswhite = piece > 0

        # --- Restaurer la case de départ (promotion ou pas)
        self.engine.board[a][b] = backup.get("promoted_from", self.engine.board[c][d])

        # --- Restaurer la case d’arrivée
        self.engine.board[c][d] = backup["captured_piece"]

        # --- Restaurer les états du roi
        if "wk_has_moved" in backup:
            self.engine.wk_has_moved = backup["wk_has_moved"]
            self.engine.wk_pos = backup["wk_pos"]
        if "bk_has_moved" in backup:
            self.engine.bk_has_moved = backup["bk_has_moved"]
            self.engine.bk_pos = backup["bk_pos"]

        # --- Restaurer les états des tours
        for attr in ["wrl_has_moved", "wrr_has_moved", "brl_has_moved", "brr_has_moved"]:
            if attr in backup:
                setattr(self.engine, attr, backup[attr])

        # --- Gérer les coups spéciaux
        row = 7 if iswhite else 0

        if move_type == "castlekingside":
            self.engine.board[row][7] = self.engine.board[row][5]  # Replacer la tour
            self.engine.board[row][5] = 0
            if iswhite:
                self.engine.wk_castle = backup.get("wk_castle", False)
            else:
                self.engine.bk_castle = backup.get("bk_castle", False)

        elif move_type == "castlequeenside":
            self.engine.board[row][0] = self.engine.board[row][3]  # Replacer la tour
            self.engine.board[row][3] = 0
            if iswhite:
                self.engine.wk_castle = backup.get("wk_castle", False)
            else:
                self.engine.bk_castle = backup.get("bk_castle", False)

        elif move_type == "enpassantcapture":
            captured_row, col = backup["enpassant_captured_pos"]
            self.engine.board[captured_row][col] = backup["captured_piece"]
            self.engine.board[c][d] = 0  # La case de destination du pion reste vide

        elif move_type and "promotion" in move_type:
            self.engine.board[a][b] = backup["promoted_from"]  # Remettre le pion
            self.engine.board[c][d] = backup["captured_piece"]  # Remettre la pièce capturée

    def move_score(self, move):
        """
        Calculate a score for a move, used for move ordering in search algorithms.

        Higher scores are given to moves that are likely to be good, such as captures of high-value pieces,
        promotions, and checks.

        Args:
            move (Move): The move to score.

        Returns:
            float: A negative score for the move (negative because lower scores are better in the minimax algorithm).
        """


        to_pos = move.end
        from_pos = move.start
        move_type = move.specificity
        board = self.engine.board

        score = 0

        if move_type:
            if "promotion" in move_type:
                score += 900  # Priorité haute pour promotions

            if "capture" in move_type:
                target_val = abs(board[to_pos[0]][to_pos[1]])
                attacker_val = abs(board[from_pos[0]][from_pos[1]])


                score += target_val - attacker_val + 300

            if move.gives_check != '':
                score += 0.2  # On augmente un peu plus le poids du check

        return -score

