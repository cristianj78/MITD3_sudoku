import tkinter as tk
import random as rd
import time


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

i = 0
j = 0
k = 0
l = 0
retour = 0
num_possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
num_possible_ephemere = {}

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
        




def sudoku_affichage():
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
sudoku_affichage()





