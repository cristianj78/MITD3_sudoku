"""
Explication des variables importantes et variables globales : 

grille_de_depart -> C'est le début de tout modèle, cette grille n'est pas modifiée car
 on l'utilise dans le cas où l'utilisateur veut recommencer un modèle depuis le début.

grille -> C'est la grille de jeu, celle qui sera modifiée par l'utilisateur, elle aussi peut-être 
sauvegardée par l'utilisateur.

grille_corrigee -> C'est la correction du modèle, n'est jamais modifiée, sert en général à de multiples
comparaisons, elle aussi peut être sauvegardée par l'utilisateur.

nb_vies -> Je vais pas m'étaler...

care_colorie -> c'est une variable globale, exclusivement utilisée dans la fonction "aide_visuelle", 
elle permet le fonctionnement de l'aide visuelle qui affiche le petit carré gris selon la position de la 
souris.

case_cliquee -> C'est clairement le même fonctionnement que pour care_colorie

retour : C'est le bouton qui permet d'effectuer un retour en arrière, (effacer le dernier chiffre) 
on doit pouvoir le supprimer dans plusiuers fonctions

effacer = C'est le bouton qui efface un chiffre en particuilier, choisi par le joueur, lui aussi
doit pouvoir être supprimable dans plusieurs fonctions

liste_ations : C'est en quelque sorte l'historique des chiffres entrés par le joueur, doit être modifiable dans
plusieurs fonctions.
"""

from tkinter import *
from random import *
from copy import deepcopy
import time 
import json 
import webbrowser

racine = Tk()
racine.config(bg="white")
racine.geometry("1080x600")
racine.title("Fenêtre principale")
racine.resizable(False, False)

retour = None
effacer = None
case_cliquee = None
care_colorie = None

liste_actions = []
nb_vies = 15

def effacer_widget(fenetre):
    """ Fonction qui nous sera très utile par la suite, efface tout le contenu d'une fenêtre"""
    for widget in fenetre.winfo_children(): # Fenetre.winfo_children() renvoit une liste d'objets correspondant aux widget de la fenetre.
        widget.destroy()

#####################
# Génération Sudoku #
#####################

sudoku = [[] for i in range(9)]

