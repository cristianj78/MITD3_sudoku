import tkinter as tk  

fenetre_principal = tk.Tk()
fenetre_principal.title("Projet informatique")
fenetre_principal.geometry("600x600")
fenetre_principal.config(bg="#E2EAF4")
fenetre_sudoku = tk.Canvas(fenetre_principal,height=500, width=700, bg="#98F5F9", bd=3, )
fenetre_sudoku.pack(pady=10)
bouton_nouvelle_partie = tk.Button(fenetre_principal, text="Nouvelle partie", font=("Courier", 16, "italic"))
bouton_nouvelle_partie.pack()
cadre_sudoku = tk.Frame(fenetre_sudoku, width=400, height=440, bg="black")
cadre_sudoku.place(x=20,y=70)
cadre_nombre = tk.Frame(fenetre_sudoku, width=260, height=300, bg='white')
cadre_nombre.place(x=430, y=230)
bouton_reture = tk.Button(fenetre_sudoku, text="↶",width=13,height=2,bg="white")
bouton_reture.place(x=440, y=160)
bouton_supprime = tk.Button(fenetre_sudoku, text="x",width=13,height=2,bg="white")
bouton_supprime.place(x=580,y=160)
label_niveux = tk.Label(fenetre_sudoku, text="Dificulter :", width=10, height=2)
label_niveux.place(x=20, y=15)
bouton_facile = tk.Button(fenetre_sudoku, text="Facile",width=7,height=1,bg="white")
bouton_facile.place(x=120,y=18)
bouton_moyenne = tk.Button(fenetre_sudoku, text="Moyen",width=7,height=1,bg="white")
bouton_moyenne.place(x=190,y=18)
bouton_dificile = tk.Button(fenetre_sudoku, text="Difficile",width=7,height=1,bg="white")
bouton_dificile.place(x=260,y=18)
bouton_experte = tk.Button(fenetre_sudoku, text="Expert",width=7,height=1,bg="white")
bouton_experte.place(x=330,y=18)

z = 1
for i in range(3):
    for e in range(3):
        bouton_numero = tk.Button(cadre_nombre, text=str(z), width=11, height=5, bg="white")
        bouton_numero.grid(row=i, column=e)
        z += 1


for t in range (3):
    for y in range(3):
        case = tk.Frame(cadre_sudoku, width=17, height=6, bg = "black", padx=1, pady=1)
        case.grid(row=t, column=y)
        for o in range (3):
            for p in range(3):
                button = tk.Button(case, width=4, height=2, bg = "#FFECA1", padx=1, pady=1)
                button.grid(row=o, column=p)

entre_1 = []
import time 
demare = time.time()
fin = time.time()
le_temp_reel = fin - demare
affiche ="%d %d s" % (le_temp_reel//60, le_temp_reel%60)
affichage_temp = tk.Label(fenetre_sudoku, text= str(le_temp_reel), width=10, height=2)
affichage_temp.place(x=600, y=10)

fenetre_principal.mainloop()

