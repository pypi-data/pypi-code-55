"""
How many occurrences of string J are there in string S
"""


def numJewelsInStones(J, S):
    """
    :type J: str
    :type S: str
    :rtype: int
    """
    count = 0
    for v in J:
        for x in S:
            if v == x:
                count += 1
    print(f'la letra "{J}" se encontró {count} veces')
    return


print('↓ Escribe un nombre ↓')
S = input()
print('↓ Letra a Buscar ↓')
J = input()
numJewelsInStones(J, S)
