import json
import random
from datetime import datetime
from requestalgorithms import questions, answers, questions_file, read_questions, read_answers

def userLogin():
    print('Welcome to RandoAlgo, this app gives you random algorithm questions to practice with. ')
    welcome_options=int(input('For new user, choose 1 to signup, if you have signed up already choose 2 to login, choose 3 to exit the game:\n'))
    if welcome_options==1:
        user_file=[]
        supply_username=input('Enter a username you want here:')
        supply_password=input('Enter a password you want here:')
        confirm_password=input('Confirm the password you entered here:')
        while True:
            user_file.append(supply_username)    
            user_file.append(supply_password)
            user_file.append(confirm_password)
            if supply_password == confirm_password:
                with open('user.txt', 'a')as users_info:
                    users_info.write(f'{user_file}')
                    users_info.write('\n')
                print('Thanks for signing up')
                welcome_options=int(input('Welcome to RandoAlgo, now that you have signed up,choose 2 to login:\n'))
                break
            elif supply_password != confirm_password:
                print('Sorry, passwords do not match!')
                userLogin()
                   
            
            
    if welcome_options==2:
        files=open('user.txt', 'r')
        users_info=files.read()
        username=input('Enter your username:\n')
        password=input('Enter your password:\n')
        
        
        if username in users_info and password in users_info:
            print('Login Sucessful')
            try:
                number=int(input('Note: you can chose a number from 1 to 19.If you do not choose, RandoAlgo will show you just one question to start with. Choose the number of questions you want to see here:\n'))
                print (random.sample(read_questions, number))
            except ValueError:
                print('Sorry that number of algorithm questions is not available')
            if number == 0:
                print(random.choice(questions))
            play_again = input('Would you like to play again. Choose Yes or No:\n') 
            if play_again == 'Yes':
                try:
                    number=int(input('Note: you can chose a number from 1 to 19. Choose the number of questions you want to see here:\n'))
                    print(random.sample(read_questions, number))
                    play_again = input('Would you like to play again. Choose Yes or No:\n')
                except ValueError:
                    print('Sorry, you should choose an available number')
            if play_again == 'No':
                print('THANKS FOR PLAYING RANDOALGO, REMEMBER PRACTICE MAKES PERFECT!!')
             

                
        elif username not in users_info and password not in users_info:
            print('Invalid login, user details incorrect!')
            userLogin()
    elif welcome_options==3:
        print('You are now exiting the App')
        print('Thankyou for choosing RandoAlgo, see you soon!')
        exit()

    else:
        print('Invalid input, please try again!')
        userLogin()
     

userLogin()
