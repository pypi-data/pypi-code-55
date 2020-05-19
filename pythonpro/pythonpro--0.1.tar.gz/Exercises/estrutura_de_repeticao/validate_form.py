"""
Faça um programa que leia e valide as seguintes informações:
        Nome: maior que 3 caracteres;
        Idade: entre 0 e 150;
        Salário: maior que zero;
        Sexo: 'f' ou 'm';
        Estado Civil: 's', 'c', 'v', 'd';
"""

primer = 1
while primer == 1:
    try:
        nome = input('Digite seu nome : ')
    except ValueError:
        print('Nome digitado não é valido')
    else:
        if len(nome) <= 3:
            print('Nome Inválido')
        else:
            primer = 0

segundo = 1
while segundo == 1:
    try:
        idade = int(input('Digite sua idade : '))
    except ValueError:
        print('Idade digitada não é válido')
    else:
        if 0 <= idade <= 150:
            segundo = 0
        else:
            print('O valor digitado não é válido')

tercero = 1
while tercero == 1:
    try:
        salario = int(input('Cuanto é seu Salario : '))
    except ValueError:
        print('Salario digitado não é válido')
    else:
        if 0 < salario < 100_000_000:
            tercero = 0
        else:
            print('O valor digitado não é válido')

quarto = 1
while quarto == 1:
    try:
        sexo = input("Digite 'M' Masculino, 'F' Femenino : ")
    except ValueError:
        print('Sexo digitado não é valido')
    else:
        if sexo.upper() != 'M' and sexo.upper() != 'F':
            print("Sexo digitado não é valido")
        else:
            quarto = 0

quinto = 1
estado_civil_dict = {'S': 'Solteira', 'C': 'Casada', 'V': 'Viuda', 'D': 'Divorciada'}
while quinto == 1:
    try:
        if sexo.upper() == 'M':
            estado_civil = input(
                "\t\t\tEstado Civil\n'S' Solteiro\t'C' Casado\t'V' Viudo\t'D' Divorciado\nDigite seu Estado Civil : ")
        else:
            estado_civil = input(
                "\t\t\tEstado Civil\n'S' Solteira\t'C' Casada\t'V' Viuda\t'D' Divorciada\nDigite seu Estado Civil : ")
    except ValueError:
        print('Estado Civil digitado não é valido')
    else:
        if estado_civil.upper() in estado_civil_dict:
            quinto = 0
        else:
            print('Estado Civil Inválido')
