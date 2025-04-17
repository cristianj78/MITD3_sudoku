from tkinter import *
from random import *
from copy import deepcopy
import time 
import json 
import webbrowser

racine = Tk()
racine.config(bg="white")
racine.geometry("1080x800")
racine.title("Fenêtre principale")

def effacer_widget(fenetre):
    for widget in fenetre.winfo_children(): 
        widget.destroy()

def ajouter_sauvegarde(sauvegarde):
    sauvegarde["Nombre de vie"] = nb_vies 
    with open("sauvegardes.json", "r") as fichier:
        try:
            ajout = json.load(fichier)
        except json.JSONDecodeError: 
            ajout = {}
        if len(ajout) > 9:
            print("trop de sauvegardes")
        else:
            ajout[f"sauvegarde{len(ajout)+1}"] = sauvegarde 
            print(ajout)
            with open("sauvegardes.json", "w") as fich:
                json.dump(ajout, fich) 

sudoku = [[] for i in range(9)]

def est_valide(grille_corrigee, ligne, col, num):
    bloc_x, bloc_y = (ligne // 3) * 3, (col // 3) * 3
    return (
        num not in grille_corrigee[ligne] and 
        num not in [grille_corrigee[i][col] for i in range(9)] and 
        num not in [grille_corrigee[i][j] for i in range(bloc_x, bloc_x+3) for j in range(bloc_y, bloc_y+3)]
    )

def remplir_grille(grille):
    for ligne in range(9):
        for col in range(9):
            if grille[ligne][col] == 0:
                for num in sample(range(1, 10), 9):  
                    if est_valide(grille, ligne, col, num):
                        grille[ligne][col] = num
                        if remplir_grille(grille): 
                            return True
                        grille[ligne][col] = 0  
                return False  
    return True  

def generer_sudoku(): 
    grille = [[0] * 9 for i in range(9)]  
    remplir_grille(grille)
    return grille

def creer_cases_vides(grille, nb_cases=40):
    cases = [(i, j) for i in range(9) for j in range(9)]
    shuffle(cases) 
    for i in range(nb_cases):
        ligne, col = cases.pop()
        grille[ligne][col] = 0   
    return grille

def dessiner_numeros(sudoku, position, hauteur, police):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                x = hauteur//17
                y = hauteur//9
                position.create_text(x + y*j, x+y*i,  text=str(sudoku[i][j]), fill="black", font=("Arial", police))
    return sudoku

def dessiner_lignes(canva, hauteur):
    """On divise la longueur ou la hauteur (c'est un carré) par 9 (9 cases)"""  
    x = hauteur//9
    y = hauteur//3
    for i in range(10):  
        canva.create_line(0, i * x, hauteur, i * x, fill="black", width=2, tags="ligne") 
    for j in range(10):  
        canva.create_line(j * x, 0, j * x, hauteur, fill="black", width=2, tags="ligne") 
    for i in range(4):
        canva.create_line(0, i * y-3, hauteur, i * y-3, fill="black", width=5, tags="ligne")
    for j in range(4):    
        canva.create_line(j * y-3, 0, j * y-3, hauteur, fill="black", width=5, tags="ligne")

nb_vies = 15

def afficher_sauvegarde_effectuee(sauvegarde, fenetre):
    ajouter_sauvegarde(sauvegarde)
    text = Label(fenetre, text="Sauvegarde effectuée !", bg="white").pack()

def verifier_reponse(reponse, grille_corrigee, grille, boite_information, modele_choisi, i, j, jeu, affichage_vie, debut_chrono, Choix_numero, sauvegarde):
    global nb_vies, case_cliquee, nb_erreurs
    if reponse == grille_corrigee[i][j]: 
        jeu.create_rectangle(55*j, 55*i, 55*(j+1), 55*(i+1), fill="#cccac3", outline = "#cccac3") 
        jeu.create_text(28 + 55*j, 29 + 55*i,  text=str(grille_corrigee[i][j]), fill="black", font=("Arial", 25))
        grille[i][j] = grille_corrigee[i][j]
        jeu.delete(case_cliquee)
    if grille[i][j] == 0: 
        jeu.delete(case_cliquee)
        jeu.create_rectangle(55*j, 55*i, 55*(j+1), 55*(i+1), fill="red") 
        jeu.tag_raise("ligne")
        nb_vies = nb_vies-1
        affichage_vie.config(text=f"Vies restantes : {nb_vies}")
        if nb_vies <= 0: 
            effacer_widget(modele_choisi)
            defaite = Label(modele_choisi, text = "Dommage, vous avez perdu..", font=("Arial",25), bg="white").pack(expand=YES)
            Retour = Button(modele_choisi, text = "Revenir à la sélection des modèles", font=("Arial", 10), width=30, height=3, bg="grey" ,command=modele_choisi.destroy).pack(expand=YES)
    if grille_corrigee == grille:
        effacer_widget(modele_choisi)
        victoire = Label(modele_choisi, text = "Bravo, vous avez gagné !", font=("Arial",21), bg="white").pack(expand=YES)
        erreurs = Label(modele_choisi, text=f"- Nombres d'erreurs comises : {15 - nb_vies}", font=("Arial", 15), bg="white").pack()
        temps = Label(modele_choisi, text=f"- Chronomètre : {int(time.perf_counter() - debut_chrono)}s", font=("Arial", 15), bg='white').pack() 
        sauvegarder = Button(modele_choisi, text="Sauvegarder le modèle ?", command=lambda:afficher_sauvegarde_effectuee(sauvegarde, modele_choisi),width=25, height=2, bg="grey", fg="white").pack()
        retour = Button(modele_choisi, text = "Revenir à la sélection des modèles", font=("Arial", 10), width=30, height=3, bg="grey", fg="white" ,command=modele_choisi.destroy).pack(expand=YES)



care_colorie = None
def aide_visuelle(event, grille_de_depart, grille_corrigee, grille, jeu):
    global care_colorie
    if care_colorie:
        jeu.delete(care_colorie)
    for x in range(9):
        for y in range(9):
            """exactement le même principe que pour la fonction "cliquer case"""
            if (x * 55) <= event.x < ((x + 1) * 55) and (y * 55) <= event.y < ((y + 1) * 55): 
                care_colorie = jeu.create_rectangle(55*x, 55*y, 55*(x+1), 55*(y+1), fill="grey")

def effacer_nombre(jeu, effacer, i, j, grille_de_depart, grille, grille_corrigee):
    grille[i][j] = 0
    jeu.create_rectangle(55*j, 55*i, 55*(j+1), 55*(i+1), fill="white", outline = "white")
    jeu.tag_raise("ligne")

case_cliquee = None

def cliquer_case(event, grille_de_depart, grille_corrigee, grille, jeu, position, nb_vies, affichage_vie, debut_chrono, sauvegarde):
    global case_cliquee
    if case_cliquee:
        jeu.delete(case_cliquee)
    trouvé = False
    i, j = -1, -1
    for x in range(9):
        for y in range(9):
            if (x * 55) <= event.x < ((x + 1) * 55) and (y * 55) <= event.y < ((y + 1) * 55):
                j, i, = x, y
                print(f"c'est la case {i+1} {j+1}") 
                trouvé = True
                break
        if trouvé:
            break
    case_cliquee = jeu.create_rectangle(55*j, 55*i, 55*(j+1), 55*(i+1), fill="black")
    jeu.tag_raise("ligne")
    Boite_information = Frame(position)
    Boite_information.grid(row=2, column=0)
    if grille_de_depart[i][j] == 0 and grille[i][j] != 0: 
        effacer = Button(position, text="effacer ce nombre", bg="grey", fg="white", command=lambda:effacer_nombre(jeu, effacer, i, j, grille_de_depart, grille, grille_corrigee))
        effacer.grid(row=7, column=0)
    if grille[i][j] == 0:
        Choix_numero = Label(position, text=f"modele_choisissez un numéro pour ({i+1}, {j+1})", bg="white") 
        Choix_numero.grid(row=5, column=0) 
        for k in range(1, 10):
            Numero = Button(Boite_information, text=str(k), command=lambda k=k :verifier_reponse(k, grille_corrigee, grille, Boite_information, position, i, j, jeu, affichage_vie, debut_chrono, Choix_numero, sauvegarde), width=5, height=2, bg="grey", fg="white")
            Numero.grid(row=2, column=k-1)

def validation_aide(Aide, jeu, grille_corrigee, grille, modele_choisi, aide_entry):
    if int(aide_entry.get()) < 1 or int(aide_entry.get()) > 9:
        erreur = Label(Aide, text="Veuillez respecter les contraintes.").pack(side=BOTTOM)
    else:
        for i in range(len(grille_corrigee)):
            for j in range(len(grille_corrigee[0])):
                if grille_corrigee[i][j] == int(aide_entry.get()):
                    grille[i][j] = grille_corrigee[i][j]
                    jeu.create_rectangle(55*j, 55*i, 55*(j+1), 55*(i+1), fill="#cccac3", outline = "#cccac3")
                    jeu.create_text(28 + 55*j, 29 + 55*i,  text=str(grille_corrigee[i][j]), fill="black", font=("Arial", 25))  
                    jeu.tag_raise("ligne")
        Aide.destroy()
    

def aide(jeu, grille_corrigee, grille, modele_choisi):
    Aide = Toplevel(modele_choisi)
    Aide.geometry("300x75")
    Aide.resizable(False, False)
    Aide.title("Aide")
    aide_text = Label(Aide, text="modele_choisissez un numéro, il sera révélé là où il apparait").pack(side=TOP)
    aide_entry = Entry(Aide)
    aide_entry.pack()
    valider_bouton = Button(Aide, text="Valider", command=lambda:validation_aide(Aide, jeu, grille_corrigee, grille, modele_choisi, aide_entry))
    valider_bouton.pack(side=BOTTOM)

def nouveau_jeu(grille_de_depart, grille_corrigee, i, grille, a_coche_aide, nb_vies_sauvegarde=15):
    """On va utiliser les varianles globales, car nb_vies doit pouvoir être modifié par plusiuers fonctions, et son contenu
    Doit pouvoir être retrouvé à tout moment, on peut donc pour chaque nouveau jeu rénitialiser nb_vies à 3"""
    global nb_vies
    nb_vies = nb_vies_sauvegarde
    debut_chrono = time.perf_counter() 
    modele_choisi = Toplevel(racine)
    modele_choisi.resizable(False, False)
    modele_choisi.geometry("500x650")
    modele_choisi.title(f"Modèle {i}")
    modele_choisi.config(bg="white")

    """ On initialise la sauvegarde, elle sera mis à jour toute seul car grille est modifiée """

    sauvegarde = {"Grille de depart" : grille_de_depart,
                  "Grille en cours" : grille,
                  "Grille corrigee" : grille_corrigee}  
    
    menu = Menu(modele_choisi)
    if a_coche_aide.get() == 1: 
        Aide = menu.add_command(label="Aide", command=lambda:aide(jeu, grille_corrigee, grille, modele_choisi))
    Sauvegarder = menu.add_command(label="Sauvegarder", command=lambda:ajouter_sauvegarde(sauvegarde))
    Quitter = menu.add_command(label="Quitter", command=modele_choisi.destroy)
    menu.add_separator()
    modele_choisi.config(menu = menu)
    Boite_menu = Frame(modele_choisi)
    Boite_menu.grid(row=1)

    affichage_vie = Label(Boite_menu, text=f"Vies restantes : {nb_vies}", bg="white", font=("Arial", 15))
    affichage_vie.grid(row=3, column=1)
    jeu = Canvas(modele_choisi, width=495, height=495, bg="white", highlightbackground="black")
    jeu.grid(row=0)
    dessiner_lignes(jeu, 500)
    dessiner_numeros(grille, jeu, 500, 25)
    jeu.bind("<Button-1>", lambda event :cliquer_case(event, grille_de_depart, grille_corrigee, grille, jeu, modele_choisi, nb_vies, affichage_vie, debut_chrono, sauvegarde))
    jeu.bind("<Motion>", lambda event: aide_visuelle(event, grille_de_depart, grille_corrigee, grille, jeu))

def modele_choisir_sauvegarde():
    sauvegardes = Toplevel(racine)
    sauvegardes.geometry("650x700")
    sauvegardes.config(bg="white")
    sauvegardes.resizable(False, False)
    sauvegardes.title("Sauvegardes")
    with open("sauvegardes.json", 'r') as fichier:
        donnees = json.load(fichier)
    liste_sudoku = []
    i = 0
    for modele in donnees:
        grille_de_depart = donnees[modele]["Grille de depart"]
        grille_en_cours = donnees[modele]["Grille en cours"]
        grille_corrigee = donnees[modele]["Grille corrigee"]
        nb_vie_sauvegarde = donnees[modele]["Nombre de vie"]
        boite_sauvegarde = Frame(sauvegardes, bg="white")
        nom = Label(boite_sauvegarde, text=f'Sauvegarde N°{i}', bg="white", font=("Arial", 15)).grid(row=0, column=0)
        liste_sudoku.append(grille_en_cours)
        boite_sauvegarde.grid(row=i//2, column=i%2, padx=25, pady=25)
        a_coche_aide = IntVar()
        option_aide = Checkbutton(boite_sauvegarde, text="Aide", variable=a_coche_aide, bg="grey")
        option_aide.grid(row=2, column=1)
        depuis_debut_chrono = Button(boite_sauvegarde, bg="grey", fg="white", text="Recommencer le modèle depuis le début", command=lambda i=i, nb_vie_sauvegarde = nb_vie_sauvegarde :nouveau_jeu(liste_sudoku[i], grille_corrigee, i+1, grille_de_depart, a_coche_aide, 15)) 
        depuis_debut_chrono.grid(row=1, column=0)  
        continuer = Button(boite_sauvegarde, bg="grey", fg="white", text="Continuer le modèle", command=lambda i=i, nb_vie_sauvegarde = nb_vie_sauvegarde:nouveau_jeu(grille_de_depart, grille_corrigee, i+1, liste_sudoku[i], a_coche_aide, nb_vie_sauvegarde)) 
        continuer.grid(row=2, column=0)   
        i += 1

couleurs = ["black", "green", "blue", "red", "grey", "orange"]

def deplacer(label, descend, root):
    """ Comme on utilise une fonction de regénération de modèle (qui supprime tout puis fait réapparaitre), la fonction tentera de manipuler
    des widgets qui n'existent plus (car la fonction se répète après 70ms) et renvera donc une erreur, on prévoit cela """
    try:
        label.config(fg=f"{couleurs[randint(0, len(couleurs)-1)]}")
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
    except TclError:
        return 

def choix_modele(Niveau):
    effacer_widget(racine)

    frame_animation = Frame(racine, width=300, height=110, bg="white")
    frame_animation.pack(side=TOP)

    s = Label(frame_animation, text="S", bg="white", font=("Arial", 30))
    s.place(x=0, y=0)
    u = Label(frame_animation, text="u", bg="white", font=("Arial", 30))
    u.place(x=50, y=15)
    d = Label(frame_animation, text="d", bg="white", font=("Arial", 30))
    d.place(x=100, y=30)
    o = Label(frame_animation, text="o", bg="white", font=("Arial", 30))
    o.place(x=150, y=45)
    k = Label(frame_animation, text="k", bg="white", font=("Arial", 30))
    k.place(x=200, y=60)
    u2 = Label(frame_animation, text="u", bg="white", font=("Arial", 30))
    u2.place(x=250, y=50)

    deplacer(s,descend = True, root=racine)
    deplacer(u,descend = True, root=racine)
    deplacer(d,descend = True, root=racine)
    deplacer(o,descend = True, root=racine)
    deplacer(k,descend=False, root=racine)
    deplacer(u2,descend=False, root=racine)   

    Boite_option = Frame(racine)
    Boite_option.pack(side=TOP, expand=YES)
    option = Label(Boite_option, text="Options :", fg="black")
    option.pack(side=LEFT)
    Sasuvegardes = Button(Boite_option, text="Ouvrir une sauvegarde", bg="white", command=modele_choisir_sauvegarde)
    Sasuvegardes.pack(side=LEFT, padx=20)
    regeneration = Button(Boite_option, text="Regénérer les modèles", bg= "white", command=lambda:choix_modele(Niveau))
    regeneration.pack(side=LEFT, padx=20)
    a_coche_aide = IntVar()
    option_aide = Checkbutton(Boite_option, text="Aide", variable=a_coche_aide, bg="white")
    option_aide.pack(side=RIGHT, padx=20)
    difficulté_retour = Button(Boite_option, text="modele_choisir la difficulté", bg= "white", command=jouer_au_sudoku)
    difficulté_retour.pack(side=RIGHT, padx=20)
    ouvrir_notice = Button(Boite_option, text="(Si vous ne connaissez pas les règles :) )", bg = "white", command=lambda:webbrowser.open("https://sudoku.com/fr/comment-jouer/regles-de-sudoku-pour-les-debut_chronoants-complets/"))
    ouvrir_notice.pack(side=RIGHT, padx=20)

    def zoom_modele(case_modele, event):
        case_modele.scale("all", 0, 0, 0.9, 0.9)
        case_modele.config(width=230, height=230)

    def reset_modele(case_modele, event):
        case_modele.scale("all", 0, 0, 1/0.9, 1/0.9)
        case_modele.config(width=255, height=255)

    racine.config(bg="white")
    boite_widget.destroy()
    Choix = Frame(racine, bg="grey")
    Choix.pack()
    liste_sudoku = []
    for i in range(6):
        boite = Frame(Choix, bg="grey")
        boite.grid(row=i//3, column=i%3, padx=25, pady=25)
        cases_modele = Canvas(boite, width=255, height=255, bg="white", highlightbackground="black")
        cases_modele.grid(row=0)
        """i//3 permet de placer les trois premiers canvas sur la première ligne avec la division entière, i%3 renvoie le reste 
        et place le canvas sur la colonne souhaitée, padx, pady sont utiles pour les espaces"""
        a = generer_sudoku()
        grille_corrigee = deepcopy(a) 
        grille_avec_vide = creer_cases_vides(a, Niveau)
        grille_de_depart = deepcopy(grille_avec_vide)
        dessiner_numeros(grille_avec_vide, cases_modele, 260, 15)
        dessiner_lignes(cases_modele, 260)
        liste_sudoku.append(grille_avec_vide)
        choix = cases_modele.bind("<Button-1>", lambda event, i=i, grille_corrigee = grille_corrigee, grille_de_depart = grille_de_depart:nouveau_jeu(grille_de_depart, grille_corrigee, i+1, liste_sudoku[i], a_coche_aide))             
        cases_modele.bind("<Enter>", lambda event, case_modele = cases_modele: zoom_modele(case_modele, event))
        cases_modele.bind("<Leave>", lambda event, case_modele = cases_modele: reset_modele(case_modele, event))
                           

def jouer_au_sudoku():
    effacer_widget(racine)
    boite_widget = Frame(racine) 
    boite_widget.pack(expand=YES, side=BOTTOM)
    difficulte = Label(racine, text="modele_choisissez la difficulté", font=("Times", 35, "bold"), bg="white")
    difficulte.pack(expand=YES, side=TOP)
    Facile = Button(boite_widget, text="Facile", fg="white", bg="grey", command=lambda:choix_modele(40), width=10, font=("Times", 25), height=3)
    Facile.grid(row=1, column=0)
    Moyen = Button(boite_widget, text="Moyen", fg="white", bg="grey", command=lambda:choix_modele(50), width=10, font=("Times", 25), height=3)
    Moyen.grid(row=1, column=1)
    Difficile = Button(boite_widget, text="Difficile", fg="white", bg="grey", command=lambda:choix_modele(60), width=10, font=("Times", 25), height=3)
    Difficile.grid(row=1, column=2)
    test = Button(boite_widget, text="test", fg="white", bg="grey", command=lambda:choix_modele(1), width=10, font=("Times", 25), height=3)
    test.grid(row=1, column=3)

boite_widget = Frame(racine)
boite_widget.pack(expand=YES, side=BOTTOM)

Choix = Label(racine, text="Sélectionner le jeu auquel vous voulez jouer.", font=("Times", 35, "bold"), bg="white")
Choix.pack(expand=YES, side=TOP)
Choix_sudoku = Button(boite_widget, text="Sudoku", width=10, fg="white", bg="grey", font=("Times", 25), height=3, command=jouer_au_sudoku).pack(side=LEFT)
choix_Hitori = Button(boite_widget, text="Hitori", width=10, fg="white", bg="grey", font=("Times", 25), height=3).pack(side=RIGHT)

img = PhotoImage(file="")
label = Label(racine, image=img)
label.pack()

racine.mainloop()