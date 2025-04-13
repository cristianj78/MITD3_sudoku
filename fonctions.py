import tkinter as tk
import random as rd
import time
import copy #Conseiller par chatgpt, car .copy() ne copie pas ne profondeur

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
    # print(retour)
    if not retour:
        liste_possible_ephemere = num_possible.copy()
        # print(num_possible_ephemere)
        num_possible_ephemere[cle] = num_possible.copy()
        # print(num_possible_ephemere)
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
        # print("r")
        return True
            
        


    else:
        retour = True
        # print('e')
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
            # print(z,e,r,t)            
            
            num_fixe.append((z,e,r,t))
            sudoku_incomplet2 = copy.deepcopy(sudoku_incomplet)
            test_solve = solveur(sudoku_incomplet2, sudoku_complet)
            
            # print(test_solve)
            if test_solve == False:
                num_fixe.remove((z,e,r,t))
                sudoku_incomplet[z][e][r][t] = temp
        test_solve = False
    return sudoku_incomplet, sudoku_complet

def solveur(sudoku_incomplet, sudoku_complet): # faire uen sorte de verifier si cest possible d avoir deux solution
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
                    # print(i,j,k,l)
                    if (i,j,k,l) in num_fixe:
                        next = next_number(sudoku_incomplet,i,j,k,l)
                    # print(i,j,k,l)
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

def changement_frame(root, menu, frame_menu, frame_nouvelle_partie, frame_a_afficher):
    frame_menu.pack_forget()
    frame_nouvelle_partie.pack_forget()
    frame_a_afficher.pack(pady=5)
    if frame_a_afficher != frame_menu:
        root.config(menu=menu)
    else:
        root.config(menu=menu)


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
        
# def changement_vers_partie_jouable()









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