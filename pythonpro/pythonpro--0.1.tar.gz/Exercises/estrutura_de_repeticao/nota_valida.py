"""
Faça um programa que peça uma nota, entre zero e dez.
Mostre uma mensagem caso o valor seja inválido e
continue pedindo até que o usuário informe um valor válido .
"""

point = 1
while point == 1:
    try:
        nota = int(input('Digite a nota : '))
    except ValueError:
        print('O valor digitado não é válido')
    else:
        if isinstance(nota, int) and 0 <= nota <= 10:
            point = 0
        else:
            print('O valor digitado não é válido')

print('Continue con su compra')
