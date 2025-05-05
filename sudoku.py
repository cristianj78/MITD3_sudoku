import tkinter as tk
# import fonctions_gene as fct
import time
import copy
import json 
import os
import random as rd

sudoku = [
    [
        [
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
        ],
        [
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
        ],
        [
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
        ],
    ],
    [
        [
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
        ],
        [
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
        ],
        [
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
        ],
    ],
    [
        [
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
        ],
        [
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
        ],
        [
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ],
            [
                0,
                0,
                0
            ]
        ]
    ]
]

bg_color = "#E2EAF4"
retour = 0
num_possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
num_possible_ephemere = {}

num_fixe = []

def next_number(sudoku_next,a,b,c,d):
    """Change la valeur de la case parmi les nombres possible, retourne false si aucune sol n'est trouvé, sinon true"""
    global retour
    cle = (a, b, c, d)
    if not retour:
        liste_possible_ephemere = num_possible.copy()
        num_possible_ephemere[cle] = num_possible.copy()
        if sudoku[a][b][c][d] in liste_possible_ephemere:
            liste_possible_ephemere.remove(sudoku[a][b][c][d])
        
        
    else:
        if num_possible_ephemere[cle] != "":
            if sudoku_next[a][b][c][d] in num_possible_ephemere[cle]:
                num_possible_ephemere[cle].remove(sudoku_next[a][b][c][d])
            liste_possible_ephemere = num_possible_ephemere[cle]


    for j in range(3):
        for l in range(3):
            if sudoku_next[a][j][c][l] in liste_possible_ephemere:
                liste_possible_ephemere.remove(sudoku_next[a][j][c][l])

    for i in range(3):
        for k in range(3):
            if sudoku_next[i][b][k][d] in liste_possible_ephemere:
                liste_possible_ephemere.remove(sudoku_next[i][b][k][d])

    for k in range(3):
        for l in range(3):
            if sudoku_next[a][b][k][l] in liste_possible_ephemere:
                liste_possible_ephemere.remove(sudoku_next[a][b][k][l])


    num_possible_ephemere[cle] = liste_possible_ephemere
    if liste_possible_ephemere != []:
        num_random = rd.choice(liste_possible_ephemere)
        sudoku_next[a][b][c][d] = num_random
        retour = False
        return True
    else:
        retour = True
        sudoku_next[a][b][c][d] = 0
        return False
        



def generateur():
    """Genere la grille résolu"""
    global num_possible_ephemere, sudoku_incomplet
    i = 0
    j = 0
    k = 0
    l = 0
    num_possible_ephemere = {}
    sudoku_complet = copy.deepcopy(sudoku)
    while i < 3:
        while j < 3:
            while k < 3:
                while l < 3:
                    next = next_number(sudoku_complet,i,j,k,l)
                    if next == False:
                        if l > 0:
                            l = l-1

                        elif l == 0 and k > 0:
                            l = 2
                            k = k-1

                        elif l == 0 and k == 0 and j > 0:
                            l = 2
                            k = 2
                            j = j-1

                        elif l == 0 and k == 0 and j == 0 and i > 0:
                            l = 2
                            k = 2
                            j = 2
                            i = i-1
                    else:
                        if l < 2:
                            l = l+1

                        elif l == 2 and k < 2:
                            l = 0
                            k = k+1
                            
                        elif l == 2 and k == 2 and j < 2:
                            l = 0
                            k = 0
                            j = j+1
                            
                        elif l == 2 and k == 2 and j == 2 and i < 2:
                            l = 0
                            k = 0
                            j = 0
                            i = i+1
                        else:
                            l = 3
                            k = 3
                            j = 3
                            i = 3
    sudoku_incomplet = copy.deepcopy(sudoku_complet)
    return sudoku_complet
                    

sudoku_incomplet = []

def suppression_solution(difficulte):
    """Supprime un a un chauqe nombre pour arriver a un sudoku resolvable"""
    z = 0
    e = 0
    r = 0
    t = 0

    sudoku_complet = generateur()

    if difficulte == "Facile":
        case_supprimer = 0 + 1
    elif difficulte == "Normal":
        case_supprimer = 42+1
    elif difficulte == "Difficile":
        case_supprimer = 50+1
    else:
        case_supprimer = 55+1
    
    for _ in range(case_supprimer):
        test_solve = False
        while test_solve == False:
            z,e,r,t = rd.randint(0,2), rd.randint(0,2), rd.randint(0,2), rd.randint(0,2)

            while sudoku_incomplet[z][e][r][t] == 0:
                z,e,r,t = rd.randint(0,2), rd.randint(0,2), rd.randint(0,2), rd.randint(0,2)
            temp = sudoku_incomplet[z][e][r][t]
            sudoku_incomplet[z][e][r][t] = 0
                        
            
            num_fixe.append((z,e,r,t))
            sudoku_incomplet2 = copy.deepcopy(sudoku_incomplet)
            test_solve = solveur(sudoku_incomplet2, sudoku_complet)
            
            
            if test_solve == False:
                num_fixe.remove((z,e,r,t))
                sudoku_incomplet[z][e][r][t] = temp
        test_solve = False
    return sudoku_incomplet, sudoku_complet

