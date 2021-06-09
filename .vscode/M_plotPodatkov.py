import matplotlib.pyplot as plt
import numpy as np
import statistics
import scipy as sp
#from Funkcije import *

def row_cleanup(irow):
    orow = ""
    for part in irow:
        orow = orow + part
    return orow.split("\t")
    
def mediana(sigma):
    st_meritev = 13     #13 meritev pri razlicni T
    st_blokov = 6       #blok velikosti 13, meritev pri drugi T

    i_podatki, t_podatki, e_podatki = [], [], []
    for vrstica in open('C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python\\tok_0deg.txt', 'r'):
        vrstica = row_cleanup(vrstica[:-1])     #vrstica v fileu je ločena na \t, spremenjena v array, izbrisan je zadnji elem: \n -> ''
        vrstica = vrstica[:-1]
        i_podatki.append(vrstica)

    for vrstica in open('C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python\\temperatura_0deg.txt', 'r'):
        vrstica = row_cleanup(vrstica[:-1])     
        vrstica = vrstica[:-1]
        t_podatki.append(vrstica)

    for vrstica in open('C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python\\pogresek_0deg.txt', 'r'):
        vrstica = row_cleanup(vrstica[:-1])     
        vrstica = vrstica[:-1]
        e_podatki.append(vrstica)
    
    i_podatki = [[float(a) for a in j] for j in i_podatki]  #lists
    t_podatki = [[float(a) for a in j] for j in t_podatki]
    e_podatki = [[float(a) for a in j] for j in e_podatki]

    print(i_podatki)

    i_vektor_median, t_vektor_median, e_vektor_median = [], [], []      #dolocanje mediane za vsako vrstico (mediana tock po meritah)
    for u in range(0, st_blokov*13):
        e_vektor_median.append(round(statistics.median(e_podatki[u]), 3))  
        i_vektor_median.append(round(statistics.median(i_podatki[u]), 3))  
        t_vektor_median.append(round(statistics.median(t_podatki[u]), 3))  
    '''print(e_vektor_median)
    print(i_vektor_median)
    print(t_vektor_median)
    print("\n")'''

    #dolocanje tock (v vrstici), ki ustrezajo pogoju (mediana - sigma < x < mediana + sigma) 
    #e_sigma, i_sigma, t_sigma = [[False for m in range(0,7)] for i in range(st_blokov*st_meritev)], [[False for m in range(0,7)] for i in range(st_blokov*st_meritev)], [[False for m in range(0,7)] for i in range(st_blokov*st_meritev)]
    #e_zavrzene, i_zavrzene, t_zavrzene = [[False for m in range(0,7)] for i in range(st_blokov*st_meritev)], [[False for m in range(0,7)] for i in range(st_blokov*st_meritev)], [[False for m in range(0,7)] for i in range(st_blokov*st_meritev)]
    e_sigma, i_sigma, t_sigma = [[np.nan for m in range(0,7)] for i in range(st_blokov*st_meritev)], [[np.nan for m in range(0,7)] for i in range(st_blokov*st_meritev)], [[np.nan for m in range(0,7)] for i in range(st_blokov*st_meritev)]
    e_zavrzene, i_zavrzene, t_zavrzene = [[np.nan for m in range(0,7)] for i in range(st_blokov*st_meritev)], [[np.nan for m in range(0,7)] for i in range(st_blokov*st_meritev)], [[np.nan for m in range(0,7)] for i in range(st_blokov*st_meritev)]

    counter_zavrzenih = 0
    for i in range(0, st_blokov*st_meritev):    #sprehajanje navzdol
        for j in range(0, 7):                   #sprehajanje desno
            if (e_podatki[i][j] < (e_vektor_median[i] + sigma) and e_podatki[i][j] > (e_vektor_median[i] - sigma)):
                e_sigma[i][j] = e_podatki[i][j]         #matrike sprejetih tock
                i_sigma[i][j] = i_podatki[i][j]
                t_sigma[i][j] = t_podatki[i][j]
            else:
                e_zavrzene[i][j] = e_podatki[i][j]      #matrike zavrzenih tock
                i_zavrzene[i][j] = i_podatki[i][j]
                t_zavrzene[i][j] = t_podatki[i][j]
                counter_zavrzenih = counter_zavrzenih +  1
    
    #dolocanje vektorja povprečnih vrednosti po vrsticah
    e_povp_predSigmo, e_povp_poSigmi = [], []
    i_povp_predSigmo, i_povp_poSigmi = [], []
    t_povp_predSigmo, t_povp_poSigmi = [], []

    e_sigma_ociscena = [[] for i in range(st_blokov*st_meritev)]    #iz e_sigma umaknem vse vrednosti False; sicer me motijo pri izracunu povprecja (so enake 0)
    i_sigma_ociscena, t_sigma_ociscena = [[] for i in range(st_blokov*st_meritev)], [[] for i in range(st_blokov*st_meritev)]
    for i in range(0, st_blokov*st_meritev):
        for j in range(0, 7):
            if type(i_sigma[i][j]) != bool:
                i_sigma_ociscena[i].append(i_sigma[i][j])
            if type(t_sigma[i][j]) != bool:
                t_sigma_ociscena[i].append(t_sigma[i][j])
            if type(e_sigma[i][j]) != bool:
                e_sigma_ociscena[i].append(e_sigma[i][j]) 
        
        i_povp_predSigmo.append(round(statistics.mean(i_podatki[i]), 3))
        t_povp_predSigmo.append(round(statistics.mean(t_podatki[i]), 3))
        e_povp_predSigmo.append(round(statistics.mean(e_podatki[i]), 3))  
        i_povp_poSigmi.append(round(statistics.mean(i_sigma_ociscena[i]), 3))
        t_povp_poSigmi.append(round(statistics.mean(t_sigma_ociscena[i]), 3))
        e_povp_poSigmi.append(round(statistics.mean(e_sigma_ociscena[i]), 3))

    #with open('e_sigma_ociscena.txt', 'w') as f:
    #    print(e_sigma_ociscena, file=f)

    def interpolate_surface(order):
        if order == 2:
            data = np.asarray([i_sigma, t_sigma, e_sigma]).T      # matrika, kjer so stolcpi I, T, e; prvi subarray je razdeljen na tri stolpce in predstavlja prvi stolpec podatkov v file
            
            '''print(data.shape) 
            print(np.ones(data.shape[0]))           #data.shape[0]: 7; data.shape (7, 78, 3): 7 subarray, 78 vrstic, 3 stolpci
            #print(np.tile((np.ones(data.shape[0])), (2,1))) # [1 1 1 1 1 1] doda se eno tako vrstico
            print(data[:, :2])                      #prvi dve vrstici v file; 7 stolpcev, 
            print(np.prod(data[:, :2], axis=1))     #zmnozek elems prvega stolpca v data[:, :2]; matrika 7x3
            print(data[:, :2] ** 2)                 #kvadrira elems matrike

            #I = [[] for i in range(0,6)]
            #I, T, e = [[] for i in range(0,6)], [[] for i in range(0,6)], [[] for i in range(0,6)]
            #for u in range(0, 6):
            #    I[u] = np.array([i for i in data[u][:,0:1] if i != 0.0]).flatten()
            #    T[u] = np.array([i for i in data[u][:,1:2] if i != 0.0]).flatten()
            #    e[u] = np.array([i for i in data[u][:,2:3] if i != 0.0]).flatten()
            I = np.array([i for i in data[0][:,0:1] if i != 0.0]).flatten()     # = sprejete tocke
            T = np.array([i for i in data[0][:,1:2] if i != 0.0]).flatten()     # data[0][:,0:1] = tok (1. stolpec), data[0][:,1:2] = temperatura, data[0][:,2:3] = pogresek
            e = np.array([i for i in data[0][:,2:3] if i != 0.0]).flatten()     # + pobrisane vrednosti 0.0 = False

            #kubni cleni x**3
            #print([i**3 for i in I])
            #print([i**3 for i in T])
            #print((np.array([i**3 for i in I]).shape))

            #kvadratni cleni x**2
            #print([i**2 for i in I])
            #print((np.array([i**2 for i in I]).shape))

            #monomski (?) cleni x
            #print([i for i in I])
            #print((np.array([i for i in I]).shape))

            #skalarni (?) cleni
            #print(np.ones(I.shape[0]))
            #print((np.ones(I.shape[0])).shape)

            #mesani cleni do 2
            #print([a*b for a, b in zip(I, T)])  
    #interpolate_surface(2)'''
    
    slika = plt.figure()
    os = slika.add_subplot(1, 2, 1, projection="3d")
    os2 = slika.add_subplot(1, 2, 2, projection="3d")
    #os.scatter(i_podatki, t_podatki, e_podatki, label='izmerjene tocke')
    os2.scatter(i_povp_predSigmo, t_povp_predSigmo, e_povp_predSigmo, marker = '+', color = 'purple', label = 'povprecje pred $\sigma$')
    os2.scatter(i_povp_poSigmi, t_povp_poSigmi, e_povp_poSigmi, color = 'green', label = 'povprecje po $\sigma$')
    os.scatter(i_sigma, t_sigma, e_sigma, color = 'black', label= 'sprejete tocke')
    if counter_zavrzenih > 0:
        os.scatter(i_zavrzene, t_zavrzene, e_zavrzene, color='red', label= 'zavrzenih tock: ' + str(counter_zavrzenih)) #eno tocko pri (0,0,0) narobe prikazuje
        print("counter_zavrzenih: ", counter_zavrzenih)

    os.legend()
    os.set_xlabel("I[A]")
    os.set_ylabel("T[°C]")
    os.set_zlabel("e[%]")
    os2.legend()
    os2.set_xlabel("I[A]")
    os2.set_ylabel("T[°C]")
    os2.set_zlabel("e[%]")
    plt.show()

