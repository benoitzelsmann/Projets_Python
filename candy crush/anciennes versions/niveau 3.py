from random import randint
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from math import sqrt

def affiche_grille(grille,nb_couleurs,score,nb):
    plt.imshow(grille, vmin = 0, vmax = nb_couleurs, cmap = 'jet')
    plt.title(f"score :  = {score}      déplacements :  = {nb} ")
    while plt.waitforbuttonpress():
        plt.close()
        break

def creation_grille(size,nb_couleurs):
    table = [[randint(1,nb_couleurs)for _ in range(size)]for _ in range(size)]
    for i in table:
        i.append(0)
        i.insert(0,0)
    table.append([0 for _ in range (size+2)])
    table.insert(0,[0 for _ in range (size+2)])
    return table

def detecte_voisins(grille,tuple):
    liste = []
    couleur = grille[tuple[0]][tuple[1]]
    if grille[tuple[0]+1][tuple[1]] == couleur :
        liste.append((tuple[0]+1,tuple[1]))
    if grille[tuple[0]-1][tuple[1]] == couleur :
        liste.append((tuple[0]-1,tuple[1]))
    if grille[tuple[0]][tuple[1]+1] == couleur :
        liste.append((tuple[0],tuple[1]+1))
    if grille[tuple[0]][tuple[1]-1] == couleur :
        liste.append((tuple[0],tuple[1]-1))
    return liste

def detecte_coordonnes(grille,couple):
    """propagation"""
    liste_voisins = [(couple[0],couple[1])]
    c = 1
    while c != 0 :
        for tuple in liste_voisins :
            a = detecte_voisins(grille,tuple)
            c = 0
            for i in a :
                c = 0
                if i not in liste_voisins :
                    c = c + 1
                    liste_voisins.append(i)
    """verification"""
    v = False
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

def detecte_coordonnes_totales(grille):
    liste_totale = []
    for i in  range(1,len(grille)-1) :
        for j in range(1,len(grille)-1) :
            a = detecte_coordonnes(grille,(i,j))
            if a != False :
                for k in a:
                    if k not in liste_totale :
                        liste_totale.append(k)
    return liste_totale

def supression(table,list_coord):
    for tuple in list_coord :
        table[tuple[0]][tuple[1]] = 0
    return table

def update(grille,nb_couleurs):
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
    global x,y
    if event.button is MouseButton.LEFT and event.inaxes :
        x,y = int(round(event.xdata,0)) , int(round(event.ydata,0))

def possible(grille,tuple1,tuple2):
    temp = []
    for i in grille :
        sous_liste = []
        for j in i:
            sous_liste.append(j)
        temp.append(sous_liste)     
    v = True
    if sqrt((tuple1[0]-tuple2[0])**2+(tuple1[1]-tuple2[1])**2) > 1:
        v = False
    temp[tuple1[1]][tuple1[0]],temp[tuple2[1]][tuple2[0]]=temp[tuple2[1]][tuple2[0]],temp[tuple1[1]][tuple1[0]]
    if len(detecte_coordonnes_totales(temp)) == 0:
        v =  False
    return v

def jeu(nb_coups,size,couleurs):
    nb_couleurs = couleurs
    nb = nb_coups
    score = 0
    grille = creation_grille(size,nb_couleurs)
    bool = True
    while bool != False :
        liste1 = detecte_coordonnes_totales(grille)
        score = score + len(liste1)
        grille = supression(grille,liste1)
        bool,grille = update(grille,nb_couleurs)
    i = 0
    while i < nb :
        a = plt.connect('button_press_event', on_click)
        affiche_grille(grille,nb_couleurs,score,nb_coups-i)
        x1 = x
        y1 = y
        plt.disconnect(a)
        b = plt.connect('button_press_event', on_click)
        affiche_grille(grille,nb_couleurs,score,nb_coups - i)
        x2 = x
        y2 = y
        plt.disconnect(b)
        if possible(grille,(x1,y1),(x2,y2)) == True:
            i = i + 1
            grille[y1][x1],grille[y2][x2]=grille[y2][x2],grille[y1][x1]
            bool = True
            while bool != False :
                liste1 = detecte_coordonnes_totales(grille)
                score = score + len(liste1)
                grille = supression(grille,liste1)
                bool,grille = update(grille,nb_couleurs)
        else :
            print("coup impossible")
    plt.text(4,4, str(score), fontsize=50, color='white')
    plt.pause(5)

jeu(20,7,6)