def solveur(sudoku_incomplet, sudoku_complet):
    """Resous le sudoku pour tester l unicite de la solution"""
    next = True
    global num_possible_ephemere, retour
    i = 0
    j = 0
    k = 0
    l = 0
    num_possible_ephemere = {}

    while i < 3:
        while j < 3:
            while k < 3:
                while l < 3 and num_fixe != []:
                    if (i,j,k,l) in num_fixe:
                        next = next_number(sudoku_incomplet,i,j,k,l)
                    if next == False:
                        
                        if l > 0:
                            l = l-1

                        elif l == 0 and k > 0:
                            l = 2
                            k = k-1

                        elif l == 0 and k == 0 and j > 0:
                            l = 2
                            k = 2
                            j = j-1

                        elif l == 0 and k == 0 and j == 0 and i > 0:
                            l = 2
                            k = 2
                            j = 2
                            i = i-1
                        
                        elif l == 0 and k == 0 and j == 0 and i == 0:
                            retour = False
                            return True

                        while (i,j,k,l) in num_fixe:
                            if l > 0:
                                l = l-1

                            elif l == 0 and k > 0:
                                l = 2
                                k = k-1

                            elif l == 0 and k == 0 and j > 0:
                                l = 2
                                k = 2
                                j = j-1

                            elif l == 0 and k == 0 and j == 0 and i > 0:
                                l = 2
                                k = 2
                                j = 2
                                i = i-1
                            
                            elif l == 0 and k == 0 and j == 0 and i == 0:
                                retour = False
                                return True
                    else:
                        if l < 2:
                            l = l+1

                        elif l == 2 and k < 2:
                            l = 0
                            k = k+1
                                
                        elif l == 2 and k == 2 and j < 2:
                            l = 0
                            k = 0
                            j = j+1
                                
                        elif l == 2 and k == 2 and j == 2 and i < 2:
                            l = 0
                            k = 0
                            j = 0
                            i = i+1
                        else:
                            l = 3
                            k = 3
                            j = 3
                            i = 3
    if sudoku_incomplet == sudoku_complet:
        return True
    else:
        return False




def sudoku_affichage(sudoku):
    """Affiche le sudoku"""
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    print(sudoku[i][k][j][l], end=" ")
                print(end="  ")
            print("")
        print("")
    print(".........")



def deplacer(label, descend, root):
    try:
        pos = label.place_info()
    except tk.TclError:
        return  # Le label n'existe plus, on arrête l'animation

    place_x = int(pos['x'])
    place_y = int(pos['y'])

    place_y += 1 if descend else -1

    if place_y == 61:
        descend = False
    elif not descend and place_y == 0:
        descend = True

    label.place(x=place_x, y=place_y)
    root.after(70, lambda: deplacer(label, descend, root))

difficulte = "Normal"
temps = 0

def recreer_menu(root):
    global menu
    menu_creer = tk.Menu(root)
    menu = menu_creer
    Accueil = menu.add_command(label="Accueil", command=lambda: (effacer_widget_sans_forget(root), recreer_menu(root), creation_menu()))
    menu.add_separator()
    Nouvelle_partie = menu.add_command(label="Nouvelle Partie", command=lambda: (effacer_widget_sans_forget(root), recreer_menu(root), nouvelle_partie()))
    menu.add_separator()
    Sauvegarder = menu.add_command(label="Sauvegarder", command=lambda: ajouter_sauvegarde(sudoku_a_completer))
    menu.add_separator()
    Quitter = menu.add_command(label="Quitter", command=root.destroy)

def effacer_widget(widget):
    for child in widget.winfo_children():
        child.destroy()
    widget.pack_forget()  # ← Important si tu veux cacher complètement la frame elle-même

def effacer_widget_sans_forget(widget):
    for child in widget.winfo_children():
        child.destroy()


