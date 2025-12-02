import os
import sys
from stockfish import Stockfish

class Game(Stockfish):
    """
    Classe wrapper autour de Stockfish pour gérer la logique spécifique au jeu.
    """
    
    dir = os.path.dirname(os.path.abspath(__file__))
    DEFAULT_PATH = dir + "\\code_source_stockfish/stockfish-windows-x86-64-avx2.exe"

    def __init__(self, initial_difficulty):
        # Vérification de l'existence du fichier
        if not os.path.exists(self.DEFAULT_PATH):
            print(f"ERREUR CRITIQUE: Stockfish introuvable à : {self.DEFAULT_PATH}")
            # Fallback pour éviter le crash immédiat si le chemin est faux, 
            # mais il faudra le corriger
            path = "stockfish" 
        else:
            path = self.DEFAULT_PATH

        try:
            super().__init__(path=path)
        except Exception as e:
            print(f"Erreur au chargement de Stockfish: {e}")
            raise e

        self.update_engine_parameters({"UCI_Elo": initial_difficulty})
        self.move_history = [] # Historique interne des coups

    def get_board_array(self):
        """
        Récupère la représentation visuelle de Stockfish et la transforme en matrice 8x8.
        C'est une version nettoyée de ton ancienne fonction get_board.
        """
        # On utilise get_fen_position qui est beaucoup plus fiable que le parsing visuel
        # Mais pour respecter ton code existant qui attend une matrice 'wP', 'bn', etc.,
        # on va parser le FEN (Forsyth-Edwards Notation).
        
        fen = self.get_fen_position()
        rows = fen.split(' ')[0].split('/')
        board = []

        for row in rows:
            board_row = []
            for char in row:
                if char.isdigit():
                    # Les chiffres représentent des cases vides
                    board_row.extend([None] * int(char))
                else:
                    # Les lettres représentent des pièces
                    color = 'w' if char.isupper() else 'b'
                    piece = color + char.lower()
                    board_row.append(piece)
            board.append(board_row)
        
        return board

    def calculs_win_eval(self):
        evalu = self.get_evaluation()
        if evalu['type'] == 'cp':
            return ['cp', evalu['value'] / 100]
        elif evalu['type'] == 'mate':
            return ['mate', evalu['value']]
        return ['cp', 0.0]

    def get_niv_elo(self):
        return self.get_parameters()["UCI_Elo"]

    def set_difficulty(self, difficulty):
        self.update_engine_parameters({"UCI_Elo": difficulty})

    def move_piece(self, move):
        if self.is_move_correct(move):
            self.make_moves_from_current_position([move])
            self.move_history.append(move)
            return True
        return False

    def test_move(self, move):
        return self.is_move_correct(move)

    def test_capture(self, move):
        # Attention: will_move_be_a_capture peut renvoyer NO_CAPTURE (enum)
        capture = str(self.will_move_be_a_capture(move))
        return "DIRECT_CAPTURE" in capture

    def is_a_promotion(self, move_str):
        """
        Vérifie si un coup est une promotion (pion qui arrive au bout).
        move_str: ex 'e7e8'
        """
        # Logique simplifiée mais robuste basée sur le FEN et les coordonnées
        start_sq = move_str[:2]
        end_sq = move_str[2:4]
        
        piece = self.get_what_is_on_square(start_sq)
        if not piece: return False
        
        piece_type = str(piece).replace("Piece.", "") # EX: Piece.WHITE_PAWN -> WHITE_PAWN
        
        if "PAWN" in piece_type:
            # Si Blanc va sur la ligne 8 ou Noir sur la ligne 1
            if ("WHITE" in piece_type and end_sq[1] == '8') or \
               ("BLACK" in piece_type and end_sq[1] == '1'):
                return True
                
        return False

    def find_best_move(self):
        return self.get_best_move_time(500) # Temps un peu plus long pour meilleure qualité

    def reset_position(self, moves):
        """Réinitialise le plateau à une liste de coups spécifique."""
        self.set_position(moves)
        self.move_history = moves

    def close_engine(self):
        """Ferme proprement le process."""
        # Stockfish n'a pas de méthode close explicite dans toutes les versions de la lib,
        # mais le destructeur __del__ s'en occupe souvent.
        # On peut envoyer la commande UCI 'quit'
        try:
            self._put(f"quit")
        except:
            pass