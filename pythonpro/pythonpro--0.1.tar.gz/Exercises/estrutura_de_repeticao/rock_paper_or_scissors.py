"""
Jokenpo é uma brincadeira japonesa, onde dois jogadores escolhem um dentre
três possíveis itens: Pedra, Papel ou Tesoura.
O objetivo é fazer um juiz de Jokenpo que dada a jogada dos dois jogadores
informa o resultado da partida. As regras são as seguintes:

Pedra empata com Pedra e ganha de Tesoura
Tesoura empata com Tesoura e ganha de Papel
Papel empata com Papel e ganha de Pedra
"""
print('='*17, 'Bienvenido a Piedra, Papel o Tijera', '='*17)
print('*'*22, 'Presiona (PI) para Piedra', '*'*22)
print('*'*22, 'Presiona (PA) para Papel', '*'*23)
print('*'*22, 'Presiona (TI) para Tijera', '*'*22)
print('-'*8, 'En cualquier momento presione (X) para salir del juego',  '-'*6, '\n')


def validate_values():
    P1 = 1
    while P1 == 1:
        player1 = input('Player 1: Digite la letra de su juego -> ').upper()
        if player1 not in ['PI', 'PA', 'TI']:
            print('Valor Incorrecto, Should digit (PI), (PA), OR (TI)')
        else:
            P1 = 0
    P2 = 1
    while P2 == 1:
        player2 = input('Player 2: Digite la letra de su juego -> ').upper()
        if player2 not in ['PI', 'PA', 'TI']:
            print('Valor Incorrecto, Should digit (PI), (PA), OR (TI)')
        elif player2 and player1 == 'X':
            break
        else:
            P2 = 0
    return player1, player2


def rock_paper_scissors(player1, player2):
    PI = {'PA': False, 'TI': True, 'PI': None}
    PA = {'PI': False, 'TI': False, 'PA': None}
    TI = {'PA': True, 'PI': False, 'TI': None}
    if player1 == 'PI':
        return PI[player2]
    elif player1 == 'PA':
        return PA[player2]
    else:
        return TI[player2]


def run_game():
    player1, player2 = validate_values()
    who_won = rock_paper_scissors(player1, player2)
    if who_won:
        return 'Ganó el Player 1'
    elif False:
        return 'Ganó el Player 2'
    else:
        return 'Empate'


if __name__ == '__main__':
    print(run_game())
