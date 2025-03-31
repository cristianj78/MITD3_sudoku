Ce README explique le code contenu dans le fichier "main.py":

1 : Les modules 

Tkinter : Afin de pouvoir réaliser les interfaces graphique pour y instaurer le jeu du Sudoku.

Random : Pour générer les grilles de Sudoku de façon aléatoire.

Copy : Car on est en présence de liste de sous-listes (même cas pour les objets).

Json : Pour implanter le système de sauvegarde des modèles.

time : Qui va nous servir pour créer le chronomètre.

Webbrowser : Pas d'une grande importance, sert uniquement pour le bouton qui vous mène vers le sites vous expliquant les règles du Sudoku

2 : Que fait le programme ?

Lorsque vous exécuter le programme, une première fenêtre se lance en vous proposant de jouer à l'un des deux jeux:

-Le Sudoku
-Le Hitori (bientôt...)

En choisissant l'un des deux, trois difficultés vous seront alors proposées (Facile, Moyen, Difficile)
Ces difficultés se basent sur le nombre de cases vides (Facile: 40, Moyen: 50, Difficile: 60), notez qu'il est possible de modifier ces
nombres de cases vides à tout moment à la fin du programme, veuillez à ne pas dépasser le nombre de 60 cases vides, au-delà, le sudoku
est alors impossible à résoudre car plusieurs solutions sont envisageables.

3 : Sauvegardes.

Json est utilisé dans ce programme afin de pouvoir permettre la mémorisation des modèles, ces mêmes modèles sont stockés sous forme de dictionnaires, lesquels sont eux-même associés à une clé unique (on y retrouve la grille du début, la grille modifiée (par le joueur) ainsi que la grille corrigée qui sont les éléments essentiels pour la sauvegarde), vous pouvez dès lors recommencer un modèle depuis le début, ou
bien même continuer là où vous vous en êtes arrété 
