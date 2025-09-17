from functions import *
import os
from math import sqrt
from matplotlib.backend_bases import MouseButton
from random import shuffle


chemin_images = os.path.join(os.path.dirname(__file__), '../pngs_candy_crush')
"""100*100 pixels"""
images = {
    0: os.path.join(chemin_images, 'blanc.png'),

    1: os.path.join(chemin_images, 'jaune.png'),
    11: os.path.join(chemin_images, 'jaune_v.png'),
    21: os.path.join(chemin_images, 'jaune_h.png'),
    31: os.path.join(chemin_images, 'jaune_w.png'),
    41: os.path.join(chemin_images, 'jaune_b.png'),

    2: os.path.join(chemin_images, 'violet.png'),
    12: os.path.join(chemin_images, 'violet_v.png'),
    22: os.path.join(chemin_images, 'violet_h.png'),
    32: os.path.join(chemin_images, 'violet_w.png'),
    42: os.path.join(chemin_images, 'violet_b.png'),

    3: os.path.join(chemin_images, 'bleu2.png'),
    13: os.path.join(chemin_images, 'bleu2_v.png'),
    23: os.path.join(chemin_images, 'bleu2_h.png'),
    33: os.path.join(chemin_images, 'bleu2_w.png'),
    43: os.path.join(chemin_images, 'bleu2_b.png'),

    4: os.path.join(chemin_images, 'vert.png'),
    14: os.path.join(chemin_images, 'vert_v.png'),
    24: os.path.join(chemin_images, 'vert_h.png'),
    34: os.path.join(chemin_images, 'vert_w.png'),
    44: os.path.join(chemin_images, 'vert_b.png'),

    5: os.path.join(chemin_images, 'orange.png'),
    15: os.path.join(chemin_images, 'orange_v.png'),
    25: os.path.join(chemin_images, 'orange_h.png'),
    35: os.path.join(chemin_images, 'orange_w.png'),
    45: os.path.join(chemin_images, 'orange_b.png'),

    6: os.path.join(chemin_images, 'rouge.png'),
    16: os.path.join(chemin_images, 'rouge_v.png'),
    26: os.path.join(chemin_images, 'rouge_h.png'),
    36: os.path.join(chemin_images, 'rouge_w.png'),
    46: os.path.join(chemin_images, 'rouge_b.png'),

    7: os.path.join(chemin_images, 'bleu.png'),
    17: os.path.join(chemin_images, 'bleu_v.png'),
    27: os.path.join(chemin_images, 'bleu_h.png'),
    37: os.path.join(chemin_images, 'bleu_w.png'),
    47: os.path.join(chemin_images, 'bleu_b.png'),

    10: os.path.join(chemin_images, 'gateau.png')}


"""parametres"""
size = 8
nb_couleurs = 5
nb_coups = 50
x = 0
y = 0
coups_joues = 0
score = 0
grille = creation_grille(size=size, nb_couleurs=nb_couleurs)
axes, button, gateau, neptune, raye, emballe = graphique(grille=grille, nb_couleurs=nb_couleurs, size=size, images=images)


def affiche_grille():
    global coups_joues
    nb = nb_coups - coups_joues
    liste_images = images_from_grille(images, grille, size)
    for i in range(2, size + 2):
        for j in range(2, size + 2):
            axes[i][j].set_data(liste_images[i][j])
    plt.title(f"score :  = {score}      déplacements :  = {nb} ", x=-1.65, y=8.8)
    plt.pause(0.05)


def supression_raye(x_grid, y_grid, orientation):
    global score
    grille[x_grid][y_grid] = 0
    if orientation == "co":
        for i in range(2, size + 2):
            if grille[i][y_grid] == 10 or grille[i][y_grid] > 40:
                supression_subite(i, y_grid)
            elif 10 < grille[i][y_grid] < 18:
                supression_raye(i, y_grid, "co")
            elif 20 < grille[i][y_grid] < 28:
                supression_raye(i, y_grid, "li")
            elif 30 < grille[i][y_grid] < 40:
                supression_wrapped(i, y_grid)
            else:
                grille[i][y_grid] = 0
        score += size
    if orientation == "li":
        for i in range(2, size + 2):
            if grille[x_grid][i] == 10 or grille[x_grid][i] > 40:
                supression_subite(x_grid, i)
            elif 10 < grille[x_grid][i] < 18:
                supression_raye(x_grid, i, "co")
            elif 20 < grille[x_grid][i] < 28:
                supression_raye(x_grid, i, "li")
            elif 30 < grille[x_grid][i] < 40:
                supression_wrapped(x_grid, i)
            else:
                grille[x_grid][i] = 0
        score += size


