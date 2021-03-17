import  datosn 
from datosn import *

import setup
from setup import *

import graficador 
from graficador import *

import calcuv
from calcuv import *


intensidad=[]
#el espacio de coordenadas es el mismo para el arreglo


coord=crear_coord()

#se calculan las distancias para cada lampara 

#Lampara 1

#distancias(coord,lampx1=lampx1,lampy1=lampy2,lampz1=lampz1,lampx2=lampx1,lampy2=lampy2,lampz2=lampz1,p2=p2)
distancia, dist_axis=distancias(coord,lampx1[0],lampy1[0],lampz1[0],lampx2[0],lampy2[0],lampz2[0],p2[0],x2[0],y2[0],z2[0])
intensidad.append(Calcular_intensidad(distancia,dist_axis))

#Lampara 2
distancia1, dist_axis1=distancias(coord,lampx1[1],lampy1[1],lampz1[1],lampx2[1],lampy2[1],lampz2[1],p2[1],x2[1],y2[1],z2[1])
intensidad.append(Calcular_intensidad(distancia1,dist_axis1))

intensidad=np.array(intensidad)


TF=[]

for i in range(len(intensidad[0])):
	a=0
	for j in range(len(intensidad)):
		k=a+intensidad[j][i]
		a=k
	TF.append(a)


totalF=100*np.array(TF)/np.max(TF)

#esta intensidad no ha sido normalizada, y para poder apreciarla bien graficament
#se necesita trabajarla.

pl_frontal(100,intensidad[0],coord)
pl_frontal(100,intensidad[1],coord)
pl_frontal(100,totalF,coord)

t1,t2=time_kill(totalF)

ks=KillRate(1200,totalF)
ks1=KillRate(1200,intensidad[1])
pl_uvfront(100,ks,coord)
pl_uvfront(100,ks1,coord) 

