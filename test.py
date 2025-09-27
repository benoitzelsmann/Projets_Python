
import numpy as np
import matplotlib.pyplot as plt

# Chargement des données
data = np.loadtxt(r"C:\Users\benoi\Downloads\current_ramp.txt", skiprows=1)  # skiprows=1 pour ignorer l'entête

time = data[:, 0]      # première colonne
voltage = data[:, 1]   # deuxième colonne
current = data[:, 2]   # troisième colonne

# Tracé
fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Vout_ (V)', color=color)
ax1.plot(time, voltage, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # axe Y secondaire
color = 'tab:red'
ax2.set_ylabel('I_out (A)', color=color)
ax2.plot(time, current, color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(0, 100)
plt.title("Buck Converter, Load Step")
plt.grid(True)
plt.show()