def supression_wrapped(x_sw, y_sw):
    global score
    for i in range(3):
        for j in range(3):
            if grille[x_sw - 1 + j][y_sw - 1 + i] == 10 or grille[x_sw - 1 + j][y_sw - 1 + i] > 40:
                supression_subite(x_sw - 1 + j, y_sw - 1 + i)
            elif 10 < grille[x_sw - 1 + j][y_sw - 1 + i] < 18:
                supression_raye(x_sw - 1 + j, y_sw - 1 + i, "co")
            elif 20 < grille[x_sw - 1 + j][y_sw - 1 + i] < 28:
                supression_raye(x_sw - 1 + j, y_sw - 1 + i, "li")
            elif 30 < grille[x_sw - 1 + j][y_sw - 1 + i] < 40:
                grille[x_sw - 1 + j][y_sw - 1 + i] = 0
                supression_wrapped(x_sw - 1 + j, y_sw - 1 + i)
            grille[x_sw - 1 + j][y_sw - 1 + i] = 0
    score += 8


def supression_speciale(x_1, y_1, x_2, y_2):
    global score
    """booster"""
    if (grille[y_2][x_2] == 10 and grille[y_1][x_1] == 10) or (grille[y_2][x_2] > 40 and grille[y_1][x_1] == 10) or (
            grille[y_2][x_2] > 40 and grille[y_1][x_1] > 40) or (grille[y_2][x_2] == 10 and grille[y_1][x_1] > 40):
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                grille[i][j] = 0
        score += size ** 2
        return None

    if grille[y_2][x_2] == 10 or grille[y_1][x_1] == 10:
        if grille[y_2][x_2] == 10:
            coul = grille[y_1][x_1]
        else:
            coul = grille[y_2][x_2]
        grille[y_2][x_2] = 0
        grille[y_1][x_1] = 0
        supression_gateau_comb(coul)
        return None
    elif grille[y_2][x_2] > 40 or grille[y_1][x_1] > 40:
        if grille[y_2][x_2] > 40:
            coul = grille[y_1][x_1]
            coul_b = grille[y_2][x_2]
        else:
            coul = grille[y_2][x_2]
            coul_b = grille[y_1][x_1]
        grille[y_2][x_2] = 0
        grille[y_1][x_1] = 0
        supression_boule_comb(coul_b, coul)
        return None


def supression_subite(x_ss, y_ss):
    global score
    if grille[x_ss][y_ss] == 10:
        grille[x_ss][y_ss] = 0
        coul = randint(1, nb_couleurs)
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                if 20 > grille[i][j] > 10 and grille[i][j] % 10 == coul:
                    supression_raye(i, j, "co")
                elif 30 > grille[i][j] > 20 and grille[i][j] % 10 == coul:
                    supression_raye(i, j, "li")
                elif 40 > grille[i][j] > 30 and grille[i][j] % 10 == coul:
                    supression_wrapped(i, j)
                elif grille[i][j] == coul:
                    grille[i][j] = 0
                    score += 1
        affiche_grille()
    else:
        coul_b = grille[x_ss][y_ss]
        grille[x_ss][y_ss] = 0
        coul = randint(1, nb_couleurs)
        while coul == coul_b % 10:
            coul = randint(1, nb_couleurs)
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                if 50 > grille[i][j] > 10 and grille[i][j] % 10 == coul_b % 10:
                    grille[i][j] = coul_b % 10 + grille[i][j] - grille[i][j] % 10
                elif grille[i][j] == coul:
                    grille[i][j] = coul_b % 10
                    score += 1
        affiche_grille()


