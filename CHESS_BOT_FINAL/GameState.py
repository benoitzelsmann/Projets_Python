from Rules import initial_position


class GameState:
    """
    Represents the state of a chess game.

    This class stores all the information needed to represent a chess game state,
    including the board configuration, piece positions, castling rights, and move history.
    """
    def __init__(self, board, wk_has_moved, wrr_has_moved, wrl_has_moved, bk_has_moved, brr_has_moved, brl_has_moved,
                 wk_castle, bk_castle, last_move, wk_pos, bk_pos):
        """
        Initialize a new game state.

        Parameters:
            board (list): 2D list representing the chess board with pieces
            wk_has_moved (bool): Whether the white king has moved
            wrr_has_moved (bool): Whether the white right rook has moved
            wrl_has_moved (bool): Whether the white left rook has moved
            bk_has_moved (bool): Whether the black king has moved
            brr_has_moved (bool): Whether the black right rook has moved
            brl_has_moved (bool): Whether the black left rook has moved
            wk_castle (bool): Whether white king has castled
            bk_castle (bool): Whether black king has castled
            last_move: The last move made in the game
            wk_pos (tuple): Position of the white king (row, col)
            bk_pos (tuple): Position of the black king (row, col)
        """
        self.board = board
        self.wk_has_moved = wk_has_moved
        self.wrr_has_moved = wrr_has_moved
        self.wrl_has_moved = wrl_has_moved
        self.bk_has_moved = bk_has_moved
        self.brr_has_moved = brr_has_moved
        self.brl_has_moved = brl_has_moved
        self.wk_castle = wk_castle
        self.bk_castle = bk_castle

        self.last_move = last_move

        self.wk_pos = wk_pos
        self.bk_pos = bk_pos

    def clone(self):
        """
        Create a deep copy of the current game state.

        Returns:
            GameState: A new GameState object with the same attributes as the current one
        """
        return GameState(
            [row[:] for row in self.board],
            self.wk_has_moved,
            self.wrr_has_moved,
            self.wrl_has_moved,
            self.bk_has_moved,
            self.brr_has_moved,
            self.brl_has_moved,
            self.wk_castle,
            self.bk_castle,
            self.last_move,
            self.wk_pos,
            self.bk_pos
        )

    def reset(self):
        """
        Reset the game state to the initial position.

        This method resets the board to the starting position of a chess game,
        resets all castling flags, and sets the kings to their initial positions.
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
        self.bk_pos = (0, 4)
        self.wk_pos = (7, 4)

        self.last_move = None
