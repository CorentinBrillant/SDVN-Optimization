#coding:utf-8

from fctObjectives import *
from datetime import datetime
import numpy as np

mapWidth = 7000
mapHeight= 6000
nbVoitures = 1000

#Initialisation des RSUs
RSUs = []
for i in range(5):
	for j in range(6):
		if i%2==0:
			RSUs.append(Rsu(600+j*1100,600+i*1100,datetime.now(),0))
		else:
			if j not in [1,3,4]:
				RSUs.append(Rsu(600+j*1100,600+i*1100,datetime.now(),0))

# Initialisation des voitures    
voitures_tmp = []
for i in range(nbVoitures):
    voitures_tmp.append(Voiture(datetime.now(),randrange(14)))

# attribution des RSUs aux véhicules
for v in voitures_tmp:
	v.attrClosestRsu(RSUs)

# on ne prend en compte que les véhicules à portée d'un RSU
voitures = []
for v in voitures_tmp:
	if v.rsuAtr in range(24):
		voitures.append(v)

# affectation des RSUs non contrôleurs aux RSUs contrôleurs
def choseControllerForEachRsu():
	D = calcDists(RSUs)
	RSU_Controller = [rsu for rsu in RSUs if rsu.isCont]
	for rsu in RSUs:
		if rsu.isCont == 0:
			d_min = mapWidth*mapHeight
			i_min = rsu.id
			for c in RSU_Controller:
				if D[rsu.id,c.id] < d_min:
					i_min = c.id
			if i_min != rsu.id:
				rsu.cAtr = i_min

# à partir d'un individu de notre population on configure l'implémentation objet du SDVN
def particleToObjects(vect):

	#on vérifie que la particle a autant de valeurs qu'il y a de RSUs
	assert len(vect)==24
	for i in range(len(RSUs)):
		RSUs[i].isCont = vect[i]

	# on affecte les RSUs non contrôleurs aux RSUs contrôleurs
	choseControllerForEachRsu()

	# on calcule les 4 objectifs 
	values = []
	values.append(clockSync(RSUs, voitures))
	values.append(nbControleurs(RSUs))
	values.append(latency(RSUs, voitures))
	values.append(equiCharge(RSUs, voitures))

	return values


#print(particleToObjects((np.random.rand(24) > 0.5).astype(int)))