def supression_gateau_comb(coul):
    if 30 > coul > 10:
        liste = []
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                if grille[i][j] == coul % 10:
                    temp = choice([10, 20])
                    grille[i][j] = coul % 10 + temp
                    liste.append((i, j))
        affiche_grille()
        for (i, j) in liste:
            if coul > 20:
                supression_raye(i, j, "li")
            else:
                supression_raye(i, j, "co")

    elif 40 > coul > 30:
        liste = []
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                if grille[i][j] == coul % 10:
                    grille[i][j] = coul % 10 + 30
                    liste.append((i, j))
        affiche_grille()
        for (i, j) in liste:
            supression_wrapped(i, j)
    else:
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                if 20 > grille[i][j] > 10 and grille[i][j] % 10 == coul % 10:
                    supression_raye(i, j, "co")
                elif 30 > grille[i][j] > 20 and grille[i][j] % 10 == coul % 10:
                    supression_raye(i, j, "li")
                elif 40 > grille[i][j] > 30 and grille[i][j] % 10 == coul % 10:
                    supression_wrapped(i, j)
                elif grille[i][j] == coul % 10:
                    grille[i][j] = 0
        affiche_grille()


def supression_boule_comb(coul_b, coul):
    if 30 > coul > 10:
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                if grille[i][j] == coul % 10 or grille[i][j] == coul_b % 10:
                    alea = choice([10, 20])
                    grille[i][j] = coul_b % 10 + alea
        affiche_grille()
    elif 40 > coul > 30:
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                if grille[i][j] == coul % 10 or grille[i][j] == coul_b % 10:
                    grille[i][j] = coul_b % 10 + 30
        affiche_grille()
    else:
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                if 40 > grille[i][j] > 10 and ((grille[i][j] % 10 == coul % 10) or (grille[i][j] % 10 == coul_b % 10)):
                    grille[i][j] = coul + grille[i][j] - grille[i][j] % 10

                elif grille[i][j] % 10 == coul % 10:
                    grille[i][j] = coul_b % 10
        affiche_grille()


def supression_double_wrapped(x_sdw, y_sdw):
    global score
    for i in range(5):
        for j in range(5):
            if grille[x_sdw - 2 + j][y_sdw - 2 + i] == 10 or grille[x_sdw - 2 + j][y_sdw - 2 + i] > 40:
                supression_subite(x_sdw - 2 + j, y_sdw - 2 + i)
            elif 10 < grille[x_sdw - 2 + j][y_sdw - 2 + i] < 18:
                supression_raye(x_sdw - 2 + j, y_sdw - 2 + i, "co")
            elif 20 < grille[x_sdw - 2 + j][y_sdw - 2 + i] < 28:
                supression_raye(x_sdw - 2 + j, y_sdw - 2 + i, "li")
            elif 30 < grille[x_sdw - 2 + j][y_sdw - 2 + i] < 40:
                grille[x_sdw - 2 + j][y_sdw - 2 + i] = 0
                supression_wrapped(x_sdw - 2 + j, y_sdw - 2 + i)
            grille[x_sdw - 2 + j][y_sdw - 2 + i] = 0
    score += 25


def supression_bonus_wrapped(x_sbw, y_sbw):
    global score
    supression_raye(x_sbw - 1, y_sbw, "li")
    supression_raye(x_sbw, y_sbw, "li")
    supression_raye(x_sbw + 1, y_sbw, "li")
    supression_raye(x_sbw, y_sbw - 1, "co")
    supression_raye(x_sbw, y_sbw + 1, "co")
    supression_raye(x_sbw, y_sbw, "co")
    score += 9


