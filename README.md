# Advent Of Code 2024

Cette année ça va être "quand j'ai le temps :smile:"

### Progression

- jour 06 : ✅ ✅ j'ai galéré sur la P2... je ne comprends pas l'erreur de mon code initial. Le raisonnement est le suivant : j'ai un garde dans un labyrinthe. Avant de faire avancer le garde, je regarde si la case devant est libre, auquel cas je crée une copie du labyrinthe (je sais c'est violent) et un _fantôme_ a la position courante, même direction sur le garde. Puis j'envoie le _fantôme_ partrouiller. La patrouille s'arrête lorsque le _fantôme_ sort du labyrinthe ou qu'on repasse par le même point, avec la même direction (une boucle donc). Si on a détecté une boucle on garde en mémoire la position où on a construit le mur. Et bien ça ne marche pas, il y a trop de boucle détectées. Il faut placer le _fantôme_ à la position de départ et non à la position courante.
- jour 05 : ✅ ✅ pas sûr que ma solution soit très élégante :cry:
- jour 04 : ✅ ✅ sympa :smile: ma méthode : mettre tous les `MAS` (position et direction) dan sun ensemble, puis compter une croix pour chaque `MAS` présent avec sa symétrie horizontale ou verticale
- jour 03 : ✅ ✅ ça commence avec les _regex_ :smile:
- jour 02 : ✅ ✅
- jour 01 : ✅ ✅
