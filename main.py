from tkinter import *
from random import *
from copy import deepcopy
import time 
import json 
import webbrowser

racine = Tk()
racine.config(bg="#51aeb0")
racine.geometry("1080x800")
racine.title("Fenêtre principale")

def effacer_widget(fenetre):
    for widget in fenetre.winfo_children(): #fenetre.winfo_children() renvoit une liste d'objets correspondant aux widget de la fenetre
        widget.destroy()

def ajouter_sauvegarde(sauvegarde):
    with open("sauvegardes.json", "r") as fichier:
        try:
            ajout = json.load(fichier)
        except json.JSONDecodeError: #Si fichier vide
            ajout = {}
        ajout[f"sauvegarde{len(ajout)+1}"] = sauvegarde
        print(ajout)
    with open("sauvegardes.json", "w") as fich:
        json.dump(ajout, fich) 

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
        canva.create_line(0, i * y, hauteur, i * y, fill="black", width=5)
    for j in range(4):    
        canva.create_line(j * y, 0, j * y, hauteur, fill="black", width=5)

nb_vies = 15

def afficher_sauvegarde_effectuee(sauvegarde, fenetre):
    ajouter_sauvegarde(sauvegarde)
    text = Label(fenetre, text="Sauvegarde effectuée !", bg="#51aeb0").pack()


def verifier_reponse(reponse, grille_sans_vide, grille, boite_information, Choisi, i, j, jeu, affichage_vie, debut, Choix_numero, sauvegarde):
    global nb_vies
    if reponse == grille_sans_vide[i][j]:
        jeu.create_rectangle(55*j+5, 55*i+5, 55*(j+1)-5, 55*(i+1)-5, fill="#ded26f", outline = "#ded26f")
        jeu.create_text(28 + 55*j, 29 + 55*i,  text=str(grille_sans_vide[i][j]), fill="black", font=("Arial", 25))
        grille[i][j] = grille_sans_vide[i][j]
    if grille[i][j] == 0:
        jeu.create_rectangle(55*j+5, 55*i+5, 55*(j+1)-5, 55*(i+1)-5, fill="red") 
        nb_vies = nb_vies-1
        affichage_vie.config(text=f"Vies restantes : {nb_vies}")
        if nb_vies <= 0:
            effacer_widget(Choisi)
            defaite = Label(Choisi, text = "Dommage, vous avez perdu..", font=("Arial",25), bg="#51aeb0").pack(expand=YES)
            Retour = Button(Choisi, text = "Revenir à la sélection des modèles", font=("Arial", 10), width=30, height=3, bg="#ded26f" ,command=Choisi.destroy).pack(expand=YES)
    if grille_sans_vide == grille:
        effacer_widget(Choisi)
        victoire = Label(Choisi, text = "Bravo, vous avez gagné !", font=("Arial",25), bg="#51aeb0").pack(expand=YES)
        erreurs = Label(Choisi, text=f"- Nombres d'erreurs comises : {15 - nb_vies}", bg="#ded26f").pack()
        temps = Label(Choisi, text=f"Chronomètre : {time.perf_counter() - debut}", bg='#ded26f').pack() #On fait la différence entre la date de fin et celle du début ce qui nous donne le temps en secondes
        retour = Button(Choisi, text = "Revenir à la sélection des modèles", font=("Arial", 10), width=30, height=3, bg="#ded26f" ,command=Choisi.destroy).pack(expand=YES)
        sauvegarder = Button(Choisi, text="Sauvegarder le modèle ?", command=lambda:afficher_sauvegarde_effectuee(sauvegarde, Choisi), bg="#ded26f").pack()

def effacer_nombre(jeu, effacer, i, j, grille_a_sauvegarder, grille, grille_sans_vide):
        grille[i][j] = 0
        jeu.create_rectangle(55*j+3, 55*i+1, 55*(j+1)-1, 55*(i+1)-2, fill="#ded26f")

def cliquer_case(event, grille_a_sauvegarder, grille_sans_vide, grille, jeu, position, nb_vies, affichage_vie, debut, sauvegarde):
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
    if grille_a_sauvegarder[i][j] == 0 and grille[i][j] != 0:  #On vérifie que la case a été remplie par le joueur ET que cette même case n'était pas pré-remplie
        effacer = Button(position, text="effacer ce nombre", bg="#ded26f", command=lambda:effacer_nombre(jeu, effacer, i, j, grille_a_sauvegarder, grille, grille_sans_vide))
        effacer.grid(row=7, column=0)
    if grille[i][j] == 0:
        Choix_numero = Label(position, text=f"Choisissez un numéro pour ({i+1}, {j+1})", bg="#51aeb0") #On ne met pas le .grid() directement à la suite, cela renverrai None (causant des problèmes par la suite)
        Choix_numero.grid(row=5, column=0) 
        for k in range(1, 10):
            Numero = Button(Boite_information, text=str(k), command=lambda k=k :verifier_reponse(k, grille_sans_vide, grille, Boite_information, position, i, j, jeu, affichage_vie, debut, Choix_numero, sauvegarde), width=5, height=2, bg="#ded26f")
            Numero.grid(row=2, column=k-1)

