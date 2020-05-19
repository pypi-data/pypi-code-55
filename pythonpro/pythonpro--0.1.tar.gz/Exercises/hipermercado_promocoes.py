"""
O Hipermercado Tabajara está com uma promoção de carnes que é imperdível. Confira:
                      Até 5 Kg           Acima de 5 Kg
File Duplo      R$ 4,90 por Kg          R$ 5,80 por Kg
Alcatra         R$ 5,90 por Kg          R$ 6,80 por Kg
Picanha         R$ 6,90 por Kg          R$ 7,80 por Kg
Para atender a todos os clientes, cada cliente poderá levar apenas um dos tipos de
carne da promoção, porém não há limites para a quantidade de carne por cliente.

Se compra for feita no cartão Tabajara o cliente receberá ainda um desconto de 5%
sobre o total da compra. Escreva um programa que peça o tipo e a quantidade de carne
comprada pelo usuário e gere um cupom fiscal, contendo as informações da compra:
tipo e quantidade de carne, preço total, tipo de pagamento, valor do desconto e
valor a pagar.
"""


compra = 1
listdeCarnes = []
kilosdeCarnes = []
while compra <= 2:
    carne = int(input('1 - File Duplo\n'
                      '2 - Alcatra\n'
                      '3 - Picanha\n'
                      'Digite el número de la carne que compró: '))
    listdeCarnes.append(carne)
    carnes_dict = {1: 'File Duplo', 2: 'Alcatra', 3: 'Picanha'}
    kilos = int(input(f'Cuantos kilos de {carnes_dict[carne]} ? : '))
    kilosdeCarnes.append(kilos)
    comprouMais = input('Compro Mais Alguma Carne? S/N: ').upper()
    if comprouMais == 'S':
        compra += 1
    else:
        break

if compra == 3 and comprouMais == 'S':
    pagamento = input('\t>>>> NÃO É POSSIVEL COMPRAR MAIS DE DOIS TIPOS DE CARNES <<<<<\n'
                      '==== PAGAMENTO ===\nO Pagamento vai ser com cartão Hipermercado S/N : ').upper()
else:
    pagamento = input('==== PAGAMENTO ===\nO Pagamento vai ser com cartão Hipermercado S/N : ').upper()


def calcula_factura(listdeCarnes, kilosdeCarnes, pagamento):
    precos_ate_5kg = {1: 4.9, 2: 5.9, 3: 6.9}
    precos_acima_5kg = {1: 5.8, 2: 6.8, 3: 7.8}
    conta = []
    for i, v in enumerate(listdeCarnes):
        for j, x in enumerate(kilosdeCarnes):
            if i == j:
                if x <= 5:
                    item = x * precos_ate_5kg[v]
                    conta.append(round(item, 2))
                else:
                    item = x * precos_acima_5kg[v]
                    conta.append(round(item, 2))

    subtotal = sum(conta)
    if pagamento == 'S':
        dcto = 0.05 * subtotal
        total = subtotal - dcto
    else:
        total = subtotal
        dcto = 0
    print('\n===== CUPOM FISCAL =====\nKILOS\tCARNE\tSUBTOTAL')
    for i, v in enumerate(conta):
        print(kilosdeCarnes[i], '\t\t', carnes_dict[listdeCarnes[i]], '\tR$', conta[i])
    print(f'\t\tSUBTOTAL :  R$ {subtotal}')
    print(f'\t\t\tDCTO :  R$ {round(dcto, 2)}')
    print(f'  VALOR A PAGAR  :  R$ {round(total, 2)}\n\t\t GRACIAS POR SU COMPRA 👍')


print(calcula_factura(listdeCarnes, kilosdeCarnes, pagamento))
