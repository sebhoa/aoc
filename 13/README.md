# Day 13

On manipule une _grande feuille tranparente_ qu'on va plier en deux horizontalement et verticalement. Les marques à certains endroits se chevauchent et à la fin ceux qui restent visibles forment le code à saisir (part two).

- Version 1 : pour comprendre le fonctionnement du pliage, on demande le nombre de point après 1 seul pliage
- Version 2 : on effectue tous les pliages, on affiche le résultat qui nous donne en ASCII art le code à entrer

En Python on va juste faire diminuer un ensemble : à chaque pliage, on supprime les points de la moitié basse ou droite et on rajoute le symétrique (qui peut déjà s'y trouver).