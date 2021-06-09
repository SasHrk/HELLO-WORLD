from Funkcije import *  # S tem importaš vse svoje funkcije
from math import *
import numpy as np

# ----------------TA DEL MORAŠ SPROTI SPREMINJATI!---------------- #
#vhodna_lokacija = 'C:/Users/38651/Desktop/Faks/Magistrsko delo/Python/Meritev - 17.05.2021/'
vhodna_lokacija = 'C:\\Users\\s_hrka\\OneDrive - ISKRAEMECO, d.d\\Desktop\\python'
vhodna_datoteka_0 = '0_hor'
vhodna_datoteka_60 = '60_hor'
vhodna_datoteka_300 = '300_hor'
tok_vrstica = 1
temperatura_vrstica = 4
pogresek_vrstica = 2
red_polinoma = 3
faza = [0, 60, 300]
temperature = ["60", "40", "23", "0", "-25", "-40"]
mediana = False
# ---------------------------------------------------------------- #
# Unpack the data (to be simplified currently have a class to pack it in...)
I_0deg, T_0deg, e_0deg = read_file_and_unpack(vhodna_datoteka_0, vhodna_lokacija, tok_vrstica, temperatura_vrstica, pogresek_vrstica)
I_60deg, T_60deg, e_60deg = read_file_and_unpack(vhodna_datoteka_60, vhodna_lokacija, tok_vrstica, temperatura_vrstica, pogresek_vrstica)
I_300deg, T_300deg, e_300deg = read_file_and_unpack(vhodna_datoteka_300, vhodna_lokacija, tok_vrstica, temperatura_vrstica, pogresek_vrstica)

delta = np.degrees(np.arctan((1 - np.divide((e_60deg + 1),(e_0deg + 1)))/np.tan(np.radians(60))))
#print(delta)

print(e_0deg)

interpolation_3D(I_0deg, T_0deg, delta, faza[0], red_polinoma, median=mediana)
#interpolation_3D(I_60deg, T_60deg, e_60deg, faza[1], red_polinoma, median=mediana)
#interpolation_3D(I_300deg, T_300deg, e_300deg, faza[2], red_polinoma, median=mediana)