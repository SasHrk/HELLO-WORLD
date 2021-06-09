import Funkcije

# ----------------TA DEL MORAŠ SPROTI SPREMINJATI!---------------- #
tok_vrstica = 1
temperatura_vrstica = 4
pogresek_vrstica = 2
vhodna_datoteka = "300_hor"
vhodna_datoteka_lokacija = 'C:/Users/s_hrka/Downloads'
izhodna_datoteka_lokacija = 'C:/Users/s_hrka/Downloads'
število_meritev = 3  # v stevilke shranis array števil, v število_meritev pa shranis, koliko meritev je bilo narejenih
# ---------------------------------------------------------------- #

stopinje = Funkcije.degrees(vhodna_datoteka)
tok, temperatura, pogresek = Funkcije.read_file(vhodna_datoteka, vhodna_datoteka_lokacija, tok_vrstica, temperatura_vrstica, pogresek_vrstica)

print(tok[2])
dolzina_tok, dolzina_temperatura, dolzina_pogresek = Funkcije.length(tok, temperatura, pogresek)
Funkcije.create_file_and_print("tok", stopinje, izhodna_datoteka_lokacija, dolzina_tok, število_meritev, tok)
Funkcije.create_file_and_print("temperatura", stopinje, izhodna_datoteka_lokacija, dolzina_temperatura, število_meritev, temperatura)
Funkcije.create_file_and_print("pogresek", stopinje, izhodna_datoteka_lokacija, dolzina_pogresek, število_meritev, pogresek)


print(tok)
#print(temperatura)
#print(pogresek)
print("Število elementov v arrayu:" + str(dolzina_tok))
print("Število vrstic je enako " + str(int(dolzina_tok/število_meritev)))
