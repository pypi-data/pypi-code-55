from utils import check, options


def runapp():
    print('\033[1;33m WELCOME to DevGossip. Catch up on the most entertaining gossip right here!')
    print('\nA. Sign Up \nB. Log in \nC. Post as anonymous \nD. Close App')
    user_choice = input('Choose an action(A-D). \n>> ').upper()

    while not check(user_choice):
        print('Invalid action!')
        user_choice = input('Make a choice(A-D): ').upper()
        print()

    else:
        options(user_choice)


runapp()