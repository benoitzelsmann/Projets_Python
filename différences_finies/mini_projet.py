import matplotlib.pyplot as plt
import numpy as np


# Paramètres 
rint = 30e-3
rext = 75e-3
rinj = 48e-3
Pe = 10e5  # Patm
Ppi = 1.0967 * 10e5  # a voir
N = 5

tetamin = 0
tetamax = np.pi/6

rmoy = (rext + rint)/2

xmin = tetamax*rmoy
xmax = tetamax*rmoy


dr = (rext - rint) / (N - 1)

r1 = np.linspace(rint, rext, N)
x1 = np.linspace(xmin, xmax, N)


A1 = np.zeros((N, N))
B1 = np.zeros(N)


for i in range(1, N - 1):

        A1[i, i - 1] = rint + dr * (i - (1 / 2))
        A1[i, i] = -((rint + dr * (i + (1 / 2))) + (rint + dr * (i - (1 / 2))))
        A1[i, i + 1] = rint + dr * (i + (1 / 2))



print(A1)

A1[0, 0] = 1

A1[(N-1)//2, (N-1)//2] = 1

A1[N - 1, N - 1] = 1

B1[0] = Pe ** 2
B1[N - 1] = Pe ** 2

B1[(N-1)//2] = Ppi ** 2


# Solution

Q1 = np.linalg.solve(A1, B1)
print(Q1)

P1 = np.sqrt(Q1)


r_global = r1  # r2[1,:] permet d'éviter le doublon en rinj
Q_global = Q1.flatten()
P_global = P1.flatten()

plt.figure(figsize=(10, 5))
plt.plot(r_global, Q_global, label='Q(r)')
plt.xlabel('Rayon (m)')
plt.ylabel('Q')
plt.title('Distribution de Q sur [rint, rext]')
plt.grid(True)
plt.legend()
plt.show()

# Tracé global de P
plt.figure(figsize=(10, 5))
plt.plot(r_global, P_global, label='P(r)', color='orange')
plt.xlabel('Rayon (m)')
plt.ylabel('Pression (Pa)')
plt.title('Distribution de la pression sur [rint, rext]')
plt.grid(True)
plt.legend()
plt.show()
