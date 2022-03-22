#coding:utf-8

def generateRandomPop(N):
	pop = []
	return pop

def sortAndKeepPermutation(V):
	sorted(range(len(s)), key=lambda k: s[k])

def computeLatency(X):
	return 0

def critereArret():
	end = False
	return end

def VBO():
	N = 100 # population size
	d = 10 # num of RSUs
	alpha = 0.1 # proportion class A
	Na = int(alpha*N)
	P = generateRandomPop(N)
	L = [computeLatency(x) for x in P]
	indexSort = sorted(range(len(L)), key=lambda k: L[k])
	while not critereArret():
		Xbest = P[indexSort[0]]
		Xworst = P[indexSort[-1]]
		for i in range(Na):
			ra = 