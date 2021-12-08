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

## Explications de mon implémentation de la version 2

On peut tout résoudre par opérations ensemblistes. On appelle s1, s4, s7 et s8 les 4 ensembles de segments pour les chiffres 1, 4, 7 et 8. D'après la version 1, on sait que ces 4 là donnent un unique ensemble.

Et on note d1, d4, d7, d8 les correspondances _erronées_

- s7 - s1 donne un unique segment (d) qui correspond donc à d7 - d1
- s7 inter s1 donne 2 segments (ab) qui correspondent à d7 inter d1
- s4 - s1 donne ef qui correspond à d4 - d1
- les chiffres 0, 6, et 9 sont à 6 segments noton S6 cet ensemble s8 - S6 correspond alors à d8 - D6... et en croisant avec s7 - s1 et s4 - s1 on trouve les segments a et f. On en déduit alors b, e et g
- On a 6 segments on déduit le dernier.

