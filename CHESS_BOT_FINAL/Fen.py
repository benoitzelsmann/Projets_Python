import re


class Fen:
    """
    Class for handling Forsyth-Edwards Notation (FEN) in chess.

    This class provides methods to convert between FEN strings and board representations,
    validate FEN strings, and update the game engine with the board state from a FEN string.

    FEN is a standard notation to describe a particular board position of a chess game.
    """
    def __init__(self, engine):
        """
        Initialize a Fen object.

        Parameters:
            engine: The chess engine object that will be updated with the board state.
                    This object should have attributes like board, wk_pos, bk_pos, and castling rights.

        Attributes:
            fen_example: A string example of a valid FEN notation.
            engine: Reference to the chess engine.
        """
        self.fen_example = "rnbqkbnr/ppp2ppp/4p3/3p4/3P4/4P3/PPP2PPP/RNBQKBNR w KQkq d6 0 3"
        self.engine = engine

    def fen_to_board(self, fen):
        """
        Convert a FEN string to a board representation and update the engine.

        This method parses a FEN string, creates a board representation, and updates
        the engine's board state, king positions, and castling rights.

        Parameters:
            fen (str): A valid FEN string representing a chess position.

        Returns:
            list: A 2D list representing the chess board, where each element is either
                  a piece character or '.' for empty squares.
        """
        board = []
        fen_position = fen.split()[0]  # Partie des pièces uniquement
        rows = fen_position.split('/')

        # Création du tableau de jeu
        for row in rows:
            board_row = []
            for char in row:
                if char.isdigit():
                    # Ajouter des cases vides ('.') pour le chiffre
                    board_row.extend(['.' for _ in range(int(char))])
                else:
                    # Ajouter la pièce spécifiée
                    board_row.append(char)
            board.append(board_row)

        # Mise à jour du plateau
        self.engine.board = board

        for x in range(8):
            for y in range(8):
                piece = self.engine.board[x][y]
                if piece == 'K':
                    self.engine.wk_pos = (x, y)  # Position du roi blanc
                elif piece == 'k':
                    self.engine.bk_pos = (x, y)  # Position du roi noir

        _, castling_rights, _, _, _, _ = fen.split()


        # Initialisation des droits de roque (True/False)
        self.engine.wrr_has_moved = False if 'K' in castling_rights else True   # Droit de roque pour le roi blanc (côté roi)
        self.engine.brr_has_moved = False if 'k' in castling_rights else True  # Droit de roque pour le roi noir (côté roi)
        self.engine.wrl_has_moved = False if 'Q' in castling_rights else True  # Droit de roque pour la tour blanche (côté dame)
        self.engine.brl_has_moved = False if 'q' in castling_rights else True  # Droit de roque pour la tour noire (côté dame)


    @staticmethod
    def is_valid_fen(fen):
        """
        Validate if a string is a correctly formatted FEN notation.

        This static method checks if the provided string follows the Forsyth-Edwards Notation
        rules by validating each component of the FEN string:
        - Position (8 rows with 8 squares each)
        - Active color (w or b)
        - Castling availability
        - En passant target square
        - Halfmove clock
        - Fullmove number

        Parameters:
            fen (str): The FEN string to validate.

        Returns:
            bool: True if the FEN string is valid, False otherwise.
        """
        parts = fen.strip().split()

        if len(parts) != 6:
            return False

        position, active_color, castling, en_passant, halfmove, fullmove = parts

        # Vérification de la position (8 rangées)
        rows = position.split('/')
        if len(rows) != 8:
            return False

        for row in rows:
            count = 0
            for char in row:
                if char.isdigit():
                    count += int(char)
                elif char in 'rnbqkpRNBQKP':
                    count += 1
                else:
                    return False
            if count != 8:
                return False

        # Vérification du joueur actif
        if active_color not in ('w', 'b'):
            return False

        # Vérification des droits de roque
        if castling != '-' and not re.fullmatch(r'[KQkq]+', castling):
            return False

        # Vérification de la case en passant
        if en_passant != '-' and not re.fullmatch(r'^[a-h][36]$', en_passant):
            return False

        # Vérification des compteurs (demi-coups et numéro de coup)
        try:
            if int(halfmove) < 0 or int(fullmove) <= 0:
                return False
        except ValueError:
            return False

        return True

    def get_board_from_fen(self, fen):
        """
        Validate and convert a FEN string to a board representation.

        This method first validates the FEN string using is_valid_fen, and if valid,
        converts it to a board representation using fen_to_board.

        Parameters:
            fen (str): The FEN string to convert.

        Returns:
            list or None: A 2D list representing the chess board if the FEN is valid,
                         None otherwise.
        """
        if self.is_valid_fen(fen):
            board = self.fen_to_board(fen)
        else:
            print('Not a Valid FEN file')
            board = None

        return board
