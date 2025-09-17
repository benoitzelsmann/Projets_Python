import tkinter as tk
import cProfile

from PIL import Image, ImageTk

from Engine import Engine

""" Fonction à ajouter :

- retour arriere plus malin avec une sorte d'historique

"""


class ChessGUI(tk.Tk):
    """
    Main class for the Chess GUI application.
    Inherits from tkinter.Tk to create the main window.
    Handles the chess board display, user interactions, and game logic.
    """
    def __init__(self):
        """
        Initialize the Chess GUI application.
        Sets up the game state, board configuration, and UI components.
        """
        super().__init__()

        self.engine_color = 'b'
        self.mode = 'againstcomputer'

        self.choosed_detph = None
        self.choosed_detph_qs = None
        self.mode_choisi = None
        self.gear_window = None
        self.case_en_memoire = None
        self.case_numero_1 = None
        self.case_numero_2 = None
        self.window = None
        self.move_final_prom = None
        self.image_ids_prom = None
        self.advantage_engine_label = None
        self.advantage_you = None
        self.parameters = None
        self.gear_image = None

        self.board_visu = None
        self.canvas_3 = None
        self.canvas_4 = None
        self.frame_board = None
        self.eval_label = None
        self.proportion = None
        self.rectangle_eval = None
        self.canvas_2 = None

        self.files = None
        self.canvas = None
        self.stop = None
        self.move_eclaire = None

        self.dessins_ronds = []
        self.legende_adversaire = []
        self.new_case_selectionnee = []
        self.moves_a_jouer = []
        self.pieces_taken_draws_3 = []
        self.pieces_taken_draws_4 = []
        self.move_joues_cases = []
        self.move_joues = []

        self.moves_possibles = {}
        self.cases_index_with_case = {}
        self.cases_index_with_case_rev = {}
        self.pieces_index = {}
        self.images = {}
        self.images_mini = {}

        self.pieces_taken = {"white": [], "black": []}

        self.board_size = 80 * 8
        self.cell_size = 80
        self.radius = 10
        self.colors = ["lightgrey", "darkblue"]
        self.font_color = 'lightgrey'

        self.largeur_labels = 20
        self.canvas_size = (self.board_size + self.largeur_labels * 2, self.board_size + self.largeur_labels * 2)
        self.canvas_2_size = (60, self.board_size + self.largeur_labels * 2)
        self.dimension_bar = (35, self.board_size)
        self.offset_bar = (self.canvas_2_size[0] - self.dimension_bar[0]) // 2
        self.canvas_34_size = (self.canvas_size[0] + self.canvas_2_size[0] + 3, 70)
        self.dimension_button = (50, 50)

        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)

        self.player_color = 'b' if self.engine_color == 'w' else 'w'
        self.color_playing = "w"
        self.player_num = 0 if self.player_color == 'w' else 1

        self.Engine = Engine()

        self.initalisation_board()

        self.evaluation_game()
        self.update_images()
        self.updates_actions()

    def initalisation_board(self):
        """
        Initialize the chess board and UI components.
        Sets up the game window, chess board, evaluation bar, and player profiles.
        Binds events and loads piece images.
        """
        self.bind("<Left>", self.retour_arriere)
        self.title("Chess Board")
        self.configure(bg='white')
        self.size = 8
        self.geometry(f"{self.canvas_size[0] + self.canvas_2_size[0]}x"
                      f"{self.canvas_size[1] + self.canvas_34_size[1] * 2 + 20}")

        def draw_window():
            """
            Create and configure the main window parts.
            Sets up the engine profile, chess board canvas, evaluation bar, and player profile.
            """
            # Engine Profile
            self.canvas_3 = tk.Canvas(self, bg='lightgrey', width=self.canvas_34_size[0], height=self.canvas_34_size[1],
                                      highlightbackground=self.font_color)
            self.canvas_3.pack(side=tk.TOP)

            self.gear_image = ImageTk.PhotoImage(Image.open("parameters.png").resize(self.dimension_button))
            self.parameters = self.canvas_3.create_image((670, 20), anchor=tk.NW, image=self.gear_image)
            self.canvas_3.tag_bind(self.parameters, '<Button-1>', self.open_parameters_window)

            self.legende_adversaire += [
                self.canvas_3.create_text(30, 25, text="CHESS ENGINE", font=("Arial", 15), fill="black", anchor='w'),
                self.canvas_3.create_text(180, 25, text="(Elo : 1000)", font=("Arial", 13), fill="black", anchor='w')
            ]
            self.advantage_engine_label = self.canvas_3.create_text(280, 25, text='', font=("Arial", 13, "bold"),
                                                                    fill="black", anchor='w')

            """Frame for chess board and eval bar"""
            self.frame_board = tk.Frame(self)
            self.frame_board.pack(side=tk.TOP)

            # Echiquier
            self.canvas = tk.Canvas(self.frame_board, bg=self.font_color, width=self.canvas_size[0],
                                    height=self.canvas_size[1],
                                    highlightbackground=self.font_color)
            self.canvas.bind("<Button-1>", self.on_click)
            self.canvas.pack(side=tk.LEFT)

            # Barre d'évaluation (canvas_2)
            self.canvas_2 = tk.Canvas(self.frame_board, bg=self.font_color, width=self.canvas_2_size[0],
                                      height=self.canvas_2_size[1],
                                      highlightbackground=self.font_color)
            self.canvas_2.pack(side=tk.LEFT)

            self.canvas_2.create_rectangle(
                self.offset_bar, self.largeur_labels,
                self.dimension_bar[0] + self.offset_bar,
                self.canvas_2_size[1] - self.largeur_labels,
                fill="white"
            )

            self.rectangle_eval = self.canvas_2.create_rectangle(
                self.offset_bar, self.largeur_labels,
                self.dimension_bar[0] + self.offset_bar,
                self.largeur_labels + self.board_size // 2,
                fill="black"
            )

            self.eval_label = self.canvas_2.create_text(
                self.offset_bar + self.dimension_bar[0] // 2,
                self.dimension_bar[1] + 5,
                text="0.0", font=("Helvetica", 8, "bold"),
                fill="green"
            )

            """My Profile"""
            self.canvas_4 = tk.Canvas(self, bg='lightgrey', width=self.canvas_34_size[0], height=self.canvas_34_size[1],
                                      highlightbackground=self.font_color)
            self.canvas_4.pack(side=tk.TOP)

            self.canvas_4.create_text(30, 15, text="Road to GMMM", font=("Arial", 15), fill="black", anchor='w')
            self.canvas_4.create_text(180, 15, text="(Elo : 1500)", font=("Arial", 13), fill="black", anchor='w')

            self.advantage_you = self.canvas_4.create_text(280, 15, text='', font=("Arial", 13, "bold"), fill="black",
                                                           anchor='w')

        def draw_chessboard():
            """
            Create the visual chess board with squares and coordinates.
            Sets up the 8x8 grid with alternating colors and adds row/column labels.
            Maps chess notation (e.g., 'e4') to canvas rectangle IDs.
            """
            line = 8
            for row in range(self.size):
                icol = 0
                for col in range(self.size):
                    column = chr(65 + icol)
                    color = self.colors[(row + col) % 2]
                    x1 = col * self.cell_size + self.largeur_labels
                    y1 = row * self.cell_size + self.largeur_labels
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    index = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                    case = column.lower() + str(line)

                    self.cases_index_with_case[index] = case
                    self.cases_index_with_case_rev[case] = index

                    icol += 1
                line -= 1

            for col in range(self.size):
                x = col * self.cell_size + self.cell_size / 2 + self.largeur_labels
                y_bottom = self.board_size + self.largeur_labels * 3 / 2
                self.canvas.create_text(x, y_bottom, text=chr(65 + col), font=("Arial", 12, "bold"), fill="black")

            for row in range(self.size):
                x_right = self.board_size + self.largeur_labels * 3 / 2
                y = row * self.cell_size + self.cell_size / 2 + self.largeur_labels
                self.canvas.create_text(x_right, y, text=str(self.size - row), font=("Arial", 12, "bold"), fill="black")

        def path_pieces():
            """
            Load and prepare chess piece images.
            Creates two sets of images for each piece: regular size for the board
            and smaller size for displaying captured pieces.
            """
            names = ['wk', 'wq', 'wr', 'wb', 'wn', 'wp', 'bk', 'bq', 'br', 'bb', 'bn', 'bp']
            names_2 = ['K', 'Q', 'R', 'B', 'N', 'P', 'k', 'q', 'r', 'b', 'n', 'p']
            names_3 = [1, 900, 500, 325, 300, 100, -1, -900, -500, -325, -300, -100]

            for name1, name2 in zip(names, names_3):
                self.images[name2] = ImageTk.PhotoImage(
                    Image.open(f'pieces/{name1}.png').resize((int(self.cell_size), int(self.cell_size))))
                self.images_mini[name2] = ImageTk.PhotoImage(
                    Image.open(f'pieces/{name1}.png').resize((int(self.cell_size * 0.5), int(self.cell_size * 0.5))))

        draw_window()
        draw_chessboard()
        path_pieces()

    def fill_taken_pieces(self):
        """
        Update the display of captured pieces.
        Sorts captured pieces by value and displays them in the respective player's area.
        """
        self.pieces_taken["white"].sort(key=lambda x: x, reverse=True)
        self.pieces_taken["black"].sort(key=lambda x: x, reverse=True)

        for draw in self.pieces_taken_draws_3:
            self.canvas_3.delete(draw)

        for draw in self.pieces_taken_draws_4:
            self.canvas_4.delete(draw)

        for i, piece in enumerate(self.pieces_taken["white"]):
            draw = self.canvas_3.create_image((25 + i * 40, 35), anchor=tk.NW, image=self.images_mini[piece])
            self.pieces_taken_draws_3.append(draw)

        for i, piece in enumerate(self.pieces_taken["black"]):
            draw = self.canvas_4.create_image((25 + i * 40, 30), anchor=tk.NW, image=self.images_mini[piece])
            self.pieces_taken_draws_4.append(draw)

    def material_advantage(self):
        """
        Calculate and display the material advantage.
        Updates the UI to show which player has a material advantage and by how much.
        """
        material_adv = self.Engine.Eval.adv_piece_value()

        if material_adv < 0:
            self.canvas_3.itemconfig(self.advantage_engine_label, text=f'+ {- material_adv}')
            self.canvas_4.itemconfig(self.advantage_you, text='')
        elif material_adv > 0:
            self.canvas_4.itemconfig(self.advantage_you, text=f'+ {material_adv}')
            self.canvas_3.itemconfig(self.advantage_engine_label, text='')
        else:
            self.canvas_3.itemconfig(self.advantage_engine_label, text='')
            self.canvas_4.itemconfig(self.advantage_you, text='')

    def update_images(self):
        """
        Update the chess piece images on the board.
        Removes all existing piece images and redraws them based on the current board state.
        """
        for piece in self.pieces_index.keys():
            self.canvas.delete(piece)
            del piece

        for i, liste in enumerate(self.Engine.board):
            for j, piece in enumerate(liste):
                if piece != 0:
                    index = self.canvas.create_image(
                        (self.largeur_labels + j * self.cell_size,
                         self.largeur_labels + i * self.cell_size),
                        anchor=tk.NW, image=self.images[piece])
                    self.pieces_index[index] = piece

        self.canvas.update()

    def dark_case(self, case):
        """
        Darken the color of a chess square.
        Changes lightgrey to grey and darkblue to blue.

        Args:
            case: The canvas ID of the square to darken
        """
        actual_color = self.canvas.itemcget(case, 'fill')
        if actual_color == 'lightgrey':
            new_color = 'grey'
            self.canvas.itemconfig(case, fill=new_color)
        elif actual_color == 'darkblue':
            new_color = 'blue'
            self.canvas.itemconfig(case, fill=new_color)

    def light_case(self, case):
        """
        Lighten the color of a chess square.
        Changes grey to lightgrey and blue to darkblue.

        Args:
            case: The canvas ID of the square to lighten
        """
        actual_color = self.canvas.itemcget(case, 'fill')
        if actual_color == 'grey':
            new_color = 'lightgrey'
            self.canvas.itemconfig(case, fill=new_color)
        elif actual_color == 'blue':
            new_color = 'darkblue'
            self.canvas.itemconfig(case, fill=new_color)

    def show_last_move(self, move_cases, var):
        """
        Highlight or unhighlight the squares involved in the last move.

        Args:
            move_cases: String representation of the move (e.g., 'e2e4')
            var: Boolean indicating whether to unhighlight (True) or highlight (False) the squares
        """
        if move_cases:
            case1 = self.cases_index_with_case_rev[move_cases[:2]]
            case2 = self.cases_index_with_case_rev[move_cases[2:4]]

            if var:
                actual_color1 = self.canvas.itemcget(case1, 'fill')
                if actual_color1 == 'grey':
                    new_color = 'lightgrey'
                    self.canvas.itemconfig(case1, fill=new_color)
                elif actual_color1 == 'blue':
                    new_color = 'darkblue'
                    self.canvas.itemconfig(case1, fill=new_color)

                actual_color2 = self.canvas.itemcget(case2, 'fill')
                if actual_color2 == 'grey':
                    new_color = 'lightgrey'
                    self.canvas.itemconfig(case2, fill=new_color)
                elif actual_color2 == 'blue':
                    new_color = 'darkblue'
                    self.canvas.itemconfig(case2, fill=new_color)
            else:
                actual_color1 = self.canvas.itemcget(case1, 'fill')
                if actual_color1 == 'lightgrey':
                    new_color = 'grey'
                    self.canvas.itemconfig(case1, fill=new_color)
                elif actual_color1 == 'darkblue':
                    new_color = 'blue'
                    self.canvas.itemconfig(case1, fill=new_color)

                actual_color2 = self.canvas.itemcget(case2, 'fill')
                if actual_color2 == 'lightgrey':
                    new_color = 'grey'
                    self.canvas.itemconfig(case2, fill=new_color)
                elif actual_color2 == 'darkblue':
                    new_color = 'blue'
                    self.canvas.itemconfig(case2, fill=new_color)

    def on_click(self, event):
        """
        Handle mouse clicks on the chess board.
        Manages piece selection and move execution based on user clicks.

        Args:
            event: The mouse click event containing x and y coordinates
        """
        def show_moves_if_asked():
            """
            Show possible moves for the selected piece if appropriate.
            Only shows moves for pieces of the current player's color.
            """
            piece = self.Engine.get_what_is_on_square(self.case_numero_1)
            if self.mode == "againstcomputer":
                if (self.player_color == "w" and piece > 0) or (self.player_color == "b" and piece < 0):
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
                move = self.case_numero_1 + self.case_numero_2

                if self.Engine.test_move(self.color_playing, move):
                    # --- Case : valid move ---
                    self.moves_a_jouer.append(move)
                    self.light_case(self.case_en_memoire)
                    self.case_numero_1 = self.case_numero_2 = self.case_en_memoire = None
                else:
                    # --- Case : invalid move ---
                    self.light_case(self.case_en_memoire)
                    self.dark_case(case_index)
                    self.case_en_memoire = case_index
                    self.case_numero_1 = self.case_numero_2
                    self.case_numero_2 = None
                    show_moves_if_asked()

    def trouver_case_index(self, event):
        """
        Find the chess square at a given mouse position.

        Args:
            event: The mouse event containing x and y coordinates

        Returns:
            tuple: (canvas_id, chess_notation) of the square, or (None, None) if no square was clicked
        """
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        case_index = 0
        for item in items:
            if item <= 64:
                case_index = item
        if case_index != 0:
            case_coord = self.cases_index_with_case[case_index]
            return case_index, case_coord
        else:
            return None, None

    def open_parameters_window(self, event):
        """
        Open a settings window for configuring the chess engine and game mode.

        Args:
            event: The event that triggered the window opening
        """
        def update_legende():
            """
            Update the opponent legend based on the selected game mode.
            Changes the text displayed in the opponent's area.
            """
            if self.mode == 'againstcomputer':
                self.canvas_3.itemconfig(self.legende_adversaire[0], text=f"CHESS ENGINE")
                self.canvas_3.itemconfig(self.legende_adversaire[1], text=f"(Elo : 1000)")


            elif self.mode == 'againstfriend':
                self.canvas_3.itemconfig(self.legende_adversaire[0], text=f"Friendly match")
                self.canvas_3.itemconfig(self.legende_adversaire[1], text="")

        def enregistrer():
            """
            Save the settings and close the parameters window.
            Updates engine depth, quiescence search depth, and game mode.
            """
            depth = self.choosed_detph.get()
            qs_depht = self.choosed_detph_qs.get()
            self.Engine.set_depth(depth)
            self.Engine.qs_depht = qs_depht
            self.mode = self.mode_choisi.get()
            self.gear_window.destroy()
            update_legende()

        self.gear_window = tk.Toplevel(self.master)
        self.gear_window.geometry('250x260')
        self.gear_window.title("Paramètres du Bot")

        self.choosed_detph = tk.IntVar(value=self.Engine.depth)
        self.choosed_detph_qs = tk.IntVar(value=self.Engine.qs_depht)

        elo_label = tk.Label(self.gear_window, text="Profondeur de calcul")
        elo_label.pack(padx=20, pady=(10, 0))

        elo_scale = tk.Scale(self.gear_window, from_=1, to=10, orient="horizontal", length=200,
                             variable=self.choosed_detph)
        elo_scale.pack(padx=20, pady=0)

        depht_qs_label = tk.Label(self.gear_window, text="Profondeur de QS")
        depht_qs_label.pack(padx=20, pady=(10, 0))

        depht_qs_scale = tk.Scale(self.gear_window, from_=0, to=10, orient="horizontal", length=200,
                             variable=self.choosed_detph_qs)
        depht_qs_scale.pack(padx=20, pady=0)


        mode_label = tk.Label(self.gear_window, text="Mode de jeu")
        mode_label.pack(padx=20, pady=(10, 0))

        self.mode_choisi = tk.StringVar(value=self.mode)

        mode_computer = tk.Radiobutton(self.gear_window, text="Contre l'ordinateur", variable=self.mode_choisi,
                                       value="againstcomputer")
        mode_computer.pack(anchor="w", padx=20)

        mode_friend = tk.Radiobutton(self.gear_window, text="Contre un Ami", variable=self.mode_choisi,
                                     value="againstfriend")

        mode_friend.pack(anchor="w", padx=20)
        save_button = tk.Button(self.gear_window, text="Enregistrer", command=enregistrer)
        save_button.place(x=160, y=220)

    def promotion(self, list_move_coord):
        """
        Display a window for pawn promotion piece selection.

        Args:
            list_move_coord: List of possible promotion moves

        Returns:
            The selected promotion move is stored in self.move_final_prom
        """
        a, b = list_move_coord[0].start

        color = "w" if self.Engine.board[a][b] > 0 else "b"

        def not_choice():
            """
            Handle the case when no promotion piece is explicitly chosen.
            Defaults to the first option (usually queen) and closes the window.
            """
            self.move_final_prom = list_move_coord[0]
            self.window.destroy()
            self.window.quit()

        def on_image_double_click(idx):
            """
            Handle the selection of a promotion piece.

            Args:
                idx: Index of the selected piece (0=queen, 1=rook, 2=bishop, 3=knight)
            """
            choice = [900, 500, 325, 300][idx]

            for move in list_move_coord:
                if int(move.specificity[0:3]) == choice:
                    self.move_final_prom = move

            self.window.destroy()
            self.window.quit()

        self.window = tk.Toplevel(self)
        self.window.title("")
        self.window.canvas = tk.Canvas(self.window, width=100, height=330)

        self.window.canvas.pack()

        if color == "b":
            pieces = [-900, -500, -325, -300]
        else:
            pieces = [900, 500, 325, 300]

        self.image_ids_prom = []

        for i, piece in enumerate(pieces):
            x = 13
            y = 80 * i
            image_id = self.window.canvas.create_image(x, y, image=self.images[piece], anchor=tk.NW)
            self.image_ids_prom.append(image_id)
            self.window.canvas.tag_bind(image_id, "<Button-1>", lambda event, idx=i: on_image_double_click(idx))

        self.window.protocol("WM_DELETE_WINDOW", not_choice)

        self.window.mainloop()

    def evaluation_game(self):
        """
        Update the evaluation bar based on the current game state.
        Continuously updates to show the current advantage for either player.
        Uses the engine's evaluation function and schedules itself to run again after a delay.
        """
        eval_win = self.Engine.Eval.total_adv()

        self.proportion = eval_win / 20 * self.board_size
        text = str(eval_win)

        if self.proportion > self.board_size / 2:
            self.proportion = self.board_size / 2

        self.canvas_2.coords(self.rectangle_eval,
                             self.offset_bar,
                             self.largeur_labels,
                             self.dimension_bar[0] + self.offset_bar,
                             self.largeur_labels + self.board_size // 2 - self.proportion)

        self.canvas_2.itemconfig(self.eval_label, text=text)
        self.canvas.update()

        self.after(200, self.evaluation_game)

    def show_possible_moves(self, case):
        """
        Show the possible moves for a selected piece.
        Displays visual indicators on the board for legal moves.

        Args:
            case: Chess notation of the square containing the piece (e.g., 'e2')
        """
        def dessiner_ronds(cases):
            """
            Draw circles on the board to indicate possible moves.
            Different colors indicate different types of moves (capture, castle, etc.).

            Args:
                cases: List of possible moves with their types
            """
            def trad_case_coord(case_dessin):
                """
                Convert chess notation to canvas coordinates.

                Args:
                    case_dessin: Chess notation of a square (e.g., 'e4')

                Returns:
                    tuple: (x, y) coordinates on the canvas
                """
                coordx = 0
                for i, l in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']):
                    if l == case_dessin[0]:
                        coordx = i * self.cell_size + self.cell_size / 2 + self.largeur_labels
                coordy = (9 - int(case_dessin[1])) * self.cell_size - self.largeur_labels
                return coordx, coordy

            for element in cases:
                case_a_traiter = element[0]
                coord_x, coord_y = trad_case_coord(case_a_traiter)
                if element[1] is None:
                    self.dessins_ronds.append(
                        self.canvas.create_oval(coord_x - self.radius, coord_y - self.radius, coord_x + self.radius,
                                                coord_y + self.radius, fill='grey30'))
                elif "promotion" in element[1]:
                    self.dessins_ronds.append(
                        self.canvas.create_oval(coord_x - self.radius, coord_y - self.radius, coord_x + self.radius,
                                                coord_y + self.radius, fill='yellow'))

                elif "capture" in element[1]:
                    self.dessins_ronds.append(
                        self.canvas.create_oval(coord_x - self.radius, coord_y - self.radius, coord_x + self.radius,
                                                coord_y + self.radius, fill='red'))


                elif "castle" in element[1]:
                    self.dessins_ronds.append(
                        self.canvas.create_oval(coord_x - self.radius, coord_y - self.radius, coord_x + self.radius,
                                                coord_y + self.radius, fill='green'))

                elif element[1] == "doublepush":
                    self.dessins_ronds.append(
                        self.canvas.create_oval(coord_x - self.radius, coord_y - self.radius, coord_x + self.radius,
                                                coord_y + self.radius, fill='purple'))

        cases_possibles = self.Engine.moves_possibles_case(case, self.color_playing)

        dessiner_ronds(cases_possibles)

    def cacher_moves_possibles(self):
        """
        Hide the visual indicators for possible moves.
        Removes all circles that were drawn to show possible moves.
        """
        for element in self.dessins_ronds:
            self.canvas.delete(element)
            del element

    def updates_actions(self):
        """
        Handle the game flow and move execution.
        Manages player and computer moves based on the selected game mode.
        Schedules itself to run periodically to check for and execute moves.
        """
        def play_move(move_case_given, move_tot):
            """
            Execute a move on the board.
            Handles move execution, including special cases like promotion and captures.
            Updates the UI to reflect the new board state.

            Args:
                move_case_given: String representation of the move (e.g., 'e2e4')
                move_tot: Pre-calculated move object, if available
            """
            if move_case_given:
                if move_tot:
                    move_coord = move_tot
                else:

                    list_move_coord = self.Engine.test_move(self.color_playing, move_case_given)


                    if isinstance(list_move_coord, list):
                        self.promotion(list_move_coord)
                        move_coord = self.move_final_prom

                    else:
                        move_coord = list_move_coord

                print(move_coord)

                if move_coord.specificity is not None and "capture" in move_coord.specificity:
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

            if self.mode == 'againstfriend':

                if self.moves_a_jouer:
                    move = self.moves_a_jouer.pop(0)

                    play_move(move, None)

                    self.color_playing = "b" if self.color_playing == "w" else "w"

                    # for move_1 in self.Engine.Movement.find_all_possible_moves(self.color_playing, self.Engine.last_move):
                    #     print(move_1)
                    self.player_num = 1 - self.player_num

            elif self.mode == 'againstcomputer':

                if self.player_num == 0:
                    self.color_playing = self.player_color
                    if self.moves_a_jouer:
                        move = self.moves_a_jouer.pop(0)

                        play_move(move, None)

                        self.player_num = 1
                else:
                    self.color_playing = self.engine_color

                    # pr = cProfile.Profile()
                    # pr.enable()


                    move_case, best_move = self.Engine.find_best_move_cases(self.engine_color)
                    # pr.disable()
                    # pr.print_stats()

                    if move_case:

                        play_move(move_case, best_move)
                        self.player_num = 0
                    else:
                        self.stop = True

            self.after(100, self.updates_actions)

    def take_piece(self, case):
        """
        Record a captured piece.
        Adds the captured piece to the appropriate player's captured pieces list.

        Args:
            case: Chess notation of the square containing the captured piece
        """
        piece = self.Engine.get_what_is_on_square(case)
        if piece > 0:
            self.pieces_taken["white"].append(piece)
        elif piece < 0:
            self.pieces_taken["black"].append(piece)

    def retour_arriere(self, event):
        """
        Handle undoing the last two moves (one for each player).
        Resets the board to the state before the last two moves were made.

        Args:
            event: The event that triggered the undo action
        """
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
        """
        Safely close the application.
        Stops ongoing processes before destroying the window to prevent errors.
        """
        self.stop = True
        self.after(60, self.destroy)


def main():
    """
    Main entry point for the chess application.
    Creates and runs the ChessGUI instance.
    """
    board = ChessGUI()
    board.mainloop()


if __name__ == "__main__":
    main()