def validation_aide(Aide, jeu, grille_sans_vide, grille, Choisi, aide_entry):
    if int(aide_entry.get()) < 1 or int(aide_entry.get()) > 9:
        erreur = Label(Aide, text="Veuillez respecter les contraintes.").pack(side=BOTTOM)
    else:
        for i in range(len(grille_sans_vide)):
            for j in range(len(grille_sans_vide[0])):
                if grille_sans_vide[i][j] == int(aide_entry.get()):
                    grille[i][j] = grille_sans_vide[i][j]
                    jeu.create_rectangle(55*j+2, 55*i, 55*(j+1)-1, 55*(i+1)-2, fill="#ded26f")
                    jeu.create_text(28+ +55*j,28+55*i,  text=str(grille_sans_vide[i][j]), fill="black", font=("Arial", 25))
        Aide.destroy()
    

def aide(jeu, grille_sans_vide, grille, Choisi):
    Aide = Toplevel(Choisi)
    Aide.geometry("300x75")
    Aide.resizable(False, False)
    Aide.title("Aide")
    aide_text = Label(Aide, text="Choisissez un numéro, il sera révélé là où il apparait").pack(side=TOP)
    aide_entry = Entry(Aide)
    aide_entry.pack()
    valider_bouton = Button(Aide, text="Valider", command=lambda:validation_aide(Aide, jeu, grille_sans_vide, grille, Choisi, aide_entry))
    valider_bouton.pack(side=BOTTOM)

    
def nouveau_jeu(grille_a_sauvegarder, grille_sans_vide, i, grille, resultat):
    """On va utiliser les varianles globales, car nb_vies doit pouvoir être modifié par plusiuers fonctions, et son contenu
    Doit pouvoir être retrouvé à tout moment, on peut donc pour chaque nouveau jeu rénitialiser nb_vies à 3"""
    global nb_vies 
    debut = time.perf_counter() #C'est comme si on actionnait le chrono :)
    Choisi = Toplevel(racine)
    Choisi.resizable(False, False)
    Choisi.geometry("500x650")
    Choisi.title(f"Modèle {i}")
    Choisi.config(bg="#51aeb0")

    sauvegarde = {"Grille de depart" : grille_a_sauvegarder,
                  "Grille en cours" : grille,
                  "Grille corrigee" : grille_sans_vide}
                            
    menu = Menu(Choisi)
    if resultat.get() == 1:
        Aide = menu.add_command(label="Aide", command=lambda:aide(jeu, grille_sans_vide, grille, Choisi))
    Sauvegarder = menu.add_command(label="Sauvegarder", command=lambda:ajouter_sauvegarde(sauvegarde))
    Quitter = menu.add_command(label="Quitter", command=Choisi.destroy)
    menu.add_separator()
    Choisi.config(menu = menu)
    Boite_menu = Frame(Choisi)
    Boite_menu.grid(row=1)

    nb_vies = 15
    affichage_vie = Label(Boite_menu, text=f"Vies restantes : {nb_vies}", bg="#51aeb0", font=("Arial", 15))
    affichage_vie.grid(row=3, column=1)

    jeu = Canvas(Choisi, width=500, height=500, bg="#ded26f")
    jeu.grid(row=0)
    construire_sudoku(jeu, 500)
    dessiner_sudoku(grille, jeu, 500, 25)
    jeu.bind("<Button-1>", lambda event :cliquer_case(event, grille_a_sauvegarder, grille_sans_vide, grille, jeu, Choisi, nb_vies, affichage_vie, debut, sauvegarde))


