#coding:utf-8

import numpy as np

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


def VBO():
	c1, c2 = 1.5, 1.25 #recommanded 
	N = 100 # population size
	d = 10 # num of RSUs
	alpha = 0.1 # proportion class A
	Na = int(alpha*N)
	P = generateRandomPop(N,d)
	next_P = [[x for x in particle] for particle in P]
	L = [computeLatency(x) for x in P]
	next_L = [x for x in L]
	indexSort = sorted(range(len(L)), key=lambda k: L[k])
	cou = 100
	while not critereArret() and cou>0:
		cou -= 1
		Xbest = P[indexSort[0]]
		Xworst = P[indexSort[-1]]
		for i in range(Na):
			ra = (np.random.rand(d) > 0.5).astype(int)
			next_P[indexSort[i]] = softmax(P[indexSort[i]] + ra * ([a-b for (a,b) in zip(Xbest,Xworst)]))
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
		next_L = [computeLatency(x) for x in next_P]
		for i in range(N):
			if next_L[i] < L[i]:
				P[i] = [x for x in next_P[i]]
				L[i] = next_L[i]
		indexSort = sorted(range(len(L)), key=lambda k: L[k])
	return P[indexSort[0]], L[indexSort[0]]

#print(VBO())

def dominate(O, idx_x_1, idx_x_2):
	dom = True
	for i in range(len(O)):
		dom = dom and (O[i][idx_x_1] > O[i][idx_x_2])
	return dom

def nonDominatedSet(X, objList):
	O = []
	for i in range(len(objList)):
		O.append([objList[i](x) for x in X])

	P = popCopy(X)
	S = []
	while len(P)>0:
		F_i = []
		F = []
		for i in range(len(P)):
			if len(list(filter(lambda x: dominate(O, x, i), range(len(P)))))<= 0:
				F_i.append(i)
		for x in F_i[::-1]:
			F.append(P.pop(x))
			for i in range(len(O)):
				O[i].pop(x)
		S.append(F)
	return S
	"""
	C = [len(x) for x in S]
	return C
	"""

print(nonDominatedSet(generateRandomPop(50,10),[computeLatency]))

