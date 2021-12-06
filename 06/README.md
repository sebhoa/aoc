# Day 06

Premier puzzle où le problème est exactement le même en _part one_ et en _part two_

La différence est sur la taille de la donnée. La deuxième demande explose l'algorithme naïf qui a probablement été codé en version 1.

- Version 1 : on modélise la population de poissons, naïvement par une liste où chaque individu est représenté par son _internal timer_ puis à chaque étape, on décrémente cette valeur, on rajoute les poissons qu'il faut etc. pour 80 jours ça passe...

- Version 2 : pour 256 notre liste de poissons explose. Il faut modéliser autrement. En fait chaque poisson n'a pas besoin d'être identifié, il suffit de compter les poissons qui ont le même _timer_ A chaque étape, on fait glisser les valeurs de cette liste de 10 valeurs (la dernière sert de tampon) vers la gauche et on ajoute à la population de timer 6 le nombre de poissons de timer 0... à la fin on somme ces valeurs (sauf la dernière).