#coding:utf-8

import numpy as np

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

#on génère aléatoirement N individus avec une dimension d (d RSUs)
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

def critereArret():
	end = False
	return end

#une fonction pour copier en profondeur une population
def popCopy(P):
	P_copy = []
	if len(P)>0:
		l = len(P[0])
		for i in range(len(P)):
			P_copy.append([])
			for j in range(len(P[0])):
				P_copy[i].append(P[i][j])
	return P_copy

#notre méta-heuristique
def VBO():
	c1, c2 = 1.5, 1.25 #recommanded 
	N = 100 # population size
	d = 10 # num of RSUs
	alpha = 0.1 # proportion class A
	Na = int(alpha*N) #nb d'individus dans la classe A
	P = generateRandomPop(N,d)
	next_P = [[x for x in particle] for particle in P] # Prochaine génération
	L = [computeLatency(x) for x in P]
	next_L = [x for x in L]
	indexSort = sorted(range(len(L)), key=lambda k: L[k])
	cou = 100
	while not critereArret() and cou>0:
		cou -= 1

		# on repère le meilleur et le pire individu
		Xbest = P[indexSort[0]] 
		Xworst = P[indexSort[-1]]

		# on fait évoluer les individus de la classe A
		for i in range(Na):
			ra = (np.random.rand(d) > 0.5).astype(int)
			next_P[indexSort[i]] = softmax(P[indexSort[i]] + ra * ([a-b for (a,b) in zip(Xbest,Xworst)]))

		# puis ceux de la classe B
		for i in range(Na,N):
			i_peer = np.random.randint(N)
			while (i_peer == i):
				i_peer = np.random.randint(N)
			rb = (np.random.rand(d) > 0.5).astype(int)
			latency_peer = L[indexSort[i_peer]]
			latency_X = L[indexSort[i]]
			if latency_X < latency_peer:
				next_P[indexSort[i]] = softmax(P[indexSort[i]] + c1 * rb * ([a-b for (a,b) in zip(Xbest,P[indexSort[i_peer]])]))
			elif latency_X > latency_peer:
				next_P[indexSort[i]] = softmax(P[indexSort[i]] + c2 * rb * ([a-b for (a,b) in zip(P[indexSort[i_peer]],P[indexSort[i]])]))
			else:
				next_P[indexSort[i]] = softmax(2 * rb * P[indexSort[i]])

		# on recalcule les fonctions objectifs pur chaque nouvel individu
		next_L = [computeLatency(x) for x in next_P]
		for i in range(N):
			if next_L[i] < L[i]:
				P[i] = [x for x in next_P[i]]
				L[i] = next_L[i]
		indexSort = sorted(range(len(L)), key=lambda k: L[k])

	# si on a atteint le critère d'arrêt, on renvoie le meilleur individu et sa valeur
	return P[indexSort[0]], L[indexSort[0]]

#print(VBO())

# objList : la liste des objectifs à minimiser
# i_1, i_2 : les deux individus, donc deux vecteurs avec des valeurs entre 0 et 1 
def dominate_aux(objList, i_1, i_2):
	dom = True
	for obj in objList:
		dom = dom and (obj(i_1) < obj(i_2))
	return dom

# Pour une population donnée, on considère O un tableau regroupant les valeurs de chaque individu pour chaque fonction objectif
# Soient idx_x_1 et idx_x_2, les deux indices de deux individus de la population. On veut savoir si idx_x_1 domine idx_x_2.
def dominate(O, idx_x_1, idx_x_2):
	dom = True
	for i in range(len(O)):
		# Vrai si l'individu idx_x_1 domine l'individu idx_x_2 selon l'objectif i, on veut minimiser l'objectif
		dom = dom and (O[i][idx_x_1] < O[i][idx_x_2])
	return dom

# une fonction qui retourne la population triée par ordre de dominance, des individus non dominés entre eux appartiennent au même groupe au sein de la population.
# X une population, objList la liste des objectifs à optimiser
def nonDominatedSet(X, objList):

	# on calcule les valeurs de chaque individu selon tous les objectifs 
	O = []
	for i in range(len(objList)):
		O.append([objList[i](x) for x in X])

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
			if len(list(filter(lambda x: dominate(O, x, i), range(len(P)))))<= 0:
				# on le rajoute dans le groupe F_i
				F_i.append(i)

		# puis on le retire de la population 
		for x in F_i[::-1]:
			F.append(P.pop(x))
			for i in range(len(O)):
				O[i].pop(x)

		# on rajoute ce groupe à la suite de la liste S qui contient les groupes d'invidus classés par ordre de dominance
		S.append(F)
	return S
	"""
	C = [len(x) for x in S]
	return C
	"""

#print(nonDominatedSet(generateRandomPop(50,10),[computeLatency]))

#notre méta-heuristique customizée pour plusieurs objectifs
def MOVBO():

	objList = [computeLatency]
	c1, c2 = 1.5, 1.25 #recommanded 
	N = 100 # population size
	d = 10 # num of RSUs
	alpha = 0.1 # proportion class A
	Na = int(alpha*N) #nb d'individus dans la classe A
	Alea_P = generateRandomPop(N,d)
	P = sum(nonDominatedSet(Alea_P,objList),[]) # on trie la population par groupes de dominance puis on "flatten" les groupes pour récupérer les individus de la classe A.
	O = []
	for i in range(len(objList)):
		O.append([objList[i](x) for x in P])
	next_P = [[x for x in particle] for particle in P] # Prochaine génération

	cou = 100
	while not critereArret() and cou>0:
		cou -= 1

		# on repère le meilleur et le pire individu
		Xbest = P[0] 
		Xworst = P[-1]

		# on fait évoluer les individus de la classe A
		for i in range(Na):
			ra = (np.random.rand(d) > 0.5).astype(int)
			next_P[i] = softmax(P[i] + ra * ([a-b for (a,b) in zip(Xbest,Xworst)]))

		# puis ceux de la classe B
		for i in range(Na,N):
			i_peer = np.random.randint(N)
			while (i_peer == i):
				i_peer = np.random.randint(N)
			rb = (np.random.rand(d) > 0.5).astype(int)

			# on regarde les rapports de dominance entre le i-ème et le i_peer-ème individu
			i_dom_i_peer = dominate(O, i, i_peer)
			i_peer_dom_i = dominate(O, i_peer, i)
			if i_dom_i_peer:
				next_P[i] = softmax(P[i] + c1 * rb * ([a-b for (a,b) in zip(Xbest,P[i_peer])]))
			elif i_peer_dom_i:
				next_P[i] = softmax(P[i] + c2 * rb * ([a-b for (a,b) in zip(P[i_peer],P[i])]))
			else:
				next_P[i] = softmax(2 * rb * P[i])

		# on recalcule les fonctions objectifs pour chaque nouvel individu de next_P
		next_O = []
		for i in range(len(objList)):
			next_O.append([objList[i](x) for x in next_P])

		# on applique les maj de chaque individu uniquement sa nouvelle position domine l'ancienne
		for i in range(N):
			if dominate_aux(objList, P[i], next_P[i]):
				P[i] = [x for x in next_P[i]]
				for j in range(len(objList)):
					O[j][i] = next_O[j][i]

		# et on trie de nouveau la population par ordre de dominance
		P = sum(nonDominatedSet(P,objList),[])
		for i in range(len(objList)):
			O.append([objList[i](x) for x in P])

	# si on a atteint le critère d'arrêt, on renvoie le meilleur individu et sa valeur
	return P[0]

print(MOVBO())