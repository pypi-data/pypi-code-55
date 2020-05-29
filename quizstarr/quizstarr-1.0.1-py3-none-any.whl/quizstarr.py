import requests
import json
import string
import random
    
url = 'https://opentdb.com/api.php?amount=25'
response = requests.get(url)
data = response.json()
question = data['results']
file = open('question.json', 'w')
file = json.dump(question, file)

def main():
    print('Welcome to Quizz Starr!!!')
    print(f' 1. Signup\n'
          f' 2. Login\n'
          f' 3. Quit\n')
    choice = input('Enter your choice: ')

    if int(choice) == 1:
        signup()
    elif int(choice) == 2:
        access = login()
        if access:
            no_of_questions()
    elif int(choice) == 3:
        exit()
    else:
        print('Invalid Choice')
        start()
        
def signup():
    user_login = open('user-login.txt', 'a+')

    username = input('Entered Desired Username: ')
    password = input('Entered Desired Password: ')

    user_login.write(f'{username},'
                     f'{password}')
    user_login.write('-')
    user_login.close()


    no_of_questions()

def login():
    holder = []
    container = []
    header = ['username', 'password']
    user = open('user-login.txt', 'r')
    users = user.readline()
    users = users.split('-')
    user.close()

    for details in users:
        holder.append(details.split(','))
        
    for user in holder:
        container.append(dict(zip(header, user)))

    def check():
        trial = 3
        while trial > 0:
            trial -= 1
            input_username = input('Enter your username: ')
            input_password = input('Enter your password: ')

            for item in container:
                if input_username.lower() == item['username'].strip():
                    if input_password == item['password'].strip():
                        print('Login Successful')
                        return True

            print('Wrong username or password inpuuted')
            
        return False
    
    return check()


def no_of_questions():
    print("\n=========QUIZ START============")
    print('Please Select the nunmber of questions you want to answer')
    print(f' 1. 10 Questions\n'
          f' 2. 15 Questions\n'
          f' 3. 20 Questions')

    feedback = input('Enter your choice: ')

    if int(feedback) == 1:
        ten_questions()
    elif int(feedback) == 2:
        fifteen_questions()
    elif int(feedback) == 3:
        twenty_questions()
    else:
        print('Invalid Selection')
        no_of_questions()


def ten_questions():
    score = 0
    with open('question.json', 'r') as f:
        j = json.load(f)
        for i in range(10):
            no_of_questions = len(j)
            ch = random.randint(0, no_of_questions-1)
            a = j[ch]['correct_answer']
            b = j[ch]['incorrect_answers']
            b.append(a)
            print(f'\nQ{i+1} {j[ch]["question"]}\n')
            for option in b:
                print(option)

            answer = input('\nEnter your answer: ')
            if j[ch]['correct_answer'][0] == answer[0].upper():
                print('\nYou are correct')
                score += 1
            else:
                print('\nYou are incorrect')

            del j[ch]
            
        print(f'\nFINAL SCORE: {score}')
        play_again()


def fifteen_questions():
    score = 0
    with open('question.json', 'r') as f:
        j = json.load(f)
        for i in range(15):
            no_of_questions = len(j)
            ch = random.randint(0, no_of_questions-1)
            a = j[ch]['correct_answer']
            b = j[ch]['incorrect_answers']
            b.append(a)
            print(f'\nQ{i+1} {j[ch]["question"]}\n')
            for option in b:
                print(option)

            answer = input('\nEnter your answer: ')
            if j[ch]['correct_answer'][0] == answer[0].upper():
                print('\nYou are correct')
                score += 1
            else:
                print('\nYou are incorrect')

            del j[ch]
            
        print(f'\nFINAL SCORE: {score}')
        play_again()
        

def twenty_questions():
    score = 0
    with open('question.json', 'r') as f:
        j = json.load(f)
        for i in range(20):
            no_of_questions = len(j)
            ch = random.randint(0, no_of_questions-1)
            a = j[ch]['correct_answer']
            b = j[ch]['incorrect_answers']
            b.append(a)
            print(f'\nQ{i+1} {j[ch]["question"]}\n')
            for option in b:
                print(option)

            answer = input('\nEnter your answer: ')
            if j[ch]['correct_answer'][0] == answer[0].upper():
                print('\nYou are correct')
                score += 1
            else:
                 print('\nYou are incorrect')

            del j[ch]
            
        print(f'\nFINAL SCORE: {score}')
        play_again()


def play_again():
    print(f' Play Again?\n'
          f' 1. Yes\n'
          f' 2. No\n')
    choice = input('Enter: ')
    if int(choice) == 1:
        no_of_questions()
    elif int(choice) == 2:
        exit()
    else:
        print('Invalid Selection')
        play_again()
