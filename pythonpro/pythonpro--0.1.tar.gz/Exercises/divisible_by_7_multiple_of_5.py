"""
Given a range of numbers, this program calculate which are divisible by 7 and multiples of 5
"""


def divisibleby7(n):
    result5 = []
    result7 = []
    for v in n:
        if len(str(v)) == 4:
            lastN = str(v)[-1::]  # Aqui obtengo el último
            firstN = str(v)[:3:]  # Aqui obtengo los 3 primeros
            x = int(firstN) - (2 * int(lastN))  # Aqui el resultado es un numero de len 3
        if lastN == '5' or lastN == '0':
            result5.append(v)
        if len(str(x)) == 3:
            lastN = str(x)[-1::]  # aqui obtengo el último
            firstN = str(x)[:2:]  # aqui obtengo los 3 primeros
            y = int(firstN) - (2 * int(lastN))  # aqui el resultado es un numero de len 2
        if (y / 7).is_integer():
            result7.append(v)
        divisibleby_7 = {"7": result7, "5": result5}
    return divisibleby_7


numbers = list(range(1500, 2700))
respuesta = divisibleby7(numbers)
print('Los Divisibles por 7 son :\n ', respuesta['7'])
print('Los Multiplos de 5 son :\n ', respuesta['5'], '\n')


print('Los números divisibles por 7 y multiplos de 5 son:')
nl = []
for x in range(1500, 2701):
    if (x % 7 == 0) and (x % 5 == 0):
        nl.append(str(x))
print(','.join(nl))
