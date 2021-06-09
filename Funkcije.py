import os
from math import *
import matplotlib.lines
import numpy as np
from scipy.linalg import lstsq
from matplotlib import cm, pyplot as plt

def string_to_list(string):
    li = list(string.split(" "))
    return li


def length(current, temperature, error):
    length_current = len(current)
    length_temperature = len(temperature)
    length_error = len(error)
    return length_current, length_temperature, length_error


def read_file(input_file, input_file_location, current_column, temperauture_column, error_column):
    uvozna_datoteka_polno = input_file + ".txt"
    lokacija = input_file_location
    polno_ime = os.path.join(lokacija, uvozna_datoteka_polno)
    with open(polno_ime, 'r') as f:
        vrstica = f.readlines()
        current = string_to_list(vrstica[current_column - 1])
        temperature = string_to_list(vrstica[temperauture_column - 1])
        error = string_to_list(vrstica[error_column - 1])
    f.close()
    return current, temperature, error

def read_file_and_unpack(input_file, input_file_location, current_column, temperauture_column, error_column):
    uvozna_datoteka_polno = input_file + ".txt"
    lokacija = input_file_location
    polno_ime = os.path.join(lokacija, uvozna_datoteka_polno)
    with open(polno_ime, 'r') as f:
        vrstica = f.readlines()
        current = np.array(string_to_list(vrstica[current_column - 1])).astype(np.float64)
        temperature = np.array(string_to_list(vrstica[temperauture_column - 1])).astype(np.float64)
        error = np.array(string_to_list(vrstica[error_column - 1])).astype(np.float64) #astype je potreben, sicer napiše napako, saj je podatek pred tem v obliki stringa, potreben pa je v obliki floata!
    f.close()
    return current, temperature, error


def degrees(input_file):
    if input_file[1] == "_":
        degree = input_file[0]
    elif input_file[2] == "0":
        degree = input_file[0] + input_file[1] + input_file[2]
    else:
        degree = input_file[0] + input_file[1]
    return degree


def create_file_and_print(name, degree, output_location, length_data, number_of_measurement, data):
    ime_datoteke = name
    ime_datoteke_polno = ime_datoteke + '_' + degree + 'deg' + ".txt"
    lokacija = output_location
    polno_ime = os.path.join(lokacija, ime_datoteke_polno)
    file = open(polno_ime, "w")
    file.truncate(0)
    for i in range(0, length_data, 1):
        if (i != 0) & ((i % number_of_measurement) == 0):
            file.write("\n" + str(data[i]) + "\t")
        else:
            file.write(str(data[i]) + "\t")


def array_resize_and_split(current, error, temperature, number_rows, number_of_repetitions, temperatures_list):
    ustvari_matriko_tok = np.resize(current, (number_rows, number_of_repetitions))  # iz ene vrstice v 78x7 matriko
    ustvari_matriko_pogrešek = np.resize(error, (number_rows, number_of_repetitions))
    #ustvari_matriko_temperatura = np.resize(temperature, (number_rows, number_of_repetitions))
    razbij_matriko_tok = np.array_split(ustvari_matriko_tok,len(temperatures_list))  # razbij matriko na toliko enakih delov, kot je temperatur
    razbij_matriko_pogrešek = np.array_split(ustvari_matriko_pogrešek,len(temperatures_list))
    #return ustvari_matriko_temperatura
    return razbij_matriko_tok, razbij_matriko_pogrešek


def save_to_dictionary(name_current, name_error, temperature, split_current, split_error):
    my_dict_current = {}
    my_dict_error = {}
    for i in range(0, len(temperature), 1):
        ime_spremenljivke_tok = name_current + f"_{temperature[i]}°C"
        ime_spremenljivke_pogrešek = name_error + f"_{temperature[i]}°C"
        my_dict_current[ime_spremenljivke_tok] = split_current[i]
        my_dict_error[ime_spremenljivke_pogrešek] = split_error[i]
    return my_dict_current, my_dict_error


def fitting_coefficient(current, temperature, error, coefficient, order):
    x = current
    y = temperature
    if order == 2:
        enačba = coefficient[0] + coefficient[1]*x + coefficient[2]*y + coefficient[3]*x*y + coefficient[4]*x**2 + coefficient[5]*y**2
        residuum = error - enačba
        standardna_deviacija = round(sqrt(sum(residuum ** 2) / len(residuum)), 6)
    if order == 3:
        enačba = coefficient[0] + coefficient[1] * x + coefficient[2] * y + coefficient[3] * x ** 2 + coefficient[4] * x * y + coefficient[5] * y ** 2 + coefficient[6] * x ** 3 + coefficient[7] * x ** 2 * y + coefficient[8] * y ** 2 * x + coefficient[9] * y ** 3
        residuum = error - enačba
        standardna_deviacija = round(sqrt(sum(residuum ** 2) / len(residuum)), 6)
    return standardna_deviacija

