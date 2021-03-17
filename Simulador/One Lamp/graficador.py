#Para explorar los resultados, es conveniente recuperar el vector de datos DirectField para
#cada plano de intersección
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np

import datos 
from datos import *

import setup
from setup import *

 

def pl_frontal(planox,DirectField,coord,ladox=ladox,ladoy=ladoy,ladoz=ladoz):

#Vista Frontal
#En la vista frontal X es un valor constante
#Z ocupa el valor de x y Y continúa siendo y
#	print('Plano Frontal, Corte en X: ')
#	planox=50  #int(input()) # Corte en el medio

	ax=np.where(coord[0,:,0]==planox,True,False)
	tt=DirectField[ax]

	levels = np.logspace(-4,2,5,endpoint=True).ravel()

	X=np.arange(0,ladoz+1,1)
	Y=np.arange(0,ladoy+1,1)
	Z=tt.reshape((ladoy+1,ladoz+1))

	a=plt.figure()

	h = plt.contourf(X,Y,Z,levels,alpha=0.8, cmap=plt.cm.afmhot)

	plt.title('Proyección en plano Frontal \n corte en coordenada x: %d'%planox,fontsize=15,color="blue")
	plt.grid()
	plt.colorbar()
	contours = plt.contour(X, Y, Z, levels, colors='black')
	plt.clabel(contours, inline=True, fontsize=8)
	plt.show()



def pl_superior(planoy,DirectField,coord,ladox=ladox,ladoy=ladoy,ladoz=ladoz):
	ay=np.where(coord[0,:,1]==planoy,True,False)
	tt=DirectField[ay]

	levels = np.logspace(-3,1.5,5,endpoint=True).ravel()

	X=np.arange(0,ladoz+1,1)
	Y=np.arange(0,ladox+1,1)
	Z=tt.reshape((ladox+1,ladoz+1))

	a=plt.figure()
	h = plt.contourf(X,Y,Z,levels,alpha=0.8, cmap=plt.cm.afmhot)

	plt.title('Proyección en plano Superior \n corte en coordenada y: %d'%planoy,fontsize=15,color="blue")
	plt.grid()
	plt.colorbar()
	contours = plt.contour(X, Y, Z, levels, colors='black')
	plt.clabel(contours, inline=True, fontsize=8)
	plt.show()



def pl_lateral(planoz,DirectField,coord,ladox=ladox,ladoy=ladoy,ladoz=ladoz):

	az=np.where(coord[0,:,2]==planoz,True,False)
	tt=DirectField[az]
	ord=[]
	cd=coord[0,:,:]
	for  k in range(ladoy+1):
		for n,(i,j,q) in enumerate(cd[az]):
			if(j==k):
				ord.append(n)
	orden=tt[ord]

	levels = np.logspace(-3,2,5,endpoint=True).ravel()

	X=np.arange(0,ladox+1,1)
	Y=np.arange(0,ladoy+1,1)
	Z=orden.reshape((ladoy+1,ladox+1))

	a=plt.figure()
	h = plt.contourf(X,Y,Z,levels,alpha=0.8, cmap=plt.cm.afmhot)
	plt.colorbar()

	plt.title('Proyección en plano Lateral \n corte en coordenada z: %d'%planoz,fontsize=15,color="blue")
	plt.grid()
	contours = plt.contour(X, Y, Z, levels, colors='black')
	plt.clabel(contours, inline=True, fontsize=8)
	plt.show()


if __name__=='__main__':

	coord=crear_coord()
	distancia, dist_axis=distancias(coord)
	intensidad=Calcular_intensidad(distancia,dist_axis)
#La función retorna del core de intensidad, un vector con 
#el calculo de intensidades. Para poder apreciar una buena 
#representación de la intensidad primero la normalizamos.

	intensidadN= np.divide(100*intensidad,np.max(intensidad))

	
	pl_superior(50,intensidadN,coord)
	#pl_lateral(100,intensidadN,coord)
	pl_frontal(50,intensidadN,coord)


