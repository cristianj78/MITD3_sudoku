import tkinter as tk
import fonctions as fct


bg_color = "#E2EAF4"

root = tk.Tk()
root.title("Sudoku")
root.geometry("600x600")
root.config(bg=bg_color)

###Faudra utiliser cascade avec les options..
menu = tk.Menu(root)
Accueil = menu.add_command(label="Accueil")
menu.add_separator()
Nouvelle_partie = menu.add_command(label="Nouvelle Partie", command=lambda: fct.changement_frame(root, menu, frame_menu, frame_nouvelle_partie, frame_nouvelle_partie))
menu.add_separator()
Sauvegarder = menu.add_command(label="Sauvegarder")
menu.add_separator()
Quitter = menu.add_command(label="Quitter", command=root.destroy)


# FRAME MENU
frame_menu = tk.Frame(root)
frame_menu.pack()

    #LABEL SUDOKU
frame_label_sudoku = tk.Frame(frame_menu, width=600, height=200, bg=bg_color)
frame_label_sudoku.pack()

label1 = tk.Label(frame_label_sudoku, text="S", bg=bg_color, font=("Arial", 60))
label1.place(x=120, y=0)
label2 = tk.Label(frame_label_sudoku, text="u", bg=bg_color, font=("Arial", 60))
label2.place(x=180, y=20)
label3 = tk.Label(frame_label_sudoku, text="d", bg=bg_color, font=("Arial", 60))
label3.place(x=240, y=40)
label4 = tk.Label(frame_label_sudoku, text="o", bg=bg_color, font=("Arial", 60))
label4.place(x=300, y=60)
label5 = tk.Label(frame_label_sudoku, text="k", bg=bg_color, font=("Arial", 60))
label5.place(x=360, y=40)
label6 = tk.Label(frame_label_sudoku, text="u", bg=bg_color, font=("Arial", 60))
label6.place(x=420, y=20)

fct.deplacer(label1,descend = True, root=root)
fct.deplacer(label2,descend = True, root=root)
fct.deplacer(label3,descend = True, root=root)
fct.deplacer(label4,descend = True, root=root)
fct.deplacer(label5,descend=False, root=root)
fct.deplacer(label6,descend=False, root=root)

    #BOUTONS
frame_buttons = tk.Frame(frame_menu, bg=bg_color)
frame_buttons.pack(fill="both")

button_reprendre = tk.Button(frame_buttons, text="Reprendre la partie", font=("Arial", 27))
button_reprendre.pack(pady=10)

button_nvl_partie = tk.Button(frame_buttons, text="Nouvelle partie", font=("Arial", 27), command=lambda: fct.changement_frame(root, menu, frame_menu, frame_nouvelle_partie, frame_nouvelle_partie))
button_nvl_partie.pack(pady=10)

button_reprendre_sauvegarde = tk.Button(frame_buttons, text="Autres sauvegardes", font=("Arial", 27))
button_reprendre_sauvegarde.pack(pady=10)

# FRAME NOUVELLE PARTIE
frame_nouvelle_partie = tk.Frame(root)

    #CHOIX DIFFICULTE
difficulte = "Normal"

frame_difficulte = tk.Frame(frame_nouvelle_partie, bg=bg_color)

label_difficulte = tk.Label(frame_difficulte, text="Choisis la difficulté", bg=bg_color, font=("Arial", 13))

button_facile = tk.Button(frame_difficulte, text="Facile", font=("Arial", 13), command=lambda: fct.changement_difficulte("Facile", liste_button, button_facile, button_facile, button_normal, button_difficile, button_extreme))
button_normal = tk.Button(frame_difficulte, text="Normal", font=("Arial", 13), state="disabled", command=lambda: fct.changement_difficulte("Normal", liste_button, button_normal, button_facile, button_normal, button_difficile, button_extreme))
button_difficile = tk.Button(frame_difficulte, text="Difficile", font=("Arial", 13), command=lambda: fct.changement_difficulte("Difficile", liste_button, button_difficile, button_facile, button_normal, button_difficile, button_extreme))
button_extreme = tk.Button(frame_difficulte, text="Extreme", font=("Arial", 13), command=lambda: fct.changement_difficulte("Extreme", liste_button, button_extreme, button_facile, button_normal, button_difficile, button_extreme))
frame_modeles = tk.Frame(frame_nouvelle_partie, bg=bg_color, pady= 10)


frame_difficulte.pack(fill="x")
label_difficulte.grid(column=0, row=0)
button_facile.grid(column=1, row=0, padx=3)
button_normal.grid(column=2, row=0, padx=3)
button_difficile.grid(column=3, row=0, padx=3)
button_extreme.grid(column=4, row=0, padx=3)
frame_modeles.pack(fill="both")

    #CHOIX MODELE
sudoku_liste_choix = []
sudoku1_incomplet, sudoku1_complet = fct.suppression_solution(difficulte)
sudoku2_incomplet, sudoku2_complet = fct.suppression_solution(difficulte)
sudoku3_incomplet, sudoku3_complet = fct.suppression_solution(difficulte)
sudoku4_incomplet, sudoku4_complet = fct.suppression_solution(difficulte)
sudoku_liste_choix.append(sudoku1_incomplet)
sudoku_liste_choix.append(sudoku2_incomplet)
sudoku_liste_choix.append(sudoku3_incomplet)
sudoku_liste_choix.append(sudoku4_incomplet)

index=0
liste_button = []
for a in range(2):
    liste_button.append([])
    for b in range(2):
        liste_button[a].append([])
        frame_grille_bouton = tk.Frame(frame_modeles, bg=bg_color)
        frame_grille_bouton.grid(row=a, column=b, padx=6, pady=4)
        frame_grille = tk.Frame(frame_grille_bouton)
        frame_grille.pack()
        for i in range(3):
            liste_button[a][b].append([])
            for j in range(3):
                liste_button[a][b][i].append([])
                case = tk.Frame(frame_grille, bg = "black", padx=1, pady=1)
                case.grid(row=i, column=j) # Positionnement des cases
                for k in range(3):
                    liste_button[a][b][i][j].append([])
                    for l in range(3):
                        label = tk.Label(case, width=2, height=1, bg = "#FFECA1", padx=1, pady=1, font = ("Arial", 14), text=str(sudoku_liste_choix[index][i][j][k][l]) if sudoku_liste_choix[index][i][j][k][l] != 0 else "", borderwidth=1, relief="solid")
                        # button.config(command= lambda bonton = button: placer(bonton, valeur_chiffre))
                        label.grid(row=k, column=l) # Positionnement des boutons
                        liste_button[a][b][i][j][k].append(label)
        button_choisir_modele = tk.Button(frame_grille_bouton, text="Choisir ce modèle")
        button_choisir_modele.pack()
        index+=1

#FRAME PARTIE JOUABLE

frame_partie_jouable = tk.Frame(root)









root.mainloop()


# frame_grille_bouton = tk.Frame(frame_modeles, bg=bg_color)
# frame_grille_bouton.pack()
# caneva = tk.Canvas(frame_grille_bouton, width=506, height=506, bg="#FFECA1")
# caneva.pack()
# fct.construire_modeles(caneva, 506)