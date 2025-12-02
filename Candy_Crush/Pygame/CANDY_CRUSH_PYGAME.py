from math import sqrt, floor
from random import shuffle
from functions import *

pygame.init()

taille_bonbon = 30
marge = 0
size = 25
nb_couleurs = 7
score = 0
coups_joues = 0
nb_coups = 30
x1, y1, x2, y2 = 0, 0, 0, 0

grille = creation_grille(size, nb_couleurs)
images = create_images(taille_bonbon)

largeur_fenetre = (len(grille) - 4) * taille_bonbon
hauteur_fenetre = (len(grille[0]) - 4) * taille_bonbon

fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Candy Crush")


# NOIR = (0, 0, 0)
# rect = (marge / 2, marge / 2, (len(grille[0]) - 4) * taille_bonbon + marge, (len(grille[0]) - 4) * taille_bonbon + marge)


def affiche_grille(grille):
    pygame.time.delay(50)
    fenetre.fill((255, 255, 255))

    for (k, liste) in enumerate(grille[2:-2]):
        for (j, element) in enumerate(liste[2:-2]):
            x_pos = j * taille_bonbon + marge
            y_pos = k * taille_bonbon + marge

            fenetre.blit(images[element], (x_pos, y_pos))
    pygame.display.flip()


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
        affiche_grille(grille)
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
        affiche_grille(grille)


def supression_gateau_comb(coul):
    if 30 > coul > 10:
        liste = []
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                if grille[i][j] == coul % 10:
                    temp = choice([10, 20])
                    grille[i][j] = coul % 10 + temp
                    liste.append((i, j))
        affiche_grille(grille)
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
        affiche_grille(grille)
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
        affiche_grille(grille)


def supression_boule_comb(coul_b, coul):
    if 30 > coul > 10:
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                if grille[i][j] == coul % 10 or grille[i][j] == coul_b % 10:
                    alea = choice([10, 20])
                    grille[i][j] = coul_b % 10 + alea
        affiche_grille(grille)
    elif 40 > coul > 30:
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                if grille[i][j] == coul % 10 or grille[i][j] == coul_b % 10:
                    grille[i][j] = coul_b % 10 + 30
        affiche_grille(grille)
    else:
        for i in range(2, size + 2):
            for j in range(2, size + 2):
                if 40 > grille[i][j] > 10 and ((grille[i][j] % 10 == coul % 10) or (grille[i][j] % 10 == coul_b % 10)):
                    grille[i][j] = coul + grille[i][j] - grille[i][j] % 10

                elif grille[i][j] % 10 == coul % 10:
                    grille[i][j] = coul_b % 10
        affiche_grille(grille)


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


def update():
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


def update_smooth():
    re_run = True

    while re_run:
        re_run = False
        for ligne in range(2, size + 2):
            for colonne in range(2, size + 2):
                if grille[ligne][colonne] == 0:
                    re_run = True
                    for i in range(1, taille_bonbon + 1):
                        pygame.time.delay(5)
                        x_pos = (colonne - 2) * taille_bonbon
                        y_pos = (ligne - 1) * taille_bonbon + i
                        fenetre.blit(images[grille[ligne - 1][colonne]], (x_pos, y_pos))
                        pygame.display.flip()

                    # grille[ligne][colonne] = grille[ligne-1][colonne]
                    # grille[ligne-1][colonne] = 0


def evolution(first, x1_clic, y1_clic, x2_clic, y2_clic):
    if not first:
        temp = True
        while temp:
            detecte_coordonnes_totales(x1_clic, y1_clic, x2_clic, y2_clic)
            affiche_grille(grille)
            temp = update()
            affiche_grille(grille)

    temp = True
    while temp:
        detecte_coordonnes_totales(0, 0, 0, 0)
        temp = update()


while coups_joues < nb_coups:
    evolution(True, 0, 0, 0, 0)
    affiche_grille(grille)
    coords_clic1 = None
    coords_clic2 = None
    wait = True

    while wait:
        print()
        while coords_clic2 is None or coords_clic1 is None:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x = floor(event.pos[0] / taille_bonbon) + 2
                        y = floor(event.pos[1] / taille_bonbon) + 2
                        if coords_clic1 is None:
                            coords_clic1 = (x, y)
                            print("clic1")
                        else:
                            coords_clic2 = (x, y)
                            coups_joues += 1
                            print("clic2")
                            wait = False

    x1, y1, = coords_clic1 if coords_clic1 else (0, 0)
    x2, y2 = coords_clic2 if coords_clic2 else (0, 0)

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
        affiche_grille(grille)
        evolution(False, x1, y1, x2, y2)
        test_fin()

    else:
        print("coup impossible")
        affiche_grille(grille)
        grille[y1][x1], grille[y2][x2] = grille[y2][x2], grille[y1][x1]

        affiche_grille(grille)
        grille[y2][x2], grille[y1][x1] = grille[y1][x1], grille[y2][x2]

print(score)
pygame.quit()
