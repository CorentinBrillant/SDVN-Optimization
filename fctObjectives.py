import numpy as np
from random import randrange
import math
import uuid
from datetime import datetime

mapWidth = 7000
mapHeight= 6000
T = 4000 #taille total de la map T*T
p= -1 #Coefficient p pour le calcul du coefficient C
nbVoitures = 100 #Le nombre total de voitures
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

    id = 0

    def __init__(self,H,vitesse):
        self.h = H 
        self.v = vitesse
        self.rsuAtr = basicID
        self.x = randrange(mapWidth)
        self.y = randrange(mapHeight)
        self.id = Voiture.id
        Voiture.id += 1
        
    #méthode pour attribruer un RSU  
    def attrRsu(self,rsu):
        if distance(self,rsu) <= S:
            self.rsuAtr = rsu.id
            return 1
        else:
            return 0

    # attribue au véhicule le premier RSU à portée dans la liste RSUs
    def attrClosestRsu(self, RSUs):
        for rsu in RSUs:
            if self.attrRsu(rsu)==1:
                break

    def printVoiture(self):
        print("h = ",self.h.second)
        print("vitesse = ",self.v)
        print("controleur attribué = ", self.rsuAtr)
        print("position = (",self.x,",",self.y,")")
        


#Classe pour les RSU
class Rsu:

    idRSU = 0

    def __init__(self,x,y,H,isControleur):
        self.hRsu = H 
        self.x = x #randrange(T)
        self.y = y #randrange(T)
        self.isCont = isControleur
        self.cAtr = basicID
        self.z = 0
        self.coef = 0
        self.s = S
        self.novi = 0
        self.id = Rsu.idRSU
        Rsu.idRSU += 1
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

    
    #Calculer le coeff novi (nb de véhicule couvert par le rsu)
    def calcNovi(self,voitures):
        novi = 0
        for v in voitures:
            if v.rsuAtr == self.id:
                novi = novi + 1
        self.novi = novi 

    # on calcule le nb de voisins d'un RSU
    def calcVois(self, rs):
        count = 0
        for rsu in rs:
            if distance(self, rsu) < C and rsu.id != self.id:
                count += 1
        self.nbVois = count
                    
       
    #Méthode pour le calcul du coefficient C
    def calcCoef (self, vs, rs):
        vMoy = 0
        for v in vs:
            if v.rsuAtr == self.id:
                vMoy += v.v
        self.calcNovi(vs)
        if self.novi <= 0:
            self.coef = 0
        else:
            vMoy = vMoy / self.novi
            if vMoy>0:
                self.calcVois(rs)
                self.coef = p * ((self.novi*self.nbVois)/vMoy)
            else:
                self.coef = 0
        
        
#Initialisation de Dist la matrice des distances entre les RSU
def calcDists(rs):
    D = np.zeros((nbRsu,nbRsu))
    for i in range(nbRsu):
        for j in range(nbRsu):
            D[i,j] = distance(rs[i],rs[j])  
    return D


#Fonction pour la synchronization des horloges           
def clockSync(rs, vs):
    sync = 0
    for i in range(len(vs)):
        for j in range(len(rs)):
            if vs[i].rsuAtr == j:
                sync = sync + abs(vs[i].h.second - rs[j].hRsu.second)
    return sync


#Fonction pour avoir le nombre de controleurs
def nbControleurs(rs):
    c = 0
    for r in rs:
        if r.isCont == 1:
            c = c+1
    return c 

#Fonction pour la latence 
def latency(rs, vs):
    D = calcDists(rs)
    lat = 0 
    for i in range(nbRsu):
        for j in range(nbRsu):
            if rs[i].cAtr == j:
                rs[i].calcCoef(vs,rs)
                lat = lat +((C - D[i,j])*rs[i].coef)
    return lat


#Fonction pour l'équité des charges
def equiCharge(rs, vs):
    Z = []
    for rsu in rs:
        rsu.calcNovi(vs)
    for rsu in rs:
        if rsu.isCont:
            Z_i = 0
            for j in rs:
                if j.isCont==0 and j.cAtr == rsu.id:
                    Z_i += j.novi
            Z.append(Z_i)
    zmin = min(Z)
    zmax = max(Z)
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