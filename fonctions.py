import tkinter as tk
import random as rd
import time
import copy

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
        case_supprimer = 36 + 1
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


#Début, lancement des fonction de generation

#######################################""
def deplacer(label, descend, root):
    pos = label.place_info()
    
    place_x = int(pos['x'])
    place_y = int(pos['y'])
    if descend:
        place_y += 1

    else:
        place_y -= 1

    if place_y == 61:
        descend = False
    elif not descend and place_y == 0:
        descend = True
    place_y 
    label.place(x=place_x, y=place_y)
    root.after(70, lambda: deplacer(label,descend,root))

def changement_frame(root, menu, frame_menu, frame_nouvelle_partie, frame_partie_jouable, frame_a_afficher, label_time):
    global temps
    frame_menu.pack_forget()
    frame_nouvelle_partie.pack_forget()
    frame_partie_jouable.pack_forget()
    frame_a_afficher.pack(pady=5)
    temps = time.time()
    creation_temps(label_time)
    if frame_a_afficher != frame_menu:
        root.config(menu=menu)
    else:
        root.config(menu=None)

    if frame_a_afficher == frame_partie_jouable:
        root.geometry("1000x600")

def changement_difficulte(difficulte, liste_button, button_non_affecte, button_facile, button_normal, button_difficile, button_extreme):
    button_facile.config(state="active")
    button_normal.config(state="active")
    button_difficile.config(state="active")
    button_extreme.config(state="active")
    button_non_affecte.config(state="disabled")


    sudoku_liste_choix = []
    sudoku1_incomplet, sudoku1_complet = suppression_solution(difficulte)
    sudoku2_incomplet, sudoku2_complet = suppression_solution(difficulte)
    sudoku3_incomplet, sudoku3_complet = suppression_solution(difficulte)
    sudoku4_incomplet, sudoku4_complet = suppression_solution(difficulte)
    sudoku_liste_choix.append(sudoku1_incomplet)
    sudoku_liste_choix.append(sudoku2_incomplet)
    sudoku_liste_choix.append(sudoku3_incomplet)
    sudoku_liste_choix.append(sudoku4_incomplet)
    index = 0
    for a in range(len(liste_button)):
        for b in range(len(liste_button[a])):
            for i in range(len(liste_button[a][b])):
                for j in range(len(liste_button[a][b][i])):
                    for k in range(len(liste_button[a][b][i][j])):
                        for l in range(len(liste_button[a][b][i][j][k])):
                            liste_button[a][b][i][j][k][l].config(text=str(sudoku_liste_choix[index][i][j][k][l]) if sudoku_liste_choix[index][i][j][k][l] != 0 else "")
            index +=1
    return sudoku_liste_choix
        
temps = time.time()

def creation_temps(label_time):
    global temps
    delta = int(time.time() - temps)
    minutes = delta // 60
    seconds = delta % 60
    label_time.config(text=f"{minutes:02d}:{seconds:02d}")
    label_time.after(1000, lambda: creation_temps(label_time))

selectionne = None
ancien_selectionne = None
valeur = 0
nombre_choisi = None
coordonnee = []
def selectionnement(label,val,coord):
    global selectionne, valeur, ancien_selectionne, nombre_choisi, coordonnee
    valeur = val
    selectionne = label
    coordonnee = coord
    selectionne.config(bg="#ffcff6")
    if ancien_selectionne and ancien_selectionne != selectionne:
        ancien_selectionne.config(bg="#FFECA1")
    ancien_selectionne = selectionne
    # if nombre_choisi:
    #     selectionne.config(text=str(nombre_choisi), fg="#7FB3FF")

liste_button_jouable = []
sudoku_liste = []
ind = None
def generation_sudoku(index, frame_grille_jouable, sudoku_liste_choix):
    global ind, liste_button_jouable, sudoku_liste
    liste_button_jouable = []
    sudoku_liste = sudoku_liste_choix
    ind = index
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
                    label.bind("<Button-1>", lambda event, lab=label,val=sudoku_liste_choix[index][i][j][k][l], coord=[i,j,k,l] : (selectionnement(lab,val,coord), print('te')))

                    label.grid(row=k, column=l, ipadx=8, ipady=8)
                    liste_button_jouable[i][j][k].append(label)
                    

def changement_nombre(event):
    global selectionne,valeur, nombre_choisi
    chr_possible = ["1","2","3","4","5","6","7","8","9",""]
    if event.keysym in ["Up", "Down", "Left", "Right"] and selectionne:
        selectionnment_fleche(event.keysym)
        print("t")
    elif event.char in chr_possible:
        nombre_choisi = None
        if selectionne and valeur == 0:
            selectionne.config(text=str(event.char), fg="#7FB3FF")
        print("ru")
    elif event.char == "0":
        nombre_choisi = None
        if selectionne and valeur == 0:
            selectionne.config(text="", fg="#7FB3FF")
        print("re")
    print(event.keysym)
    