def generation_liste_sudoku():
    global difficulte
    sudoku_liste_choix = []
    sudoku_liste_corrigees = []
    sudoku1_incomplet, sudoku1_complet = suppression_solution(difficulte)
    sudoku2_incomplet, sudoku2_complet = suppression_solution(difficulte)
    sudoku3_incomplet, sudoku3_complet = suppression_solution(difficulte)
    sudoku4_incomplet, sudoku4_complet = suppression_solution(difficulte)
    sudoku_liste_choix.append(sudoku1_incomplet)
    sudoku_liste_choix.append(sudoku2_incomplet)
    sudoku_liste_choix.append(sudoku3_incomplet)
    sudoku_liste_choix.append(sudoku4_incomplet)
    sudoku_liste_corrigees.append(sudoku1_complet)
    sudoku_liste_corrigees.append(sudoku2_complet)
    sudoku_liste_corrigees.append(sudoku3_complet)
    sudoku_liste_corrigees.append(sudoku4_complet)
    return sudoku_liste_choix, sudoku_liste_corrigees

def dessiner_lignes(canva, hauteur):
    """On divise la longueur ou la hauteur (c'est un carré) par 9 (9 cases)"""  
    x = hauteur//9
    y = hauteur//3
# Création de la grille principale
    for i in range(10):  
        canva.create_line(0, i * x, hauteur, i * x, fill="black", width=2, tags="ligne") 
    for j in range(10):  
        canva.create_line(j * x, 0, j * x, hauteur, fill="black", width=2, tags="ligne") #Important !, "tags=ligne" va permettre de rassembler les priorités d'affichage de chaque ligne dans une boite 
                                                                     #et à chaque fois qu'on créera un rectangle, on remontera cette priorité, les lignes s'afficheront donc à chaque fois en priorité
# On dessine les bordure épaisses 
    for i in range(4):
        canva.create_line(0, i * y-3, hauteur, i * y-3, fill="black", width=5, tags="ligne")
    for j in range(4):    #Ne surtout pas toucher, les "-3" sont des ajustements
        canva.create_line(j * y-3, 0, j * y-3, hauteur, fill="black", width=5, tags="ligne")

def dessiner_numeros(position, hauteur, police, index, sudoku_liste_choix):
    cell_size = hauteur // 9
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    val = sudoku_liste_choix[index][i][j][k][l]
                    if val != 0:
                        # Calcul de la position réelle sur la grille
                        row = i * 3 + k
                        col = j * 3 + l
                        x = col * cell_size + cell_size // 2
                        y = row * cell_size + cell_size // 2
                        position.create_text(x, y, text=str(val), fill="black", font=("Arial", police))