def est_valide(grille_corrigee, ligne, col, num):
    """ Vérifie que le num entré en paramètre respecte les règles du sudoku """
    bloc_x, bloc_y = (ligne // 3) * 3, (col // 3) * 3
    return (
        num not in grille_corrigee[ligne] and # Num n'est ni dans la ligne
        num not in [grille_corrigee[i][col] for i in range(9)] and # Ni dans la colonne
        num not in [grille_corrigee[i][j] for i in range(bloc_x, bloc_x+3) for j in range(bloc_y, bloc_y+3)]# Ni dans le bloc
    )

# On utilise le backtracking
def remplir_grille(grille):
    """ Permet de remplir une grille du Sudoku"""
    for ligne in range(9):
        for col in range(9):
            if grille[ligne][col] == 0:
                for num in sample(range(1, 10), 9):  # Mélange des nombres (Pas de shuffle, ça renverrait None)
                    if est_valide(grille, ligne, col, num):
                        grille[ligne][col] = num
                        if remplir_grille(grille): # Appel récursif, tant que la grille n'est pas valide.
                            return True
                        grille[ligne][col] = 0  # Retour en arrière
                return False  # Retour en arrière
    return True  

def a_deuxieme_solution(grille):
    """ Vérifie s'il existe une deuxième solution pour le sudoku """
    for ligne in range(9):
        for col in range(9):
            if grille[ligne][col] == 0:
                for num in range(1, 10):
                    if est_valide(grille, ligne, col, num):
                        grille[ligne][col] = num
                        if not remplir_grille(grille):  # Si une deuxième solution est trouvée
                            return True
                        grille[ligne][col] = 0  # Retour en arrière
    return False
# On sépare les deux fonctions par souci de sauvegarde

def generer_sudoku(): 
    grille = [[0] * 9 for i in range(9)]  
    remplir_grille(grille)
    return grille

def verifier_unicite(grille):
    """ Vérifie que la grille a une solution unique """
    copie_grille = [ligne[:] for ligne in grille]  # Copie de la grille
    if remplir_grille(copie_grille):  # Si une solution est trouvée
        return not a_deuxieme_solution(copie_grille)  # S'assurer qu'il n'y a pas de deuxième solution
    return False

def reinitialiser_grille_avec_solution_unique(nb_cases_vides):
    """Réarrange la grille de manière à garantir qu'elle a une solution unique"""
    while True: # Tant qu'on a pas trouvé, (ça peut être long...)
        grille = generer_sudoku()
        grille_corrigee = deepcopy(grille)
        grille_vides = creer_cases_vides(grille, nb_cases_vides)
        if verifier_unicite(grille_vides):
            return grille_vides, grille_corrigee

def creer_cases_vides(grille, nb_cases=40):
    """ Cette fonction nous permet de créer les niveaux de difficulté selon le nombre de cases restantes"""
    cases = [(i, j) for i in range(9) for j in range(9)]
    shuffle(cases) #mélange les cordonnés des élements de la liste
    for i in range(nb_cases):
        ligne, col = cases.pop()
        grille[ligne][col] = 0   
    return grille

def dessiner_numeros(sudoku, position, hauteur, police):
    """ Pour dessiner les numéros à l'intérieur des cases """
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                x = hauteur//17
                y = hauteur//9
                position.create_text(x + y*j, x+y*i,  text=str(sudoku[i][j]), fill="black", font=("Arial", police), tag="Nombres")
    return sudoku

def dessiner_lignes(canva, hauteur):
    """ On crée les lignes """
    x = hauteur//9 # On divise la longueur ou la hauteur (c'est un carré) par 9 (9 cases)
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

###############
# Sauvegardes #
###############

def ajouter_sauvegarde(sauvegarde):
    """ Ecrit la sauvegarde dans le fichier Json """
    sauvegarde["Nombre de vie"] = nb_vies # Car nb_vies est modifié globalement, on la sauvegarde donc uniquement lorsqu'on appuie sur sauvegarder
    with open("sauvegardes.json", "r") as fichier:
        try:
            ajout = json.load(fichier)
        except json.JSONDecodeError: # Si fichier vide
            ajout = {}
        if len(ajout) > 7: # Nombre sauvegarde maximale
            print("trop de sauvegardes")
        else:
            ajout[f"Sauvegarde {len(ajout)+1}"] = sauvegarde # On crée la nouvelle sauvegarde s'il reste de la place
            with open("sauvegardes.json", "w") as fich:
                json.dump(ajout, fich) 

def supprimer_sauvegarde(modele, donnees, boite_sauvegarde):
    """ Supprimer la sauvegarde en temps réel dans l'interface graphqique """
    del donnees[modele]
    with open("sauvegardes.json", "w") as f:
        json.dump(donnees, f)  # Il faut mettre à jour le fichier !
    boite_sauvegarde.destroy()

def choisir_sauvegarde():
    """ Création de la fenêtre "ouvrir sauvegarde" dans le menu principal """
    global retour, liste_actions, effacer
    retour, liste_actions, effacer = None, [], None # On est certain de recommencer une partie de sudoku sans probkème (variable qui serait déjà initialisée par exemple)
    sauvegardes = Toplevel(racine)
    sauvegardes.geometry("650x650")
    sauvegardes.config(bg="white")
    sauvegardes.resizable(False, False)
    sauvegardes.title("Sauvegardes")
    with open("sauvegardes.json", 'r') as fichier: # Ouverture du fichier, on va récup les éléments
        donnees = json.load(fichier)  
    i = 0
    Choix_sauvegarde = Frame(sauvegardes, bg="grey", relief=RAISED, highlightbackground="black", bd=10)
    Choix_sauvegarde.pack()
    for modele in donnees:
        grille_de_depart = donnees[modele]["Grille de depart"]
        grille_en_cours = donnees[modele]["Grille en cours"]
        grille_corrigee = donnees[modele]["Grille corrigee"]
        nb_vie_sauvegarde = donnees[modele]["Nombre de vie"]
        boite_sauvegarde = Frame(Choix_sauvegarde, bg="grey")
        nom_sauvegarde = Label(boite_sauvegarde, text=str(modele), bg="grey", font=("Arial", 15)).grid(row=0, column=0)
        boite_sauvegarde.grid(row=i//2, column=i%2, padx=25, pady=25)
        a_coche_aide = IntVar()
        option_aide = Checkbutton(boite_sauvegarde, text="Aide", variable=a_coche_aide, bg="grey")
        option_aide.grid(row=2, column=1)
        """ Toutes les variables à mettre dans le lambda sont celles qui changent car nous sommes dans une boucle parcourant
         un dictionnaire ! """
        depuis_debut = Button(boite_sauvegarde, bg="white", fg="black", text="Recommencer le modèle depuis le début", 
                                    command=lambda a_coche_aide = a_coche_aide, 
                                    i=i, nb_vie_sauvegarde = nb_vie_sauvegarde, 
                                    grille_corrigee = grille_corrigee, grille_en_cours = grille_en_cours, grille_de_depart = grille_de_depart 
                                    :nouveau_jeu(grille_en_cours, grille_corrigee, i+1, grille_de_depart, a_coche_aide, 15)) 
        depuis_debut.grid(row=1, column=0)    

        if grille_en_cours != grille_corrigee: # Si le joueur a sauvegardé le modèle dans le menu du jeu, cela veut dire qu'il l'a terminé, il doit donc le recommencer depuis le début
            continuer = Button(boite_sauvegarde, bg="white", fg="black", text="Continuer le modèle", command=lambda a_coche_aide = a_coche_aide, 
                               i=i, nb_vie_sauvegarde = nb_vie_sauvegarde,
                                grille_corrigee = grille_corrigee, grille_en_cours = grille_en_cours, grille_de_depart = grille_de_depart
                                :nouveau_jeu(grille_de_depart, grille_corrigee, i+1, grille_en_cours, a_coche_aide, nb_vie_sauvegarde)) 
            continuer.grid(row=2, column=0)  

        supprimer_sauvegarde1 = Button(boite_sauvegarde, bg="white", fg="black", text="Supprimer la sauvegarde", command=lambda 
                                        modele = modele, donnees = donnees, boite_sauvegarde = boite_sauvegarde :
                                        supprimer_sauvegarde(modele, donnees, boite_sauvegarde))
        supprimer_sauvegarde1.grid(row=3, column=0)

        i += 1

def afficher_sauvegarde_effectuee(sauvegarde, modele_choisi):
    """ Fonction passerelle """
    ajouter_sauvegarde(sauvegarde)
    text = Label(modele_choisi, text="Sauvegarde effectuée !", bg="white")
    text.pack()

####################
# Interface de jeu #
####################

def nouveau_jeu(grille_de_depart, grille_corrigee, i, grille, a_coche_aide, nb_vies_sauvegarde=15):
    """ Fonction créant le sudoku correspondant au modèle choisi, crée la potentielle sauvegarde """
    global nb_vies, retour, liste_actions, effacer          
    reotur, effacer, liste_actions = None, None, [] # L'user peut changer de modèle
    nb_vies = nb_vies_sauvegarde
    debut_chrono = time.perf_counter() # C'est comme si on actionnait le chrono :)
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
    if a_coche_aide.get() == 1: # Si le joueur a coché l'aide 
        Aide = menu.add_command(label="Aide", command=lambda:aide(debut_chrono, jeu, grille_corrigee, grille, modele_choisi, sauvegarde))
    Sauvegarder = menu.add_command(label="Sauvegarder", command=lambda:ajouter_sauvegarde(sauvegarde))
    Quitter = menu.add_command(label="Quitter", command=modele_choisi.destroy)
    menu.add_separator()
    modele_choisi.config(menu = menu)
    Boite_menu = Frame(modele_choisi)
    Boite_menu.grid(row=1)

    Boite_fonctionnalites = Frame(modele_choisi, bg="white")
    Boite_fonctionnalites.grid(row=3, column=0)

    retour = Button(Boite_fonctionnalites, text="Revenir en arrière", command=lambda : retour_en_arriere(jeu), bg="grey", fg="white")
    retour.grid(row=0, column=1, padx=20, pady=20)

    affichage_vie = Label(Boite_menu, text=f"Vies restantes : {nb_vies}", bg="white", font=("Arial", 15))
    affichage_vie.grid(row=3, column=1)
    jeu = Canvas(modele_choisi, width=495, height=495, bg="white", highlightbackground="black")
    jeu.grid(row=0)
    dessiner_lignes(jeu, 500)
    dessiner_numeros(grille, jeu, 500, 25)
    jeu.bind("<Button-1>", lambda event :cliquer_case(event, grille_de_depart, grille_corrigee, grille, jeu, modele_choisi, affichage_vie, debut_chrono, sauvegarde, Boite_fonctionnalites))
    jeu.bind("<Motion>", lambda event: aide_visuelle(event, grille, jeu))

def cliquer_case(event, grille_de_depart, grille_corrigee, grille, jeu, modele_choisi, affichage_vie, debut_chrono, sauvegarde, Boite_fonctionnalites):
    """Fonction qui affiche le choix des numéros pour la case modele_choisie."""
    global case_cliquee, liste_actions, retour, effacer # Obligation d'utiliser les variables globales, pour les mises à jour des dessins.
    jeu.delete("conflit") # On delete les cases en conflit à chaque clic
    if case_cliquee:
        jeu.delete(case_cliquee)
    trouvé = False
    i, j = -1, -1
    for x in range(9):
        for y in range(9):
            if (x * 55) <= event.x < ((x + 1) * 55) and (y * 55) <= event.y < ((y + 1) * 55):
                j, i, = x, y
                trouvé = True # La case a été trouvée, on break les deux boucles
                break
        if trouvé:
            break
    case_cliquee = jeu.create_rectangle(55*j, 55*i, 55*(j+1), 55*(i+1), fill="grey")
    if grille[i][j] != 0:
        jeu.create_text(28 + 55*j, 29 + 55*i,  text=str(grille_corrigee[i][j]), fill="black", font=("Arial", 25))
    jeu.tag_raise("ligne")

    Boite_nombres = Frame(modele_choisi, bg="white")
    Boite_nombres.grid(row=2, column=0)

    if grille_de_depart[i][j] == 0 and grille[i][j] != 0 and effacer == None:  # On vérifie que la case a été remplie par le joueur ET que cette même case n'était pas pré-remplie.
        effacer = Button(Boite_fonctionnalites, text="Effacer ce chiffre", bg="grey", fg="white", command=lambda:effacer_nombre(jeu, i, j, grille))
        effacer.grid(row=0, column=0, padx=20, pady=20)
    else:
        if effacer: # Pour faire en sorte que le bouton s'efface lorsque le joueur clique sur une case qui elle n'est pas effaçable
            effacer.destroy()
            effacer = None
    if grille[i][j] == 0: 
        for k in range(1, 10):
            Numero = Button(Boite_nombres, text=str(k), command=lambda k=k
                             :verifier_reponse(k, grille_corrigee, grille, modele_choisi, 
                             i, j, jeu, affichage_vie, debut_chrono, sauvegarde, grille_de_depart),
                             width=5, height=2, bg="grey", fg="white")
            Numero.grid(row=2, column=k-1)

def verifier_reponse(reponse, grille_corrigee, grille, modele_choisi, i, j, jeu, affichage_vie, debut_chrono, sauvegarde, grille_de_depart):
    """ Fonction qui vérifie à la fois la véracité d'une réponse et qui détecte si le joueur a résolu le modèle """
    global nb_vies, case_cliquee, liste_actions
    if reponse == grille_corrigee[i][j]: # Si le joueur a choisi le bon numéro
        jeu.delete("conflit")
        jeu.create_rectangle(55*j, 55*i, 55*(j+1), 55*(i+1), fill="#cccac3", outline = "#cccac3") 
        jeu.tag_raise("ligne") # à chaque fois qu'on dessine un rectangle, il se superpose sur une des lignes, on "remonte" alors les lignes dans la priorité d'affichage (voir fonction qui dessine les lignes, on se référe aux tags)
        jeu.create_text(28 + 55*j, 29 + 55*i,  text=str(grille_corrigee[i][j]), fill="black", font=("Arial", 25), tag="Nombres")
        grille[i][j] = grille_corrigee[i][j]
        jeu.delete(case_cliquee)

        rearranger_liste(i, j) # Le joueur peut valider plusieurs fois la réponse
        liste_actions.append([grille, i, j])

    if grille[i][j] == 0: # Si le joueur s'est trompé de numéro
        montrer_conflits(i, j, reponse, grille, jeu, grille_de_depart) # Pour montrer les contraintes
        jeu.delete(case_cliquee)
        jeu.create_rectangle(55*j, 55*i, 55*(j+1), 55*(i+1), fill="red") 
        jeu.tag_raise("ligne")
        nb_vies = nb_vies-1
        affichage_vie.config(text=f"Vies restantes : {nb_vies}")
        if nb_vies <= 0: # Si le joueur a perdu
            gagne_ou_perdu("perdu", modele_choisi, debut_chrono, sauvegarde)
    if grille_corrigee == grille: # Si le joueur a gagné
        gagne_ou_perdu("gagné", modele_choisi, debut_chrono, sauvegarde)

def rearranger_liste(i, j): 
    """ Fonction très importante ! L'utilisateur peut valider plusieurs fois la même réponse,
        ce qui va surcharger la liste, on fait donc en sorte qu'elle ne contiennent que des éléments uniques !"""
    global liste_actions
    for x in range(len(liste_actions)-1):
        if liste_actions[x][1] == i and liste_actions[x][2] == j:
            liste_actions.remove(liste_actions[x])  

def montrer_conflits(i, j, valeur, grille, jeu, grille_de_depart):
    """Colorie en rouge les cases en conflit avec la valeur donnée à la position (i, j). (évidemment si le joueur a
    entré une mauvaise réponse.)"""
    jeu.delete("conflit") # Eviter une surcharge des carrés conflits
    for col in range(9): # Pour les colones 
        if col != j and grille[i][col] == valeur and grille_de_depart[i][j] == 0:
            jeu.create_rectangle(55*col, 55*i, 55*(col+1), 55*(i+1), fill="#ffb5b5", outline="#ffb5b5", tag="conflit")
            jeu.tag_raise("Nombres")
    for row in range(9): # Pour les lignes
        if row != i and grille[row][j] == valeur and grille_de_depart[i][j] == 0:
            jeu.create_rectangle(55*j, 55*row, 55*(j+1), 55*(row+1), fill="#ffb5b5", outline="#ffb5b5", tag="conflit")
            jeu.tag_raise("Nombres")
    bloc_i, bloc_j = 3 * (i // 3), 3 * (j // 3)
    for row in range(bloc_i, bloc_i + 3): # Pour les blocs
        for col in range(bloc_j, bloc_j + 3):
            if (row != i or col != j) and grille[row][col] == valeur:
                jeu.create_rectangle(55*col, 55*row, 55*(col+1), 55*(row+1), fill="#ffb5b5", outline="#ffb5b5", tag="conflit")
                jeu.tag_raise("Nombres")
    jeu.tag_raise("ligne")

def gagne_ou_perdu(choix, modele_choisi, debut_chrono, sauvegarde):
    """ Permet d'afficher la victoire ou la défaite à partir des fonctions validation_aide ou verifier_reponse, facilite la compréhension"""
    if choix == "gagné":
        effacer_widget(modele_choisi)
        victoire = Label(modele_choisi, text = "Bravo, vous avez gagné !", font=("Arial",21), bg="white").pack(expand=YES)
        erreurs = Label(modele_choisi, text=f"- Nombres d'erreurs comises : {15 - nb_vies}", font=("Arial", 15), bg="white").pack()
        temps = Label(modele_choisi, text=f"- Chronomètre : {int(time.perf_counter() - debut_chrono)}s", font=("Arial", 15), bg='white').pack() #On fait la différence entre la date de fin et celle du début ce qui nous donne le temps en secondes, int() permet de convertir les secondes float en int pour obtenir un entier
        sauvegarder = Button(modele_choisi, text="Sauvegarder le modèle ?", command=lambda:afficher_sauvegarde_effectuee(sauvegarde, modele_choisi),width=25, height=2, bg="grey", fg="white").pack()
        retour = Button(modele_choisi, text = "Revenir à la sélection des modèles", font=("Arial", 10), width=30, height=3, bg="grey", fg="white" ,command=modele_choisi.destroy).pack(expand=YES)
    else:
        effacer_widget(modele_choisi)
        defaite = Label(modele_choisi, text = "Dommage, vous avez perdu..", font=("Arial",25), bg="white").pack(expand=YES)
        Retour = Button(modele_choisi, text = "Revenir à la sélection des modèles", font=("Arial", 10), width=30, height=3, bg="grey" ,command=modele_choisi.destroy).pack(expand=YES)

couleurs = ["black", "green", "blue", "red", "grey", "orange"]

def aide(debut_chrono, jeu, grille_corrigee, grille, modele_choisi, sauvegarde):
    """ Simple création de la fenêtre d'aide"""
    Aide = Toplevel(modele_choisi)
    Aide.geometry("300x75")
    Aide.resizable(False, False)
    Aide.title("Aide")
    aide_text = Label(Aide, text="choisissez un numéro, il sera révélé là où il apparait").pack(side=TOP)
    aide_entry = Entry(Aide)
    aide_entry.pack()
    valider_bouton = Button(Aide, text="Valider", command=lambda:validation_aide(debut_chrono, Aide, jeu, grille_corrigee, grille, modele_choisi, aide_entry, sauvegarde))
    valider_bouton.pack(side=BOTTOM)

def validation_aide(debut_chrono, Aide, jeu, grille_corrigee, grille, modele_choisi, aide_entry, sauvegarde):
    """ Partie logique de l'aide au joueur (rempli les cases où le numéro choisi apparait)."""
    global liste_actions
    if int(aide_entry.get()) < 1 or int(aide_entry.get()) > 9: # Si l'user entre un float
        erreur = Label(Aide, text="Veuillez respecter les contraintes.").pack(side=BOTTOM) # Le joueur a entré un chiffre ou nombre invalide
    else:
        for i in range(len(grille_corrigee)):
            for j in range(len(grille_corrigee[0])):
                if grille_corrigee[i][j] == int(aide_entry.get()) and grille[i][j] == 0: # La case n'est pas préremplie et elle correspond au chiffre:
                    grille[i][j] = grille_corrigee[i][j]
                    jeu.create_rectangle(55*j, 55*i, 55*(j+1), 55*(i+1), fill="#cccac3", outline = "#cccac3")
                    jeu.create_text(28 + 55*j, 29 + 55*i,  text=str(grille_corrigee[i][j]), fill="black", font=("Arial", 25), tag="Nombres")  
                    jeu.tag_raise("ligne")
                    liste_actions.append([grille, i, j])
        if grille_corrigee == grille: # L'aide a fait gagné le joueur
            gagne_ou_perdu("gagné", modele_choisi, debut_chrono, sauvegarde)
        Aide.destroy()

def aide_visuelle(event, grille, jeu):
    """ Pour créer les petties cases grises qui améliore le confort de jeu """
    global care_colorie
    if care_colorie:
        jeu.delete(care_colorie)
    for x in range(9):
        for y in range(9):
            """exactement le même principe que pour la fonction "cliquer case"""
            if (x * 55) <= event.x < ((x + 1) * 55) and (y * 55) <= event.y < ((y + 1) * 55): 
                care_colorie = jeu.create_rectangle(55*x, 55*y, 55*(x+1), 55*(y+1), fill="#dadada")
                jeu.tag_raise("ligne")
                if grille[y][x] != 0: # Empêche de cacher la case à cause de l'aide visuelle
                    jeu.tag_raise("Nombres")

def effacer_nombre(jeu, i, j, grille):
    """ Comme son nom l'indique"""
    global effacer, liste_actions, retour
    if len(liste_actions) > 0:
        grille[i][j] = 0
        jeu.create_rectangle(55*j, 55*i, 55*(j+1), 55*(i+1), fill="white", outline = "white")
        """Un peu complexe, le cacher ne suffit pas. Comme nous avons attribué un tag "Nombres" à tous les nombres, 
        dès qu'on remonte ce tag, les nombres effacés remontent aussi et on les revoit donc, 
        on doit donc chercher directement l'objet pour réellement le supprimer"""
        items = jeu.find_overlapping(28 + 55*j, 30 + 55*i, 28 + 55*j, 30 + 55*i) # Trouve tous les objets se trouvant dans cet interval de cordonnés
        for item in items:
            if jeu.type(item) == 'text':
                jeu.delete(item)
        jeu.tag_raise("ligne")
        """en effaçant un nombre, on doit aussi effacer l'action!!"""
        if len(liste_actions) > 1:
            liste_actions = [action for action in liste_actions if not (action[1] == i and action[2] == j)]
        else:
            liste_actions.pop()
    if effacer:
        effacer.destroy()
        effacer = None

def retour_en_arriere(jeu):
    """ Effectue un retour en arrière en supprimant le dernier chiffre entré par l'user """
    global liste_actions, retour, effacer
    if len(liste_actions) > 0:
        a_enlever = liste_actions.pop()
        i, j = a_enlever[1], a_enlever[2]
        a_enlever[0][i][j] = 0 # a_enlever[0][0] -> grille
        items = jeu.find_overlapping(28 + 55*j, 30 + 55*i, 28 + 55*j, 30 + 55*i) #Trouve tous les objets se trouvant dans cet interval de cordonnés
        for item in items:
            if jeu.type(item) == 'text':
                jeu.delete(item)
        jeu.create_rectangle(55*j, 55*i, 55*(j+1), 55*(i+1), fill="white", outline = "white")
        jeu.tag_raise("ligne")
    
##################
# Menu principal #
##################

#uniquement pour l'animation.
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
        label.place(x=place_x, y=place_y)
        root.after(70, lambda: deplacer(label,descend,root))
    except TclError:
        return 

def choix_modele(Niveau):
    """ Menu principal du sudoku """
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
    Boite_option.place(x=40, y=470)
    option = Label(Boite_option, text="Options :", fg="black")
    option.pack(side=LEFT)
    Sasuvegardes = Button(Boite_option, text="Ouvrir une sauvegarde", bg="#dedede", width=20, height=2, command=choisir_sauvegarde)
    Sasuvegardes.pack(side=LEFT, padx=20)
    regeneration = Button(Boite_option, width=20, height=2, text="Regénérer les modèles", bg= "#dedede", command=lambda:choix_modele(Niveau))
    regeneration.pack(side=LEFT, padx=20)
    a_coche_aide = IntVar()
    option_aide = Checkbutton(Boite_option, text="Aide", variable=a_coche_aide, bg="#dedede")
    option_aide.pack(side=RIGHT, padx=20)
    difficulté_retour = Button(Boite_option, text="Choisir la difficulté", width=20, height=2, bg= "#dedede", command=jouer_au_sudoku)
    difficulté_retour.pack(side=RIGHT, padx=20)
    ouvrir_notice = Button(Boite_option, width=30, height=2, text="(Si vous ne connaissez pas les règles :) )", bg = "#dedede", 
                           command=lambda:
                           webbrowser.open("https://sudoku.com/fr/comment-jouer/regles-de-sudoku-pour-les-debutants-complets/"))
    ouvrir_notice.pack(side=RIGHT, padx=20)

    def zoom_modele(case_modele, event):
        """ Permet de rétrécir le modèle pour plus d'effet esthétique """
        case_modele.config(width=230, height=230)
        case_modele.scale("all", 0, 0, 0.9, 0.9)

    def reset_modele(case_modele, event):
        """ Fait revenir le modèle dans sa taille initiale lorsque l'user quitte le modèle avec la souris"""
        case_modele.config(width=255, height=255)
        case_modele.scale("all", 0, 0, 1/0.9, 1/0.9)

    racine.config(bg="white")
    Choix = Frame(racine, bg="grey", relief=RAISED, highlightbackground="black", bd=10)
    Choix.place(x=50, y=130)                 # Afficher bordures
    # On crée un canvas pour chaque modèle (pour chaque frame)
    for i in range(3):
        boite = Frame(Choix, bg="grey")
        boite.grid(row=i//3, column=i%3, padx=25, pady=25)
        cases_zoom = Canvas(boite, width=255, height=255, bg="grey", highlightbackground="#dedede")
        cases_zoom.grid(row=0)
        cases_modele = Canvas(boite, width=255, height=255, bg="white", highlightbackground="black")
        cases_modele.grid(row=0)
        """i//3 permet de placer les trois premiers canvas sur la première ligne avec la division entière, i%3 renvoie le reste 
        et place le canvas sur la colonne souhaitée, padx, pady sont utiles pour les espaces"""
        grille_avec_vide, grille_corrigee = reinitialiser_grille_avec_solution_unique(Niveau)
        grille_de_depart = deepcopy(grille_avec_vide) # Copy ou list ne suffit plus, car on est en présence de sous-listes (même cas pour les objets)
        dessiner_numeros(grille_avec_vide, cases_modele, 260, 15)
        dessiner_lignes(cases_modele, 260)
        choix = cases_modele.bind("<Button-1>", lambda event, i=i, grille_corrigee = grille_corrigee, 
                                  grille_de_depart = grille_de_depart,
                                  grille_avec_vide = grille_avec_vide: # On instaure ces paramètres dans le lambda car ces mêmes paramètres changent selon l'indice de la boucle, il faut donc les stocker. 
                                  nouveau_jeu(grille_de_depart, grille_corrigee, i+1, grille_avec_vide, a_coche_aide))         
                                
        cases_modele.bind("<Enter>", lambda event, case_modele = cases_modele: zoom_modele(case_modele, event))
        cases_zoom.bind("<Leave>", lambda event, case_modele = cases_modele: reset_modele(case_modele, event))
        cases_zoom.bind("<Enter>", lambda event, case_modele = cases_modele: zoom_modele(case_modele, event))
        cases_modele.bind("<Leave>", lambda event, case_modele = cases_modele: reset_modele(case_modele, event))     

def jouer_au_sudoku():
    """ Choix de la difficulté """
    effacer_widget(racine)
    boite_widget = Frame(racine, bg="grey", relief=RAISED, highlightbackground="black", bd=10)
    boite_widget.pack(expand=YES, side=BOTTOM)
    difficulte = Label(racine, text="Choisissez la difficulté", font=("Times", 35, "bold"), bg="white")
    difficulte.pack(expand=YES, side=TOP)
    Facile = Button(boite_widget, text="Facile", fg="black", bg="#dedede", command=lambda:choix_modele(20), width=10, font=("Times", 25), height=3)
    Facile.grid(row=1, column=0)
    Moyen = Button(boite_widget, text="Moyen", fg="black", bg="#b2b1b1", command=lambda:choix_modele(30), width=10, font=("Times", 25), height=3)
    Moyen.grid(row=1, column=1)
    Difficile = Button(boite_widget, text="Difficile", fg="black", bg="grey", command=lambda:choix_modele(40), width=10, font=("Times", 25), height=3)
    Difficile.grid(row=1, column=2)
    Extreme = Button(boite_widget, text="Extrême", fg="#b2b1b1", bg="black", command=lambda:choix_modele(50), width=10, font=("Times", 25), height=3)
    Extreme.grid(row=1, column=3)

jouer_au_sudoku()

racine.mainloop()
