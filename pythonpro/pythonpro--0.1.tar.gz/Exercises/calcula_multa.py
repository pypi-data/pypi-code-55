"""
João Papo-de-Pescador, homem de bem, comprou um microcomputador para controlar o
rendimento diário de seu trabalho. Toda vez que ele traz um peso de peixes maior
que o estabelecido pelo regulamento de pesca do estado de São Paulo (50 quilos)
deve pagar uma multa de R$ 4,00 por quilo excedente. João precisa que você faça
um programa que leia a variável peso (peso de peixes) e calcule o excesso.

 Gravar na variável excesso a quantidade de quilos além do limite e na variável
 multa o valor da multa que João deverá pagar. Imprima os dados do programa com
 as mensagens adequadas..
"""
pesoDepeixes = int(input('Cuantos Kilos Pescaste Hoy?\n\r'))


def calcula_multa(p):
    if p > 50:
        excesso = p - 50
        multa = excesso*4
        print('Deve pagar uma multa de R$', multa, 'por ter', int(excesso), 'Kilos de mais')
    else:
        print('Não tem multa')


calcula_multa(pesoDepeixes)
