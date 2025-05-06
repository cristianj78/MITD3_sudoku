# Explication du contenu du fichier "main.py":

## 1 : Les modules 

- **Tkinter** : Afin de pouvoir réaliser les interfaces graphique pour y instaurer le jeu du Sudoku.
- **Random** : Pour générer les grilles de Sudoku de façon aléatoire.
- **Copy** : Car on est en présence de liste de sous-listes (même cas pour les objets).
- **Json** : Pour implanter le système de sauvegarde des modèles.
- **Time** : Qui va nous servir pour créer le chronomètre.
- **Webbrowser** : Pas d'une grande importance, sert uniquement pour le bouton qui vous mène vers le sites vous expliquant les règles du Sudoku

## 2 : Que fait le programme ?

En choisissant l'un des deux, trois difficultés vous seront alors proposées (Facile, Moyen, Difficile)
<div align="center">
  <img src="https://github.com/cristianj78/MITD3_sudoku/blob/main/images/Capture%20d%E2%80%99%C3%A9cran%202025-05-03%20193457.png" alt="Capture d'écran" width="600"/>
</div>



Ces difficultés se basent sur le nombre de cases vides (Facile: 40, Moyen: 50, Difficile: 60), <ins>notez</ins> qu'il est possible de modifier ces
nombres de cases vides à tout moment à la fin du programme, veuillez à ne pas **dépasser** le nombre de **60 cases vides**, au-delà, la résolution du sodoku devient ambigüe.

Après avoir choisi la difficulté, il vous est alors possible de choisir parmi une panoplie de modèles au nombre de <ins>6</ins>.

<div align="center">
  <img src="https://github.com/cristianj78/MITD3_sudoku/blob/main/images/Capture%20d%E2%80%99%C3%A9cran%202025-05-03%20193545.png" alt="Capture d'écran" width="600"/>
</div>

Avant de choisir le modèle, vous pouvez visiter les différentes options proposées : ouvrir une sauvegarde (Voir (3)), regénérer les modèles si aucun ne vous convient, étudier les règles du sudoku à travers un bouton vous redirigeant vers un site internet,
changer la difficulté, ou encore un bouton aide qui une fois pressé, active une possible aide dans le modèle choisi.

Une fois le modèle choisi, une deuxième fenêtre s'ouvre, c'est la fenêtre de jeu, vous pouvez alors commencer à jouer.

<div align="center">
  <img src="https://github.com/cristianj78/MITD3_sudoku/blob/main/images/Capture%20d%E2%80%99%C3%A9cran%202025-05-03%20193635.png" alt="Capture d'écran" width="300"/>
</div>
  
Sélectionnez à l'aide de la souris la case que vous voulez remplir, vous devrez évidemment choisir un chiffre entre 1 et 9, une réponse fausse entraine la perte d'un point de vie, un petit rectangle rouge de la taille de la case apparaitra pour signaler une erreur, noter que vous disposez un nombre total de 15 vies, entrainant la fin de la partie si toutes les vies sont perdues. 

<ins>**IMPORTANT**</ins> : Notez qu'une partie perdue **ne permet pas** la sauvegarde du modèle.

Si la réponse est validée, le numéro est affiché avec la case coloriée en gris vous indiquant que ce numéro est effaçable (car la case n'a pas été préremplie). Lorsque vous avez gagné 
(c'est à dire lorsque que toutes les cases ont été remplies), plusieurs statistiques seront affichées à l'écran telles que le temps mis pour résoudre ke sudoku, ainsi que le nombre d'erreurs comises.

<div align="center">
  <img src="https://github.com/cristianj78/MITD3_sudoku/blob/main/images/Capture%20d%E2%80%99%C3%A9cran%202025-05-03%20193714.png" alt="Capture d'écran" width="300"/>
</div>

<ins>IMPORTANT</ins> : En cas de partie gagnée, vous avez cette fois la **possibilité** de sauvegarder le modèle.

## 3 : Sauvegardes.

<ins>Json</ins> est utilisé dans ce programme afin de pouvoir permettre la mémorisation des modèles, ces mêmes modèles sont stockés sous forme de <ins>dictionnaires</ins>, lesquels sont eux-même associés à une clé unique
(on y retrouve la grille du début, la grille modifiée (par le joueur) ainsi que la grille corrigée qui sont les éléments essentiels pour la sauvegarde), vous pouvez dès lors recommencer un modèle depuis le début, ou
bien même continuer là où vous vous en êtes arrété, le nombre de sauvegardes maximale est de **7**. Vous avez la possibilité d'en supprimer directement à partir de l'interface graphique.

<div align="center">
  <img src="https://github.com/cristianj78/MITD3_sudoku/blob/main/images/Capture%20d%E2%80%99%C3%A9cran%202025-05-03%20194040.png" alt="Capture d'écran" width="300"/>
</div>

## 4 Fonctionnalités supplémentaires :

Le programme prend en charge plusieurs fonctionnalités supplémentaires:

- Les cases que vous aurez remplies sont toutes effaçable. (Remarque : les cases pré-remplies ne sont pas effaçables).
- le programme embarque un système permettant d'effectuer un "retour en arrière" c'est à dire effacer le dernier chiffre entré par le joueur.
- Une aide vous permettant d'afficher le chiffre entré par l'utilisateur partout où il apparait dans le puzzle.


