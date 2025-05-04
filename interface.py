# -*- coding: utf-8 -*-
import tkinter as tk
import time

temps = 0
lst_chiffre = []
bontons = []  # Changé de "boutons" à "bontons" pour correspondre à votre extrait
valeur_chiffre = ""

def interface():
    # Création de la fenêtre principale
    fenetre_principal = tk.Tk()
    fenetre_principal.title("Projet informatique")
    fenetre_principal.geometry("600x600")
    fenetre_principal.config(bg="#E2EAF4")

    # Création de la fenêtre du sudoku
    fenetre_sudoku = tk.Canvas(fenetre_principal, height=550, width=800, bg="#98F5F9", bd=3)
    fenetre_sudoku.pack(pady=10)

    # Création du bouton nouvelle partie
    bouton_nouvelle_partie = tk.Button(fenetre_principal, text="Nouvelle Partie", width=20, height=2, font="Arial", bg="white")
    bouton_nouvelle_partie.pack(pady=10)

    # Création du bouton quitter
    button_quiter_partie = tk.Button(fenetre_sudoku, text="Quitter", width=10, height=2, bg="white", font=("Arial", 13))
    button_quiter_partie.place(x=500, y=15)

    # Création des cadres
    cadre_sudoku = tk.Frame(fenetre_sudoku, width=400, height=200, bg="black")
    cadre_sudoku.place(x=20, y=80)
    cadre_nombre = tk.Frame(fenetre_sudoku, width=260, height=300, bg='white')
    cadre_nombre.place(x=500, y=230)

    # Création des boutons de contrôle
    bouton_reture = tk.Button(fenetre_sudoku, text="↶", width=10, height=2, bg="white", font="Arial")
    bouton_reture.place(x=500, y=160)
    bouton_supprime = tk.Button(fenetre_sudoku, text="x", width=10, height=2, bg="white", font="Arial")
    bouton_supprime.place(x=640, y=160)

    # Création des boutons de niveaux
    bouton_facile = tk.Button(fenetre_sudoku, text="Facile", width=6, height=1, bg="white", font="Arial")
    bouton_facile.place(x=120, y=13)
    bouton_moyen = tk.Button(fenetre_sudoku, text="Moyen", width=6, height=1, bg="white", font="Arial")
    bouton_moyen.place(x=190, y=13)
    bouton_dificile = tk.Button(fenetre_sudoku, text="Difficile", width=6, height=1, bg="white", font="Arial")
    bouton_dificile.place(x=260, y=13)
    bouton_expert = tk.Button(fenetre_sudoku, text="Expert", width=6, height=1, bg="white", font="Arial")
    bouton_expert.place(x=330, y=13)

    # Création des labels
    label_niveux = tk.Label(fenetre_sudoku, text="Difficulté :", width=10, height=2, font="Arial")
    label_niveux.place(x=20, y=5)

    # Création de la case de l'heure
    label_temp = tk.Label(fenetre_sudoku, width=10, height=2, font=("Arial", 13))
    label_temp.place(x=650, y=15)

    # Création des boutons de nombres
    z = 1
    for i in range(3):
        for e in range(3):
            button_numero = tk.Button(cadre_nombre, text=str(z), width=10, height=5, bg="white", command=lambda chiffre=z: choisir_chiffre(chiffre))
            button_numero.grid(row=i, column=e)
            z += 1

    # Création des grilles de sudoku
    button = None
    for t in range(3):
        for y in range(3):
            case = tk.Frame(cadre_sudoku, width=15, height=5, bg="black", padx=1, pady=1)
            case.grid(row=t, column=y)
            for o in range(3):
                for p in range(3):
                    button = tk.Button(case, width=4, height=2, bg="#FFECA1", padx=1, pady=1, font="Arial")
                    button.config(command=lambda b=button: placer(b, valeur_chiffre))
                    button.grid(row=o, column=p)

    # Fonction pour afficher le temps
    def creation_temps():
        global temps
        temps += 1
        heures = temps // 3600
        minutes = (temps % 3600) // 60
        secondes = temps % 60
        label_temp.config(text=f"{heures:02}:{minutes:02}:{secondes:02}")
        label_temp.after(1000, creation_temps)

    # Démarrer le chronomètre
    creation_temps()

    # Fonction pour quitter la partie
    def quitter_partie():
        fenetre_principal.destroy()

    button_quiter_partie.config(command=quitter_partie)

    # Fonction pour commencer une nouvelle partie
    def nouvelle_partie():
        nouvelle_fenetre = tk.Toplevel()
        nouvelle_fenetre.title("Nouvelle Partie")
        nouvelle_fenetre.geometry("300x200")

    bouton_nouvelle_partie.config(command=nouvelle_partie)

    # Fonction pour choisir un chiffre
    def choisir_chiffre(chiffre):
        global valeur_chiffre
        valeur_chiffre = str(chiffre)
        lst_chiffre.append(valeur_chiffre)

    # Fonction pour placer un chiffre dans une case
    def placer(b, valeur_chiffre):
        global bontons
        for entry in bontons:
            if b in entry:
                entry[b].append(valeur_chiffre)
                break
        else:
            bontons.append({b: [valeur_chiffre]})
        b.config(text=valeur_chiffre)
        print(f"État des boutons : {bontons}")

    # Fonction pour revenir en arrière
    def revenir_en_arriere():
        global valeur_chiffre, bontons
        if bontons:
            dernier_bouton_dict = bontons[-1]
            b = list(dernier_bouton_dict.keys())[0]  # Récupère le bouton du dernier dictionnaire
            valeurs = dernier_bouton_dict[b]
            if len(valeurs) > 1:
                valeurs.pop(-1)
                valeur_chiffre = valeurs[-1]
            else:
                bontons.pop(-1)
                valeur_chiffre = ""
            b.config(text=valeur_chiffre)
            print(f"Valeur actuelle : {valeur_chiffre}")
            print(f"État des boutons : {bontons}")
        else:
            print("Aucun bouton dans la liste.")

    bouton_reture.config(command=revenir_en_arriere)

    #Fonction pour supprimer
    def supprimer():
        global valeur_chiffre, bontons
        if bontons:
            dernier_bouton_dict = bontons[-1]
            b = list(dernier_bouton_dict.keys())[0]
            valeurs = dernier_bouton_dict[b]
            if len(valeurs) > 1:
                valeurs.pop(-1)
                valeur_chiffre = valeurs[-1]
            else:
                bontons.pop(-1)
                valeur_chiffre = ""
            b.config(text=valeur_chiffre)
            lst_chiffre.append(valeur_chiffre)
            print(f"Valeur actuelle : {valeur_chiffre}")
            print(f"État des boutons : {bontons}")
        else:
            print("Aucun bouton à supprimer.")

    bouton_supprime.config(command=supprimer)

    fenetre_principal.mainloop()

interface()