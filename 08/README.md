# Day 08

Problème sur un affichage 7-segments défectueux.

Les 7 segments sont censés être :

```
 aaaa
b    c
b    c
 dddd
e    f
e    f
 gggg

```

Mais ils sont tous mélangés, le but est de retrouver où se trouve chaque segment.

- Version 1 : on compte dans les sorties de logs combien correspondent aux digits 1, 4, 7 et 8 qui sont les 4 seuls à présenter une signature (nombre de segments allumés) unique.

- Version 2 : finaliser l'analyse pour reconstituer l'information complète.

PS : code ignoble... à revoir absolument.