# -*- coding: utf-8 -*-
"""


#msg_code = open("E:\Transport\MINI\ED1 - Révision de Python Procédural - Jeu de piste numérique\2021 - Ave Cesar, ceux qui vont te casser te saluent !.txt", "r")
#msg_decode = open("E:\Transport\MINI\ED1 - Révision de Python Procédural - Jeu de piste numérique\decryptage.txt", "w")


msg_code = open("2021 - Ave Cesar, ceux qui vont te casser te saluent !.txt", "r", encoding="utf8")
msg_decode = open("decryptage.txt", "w", encoding="utf8")


abc = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
ABC = [abc[i].upper() for i in range(len(abc))]

phrase = msg_code.readline()
caracteres = list(phrase)
caracteres.pop(0)               #truc bizarre au début : \ufeff
caracteres_decales = ["" for i in range(len(caracteres))]    #initialisation
            
def decaler_lettre(caractere,decalage,abc):
    for place_lettre, lettre in enumerate(abc):
        if caractere == lettre:
            nvlle_place = (place_lettre + decalage)%26
            return abc[nvlle_place]

def decaler_caracteres(caracteres, decalage):
    for position, caractere in enumerate(caracteres):
        if caractere in abc:
            caracteres_decales[position] = decaler_lettre(caractere,decalage,abc)
        elif caractere in ABC:
            caracteres_decales[position] = decaler_lettre(caractere,decalage,ABC)
        else:
            caracteres_decales[position] = caracteres[position]
    return "".join(caracteres_decales)  #renvoie la phrase réassemblée

for decalage in range(1,26):    #de 1 à 25  inclus
    phrase_decalee = decaler_caracteres(caracteres,decalage)    #jointure des caracteres décalés
    msg_decode.write("Décalage de " + str(decalage) + " :" + "\n")
    msg_decode.write(phrase_decalee + "\n\n")
         
msg_code.close()
msg_decode.close()

"""

#ou

abc = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
ABC = [abc[i].upper() for i in range(len(abc))]

phrase = "ZYBCZXXRBFREBCCAEVREZ"
caracteres = list(phrase)
caracteres.pop(0)               #truc bizarre au début : \ufeff
caracteres_decales = ["" for i in range(len(caracteres))]    #initialisation
            
def decaler_lettre(caractere,decalage,abc):
    for place_lettre, lettre in enumerate(abc):
        if caractere == lettre:
            nvlle_place = (place_lettre + decalage)%26
            return abc[nvlle_place]

def decaler_caracteres(caracteres, decalage):
    for position, caractere in enumerate(caracteres):
        if caractere in abc:
            caracteres_decales[position] = decaler_lettre(caractere,decalage,abc)
        elif caractere in ABC:
            caracteres_decales[position] = decaler_lettre(caractere,decalage,ABC)
        else:
            caracteres_decales[position] = caracteres[position]
    return "".join(caracteres_decales)  #renvoie la phrase réassemblée

for decalage in range(1,26):    #de 1 à 25  inclus
    phrase_decalee = decaler_caracteres(caracteres,decalage)    #jointure des caracteres décalés
    print("Décalage de " + str(decalage) + " :" + "\n")
    print(phrase_decalee + "\n\n")

   
   