def dessiner_modeles(frame_modeles, frame_nouvelle_partie, sauvegarde=False):
    global difficulte
    # global root, menu, frame_nouvelle_partie, frame_partie_jouable, frame_partie_jouable, label_time, frame_grille_jouable
    index = 0
    nombre_de_modeles = 4
    effacer_widget(frame_modeles)
    frame_modeles.pack()
    if not sauvegarde:
        sudoku_liste_choix, sudoku_liste_corrigees = generation_liste_sudoku()
    else:
        with open("sauvegardes.json", "r") as fichier:
            try:
                donnees = json.load(fichier)
                nombre_de_modeles = len(donnees) //2
                sudoku_liste_choix = [donnees["sauvegarde1"]["a_completer"]]
                sudoku_liste_corrigees = [donnees["sauvegarde1"]["a_corriger"]]
                global vie_restantes
                vie_restantes = donnees.get("nombre_de_vie1", 3)
            except (json.JSONDecodeError, KeyError):
                print("Erreur : Sauvegarde 1 introuvable ou fichier invalide")
                return  # Ou afficher un message d'erreur



    def zoom_modele(case_modele, event):
        case_modele.scale("all", 0, 0, 0.9, 0.9)
        case_modele.config(width=181, height=181)

    def reset_modele(case_modele, event):
        case_modele.scale("all", 0, 0, 1/0.9, 1/0.9)
        case_modele.config(width=206, height=206)
    for i in range(nombre_de_modeles):
        boite = tk.Frame(frame_modeles, bg=bg_color)
        boite.grid(row=i//2, column=i%2, padx=25, pady=25)
        canvas_zoom = tk.Canvas(boite, width=206, height=206, bg=bg_color, highlightbackground=bg_color)
        canvas_zoom.grid(row=0)
        cases_modele = tk.Canvas(boite, width=206, height=206, bg="#FFECA1", highlightbackground="black")
        cases_modele.grid(row=0)
        dessiner_lignes(cases_modele,211)
        dessiner_numeros(cases_modele, 211, 14, i, sudoku_liste_choix)
        cases_modele.bind("<Button-1>", lambda event, ind=index: (effacer_widget(frame_nouvelle_partie), partie_jouable(ind, sudoku_liste_choix, sudoku_liste_corrigees)))
        cases_modele.bind("<Enter>", lambda event, case_modele = cases_modele: zoom_modele(case_modele, event))
        canvas_zoom.bind("<Leave>", lambda event, case_modele = cases_modele: reset_modele(case_modele, event))
        canvas_zoom.bind("<Enter>", lambda event, case_modele = cases_modele: zoom_modele(case_modele, event))
        cases_modele.bind("<Leave>", lambda event, case_modele = cases_modele: reset_modele(case_modele, event))
        index +=1

frame_partie_finie = None

def creation_menu():
    global frame_partie_finie
    if frame_partie_finie:
        effacer_widget(frame_partie_finie)
    # FRAME MENU
    root.geometry("600x600")
    root.config(menu=None)
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

    deplacer(label1,descend = True, root=root)
    deplacer(label2,descend = True, root=root)
    deplacer(label3,descend = True, root=root)
    deplacer(label4,descend = True, root=root)
    deplacer(label5,descend=False, root=root)
    deplacer(label6,descend=False, root=root)

        #BOUTONS
    frame_buttons = tk.Frame(frame_menu, bg=bg_color)
    frame_buttons.pack(fill="both")

    button_reprendre = tk.Button(frame_buttons, text="Reprendre la partie", font=("Arial", 27))
    button_reprendre.pack(pady=10)

    button_nvl_partie = tk.Button(frame_buttons, text="Nouvelle partie", font=("Arial", 27), command=lambda: (effacer_widget(frame_menu), nouvelle_partie()))
    button_nvl_partie.pack(pady=10)

    button_reprendre_sauvegarde = tk.Button(frame_buttons, text="Autres sauvegardes", font=("Arial", 27), command=lambda: (effacer_widget(frame_menu), autres_sauvegardes()))
    button_reprendre_sauvegarde.pack(pady=10)

frame_modeles = None

def nouvelle_partie():
    global frame_modeles, frame_partie_finie, difficulte
    difficulte = "Normal"
    if frame_partie_finie:
        effacer_widget(frame_partie_finie)
    # FRAME NOUVELLE PARTIE
    root.geometry("600x600")
    root.config(menu=menu)
    frame_nouvelle_partie = tk.Frame(root)
    frame_nouvelle_partie.pack()
    

        #CHOIX DIFFICULTE

    frame_difficulte = tk.Frame(frame_nouvelle_partie, bg=bg_color)

    label_difficulte = tk.Label(frame_difficulte, text="Choisis la difficulté", bg=bg_color, font=("Arial", 13))

    button_facile = tk.Button(frame_difficulte, text="Facile", font=("Arial", 13), command=lambda: changement_difficulte("Facile", button_facile))
    button_normal = tk.Button(frame_difficulte, text="Normal", font=("Arial", 13), state="disabled", command=lambda: changement_difficulte("Normal", button_normal))
    button_difficile = tk.Button(frame_difficulte, text="Difficile", font=("Arial", 13), command=lambda: changement_difficulte("Difficile", button_difficile))
    button_extreme = tk.Button(frame_difficulte, text="Extreme", font=("Arial", 13), command=lambda: changement_difficulte("Extreme", button_extreme))
    frame_modeles = tk.Frame(frame_nouvelle_partie, bg=bg_color, pady= 10)

        # bf,bn,bd,be = None,None,None,None
    def changement_difficulte(difficulte_a_changer, button_non_affecte):
        global difficulte
        # global bf,bn,bd,be
        # bf,bn,bd,be = button_facile, button_normal, button_difficile, button_extreme
        difficulte = difficulte_a_changer
        button_facile.config(state="active")
        button_normal.config(state="active")
        button_difficile.config(state="active")
        button_extreme.config(state="active")
        button_non_affecte.config(state="disabled")


        dessiner_modeles(frame_modeles, frame_nouvelle_partie)


    frame_difficulte.pack(fill="x")
    label_difficulte.grid(column=0, row=0)
    button_facile.grid(column=1, row=0, padx=3)
    button_normal.grid(column=2, row=0, padx=3)
    button_difficile.grid(column=3, row=0, padx=3)
    button_extreme.grid(column=4, row=0, padx=3)
    frame_modeles.pack(fill="both")

    dessiner_modeles(frame_modeles, frame_nouvelle_partie)

selectionne = None
ancien_selectionne = None
valeur = 0
coordonnee = []
correction = 0

sudoku_choisi = []
sudoku_choisi_corrige = []
ind = 0
nombre_choisi = None

liste_button_jouable = []
liste_boutons_restants = []
sudoku_a_completer = []

vie_restantes = 0
label_vie_restantes = None
label_time = None

def selectionnement(label,case,coord,case_corrige):
    global selectionne, valeur, ancien_selectionne, coordonnee, correction #On ne peut pas utiliser global, car les variable ne sont pas vraiment global
    valeur = case
    selectionne = label
    coordonnee = coord
    correction = case_corrige
    if selectionne:
        selectionne.config(bg="#ffcff6")
    if ancien_selectionne and ancien_selectionne != selectionne:
        ancien_selectionne.config(bg="#FFECA1")
    ancien_selectionne = selectionne



def changement_nombre(event):
    global selectionne,valeur, nombre_choisi, correction, label_vie_restantes, vie_restantes, liste_boutons_restants, ancien_selectionne, coordonnee, sudoku_a_completer
    chr_possible = ["1","2","3","4","5","6","7","8","9"]
    if event.keysym in ["Up", "Down", "Left", "Right"] and selectionne:
        selectionnment_fleche(event.keysym)
    elif event.char in chr_possible:
        nombre_choisi = None
        sudoku_a_completer["a_completer"][coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]] = int(event.char)
        if selectionne and valeur == 0 and int(event.char) == correction:
            selectionne.config(text=str(event.char), fg="#7FB3FF")
            liste_boutons_restants.remove(selectionne)
            if liste_boutons_restants == []:
                ancien_selectionne = None
                fin_partie(True)
        elif selectionne and valeur == 0 and int(event.char) != correction:
            selectionne.config(text=str(event.char), fg="#ff4b00")
            vie_restantes -=1
            label_vie_restantes.config(text="Vies restantes: " + "l "*vie_restantes)
            if vie_restantes == 0:
                label_vie_restantes.config(text="Vies restantes: 0")
                ancien_selectionne = None
                fin_partie(False)

    elif event.char == "0":
        nombre_choisi = None
        sudoku_a_completer["a_completer"][coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]] = 0
        if selectionne and valeur == 0:
            selectionne.config(text="", fg="#7FB3FF")