#mediana(0.02)

def izracunDelte(faza):

    st_stolpcev, st_vrstic = 7, 78
    if(faza != 60 and faza != 300):
        print("Neobstojeca faza, nehi se zezat. Pa 0 tud ne bo prava.")
        return 0

    e_0, e_60, e_300 = [], [], []
    t_60, t_300, i_60, i_300 = [], [], [], []
    for vrstica in open('C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python\\pogresek_0deg.txt', 'r'):
        vrstica = row_cleanup(vrstica[:-1])     #vrstica v fileu je ločena na \t, spremenjena v array, izbrisan je zadnji elem: \n -> ''
        vrstica = vrstica[:-1]
        e_0.append(vrstica)

    for vrstica in open('C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python\\pogresek_60deg.txt', 'r'):
        vrstica = row_cleanup(vrstica[:-1])     #vrstica v fileu je ločena na \t, spremenjena v array, izbrisan je zadnji elem: \n -> ''
        vrstica = vrstica[:-1]
        e_60.append(vrstica)

    for vrstica in open('C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python\\temperatura_60deg.txt', 'r'):
        vrstica = row_cleanup(vrstica[:-1])     
        vrstica = vrstica[:-1]
        t_60.append(vrstica)
    
    for vrstica in open('C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python\\temperatura_300deg.txt', 'r'):
        vrstica = row_cleanup(vrstica[:-1])     
        vrstica = vrstica[:-1]
        t_300.append(vrstica)

    for vrstica in open('C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python\\tok_60deg.txt', 'r'):
        vrstica = row_cleanup(vrstica[:-1])     
        vrstica = vrstica[:-1]
        i_60.append(vrstica)
    
    for vrstica in open('C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python\\tok_300deg.txt', 'r'):
        vrstica = row_cleanup(vrstica[:-1])     
        vrstica = vrstica[:-1]
        i_300.append(vrstica)
    
    e_0 = [[float(a) for a in j] for j in e_0]
    e_60 = [[float(a) for a in j] for j in e_60]
    e_300 = [[float(a) for a in j] for j in e_300]

    delta, razSS = [[0 for j in range(0, st_stolpcev)] for i in range(0,st_vrstic)], [[0 for j in range(0, st_stolpcev)] for i in range(0,st_vrstic)]
    for p in range(0, st_vrstic):
        for r in range(0, st_stolpcev):
            if faza == 60:
                delta[p][r] = np.degrees(np.arctan((1 - (e_60[p][r]/100 + 1) / (e_0[p][r]/100 + 1)) / (np.tan(np.radians(faza)))))
                razSS[p][r] = (e_0[p][r]/100 + 1) / np.cos(np.radians(delta[p][r]))
            else:
                delta[p][r] = np.degrees(np.arctan((1 - (e_300[p][r]/100 + 1) / (e_0[p][r]/100 + 1)) / (np.tan(np.radians(faza)))))
                razSS[p][r] = (e_0[p][r]/100 + 1) / np.cos(np.radians(delta[p][r]))
            
    #print(delta)

    slika = plt.figure()
    os = slika.add_subplot(1, 1, 1, projection="3d")
    #os.scatter(i_60, t_60, delta, label='$\delta$ pri fazi ' + str(faza) + '°')
    #os.scatter(i_60, t_60, razSS, label='razmerje $\\frac{S_{0}^{\'}}{S_{0}}$ pri fazi ' + str(faza) + '°')

    if faza == 60:
        os.scatter(i_60, t_60, delta, label='$\delta$ pri fazi ' + str(faza) + '°')
        os.scatter(i_60, t_60, razSS, label='razmerje $\\frac{S_{0}^{\'}}{S_{0}}$ pri fazi ' + str(faza) + '°')
    else:
        os.scatter(i_300, t_300, delta, label='$\delta$ pri fazi ' + str(faza) + '°')
        os.scatter(i_300, t_300, razSS, label='razmerje $\\frac{S_{0}^{\'}}{S_{0}}$ pri fazi ' + str(faza) + '°')

    os.legend()
    os.set_xlabel("I[A]")
    os.set_ylabel("T[°C]")
    os.set_zlabel("$\delta$[°]")
    #plt.xlim([0,41])
    #plt.ylim([-40,61])
    #plt.xticks(np.arange(0, 50, 5))
    #slika.set_figheight(50)
    #slika.set_figwidth(60)

    plt.show()

#izracunDelte(60)

def interpolacija():

    I, T, e = [], [], []
    data = []
    for vrstica in open('C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python\\tok_interpol.txt', 'r'):
        vrednosti = [float(s) for s in vrstica.split()]
        I = vrednosti
    for vrstica in open('C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python\\temperatura_interpol.txt', 'r'):
        vrednosti = [float(s) for s in vrstica.split()]
        T = vrednosti
    print(np.array(T).T)
    for vrstica in open('C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python\\pogresek_interpol.txt', 'r'):
        vrednosti = [float(s) for s in vrstica.split()]
        e = vrednosti
    print(e)

    

interpolacija()
