from tkinter import *
from random import *
from copy import *
import json 

racine = Tk()
racine.config(bg="#51aeb0")
racine.geometry("1080x800")
racine.title("sudoku")

#Boites contenant les différents choix
def ajouter_sauvegarde(sudoku): #Utilsation de JSON
    with open("sauvegardes.json", "a") as fichier:
        json.dump(sudoku, fichier) 

def sauvegarder(grille_sans_vide, grille):
    ajouter_sauvegarde(grille_sans_vide)

def chargement(fichier):
    with open("sauvegardes.json", "r") as fichier:
        json.load(fichier)

menu_bar = Menu(racine)
menu_bar.add_command(label="Ouvrir ")

sudoku = [[] for i in range(9)]

def est_valide(grille, ligne, col, num):
    bloc_x, bloc_y = (ligne // 3) * 3, (col // 3) * 3
    return (
        num not in grille[ligne] and #num n'est ni dans la ligne, ni dans la colonne, ni dans le bloc
        num not in [grille[i][col] for i in range(9)] and
        num not in [grille[i][j] for i in range(bloc_x, bloc_x+3) for j in range(bloc_y, bloc_y+3)]
    )

# On utilise le backtracking
def remplir_grille(grille):
    for ligne in range(9):
        for col in range(9):
            if grille[ligne][col] == 0:
                for num in sample(range(1, 10), 9):  # Mélange des nombres (Pas de shuffle, ça renverrait None)
                    if est_valide(grille, ligne, col, num):
                        grille[ligne][col] = num
                        if remplir_grille(grille): #appel récursif, tant que la grille n'est pas valide.
                            return True
                        grille[ligne][col] = 0  # Retour en arrière
                return False  # Retour en arrière
    return True  

def generer_sudoku(): #Position = Dans quel canva
    grille = [[0] * 9 for i in range(9)]  
    remplir_grille(grille)
    return grille

#On sépare les deux fonctions par souci de sauvegarde

def creer_cases_vides(grille, nb_cases=40):
    cases = [(i, j) for i in range(9) for j in range(9)]
    shuffle(cases) #mélange les cordonnés des élements de la liste
    for i in range(nb_cases):
        ligne, col = cases.pop()
        grille[ligne][col] = 0   
    return grille

def dessiner_sudoku(sudoku, position, hauteur, police):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                x = hauteur//17
                y = hauteur//9
                position.create_text(x + y*j, x+y*i,  text=str(sudoku[i][j]), fill="black", font=("Arial", police))
    return sudoku

def construire_sudoku(canva, hauteur):
    """On divise la longueur ou la hauteur (c'est un carré) par 9 (9 cases)"""  
    x = hauteur//9
    y = hauteur//3
#Création de la grille principale
    for i in range(10):  
        canva.create_line(0, i * x, hauteur, i * x, fill="black", width=2) 
    for j in range(10):  
        canva.create_line(j * x, 0, j * x, hauteur, fill="black", width=2)
#On dessine les bordure épaisses 
    for i in range(4):
        canva.create_line(0, i * y-2, hauteur, i * y-2, fill="black", width=7)
    for j in range(4):    
        canva.create_line(j * y, 0, j * y, hauteur, fill="black", width=7)

def verifier_reponse(reponse, grille_sans_vide, grille, boite_information, Choisi, i, j, jeu, text):
    if reponse == grille_sans_vide[i][j]:
        jeu.create_rectangle(55*j, 55*i+1, 55*(j+1)-1, 55*(i+1)-2, fill="#ded26f")
        jeu.create_text(28+ +55*j,28+55*i,  text=str(grille_sans_vide[i][j]), fill="black", font=("Arial", 25))
        grille[i][j] = grille_sans_vide[i][j]
    else:
        if grille[i][j] == 0:
            jeu.create_rectangle(55*j, 55*i, 55*(j+1), 55*(i+1)-2, fill="red")    
    if grille_sans_vide == grille:
        jeu.destroy()
        boite_information.destroy()
        text.destroy()
        Victoire = Label(Choisi, text = "Bravo, vous avez gagné !").grid(row=5, column=1)
        Retour = Button(Choisi, text = "Revenir à la sélection des modèles", command=Choisi.destroy).grid(row=4, column=1)
        

def cliquer_case(event, grille_sans_vide, grille, jeu, position):
    trouvé = False
    i, j = -1, -1
    for x in range(9):
        for y in range(9):
            if (x * 55) <= event.x < ((x + 1) * 55) and (y * 55) <= event.y < ((y + 1) * 55):
                j, i, = x, y
                print(f"c'est la case {i+1} {j+1}") #test
                trouvé = True
                break
        if trouvé:
            break

    Boite_information = Frame(position)
    Boite_information.grid(row=2, column=0)
    print(i+1, j+1) 
    print(grille[i][j])
    if grille[i][j] == 0:
        Choix_numero = Label(position, text=f"Choisissez un numéro pour ({i+1}, {j+1})") #On ne met pas le .grid() directement à la suite, cela renverrai None (causant des problèmes par la suite)
        Choix_numero.grid(row=5, column=0) 
        for k in range(1, 10):
            Numero = Button(Boite_information, text=str(k), command=lambda k=k :verifier_reponse(k, grille_sans_vide, grille, Boite_information, position, i, j, jeu, Choix_numero), width=5, height=2)
            Numero.grid(row=2, column=k-1)

liste_boutons = []
def nouveau_jeu(grille_sans_vide, i, grille):
    Choisi = Toplevel(racine)
    Choisi.resizable(False, False)
    Choisi.geometry("500x600")
    Choisi.title(f"Modèle {i}")

    menu = Menu(Choisi)
    Ouvrir = menu.add_command(label="Ouvrir")
    Sauvegarder = menu.add_command(label="Sauvegarder", command=lambda:sauvegarder(grille_sans_vide, grille))
    Quitter = menu.add_command(label="Quitter", command=Choisi.destroy)
    menu.add_separator()

    Choisi.config(menu = menu)

    Boite_menu = Frame(Choisi)
    Boite_menu.grid(row=1)
    jeu = Canvas(Choisi, width=500, height=500, bg="#ded26f")
    jeu.grid(row=0)
    construire_sudoku(jeu, 500)
    dessiner_sudoku(grille, jeu, 500, 25)
    jeu.bind("<Button-1>", lambda event :cliquer_case(event, grille_sans_vide, grille, jeu, Choisi))


def choix_modele(Niveau):
    Sasuvegardes = Button(racine, text="Ouvrir une sauvegarde", command=sauvegarder)
    Sasuvegardes.pack(side=TOP)

    racine.config(bg="#51aeb0")
    global difficulte
    difficulte.config(text="Choisssez le modèle", bg="#51aeb0", font=("Times", 35, "bold"))
    boite_widget.destroy()
    Choix = Frame(racine, bg="#51aeb0")
    Choix.pack()
    liste_sudoku = []
    #On crée un canvas pour chaque boite
    for i in range(6):
        cases_modele = Canvas(Choix, width=275, height=275, bg="#ded26f")
        cases_modele.grid(row=i//3, column=i%3, padx=25, pady=25)
        """i//3 permet de placer les trois premiers canvas sur la première ligne avec la division entière, i%3 renvoie le reste 
        et place le canvas sur la colonne souhaitée, padx, pady sont utiles pour les espaces
        """
        a = generer_sudoku()
        grille_sans_vide = deepcopy(a) #copy ou list ne suffit plus, car on est en présence de sous-listes (même cas pour les objets)
        grille_avec_vide = creer_cases_vides(a, Niveau)
        dessiner_sudoku(grille_avec_vide, cases_modele, 275, 15)
        construire_sudoku(cases_modele, 275)
        liste_sudoku.append(grille_avec_vide)
        boite = Frame(Choix)
        boite.grid(row=i//3, column=i%3, padx=25, pady=25)
        bouton = Button(boite, text=f"Choisir le modèle {i+1}", command=lambda i=i, grille_sans_vide = grille_sans_vide:nouveau_jeu(grille_sans_vide, i+1, liste_sudoku[i])) #On est obligé d'utiliser lambda à cause des parenthèses
        bouton.grid(row=1, column=0)                              #Car i change de valeur à chaque itération? on la stock donc


boite_widget = Frame(racine, bg="lightgrey")
boite_widget.pack(expand=YES, side=BOTTOM)
difficulte = Label(racine, text="Choisissez la difficulté", font=("Times", 35, "bold"), bg="#51aeb0")
difficulte.pack(expand=YES, side=TOP)
Facile = Button(boite_widget, text="Facile", command=lambda:choix_modele(40), width=10, font=("Times", 25), height=3, bg="#ded26f")
Facile.grid(row=1, column=0)
Moyen = Button(boite_widget, text="Moyen", command=lambda:choix_modele(50), width=10, font=("Times", 25), height=3, bg="#ded26f")
Moyen.grid(row=1, column=1)
Difficile = Button(boite_widget, text="Difficile", command=lambda:choix_modele(60), width=10, font=("Times", 25), height=3, bg="#ded26f")
Difficile.grid(row=1, column=2)
test = Button(boite_widget, text="test", command=lambda:choix_modele(1), width=10, font=("Times", 25), height=3, bg="#ded26f")
test.grid(row=1, column=3)

racine.mainloop()