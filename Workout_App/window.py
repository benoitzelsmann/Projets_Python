import tkinter as tk
import json
import os

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.repetitions = None
        self.nb_zones = None
        self.difficulty = None
        self.title("Configuration de l'exercice")

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Facile")  # Valeur par défaut

        self.zones_var = tk.IntVar()
        self.zones_var.set(2)  # Valeur par défaut

        # Frame pour les boutons radio de la difficulté
        difficulty_frame = tk.Frame(self)
        difficulty_frame.pack(pady=10)

        tk.Label(difficulty_frame, text="Difficulté de l'exercice:", font=("Helvetica", 12, "bold")).pack()

        difficulties = ["Facile", "Moyen", "Difficile"]
        for difficulty in difficulties:
            tk.Radiobutton(difficulty_frame, text=difficulty, variable=self.difficulty_var, value=difficulty,
                           font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

        # Frame pour les boutons radio du nombre de zones
        zones_frame = tk.Frame(self)
        zones_frame.pack(pady=10)

        tk.Label(zones_frame, text="Nombre de zones à travailler:", font=("Helvetica", 12, "bold")).pack()

        for zones in range(2, 5):
            tk.Radiobutton(zones_frame, text=str(zones), variable=self.zones_var, value=zones,
                           font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)

        # Frame pour les boutons de répétitions
        repetitions_frame = tk.Frame(self)
        repetitions_frame.pack(pady=10)

        tk.Label(repetitions_frame, text="Nombre de répétitions:", font=("Helvetica", 12, "bold")).pack()

        for repetitions in [1, 2, 3]:
            button = tk.Button(repetitions_frame, text=str(repetitions),
                               command=lambda r=repetitions: self.generate_workout(r), font=("Helvetica", 12, "bold"))
            button.pack(side=tk.LEFT, padx=10)
            button.config(width=8, height=2)  # Ajustement de la taille des boutons

    def generate_workout(self, repetitions):
        self.difficulty = self.difficulty_var.get()
        self.nb_zones = self.zones_var.get()
        self.repetitions = repetitions
        self.quit()


    def __str__(self):
        res = str(type(self).__name__).upper() + '\n'
        for (key, value) in vars(self).items():
            res += f'{key} : {value}\n'
        return res


class SummaryWindow(tk.Tk):
    def __init__(self, workout_summary, repetitions):
        super().__init__()

        dir = os.path.dirname(__file__)

        self.recap_exos = json.load(open(dir + '\\recap_exos.json', 'r', encoding='utf-8'))

        self.title("Résumé de l'entraînement")
        hauteur_ligne = 35
        hauteur = 195 + len(workout_summary.keys()) * hauteur_ligne
        self.geometry(f"420x{hauteur}")

        repetitions_label = tk.Label(self, text=f"Nombre de répétitions: {repetitions}".upper(), font=("Helvetica", 13, "bold"), fg='red')
        repetitions_label.pack(pady=10)

        self.summary_frame = tk.Frame(self)
        self.summary_frame.pack()

        self.detail_buttons = []
        row = 1
        tk.Label(self.summary_frame, text="Exercice", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.summary_frame, text="Durée / Répétitions", font=("Helvetica", 12, "bold")).grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        for exercise in workout_summary:

            tk.Label(self.summary_frame, text=exercise, font=("Helvetica", 11)).grid(row=row, column=0, padx=5, pady=5, sticky="n")
            tk.Label(self.summary_frame, text=workout_summary[exercise], font=("Helvetica", 11, "bold")).grid(row=row, column=1, padx=5, pady=5, sticky="e")
            detail_button = tk.Button(self.summary_frame, text="Détails", command=lambda e=exercise: self.show_details(e),  bg="lightblue", fg="black", relief="flat")
            detail_button.grid(row=row, column=2, padx=5, pady=5)
            self.detail_buttons.append(detail_button)
            row += 1

        self.detail_frame = tk.Frame(self)
        self.detail_text = tk.Text(self.detail_frame, wrap=tk.WORD, height=4, width=40, font=("Helvetica", 11), bd=0, highlightthickness=0, bg="white")
        self.detail_text.pack(padx=10, pady=5)
        self.detail_frame.pack_forget()





    def show_details(self, exercise):
        detail_text = self.recap_exos[exercise]['description']
        self.detail_text.delete(1.0, tk.END)  # Effacer le contenu précédent
        self.detail_text.insert(tk.END, detail_text)
        self.detail_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=(10, 20))



