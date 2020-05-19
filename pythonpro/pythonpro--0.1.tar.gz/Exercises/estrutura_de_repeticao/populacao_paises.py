"""Supondo que a população de um país A seja da ordem de 80000
habitantes com uma taxa anual de crescimento de 3% e que a
 população de B seja 200000 habitantes com uma taxa de crescimento
 de 1.5%. Faça um programa que calcule e escreva o número de anos
  necessários para que a população do país A ultrapasse ou iguale
  a população do país B, mantidas as taxas de crescimento.  """


pais_A = 80_000
pais_B = 200_000
taixa_crescimento_A = 0.03
taixa_crescimento_B = 0.015
count = 0
point = 1
while point == 1:
    pais_A = pais_A + (pais_A * taixa_crescimento_A)
    pais_B = pais_B + (pais_B * taixa_crescimento_B)
    if pais_A > pais_B:
        point = 0
    else:
        count += 1

print(f'En {count+1} años la Populacao del Pais A será mayor que la del Pais B ')