def boutton_changement_nombre(val):
    global nombre_choisi, selectionne, valeur
    nombre_choisi = val
    if selectionne and valeur == 0:
        selectionne.config(text=str(nombre_choisi), fg="#7FB3FF")

def selectionnment_fleche(key):
    global selectionne, coordonnee, ind, liste_button_jouable, sudoku_liste
    if key == "Up":
        if coordonnee[2] > 0:
            print("t")
            new_coord = [coordonnee[0],coordonnee[1],coordonnee[2]-1,coordonnee[3]]
            print(liste_button_jouable)
            selectionnement(liste_button_jouable[coordonnee[0]][coordonnee[1]][coordonnee[2]-1][coordonnee[3]], sudoku_liste[ind][coordonnee[0]][coordonnee[1]][coordonnee[2]-1][coordonnee[3]],new_coord)
        elif coordonnee[0] > 0:
            new_coord = [coordonnee[0]-1,coordonnee[1],2,coordonnee[3]]
            print(liste_button_jouable)
            selectionnement(liste_button_jouable[coordonnee[0]-1][coordonnee[1]][2][coordonnee[3]], sudoku_liste[ind][coordonnee[0]-1][coordonnee[1]][2][coordonnee[3]],new_coord)
    elif key == "Down":
        if coordonnee[2] < 2:
            print("t")
            new_coord = [coordonnee[0],coordonnee[1],coordonnee[2]+1,coordonnee[3]]
            print(liste_button_jouable)
            selectionnement(liste_button_jouable[coordonnee[0]][coordonnee[1]][coordonnee[2]+1][coordonnee[3]], sudoku_liste[ind][coordonnee[0]][coordonnee[1]][coordonnee[2]+1][coordonnee[3]],new_coord)
        elif coordonnee[0] < 2:
            new_coord = [coordonnee[0]+1,coordonnee[1],0,coordonnee[3]]
            print(liste_button_jouable)
            selectionnement(liste_button_jouable[coordonnee[0]+1][coordonnee[1]][0][coordonnee[3]], sudoku_liste[ind][coordonnee[0]+1][coordonnee[1]][0][coordonnee[3]],new_coord)
    elif key == "Left":
        if coordonnee[3] > 0:
            print("t")
            new_coord = [coordonnee[0],coordonnee[1],coordonnee[2],coordonnee[3]-1]
            print(liste_button_jouable)
            selectionnement(liste_button_jouable[coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]-1], sudoku_liste[ind][coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]-1],new_coord)
        elif coordonnee[1] > 0:
            new_coord = [coordonnee[0],coordonnee[1]-1,coordonnee[2],2]
            print(liste_button_jouable)
            selectionnement(liste_button_jouable[coordonnee[0]][coordonnee[1]-1][coordonnee[2]][2], sudoku_liste[ind][coordonnee[0]][coordonnee[1]-1][coordonnee[2]][2],new_coord)
    elif key == "Right":
        if coordonnee[3] < 2:
            print("t")
            new_coord = [coordonnee[0],coordonnee[1],coordonnee[2],coordonnee[3]+1]
            print(liste_button_jouable)
            selectionnement(liste_button_jouable[coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]+1], sudoku_liste[ind][coordonnee[0]][coordonnee[1]][coordonnee[2]][coordonnee[3]+1],new_coord)
        elif coordonnee[1] < 2:
            new_coord = [coordonnee[0],coordonnee[1]+1,coordonnee[2],0]
            print(liste_button_jouable)
            selectionnement(liste_button_jouable[coordonnee[0]][coordonnee[1]+1][coordonnee[2]][0], sudoku_liste[ind][coordonnee[0]][coordonnee[1]+1][coordonnee[2]][0],new_coord)




# def construire_modeles(caneva, hauteur):
#     x = (hauteur - 40)//9
#     caneva.create_line(0, 6, hauteur, 6, fill="black", width=7)
#     caneva.create_line(6, 0, 6, hauteur, fill="black", width=7)
#     for i in range(1,4):
#         caneva.create_line(0, 6 + i * x, hauteur, 6 + i * x, fill="black", width=2) 
#         caneva.create_line(6 + i * x, 0, 6 + i * x, hauteur, fill="black", width=2)


#     for i in range(10):  
#         caneva.create_line(0, 3 + i * x, hauteur, 3 + i * x, fill="black", width=2) 
#     for j in range(0):  
#         caneva.create_line(7 + j * x, 0, 7 + j * x, hauteur, fill="black", width=2)
# #On dessine les bordure épaisses 
#     caneva.create_line(0, 0, hauteur, 7 , fill="black", width=7)
#     for i in range(1,4):
#         caneva.create_line(0, i * y-2, hauteur, 0 + i * y-2, fill="black", width=7)
#     for j in range(0):    
#         caneva.create_line(j * y, 0, j * y, hauteur, fill="black", width=7)