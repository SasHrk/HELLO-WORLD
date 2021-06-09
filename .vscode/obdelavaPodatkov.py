from math import *
import matplotlib.pyplot as plt
import numpy as np
import random

from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

#generiraj random decimalke na nacin rand() + rand() in jih zapisi v file - 2 stolpca
txtFile = open('obdelavaPodatkov.txt', 'w')

randomlist, Ymod = [], []
meja = 100
X = np.linspace(0, 20, meja, endpoint=False)
Y = [np.math.log(x+1) for x in X]
for i in range(0,meja):
    n = random.random()
    randomlist.append(n)
    Ymod.append(Y[i] + n - 0.5)
    txtFile.write("%f\t" %(X[i]))
    txtFile.write("%f\n" %(Ymod[i]))

txtFile.close()


def fitting():
    plt.plot(X, np.log(X+1), 'r')
    
    plt.scatter(X,Ymod)
    plt.plot(X, Ymod)
    plt.show()

#fitting()

