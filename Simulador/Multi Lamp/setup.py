
import numpy as np
import datosn
from datosn import *

import numexpr as ne
ne.set_num_threads(8) 



def crear_coord(ladox=ladox,ladoy=ladoy,ladoz=ladoz):
	ix = np.arange(0, ladox+1, 1).astype(np.float16)   # se construye una base vectorial
	iy = np.arange(0, ladoy+1, 1).astype(np.float16)   # ix, iy, iz  
	iz = np.arange(0, ladoz+1, 1).astype(np.float16)   # y se escala los puntos de analisis de los ejes

	xx,yy,zz = np.meshgrid(ix, iy, iz, indexing='ij')
#la funcion meshgrid construye vectores que contiene
#las combinaciones de los puntos separadamente

#Para poder ejecutar el calculo geometrico por cada punto
# i,j,k reordenamos la combinación de meshgrid en 
#un solo vector 

	x=xx.ravel()
	y=yy.ravel()
	z=zz.ravel()
	coord=np.dstack((x,y,z))  #se crea el espacio vectorial de las coordenadas
	return coord 

def distancias(coord,lampx1,lampy1,lampz1,lampx2,lampy2,lampz2,p2,x2,y2,z2):
	#esta función genera el calculo (para cada punto de una matriz 3D de entrada)
	#de la distancia al eje de la lampara y la distancia dist_axis 
	#al extremo mas alejado de la lámpara.
	R=np.add(coord,-np.dstack((lampx1,lampy1,lampz1)))
	p1=np.sum(R*R,axis=2)
	aux= np.sum(R*np.dstack((x2,y2,z2)),axis=2, dtype = float) 
	aux1= np.sqrt((p1*p2), dtype = float)
	aux=aux[0,:]
	aux1=aux1[0,:]
	aux_1=ne.evaluate("where(aux1==0,0.0001,aux1)")  
	tt= np.true_divide(aux, aux_1)

	dotprod=ne.evaluate("arccos(tt)")
	dist=ne.evaluate('abs(sin(dotprod))*sqrt(p1)')
	distancia=dist[0,:]

	posit1=ne.evaluate("where(p1*p2>0, abs(cos(dotprod))*sqrt(p1), radio+0.0001)") 
	R1=np.add(coord,-np.dstack((lampx2,lampy2,lampz2)))
	p3=np.sum(R1*R1,axis=2)
	aux1= np.sum(R1*np.dstack((x2,y2,z2)),axis=2, dtype = float)
	aux2= np.sqrt(p3*p2, dtype = float)
	aux1=aux1[0,:]
	aux2=aux2[0,:]
	aux_2=ne.evaluate("where(aux2==0,0.0001,aux2)")  
	tt1 = np.true_divide(aux1, aux_2)
	dotprod1=ne.evaluate("arccos(tt1)")
	posit2=ne.evaluate("where(p3*p2>0,abs(cos(dotprod1))*sqrt(p3),radio+0.0001)")    
	dist_axis = np.maximum(posit1,posit2)
	return distancia,dist_axis