def choisir_sauvegarde():
    sauvegardes = Toplevel(racine)
    sauvegardes.geometry("650x700")
    sauvegardes.config(bg="#51aeb0")
    sauvegardes.resizable(False, False)
    sauvegardes.title("Sauvegardes")
    with open("sauvegardes.json", 'r') as fichier:
        donnees = json.load(fichier)
    liste_sudoku = []
    i = 0
    for modele in donnees:
        grille_a_sauvegarder = donnees[modele]["Grille de depart"]
        grille_en_cours = donnees[modele]["Grille en cours"]
        grille_sans_vide = donnees[modele]["Grille corrigee"]
        boite_sauvegarde = Frame(sauvegardes, bg="#51aeb0")
        nom = Label(boite_sauvegarde, text=f'Sauvegardes N°{i}', bg="#51aeb0", font=("Arial", 15)).grid(row=0, column=0)
        liste_sudoku.append(grille_en_cours)
        boite_sauvegarde.grid(row=i//2, column=i%2, padx=25, pady=25)
        resultat = IntVar()
        option_aide = Checkbutton(boite_sauvegarde, text="Aide", variable=resultat, bg="#ded26f")
        option_aide.grid(row=2, column=1)
        depuis_debut = Button(boite_sauvegarde, bg="#ded26f", text="Recommencer le modèle depuis le début", command=lambda i=i:nouveau_jeu(liste_sudoku[i], grille_sans_vide, i+1, grille_a_sauvegarder, resultat)) 
        depuis_debut.grid(row=1, column=0)  
        continuer = Button(boite_sauvegarde, bg="#ded26f", text="Continuer le modèle", command=lambda i=i:nouveau_jeu(grille_a_sauvegarder, grille_sans_vide, i+1, liste_sudoku[i], resultat)) 
        continuer.grid(row=2, column=0)   
        i += 1

def choix_modele(Niveau):
    effacer_widget(racine)
    Texte_modele = Label(racine, text="Choisir le modèle",  bg="#51aeb0", font=("Times", 35, "bold"))
    Texte_modele.pack(side=TOP, expand=YES)
    Boite_option = Frame(racine)
    Boite_option.pack(side=BOTTOM, expand=YES)
    Sasuvegardes = Button(Boite_option, text="Ouvrir une sauvegarde", bg="#ded26f", command=choisir_sauvegarde)
    Sasuvegardes.pack(side=RIGHT)
    regeneration = Button(Boite_option, text="Regénérer les modèles", bg= "#ded26f", command=lambda:choix_modele(Niveau))
    regeneration.pack(side=LEFT)
    resultat = IntVar()
    option_aide = Checkbutton(racine, text="Aide", variable=resultat, bg="#ded26f")
    option_aide.pack(side=BOTTOM)
    difficulté_retour = Button(Boite_option, text="Choisir la difficulté", bg= "#ded26f", command=jouer_au_sudoku)
    difficulté_retour.pack(side=TOP)
    ouvrir_notice = Button(racine, text="(Si vous ne connaissez pas les règles :) )", bg = "#ded26f", command=lambda:webbrowser.open("https://sudoku.com/fr/comment-jouer/regles-de-sudoku-pour-les-debutants-complets/"))
    ouvrir_notice.pack(side=TOP)

    racine.config(bg="#51aeb0")
    boite_widget.destroy()
    Choix = Frame(racine, bg="#51aeb0")
    Choix.pack()
    liste_sudoku = []
    #On crée un canvas pour chaque modèle (pour chaque frame)
    for i in range(6):
        cases_modele = Canvas(Choix, width=275, height=275, bg="#ded26f")
        cases_modele.grid(row=i//3, column=i%3, padx=25, pady=25)
        """i//3 permet de placer les trois premiers canvas sur la première ligne avec la division entière, i%3 renvoie le reste 
        et place le canvas sur la colonne souhaitée, padx, pady sont utiles pour les espaces"""
        a = generer_sudoku()
        grille_sans_vide = deepcopy(a) #copy ou list ne suffit plus, car on est en présence de sous-listes (même cas pour les objets)
        grille_avec_vide = creer_cases_vides(a, Niveau)
        grille_a_sauvegarder = deepcopy(grille_avec_vide)
        dessiner_sudoku(grille_avec_vide, cases_modele, 275, 15)
        construire_sudoku(cases_modele, 275)
        liste_sudoku.append(grille_avec_vide)
        boite = Frame(Choix)
        boite.grid(row=i//3, column=i%3, padx=25, pady=25)
        bouton = Button(boite, text=f"Choisir le modèle {i+1}", activebackground="blue", command=lambda i=i, grille_sans_vide = grille_sans_vide, grille_a_sauvegarder = grille_a_sauvegarder:nouveau_jeu(grille_a_sauvegarder, grille_sans_vide, i+1, liste_sudoku[i], resultat)) #On est obligé d'utiliser lambda à cause des parenthèses
        bouton.grid(row=1, column=0)                              #Car i change de valeur à chaque itération? on la stock donc

def jouer_au_sudoku():
    effacer_widget(racine)
    boite_widget = Frame(racine) #On l'a recréée parce qu'on vient de la delete
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

boite_widget = Frame(racine)
boite_widget.pack(expand=YES, side=BOTTOM)

Choix = Label(racine, text="Sélectionner le jeu auquel vous voulez jouer", font=("Times", 35, "bold"), bg="#51aeb0")
Choix.pack(expand=YES, side=TOP)
Choix_sudoku = Button(boite_widget, text="Sudoku", width=10, font=("Times", 25), height=3, bg="#ded26f", command=jouer_au_sudoku).pack(side=LEFT)
choix_Hitori = Button(boite_widget, text="Hitori", width=10, font=("Times", 25), height=3, bg="#ded26f").pack(side=RIGHT)

racine.mainloop()