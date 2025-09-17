from matplotlib.backend_bases import MouseButton
from random import randint,shuffle
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np
import os


# def affiche_grille(grille,nb_couleurs,score,nb,first):
#     """affiche la grille pendant 0.1 sec"""
#     if first == True :
#         global plotid
#         plotid = plt.imshow(grille,vmin=0,vmax= nb_couleurs, cmap= 'jet')
#         plt.title(f"score :  = {score}      déplacements :  = {nb} ")
#         plt.draw()
#     else:
#         plotid.set_data(grille)
#         plt.title(f"score :  = {score}      déplacements :  = {nb} ")
#         plt.draw()
#     plt.pause(0.1)



chemin_images = os.path.join(os.path.dirname(__file__), 'pngs_candy_crush')
images = {
    0: os.path.join(chemin_images, 'blanc.png'),
    1: os.path.join(chemin_images, 'jaune.png'),
    2: os.path.join(chemin_images, 'violet.png'),
    3: os.path.join(chemin_images, 'bleu2.png'),
    4: os.path.join(chemin_images, 'vert.png'),
    5: os.path.join(chemin_images, 'orange.png'),
    6: os.path.join(chemin_images, 'rouge.png'),
    }


def images_from_grille(grille):
    liste_images = [[0 for _ in range(len(grille))]for _ in range(len(grille))]
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            liste_images[i][j] = imageio.imread(images[grille[i][j]])
    return liste_images

def affiche_grille(grille,nb_couleurs,score,nb,axes):
    """affiche la grille pendant 0.1 sec"""
    liste_images = images_from_grille(grille)
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            axes[i][j].set_data(liste_images[i][j])
    plt.title(f"score :  = {score}      déplacements :  = {nb} ")
    plt.pause(0.1)
    
def creation_grille(size,nb_couleurs):
    """crée une grille de taille size*size"""
    table = [[randint(1,nb_couleurs)for _ in range(size)]for _ in range(size)]
    for i in table:
        i.append(0)
        i.insert(0,0)
    table.append([0 for _ in range (size+2)])
    table.insert(0,[0 for _ in range (size+2)])
    return table

def detecte_voisins(grille,a,b):
    """renvoie les coordonnées des cases adjacentes à celle que l'on étudie"""
    liste = []
    couleur = grille[a][b]
    if grille[a+1][b] == couleur :
        liste.append((a+1,b))
    if grille[a-1][b] == couleur :
        liste.append((a-1,b))
    if grille[a][b+1] == couleur :
        liste.append((a,b+1))
    if grille[a][b-1] == couleur :
        liste.append((a,b-1))
    return liste

def detecte_coordonnees_1(grille,couple,liste_tot):
    couleur = grille[couple[0]][couple[1]]
    liste_col =[(couple[0],couple[1])]
    liste_li = [(couple[0],couple[1])]
    if grille[couple[0]+1][couple[1]] == couleur and (couple[0]+1,couple[1]) not in liste_tot:
        liste_col.append((couple[0]+1,couple[1]))
    if grille[couple[0]-1][couple[1]] == couleur and (couple[0]-1,couple[1]) not in liste_tot:
        liste_col.append((couple[0]-1,couple[1]))
    if grille[couple[0]][couple[1]+1] == couleur and (couple[0],couple[1]+1) not in liste_tot:
        liste_li.append((couple[0],couple[1]+1))
    if grille[couple[0]][couple[1]-1] == couleur and (couple[0],couple[1]-1) not in liste_tot:
        liste_li.append((couple[0],couple[1]-1))
    v = False
    if len(liste_col) == 3 :
        v = liste_col
    elif len(liste_li) == 3 :
        v = liste_li
    return v

def detecte_coordonnees_2(grille,couple):
    couleur = grille[couple[0]][couple[1]]
    liste_col =[(couple[0],couple[1])]
    liste_li = [(couple[0],couple[1])]
    if grille[couple[0]+1][couple[1]] == couleur :
        liste_col.append((couple[0]+1,couple[1]))
    if grille[couple[0]-1][couple[1]] == couleur :
        liste_col.append((couple[0]-1,couple[1]))
    if grille[couple[0]][couple[1]+1] == couleur :
        liste_li.append((couple[0],couple[1]+1))
    if grille[couple[0]][couple[1]-1] == couleur :
        liste_li.append((couple[0],couple[1]-1))
    v = False
    if len(liste_col) == 3 :
        v = liste_col
    elif len(liste_li) == 3 :
        v = liste_li
    return v

def detecte_coordonnees_3(grille,a,b):
    """propagation, toutes les cases appartenant à un groupe adjacent à la case étudiée sont données"""
    liste_voisins = [(a,b)]
    c = 1
    while c != 0 :
        for bi in liste_voisins :
            lis = detecte_voisins(grille,bi[0],bi[1])
            c = 0
            for i in lis :
                c = 0
                if i not in liste_voisins :
                    c = c + 1
                    liste_voisins.append(i)
    """verification, ok si il y a bien 3 cases alignées dans la combinaison"""
    v = []
    liste_colonnes = []
    liste_lignes = []
    for i in liste_voisins :
        liste_colonnes.append(i[1])
        liste_colonnes.sort()
        liste_lignes.append(i[0])
        liste_lignes.sort()
    for x in range(len(liste_colonnes)-2):
        for n in range(max(liste_colonnes)+1):
            if [n,n,n] == liste_colonnes[x:x+3] :
                v = liste_voisins
    for y in range(len(liste_colonnes)-2):
        for k in range(max(liste_lignes)+1):
            if [k,k,k] == liste_lignes[y:y+3]:
                v = liste_voisins
    return v

