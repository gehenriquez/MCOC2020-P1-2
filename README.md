# MCOC2020-P1-2
![Entrega 1](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%201/Balistica.png)


# Entrega 2
Para encontrar la velocidad vt de modo que el satelite orbite sin caer de vuelta dentro de la atmosfera se utilizaron los graficos entregados por el programa. Primero se determino que vt se encontraba entre 22000 km/h y 28000 km/h, debido a los siguientes graficos. Estos graficos muestran la distancia al centro de la tierra del satélite vs. el tiempo, indicando la superficie de la tierra y la atmósfera como una línea de distancia constante.

Para 22000 km/h:

![Entrega 2](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%202/orbitas22000.png)
![Entrega 2](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%202/orbitaszoom22000.png)

Para 28000 km/h:

![Entrega 2](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%202/orbitas28000.png)
![Entrega 2](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%202/orbitaszoom28000.png)
 
 Al comparar se aprecia que con 22000 km/h la orbita se abre hacia un lado y con 28000 km/h se cierra (o abre hacia el otro lado), entonces se fueron probando valores entre 22000 y 28000 y viendo de que lado faltaba aumentar o disminuir. Partiendo por 25000, 25500, 25150, 25250, 25166, 25200, 2188 y 25175 obteniendo un resultado satisfactorio. Para alcanzar este nivel de precisión se realizo zoom a los graficos, ya que a simple vista no se observa bien en todos los casos hacia donde corresponde avanzar. 
 
Para 25000 km/h:

![Entrega 2](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%202/orbitas25000.png)
![Entrega 2](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%202/orbitaszoom25000.png)

Para 25500 km/h:

![Entrega 2](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%202/orbitas25500.png)
![Entrega 2](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%202/orbitaszoom25500.png)

Para vt = 25175 km/h:

![Entrega 2](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%202/orbitas25175.png)
![Entrega 2](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%202/orbitaszoom25175.png)

Además se adjunta los graficos x(t), y(t), z(t) para dos orbitas completas.
![Entrega 2](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%202/graficos.png)

# Entrega 3

En esta entrega hice dos archivos, prediccion_edm_basica.py y prediccion_edm_basica.1.py, esto debido a que inicialmente me dio valores muy altos de diferencia entre la posicion predicha y la real. 
El primero lo hice utilizando como base el archivo de la entrega 2, y el segundo lo hice utilizando lo mostrado por el ayudante. Los resultados obtenidos son de 52258192.43006318 metros para el archivo principal (prediccion_edm_basica.py) y de 1217117708.7218955 metros para el archivo con base en la ayudantia (prediccion_edm_basica.1.py).

# Entrega 4

En el grafico se puede ver que la funcion odeint es una buena aproximacion de la real, ya que esta tiene divisiones automaticamente por la forma como esta construida. En cambio, la función eulerint de pende de la cantidad de particiones o subdivisiones que se hagan para tener una mejor aproximación. Se observa en el grafico que a mayor cantidad de subdivisiones, eo resultado es ams cercano a la funcion real. Con un t = np.linspace(0, 4., 100), se va a tener un odeint de 100 particiones y por lo tanto con un eulerint de 100 subdivisiones se alcanza un resultado suficientemente cercano al real.

![Entrega 4](https://github.com/gehenriquez/MCOC2020-P1-2/blob/main/Entrega%204/Entrega4.png)

# Entrega 5

La solucion de eulerint demora 0.4129541999999997 segundos
La solucion de odeint demora 0.14667249999999932 segundos
La solucion de odeint difiere en 19678.69  KM de la solucion eulerint al final del tiempo
La solucion de eulerint_J2_J3 demora 0.613205899999997 segundos
La solucion de odeint_J2_J3 demora 0.06577210000000377 segundos
La solucion de odeint_J2_J3 difiere en 1161405342508.27  KM de la solucion eulerint al final del tiempo
La Parte 4 demora 44.008612600000006 segundos en correr
Todo el archivo demora 96.2102592 segundos en correr (sin la parte 3)


