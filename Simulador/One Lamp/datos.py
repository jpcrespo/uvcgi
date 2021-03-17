#En este archivo contiene la información técnica de todos los 
#tubos fluorescentes del mercado.

import numpy as np

lamparas = {'782H10' : ['AU', 2.8, 1, 22.2, 1.58, 0.79, 110 ,254, 28, 'LP'],
'782H20':['AU', 5.5, 1, 47.6, 1.58, 0.79, 236, 233, 52 ,'MP'],
'782H30' : ['AU', 5.2, 1 ,73, 1.58, 0.79, 362, 144, 46, 'MP']}

#Referencia se guardar con la siguiente disposicion
#LAMP  Mfr. Output  # of  Arclength  Dia. Radius Area  Surface I  Rating  Type
#      Ref.  UV W   coils    cm      cm    cm     cm2    W/m2     μW/cm2  MP/LP



#parametros de la lampara
radio=1.21             #en cm
long_lamp=81.5        #en cm

intensidad_sup=110        #en microW/cm2


#Inicialmente se necesita crear un espacio vectorial 
#con las coordenadas de un ambiente.

ladox=123
ladoy=321
ladoz=159

#Posiciones por extremales de cada lampara 
#Posicion inicial
lampx1=np.array([50])
lampy1=np.array([0])
lampz1=np.array([50])

#posicion final
lampx2=np.array([50])
lampy2=np.array([82])
lampz2=np.array([50])


x2=lampx2-lampx1
y2=lampy2-lampy1
z2=lampz2-lampz1

p2=x2*x2+y2*y2+z2*z2

