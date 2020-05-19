"""Supondo que a população de um país A seja da ordem de 80000 habitantes com uma
 taxa anual de crescimento de 3% e que a população de B seja 200000 habitantes com
 uma taxa de crescimento de 1.5%. Faça um programa que calcule e escreva o número
  de anos necessários para que a população do país A ultrapasse ou iguale a população
  do país B, mantidas as taxas de crescimento. """


def leer_dados():
    point = 1
    count = 0
    pais_A = int(input('Digite a Populacao do Pais A : '))
    pais_B = int(input('Digite a Populacao do Pais B : '))
    taixa_crescimento_A = float(input('Digite a Taixa de Crescimento do Pais A : '))
    taixa_crescimento_B = float(input('Digite a Taixa de Crescimento do Pais B : '))
    while point == 1:
        pais_A = pais_A + (pais_A * taixa_crescimento_A)
        pais_B = pais_B + (pais_B * taixa_crescimento_B)
        if pais_A > pais_B:
            point = 0
        else:
            count += 1

    print(f'En {count} años la Populacao del Pais A será mayor que la del Pais B ')
    inserir_dados_novamente()
    pass


def inserir_dados_novamente():
    again = input('Deseja Inserir Novos Dados S/N : ')
    if again.upper() == 'S':
        leer_dados()
    elif again.upper() == 'N':
        print('Obrigado pelo uso de Nosso Programa')
    else:
        print('Informacao inválida')
        inserir_dados_novamente()


leer_dados()
