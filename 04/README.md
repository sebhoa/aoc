# Day 04

Des grilles de bingo... une suite de nombres, il faut remplir les grilles et trouver la gagnante. On va reste sur de la POO (toujours cette idée de pouvoir utiliser ces petits exercices comme exemples en L1)

On va modéliser une grille par un dictionnaire qui à la valeur associe le couple de coordonnées. Ainsi, on _check_ la valeur sur la grille, on récupère les coordonnées et on met à jour un décompte des valeurs marquées sur la ligne et sur la colonne correspondante... arrivé à 5 sur l'une des entités la grille est gagnante.