import numpy as np
from random import randrange
import math
import uuid
from datetime import datetime

T = 4000 #taille total de la map T*T
p= -1 #Coefficient p pour le calcul du coefficient C
nbVoitures = 100#Le nombre total de voitures
nbRsu = 24 #Le nombre total de RSU
basicID = str(uuid.uuid4()) #basic ID pour les initialisations d'objets   
S = 500 #taille de couverture
C = 4*S
beta = 1

#fonctions pour le calcul de distance entre deux items de la map    
def distance(item1,item2):
   return math.sqrt( (item1.x - item2.x)**2 + (item1.y - item2.y)**2 )    


#Classe pour les voitures      
class Voiture:
    def __init__(self,H,vitesse):
        self.h = H 
        self.v = vitesse
        self.rsuAtr = basicID
        self.x = randrange(T)
        self.y = randrange(T)
        
    #méthode pour attribruer un controleur  
    def attrRsu(self,rsu):
        if distance(self,rsu) <= S:
            self.rsuAtr = rsu.id
        else:
            print("le rsu est trop loin")

    def printVoiture(self):
        print("h = ",self.h.second)
        print("vitesse = ",self.v)
        print("controleur attribué = ", self.rsuAtr)
        print("position = (",self.x,",",self.y,")")
        


#Classe pour les RSU
class Rsu:
    def __init__(self,H,isControleur):
        self.hRsu = H 
        self.x = randrange(T)
        self.y = randrange(T)
        self.isCont = isControleur
        self.cAtr = basicID
        self.z = 0
        self.coef = 0
        self.s = S
        self.novi = 0
        self.id = str(uuid.uuid4())
        self.nbVois = 0
    #Méthode string des rsu
    def printRsu(self):
        print("h = ",self.hRsu.second)
        print("etat controleur = ",self.isCont)
        print("controleur attribué = ", str(self.cAtr))
        print("position = (",self.x,",",self.y,")")
        print("z = ",self.z)
        print("C = ",self.coef)
        print("novi = ",self.novi)
        print("id = ",self.id)
        print("nombre de voisins",self.nbVois)
    
    #Méthode pour mettre a jour le nombre voisins
    def majVois(self,nb):
        self.nbVois = nb
    
    #Calculer le coeff novi (nb de véhicule couvert par le rsu)
    def calcNovi(self,voitures):
        novi = 0
        for v in voitures:
            if distance(self,v) <= S:
                novi = novi + 1
        self.novi = novi 
    #Calculer le coeff z du rsu (si le rsu est un controleur z est le nombre de véhicule controlé par le rsu)
    def calcZ(self,vs,rs):
        for v in vs:
            if (distance(self,v) < S):
                if (self.isCont == 1):
                    if v.rsuAtr == self.id: 
                        self.z = self.z+1
                else:
                    for r in rs: 
                        if r.id == self.cAtr:
                            r.z = r.z+1
                    
       
    #Méthode pour le calcul du coefficient C
    def calcCoef (self,vMoy):
        self.coef = p * ((nbVoitures*self.nbVois)/vMoy)
    
    #Méthode pour attribuer un controleur a un RSU
    def attrCont(self,controleur,rs,vs):
        if (distance(self,controleur) <= C): #Contrainte de la distance entre un rsu et son controleur
            if controleur.isCont == 1:
                self.cAtr = controleur.id
                self.calcZ(vs,rs)
            else:
                print("ce rsu n'est pas un controleur")
        else:
            print("non la contrainte de distance n'est pas respecté")
    def devContr(self,vs,rs):
        self.isCont = 1
        self.calcZ(vs,rs)
        
        
        
#Initialisation des voitures    
voitures = []
for i in range(nbVoitures):
    now = datetime.now()
    v = Voiture(now,randrange(14))
    voitures.append(v)
    
#On calcule la vitesse moyenne
vitMoy = 0
for v in voitures:
    vitMoy = vitMoy + v.v
vitMoy = vitMoy/nbVoitures

#Initialisation des RSU
rsus = []
for i in range(nbRsu):
    now = datetime.now()
    r = Rsu(now,0)
    rsus.append(r)

