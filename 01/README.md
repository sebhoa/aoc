# Day 01

Dans ces deux versions j'ai essayé de lire les données ligne par ligne sans tout charger. 

Puis d'avancer pas à pas, comme dans la version itérative de Fibonacci :

```    
171 <- a
173 <- b  <- a
174       <- b <- a
163            <- b
161
157
```

La première fois `a == b` donc le test est faux et on ne compte pas +1 mais attention la généralisation de cette méthode au cas de 3 variables d'un coup nécessite une petite astuce pour le départ. Le principe ensuite reste le même

```
171 <- a
173 <- b  <- x <- a
174 <- c  <- y <- b <- x 
163       <- z <- c <- y
161                 <- z
157
```
