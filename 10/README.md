# Day 10

Aujourd'hui un grand classique : vérifier qu'une chaîne de caractères est correctement parenthésée.

- Version 1 : on fait un calcul de score sur les lignes corrompues (ie qui présente un caractère fermant qui ne matche pas un ouvrant)
- Version 2 : on fait un calcul de score sur les lignes incomplètes (pas de cractères fermants qui dysfonctionnent mais il manque une partie)

On peut donc traiter en une seule fois et calculer les deux scores.