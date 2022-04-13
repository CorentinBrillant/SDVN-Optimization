import numpy as np
from statistics import mean
from random import randrange
import random
from fctObjectives import *
from Results import *

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def generateRandomPop(N,d):
	P = []
	for i in range(N):
		P.append(np.random.rand(d))
	return P

def computeLatency(X):
	c=0
	for x in X:
		c += x
	return c


# on dicretise le vecteur de flottant en vecteur de 0 ou 1
def discretise(vect):
	return [1 if x > 0.5 else 0 for x in vect ]

def critereArret():
	end = False
	return end

def popCopy(P):
	P_copy = []
	if len(P)>0:
		l = len(P[0])
		for i in range(len(P)):
			P_copy.append([])
			for j in range(len(P[0])):
				P_copy[i].append(P[i][j])
	return P_copy

"""
def TLBO():
    N =100
    d = 24 #nombre de rsu
    alpha = 0.1 # proportion class A
    Na = int(alpha*N)
    P = generateRandomPop(N,d)
    L = [computeLatency(x) for x in P]
    indexSort = sorted(range(len(L)), key=lambda k: L[k])

    cou = 100
    while not critereArret() and cou>0:
        cou=-1
        xm = mean(P)
        Xmean = [xm  for x in P]
        Xbest = P[indexSort[0]]
        r = (np.random.rand(d) > 0.5).astype(int)
        TF = randrange(1)+1
        for i in range(N):
            P_p = P[i] + r * (Xbest - TF*Xmean)
        L_p = [computeLatency(x) for x in P_p]
        for i in range(N):
            if(L_p[i] < L[i]):
                P[i] = P_p[i]
                L[i] = L_p[i]
        r_s = (np.random.rand(d) > 0.5).astype(int)
        for i in range(N):
            Xpeer = random.choice(P)   
            if (L[i]< computeLatency(Xpeer)): #A modifier
                P_p[i] = P[i] + r_s*(P[i] - Xpeer)
            else:
                P_p[i] = P[i] + r_s*(Xpeer - P[i])
        L_p = [computeLatency(x) for x in P_p]
        for i in range(N):
            if (L_p[i] < L[i]):
                P[i] = P_p[i]
    
    optimPlacement = P[indexSort[0]] 
    L = [computeLatency(x) for x in P]
    optimLatency = L[indexSort[0]]
    return (optimPlacement,optimLatency)   """                       
                
# Pour une population donnée, on considère O un tableau regroupant les valeurs de chaque individu pour chaque fonction objectif
# Soient idx_x_1 et idx_x_2, les deux indices de deux individus de la population. On veut savoir si idx_x_1 domine idx_x_2.
def dominate(O_1, O_2):
	dom = True
	for i in range(len(O_1)):
		# Vrai si l'individu idx_x_1 domine l'individu idx_x_2 selon l'objectif i, on veut minimiser l'objectif
		dom = dom and (O_1[i] < O_2[i])
	return dom

# une fonction qui retourne la population triée par ordre de dominance, des individus non dominés entre eux appartiennent au même groupe au sein de la population.
# X une population, O la liste des 4 objectifs pour chaque particule
def nonDominatedSet(X, O):

	# on effectue une copie de la population car on va trier les individus par groupe de dominance
	P = popCopy(X)
	S = []

	while len(P)>0:

		# on crée un ss-groupe de non-dominés entre eux
		F_i = []
		F = []

		#sur l'ensemble des individus 
		for i in range(len(P)):
			#s'il existe des individus non-dominés par aucun autre individu de la population restante
			if len(list(filter(lambda x: dominate(O[x], O[i]), range(len(P)))))<= 0:
				# on le rajoute dans le groupe F_i
				F_i.append(i)

		# puis on le retire de la population 
		for x in F_i[::-1]:
			F.append(P.pop(x))
			O.pop(x)

		# on rajoute ce groupe à la suite de la liste S qui contient les groupes d'invidus classés par ordre de dominance
		S.append(F)
	return S
	"""
	C = [len(x) for x in S]
	return C
	"""

 
def MOTLBO(): 
    N =100
    d = 24 #nombre de rsu
    Alea_P = generateRandomPop(N,d)
    # on calcule les fonctions objectifs pour chaque particule
    O = [particleToObjects(x) for x in Alea_P]

    # on trie la population par groupes de dominance puis on "flatten" les groupes pour récupérer les individus de la classe A.
    P = sum(nonDominatedSet(Alea_P, O),[]) 

    # on calcule les fonctions objectifs pour chaque particule
    O = [particleToObjects(discretise(x)) for x in P]
    
    cou = 500
    P_p = popCopy(P)
    while not critereArret() and cou>0:
        #Teacher Phase
        cou=-1
        
#        On recupere un X en faisant la moyenne et on prend le meilleur X
        Xmean = list(np.mean(P,axis=0))
        Xbest = P[0]
        r = (np.random.rand(d) > 0.5).astype(int)
        
        #facteur d'apprentissage ( Teaching Factor)
        TF = randrange(1)+1
        
        for i in range(N):
            P_p[i] = P[i] + r * ([a - b for a,b in zip(Xbest,TF*Xmean)])

        O_p = [particleToObjects(discretise(x)) for x in P_p]
        for i in range(N):
            if(dominate(O_p[i],O[i])):
                P[i] = P_p[i]
                O[i] = O_p[i]
        r_s = (np.random.rand(d) > 0.5).astype(int)
        
        #Student phase
        for i in range(N):
            i_peer = np.random.randint(N)
            while (i_peer == i):
                i_peer = np.random.randint(N)
            Xpeer = P[i_peer]   
            if (dominate(O[i_peer],O[i])): # A modifier
                P_p[i] = P[i] + r_s*( [a - b for a,b in zip(P[i],Xpeer)])
            else:
                P_p[i] = P[i] + r_s*( [b - a for a,b in zip(P[i],Xpeer)])
                
        O_p = [particleToObjects(discretise(x)) for x in P_p]
        for i in range(N):
            if(dominate(O_p[i],O[i])):
                P[i] = P_p[i]
                O[i] = O_p[i]
    optimPlacement = nonDominatedSet(P,O)
    n = len(optimPlacement[0])
    P = sum(optimPlacement,[])
    optimObjectif = [particleToObjects(discretise(x)) for x in P[:n]]
 
    return ([discretise(x) for x in P],optimObjectif)   


#print(MOTLBO())