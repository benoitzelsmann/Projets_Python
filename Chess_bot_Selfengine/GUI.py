import tkinter as tk
import os
from typing import Optional, List, Dict, Any, Tuple, Union
from PIL import Image, ImageTk

# Assure-toi que le fichier Engine.py est bien dans le même dossier
from Engine import Engine


class ChessGUI(tk.Tk):
    """
    Main class for the Chess GUI application.
    Inherits from tkinter.Tk to create the main window.
    Handles the chess board display, user interactions, and game logic.
    """

    def __init__(self):
        super().__init__()

        # --- 1. Configuration du Jeu ---
        self.engine_color: str = "b"
        self.mode: str = "againstcomputer"
        self.stop: bool = False
        self.proportion: float = 0.0

        # Dimensions et Couleurs
        self.board_size: int = 640  # 80 * 8
        self.cell_size: int = 80
        self.radius: int = 10
        self.colors: List[str] = ["lightgrey", "darkblue"]
        self.font_color: str = "lightgrey"
        self.largeur_labels: int = 20

        # Calcul des dimensions
        self.canvas_size: Tuple[int, int] = (
            self.board_size + self.largeur_labels * 2,
            self.board_size + self.largeur_labels * 2,
        )
        self.canvas_2_size: Tuple[int, int] = (
            60,
            self.board_size + self.largeur_labels * 2,
        )
        self.dimension_bar: Tuple[int, int] = (35, self.board_size)
        self.offset_bar: int = (self.canvas_2_size[0] - self.dimension_bar[0]) // 2
        self.canvas_34_size: Tuple[int, int] = (
            self.canvas_size[0] + self.canvas_2_size[0] + 3,
            70,
        )
        self.dimension_button: Tuple[int, int] = (50, 50)

        # --- 2. Initialisation du Moteur et Variables Logiques ---
        self.Engine = Engine()

        self.player_color: str = "b" if self.engine_color == "w" else "w"
        self.color_playing: str = "w"
        self.player_num: int = 0 if self.player_color == "w" else 1

        # Variables de mouvement (Indices de cases ou None)
        self.case_en_memoire: Optional[int] = None
        self.case_numero_1: Optional[str] = None
        self.case_numero_2: Optional[str] = None
        self.move_eclaire: Optional[str] = None
        self.move_final_prom: Any = None  # Objet Move du moteur

        # Listes et Dictionnaires
        self.dessins_ronds: List[int] = []  # IDs des objets graphiques
        self.legende_adversaire: List[int] = []
        self.moves_a_jouer: List[str] = []
        self.pieces_taken_draws_3: List[int] = []
        self.pieces_taken_draws_4: List[int] = []
        self.move_joues_cases: List[str] = []
        self.move_joues: List[Any] = []
        self.pieces_taken: Dict[str, List[int]] = {"white": [], "black": []}

        self.cases_index_with_case: Dict[int, str] = {}
        self.cases_index_with_case_rev: Dict[str, int] = {}
        self.pieces_index: Dict[int, int] = {}

        # Images (Clés: str pour les pièces, int pour les codes pièces du moteur)
        self.images: Dict[Union[str, int], ImageTk.PhotoImage] = {}
        self.images_mini: Dict[Union[str, int], ImageTk.PhotoImage] = {}

        # Fenêtres popup (restent Optional car créées à la demande)
        self.gear_window: Optional[tk.Toplevel] = None
        self.window: Optional[tk.Toplevel] = None
        self.image_ids_prom: List[int] = []

        # Variables Tkinter pour les paramètres
        self.choosed_detph = tk.IntVar(value=self.Engine.depth)
        self.choosed_detph_qs = tk.IntVar(value=self.Engine.qs_depht)
        self.mode_choisi = tk.StringVar(value=self.mode)

        # --- 3. Configuration de la Fenêtre Principale ---
        self.title("Chess Board")
        self.configure(bg="white")
        self.size = 8  # Taille grille logique
        self.geometry(
            f"{self.canvas_size[0] + self.canvas_2_size[0]}x"
            f"{self.canvas_size[1] + self.canvas_34_size[1] * 2 + 20}"
        )
        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)
        self.bind("<Left>", self.retour_arriere)

        # --- 4. Création DIRECTE des Widgets (Plus de None !) ---

        # 4.1 Header (Canvas 3 - Engine Profile)
        self.canvas_3 = tk.Canvas(
            self,
            bg="lightgrey",
            width=self.canvas_34_size[0],
            height=self.canvas_34_size[1],
            highlightbackground=self.font_color,
        )
        self.canvas_3.pack(side=tk.TOP)

        # 4.2 Frame central
        self.frame_board = tk.Frame(self)
        self.frame_board.pack(side=tk.TOP)

        # 4.3 Échiquier (Canvas Principal)
        self.canvas = tk.Canvas(
            self.frame_board,
            bg=self.font_color,
            width=self.canvas_size[0],
            height=self.canvas_size[1],
            highlightbackground=self.font_color,
        )
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<Button-1>", self.on_click)

        # 4.4 Barre d'évaluation (Canvas 2)
        self.canvas_2 = tk.Canvas(
            self.frame_board,
            bg=self.font_color,
            width=self.canvas_2_size[0],
            height=self.canvas_2_size[1],
            highlightbackground=self.font_color,
        )
        self.canvas_2.pack(side=tk.LEFT)

        # 4.5 Footer (Canvas 4 - User Profile)
        self.canvas_4 = tk.Canvas(
            self,
            bg="lightgrey",
            width=self.canvas_34_size[0],
            height=self.canvas_34_size[1],
            highlightbackground=self.font_color,
        )
        self.canvas_4.pack(side=tk.TOP)

        # --- 5. Chargement des Assets et Dessin Initial ---
        self._load_assets()
        self._draw_static_ui()
        self._draw_board_grid()

        # --- 6. Lancement des boucles de jeu ---
        self.evaluation_game()
        self.update_images()
        self.updates_actions()

    # ------------------------------------------------------------------
    # MÉTHODES D'INITIALISATION (Assets & UI)
    # ------------------------------------------------------------------

    def _load_assets(self):
        """Load images and icons."""
        current_dir = os.path.dirname(__file__)

        # Charger l'icône paramètre
        try:
            param_path = os.path.join(current_dir, "parameters.png")
            img_param = Image.open(param_path).resize(self.dimension_button)
            self.gear_image = ImageTk.PhotoImage(img_param)
        except Exception as e:
            print(f"Warning: parameters.png not found or error: {e}")
            self.gear_image = None

        # Charger les pièces d'échecs
        names = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp"]
        names_codes = [1, 900, 500, 325, 300, 100, -1, -900, -500, -325, -300, -100]

        for name_str, name_code in zip(names, names_codes):
            try:
                # Construit le chemin: dossier_courant/pieces/wk.png
                path = os.path.join(current_dir, "pieces", f"{name_str}.png")
                img = Image.open(path)

                # Image taille normale
                self.images[name_code] = ImageTk.PhotoImage(
                    img.resize((int(self.cell_size), int(self.cell_size)))
                )
                # Image taille mini (pour pièces prises)
                self.images_mini[name_code] = ImageTk.PhotoImage(
                    img.resize((int(self.cell_size * 0.5), int(self.cell_size * 0.5)))
                )
            except Exception as e:
                print(f"Error loading piece {name_str}: {e}")

    def _draw_static_ui(self):
        """Draw texts, eval bar structure, and buttons."""
        # --- Canvas 3 (Adversaire) ---
        if self.gear_image:
            self.parameters = self.canvas_3.create_image(
                (670, 20), anchor=tk.NW, image=self.gear_image
            )
            self.canvas_3.tag_bind(
                self.parameters, "<Button-1>", self.open_parameters_window
            )

        self.legende_adversaire = [
            self.canvas_3.create_text(
                30,
                25,
                text="CHESS ENGINE",
                font=("Arial", 15),
                fill="black",
                anchor="w",
            ),
            self.canvas_3.create_text(
                180,
                25,
                text="(Elo : 1000)",
                font=("Arial", 13),
                fill="black",
                anchor="w",
            ),
        ]
        self.advantage_engine_label = self.canvas_3.create_text(
            280, 25, text="", font=("Arial", 13, "bold"), fill="black", anchor="w"
        )

        # --- Canvas 4 (Joueur) ---
        self.canvas_4.create_text(
            30, 15, text="Road to GMMM", font=("Arial", 15), fill="black", anchor="w"
        )
        self.canvas_4.create_text(
            180, 15, text="(Elo : 1500)", font=("Arial", 13), fill="black", anchor="w"
        )
        self.advantage_you = self.canvas_4.create_text(
            280, 15, text="", font=("Arial", 13, "bold"), fill="black", anchor="w"
        )

        # --- Canvas 2 (Barre d'évaluation) ---
        # Fond blanc
        self.canvas_2.create_rectangle(
            self.offset_bar,
            self.largeur_labels,
            self.dimension_bar[0] + self.offset_bar,
            self.canvas_2_size[1] - self.largeur_labels,
            fill="white",
        )
        # Rectangle noir dynamique
        self.rectangle_eval = self.canvas_2.create_rectangle(
            self.offset_bar,
            self.largeur_labels,
            self.dimension_bar[0] + self.offset_bar,
            self.largeur_labels + self.board_size // 2,
            fill="black",
        )
        # Texte score
        self.eval_label = self.canvas_2.create_text(
            self.offset_bar + self.dimension_bar[0] // 2,
            self.dimension_bar[1] + 5,
            text="0.0",
            font=("Helvetica", 8, "bold"),
            fill="green",
        )

    def _draw_board_grid(self):
        """Draw the chessboard squares and coordinates."""
        line = 8
        for row in range(self.size):
            for col in range(self.size):
                column = chr(65 + col)
                color = self.colors[(row + col) % 2]

                x1 = col * self.cell_size + self.largeur_labels
                y1 = row * self.cell_size + self.largeur_labels
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                index = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="black"
                )

                case_coord = column.lower() + str(line)
                self.cases_index_with_case[index] = case_coord
                self.cases_index_with_case_rev[case_coord] = index

            line -= 1

        # Text Coordinates (Letters A-H)
        for col in range(self.size):
            x = col * self.cell_size + self.cell_size / 2 + self.largeur_labels
            y_bottom = self.board_size + self.largeur_labels * 3 / 2
            self.canvas.create_text(
                x,
                y_bottom,
                text=chr(65 + col),
                font=("Arial", 12, "bold"),
                fill="black",
            )

        # Text Coordinates (Numbers 1-8)
        for row in range(self.size):
            x_right = self.board_size + self.largeur_labels * 3 / 2
            y = row * self.cell_size + self.cell_size / 2 + self.largeur_labels
            self.canvas.create_text(
                x_right,
                y,
                text=str(self.size - row),
                font=("Arial", 12, "bold"),
                fill="black",
            )

    # ------------------------------------------------------------------
    # LOGIQUE DE JEU & INTERACTION
    # ------------------------------------------------------------------

    def on_click(self, event):
        """Handle mouse clicks on the chess board."""

        def show_moves_if_asked():
            piece = self.Engine.get_what_is_on_square(self.case_numero_1)
            if self.mode == "againstcomputer":
                if (self.player_color == "w" and piece > 0) or (
                    self.player_color == "b" and piece < 0
                ):
                    self.show_possible_moves(self.case_numero_1)
            elif self.mode == "againstfriend":
                self.show_possible_moves(self.case_numero_1)

        # --- Case : first case chosen ---
        if self.case_numero_1 is None:
            case_index, self.case_numero_1 = self.trouver_case_index(event)
            if case_index or self.case_numero_1:
                self.dark_case(case_index)
                self.case_en_memoire = case_index
                show_moves_if_asked()

        # --- Case: second case chosen ---
        elif self.case_numero_2 is None:
            self.cacher_moves_possibles()
            case_index, self.case_numero_2 = self.trouver_case_index(event)

            if case_index or self.case_numero_2:
                # Ensure cases are not None before concatenating
                if self.case_numero_1 and self.case_numero_2:
                    move = str(self.case_numero_1) + str(self.case_numero_2)

                    if self.Engine.test_move(self.color_playing, move):
                        # --- Valid move ---
                        self.moves_a_jouer.append(move)
                        self.light_case(self.case_en_memoire)
                        self.case_numero_1 = None
                        self.case_numero_2 = None
                        self.case_en_memoire = None
                    else:
                        # --- Invalid move ---
                        self.light_case(self.case_en_memoire)
                        self.dark_case(case_index)
                        self.case_en_memoire = case_index
                        self.case_numero_1 = self.case_numero_2
                        self.case_numero_2 = None
                        show_moves_if_asked()

    def trouver_case_index(self, event) -> Tuple[Optional[int], Optional[str]]:
        """Find the chess square at a given mouse position."""
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        case_index = 0
        for item in items:
            # Les rectangles des cases ont des ID bas, les images des ID hauts
            if item <= 64:
                case_index = item

        if case_index != 0:
            case_coord = self.cases_index_with_case.get(case_index)
            return case_index, case_coord
        else:
            return None, None

    def updates_actions(self):
        """Game loop to handle moves from player and engine."""

        def play_move(move_case_given, move_tot):
            if move_case_given:
                if move_tot:
                    move_coord = move_tot
                else:
                    list_move_coord = self.Engine.test_move(
                        self.color_playing, move_case_given
                    )
                    if isinstance(list_move_coord, list):
                        self.promotion(list_move_coord)
                        move_coord = self.move_final_prom
                    else:
                        move_coord = list_move_coord

                print(move_coord)

                # "specificity" attribute access on move_coord (Any type)
                if hasattr(move_coord, "specificity") and move_coord.specificity:
                    if "capture" in move_coord.specificity:
                        self.take_piece(move_case_given[2:4])

                self.show_last_move(self.move_eclaire, True)

                self.move_joues.append(move_coord)
                self.Engine.Movement.do_move(move_coord)
                self.Engine.last_move = move_coord

                self.show_last_move(move_case_given, False)
                self.move_eclaire = move_case_given

                self.move_joues_cases.append(move_case_given)
                self.update_images()

                self.fill_taken_pieces()
                self.material_advantage()

        if not self.stop:
            if self.mode == "againstfriend":
                if self.moves_a_jouer:
                    move = self.moves_a_jouer.pop(0)
                    play_move(move, None)
                    self.color_playing = "b" if self.color_playing == "w" else "w"
                    self.player_num = 1 - self.player_num

            elif self.mode == "againstcomputer":
                if self.player_num == 0:
                    self.color_playing = self.player_color
                    if self.moves_a_jouer:
                        move = self.moves_a_jouer.pop(0)
                        play_move(move, None)
                        self.player_num = 1
                else:
                    self.color_playing = self.engine_color
                    move_case, best_move = self.Engine.find_best_move_cases(
                        self.engine_color
                    )
                    if move_case:
                        play_move(move_case, best_move)
                        self.player_num = 0
                    else:
                        self.stop = True

            self.after(100, self.updates_actions)

    # ------------------------------------------------------------------
    # GESTION DES PIÈCES & VISUELS
    # ------------------------------------------------------------------

    def update_images(self):
        """Redraw pieces on the board."""
        for piece in self.pieces_index.keys():
            self.canvas.delete(piece)

        self.pieces_index.clear()

        for i, liste in enumerate(self.Engine.board):
            for j, piece in enumerate(liste):
                if piece != 0:
                    index = self.canvas.create_image(
                        (
                            self.largeur_labels + j * self.cell_size,
                            self.largeur_labels + i * self.cell_size,
                        ),
                        anchor=tk.NW,
                        image=self.images[piece],
                    )
                    self.pieces_index[index] = piece

        self.canvas.update()

    def fill_taken_pieces(self):
        """Update captured pieces visualization."""
        self.pieces_taken["white"].sort(key=lambda x: x, reverse=True)
        self.pieces_taken["black"].sort(key=lambda x: x, reverse=True)

        for draw in self.pieces_taken_draws_3:
            self.canvas_3.delete(draw)
        self.pieces_taken_draws_3.clear()

        for draw in self.pieces_taken_draws_4:
            self.canvas_4.delete(draw)
        self.pieces_taken_draws_4.clear()

        for i, piece in enumerate(self.pieces_taken["white"]):
            draw = self.canvas_3.create_image(
                (25 + i * 40, 35), anchor=tk.NW, image=self.images_mini[piece]
            )
            self.pieces_taken_draws_3.append(draw)

        for i, piece in enumerate(self.pieces_taken["black"]):
            draw = self.canvas_4.create_image(
                (25 + i * 40, 30), anchor=tk.NW, image=self.images_mini[piece]
            )
            self.pieces_taken_draws_4.append(draw)

    def take_piece(self, case):
        piece = self.Engine.get_what_is_on_square(case)
        if piece > 0:
            self.pieces_taken["white"].append(piece)
        elif piece < 0:
            self.pieces_taken["black"].append(piece)

    def material_advantage(self):
        material_adv = self.Engine.Eval.adv_piece_value()
        if material_adv < 0:
            self.canvas_3.itemconfig(
                self.advantage_engine_label, text=f"+ {- material_adv}"
            )
            self.canvas_4.itemconfig(self.advantage_you, text="")
        elif material_adv > 0:
            self.canvas_4.itemconfig(self.advantage_you, text=f"+ {material_adv}")
            self.canvas_3.itemconfig(self.advantage_engine_label, text="")
        else:
            self.canvas_3.itemconfig(self.advantage_engine_label, text="")
            self.canvas_4.itemconfig(self.advantage_you, text="")

    def evaluation_game(self):
        eval_win = self.Engine.Eval.total_adv()
        self.proportion = eval_win / 20 * self.board_size
        text = str(eval_win)

        if self.proportion > self.board_size / 2:
            self.proportion = self.board_size / 2

        self.canvas_2.coords(
            self.rectangle_eval,
            self.offset_bar,
            self.largeur_labels,
            self.dimension_bar[0] + self.offset_bar,
            self.largeur_labels + self.board_size // 2 - self.proportion,
        )

        self.canvas_2.itemconfig(self.eval_label, text=text)
        self.canvas.update()
        self.after(200, self.evaluation_game)

    # ------------------------------------------------------------------
    # HIGHLIGHTS & DESSINS
    # ------------------------------------------------------------------

    def dark_case(self, case):
        if case is None:
            return
        actual_color = self.canvas.itemcget(case, "fill")
        if actual_color == "lightgrey":
            self.canvas.itemconfig(case, fill="grey")
        elif actual_color == "darkblue":
            self.canvas.itemconfig(case, fill="blue")

    def light_case(self, case):
        if case is None:
            return
        actual_color = self.canvas.itemcget(case, "fill")
        if actual_color == "grey":
            self.canvas.itemconfig(case, fill="lightgrey")
        elif actual_color == "blue":
            self.canvas.itemconfig(case, fill="darkblue")

    def show_last_move(self, move_cases, unhighlight_flag):
        if move_cases:
            case1 = self.cases_index_with_case_rev.get(move_cases[:2])
            case2 = self.cases_index_with_case_rev.get(move_cases[2:4])

            if case1 and case2:
                if unhighlight_flag:
                    self.light_case(case1)
                    self.light_case(case2)
                else:
                    self.dark_case(case1)
                    self.dark_case(case2)

    def show_possible_moves(self, case):
        if case is None:
            return

        def dessiner_ronds(cases):
            def trad_case_coord(case_dessin):
                coordx = 0
                for i, l in enumerate(["a", "b", "c", "d", "e", "f", "g", "h"]):
                    if l == case_dessin[0]:
                        coordx = (
                            i * self.cell_size
                            + self.cell_size / 2
                            + self.largeur_labels
                        )
                coordy = (
                    9 - int(case_dessin[1])
                ) * self.cell_size - self.largeur_labels
                return coordx, coordy

            for element in cases:
                case_a_traiter = element[0]
                coord_x, coord_y = trad_case_coord(case_a_traiter)
                fill_color = "grey30"

                if element[1] is None:
                    fill_color = "grey30"
                elif "promotion" in element[1]:
                    fill_color = "yellow"
                elif "capture" in element[1]:
                    fill_color = "red"
                elif "castle" in element[1]:
                    fill_color = "green"
                elif element[1] == "doublepush":
                    fill_color = "purple"

                self.dessins_ronds.append(
                    self.canvas.create_oval(
                        coord_x - self.radius,
                        coord_y - self.radius,
                        coord_x + self.radius,
                        coord_y + self.radius,
                        fill=fill_color,
                    )
                )

        cases_possibles = self.Engine.moves_possibles_case(case, self.color_playing)
        dessiner_ronds(cases_possibles)

    def cacher_moves_possibles(self):
        for element in self.dessins_ronds:
            self.canvas.delete(element)
        self.dessins_ronds.clear()

    # ------------------------------------------------------------------
    # FENÊTRES SECONDAIRES & PARAMÈTRES
    # ------------------------------------------------------------------

    def promotion(self, list_move_coord):
        # Sécurisation des types et accès
        if not list_move_coord:
            return

        # Supposons que Move a un attribut 'start'
        a, b = list_move_coord[0].start
        color = "w" if self.Engine.board[a][b] > 0 else "b"

        def not_choice():
            self.move_final_prom = list_move_coord[0]
            if self.window:
                self.window.destroy()
                self.window.quit()

        def on_image_double_click(idx):
            choice = [900, 500, 325, 300][idx]
            for move in list_move_coord:
                if int(move.specificity[0:3]) == choice:
                    self.move_final_prom = move

            if self.window:
                self.window.destroy()
                self.window.quit()

        self.window = tk.Toplevel(self)
        self.window.title("Promotion")
        # On attache le canvas au topLevel
        cnv = tk.Canvas(self.window, width=100, height=330)
        cnv.pack()

        pieces_codes = (
            [-900, -500, -325, -300] if color == "b" else [900, 500, 325, 300]
        )
        self.image_ids_prom = []

        for i, piece in enumerate(pieces_codes):
            x = 13
            y = 80 * i
            if piece in self.images:
                image_id = cnv.create_image(
                    x, y, image=self.images[piece], anchor=tk.NW
                )
                self.image_ids_prom.append(image_id)
                cnv.tag_bind(
                    image_id,
                    "<Button-1>",
                    lambda event, idx=i: on_image_double_click(idx),
                )

        self.window.protocol("WM_DELETE_WINDOW", not_choice)
        self.window.mainloop()

    def open_parameters_window(self, event):
        def update_legende():
            # Mise à jour des textes selon le mode
            if self.mode == "againstcomputer":
                self.canvas_3.itemconfig(
                    self.legende_adversaire[0], text="CHESS ENGINE"
                )
                self.canvas_3.itemconfig(
                    self.legende_adversaire[1], text="(Elo : 1000)"
                )
            elif self.mode == "againstfriend":
                self.canvas_3.itemconfig(
                    self.legende_adversaire[0], text="Friendly match"
                )
                self.canvas_3.itemconfig(self.legende_adversaire[1], text="")

        def enregistrer():
            self.Engine.set_depth(self.choosed_detph.get())
            self.Engine.qs_depht = self.choosed_detph_qs.get()
            self.mode = self.mode_choisi.get()
            if self.gear_window:
                self.gear_window.destroy()
            update_legende()

        self.gear_window = tk.Toplevel(self)
        self.gear_window.geometry("250x260")
        self.gear_window.title("Paramètres du Bot")

        # Update vars
        self.choosed_detph.set(self.Engine.depth)
        self.choosed_detph_qs.set(self.Engine.qs_depht)
        self.mode_choisi.set(self.mode)

        tk.Label(self.gear_window, text="Profondeur de calcul").pack(
            padx=20, pady=(10, 0)
        )
        tk.Scale(
            self.gear_window,
            from_=1,
            to=10,
            orient="horizontal",
            length=200,
            variable=self.choosed_detph,
        ).pack(padx=20)

        tk.Label(self.gear_window, text="Profondeur de QS").pack(padx=20, pady=(10, 0))
        tk.Scale(
            self.gear_window,
            from_=0,
            to=10,
            orient="horizontal",
            length=200,
            variable=self.choosed_detph_qs,
        ).pack(padx=20)

        tk.Label(self.gear_window, text="Mode de jeu").pack(padx=20, pady=(10, 0))
        tk.Radiobutton(
            self.gear_window,
            text="Contre l'ordinateur",
            variable=self.mode_choisi,
            value="againstcomputer",
        ).pack(anchor="w", padx=20)
        tk.Radiobutton(
            self.gear_window,
            text="Contre un Ami",
            variable=self.mode_choisi,
            value="againstfriend",
        ).pack(anchor="w", padx=20)

        tk.Button(self.gear_window, text="Enregistrer", command=enregistrer).place(
            x=160, y=220
        )

    def retour_arriere(self, event):
        """Undo the last round of moves."""
        if len(self.move_joues) >= 2:
            self.show_last_move(self.move_eclaire, True)
            self.move_joues_cases.pop(-1)
            self.move_joues_cases.pop(-1)
            self.move_joues.pop(-1)
            self.move_joues.pop(-1)

            self.Engine.reset()
            for move in self.move_joues:
                self.Engine.Movement.do_move(move)

            self.update_images()

    def safe_destroy(self):
        self.stop = True
        self.after(60, self.destroy)


def main():
    board = ChessGUI()
    board.mainloop()


if __name__ == "__main__":
    main()
