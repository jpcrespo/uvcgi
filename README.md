# uvcgi
 Calculo de intensidades de un sistema uvcgi



# La simulación contiene dos partes:

One Lamp
Multi Lamp

Se configuran de igual forma:

- Archivo:
datos.py (One Lamp)
datosn.py (Multi Lamp)

En este apartado se tiene información de las caracteristicas de fabrica de distintas lamparas precargdas, asi como las constantes de evaluacion por patogeno: Virus, Bacteria, Hongo. 
Para calcular el tiempo de esterilización especifico según necesidad.


Se deben declarar las dimensiones  de la habitación a esterilizar, asi como la posición y coordenadas de cada lampara. 


El archivo: setup.py

contiene el core de calculo de intensidad. 


El archivo:
gradicador.py

contiene el core
de recuperación de datos, ordanmiento y representación gráfica por proyección de planos: frontal, superior y lateral.


El archivo calcuv.py

Contiene el core de
recuperación de datos, ordenamiento y representación gráfica por proyección de planos DE LA MATRIZ DEL RADIO DE ESTERILIZACIÓN:
Se supone todo el ambien contaminado, evalua según el  tiempo calculado o estimado la performance del sistema. 
Muestra un mapa al 100% de esterilización al 99,9%


El archivo:

analisismulti.py

muestra como aplicar el core para calcular
la intensidad y el killrate de toda la matriz
3d para arreglos con N lamparas. 

En el archivo datosn.py se almacena toda la información de las distintas lamparas, asi como su disposición geometrica.









