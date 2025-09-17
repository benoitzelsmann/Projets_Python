

class Init:
    def __init__(self):
        self.legende_adversaire = []
        self.elo_choisi = None
        self.mode_choisi = None
        self.gear_window = None
        self.case_en_memoire = None
        self.case_numero_1 = None
        self.case_numero_2 = None
        self.window = None
        self.choice_prom = None
        self.image_ids_prom = None
        self.advantage_stock = None
        self.advantage_you = None
        self.parameters = None
        self.gear_image = None
        self.images_mini = None
        self.board_visu = None
        self.canvas_3 = None
        self.canvas_4 = None
        self.frame_board = None
        self.eval_label = None
        self.proportion = None
        self.rectangle_eval = None
        self.canvas_2 = None
        self.images = None
        self.files = None
        self.canvas = None
        self.stop = None
        self.coup_eclaire = None

        self.dessins_ronds = []

        self.new_case_selectionnee = []
        self.coups_a_jouer = []
        self.coups_possibles = {}

        self.pieces_restantes_white = ['wk', 'wq'] + ['wr', 'wb', 'wn'] * 2 + ['wp'] * 8
        self.pieces_restantes_black = ['bk', 'bq'] + ['br', 'bb', 'bn'] * 2 + ['bp'] * 8

        self.pieces_taken_draws_3 = []
        self.pieces_taken_draws_4 = []

        self.pieces_taken = {"white": [], "black": []}

        self.cases_index_with_case = {}
        self.cases_index_with_case_rev = {}
        self.pieces_index = {}


        self.board_size = 80 * 8
        self.cell_size = 80
        self.raduis = 10
        self.colors = ["lightgrey", "darkblue"]
        self.font_color = 'lightgrey'

        self.piece_values = {'k': 0, 'q': 9, 'r': 5, 'n': 3, 'b': 3, 'p': 1}

        self.largeur_labels = 20
        self.canvas_size = (self.board_size + self.largeur_labels * 2,
                            self.board_size + self.largeur_labels * 2)
        self.canvas_2_size = (60, self.board_size + self.largeur_labels * 2)
        self.dimension_bar = (35, self.board_size)
        self.offset_bar = (self.canvas_2_size[0] - self.dimension_bar[0]) // 2
        self.canvas_34_size = (self.canvas_size[0] + self.canvas_2_size[0] + 3, 70)
        self.dimension_button = (50, 50)



        self.numero_coup = 0
        self.joueur = 0

        self.coup_joues = []