def boutton_changement_nombre(val, effacement=None):
    global nombre_choisi, selectionne, valeur, correction, label_vie_restantes, vie_restantes, liste_boutons_restants, ancien_selectionne, sudoku_a_completer
    nombre_choisi = val
    if not effacement:
        sudoku_a_completer["a_completer"][coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]] = nombre_choisi
        if selectionne and valeur == 0 and nombre_choisi == correction:
            selectionne.config(text=str(nombre_choisi), fg="#7FB3FF")
            liste_boutons_restants.remove(selectionne)
            if liste_boutons_restants == []:
                ancien_selectionne = None
                fin_partie(True)
        elif selectionne and valeur == 0 and nombre_choisi != correction:
            selectionne.config(text=str(nombre_choisi), fg="#ff4b00")
            vie_restantes -=1
            label_vie_restantes.config(text="Vies restantes: " + "l "*vie_restantes)
            if vie_restantes == 0:
                label_vie_restantes.config(text="Vies restantes: 0")
                ancien_selectionne = None
                fin_partie(False)

    elif selectionne and valeur == 0:
            sudoku_a_completer["a_completer"][coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]] = 0
            selectionne.config(text=str(nombre_choisi), fg="#7FB3FF")

    
def selectionnment_fleche(key):
    global selectionne, coordonnee, ind, liste_button_jouable, sudoku_choisi, sudoku_choisi_corrige
    if key == "Up":
        if coordonnee[2] > 0:
            new_coord = [coordonnee[0],coordonnee[1],coordonnee[2]-1,coordonnee[3]]
            selectionnement(liste_button_jouable[coordonnee[0]][coordonnee[1]][coordonnee[2]-1][coordonnee[3]], sudoku_choisi[ind][coordonnee[0]][coordonnee[1]][coordonnee[2]-1][coordonnee[3]],new_coord, sudoku_choisi_corrige[ind][coordonnee[0]][coordonnee[1]][coordonnee[2]-1][coordonnee[3]])
        elif coordonnee[0] > 0:
            new_coord = [coordonnee[0]-1,coordonnee[1],2,coordonnee[3]]
            selectionnement(liste_button_jouable[coordonnee[0]-1][coordonnee[1]][2][coordonnee[3]], sudoku_choisi[ind][coordonnee[0]-1][coordonnee[1]][2][coordonnee[3]],new_coord, sudoku_choisi_corrige[ind][coordonnee[0]-1][coordonnee[1]][2][coordonnee[3]])
    elif key == "Down":
        if coordonnee[2] < 2:
            new_coord = [coordonnee[0],coordonnee[1],coordonnee[2]+1,coordonnee[3]]
            selectionnement(liste_button_jouable[coordonnee[0]][coordonnee[1]][coordonnee[2]+1][coordonnee[3]], sudoku_choisi[ind][coordonnee[0]][coordonnee[1]][coordonnee[2]+1][coordonnee[3]],new_coord, sudoku_choisi_corrige[ind][coordonnee[0]][coordonnee[1]][coordonnee[2]+1][coordonnee[3]])
        elif coordonnee[0] < 2:
            new_coord = [coordonnee[0]+1,coordonnee[1],0,coordonnee[3]]
            selectionnement(liste_button_jouable[coordonnee[0]+1][coordonnee[1]][0][coordonnee[3]], sudoku_choisi[ind][coordonnee[0]+1][coordonnee[1]][0][coordonnee[3]],new_coord, sudoku_choisi_corrige[ind][coordonnee[0]+1][coordonnee[1]][0][coordonnee[3]])
    elif key == "Left":
        if coordonnee[3] > 0:
            new_coord = [coordonnee[0],coordonnee[1],coordonnee[2],coordonnee[3]-1]
            selectionnement(liste_button_jouable[coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]-1], sudoku_choisi[ind][coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]-1],new_coord, sudoku_choisi_corrige[ind][coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]-1])
        elif coordonnee[1] > 0:
            new_coord = [coordonnee[0],coordonnee[1]-1,coordonnee[2],2]
            selectionnement(liste_button_jouable[coordonnee[0]][coordonnee[1]-1][coordonnee[2]][2], sudoku_choisi[ind][coordonnee[0]][coordonnee[1]-1][coordonnee[2]][2],new_coord, sudoku_choisi_corrige[ind][coordonnee[0]][coordonnee[1]-1][coordonnee[2]][2])
    elif key == "Right":
        if coordonnee[3] < 2:
            new_coord = [coordonnee[0],coordonnee[1],coordonnee[2],coordonnee[3]+1]
            selectionnement(liste_button_jouable[coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]+1], sudoku_choisi[ind][coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]+1],new_coord, sudoku_choisi_corrige[ind][coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]+1])
        elif coordonnee[1] < 2:
            new_coord = [coordonnee[0],coordonnee[1]+1,coordonnee[2],0]
            selectionnement(liste_button_jouable[coordonnee[0]][coordonnee[1]+1][coordonnee[2]][0], sudoku_choisi[ind][coordonnee[0]][coordonnee[1]+1][coordonnee[2]][0],new_coord, sudoku_choisi_corrige[ind][coordonnee[0]][coordonnee[1]+1][coordonnee[2]][0])


