# Day 16

Du _parsing_ aujourd'hui. Un très bel exemple de POO avec héritage (simple, c'est juste pour pouvoir spécialiser quelques méthodes)

En gros on a un objet `Packet` qui fondamentalement est une suite de bits, à considérer en groupes divers pour former des informations diverses.

Ce paquet est donc constitué :

- d'une série de bits
- d'une _version_ qui est un entier codé sur les 3 premiers bits
- d'un _type-id_ qui est un entier codé sur les 3 suivants

Ensuite les infos changent :

- on a les paquets de type `Literal` (_type-id_ à 4) qui sont des valeurs entières
- on a les paquets de type `Operator` (tous les autres _type-id_) qui possède une série de sous paquets. De plus les paquets de type `Operator`  sont de deux sous-types différents suivant comment on considère les bits décrivant les sous paquets.

La difficulté est de bien comprendre le modèle pour faire le _parsing_ et récupérer les infos. Une fois ça fait les réponses aux versions 1 et 2 sont ultra simples.

- Version 1 : on cherche la somme des numéros de version de tous les paquets 
- Version 2 : on se donne une liste de fonctions (qui dépendent du numéro de version) et on cherche à évaluer le paquet en appliquant la bonne fonction à la liste des évaluations de sous paquets.
