import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from bibli_perso.selec_var import selection_variables


precision = 2000
nb_tours = 10
tours = 1

var = ['len_1', 'len_2', 'len_3', "rapport_vitesse_1", "rapport_vitesse_2"]


len_1, len_2, len_3, rapport_vitesse_1, rapport_vitesse_2 = selection_variables(10, *var)

# mickey : 4,2,1   2,6


def update(frame):
    ax.clear()
    ax.set_facecolor('black')
    ax.set_xlim(-13, 13)
    ax.set_ylim(-13, 13)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.plot([0, coords_x_1[frame]], [0, coords_y_1[frame]], 'ko-')
    ax.plot([coords_x_1[frame], coords_x_2[frame]], [coords_y_1[frame], coords_y_2[frame]], 'ko-')
    ax.plot([coords_x_2[frame], coords_x_3[frame]], [coords_y_2[frame], coords_y_3[frame]], 'ko-')
    ax.plot(coords_x_3[:frame + 1], coords_y_3[:frame + 1], 'r-', alpha=0.5)


def create_frames(l1, l2, l3):
    angles_1 = np.linspace(np.pi/2.0, (2 * np.pi*nb_tours + np.pi/2.0), precision)
    angles_2 = np.linspace(np.pi/2.0, (2 * np.pi*rapport_vitesse_1*nb_tours + np.pi/2.0), precision)
    angles_3 = np.linspace(np.pi/2.0, (2 * np.pi * rapport_vitesse_2 * nb_tours + np.pi / 2.0), precision)

    x_ends = [l1 * np.cos(angle) for angle in angles_1]
    y_ends = [l1 * np.sin(angle) for angle in angles_1]

    x_ends_2 = [x_1 + l2 * np.cos(angle) for angle, x_1 in zip(angles_2, x_ends)]
    y_ends_2 = [y_1 + l2 * np.sin(angle) for angle, y_1 in zip(angles_2, y_ends)]

    x_ends_3 = [x_1 + l3 * np.cos(angle) for angle, x_1 in zip(angles_3, x_ends_2)]
    y_ends_3 = [y_1 + l3 * np.sin(angle) for angle, y_1 in zip(angles_3, y_ends_2)]

    return x_ends, y_ends, x_ends_2, y_ends_2, x_ends_3, y_ends_3


coords_x_1, coords_y_1, coords_x_2, coords_y_2, coords_x_3, coords_y_3 = create_frames(l1=len_1, l2=len_2, l3=len_3)


fig, ax = plt.subplots()


# Création de l'animation
ani = FuncAnimation(fig, update, precision, interval=1)


# Affichage de l'animation
plt.show()
