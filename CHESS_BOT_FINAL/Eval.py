from Rules import grid_adv


class Eval:
    """
    Class that evaluates the position based on the placement of pieces on the board.

    This class provides methods to calculate different aspects of positional advantage,
    including piece values, piece positioning, and king safety.
    """

    def __init__(self, engine):
        """
        Initialize the Eval class with a reference to the chess engine.

        Args:
            engine: The chess engine that contains the board state and game information.
        """
        self.engine = engine
        pass


    # def adv_king_safe(self):
    #     """
    #     Calculate the advantage based on king safety through castling.
    #
    #     This method evaluates which side has an advantage based on which kings
    #     have castled. If both kings have castled or neither has, there's no advantage.
    #     If only the white king has castled, white has an advantage. If only the black
    #     king has castled, black has an advantage.
    #
    #     Returns:
    #         float: A positive value indicates an advantage for white, a negative value
    #               indicates an advantage for black, and 0 indicates no advantage.
    #     """
    #     adv = 0
    #
    #     if self.engine.wk_castle and self.engine.bk_castle:
    #         adv = 0
    #
    #     elif self.engine.wk_castle:
    #         adv = 1
    #
    #     elif self.engine.bk_castle:
    #         adv = - 1
    #
    #     return round(adv, 2)
    #
    # def adv_positionning(self):
    #     """
    #     Calculate the advantage based on piece positioning on the board.
    #
    #     This method evaluates the positional advantage by considering the placement
    #     of pieces on the board. Each square on the board has a positional value defined
    #     in the grid_adv array. Pieces on advantageous squares contribute to a higher
    #     evaluation for their side.
    #
    #     Returns:
    #         float: A positive value indicates an advantage for white, a negative value
    #               indicates an advantage for black, and 0 indicates no advantage.
    #     """
    #     adv = 0
    #     for i, line in enumerate(self.engine.board):
    #         for j, piece in enumerate(line):
    #             if piece != 0:
    #                 if piece > 0:
    #                     adv += grid_adv[i][j]
    #                 elif piece < 0:
    #                     adv -= grid_adv[i][j]
    #     return round(adv, 1)
    #
    def adv_piece_value(self):
        """
        Calculate the advantage based on the material value of pieces on the board.

        This method evaluates the material advantage by summing the values of all pieces
        on the board. Each piece type has a predefined value in the piece_values dictionary.
        White pieces contribute positively to the advantage, while black pieces contribute
        negatively.

        Returns:
            float: A positive value indicates a material advantage for white, a negative value
                  indicates a material advantage for black, and 0 indicates material equality.
        """
        adv = 0
        for line in self.engine.board:
            for piece in line:
                if piece != 0:
                    adv += round(piece / 100, 2)


        return int(adv)
    #
    #
    # def total_adv_old(self, depth):
    #     """
    #     Calculate the total advantage by combining all evaluation components.
    #
    #     This method computes the overall advantage in the position by summing the
    #     advantages from material value, piece positioning, and king safety. The result
    #     provides a comprehensive evaluation of the current board state.
    #
    #     Args:
    #         depth (int): The current search depth, which could be used to adjust the
    #                     evaluation based on whose turn it is to move.
    #
    #     Returns:
    #         float: A positive value indicates an overall advantage for white, a negative
    #               value indicates an overall advantage for black, and 0 indicates equality.
    #     """
    #     adv = (self.adv_piece_value() +
    #            self.adv_positionning() +
    #            self.adv_king_safe())
    #
    #
    #     return round(adv, 2)


    def total_adv(self) -> float:
        """
        Évalue l'avantage global en une seule passe de boucle.
        """
        adv = 0.0
        for i, line in enumerate(self.engine.board):
            for j, piece in enumerate(line):
                if piece == 0:
                    continue

                if piece > 0:  # White
                    position_bonus = grid_adv[i][j]
                else:  # Black
                    position_bonus = -grid_adv[i][j]
                adv += self.engine.board[i][j] / 100 + position_bonus


        # Ajouter sécurité du roi
        if self.engine.wk_castle and not self.engine.bk_castle:
            adv += 1
        elif self.engine.bk_castle and not self.engine.wk_castle:
            adv -= 1

        return round(adv, 1)