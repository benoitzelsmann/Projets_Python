import tkinter as tk

from PIL import Image, ImageTk

from Stock_bot import Game
from init import Init


""" Fonction à ajouter :

- retour arriere plus malin avec une sorte d'historique
- safe close
- promotion semble avoir un socui

"""


class ChessGUI(tk.Tk, Init):
    def __init__(self):
        super().__init__()
        Init.__init__(self)

        self.mode = "againstcomputer"

        self.game = Game(100)
        self.game_pro = Game(2000)

        self.bind("<Left>", self.retour_arriere)

        self.title("Chess Board")
        self.configure(bg="white")
        self.geometry(
            f"{self.canvas_size[0] + self.canvas_2_size[0]}x"
            f"{self.canvas_size[1] + self.canvas_34_size[1] * 2 + 20}"
        )
        self.size = 8

        # self.bind("<Right>", self.retour_avant)

        self.initalisation_board()

        self.evaluation_game()
        self.update_images()
        self.updates_actions()

    def initalisation_board(self):

        def draw_window():
            self.canvas_3 = tk.Canvas(
                self,
                bg="lightgrey",
                width=self.canvas_34_size[0],
                height=self.canvas_34_size[1],
                highlightbackground=self.font_color,
            )
            self.canvas_3.pack(side=tk.TOP)

            self.gear_image = ImageTk.PhotoImage(
                Image.open("parameters.png").resize(self.dimension_button)
            )
            self.parameters = self.canvas_3.create_image(
                (670, 20), anchor=tk.NW, image=self.gear_image
            )
            self.canvas_3.tag_bind(
                self.parameters, "<Button-1>", self.open_parameters_window
            )

            self.legende_adversaire.append(
                self.canvas_3.create_text(
                    70, 20, text=f"Stockfish", font=("Arial", 15), fill="Black"
                )
            )
            self.legende_adversaire.append(
                self.canvas_3.create_text(
                    160,
                    20,
                    text=f"(Elo : {self.game.get_niv_elo()})",
                    font=("Arial", 13),
                    fill="Black",
                )
            )

            self.advantage_stock = self.canvas_3.create_text(
                250, 20, text="", font=("Arial", 13, "bold"), fill="black"
            )

            self.frame_board = tk.Frame(self)
            self.frame_board.pack(side=tk.TOP)

            self.canvas = tk.Canvas(
                self.frame_board,
                bg=self.font_color,
                width=self.canvas_size[0],
                height=self.canvas_size[1],
                highlightbackground=self.font_color,
            )

            self.canvas.bind("<Button-1>", self.on_click)

            self.canvas.pack(side=tk.LEFT)

            self.canvas_2 = tk.Canvas(
                self.frame_board,
                bg=self.font_color,
                width=self.canvas_2_size[0],
                height=self.canvas_2_size[1],
                highlightbackground=self.font_color,
            )
            self.canvas_2.pack(side=tk.LEFT)

            self.canvas_2.create_rectangle(
                self.offset_bar,
                self.largeur_labels,
                self.dimension_bar[0] + self.offset_bar,
                self.canvas_2_size[1] - self.largeur_labels,
                fill="white",
            )

            self.rectangle_eval = self.canvas_2.create_rectangle(
                self.offset_bar,
                self.largeur_labels,
                self.dimension_bar[0] + self.offset_bar,
                self.largeur_labels + self.board_size // 2,
                fill="black",
            )

            self.eval_label = self.canvas_2.create_text(
                self.offset_bar + self.dimension_bar[0] // 2,
                self.dimension_bar[1] + 5,
                text=0.0,
                font=("Helvetica", 8, "bold"),
                fill="green",
            )

            self.canvas_4 = tk.Canvas(
                self,
                bg="lightgrey",
                width=self.canvas_34_size[0],
                height=self.canvas_34_size[1],
                highlightbackground=self.font_color,
            )
            self.canvas_4.pack(side=tk.TOP)

            self.canvas_4.create_text(
                100, 15, text=f"Road to GMMM", font=("Arial", 15), fill="Black"
            )
            self.advantage_you = self.canvas_4.create_text(
                200, 15, text="", font=("Arial", 13, "bold"), fill="black"
            )

        def draw_chessboard():
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
                    index = self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=color, outline="black"
                    )

                    case = column.lower() + str(line)

                    self.cases_index_with_case[index] = case
                    self.cases_index_with_case_rev[case] = index

                    icol += 1
                line -= 1

        def path_pieces():
            names = [
                "wk",
                "wq",
                "wr",
                "wb",
                "wn",
                "wp",
                "bk",
                "bq",
                "br",
                "bb",
                "bn",
                "bp",
            ]
            self.images = {
                name: ImageTk.PhotoImage(
                    Image.open(f"pieces/{name}.png").resize(
                        (int(self.cell_size), int(self.cell_size))
                    )
                )
                for name in names
            }
            self.images_mini = {
                name: ImageTk.PhotoImage(
                    Image.open(f"pieces/{name}.png").resize(
                        (int(self.cell_size * 0.5), int(self.cell_size * 0.5))
                    )
                )
                for name in names
            }

        draw_window()
        draw_chessboard()
        path_pieces()

    def fill_taken_pieces(self):

        self.pieces_taken["white"].sort(
            key=lambda x: self.piece_values[x[1]], reverse=True
        )
        self.pieces_taken["black"].sort(
            key=lambda x: self.piece_values[x[1]], reverse=True
        )

        for draw in self.pieces_taken_draws_3:
            self.canvas_3.delete(draw)

        for draw in self.pieces_taken_draws_4:
            self.canvas_4.delete(draw)

        for i, piece in enumerate(self.pieces_taken["white"]):
            draw = self.canvas_3.create_image(
                (25 + i * 40, 30), anchor=tk.NW, image=self.images_mini[piece]
            )
            self.pieces_taken_draws_3.append(draw)

        for i, piece in enumerate(self.pieces_taken["black"]):
            draw = self.canvas_4.create_image(
                (25 + i * 40, 30), anchor=tk.NW, image=self.images_mini[piece]
            )
            self.pieces_taken_draws_4.append(draw)

    def advantage(self):

        def update_sets_pieces():
            white = []
            black = []
            self.board_visu = self.game.get_board()
            for liste in self.board_visu:
                for piece1 in liste:
                    if piece1 is not None:
                        if piece1[0] == "w":
                            white.append(piece1)
                        elif piece1[0] == "b":
                            black.append(piece1)

            self.pieces_restantes_white = white
            self.pieces_restantes_black = black

        update_sets_pieces()

        stock = 0
        you = 0

        for piece in self.pieces_restantes_white:
            stock += self.piece_values[piece[1]]
        for piece in self.pieces_restantes_black:
            you += self.piece_values[piece[1]]
        diff = you - stock

        if diff > 0:
            self.canvas_3.itemconfig(self.advantage_stock, text=f"+ {diff}")
            self.canvas_4.itemconfig(self.advantage_you, text="")
        elif diff < 0:
            self.canvas_4.itemconfig(self.advantage_you, text=f"+ {- diff}")
            self.canvas_3.itemconfig(self.advantage_stock, text="")
        else:
            self.canvas_3.itemconfig(self.advantage_stock, text="")
            self.canvas_4.itemconfig(self.advantage_you, text="")

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

    def update_images(self):
        for piece in self.pieces_index.keys():
            self.canvas.delete(piece)
            del piece

        self.board_visu = self.game.get_board()
        for i, liste in enumerate(self.board_visu):
            for j, piece in enumerate(liste):
                if piece is not None:
                    index = self.canvas.create_image(
                        (
                            self.largeur_labels + j * self.cell_size,
                            self.largeur_labels + i * self.cell_size,
                        ),
                        anchor=tk.NW,
                        image=self.images[piece],
                    )
                    self.pieces_index[index] = piece

    def assombrir_case(self, case):
        actual_color = self.canvas.itemcget(case, "fill")
        if actual_color == "lightgrey":
            new_color = "grey"
            self.canvas.itemconfig(case, fill=new_color)
        elif actual_color == "darkblue":
            new_color = "blue"
            self.canvas.itemconfig(case, fill=new_color)

    def eclairer_case(self, case):
        actual_color = self.canvas.itemcget(case, "fill")
        if actual_color == "grey":
            new_color = "lightgrey"
            self.canvas.itemconfig(case, fill=new_color)
        elif actual_color == "blue":
            new_color = "darkblue"
            self.canvas.itemconfig(case, fill=new_color)

    def afficher_coup(self, coup, var):

        if coup:

            case1 = self.cases_index_with_case_rev[coup[:2]]
            case2 = self.cases_index_with_case_rev[coup[2:4]]

            if var:
                actual_color1 = self.canvas.itemcget(case1, "fill")
                if actual_color1 == "grey":
                    new_color = "lightgrey"
                    self.canvas.itemconfig(case1, fill=new_color)
                elif actual_color1 == "blue":
                    new_color = "darkblue"
                    self.canvas.itemconfig(case1, fill=new_color)

                actual_color2 = self.canvas.itemcget(case2, "fill")
                if actual_color2 == "grey":
                    new_color = "lightgrey"
                    self.canvas.itemconfig(case2, fill=new_color)
                elif actual_color2 == "blue":
                    new_color = "darkblue"
                    self.canvas.itemconfig(case2, fill=new_color)
            else:
                actual_color1 = self.canvas.itemcget(case1, "fill")
                if actual_color1 == "lightgrey":
                    new_color = "grey"
                    self.canvas.itemconfig(case1, fill=new_color)
                elif actual_color1 == "darkblue":
                    new_color = "blue"
                    self.canvas.itemconfig(case1, fill=new_color)

                actual_color2 = self.canvas.itemcget(case2, "fill")
                if actual_color2 == "lightgrey":
                    new_color = "grey"
                    self.canvas.itemconfig(case2, fill=new_color)
                elif actual_color2 == "darkblue":
                    new_color = "blue"
                    self.canvas.itemconfig(case2, fill=new_color)

    def on_click(self, event):

        if self.case_numero_1 is None:
            case_index, self.case_numero_1 = self.trouver_case_index(event)
            self.assombrir_case(case_index)
            self.case_en_memoire = case_index
            self.trouver_coups_possibles(self.case_numero_1)

        elif self.case_numero_1 is not None and self.case_numero_2 is None:
            self.cacher_coups_possibles()
            case_index, self.case_numero_2 = self.trouver_case_index(event)
            coup = self.case_numero_1 + self.case_numero_2

            if self.game.is_a_promotion(coup):
                self.promotion()
                coup += self.choice_prom

            if self.game.test_move(coup):
                self.coups_a_jouer.append(coup)
                self.eclairer_case(self.case_en_memoire)

                self.cacher_coups_possibles()
                self.case_en_memoire = None
                self.case_numero_2 = None
                self.case_numero_1 = None

            else:
                case_index, _ = self.trouver_case_index(event)
                self.cacher_coups_possibles()
                self.eclairer_case(self.case_en_memoire)
                self.assombrir_case(case_index)
                self.case_en_memoire = case_index
                self.case_numero_1 = self.case_numero_2
                self.case_numero_2 = None
                self.trouver_coups_possibles(self.case_numero_1)

    def trouver_case_index(self, event):
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        case_index = 0
        for item in items:
            if item <= 64:
                case_index = item
        case_coord = self.cases_index_with_case[case_index]
        return case_index, case_coord

    def open_parameters_window(self, event):

        def update_legende():

            if self.mode == "againstcomputer":
                self.canvas_3.itemconfig(self.legende_adversaire[0], text=f"Stockfish")
                self.canvas_3.itemconfig(
                    self.legende_adversaire[1],
                    text=f"(Elo : {self.game.get_niv_elo()})",
                )

            elif self.mode == "againstfriend":
                self.canvas_3.itemconfig(
                    self.legende_adversaire[0], text=f"     Friendly match"
                )
                self.canvas_3.itemconfig(self.legende_adversaire[1], text="")

        def enregistrer():
            elo = self.elo_choisi.get()
            self.game.set_difficulty(elo)
            self.mode = self.mode_choisi.get()
            self.gear_window.destroy()
            update_legende()

        self.gear_window = tk.Toplevel(self.master)
        self.gear_window.geometry("250x200")
        self.gear_window.title("Paramètres du Bot")

        self.elo_choisi = tk.IntVar(value=self.game.get_niv_elo())

        elo_label = tk.Label(self.gear_window, text="Niveau ELO du bot")
        elo_label.pack(padx=20, pady=(10, 0))

        elo_scale = tk.Scale(
            self.gear_window,
            from_=100,
            to=3000,
            orient="horizontal",
            length=200,
            variable=self.elo_choisi,
        )
        elo_scale.pack(padx=20, pady=10)

        mode_label = tk.Label(self.gear_window, text="Mode de jeu")
        mode_label.pack(padx=20, pady=(10, 0))

        self.mode_choisi = tk.StringVar(value=self.mode)

        mode_computer = tk.Radiobutton(
            self.gear_window,
            text="Contre l'ordinateur",
            variable=self.mode_choisi,
            value="againstcomputer",
        )
        mode_computer.pack(anchor="w", padx=20)

        mode_friend = tk.Radiobutton(
            self.gear_window,
            text="Contre un Ami",
            variable=self.mode_choisi,
            value="againstfriend",
        )

        mode_friend.pack(anchor="w", padx=20)
        save_button = tk.Button(
            self.gear_window, text="Enregistrer", command=enregistrer
        )
        save_button.place(x=160, y=160)

    def promotion(self):

        def not_choice():
            self.choice_prom = "q"
            self.window.destroy()
            self.window.quit()

        def on_image_double_click(idx):
            choice = ["q", "r", "b", "n"][idx]
            self.choice_prom = choice
            self.window.destroy()
            self.window.quit()

        self.window = tk.Toplevel(self)
        self.window.title("")
        self.window.canvas = tk.Canvas(self.window, width=100, height=330)

        self.window.canvas.pack()

        pieces = ["wq", "wr", "wb", "wn"]

        self.image_ids_prom = []

        for i, piece in enumerate(pieces):
            x = 13
            y = 80 * i
            image_id = self.window.canvas.create_image(
                x, y, image=self.images[piece], anchor=tk.NW
            )
            self.image_ids_prom.append(image_id)
            self.window.canvas.tag_bind(
                image_id, "<Button-1>", lambda event, idx=i: on_image_double_click(idx)
            )

        self.window.protocol("WM_DELETE_WINDOW", not_choice)

        self.window.mainloop()

    def evaluation_game(self):
        text = ""
        eval_win = self.game.calculs_win_eval()

        if eval_win[0] == "cp":
            eval_cp = eval_win[1]
            self.proportion = eval_cp / 20 * self.board_size
            text = eval_cp
        elif eval_win[0] == "mate":
            if eval_win[1] != 0:
                eval_cp = int(eval_win[1])
                self.proportion = (
                    self.board_size / 2 if eval_cp > 0 else -self.board_size / 2
                )
                text = "M" + str(eval_cp)
            else:
                self.proportion = 0
                if not self.stop:
                    print("vous avez perdu")
                self.stop = True

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

        self.after(500, self.evaluation_game)

    def trouver_coups_possibles(self, case):

        def dessiner_ronds():

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

            for element in self.coups_possibles.keys():
                case_a_traiter = element[2:4]
                coord_x, coord_y = trad_case_coord(case_a_traiter)
                if self.coups_possibles[element] == 0:
                    self.dessins_ronds.append(
                        self.canvas.create_oval(
                            coord_x - self.raduis,
                            coord_y - self.raduis,
                            coord_x + self.raduis,
                            coord_y + self.raduis,
                            fill="grey30",
                        )
                    )
                elif self.coups_possibles[element] == 1:
                    self.dessins_ronds.append(
                        self.canvas.create_oval(
                            coord_x - self.raduis,
                            coord_y - self.raduis,
                            coord_x + self.raduis,
                            coord_y + self.raduis,
                            fill="red",
                        )
                    )

        self.coups_possibles = {}
        for letter in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            for num in [str(i) for i in range(1, self.size + 1)]:
                coup = case + letter + num
                if self.game.test_move(coup):
                    if self.game.test_capture(coup):
                        self.coups_possibles[coup] = 1
                    else:
                        self.coups_possibles[coup] = 0
                elif self.game.test_move(coup + "q"):
                    self.coups_possibles[coup] = 0
        dessiner_ronds()

    def cacher_coups_possibles(self):
        for element in self.dessins_ronds:
            self.canvas.delete(element)
            del element

    def trouver_meilleur_coup_pro(self):
        self.game_pro.set_position(self.coup_joues)
        return self.game_pro.get_best_move()

    def updates_actions(self):

        if self.mode == "againstcomputer":

            if not self.stop:
                if self.numero_coup % 2 == 0:
                    if len(self.coups_a_jouer) != 0:

                        coup = self.coups_a_jouer.pop(0)

                        # if self.trouver_meilleur_coup_pro() == coup:
                        #     print('Meilleur couppp')

                        if self.game.test_capture(coup):
                            self.take_piece(coup[2:])

                        self.game.move_piece(coup)

                        self.afficher_coup(self.coup_eclaire, True)

                        self.afficher_coup(coup, False)
                        self.coup_eclaire = coup
                        self.coup_joues.append(coup)
                        self.update_images()
                        self.numero_coup += 1
                        self.fill_taken_pieces()
                        self.advantage()

                else:
                    self.afficher_coup(self.coup_eclaire, True)
                    best_move = self.game.find_best_move()
                    if self.game.test_capture(best_move):
                        self.take_piece(best_move[2:])
                    self.game.move_piece(best_move)
                    self.afficher_coup(best_move, False)
                    self.coup_eclaire = best_move
                    self.coup_joues.append(best_move)
                    self.numero_coup += 1
                    self.update_images()
                    self.fill_taken_pieces()
                    self.advantage()

        elif self.mode == "againstfriend":
            if not self.stop:
                if self.joueur == 0:
                    if len(self.coups_a_jouer) != 0:
                        coup = self.coups_a_jouer.pop(0)
                        if self.game.test_move(coup):
                            if self.game.test_capture(coup):
                                self.take_piece(coup[2:])
                            self.game.move_piece(coup)
                            self.coup_joues.append(coup)
                            self.update_images()
                            self.numero_coup += 1
                            self.fill_taken_pieces()
                            self.advantage()
                            self.joueur = 1

                else:
                    if len(self.coups_a_jouer) != 0:
                        coup = self.coups_a_jouer.pop(0)
                        if self.game.test_move(coup):
                            if self.game.test_capture(coup):
                                self.take_piece(coup[2:])
                            self.game.move_piece(coup)
                            self.coup_joues.append(coup)
                            self.update_images()
                            self.numero_coup += 1
                            self.fill_taken_pieces()
                            self.advantage()
                            self.joueur = 0

        self.after(50, self.updates_actions)

    def take_piece(self, case):
        res = str(self.game.get_what_is_on_square(case))
        word = ""
        for i, char in enumerate(res):
            if char == "." or char == "_":
                word += res[i + 1]
        piece = word.lower()

        if piece[1] == "k":
            piece = piece[0] + "n"
        if piece is not None:
            if piece[0] == "w":
                self.pieces_taken["white"].append(piece)
            elif piece[0] == "b":
                self.pieces_taken["black"].append(piece)

    def retour_arriere(self, event):

        self.afficher_coup(self.coup_eclaire, True)
        self.coup_joues.pop(-1)
        self.coup_joues.pop(-1)

        self.game.set_position(self.coup_joues)

        self.update_images()
        self.updates_actions()


def main():
    board = ChessGUI()

    board.mainloop()


if __name__ == "__main__":
    main()
