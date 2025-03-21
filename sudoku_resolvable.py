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

def next_number(sudoku,a,b,c,d):
    """Change la valeur de la case parmi les nombres possible, retourne false si aucune sol n'est trouvé, sinon true"""
    global retour
    cle = (a, b, c, d)
    if not retour:
        liste_possible_ephemere = num_possible.copy()
        num_possible_ephemere[cle] = num_possible.copy()
        
    else:
        if sudoku[a][b][c][d] in num_possible_ephemere[cle]:
            num_possible_ephemere[cle].remove(sudoku[a][b][c][d])
        liste_possible_ephemere = num_possible_ephemere[cle]


    for j in range(3):
        for l in range(3):
            if sudoku[a][j][c][l] in liste_possible_ephemere:
                liste_possible_ephemere.remove(sudoku[a][j][c][l])

    for i in range(3):
        for k in range(3):
            if sudoku[i][b][k][d] in liste_possible_ephemere:
                liste_possible_ephemere.remove(sudoku[i][b][k][d])

    for k in range(3):
        for l in range(3):
            if sudoku[a][b][k][l] in liste_possible_ephemere:
                liste_possible_ephemere.remove(sudoku[a][b][k][l])


    num_possible_ephemere[cle] = liste_possible_ephemere
    if liste_possible_ephemere != []:
        num_random = rd.choice(liste_possible_ephemere)
        sudoku[a][b][c][d] = num_random
        retour = False
        return True
            
        


    else:
        retour = True
        sudoku[a][b][c][d] = 0
        return False
        



def generateur():
    """Genere la grille résolu"""
    global num_possible_ephemere, sudoku_incomplet
    i = 0
    j = 0
    k = 0
    l = 0
    num_possible_ephemere = {}
    while i < 3:
        while j < 3:
            while k < 3:
                while l < 3:
                    next = next_number(sudoku,i,j,k,l)
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
    sudoku_incomplet = copy.deepcopy(sudoku)
                    

sudoku_incomplet = []

def suppression_solution():
    """Supprime un a un chauqe nombre pour arriver a un sudoku resolvable"""
    z = 0
    e = 0
    r = 0
    t = 0
    
    for _ in range(3): #Ne marche qu'avec des petits nombre (il faut pouvoir reellement verifier l unicite)
        test_solve = False
        while test_solve == False:
            z,e,r,t = rd.randint(0,2), rd.randint(0,2), rd.randint(0,2), rd.randint(0,2)

            while sudoku_incomplet[z][e][r][t] == 0:
                z,e,r,t = rd.randint(0,2), rd.randint(0,2), rd.randint(0,2), rd.randint(0,2)
            temp = sudoku_incomplet[z][e][r][t]
            sudoku_incomplet[z][e][r][t] = 0            
            
            num_fixe.append((z,e,r,t))
            sudoku_incomplet2 = copy.deepcopy(sudoku_incomplet)
            test_solve = solveur(sudoku_incomplet2)
            
            
            if test_solve == False:
                num_fixe.remove((z,e,r,t))
                sudoku_incomplet[z][e][r][t] = temp
        test_solve = False

def solveur(sudoku_incomplet): # faire uen sorte de verifier si cest possible d avoir deux solution
    """Resous le sudoku pour tester l unicite de la solution"""
    next = True
    global num_possible_ephemere
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
    if sudoku_incomplet == sudoku:
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

generateur()
sudoku_affichage(sudoku)
suppression_solution()
sudoku_affichage(sudoku_incomplet)






