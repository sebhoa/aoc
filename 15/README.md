# Day 15

Un grand classique : recherche d'un plus court chemin. On peut coder un _Dijkstra_ mais...

- Version 1 : en gérant la recherche du sommet qui minimise la distance _à la main_ c'est à dire en O(n) ça passe
- Version 2 : ça ne passe plus, le graphe étant beaucoup plus gros que celui de la version 1. D'abord il faut construire ce graphe (puisqu'il découle du précédent par 24 duplications) ensuit il faut utiliser une stucture plus optimisée pour gérer les sommets à explorer. La file de priorité du module `heapq` permet de s'en sortir.

J'ai laissé la version 15b.py qui donne le résultat mais au bout de plusieurs minutes. La version 15c.py répond en 2-3s grâce à la file de priorité.