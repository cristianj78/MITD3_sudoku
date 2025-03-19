Ce README explique le code contenu dans le fichier "main.py":

1 : Les modules 

1: Tkinter : Afin de pouvoir réaliser les interfaces graphique pour y instaurer le jeu du Sudoku
2 : Random : Pour générer les grilles de Sudoku de façon aléatoire
3 : copy : Car on est en présence de liste de sous-listes (même cas pour les objets)
4 : json : Pour implanter le système de sauvegarde des modèles

2 : Que fait le programme ?

Lorsque vous exécuter le programme, une première fenêtre se lance en vous proposant 3 difficultés (Facile, Moyen, Difficile)
Ces difficultés se basent sur le nombre de cases enlevées (Facile: 40, Moyen:50, Difficile:60), notez qu'il est possible de modifier ces
nombres de cases vides à tout moment à la fin du programme, veuillez à ne pas dépasser le nombre de 60 cases vides, au-delà, le sudoku
est alors impossible à résoudre car plusieurs solutions sont envisageables.