frame_partie_jouable = None


def ajouter_sauvegarde(sudoku_a_completer):
    global vie_restantes
    # sudoku_a_completer["Nombre de vie"] = nb_vies #car nb_vies est modifié globalement, on la sauvegarde donc uniquement lorsqu'on appuie sur sauvegarder
    fichier_sauvegarde = "sauvegardestt.json"
    if not os.path.exists(fichier_sauvegarde):
        with open(fichier_sauvegarde, "w") as f:
            json.dump({}, f)  # Initialise un fichier vide

    with open(fichier_sauvegarde, "r") as fichier:
        try:
            ajout = json.load(fichier)
        except json.JSONDecodeError: #Si fichier vide
            ajout = {}
        if len(ajout) >= 4: #Nombre sauvegarde maximale
            print("trop de sauvegardes")
        else:
            longueur = len(ajout)+1
            ajout[f"sauvegarde{longueur}"] = sudoku_a_completer
            ajout[f"sauvegarde{longueur}"]["a_completer"] = sudoku_a_completer["a_completer"] # On crée la nouvelle sauvegarde s'il reste de la place
            ajout[f"sauvegarde{longueur}"]["a_corriger"] = sudoku_a_completer["a_corriger"] # On crée la nouvelle sauvegarde s'il reste de la place
            ajout[f"nombre_de_vie{longueur}"] = vie_restantes
            with open("sauvegardes.json", "w") as fich:
                json.dump(ajout, fich) 