def get_surface(x, y, z, d=10, precision=7, order=3):
    """ Returns the interpolated surface x, y, z coordinates
    and the surface equation parameters. To see which parameters
    are which check in the function below.

    :param x:
    :param y:
    :param z:
    :param d: "resolution" of the returned surface
    :param precision: koliko decimalk upošteva pri končnem izpisu koeficientov
    :param order: order of the surface (2 or 3)
    :return: x, y, z parameters and c surface coefficients
    """
    X, Y = np.meshgrid(np.arange(np.ndarray.min(x), np.ndarray.max(x) + 1e-3, (np.ndarray.max(x) - np.ndarray.min(x)) / d),
                       np.arange(np.ndarray.min(y), np.ndarray.max(y) + 1e-3, (np.ndarray.max(y) - np.ndarray.min(y)) / d))
    XX = X.flatten()
    YY = Y.flatten()

    data = np.array([x, y, z]).T

    if order == 2:
        A = np.c_[np.ones(data.shape[0]), data[:, :2], np.prod(data[:, :2], axis=1), data[:, :2] ** 2]
        C, _, _, _ = lstsq(A, data[:, 2])
        Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX * YY, XX ** 2, YY ** 2], C).reshape(X.shape)
        equation = f"f(x,y) = {C[4]:.{precision}f}x^2 + {C[5]:.{precision}f}y^2 + {C[3]:.{precision}f}xy + {C[1]:.{precision}f}x + {C[2]:.{precision}f}y + {C[0]:.{precision}f}"
    elif order == 3:
        A = np.c_[np.ones(data.shape[0]),
                  data[:, :2],
                  data[:, 0] ** 2,
                  np.prod(data[:, :2], axis=1),
                  data[:, 1] ** 2,
                  data[:, 0] ** 3,
                  np.prod(np.c_[data[:, 0] ** 2, data[:, 1]], axis=1),
                  np.prod(np.c_[data[:, 0], data[:, 1] ** 2], axis=1),
                  data[:, 1] ** 3]
        C, residues, rank, a = lstsq(A, data[:, 2])
        # print(f"Coefficients:\n{C}\nResidues: {residues}\nRank: {rank}\nSingular values:\n{a}")
        Z = np.dot(np.c_[np.ones(XX.shape),
                         XX, YY,
                         XX ** 2,
                         XX * YY,
                         YY ** 2,
                         XX ** 3,
                         XX ** 2 * YY,
                         XX * YY ** 2,
                         YY ** 3],
                   C).reshape(X.shape)
        equation = f"f(x,y) = {C[0]:.{precision}f} + {C[1]:.{precision}f}x + {C[2]:.{precision}f}y + {C[3]:.{precision}f}x^2 + {C[4]:.{precision}f}xy + {C[5]:.{precision}f}y^2 + {C[6]:.{precision}f}x^3 + {C[7]:.{precision}f}x^2y + {C[8]:.{precision}f}y^2x + {C[9]:.{precision}f}y^3"
        equation = equation.replace("+ -", "- ")
    else:
        raise ValueError("Order must either be 2 or 3.")
    return X, Y, Z, C, equation


def plot_surface_and_scatter(current_surface, temperature_surface, error_surface, current, temperature, error, phase, coefficient, order):
    fig = plt.figure() #naredi figure
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed') #zato, da se figure izriše takoj čez cel zaslon ob klicu
    fitting = fitting_coefficient(current, temperature, error, coefficient, order)
    naslov = f"Interpolirana ploskev vhodnih podatkov pri {phase}°. Fitting = {fitting}"
    fig.suptitle(naslov) #dodaj naslov subplotu (sicer le en subplot)
    ax = fig.add_subplot(projection="3d") #sintaksa za dodajanje subplot v figure. Sicer je le en subplot, a tako je priporočeni risati v Pythonu. add_subplot uporabljamo, da
    plt.subplots_adjust(left=0, bottom=0, right=0.9, top = 1) #nastavitve, da se graf izriše čimbolj čez cel figure
    surf = ax.plot_surface(current_surface, temperature_surface, error_surface, cmap=cm.viridis) #izriše ploskev iz danih točk. Cmap je le dodatek, pomeneni pa colormap - kakšne barve ima ploskev
    clb = fig.colorbar(surf, shrink=0.8, orientation = "vertical", location = 'left')  #dodaj stolpec narisani ploskvi. Shrink je nastavljen, da se vidi celoten stolpec malo lepše in da ni od roba do roba figure-a
    clb.ax.set_title(f"e[%] pri {phase}°")
    ax.scatter(current, temperature, error, c = 'b', s=5)
    ax.set_xlabel("T[°C]")
    ax.set_ylabel("I[A]")
    ax.set_zlabel("e[%]")
    scatter_proxy = matplotlib.lines.Line2D([0],[0], linestyle = "none", c = 'b', marker = 'o')
    ax.legend([scatter_proxy], ["Izmerjene točke pogreškov"], numpoints = 1, loc = "upper left", bbox_to_anchor = (1.04,0.9)) #bbox se uporablja zato, da legendo namestimo izveni figure-a
    plt.show()


def interpolation_3D(current, temperature, error, phase, order_polynomial, median):
    if median == True:
        a = 3 ##DOPOLNI S KODO, KO BOŠ IMEL MEDIANSKI FILTER!!!
    else:
        X, Y, Z, coefficient, equation = get_surface(current, temperature, error, order = order_polynomial)
        plot_surface_and_scatter(X, Y, Z, current, temperature, error, phase, coefficient, order_polynomial)
        print(f"Enačba ploskve @ {phase}°: \n {equation}")