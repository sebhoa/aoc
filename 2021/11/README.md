# Day 11

Du déjà vu : des valeurs dans une grille et on propage une info dans cette grille.


Ici les valeurs sont des énergies de petits _octopuss_. Toujours pour faire de la petite POO simple : un objet `Octopuss` qui possède une position et une énergie. Dès que cette énergie atteint 10, l'octopuss flash et ce flash doit se propager dans la colonie.

- Version 1 : on compte le nombre de flashes après 100 étapes
- Version 2 : on cherche à quelle étape tous les octopuss flashent en même temps.