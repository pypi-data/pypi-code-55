# from welcome import signup, login, create_anon_post, close_app
import os
import sys
from datetime import datetime

select = ['A', 'B', 'C', 'D']


def check(choice):
    if choice not in select:
        return False
    return True


def options(choice):
    if choice == 'A':
        return signup()
    elif choice == 'B':
        return login()
    elif choice == 'C':
        return create_anon_post()
    elif choice == 'D':
        return close_app()


# Functions for coloured text
user = []
global username


# User sign up function
def signup():
    username = input('Enter your username: ')
    password = input('Enter your password (Password should be at least 8 characters): ')
    while len(password) < 8:
        print('\033[1;91m Invalid! Password should be at least 8 characters. Try again.')
        password = input('> ')
    else:
        print(f'\033[1;96m Signup successful! Username: \033[1;35m {username} \033[1;96m and \033[1;96m Password: \033[1;35m {password}.')
    user.append(username)
    user.append(password)

    # Saving user details to .txt file
    with open('users.txt', 'w+') as file:
        file.writelines('%s ' % line for line in user)
    print('\033[1;33m Please log in to continue.')
    return login()


# User login function
def login():
    while login:
        login.username = input('\033[1;33m Enter your username: ')
        password = input('\033[1;33m Enter your password: ')
        with open('users.txt', 'r') as file:
            for row in file:
                a = row.split()
                username1 = str(a[0])
                password1 = str(a[1])
                print(f'{username1} {password1}')
                while login.username != username1 or password != password1:
                    print('\033[1;91m Invalid username or password, please try again.')
                    username = input('\033[1;33m Enter your username: ')
                    password = input('\033[1;33m Enter your password: ')
                    # break
                else:
                    print('\033[1;96m Login successful!')
                    return login_options()
                    # break


# While User is logged in
def login_options():
    print('\033[1;33m A. Create New Post\nB. View all Posts\nC. Search Posts \nD. Logout')
    login_choice = input('>> ').upper()
    choice = ['A', 'B', 'C', 'D']
    while login_choice not in choice:
        print('\033[1;91m Invalid option! Try again.')
        login_choice = input('\033[1;33m Enter A, B or C >> ').upper()

    else:
        if login_choice == 'A':
            return create_gossip()
        elif login_choice == 'B':
            return check_gossip()
        elif login_choice == 'C':
            return search_posts()
        elif login_choice == 'D':
            return logged_out()


def create_gossip():
    print('\033[1;96m What\'s happening?')
    new_post = input('>> ')
    with open('posts.txt', 'a') as f:
        f.write(f'{login.username} posted at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: {new_post}\n')
    print('Your post has been published!')
    print('\033[1;33m What would you like to do next?\nA. View Posts \nB. Logout')
    new_choice = input('>> ').upper()
    while new_choice != 'A' and new_choice != 'B':
        print('\033[1;91m Please choose a valid option')
        new_choice = input('\033[1;33m >> ')
    else:
        if new_choice == 'A':
            return check_gossip()
        elif new_choice == 'B':
            return logged_out()


def check_gossip():
    new_file = 'posts.txt'
    if os.stat(new_file).st_size == 0:
        print('\033[1;96m No posts yet.')
        print('\033[1;33m What would you like to do?\nA. Create New Post \nB. Logout')
        add_post = input('>> ').upper()
        while add_post != 'A' and add_post != 'B':
            print('\033[1;91m Invalid option! Try again.')
            input('\033[1;33m >> ').upper()
        else:
            if add_post == 'A':
                return create_gossip()
            elif add_post == 'B':
                return logged_out()
    else:
        with open('posts.txt', 'r') as new_file:
            all_posts = new_file.read()
            print(f'\033[1;96m {all_posts}')
    print()
    print('\033[1;33m -------------------------------------------')
    print('What would you like to do next?\nA. Create New Post \nB. Search for Posts \nC. Logout')
    new_choice = input('>> ').upper()
    choice = ['A', 'B', 'C']
    while new_choice not in choice:
        print('\033[1;91m Please choose a valid option')
        new_choice = input('>> ')
    else:
        if new_choice == 'A':
            return create_gossip()
        elif new_choice == 'B':
            return search_posts()
        elif new_choice == 'C':
            return logged_out()


def create_anon_post():
    print('\033[1;96m What\'s happening?')
    while True:
        anon_post = input('>> ')
        with open('posts.txt', 'a') as file:
            file.write(f'Anonymous posted at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: {anon_post}\n')
        print('Your post has been published! ')
        print('\033[1;33m A. Login to view all gossip \nB. Signup to create an account. \nC. Close App ')
        anon_choice = input('>> ').upper()
        choice = ['A', 'B', 'C']
        while anon_choice not in choice:
            print('\033[1;91m Please choose a valid option')
            anon_choice = input('>> ')
        else:
            if anon_choice == 'A':
                return login()
            elif anon_choice == 'B':
                return signup()
            elif anon_choice == 'C':
                return close_app()


# Search for posts using keywords
def search_posts():
    print('\033[1;33m Enter a search keyword')
    search = input('>> ')
    with open('posts.txt', 'r') as file:
        for line in file:
            while search not in line:
                print('\033[1;91m Sorry, not found.')
                search = input('Try a different keyword: ')
            else:
                print(f'\033[1;96m Posts containing \033[1;33m {search}\033[1;96m:\n{line}')
    print('\033[1;33m What would you like to do next?\nA. Create New Post\nB. View Posts\nC. Logout')
    search_choice = input('>> ')
    choice = ['A', 'B', 'C']
    while search_choice not in choice:
        print('\033[1;91m Please choose a valid option')
        search_choice = input('>> ')
    else:
        if search_choice == 'A':
            return create_gossip()
        elif search_choice == 'B':
            return check_gossip()
        elif search_choice == 'C':
            return logged_out()


# User logout function
def logged_out():
    print('\033[1;96m You have been logged out!')
    print('\n\033[1;33mWhat would you like to do? \nA. Sign Up \nB. Log in \nC. Post as anonymous \nD. Close App')
    new_user_choice = input('>> ').upper()
    choose = ['A', 'B', 'C', 'D']
    while new_user_choice not in choose:
        print('\033[1;91m Invalid action')
        new_user_choice = input('>> ')
    else:
        if new_user_choice == 'A':
            return signup()
        elif new_user_choice == 'B':
            return login()
        elif new_user_choice == 'C':
            return create_anon_post()
        elif new_user_choice == 'D':
            return close_app()


# Close application
def close_app():
    sys.exit('App closed!')

