import os
import pygame
from random import randint, choice


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

def create_images(taille_bonbon):
    current_dir = os.path.dirname(__file__)
    # chemin vers le dossier pngs_candy_crush
    png_dir = os.path.join(current_dir, '..', 'pngs_candy_crush')

    images = {
        0: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, 'blanc.png')), (taille_bonbon, taille_bonbon)),

        1: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, 'jaune.png')), (taille_bonbon, taille_bonbon)),
        11: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, 'jaune_v.png')), (taille_bonbon, taille_bonbon)),
        21: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, 'jaune_h.png')), (taille_bonbon, taille_bonbon)),
        31: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, 'jaune_w.png')), (taille_bonbon, taille_bonbon)),
        41: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, 'jaune_b.png')), (taille_bonbon, taille_bonbon)),

        2: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, 'violet.png')), (taille_bonbon, taille_bonbon)),
        12: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, 'violet_v.png')), (taille_bonbon, taille_bonbon)),
        22: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, 'violet_h.png')), (taille_bonbon, taille_bonbon)),
        32: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, 'violet_w.png')), (taille_bonbon, taille_bonbon)),
        42: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, 'violet_b.png')), (taille_bonbon, taille_bonbon)),

        3: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "bleu2.png")), (taille_bonbon, taille_bonbon)),
        13: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "bleu2_v.png")), (taille_bonbon, taille_bonbon)),
        23: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "bleu2_h.png")), (taille_bonbon, taille_bonbon)),
        33: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "bleu2_w.png")), (taille_bonbon, taille_bonbon)),
        43: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "bleu2_b.png")), (taille_bonbon, taille_bonbon)),

        4: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "vert.png")), (taille_bonbon, taille_bonbon)),
        14: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "vert_v.png")), (taille_bonbon, taille_bonbon)),
        24: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "vert_h.png")), (taille_bonbon, taille_bonbon)),
        34: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "vert_w.png")), (taille_bonbon, taille_bonbon)),
        44: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "vert_b.png")), (taille_bonbon, taille_bonbon)),

        5: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "orange.png")), (taille_bonbon, taille_bonbon)),
        15: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "orange_v.png")), (taille_bonbon, taille_bonbon)),
        25: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "orange_h.png")), (taille_bonbon, taille_bonbon)),
        35: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "orange_w.png")), (taille_bonbon, taille_bonbon)),
        45: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "orange_b.png")), (taille_bonbon, taille_bonbon)),

        6: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "rouge.png")), (taille_bonbon, taille_bonbon)),
        16: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "rouge_v.png")), (taille_bonbon, taille_bonbon)),
        26: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "rouge_h.png")), (taille_bonbon, taille_bonbon)),
        36: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "rouge_w.png")), (taille_bonbon, taille_bonbon)),
        46: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "rouge_b.png")), (taille_bonbon, taille_bonbon)),

        7: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "bleu.png")), (taille_bonbon, taille_bonbon)),
        17: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "bleu_v.png")), (taille_bonbon, taille_bonbon)),
        27: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "bleu_h.png")), (taille_bonbon, taille_bonbon)),
        37: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "bleu_w.png")), (taille_bonbon, taille_bonbon)),
        47: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "bleu_b.png")), (taille_bonbon, taille_bonbon)),

        10: pygame.transform.scale(pygame.image.load(os.path.join(png_dir, "gateau.png")), (taille_bonbon, taille_bonbon)),
    }
    return images





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
