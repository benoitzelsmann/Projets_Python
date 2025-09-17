
from random import randint, choice
import imageio.v2 as imageio
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap



def images_from_grille(images, grille, size):
    return [[imageio.imread(images[grille[i][j]]) for j in range(size + 4)] for i in range(size + 4)]


def creation_grille(size, nb_couleurs):
    """crée une grille globale de taille size*size"""
    table = [[randint(1, nb_couleurs) for _ in range(size)] for _ in range(size)]
    for i in table:
        i.append(0)
        i.append(0)
        i.insert(0, 0)
        i.insert(0, 0)
    table.append([0 for _ in range(size + 4)])
    table.append([0 for _ in range(size + 4)])
    table.insert(0, [0 for _ in range(size + 4)])
    table.insert(0, [0 for _ in range(size + 4)])
    return table


def graphique(grille, nb_couleurs, size, images):
    """créé le graphique"""
    cmap_colors = plt.get_cmap('turbo', nb_couleurs + 2)
    cmap_list = [cmap_colors(i) for i in range(cmap_colors.N)]
    cmap_list[0] = (0.6, 0.6, 1.0, 1.0)
    cmap_list[nb_couleurs + 1] = (0, 0, 0, 0)
    custom_cmap = ListedColormap(cmap_list)
    liste_images = images_from_grille(images, grille, size)
    fig, plotid = plt.subplots(figsize=(size + 4, size + 4))
    plotid.set_xlim([1, size + 2])
    plotid.set_ylim([size + 2, 1])
    plotid.set_aspect('equal')
    plotid.axis("off")
    axes_graph = [[plt.imshow(liste_images[i][j], extent=[j - 0.5, j + 0.5, i + 0.5, i - 0.5], cmap=custom_cmap) for j in range(size + 4)] for i in range(size + 4)]
    button_ax = fig.add_axes([0.47, 0.87, 0.1, 0.04])
    button_quit = plt.Button(button_ax, "Quitter")
    gateau_ax = fig.add_axes([0.765, 0.6, 0.15, 0.07])
    gateau_btn = plt.Button(gateau_ax, "Gateau \n (re-clic pour confirmer)")
    neptune_ax = fig.add_axes([0.765, 0.5, 0.15, 0.07])
    neptune_btn = plt.Button(neptune_ax, "Neptune\n (re-clic pour confirmer)")
    raye_ax = fig.add_axes([0.765, 0.4, 0.15, 0.07])
    raye_btn = plt.Button(raye_ax, "raye\n (re-clic pour confirmer)")
    enballe_ax = fig.add_axes([0.765, 0.3, 0.15, 0.07])
    enballe_btn = plt.Button(enballe_ax, "Wrapped\n (re-clic pour confirmer)")
    return axes_graph, button_quit, gateau_btn, neptune_btn, raye_btn, enballe_btn


def test_bonus_1(size, ll, lc):
    for x_t in range(2, size + 2):
        if ll.count(x_t) == 4:
            return "vert"
        if lc.count(x_t) == 4:
            return "hori"
    return None


def test_gateau_1(size, ll, lc):
    for x_tg in range(2, size + 2):
        if ll.count(x_tg) == 5:
            return True
        if lc.count(x_tg) == 5:
            return True
    return None


def test_boule_1(size, ll, lc):
    for x_tb in range(2, size + 2):
        if ll.count(x_tb) > 4:
            for y_tb in range(2, size + 2):
                if lc.count(y_tb) > 2:
                    return True
        if lc.count(x_tb) > 4:
            for y_tb in range(2, size + 2):
                if ll.count(y_tb) > 2:
                    return True
    return None


def test_wrapped_1(size, ll, lc):
    for x_tw in range(2, size + 2):
        if ll.count(x_tw) > 2:
            for y_tw in range(2, size + 2):
                if lc.count(y_tw) > 2:
                    return True
        if lc.count(x_tw) > 2:
            for y_tw in range(2, size + 2):
                if ll.count(y_tw) > 2:
                    return True
    return None


def test_bonus(grille, ll, lc, v, mouv, x_tb, y_tb):
    var = test_bonus_1(len(grille), ll, lc)
    if var is not None:
        if mouv:
            choix = (y_tb, x_tb)
        else:
            choix = choice(v)
        if var == "vert":
            grille[choix[0]][choix[1]] = grille[choix[0]][choix[1]] % 10 + 10
        elif var == "hori":
            grille[choix[0]][choix[1]] = grille[choix[0]][choix[1]] % 10 + 20
        v.pop(v.index(choix))
        return True
    return False


def test_gateau(grille, ll, lc, v, mouv, x_tg, y_tg):
    var = test_gateau_1(len(grille), ll, lc)
    if var is not None:
        if mouv:
            choix = (y_tg, x_tg)
        else:
            choix = choice(v)
        grille[choix[0]][choix[1]] = 10
        v.pop(v.index(choix))
        return True
    return False


def test_wrapped(grille, ll, lc, v, mouv, x_tw, y_tw):
    var = test_wrapped_1(len(grille), ll, lc)
    if var is not None:
        if mouv:
            choix = (y_tw, x_tw)
        else:
            choix = choice(v)
        grille[choix[0]][choix[1]] = grille[choix[0]][choix[1]] % 10 + 30
        v.pop(v.index(choix))
        return True
    return False


def test_boule(grille, ll, lc, v, mouv, x_tb, y_tb):
    var = test_boule_1(len(grille), ll, lc)
    if var is not None:
        if mouv:
            choix = (y_tb, x_tb)
        else:
            choix = choice(v)
        grille[choix[0]][choix[1]] = grille[choix[0]][choix[1]] % 10 + 40
        v.pop(v.index(choix))
        return True
    return False


def detecte_voisins(table_type, x_d, y_d):
    """renvoie les coordonnées des cases adjacentes à celle que l'on étudie"""
    liste = []
    couleur = table_type[x_d][y_d] % 10
    if couleur == 0:
        return []
    if couleur == 10:
        return []
    if couleur > 40:
        return []
    if table_type[x_d + 1][y_d] % 10 == couleur and table_type[x_d + 1][y_d] < 40 and table_type[x_d + 1][y_d] != 10:
        liste.append((x_d + 1, y_d))
    if table_type[x_d - 1][y_d] % 10 == couleur and table_type[x_d - 1][y_d] < 40 and table_type[x_d - 1][y_d] != 10:
        liste.append((x_d - 1, y_d))
    if table_type[x_d][y_d + 1] % 10 == couleur and table_type[x_d][y_d + 1] < 40 and table_type[x_d][y_d + 1] != 10:
        liste.append((x_d, y_d + 1))
    if table_type[x_d][y_d - 1] % 10 == couleur and table_type[x_d][y_d - 1] < 40 and table_type[x_d][y_d - 1] != 10:
        liste.append((x_d, y_d - 1))
    return liste


def update(grille, size, nb_couleurs):
    """descend des cases à la place des cases vides et crée un élément aléatoire en haut de la grille"""
    c = 0
    for ligne in range(2, size + 2):
        for colonne in range(2, size + 2):
            if grille[ligne][colonne] == 0:
                c = c + 1
                for k in range(0, ligne):
                    grille[ligne - k][colonne] = grille[ligne - k - 1][colonne]
                grille[2][colonne] = randint(1, nb_couleurs)
    if c > 0:
        return True
    return False