def partie_jouable(index, sudoku_liste_choix, sudoku_liste_corrigees):
    global temps, sudoku_choisi, sudoku_choisi_corrige, ind, vie_restantes, label_vie_restantes, label_time, frame_partie_jouable, sudoku_a_completer
    sudoku_choisi = sudoku_liste_choix
    sudoku_choisi_corrige = sudoku_liste_corrigees
    ind = index

    root.geometry("1000x600")
    #FRAME PARTIE JOUABLE
    frame_partie_jouable = tk.Frame(root, bg=bg_color)
    frame_partie_jouable.pack()


        #FRAME LABEL

    frame_haut_label = tk.Frame(frame_partie_jouable, bg=bg_color)
    frame_haut_label.pack(pady=10, fill="x")


    label_indication_difficulte = tk.Label(frame_haut_label, text=f"Difficulté: {difficulte}", font=("Arial", 13), bg=bg_color)
    label_indication_difficulte.pack(side="left")

    label_vie_restantes = tk.Label(frame_haut_label, bg=bg_color, text="Vies restantes: l l l", font=("Arial", 20))
    label_vie_restantes.pack()

    label_time = tk.Label(frame_haut_label, text="Test", font=("Arial", 13), bg=bg_color)
    label_time.pack(side="right")

    temps = time.time()
    def creation_temps(label_time):
        global temps
        delta = int(time.time() - temps)
        minutes = delta // 60
        seconds = delta % 60
        label_time.config(text=f"{minutes:02d}:{seconds:02d}")
        label_time.after(1000, lambda: creation_temps(label_time))
    creation_temps(label_time)
        #FRAME SUDOKU


    vie_restantes = 3

    def generation_sudoku():
        global liste_button_jouable, liste_boutons_restants, sudoku_a_completer
        sudoku_a_completer["a_completer"] = copy.deepcopy(sudoku_liste_choix[index])
        sudoku_a_completer["a_corriger"] = copy.deepcopy(sudoku_liste_corrigees[index])
        liste_button_jouable = []
        for i in range(3):
            liste_button_jouable.append([])
            for j in range(3):
                liste_button_jouable[i].append([])
                case = tk.Frame(frame_grille_jouable, bg = "black", padx=1, pady=1)
                case.grid(row=i, column=j)
                for k in range(3):
                    liste_button_jouable[i][j].append([])
                    for l in range(3):
                        label = tk.Label(case, width=2, height=1, bg = "#FFECA1", font = ("Arial", 20, "bold"), text=str(sudoku_liste_choix[index][i][j][k][l]) if sudoku_liste_choix[index][i][j][k][l] != 0 else "", borderwidth=1, relief="solid")
                        label.bind("<Button-1>", lambda event, lab=label, case=sudoku_liste_choix[index][i][j][k][l], coordonnees=[i,j,k,l], case_corrige=sudoku_liste_corrigees[index][i][j][k][l]  : selectionnement(lab,case,coordonnees,case_corrige))

                        label.grid(row=k, column=l, ipadx=8, ipady=8)
                        liste_button_jouable[i][j][k].append(label)
        liste_boutons_restants = []

        
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        label = liste_button_jouable[i][j][k][l]
                        if label['text'] == "":  # uniquement les cases modifiables ?
                            liste_boutons_restants.append(label)


    frame_sudoku_jouable = tk.Frame(frame_partie_jouable, bg=bg_color)
    frame_sudoku_jouable.pack(pady=10, fill="x")

    liste_button_jouable = []

    frame_grille_jouable = tk.Frame(frame_sudoku_jouable, bg=bg_color)
    frame_grille_jouable.pack(side="left", padx=15)

    generation_sudoku()
    

    root.bind("<Key>", lambda event: changement_nombre(event))

    frame_button_placement = tk.Frame(frame_sudoku_jouable, bg="#c2d7f1")
    frame_button_placement.pack(ipadx=3, ipady=3, padx=3)

    frame_2_button = tk.Frame(frame_button_placement, bg=bg_color)
    frame_2_button.grid(column=0, row=0, columnspan=3, pady=5)

    button_revenir_arriere = tk.Button(frame_2_button, text="R", font=("Arial", 20))
    button_revenir_arriere.pack(side="left", padx=1, ipadx=20, ipady=20)
    button_effacer = tk.Button(frame_2_button, text="X", font=("Arial", 20), command= lambda: boutton_changement_nombre("", True))
    button_effacer.pack(side="right", ipadx=20, ipady=20)

    nombre = 0
    for i in range(3):
        for k in range(3):
            nombre +=1
            button_choix = tk.Button(frame_button_placement, text= str(nombre), font=("Arial", 20), fg="white", bg="#474747", command= lambda nbr=nombre: boutton_changement_nombre(nbr))
            button_choix.grid(column=k, row=1+i, padx=2, pady=2, ipadx=20, ipady=20)

