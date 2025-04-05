import tkinter as tk
import time
temps = 0
valeur_chiffre = None
def interface() :
    # Creation de la fenetre principale
    fenetre_principal = tk.Tk()
    fenetre_principal.title("Projet informatique")
    fenetre_principal.geometry("600x600")
    fenetre_principal.config(bg="#E2EAF4")
    # Creation de la fenetre du sudoku
    fenetre_sudoku = tk.Canvas(fenetre_principal,height=550, width=800, bg="#98F5F9", bd=3, )
    fenetre_sudoku.pack(pady=10)
    # Creation du bouton nouvelle partie
    bouton_nouvelle_partie = tk.Button(fenetre_principal, text="Nouvelle Parie", width=20, height=2, font= "Arial", bg ="white")
    bouton_nouvelle_partie.pack(pady=10)
    # creation de bouton
    button_quiter_partie = tk.Button(fenetre_sudoku, text="Quitter",width=10,height=2,bg="white", font = ("Arial",13))#button quiter
    button_quiter_partie.place(x=500, y=15)
    #Creation des cadres
    cadre_sudoku = tk.Frame(fenetre_sudoku, width=400, height=200, bg="black") #cadre du sudoku 
    cadre_sudoku.place(x=20,y=80)
    cadre_nombre = tk.Frame(fenetre_sudoku, width=260, height=300, bg='white') #cadre des nombres
    cadre_nombre.place(x=500, y=230)
    #Creation des boutons de controle 
    bouton_reture = tk.Button(fenetre_sudoku, text="↶",width=10,height=2,bg="white", font = "Arial") #bouton de retour
    bouton_reture.place(x=500, y=160)
    bouton_supprime = tk.Button(fenetre_sudoku, text="x",width=10,height=2,bg="white", font = "Arial") #bouton de supression
    bouton_supprime.place(x=640,y=160)
        #Creation des boutons de niveaux
    bouton_facile = tk.Button(fenetre_sudoku, text="Facile",width=6,height=1,bg="white", font = "Arial") # niveau facile
    bouton_facile.place(x=120,y=13)
    bouton_moyen = tk.Button(fenetre_sudoku, text="Moyen",width=6,height=1,bg="white", font = "Arial") #niveau moyen
    bouton_moyen.place(x=190,y=13)
    bouton_dificile = tk.Button(fenetre_sudoku, text="Difficile",width=6,height=1,bg="white", font = "Arial") #niveau dificile
    bouton_dificile.place(x=260,y=13)
    bouton_expert = tk.Button(fenetre_sudoku, text="Expert",width=6,height=1,bg="white", font = "Arial") #niveau expert
    bouton_expert.place(x=330,y=13)
    #Creation des labels
    label_niveux = tk.Label(fenetre_sudoku, text="Dificulter :", width=10, height=2, font = "Arial")
    label_niveux.place(x=20, y=5)
    # Creation de la casse de l'heure
    label_temp = tk.Label(fenetre_sudoku, width=10, height=2, font=("Arial", 13))
    label_temp.place(x=650, y=15) # Positionement du label 
    # Creation des boutons de nombres
    z = 1
    for i in range(3):
        for e in range(3):
            button_numero = tk.Button(cadre_nombre, text=str(z), width=10, height=5, bg="white", command= lambda chiffre = z: choisir_chiffre(chiffre))
            button_numero.grid(row=i, column=e)
            z += 1
    # Creation des grilles de sudoku
    button = None
    for t in range (3):
        for y in range(3):
            case = tk.Frame(cadre_sudoku, width=15, height=5, bg = "black", padx=1, pady=1)
            case.grid(row=t, column=y) # Positionnement des cases
            for o in range (3):
                for p in range(3):
                    button = tk.Button(case, width=4, height=2, bg = "#FFECA1", padx=1, pady=1, font = "Arial")
                    button.config(command= lambda bonton = button: placer(bonton, valeur_chiffre))
                    button.grid(row=o, column=p) # Positionnement des boutons

    # Fontion pour afficher le temps
    def creation_temps():
        global temps
        temps += 1
        heures = temps // 3600 # calucul des heures
        minutes = (temps % 3600) // 60 # calcul des minutes
        secondes = temps % 60 # calcul des secondes
        label_temp.config(text=f"{heures:02}:{minutes:02}:{secondes:02}") # affichage du temps 
        label_temp.after(1000, creation_temps) # Appelle la fonction toutes les 1 seconde
    # Démarrer le chronomètre
    
    # Creation d'un bouton pour quitter la partie
    def quitter_partie():
        fenetre_sudoku.destroy() # Ferme la fenetre principale
    button_quiter_partie.config(command=quitter_partie) # Appelle la fenetre pour quitter la partie
    # Creation d'un bouton pour retourner en arriere
   
    # bouton_dificile.config(command=niveau_dificile) # Appelle la fonction pour choisir le niveau facile 
    # Creation d'un bouton pour choisir le niveau facile 
    
    # bouton_expert.config(command=niveau_expert) # Appelle la fonction pour choisir le niveau facile 
    # Creation d'un bouton pour commencer une nouvelle partie
    
    def nouvelle_partie():
        bouton_nouvelle_partie = tk.Toplevel() # Creation d'une nouvelle fenetre
    bouton_nouvelle_partie.config(command=nouvelle_partie) # Appelle la fenetre pour commencer une nouvelle partie
    # Creation d'un bouton pour choisir un chiffre 
    
    # Remplir une case cliquée avec un chiffre
     # Variable pour stoker le chiffre selectioner
    def choisir_chiffre(chiffre):
        global valeur_chiffre
        valeur_chiffre = chiffre
        print(valeur_chiffre)

    bontons = []
    b = button
    def placer(b,valeur_chiffre): # Fonction pour changer le texte d'un bouton  
        b.config(text=valeur_chiffre) # Change le texte du bouton par le chiffre selectionner   
        bontons.append(b) # Ajouter la fontion placer das la liste des boutons choisies
        print (bontons)
    
    bouton_supprime.config(command=lambda: choisir_chiffre("")) 

    bout = bontons
    def revenir_en_arriere(bout):
        bng = bout.pop()   
        bng.config(text=" ")
    bouton_reture.config(command=lambda: revenir_en_arriere(bout)) # Appelle la fontion pour revenir en arriere
  
    creation_temps()
    fenetre_principal.mainloop()    

interface()


# def niveau_facile():
#     pass

# def niveau_moyen():
#     pass
    
# def niveau_dificile():
#     pass

# def niveau_expert():
#     pass
    