def detecte_coordonnees_3(table, x_candy, y_candy, test, x1_clic, y1_clic, x2_clic, y2_clic):
    """propagation, toutes les cases appartenant à un groupe adjacent à la case étudiée sont données"""
    if table[x_candy][y_candy] == 10:
        return []
    liste_voisins = [(x_candy, y_candy)]
    c = 1
    while c != 0:
        for bi in liste_voisins:
            lis = detecte_voisins(table, bi[0], bi[1])
            c = 0
            for i in lis:
                c = 0
                if i not in liste_voisins:
                    c = c + 1
                    liste_voisins.append(i)

    """verification, ok si il y a bien 3 cases alignées dans la combinaison"""
    v = []
    liste_colonnes = []
    liste_lignes = []
    for (x_candy, y_candy) in liste_voisins:
        liste_colonnes.append(y_candy)
        liste_lignes.append(x_candy)

    for n in range(2, size + 2):
        if liste_colonnes.count(n) > 2 or liste_lignes.count(n) > 2:
            v = liste_voisins

    if not test:
        """étude des coordonnées pour BONUSSS"""
        if len(v) != 0:
            """plus de 5 bonbons alignés"""
            if (y1_clic, x1_clic) in v:
                y_temp, x_temp = y1_clic, x1_clic
                var = True
            elif (y2_clic, x2_clic) in v:
                y_temp, x_temp = y2_clic, x2_clic
                var = True
            else:
                var = False
                x_temp, y_temp = 0, 0
            if not test_boule(grille, liste_lignes, liste_colonnes, v, var, x_temp, y_temp):
                """5 bonbons alignés"""
                if not test_gateau(grille, liste_lignes, liste_colonnes, v, var, x_temp, y_temp):
                    """4 bonbons alignés"""
                    if not test_wrapped(grille, liste_lignes, liste_colonnes, v, var, x_temp, y_temp):
                        test_bonus(grille, liste_lignes, liste_colonnes, v, var, x_temp, y_temp)

            for (x_candy, y_candy) in v:
                """bonus"""
                if 10 < table[x_candy][y_candy] < 18:
                    supression_raye(x_candy, y_candy, "co")
                if 20 < table[x_candy][y_candy] < 28:
                    supression_raye(x_candy, y_candy, "li")
                if 30 < table[x_candy][y_candy] < 38:
                    supression_wrapped(x_candy, y_candy)

            for (x_candy, y_candy) in v:
                if table[x_candy][y_candy] < 40:
                    table[x_candy][y_candy] = 0
    return v


def detecte_coordonnes_totales(x1_clic, y1_clic, x2_clic, y2_clic):
    """effectue la somme des coordonnées à supprimer"""
    global score
    liste_totale = []
    for i in range(2, size + 3):
        for j in range(2, size + 3):
            if (i, j) not in liste_totale:
                temp = detecte_coordonnees_3(grille, i, j, False, x1_clic, y1_clic, x2_clic, y2_clic)
                for k in temp:
                    if k not in liste_totale:
                        liste_totale.append(k)
    score += len(liste_totale)


def evolution(first, x1_clic, y1_clic, x2_clic, y2_clic):
    if not first:
        temp = True
        while temp:
            detecte_coordonnes_totales(x1_clic, y1_clic, x2_clic, y2_clic)
            affiche_grille()
            temp = update(grille, size, nb_couleurs)
            affiche_grille()
    else:
        temp = True
    while temp:
        detecte_coordonnes_totales(0, 0, 0, 0)
        temp = update(grille, size, nb_couleurs)


def on_click(event):
    """sert pour la souris"""
    global x, y
    if event.button is MouseButton.LEFT and event.inaxes:
        x, y = int(round(event.xdata, 0)), int(round(event.ydata, 0))


def on_button_click(event):
    plt.close()  # Fermer le graphique
    quit()


def on_gateau_click(event):
    temp = plt.connect('button_press_event', on_click)
    plt.waitforbuttonpress()
    x_s = x
    y_s = y
    plt.disconnect(temp)
    grille[y_s][x_s] = 10
    affiche_grille()
    return None


def on_neptune_click(event):
    temp = plt.connect('button_press_event', on_click)
    plt.waitforbuttonpress()
    x_s = x
    y_s = y
    plt.disconnect(temp)
    grille[y_s][x_s] = grille[y_s][x_s] % 10 + 40
    affiche_grille()
    return


def on_raye_click(event):
    temp = plt.connect('button_press_event', on_click)
    plt.waitforbuttonpress()
    xs = x
    ys = y
    plt.disconnect(temp)
    alea = choice([10, 20])
    grille[ys][xs] = grille[ys][xs] % 10 + alea
    affiche_grille()
    return


def on_enballe_click(event):
    temp = plt.connect('button_press_event', on_click)
    plt.waitforbuttonpress()
    xs = x
    ys = y
    plt.disconnect(temp)
    grille[ys][xs] = grille[ys][xs] % 10 + 30
    affiche_grille()
    return


