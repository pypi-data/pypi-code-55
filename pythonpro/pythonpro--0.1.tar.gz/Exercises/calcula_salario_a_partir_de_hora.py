"""
This program calculate the salary of a person from the hours he worked on a month.
After this is discounted some values
"""


def calculateSalario(s, n):
    salarioBruto = float(s)*int(n)
    rendaDosalario = 0.11*salarioBruto
    inssDosalario = 0.08*salarioBruto
    sindicatoDosalario = 0.05*salarioBruto
    return f'+ Salário Bruto : $R {salarioBruto}\n' \
           f'- IR (11%) : $R {rendaDosalario}\n' \
           f'- INSS (8%) : $R {inssDosalario}\n' \
           f'- Sindicato (5%) : $R {sindicatoDosalario}\n' \
           f'- Salário Liquido : $R {int(salarioBruto-sindicatoDosalario-rendaDosalario-inssDosalario)}\n'


print('Cuanto ganas por hora?')
salarioPorhora = input()
print('Cuantas horas trabajas al mes?')
horasAlmes = input()
print(calculateSalario(salarioPorhora, horasAlmes))
