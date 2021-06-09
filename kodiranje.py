from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
import random

#generiraj random decimalke na nacin rand() + rand() in jih zapisi v file - 2 stolpca
txtFile = open('randStev.txt', 'w')

randomlist = []
meja = 100
for i in range(0,meja):
    m = random.randint(1,5)
    p = random.randint(1,5)
    n = random.random()
    randomlist.append(n)
    txtFile.write("%f\t" %(n+m))
    txtFile.write("%f\t" %(n-m))
    txtFile.write("%f\t" %(n+p))
    txtFile.write("%f\n" %(n-p))

txtFile.close()

#narisi tocke iz txt file, locene s \t
X, Y = [], []

for vrstica in open('randStev.txt', 'r'):
    vrednosti = [float(s) for s in vrstica.split()]
    X.append(vrednosti[0])
    Y.append(vrednosti[1])

#Tx = float(input("Izberi tocko, Tx:\n"));
#Ty = float(input("Izberi tocko, Ty:\n"));
Tx, Ty = 1.2, 1.7
razdalje = []
for j in range (0, meja):
    razdalja = sqrt((float(Tx) - X[j])**2 + (float(Ty) - Y[j])**2)
    razdalje.append(razdalja)

#med tockami v fileu najde najkrajso razdaljo od zahtevane tocke T
def func_closest():
    minRazd, povpRazd = min(razdalje), sum(razdalje) / len(razdalje)
    print("Najkrajsa razdalja med izbrano in random tocko znasa: ", minRazd, "povprecna razdalja pa je enaka: ", povpRazd)
    plt.scatter(X,Y)
    plt.plot(Tx,Ty, 'ro')
    plt.plot(X[razdalje.index(minRazd)], Y[razdalje.index(minRazd)], 'go')
    plt.show()

#func_closest()












