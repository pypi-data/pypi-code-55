"""
Faça um programa que leia um nome de usuário e a sua senha e não aceite
a senha igual ao nome do usuário, mostrando uma mensagem de erro e
voltando a pedir as informações .
"""
usuario = input('Usuario: ')
senha = input('Senha: ')
point = 1
while point == 1:
    if senha.find(usuario) >= 0:
        print('A senha não pode conter o nome do usuario')
        senha = input('Digite uma Senha Diferente : ')
    else:
        point = 0
