"""
This program count the quantity of every characters in a string returning the result as a dict.
 Ejemplo:
 >>>contar_caracteres('Alfonso')
 {'f':1,'l':1,'n':1,'o':2,'s':1}
"""


def contar_caracteres(s):
    caracteres_ordenados = sorted(s.lower())  # Caracteres_ordenados = ['a','f','l','n','o','o','s']
    caracter_anterior = caracteres_ordenados[0]  # Caracter_anterior = ['a']
    contagem = 1
    resultado = {}
    for caracter in caracteres_ordenados[1::]:
        if caracter == caracter_anterior:
            contagem += 1
        else:
            resultado[caracter_anterior] = contagem
            caracter_anterior = caracter
            contagem = 1

    resultado[caracter_anterior] = contagem

    return resultado


if __name__ == '__main__':
    print(contar_caracteres('Alfonso'))
    print(contar_caracteres('Areiza'))
