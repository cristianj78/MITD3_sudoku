Ce document explique l'utilisation du code contenu dans le fichier "main.py" :

1 : Modules

On fait intervenir plusieurs modules dans ce programme:

Tkinter : pour réaliser une interface graphique où apparaitra le sudoku.
Random : pour remplir les grilles de sudoku de façon aléatoire.
Copy : utilisé car nous devons réaliser des copies de liste contenant des sous listes (même cas pour n'importe quel objet)
Json : pour implanter le système de sauvegarde des modèles de sudoku.

2 : Que fait le programme ? 

En éxecutant le programme, une fenêtre s'ouvre vous proposant de choisir le niveau de difficulté, ces niveaux se basent 
sur le nombre de cases vides dans la grille (Facile : 40, Moyen : 50, Difficile : 60). 
Vous pouvez d'ailleurs modifier ces nombres de cases vides, en ajustant le nombre associé à l'appel de la fonction choix_modele pour chacun des boutons aux lignes (187, 189, 191) 
Après avoir choisi la difficulté, une panoplie de puzzle au nombre de 6 vous est proposé, vous avez la possibilité de relancer une partie 
sauvegardée, que vous ayez déjà terminé un modèle où que vous ayez envie d'en continuer un autre.
Vous avez également la possibilté de jouer plusieurs modèles simultanément, de revenir au choix des modèles.

à finir