#Initialisation de Dist la matrice des distances entre les RSU
distInterRsus = np.zeros((nbRsu,nbRsu))
def calcDists(rs,D):
    for i in range(nbRsu):
        for j in range(nbRsu):
          D[i,j] = distance(rs[i],rs[j])  
    return D

distInterRsus = calcDists(rsus,distInterRsus)

#On calcule le nb de voisins de chaque RSU
for i in range(nbRsu):
    vois = 0
    for j in range(nbRsu):
        if distInterRsus[i,j] < C:
            vois = vois + 1
    rsus[i].majVois(vois)

#On calcule les coefficients C et novi de chacun des RSU
for r in rsus:
    r.calcCoef(vitMoy)
    r.calcNovi(voitures)
    
    
#Initialisation de distRsuVoit la matrice des distance entre les RSU et les voitures
distRsuVoit = np.zeros((nbRsu,nbVoitures))
def calcDistsRsuVoit(rs,vs,D):
    for i in range(nbRsu):
        for j in range(nbVoitures):
          D[i,j] = distance(rs[i],vs[j])  
    return D

distRsuVoit = calcDistsRsuVoit(rsus,voitures,distRsuVoit)


#Initialisation de X
X = np.zeros((nbRsu,nbRsu))

#Fonction pour mettre à jour X (on met à jour X a chaque fois qu'un rsu devient un controleur ou qu'un rsu est attribué à un controleur)
def majMatCont(rs,matCont): 
    for i in range(nbRsu):
        for j in range(nbRsu):
            if (i != j) and (rs[i].cAtr == rs[j].id) and (rs[i].cAtr != basicID):
                matCont[i,j] = 1
            else:
                if (i == j) and (rs[i].isCont == 1):
                    matCont[i,j] = 1
                else:
                    matCont[i,j] = 0
    return matCont

#faire devenir controleur un RSU
def devenirContr(rsu,matCont,rs,vs):
    rsu.devContr(vs,rs)
    majMatCont(rs,matCont)

#attribuer un controleur à un RSU
def attribContr(rsu,cont,matCont,rs,vs):
    rsu.attrCont(cont,rs,vs)
    majMatCont(rs,matCont)

#Initialisation de M
M = np.zeros((nbVoitures,nbRsu))

#Fonction pour mettre à jour M 
def majMatM(rs,vs,M): 
    for i in range(nbVoitures):
        for j in range(nbRsu):
            if (vs[i].rsuAtr == rs[j].id):
                M[i,j] = 1
            else: 
                M[i,j]=0

#Attribuer un RSU à une voiture
def attribRsu(rsu,v,vs,rs,matM):
    v.attrRsu(rsu)
    majMatM(rs,vs,matM)


#Fonction pour la synchronization des horloges           
def clockSync(M,vs,rs):
    sync = 0
    for i in range(nbVoitures):
        for j in range(nbRsu):
            sync = sync + M[i,j]*abs(vs[i].h.second - rs[j].hRsu.second)
    return sync


#Fonction pour avoir le nombre de controleurs
def nbControleurs(rs):
    c = 0
    for r in rs:
        if r.isCont == 1:
            c = c+1
    return c 


#Fonction pour la latence 
def latency(rs,D,matX):
    lat = 0 
    for i in range(nbRsu):
        for j in range(nbRsu):
            lat = lat +(((4*S) - D[i,j])*rs[i].coef*matX[i,j])
    return lat


#Fonction pour l'équité des charges
def equiCharge(rs):
    vecZ = []
    for r in rs: 
        vecZ.append(r.z)
    zmin = min(vecZ)
    zmax = max(vecZ)
    return beta * (zmax - zmin)


#Tests
'''voitures[0].printVoiture()

rsus[0].printRsu()
nbCont = nbControleurs(rsus)
print(rsus[3].z)
devenirContr(rsus[3], X, rsus,voitures)
print(rsus[3].z)
devenirContr(rsus[9], X, rsus,voitures)
print(rsus[5].cAtr)
print(rsus[9].id)
print(basicID)
print("avnt rsu9",rsus[9].z)
attribContr(rsus[7], rsus[9], X, rsus,voitures)
attribRsu(rsus[11], voitures[4], voitures, rsus, M)
print(rsus[5].z)
print("apres rsu9",rsus[9].z)
print(rsus[7].z)
print(rsus[7].novi)'''