def possible(x1_p, y1_p, x2_p, y2_p):
    if sqrt((x1_p - x2_p) ** 2 + (y1_p - y2_p) ** 2) > 1 or sqrt((x1_p - x2_p) ** 2 + (y1_p - y2_p) ** 2) < 1:
        return False
    elif grille[y1_p][x1_p] == 10 or grille[y2_p][x2_p] == 10:
        return True
    elif grille[y1_p][x1_p] > 40 or grille[y2_p][x2_p] > 40:
        return True
    elif 10 < grille[y1_p][x1_p] < 30 and 10 < grille[y2_p][x2_p] < 30:
        return True
    elif 30 < grille[y1_p][x1_p] < 40 and 30 < grille[y2_p][x2_p] < 40:
        return True
    elif (10 < grille[y1_p][x1_p] < 30 < grille[y2_p][x2_p] < 40) or (
            10 < grille[y2_p][x2_p] < 30 < grille[y1_p][x1_p] < 40):
        return True
    else:
        temp = [[j for j in i] for i in grille]
        temp[y1_p][x1_p], temp[y2_p][x2_p] = temp[y2_p][x2_p], temp[y1_p][x1_p]
        if len(detecte_coordonnees_3(temp, y1_p, x1_p, True, 0, 0, 0, 0)) == 0 and len(
                detecte_coordonnees_3(temp, y2_p, x2_p, True, 0, 0, 0, 0)) == 0:
            return False
        return True


def fin():
    for a_x in range(2, size + 1):
        for b_x in range(2, size + 1):
            if possible(b_x, a_x, b_x, a_x + 1):
                return False
            if possible(b_x, a_x, b_x + 1, a_x):
                return False
    return True


def test_fin():
    while fin():
        print("Melange !!")
        melange()


def melange():
    ngrille = []
    for i in range(2, size + 2):
        for j in range(2, size + 2):
            ngrille.append(grille[i][j])
    shuffle(ngrille)
    n = 0
    for k in range(2, size + 2):
        for w in range(2, size + 2):
            grille[k][w] = ngrille[n]
            n = n + 1
    evolution(False, 0, 0, 0, 0)


"""crée la premiere grille et l'update"""

button.on_clicked(on_button_click)
gateau.on_clicked(on_gateau_click)
neptune.on_clicked(on_neptune_click)
raye.on_clicked(on_raye_click)
emballe.on_clicked(on_enballe_click)
evolution(True, 0, 0, 0, 0)

"""code du jeu répété i fois"""
while coups_joues < nb_coups:
    """coordonnées du coup"""
    affiche_grille()
    a = plt.connect('button_press_event', on_click)
    plt.waitforbuttonpress()
    x1 = x
    y1 = y
    print(x1, y1)
    plt.disconnect(a)
    b = plt.connect('button_press_event', on_click)
    plt.waitforbuttonpress()
    x2 = x
    y2 = y
    plt.disconnect(b)
    if possible(x1, y1, x2, y2):
        """cas des bonus spéciaux"""
        if (grille[y1][x1] > 40 or grille[y2][x2] == 10) or (grille[y1][x1] == 10 or grille[y2][x2] > 40):
            coups_joues += 1
            supression_speciale(x1, y1, x2, y2)

        """cas de deux bonus"""
        if 10 < grille[y1][x1] < 30 and 10 < grille[y2][x2] < 30:
            coups_joues += 1
            grille[y1][x1] = 0
            grille[y2][x2] = 0
            supression_raye(y2, x2, "li")
            supression_raye(y2, x2, "co")

        """cas de 2 wrapped"""
        if 30 < grille[y1][x1] < 40 and 30 < grille[y2][x2] < 40:
            grille[y1][x1] = 0
            grille[y2][x2] = 0
            supression_double_wrapped(y2, x2)

        """cas de wrapped + bonus"""
        if ((10 < grille[y1][x1] < 30 < grille[y2][x2] < 40) or (
                40 > grille[y1][x1] > 30 > grille[y2][x2] > 10)):
            grille[y1][x1] = 0
            grille[y2][x2] = 0
            supression_bonus_wrapped(y2, x2)

            """cas normal"""
        else:
            coups_joues += 1
            grille[y1][x1], grille[y2][x2] = grille[y2][x2], grille[y1][x1]
        affiche_grille()
        evolution(False, x1, y1, x2, y2)
        test_fin()

    else:
        print("coup impossible")
        grille[y1][x1], grille[y2][x2] = grille[y2][x2], grille[y1][x1]
        affiche_grille()
        grille[y2][x2], grille[y1][x1] = grille[y1][x1], grille[y2][x2]
plt.text(4, 4, str(score), fontsize=50, color='black')
plt.pause(3)

print(score)