def Calcular_intensidad(distancia,dist_axis):
	h=ne.evaluate('where(distancia>radio, distancia/radio,(radio+0.000001)/radio)')
	H=ne.evaluate("where(h==1,h+0.000001,h)")
 
	l=np.true_divide(dist_axis,radio)
	L=ne.evaluate("where(l==0,l+0.000001,l)")

	X=ne.evaluate("(1+H)*(1+H)+(L*L)")
	Y=ne.evaluate("(1-H)*(1-H)+(L*L)")
	a=ne.evaluate("arctan(L/(sqrt(H*H-1)))/L")
         
	_b=ne.evaluate("X-(2*H)")
	_b1=ne.evaluate("arctan(sqrt((X/Y)*(H-1)/(H+1)))/sqrt(X*Y)")
	b=ne.evaluate("_b*_b1")
	c=ne.evaluate("arctan(sqrt((H-1)/(H+1)))")

	VF1=ne.evaluate('(L*(a+b-c))/((3.1416)*H)')
   
	lo_l=np.true_divide(long_lamp-dist_axis,radio)

	lo_L=ne.evaluate("where(lo_l==0,lo_l+0.000001,lo_l)")
	lo_X=ne.evaluate("(1+H)*(1+H)+(lo_L*lo_L)")
	lo_Y=ne.evaluate("(1-H)*(1-H)+(lo_L*lo_L)")
	lo_a=ne.evaluate("arctan(lo_L/(sqrt(H*H-1)))/lo_L")

	lo__b=ne.evaluate("lo_X-2*H")
	lo__b1=ne.evaluate("arctan(sqrt((lo_X/lo_Y)*(H-1)/(H+1)))/sqrt(lo_X*lo_Y)")
	lo_b=ne.evaluate("lo__b*lo__b1")
	lo_c=ne.evaluate("arctan(sqrt((H-1)/(H+1)))")
	VF2=ne.evaluate('(lo_L*(lo_a+lo_b-lo_c))/((3.1416)*H)')
    
	vva=ne.evaluate('(VF1+VF2)*intensidad_sup')
    
	bey_l=np.true_divide(dist_axis,radio)
	bey_L=ne.evaluate("where(bey_l==0,bey_l+0.000001,bey_l)")
	bey_X=ne.evaluate("(1+H)*(1+H)+(bey_L*bey_L)")
	bey_Y=ne.evaluate("(1-H)*(1-H)+(bey_L*bey_L)")
	bey_a=ne.evaluate("arctan(bey_L/(sqrt(H*H-1)))/bey_L")

	bey__b=ne.evaluate("bey_X-(2*H)")
	bey__b1=ne.evaluate("arctan(sqrt((bey_X/bey_Y)*(H-1)/(H+1)))/sqrt(bey_X*bey_Y)")
	bey_b=ne.evaluate("bey__b*bey__b1")
	bey_c=ne.evaluate("arctan(sqrt((H-1)/(H+1)))")

	VF3=ne.evaluate('(bey_L*(bey_a+bey_b-bey_c))/((3.1416)*H)')
    
	bey_dbl=np.true_divide(dist_axis-long_lamp,radio)
	bey_dbL=ne.evaluate("where(bey_dbl==0,bey_dbl+0.000001,bey_dbl)")

	bey_dbX=ne.evaluate("(1+H)*(1+H)+(bey_dbL*bey_dbL)")
	bey_dbY=ne.evaluate("(1-H)*(1-H)+(bey_dbL*bey_dbL)")
	bey_dba=ne.evaluate("arctan(bey_dbL/(sqrt(H*H-1)))/bey_dbL")

	bey__dbb=ne.evaluate("bey_dbX-(2*H)")
	bey__dbb1=ne.evaluate("arctan(sqrt((bey_dbX/bey_dbY)*(H-1)/(H+1)))/sqrt(bey_dbX*bey_dbY)")
	bey_dbb=ne.evaluate("bey__dbb*bey__dbb1")
	bey_dbc=ne.evaluate("arctan(sqrt((H-1)/(H+1)))")

	VF4=ne.evaluate('(bey_dbL*(bey_dba+bey_dbb-bey_dbc))/((3.1416)*H)')
    
	vvb=ne.evaluate('(VF3-VF4)*intensidad_sup')
    
	DirectField1=ne.evaluate("where(dist_axis>long_lamp,vva ,vvb)")
	DirectField1_=np.abs(DirectField1[0,:])
	#DirectField=100*np.divide(np.abs(DirectField1[0,:]),max(DirectField1[0,:]))   #Encontrar valores relativos
	return DirectField1_ 



if __name__=='__main__':
	coord=crear_coord()
	distancia, dist_axis=distancias(coord,lampx1[0],lampy1[0],lampz1[0],lampx2[0],lampy2[0],lampz2[0],p2[0],x2[0],y2[0],z2[0])
	intensidad=Calcular_intensidad(distancia,dist_axis)
	print(np.mean(intensidad))


