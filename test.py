#coding:utf-8

from TLBO import *
from VBO_Algorithm import *
import numpy as np

#for plotting
import matplotlib.pyplot as plt

X, O = MOVBO()
n = len(X[0])
O = np.array(O)
f1 = O[:n,0]
f2 = O[:n,1]
f3 = O[:n,2]

Xt, Ot = MOTLBO()
nt = len(Xt[0])
Ot = np.array(Ot)
f1t = Ot[:nt,0]
f2t = Ot[:nt,1]
f3t = Ot[:nt,2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter3D(f1, f2, f3, color="r")
ax.scatter3D(f1t, f2t, f3t, color="b")
ax.set_title("Pareto MOVBO (red), MOTLBO (blue)")
plt.show()