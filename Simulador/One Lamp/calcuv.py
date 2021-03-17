#Esta seccion calcula a partir de una matriz 3d de coordenadas
#y una matriz de intensidades asociadas a cada punto
#un computo para el tiempo especifico.

"""
Para lo cual usa el valor mas lejano (es decir donde menos intensidad
espacial se percibe) y calcular su tiempo de esterilización al 99.9%
para el covid. Puede ser cualquier virus, bacteria, hongo o espora 
que se especifica en datos.py	

Para el computo del tiempo necesario para esterilizar el covid se 
usan dos modos:
BoosT: 			Usamos el tiempo teórico de eliminación al 99.9% seguro.
Total: 		Usamos el tiempo necesario para ceder una energía de 1 J
	aconsejada por agencias como el CDC. Este nivel de esterilización es
	total para uso médico.

"""


import numpy as np  

import datos 
from datos import *

import setup
from setup import *

#Para explorar los resultados, es conveniente recuperar el vector de datos DirectField para
#cada plano de intersección
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt



def time_kill(TotalField):
	Zt=np.mean(TotalField)
	target=99.9
	s=1-(target/100)
#constante específica del virus m2/J
#k = 0.37700/100  #factor correccion para llevarlo a cm2/microJ sarscov1
#k=0.0008528 #promedio autores 2020
	kv=0.0005522 #Inagaki 2020 
#La intensidad se encuentra en microW/cm2
#dimensionalmente el tiempo esta en segundos

	tmin=np.log(s)/(-1*kv*Zt)	

	print('tiempo para D99.9= '+str(round(tmin,3))+' segundos ' + 'BoosT')


#el valor experimental 1 J/cm2
	exp=1*(10**6) #factor de corrección para llevarlo a microJ/cm2
#La intensidad se encuentra en microW/cm2

	t_emin=exp/Zt

	print('tiempo para D99.9= '+str(round(t_emin,3))+' segundos ' + 'Total')
	return tmin, t_emin


def KillRate(tiempo,TotalField):
	kV = 0.0005522   #constante virus cm2/microW.s
#Calculamos el tiempo que llevaria matar al 99% del virus con la irradiación promedio 
	#print('Calculando Matriz 3D Rate Kill')
	krs=100*(1-np.exp(-1*kV*TotalField*tiempo))
	return krs



def pl_uvfront(planox,DirectField,coord,ladox=ladox,ladoy=ladoy,ladoz=ladoz):
#Vista Frontal
#En la vista frontal X es un valor constante
#Z ocupa el valor de x y Y continúa siendo y
#	print('Plano Frontal, Corte en X: ')
#	planox=50  #int(input()) # Corte en el medio
	ax=np.where(coord[0,:,0]==planox,True,False)
	tt=DirectField[ax]

	levels = np.linspace(np.min(tt),np.max(tt),5,endpoint=True).ravel()


	X=np.arange(0,ladoz+1,1)
	Y=np.arange(0,ladoy+1,1)
	Z=tt.reshape((ladoy+1,ladoz+1))

	a=plt.figure()
	h = plt.contourf(X,Y,Z,levels,alpha=0.8, cmap=plt.cm.winter)
	plt.colorbar()

	plt.title('Proyección en plano Frontal \n corte en coordenada x: %d'%planox,fontsize=15,color="blue")
	plt.grid()


	contours = plt.contour(X, Y, Z, levels, colors='black')
	plt.clabel(contours, inline=True, fontsize=8)
	plt.show()






def pl_uvsup(planoy,DirectField,coord,ladox=ladox,ladoy=ladoy,ladoz=ladoz):
	ay=np.where(coord[0,:,1]==planoy,True,False)
	tt=DirectField[ay]

	levels = np.linspace(np.min(tt),np.max(tt),5,endpoint=True).ravel()




	X=np.arange(0,ladoz+1,1)
	Y=np.arange(0,ladox+1,1)
	Z=tt.reshape((ladox+1,ladoz+1))

	a=plt.figure()
	h = plt.contourf(X,Y,Z,levels,alpha=0.8, cmap=plt.cm.winter)
	plt.colorbar()

	plt.title('Proyección en plano Superior \n corte en coordenada y: %d'%planoy,fontsize=15,color="blue")
	plt.grid()


	contours = plt.contour(X, Y, Z, levels, colors='black')
	plt.clabel(contours, inline=True, fontsize=8)
	plt.show()



def pl_uvlat(planoz,DirectField,coord,ladox=ladox,ladoy=ladoy,ladoz=ladoz):

	az=np.where(coord[0,:,2]==planoz,True,False)
	tt=DirectField[az]
	
	ord=[]
	cd=coord[0,:,:]
	for  k in range(ladoy+1):
	    for n,(i,j,q) in enumerate(cd[az]):
	        if(j==k):
	            ord.append(n)
	orden=tt[ord]

	levels = np.linspace(np.min(orden),np.max(orden),15,endpoint=True).ravel()

	X=np.arange(0,ladox+1,1)
	Y=np.arange(0,ladoy+1,1)
	Z=orden.reshape((ladoy+1,ladox+1))

	a=plt.figure()
	h = plt.contourf(X,Y,Z,levels,alpha=0.8, cmap=plt.cm.winter)

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
	t1,t2=time_kill(intensidad)
	
	#El tiempo necesario que estima es de 2000 seg. aprox

	#Con este tiempo, se puede ir cambiando a requerimiento.
	ks=KillRate(20000,intensidad)

	pl_uvsup(40,ks,coord)
	pl_uvfront(100,ks,coord)
	pl_uvlat(50,ks,coord)
	