import matplotlib.pyplot as plt
import numpy as np

# Paramètres
rint = 30e-3
rext = 75e-3
rinj = 48e-3
Pe = 10e5
Ppi = 1.0967 * 10e5

N = 50
size = N*N

A = np.zeros((size, size))
B = np.zeros(size)

tetamin = 0
tetamax = np.pi / 6
rmoy = (rext + rint) / 2
xmin = tetamin * rmoy
xmax = tetamax * rmoy

Ninj = int(N * (rinj / rext))

dr = (rext - rint) / (N - 1)
dx = (xmax - xmin) / (N - 1)

# Construction du système
for i in range(N):
    for j in range(N):
        idx = i * N + j

        if i == 0 or i == N - 1:
            # Conditions aux bords
            A[idx, idx] = 1
            B[idx] = Pe ** 2
        elif (j == 0 or j == N - 1) and i == Ninj:
            A[idx, idx] = 1
            B[idx] = Ppi ** 2

        else:

            A[idx, idx] = (-((rint + dr * (i + 0.5)) + (rint + dr * (i - 0.5))) / dr ** 2
                           - 2 * rmoy / dx ** 2)
            A[idx, idx - N] = (rint + dr * (i - 0.5)) / dr ** 2
            A[idx, idx + N] = (rint + dr * (i + 0.5)) / dr ** 2
            A[idx, idx - 1] = rmoy / dx ** 2
            A[idx, idx + 1] = rmoy / dx ** 2

# Résolution
Q1 = np.linalg.solve(A, B)
P1 = np.sqrt(Q1)

P1 = P1.reshape((N, N))
P1_repeated = np.tile(P1, (1, 12))  # (N, N*10)

# ---- Coordonnées polaires ----
r = np.linspace(rint, rext, N)
theta = np.linspace(0, 2 * np.pi, N * 12)
R, T = np.meshgrid(r, theta, indexing='ij')

# ---- Conversion en cartésien ----
X = R * np.cos(T)
Y = R * np.sin(T)

# ---- Affichage ----
fig, ax = plt.subplots(figsize=(6, 6))
pcm = ax.pcolormesh(X, Y, P1_repeated, shading='auto', cmap='viridis')
plt.colorbar(pcm, label='Pression')
plt.title("Champ de pression dans un anneau avec 12 injecteurs")
ax.set_aspect('equal')
ax.axis('off')
plt.show()
