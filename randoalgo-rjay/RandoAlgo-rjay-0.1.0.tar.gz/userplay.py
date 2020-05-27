
import json
import random
from datetime import datetime
from requestalgorithms import questions, answers, questions_file, read_questions, read_answers

def userLogin():
    print('Welcome to RandoAlgo, this platform allows you to choose a random algorithm question and try to solve it')
    play= input(f'Hello  to continue playing RandoAlgo, select Login, otherwise select Exit:\n')
    
    if play == 'Login':
        username = input('Enter your username here:\n')
        password = input('Enter your password here:\n')
    
        with open('usersession.txt', 'w')as usersession:
            usersession.write(username+','+str(datetime.now()))
        try:
            number=int(input('Note: you can chose a number from 1 to 19.If you do not choose, RandoAlgo will show you just one question to start with. Choose the number of questions you want to see here:\n'))
            print (random.sample(read_questions, number))
        except ValueError:
            print('Sorry that number of algorithm questions is not available')
        if number == 0:
            print(random.choice(questions))
        
    elif play== 'Exit':
        print('You are now exiting the App')
        print('Thankyou for choosing Rand Algo, see you soon!')
        exit()
    else:
        print('Invalid input please try Again')
        userLogin()
    while True:
        play_again = input('Would you like to play again. Choose Yes or No:\n') 
        if play_again == 'Yes':
            try:
                number=int(input('Note: you can chose a number from 1 to 19. Choose the number of questions you want to see here:\n'))
                print(random.sample(read_questions, number))
                play_again = input('Would you like to play again. Choose Yes or No:\n')
            except ValueError:
                print('Sorry, you should choose an available number')
        if play_again == 'No':
            print('THANKS FOR PLAYING RANDALGO, REMEMBER PRACTICE MAKES PERFECT!!')
            break

userLogin()


