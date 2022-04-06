#coding:utf-8

import numpy as np

def generateRandomPop(N,d):
	P = []
	for i in range(N):
		P.append((np.random.rand(d) > 0.5).astype(int))
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
	cou = 10
	while not critereArret() and cou>0:
		cou -= 1
		Xbest = P[indexSort[0]]
		Xworst = P[indexSort[-1]]
		for i in range(Na):
			ra = (np.random.rand(d) > 0.5).astype(int)
			next_P[indexSort[i]] = P[indexSort[i]] + ra * ([a-b for (a,b) in zip(Xbest,Xworst)])
		for i in range(Na,N):
			i_peer = np.random.randint(N)
			while (i_peer == i):
				i_peer = np.random.randint(N)
			rb = (np.random.rand(d) > 0.5).astype(int)
			latency_peer = L[indexSort[i_peer]]
			latency_X = L[indexSort[i]]
			if latency_X < latency_peer:
				next_P[indexSort[i]] = P[indexSort[i]] + c1 * rb * ([a-b for (a,b) in zip(Xbest,P[indexSort[i_peer]])])
			elif latency_X > latency_peer:
				next_P[indexSort[i]] = P[indexSort[i]] + c2 * rb * ([a-b for (a,b) in zip(P[indexSort[i_peer]],P[indexSort[i]])])
			else:
				next_P[indexSort[i]] = 2 * rb * P[indexSort[i]]
		next_L = [computeLatency(x) for x in next_P]
		for i in range(N):
			if next_L[i] < L[i]:
				P[i] = [x for x in next_P[i]]
				L[i] = next_L[i]
		indexSort = sorted(range(len(L)), key=lambda k: L[k])
	return P[indexSort[0]], L[indexSort[0]]

print(VBO())