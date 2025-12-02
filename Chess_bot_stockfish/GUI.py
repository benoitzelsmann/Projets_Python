import tkinter as tk
import os
from typing import List, Dict, Optional, Any, Tuple, Union
from PIL import Image, ImageTk

# On importe ta classe Game refactorisée
from Stock_bot import Game

class ChessGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- 1. Configuration et Variables ---
        self.mode = "againstcomputer"
        self.stop = False
        
        # Chemins
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Moteur
        try:
            self.game = Game(100)
            self.game_pro = Game(2000) # Utilisé pour l'analyse
        except Exception as e:
            print("Erreur critique chargement moteur:", e)
            self.destroy()
            return

        # Variables de jeu
        self.player_color = "w" # Humain joue les blancs par défaut
        self.turn_color = "w"
        self.move_history: List[str] = [] # Liste des coups (ex: ['e2e4', 'e7e5'])
        
        # Variables interaction
        self.case_selectionnee: Optional[str] = None # Ex: "e2"
        self.case_selectionnee_id: Optional[int] = None # ID Canvas
        self.possibles_moves_ids: List[int] = [] # IDs des ronds verts/rouges
        
        # Gestion Promotion
        self.pending_promotion_move: Optional[str] = None # Stocke "a7a8" en attendant le choix

        # Variables UI (Dimensions)
        self.board_size = 640
        self.cell_size = 80
        self.radius = 10
        self.largeur_labels = 20
        self.colors = ["lightgrey", "darkblue"]
        
        # Calcul des tailles
        self.canvas_size = (self.board_size + self.largeur_labels * 2, self.board_size + self.largeur_labels * 2)
        self.canvas_2_size = (60, self.board_size + self.largeur_labels * 2)
        self.dimension_bar = (35, self.board_size)
        self.offset_bar = (self.canvas_2_size[0] - self.dimension_bar[0]) // 2
        self.canvas_34_size = (self.canvas_size[0] + self.canvas_2_size[0] + 3, 70)
        self.dimension_button = (50, 50)

        # Variables de stockage d'images et IDs canvas
        self.images: Dict[str, ImageTk.PhotoImage] = {}
        self.images_mini: Dict[str, ImageTk.PhotoImage] = {}
        self.pieces_on_board_ids: Dict[int, str] = {} # Map ID canvas -> Code pièce (ex 'wp')
        self.cases_map: Dict[int, str] = {} # ID Rect -> "e2"
        self.cases_map_rev: Dict[str, int] = {} # "e2" -> ID Rect
        
        # Pièces prises
        self.pieces_taken = {"white": [], "black": []}
        self.pieces_taken_ids_3: List[int] = []
        self.pieces_taken_ids_4: List[int] = []
        self.piece_values = {'k': 0, 'q': 9, 'r': 5, 'n': 3, 'b': 3, 'p': 1}

        # --- 2. Initialisation Fenêtre ---
        self.title("Chess Board")
        self.configure(bg="white")
        self.geometry(f"{self.canvas_size[0] + self.canvas_2_size[0]}x{self.canvas_size[1] + self.canvas_34_size[1] * 2 + 20}")
        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)
        self.bind("<Left>", self.retour_arriere)

        # --- 3. Construction UI ---
        self._init_ui_containers()
        self._load_assets()
        self._draw_static_elements()
        self._draw_board_grid()
        
        # --- 4. Premier rendu ---
        self.update_board_visuals()
        self.update_evaluation_bar()
        
        # Lancer la boucle de jeu IA
        self.check_computer_turn()

    # ------------------------------------------------------------------
    # INITIALISATION UI
    # ------------------------------------------------------------------

    def _init_ui_containers(self):
        # Header (Info Adversaire)
        self.canvas_top = tk.Canvas(self, bg="lightgrey", width=self.canvas_34_size[0], height=self.canvas_34_size[1], highlightthickness=0)
        self.canvas_top.pack(side=tk.TOP)

        self.frame_main = tk.Frame(self)
        self.frame_main.pack(side=tk.TOP)

        # Plateau
        self.canvas_board = tk.Canvas(self.frame_main, bg="lightgrey", width=self.canvas_size[0], height=self.canvas_size[1], highlightthickness=0)
        self.canvas_board.pack(side=tk.LEFT)
        self.canvas_board.bind("<Button-1>", self.on_click_board)

        # Barre d'évaluation
        self.canvas_eval = tk.Canvas(self.frame_main, bg="lightgrey", width=self.canvas_2_size[0], height=self.canvas_2_size[1], highlightthickness=0)
        self.canvas_eval.pack(side=tk.LEFT)

        # Footer (Info Joueur)
        self.canvas_bottom = tk.Canvas(self, bg="lightgrey", width=self.canvas_34_size[0], height=self.canvas_34_size[1], highlightthickness=0)
        self.canvas_bottom.pack(side=tk.TOP)

    def _load_assets(self):
        # Chargement pièces
        pieces = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp"]
        for p in pieces:
            try:
                path = os.path.join(self.base_path, "pieces", f"{p}.png")
                img = Image.open(path)
                self.images[p] = ImageTk.PhotoImage(img.resize((self.cell_size, self.cell_size)))
                self.images_mini[p] = ImageTk.PhotoImage(img.resize((int(self.cell_size/2), int(self.cell_size/2))))
            except Exception as e:
                print(f"Erreur image {p}: {e}")

        # Chargement icône paramètres
        try:
            path = os.path.join(self.base_path, "parameters.png")
            img = Image.open(path)
            self.icon_gear = ImageTk.PhotoImage(img.resize(self.dimension_button))
        except:
            self.icon_gear = None

    def _draw_static_elements(self):
        # Bouton Paramètres
        if self.icon_gear:
            self.btn_params = self.canvas_top.create_image(670, 10, anchor=tk.NW, image=self.icon_gear)
            self.canvas_top.tag_bind(self.btn_params, "<Button-1>", self.open_parameters_window)

        # Textes Adversaire
        self.text_opponent_name = self.canvas_top.create_text(70, 20, text="Stockfish", font=("Arial", 15), fill="black", anchor="w")
        self.text_opponent_elo = self.canvas_top.create_text(160, 20, text=f"(Elo : {self.game.get_niv_elo()})", font=("Arial", 13), fill="black", anchor="w")
        self.text_adv_opponent = self.canvas_top.create_text(300, 20, text="", font=("Arial", 13, "bold"), fill="black", anchor="w")

        # Textes Joueur
        self.canvas_bottom.create_text(100, 15, text="Joueur Humain", font=("Arial", 15), fill="black", anchor="w")
        self.text_adv_player = self.canvas_bottom.create_text(300, 15, text="", font=("Arial", 13, "bold"), fill="black", anchor="w")

        # Barre Eval (Fond Blanc)
        self.canvas_eval.create_rectangle(
            self.offset_bar, self.largeur_labels, 
            self.dimension_bar[0] + self.offset_bar, self.canvas_2_size[1] - self.largeur_labels, 
            fill="white"
        )
        # Rectangle Noir (Dynamique)
        self.rect_eval_black = self.canvas_eval.create_rectangle(
            self.offset_bar, self.largeur_labels,
            self.dimension_bar[0] + self.offset_bar, self.largeur_labels + self.board_size // 2,
            fill="black"
        )
        self.text_eval = self.canvas_eval.create_text(
            self.offset_bar + self.dimension_bar[0] // 2, self.dimension_bar[1] + 5,
            text="0.0", font=("Helvetica", 8, "bold"), fill="green"
        )

    def _draw_board_grid(self):
        # Dessin des cases
        line = 8
        for row in range(8):
            for col in range(8):
                column = chr(97 + col) # 'a' = 97
                case_code = f"{column}{line}"
                
                color = self.colors[(row + col) % 2]
                x1 = col * self.cell_size + self.largeur_labels
                y1 = row * self.cell_size + self.largeur_labels
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                rect_id = self.canvas_board.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags="case")
                
                # Mapping
                self.cases_map[rect_id] = case_code
                self.cases_map_rev[case_code] = rect_id
                
            line -= 1
        
        # Coordonnées
        for i in range(8):
            # Lettres (bas)
            x = i * self.cell_size + self.cell_size/2 + self.largeur_labels
            y = self.board_size + self.largeur_labels * 1.5
            self.canvas_board.create_text(x, y, text=chr(97+i), font=("Arial", 12, "bold"))
            
            # Chiffres (droite)
            x = self.board_size + self.largeur_labels * 1.5
            y = i * self.cell_size + self.cell_size/2 + self.largeur_labels
            self.canvas_board.create_text(x, y, text=str(8-i), font=("Arial", 12, "bold"))

    # ------------------------------------------------------------------
    # GESTION DES CLICS & MOUVEMENT
    # ------------------------------------------------------------------

    def on_click_board(self, event):
        # Si c'est au tour de l'ordi et qu'on joue contre, on bloque le clic
        if self.mode == "againstcomputer" and self.turn_color != self.player_color:
            return

        # Trouver la case cliquée
        clicked_id = self.canvas_board.find_closest(event.x, event.y)[0]
        # On s'assure de récupérer l'ID du rectangle (case) en dessous de la pièce potentielle
        # `find_overlapping` est mieux pour trouver la case 'sous' la souris
        items = self.canvas_board.find_overlapping(event.x, event.y, event.x, event.y)
        case_id = None
        for item in items:
            if item in self.cases_map:
                case_id = item
                break
        
        if not case_id: return
        
        case_name = self.cases_map[case_id]

        # LOGIQUE DE SÉLECTION
        
        # Cas 1: Aucune case sélectionnée -> Sélection
        if self.case_selectionnee is None:
            # Vérifier s'il y a une pièce à nous dessus
            piece = self.game.get_what_is_on_square(case_name)
            if piece:
                # Stockfish renvoie Piece.WHITE_PAWN etc.
                p_str = str(piece)
                is_white = "WHITE" in p_str
                # Vérifier si c'est notre couleur
                if (self.turn_color == 'w' and is_white) or (self.turn_color == 'b' and not is_white):
                    self.select_square(case_id, case_name)

        # Cas 2: Case déjà sélectionnée -> Déplacement ou changement de sélection
        else:
            # Si on clique sur la même case -> Désélectionner
            if case_name == self.case_selectionnee:
                self.deselect_square()
            
            # Si on clique sur une autre pièce de notre couleur -> Changer sélection
            elif self._is_own_piece(case_name):
                self.deselect_square()
                self.select_square(case_id, case_name)
            
            # Sinon -> Tenter le mouvement
            else:
                move_str = self.case_selectionnee + case_name
                self.try_player_move(move_str)

    def _is_own_piece(self, case_name):
        piece = self.game.get_what_is_on_square(case_name)
        if not piece: return False
        is_white = "WHITE" in str(piece)
        return (self.turn_color == 'w' and is_white) or (self.turn_color == 'b' and not is_white)

    def select_square(self, case_id, case_name):
        self.case_selectionnee = case_name
        self.case_selectionnee_id = case_id
        self._highlight_square(case_id, True)
        self.show_possible_moves(case_name)

    def deselect_square(self):
        if self.case_selectionnee_id:
            self._highlight_square(self.case_selectionnee_id, False)
        self.case_selectionnee = None
        self.case_selectionnee_id = None
        self._clear_possible_moves()

    def try_player_move(self, move_str):
        # 1. Vérifier si c'est une promotion
        if self.game.is_a_promotion(move_str):
            # C'est une promotion : On ouvre la fenêtre et on ARRÊTE la fonction ici.
            self.pending_promotion_move = move_str
            self.deselect_square()
            self.open_promotion_window()
            return

        # 2. Vérifier si c'est un coup légal standard
        if self.game.test_move(move_str):
            self.finalize_move(move_str)
            self.deselect_square()
        else:
            # Coup invalide
            print("Coup invalide:", move_str)
            # On peut jouer un son d'erreur ici

    def finalize_move(self, move_str):
        """
        Applique le coup (validé) dans le moteur et met à jour l'interface.
        """
        # Capture pour l'affichage (avant le move)
        if self.game.test_capture(move_str):
            captured_sq = move_str[2:4]
            # Logique prise en passant un peu complexe à gérer juste avec le visuel,
            # ici on simplifie en prenant ce qu'il y a sur la case d'arrivée.
            # Stockfish gère la logique interne.
            pass 

        # 1. Jouer dans Stockfish
        self.game.move_piece(move_str)
        
        # 2. Historique
        self.move_history.append(move_str)
        
        # 3. Mises à jour
        self.update_board_visuals()
        self.update_taken_pieces()
        self.update_evaluation_bar()
        
        # 4. Changer tour
        self.turn_color = "b" if self.turn_color == "w" else "w"
        
        # 5. Si mode ordi, déclencher son tour
        if self.mode == "againstcomputer" and not self.stop:
            self.after(500, self.check_computer_turn)

    # ------------------------------------------------------------------
    # LOGIQUE ORDINATEUR
    # ------------------------------------------------------------------

    def check_computer_turn(self):
        if self.stop: return
        if self.mode == "againstcomputer" and self.turn_color != self.player_color:
            # L'IA calcule
            best_move = self.game.find_best_move()
            if best_move:
                self.finalize_move(best_move)
            else:
                print("Plus de coup possible (Mat ou Pat)")
                self.stop = True

    # ------------------------------------------------------------------
    # RENDU VISUEL
    # ------------------------------------------------------------------

    def update_board_visuals(self):
        # Effacer toutes les pièces
        for pid in self.pieces_on_board_ids:
            self.canvas_board.delete(pid)
        self.pieces_on_board_ids.clear()
        
        # Récupérer la matrice du plateau (nettoyée dans Game)
        board_matrix = self.game.get_board_array() # 8x8 matrix
        
        for r, row in enumerate(board_matrix):
            for c, piece_code in enumerate(row):
                if piece_code: # ex 'wp'
                    x = c * self.cell_size + self.largeur_labels
                    y = r * self.cell_size + self.largeur_labels
                    
                    if piece_code in self.images:
                        pid = self.canvas_board.create_image(x, y, anchor=tk.NW, image=self.images[piece_code])
                        self.pieces_on_board_ids[pid] = piece_code

    def _highlight_square(self, rect_id, enable):
        color = "grey" if enable else self.canvas_board.itemcget(rect_id, "fill").replace("grey", "lightgrey").replace("blue", "darkblue")
        # Logique simplifiée de couleur
        original_color = self.colors[0] if "light" in self.canvas_board.itemcget(rect_id, "fill") or "grey" == self.canvas_board.itemcget(rect_id, "fill") else self.colors[1]
        
        if enable:
            new_col = "grey" if original_color == "lightgrey" else "blue"
        else:
            # Restaurer la couleur originale basée sur la position
            # Hack rapide: on regarde juste si c'était foncé ou clair
            coords = self.canvas_board.coords(rect_id)
            # ... pour faire simple, on recalcule pas tout, on suppose juste :
            new_col = "lightgrey" if "grey" in self.canvas_board.itemcget(rect_id, "fill") else "darkblue"
            
            # Meilleure méthode : recalculer la couleur d'origine via les coordonnées
            # Mais pour l'instant, faisons simple :
            case_code = self.cases_map[rect_id]
            col_idx = ord(case_code[0]) - 97
            row_idx = 8 - int(case_code[1])
            new_col = self.colors[(row_idx + col_idx) % 2]

        self.canvas_board.itemconfig(rect_id, fill=new_col)

    def show_possible_moves(self, case_start):
        # Stockfish n'a pas de fonction "get legal moves for square" simple.
        # On va brute-force légèrement : tester les coups possibles
        letters = "abcdefgh"
        numbers = "12345678"
        
        for l in letters:
            for n in numbers:
                target = l + n
                move = case_start + target
                
                # Test move standard + capture
                is_valid = False
                color = "green" # move simple
                
                if self.game.test_move(move):
                    is_valid = True
                    if self.game.test_capture(move):
                        color = "red"
                elif self.game.test_move(move + "q"): # Test promotion
                    is_valid = True
                    color = "orange"
                
                if is_valid:
                    # Dessiner le rond
                    target_id = self.cases_map_rev[target]
                    coords = self.canvas_board.coords(target_id)
                    cx = (coords[0] + coords[2]) / 2
                    cy = (coords[1] + coords[3]) / 2
                    
                    dot_id = self.canvas_board.create_oval(cx-10, cy-10, cx+10, cy+10, fill=color, tags="overlay")
                    self.possibles_moves_ids.append(dot_id)

    def _clear_possible_moves(self):
        for pid in self.possibles_moves_ids:
            self.canvas_board.delete(pid)
        self.possibles_moves_ids.clear()

    def update_evaluation_bar(self):
        # Récupération eval
        typ, val = self.game.calculs_win_eval() # ['cp', 0.5] ou ['mate', 3]
        
        text_disp = "0.0"
        proportion = 0
        
        if typ == 'cp':
            text_disp = str(val)
            # Limiter visuellement à +/- 10 pions
            capped_val = max(min(val, 10), -10)
            proportion = (capped_val / 20) * self.board_size # échelle
        elif typ == 'mate':
            text_disp = f"M{val}"
            proportion = (self.board_size / 2) if val > 0 else -(self.board_size / 2)

        # Mettre à jour le rectangle noir
        # La barre totale fait self.board_size de haut
        # Le centre est à self.largeur_labels + self.board_size // 2
        center_y = self.largeur_labels + self.board_size // 2
        delta_h = proportion 
        
        # Le rectangle noir part du haut et descend.
        # Si avantage blanc (val > 0), le noir recule (bottom remonte)
        # Si avantage noir (val < 0), le noir avance (bottom descend)
        
        new_bottom = center_y - delta_h
        
        self.canvas_eval.coords(
            self.rect_eval_black,
            self.offset_bar, self.largeur_labels,
            self.dimension_bar[0] + self.offset_bar,
            new_bottom
        )
        self.canvas_eval.itemconfig(self.text_eval, text=text_disp)

    def update_taken_pieces(self):
        # Simplification : On recrée les listes visuelles basées sur le matériel manquant
        # Pour faire ça parfaitement, il faut comparer le board initial avec l'actuel.
        # Ici, on va juste nettoyer l'affichage pour l'instant car la logique de comptage précis est lourde
        # sans librairie externe.
        pass 

    # ------------------------------------------------------------------
    # PROMOTION (POPUP)
    # ------------------------------------------------------------------

    def open_promotion_window(self):
        win = tk.Toplevel(self)
        win.title("Promotion")
        win.geometry("100x350")
        
        cnv = tk.Canvas(win, width=100, height=350)
        cnv.pack()
        
        # Couleur du joueur actuel
        color_prefix = "w" if self.turn_color == "w" else "b"
        choices = ["q", "r", "b", "n"]
        
        for i, p_char in enumerate(choices):
            p_code = color_prefix + p_char
            if p_code in self.images:
                y = i * 85 + 10
                iid = cnv.create_image(50, y, image=self.images[p_code])
                # On utilise une lambda avec valeur par défaut pour capturer la variable
                cnv.tag_bind(iid, "<Button-1>", lambda e, c=p_char, w=win: self._on_promotion_choice(c, w))

    def _on_promotion_choice(self, choice_char, window):
        window.destroy()
        if self.pending_promotion_move:
            full_move = self.pending_promotion_move + choice_char # ex "a7a8q"
            self.finalize_move(full_move)
            self.pending_promotion_move = None

    # ------------------------------------------------------------------
    # PARAMÈTRES & UNDO
    # ------------------------------------------------------------------

    def open_parameters_window(self, event=None):
        win = tk.Toplevel(self)
        win.title("Paramètres")
        win.geometry("250x200")
        
        tk.Label(win, text="Niveau Elo").pack(pady=5)
        scale = tk.Scale(win, from_=100, to=3000, orient=tk.HORIZONTAL)
        scale.set(self.game.get_niv_elo())
        scale.pack()
        
        def save():
            self.game.set_difficulty(scale.get())
            self.canvas_top.itemconfig(self.text_opponent_elo, text=f"(Elo : {scale.get()})")
            win.destroy()
            
        tk.Button(win, text="Valider", command=save).pack(pady=20)

    def retour_arriere(self, event=None):
        # Smart Undo: Si c'est à nous de jouer, on annule les 2 derniers coups (IA + Joueur)
        # Si on joue contre un ami, on annule 1 coup.
        
        if not self.move_history: return
        
        pops = 1
        if self.mode == "againstcomputer" and len(self.move_history) >= 2:
            pops = 2
            
        for _ in range(pops):
            if self.move_history:
                self.move_history.pop()
        
        # Réinitialiser Stockfish à cet état
        # Stockfish a besoin de la position de départ + liste des coups
        self.game.reset_position(self.move_history)
        
        # Mise à jour UI
        self.update_board_visuals()
        self.update_evaluation_bar()
        
        # Si on a annulé un nombre impair de coups (contre ami), changer le tour
        if pops % 2 != 0:
            self.turn_color = "b" if self.turn_color == "w" else "w"

    def safe_destroy(self):
        self.stop = True
        try:
            self.game.close_engine()
        except:
            pass
        self.destroy()

# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------

if __name__ == "__main__":
    app = ChessGUI()
    app.mainloop()