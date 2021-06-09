import matplotlib.pyplot as plt
import numpy as np

def row_cleanup(irow):
    orow = ""
    for part in irow:
        orow = orow + part
    return orow.split("\t")

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
                delta[p][r] = np.degrees(np.arctan((1 - (e_60[p][r] + 1) / (e_0[p][r] + 1)) / (np.tan(np.radians(faza)))))
                razSS[p][r] = (e_0[p][r] + 1) / np.cos(np.radians(delta[p][r]))
            else:
                delta[p][r] = np.degrees(np.arctan((1 - (e_300[p][r] + 1) / (e_0[p][r] + 1)) / (np.tan(np.radians(faza)))))
                razSS[p][r] = (e_0[p][r] + 1) / np.cos(np.radians(delta[p][r]))
            
    #print(delta)

    slika = plt.figure()
    os = slika.add_subplot(1, 1, 1, projection="3d")
    #os.scatter(i_60, t_60, delta, label='$\delta$ pri fazi ' + str(faza) + '°')
    #os.scatter(i_60, t_60, razSS, label='razmerje $\\frac{S_{0}^{\'}}{S_{0}}$ pri fazi ' + str(faza) + '°')

    if faza == 60:
        os.scatter(i_60, t_60, delta, label='$\delta$ pri fazi ' + str(faza) + '°')
        os.scatter(i_60, t_60, razSS, label='razmerje $\\frac{S_{0}^{\prime}}{S_{0}}$ pri fazi ' + str(faza) + '°')
    else:
        os.scatter(i_300, t_300, delta, label='$\delta$ pri fazi ' + str(faza) + '°')
        os.scatter(i_300, t_300, razSS, label='razmerje $\\frac{S_{0}^{\prime}}{S_{0}}$ pri fazi ' + str(faza) + '°')

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

izracunDelte(60)