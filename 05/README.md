# Day 05

Un peu de géométrie plane. Des segments qui s'entre croisent, il s'agit de déterminer pour chaque point à coordonnées entières dans un rectangle, le nombre de segments qui passent par ce point.

On peut modéliser tout ça assez simplement : un segment est un objet constitué d'un point A et d'un point B. Puisqu'on ne s'intéresse qu'à des coordonnées entières, on peut calculer la direction à prendre pour aller de A vers B (un couple de la forme (1, 1), (-1, 1) etc. pour chacun des 8 directions possibles.) et marquer les points un par un (dans un dictionnaire par exemple). On n'a alors plus qu'à compter les points marqués plus d'une fois. 

La version 1 : on ne prend en compte que 4 directions (horizontales et verticales.

La version 2 : on manipule bien les 8 directions.