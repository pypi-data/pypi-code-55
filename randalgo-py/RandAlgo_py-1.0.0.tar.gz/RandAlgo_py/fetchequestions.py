from messages import message_log
message5 = 'invalid response, enter a valid number, (e.g 10)'
message3 = 'invalid response, respond with 1, or 2'
message6 = 'please get an internet connection'


def webcrawl_site(x):
    '''This function actually serves as the API since we could'nt get one
    input:
       integer value entered by the user
    output:
        Number of questions displayed as requested by the user
    '''
    from bs4 import BeautifulSoup
    import requests
    import csv
    from random import randint

    for x in range(1, x+1):
        source = requests.get(f'https://projecteuler.net/problem={randint(1, 150)}').text
        soup = BeautifulSoup(source, 'lxml')
        content = soup.find('div', id='content').text
        print(content)
        print()
    return content


def fetch_algo_questions():
    '''This fuction allows user to input the amount of question they want and in turn returns algorithm
    questions
    input:
        integer value within a specified range
    output:
        algoruthm questions in the requested amount
    '''
    while True:
        try:
            number = int(input('How many questions do you want?\n'))
        except NameError:
            message_log(message5)
            break
        except ValueError:
            message_log(message5)
            break
        except SyntaxError:
            message_log(message5)
            break
        question = input('Are you sure connected to the internet?,(yes/no)\n')
        #question is used to put user on check if he has an internet connection
        if question == 'yes':
            question = True
        else:
            question = False

        if question == True:
            webcrawl_site(number)
            break
        else:
            message_log(message6)
            break


def give_user_question():
    '''
    This funtion comes to play when user wants to repeat action'''
    while True:
        try:
            user_action = eval(input('1 Get Question\n2 Logout\n'))
        except NameError:
            message_log(message3)
            continue
        except ValueError:
            message_log(message3)
            continue
        except SyntaxError:
            message_log(message3)
            continue
        if user_action == 1:
            fetch_algo_questions()
        elif user_action == 2:
            break
        else:
            continue

