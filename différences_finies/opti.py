import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve

# Paramètres
rint = 30e-3
rext = 75e-3
rinj = 48e-3
Pe = 10e5
Ppi = 1.0967 * 10e5
N = 50

Nr = N
Nθ = 12 * N
size = Nr * Nθ

A = lil_matrix((size, size))
B = np.zeros(size)

dr = (rext - rint) / (Nr - 1)
rmoy = (rext + rint) / 2
dx = (2 * np.pi * rmoy) / (Nθ - 1)
Ninj = int(Nr * rinj / rext)

# Construction du système
for i in range(Nr):
    for j in range(Nθ):
        idx = i * Nθ + j

        if i == 0 or i == Nr - 1:
            A[idx, idx] = 1
            B[idx] = Pe ** 2
        elif (j % (Nθ // 12) == 0) and i == Ninj:
            A[idx, idx] = 1
            B[idx] = Ppi ** 2
        else:
            r_i = rint + i * dr
            A[idx, idx] = -((rint + dr * (i + 0.5)) + (rint + dr * (i - 0.5))) / dr**2 - 2 * rmoy / dx**2
            if i > 0:
                A[idx, idx - Nθ] = (rint + dr * (i - 0.5)) / dr**2
            if i < Nr - 1:
                A[idx, idx + Nθ] = (rint + dr * (i + 0.5)) / dr**2
            A[idx, idx - 1 if j > 0 else idx + Nθ - 1] = rmoy / dx**2
            A[idx, idx + 1 if j < Nθ - 1 else idx - Nθ + 1] = rmoy / dx**2

# Conversion en format compressé pour solution rapide
A = csr_matrix(A)

# Résolution
Q1 = spsolve(A, B)
P1 = np.sqrt(Q1).reshape((Nr, Nθ))

# Coordonnées
r = np.linspace(rint, rext, Nr)
theta = np.linspace(0, 2 * np.pi, Nθ)
R, T = np.meshgrid(r, theta, indexing='ij')
X = R * np.cos(T)
Y = R * np.sin(T)

# Affichage
fig, ax = plt.subplots(figsize=(6, 6))
pcm = ax.pcolormesh(X, Y, P1, shading='auto', cmap='viridis')
plt.colorbar(pcm, label='Pression')
plt.title("Champ de pression dans un anneau avec 12 injecteurs")
ax.set_aspect('equal')
ax.axis('off')
plt.show()