def fin_partie(gagne):
    global frame_partie_jouable, root, label_time, vie_restantes, frame_partie_finie, frame_modeles
    temps_final = label_time.cget("text")

    effacer_widget(frame_partie_jouable)

    # label_vie_restantes.config(text="Vies restantes: l l l")
    frame_partie_finie = tk.Frame(root, bg=bg_color)
    frame_partie_finie.pack()
    
    if gagne:
        label_gagne = tk.Label(frame_partie_finie, text="Gagné!", font = ("Arial", 47), fg="grey", bg=bg_color)
        label_gagne.pack(pady=20)
    else:
        label_perdu = tk.Label(frame_partie_finie, text="Perdu!", font = ("Arial", 47), fg="grey", bg=bg_color)
        label_perdu.pack(pady=20)
    label_temps_final = tk.Label(frame_partie_finie, text="Temps: " + temps_final, font = ("Arial", 22), bg=bg_color)
    label_temps_final.pack()
    label_vie_final = tk.Label(frame_partie_finie, text="Vies restantes: " + "l "*vie_restantes, font = ("Arial", 22), bg=bg_color)
    label_vie_final.pack()
    if vie_restantes == 0:
        label_vie_final.config(text="Vies restantes: 0")
    vie_restantes = 3

    #Nouvelle partie
    button_refaire_une_partie = tk.Button(frame_partie_finie, text="Nouvelle partie", font=("Arial", 27), command=lambda: nouvelle_partie())
    button_refaire_une_partie.pack(pady=10)

    #Retour accueil
    button_retour_accueil = tk.Button(frame_partie_finie, text="Retourner à l'accueil", font=("Arial", 27), command=lambda: creation_menu())
    button_retour_accueil.pack(pady=10)

def autres_sauvegardes():
    global frame_modeles, frame_partie_finie, difficulte
    difficulte = "Normal"
    if frame_partie_finie:
        effacer_widget(frame_partie_finie)
    # FRAME NOUVELLE PARTIE
    root.geometry("600x600")
    root.config(menu=menu)
    frame_nouvelle_partie = tk.Frame(root)
    frame_nouvelle_partie.pack()

    frame_modeles = tk.Frame(frame_nouvelle_partie, bg=bg_color, pady= 10)
    frame_modeles.pack(fill="both")

    dessiner_modeles(frame_modeles, frame_nouvelle_partie, sauvegarde=True)

selectionne = None
ancien_selectionne = None
valeur = 0
coordonnee = []
correction = 0

sudoku_choisi = []
sudoku_choisi_corrige = []
ind = 0
nombre_choisi = None

liste_button_jouable = []
liste_boutons_restants = []
sudoku_a_completer = {}

vie_restantes = 0
label_vie_restantes = None
label_time = None

def selectionnement(label,case,coord,case_corrige):
    global selectionne, valeur, ancien_selectionne, coordonnee, correction #On ne peut pas utiliser global, car les variable ne sont pas vraiment global
    valeur = case
    selectionne = label
    coordonnee = coord
    correction = case_corrige
    if selectionne:
        selectionne.config(bg="#ffcff6")
    if ancien_selectionne and ancien_selectionne != selectionne:
        try:
            ancien_selectionne.config(bg="#FFECA1")
        except tk.TclError:
            pass  # Le widget a été détruit
    ancien_selectionne = selectionne




bg_color = "#E2EAF4"

root = tk.Tk()
root.title("Sudoku")
root.geometry("600x600")
root.config(bg=bg_color)

menu = tk.Menu(root)
Accueil = menu.add_command(label="Accueil", command=lambda: (effacer_widget_sans_forget(root), recreer_menu(root), creation_menu()))
menu.add_separator()
Nouvelle_partie = menu.add_command(label="Nouvelle Partie", command=lambda: (effacer_widget_sans_forget(root), recreer_menu(root), nouvelle_partie()))
menu.add_separator()
Sauvegarder = menu.add_command(label="Sauvegarder", command=lambda: ajouter_sauvegarde(sudoku_a_completer))
menu.add_separator()
Quitter = menu.add_command(label="Quitter", command=root.destroy)

creation_menu()

root.mainloop()
# , state="disabled"