def detecte_coordonnes_totales(grille,niv):
    """effectue la somme des coordonnées à supprimer"""
    liste_totale = []
    for i in  range(1,len(grille)-1) :
        for j in range(1,len(grille)-1) :
            if niv == 3 :
                a = detecte_coordonnees_3(grille,i,j)
            elif niv == 2 :
                a = detecte_coordonnees_2(grille,(i,j))
            elif niv == 1:
                a = detecte_coordonnees_1(grille,(i,j),liste_totale)
            if a != False :
                for k in a:
                    if k not in liste_totale :
                        liste_totale.append(k)
    return liste_totale

def supression(table,list_coord):
    """supprime les cases à supprimer"""
    for (a,b) in list_coord :
        table[a][b] = 0
    return table

def update(grille,nb_couleurs):
    """descend des cases à la place des cases vides et crée un élément aléatoire en haut de la grille"""
    c = 0
    for ligne in range(1,len(grille)-1) :
        for colonne in range(1,len(grille)-1):
            if grille[ligne][colonne] == 0:
                c = c + 1
                for k in range(0,ligne):
                    grille[ligne-k][colonne] = grille[ligne -k-1][colonne]
                grille[1][colonne] = randint(1,nb_couleurs)
    v = False
    if c > 0 :
        v = True
    return v,grille

def on_click(event):
    """sert pour la souris"""
    global x,y
    if event.button is MouseButton.LEFT and event.inaxes :
        x,y = int(round(event.xdata,0)) , int(round(event.ydata,0))

def fin(grille):
    for a in range(1,len(grille)-2):
        for b in range(1,len(grille)-2):
            if possible(grille,b,a,b,a+1) == True:
                return False
            if possible(grille,b,a,b+1,a) == True:
                return False
    return True

def possible(grille,x1,y1,x2,y2):
    """verifie si un mouvement est possible"""
    temp = []
    for i in grille :
        sous_liste = []
        for j in i:
            sous_liste.append(j)
        temp.append(sous_liste)     
    v = True
    """module"""
    if sqrt((x1-x2)**2+(y1-y2)**2) > 1:
        v = False
    """simulation du coup pour voir s'il est possible (possible si il crée une solution)"""
    temp[y1][x1],temp[y2][x2]=temp[y2][x2],temp[y1][x1]
    if len(detecte_coordonnees_3(temp,y1,x1)) == 0 and len(detecte_coordonnees_3(temp,y2,x2)) == 0 :
        v =  False
    return v

def mélange(grille):
    ngrille = []
    for i in range(1,len(grille)-1) :
        for j in range(1,len(grille[i])-1):
            ngrille.append(grille[i][j])
    shuffle(ngrille)
    n = 0
    for k in range(1,len(grille)-1) :
        for l in range(1,len(grille[k])-1):
            grille[k][l] = ngrille[n]
            n = n + 1
    return grille

def jeu(nb_coups,size,couleurs,niv):
    nb_couleurs = couleurs
    nb = nb_coups
    score = 0
    """crée la premiere grille et l'update"""
    grille = creation_grille(size,nb_couleurs)
    bool = True
    while bool != False :
        while fin(grille) == True :
            print("Mélange !!")
            mélange(grille)
        liste1 = detecte_coordonnes_totales(grille,niv)
        score = score + len(liste1)
        grille = supression(grille,liste1)
        bool,grille = update(grille,nb_couleurs)
    
    liste_images = images_from_grille(grille)
    fig, plotid = plt.subplots(figsize=(size+2,size+2))
    plotid.set_xlim([-0.5, size+2-0.5])
    plotid.set_ylim([size+2-0.5, -0.5])
    plotid.set_aspect('equal')
    axes = [[0 for _ in range(len(grille))]for _ in range(len(grille))]
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            axes[i][j] = plt.imshow(liste_images[i][j], extent=[j-0.5, j+0.5, i+0.5, i-0.5])
    """code du jeu répété i fois"""
    i = 0
    while i < nb :
        affiche_grille(grille,nb_couleurs,score,nb_coups-i,axes)
        a = plt.connect('button_press_event', on_click)
        while plt.waitforbuttonpress():
            break
        x1 = x
        y1 = y
        plt.disconnect(a)
        b = plt.connect('button_press_event', on_click)
        while plt.waitforbuttonpress():
            break
        x2 = x
        y2 = y
        plt.disconnect(b)
        if possible(grille,x1,y1,x2,y2) == True :
            i = i + 1
            grille[y1][x1],grille[y2][x2]=grille[y2][x2],grille[y1][x1]
            bool = True
            while bool != False :
                liste1 = detecte_coordonnes_totales(grille,niv)
                score = score + len(liste1)
                grille = supression(grille,liste1)
                affiche_grille(grille,nb_couleurs,score,nb_coups-i,axes)
                bool,grille = update(grille,nb_couleurs)
                while fin(grille) == True :
                    print("Mélange !!")
                    mélange(grille)
                affiche_grille(grille,nb_couleurs,score,nb_coups-i,axes)
        else :
            print("coup impossible")
    plt.text(4,4, str(score), fontsize=50, color='black')
    plt.pause(5)

def jeu_final():
    """lance le programme final"""
    coups = int(input("combien de coups :"))
    size_grille = int(input("taille de jeu :"))
    coul = int(input("nb de couleurs :"))
    niv =  int(input("niveau de jeu :"))
    # coups = 10
    # size_grille = 6
    # coul = 5
    # niv = 3
    jeu(coups,size_grille,coul,niv)


jeu_final()


