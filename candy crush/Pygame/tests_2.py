import pygame

from functions import *

pygame.init()

taille_bonbon = 50
marge = 40
size = 10
nb_couleurs = 5

grille = creation_grille(size, nb_couleurs)
images = create_images(taille_bonbon)

grille_bonbons = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 4, 5, 3, 2, 1, 2, 3, 5, 5, 3, 0, 0],
                  [0, 0, 5, 3, 5, 4, 1, 5, 3, 4, 5, 1, 0, 0],
                  [0, 0, 5, 2, 1, 3, 1, 2, 1, 4, 4, 1, 0, 0],
                  [0, 0, 1, 1, 3, 4, 2, 4, 2, 4, 1, 1, 0, 0],
                  [0, 0, 1, 2, 4, 4, 5, 2, 3, 2, 1, 4, 0, 0],
                  [0, 0, 5, 3, 3, 3, 5, 1, 2, 2, 4, 1, 0, 0],
                  [0, 0, 4, 5, 1, 4, 5, 4, 3, 1, 4, 3, 0, 0],
                  [0, 0, 4, 1, 1, 3, 4, 3, 3, 2, 3, 4, 0, 0],
                  [0, 0, 1, 4, 3, 5, 3, 1, 1, 1, 4, 5, 0, 0],
                  [0, 0, 1, 2, 2, 4, 5, 3, 3, 2, 1, 2, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

grille_bonbons_2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 4, 5, 3, 2, 1, 2, 3, 5, 5, 3, 0, 0],
                    [0, 0, 5, 3, 5, 4, 1, 5, 3, 4, 5, 1, 0, 0],
                    [0, 0, 5, 2, 1, 3, 1, 2, 1, 4, 4, 1, 0, 0],
                    [0, 0, 1, 1, 3, 4, 2, 4, 2, 4, 1, 1, 0, 0],
                    [0, 0, 1, 2, 4, 4, 5, 2, 3, 2, 1, 4, 0, 0],
                    [0, 0, 5, 3, 3, 3, 5, 1, 2, 2, 4, 1, 0, 0],
                    [0, 0, 4, 5, 1, 4, 5, 4, 3, 1, 4, 3, 0, 0],
                    [0, 0, 4, 1, 1, 3, 4, 3, 3, 2, 3, 4, 0, 0],
                    [0, 0, 1, 4, 3, 5, 3, 1, 1, 1, 4, 5, 0, 0],
                    [0, 0, 1, 2, 2, 4, 5, 3, 3, 2, 1, 2, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

grille_bonbons_deleted = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 4, 5, 3, 2, 1, 2, 3, 5, 5, 3, 0, 0],
                          [0, 0, 5, 3, 5, 4, 1, 5, 3, 0, 5, 1, 0, 0],
                          [0, 0, 5, 2, 1, 3, 1, 2, 1, 0, 4, 1, 0, 0],
                          [0, 0, 1, 1, 3, 4, 2, 4, 2, 0, 1, 1, 0, 0],
                          [0, 0, 1, 2, 4, 4, 5, 2, 3, 2, 1, 4, 0, 0],
                          [0, 0, 5, 0, 0, 0, 5, 1, 2, 2, 4, 1, 0, 0],
                          [0, 0, 4, 5, 1, 4, 5, 4, 3, 1, 4, 3, 0, 0],
                          [0, 0, 4, 1, 1, 3, 4, 3, 3, 2, 3, 4, 0, 0],
                          [0, 0, 1, 4, 3, 5, 3, 1, 1, 1, 4, 5, 0, 0],
                          [0, 0, 1, 2, 2, 4, 5, 3, 3, 2, 1, 2, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

grille_bonbons_3 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 5, 5, 5, 0, 0],
                    [0, 0, 2, 5, 4, 5, 3, 0, 0],
                    [0, 0, 3, 1, 2, 1, 4, 0, 0],
                    [0, 0, 5, 1, 3, 3, 1, 0, 0],
                    [0, 0, 4, 4, 5, 5, 5, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]

largeur_fenetre = (len(grille) - 4) * taille_bonbon + marge * 2
hauteur_fenetre = (len(grille[0]) - 4) * taille_bonbon + marge * 2

fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Candy Crush")

NOIR = (0, 0, 0)
rect = (marge / 2, marge / 2, (len(grille[0]) - 4) * taille_bonbon + marge, (len(grille[0]) - 4) * taille_bonbon + marge)


def affichage(table):
    fenetre.fill((255, 255, 255))

    for (k, liste) in enumerate(table[2:-2]):
        for (j, element) in enumerate(liste[2:-2]):
            x = j * taille_bonbon + marge
            y = k * taille_bonbon + marge

            fenetre.blit(images[element], (x, y))
    pygame.draw.rect(fenetre, NOIR, rect, 2)
    pygame.display.flip()


running = True
while running:
    affichage(grille_bonbons_deleted)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x1 = round(event.pos[0] / taille_bonbon, 2)
                y1 = round(event.pos[1] / taille_bonbon, 2)

            print(x1, y1)






pygame.quit()
