# from welcome import signup, login, create_anon_post, close_app
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


user = []


# User sign up function
def signup():
    global username
    username = input('Enter your username: ')
    password = input('Password should be at least 8 characters: ')
    while len(password) < 8:
        print('Password should be at least 8 characters. Try again.')
        password = input('> ')
    else:
        print(f'Username: {username} and Password: {password} saved!')
    user.append(username)
    user.append(password)

    # Saving user details to .txt file
    with open('users.txt', 'w+') as file:
        file.writelines('%s ' % line for line in user)
    print('Signup successful! Please log in to continue.')
    return login()


# User login function
def login():
    while login:
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        with open('users.txt', 'r') as file:
            for row in file:
                a = row.split()
                username1 = str(a[0])
                password1 = str(a[1])
                while username != username1 and password != password1:
                    print('Invalid username or password, please try again.')
                    username = input('Enter your id code: ')
                    password = input('Enter your password: ')
                    # break
                else:
                    print('Login successful')
                    return login_options()
                    # break


# While User is logged in
def login_options():
    print('A. Create New Post \nB. View all Posts \nC.Logout')
    login_choice = input('Choose an action(A/B): ').upper()
    while login_choice != 'A' and login_choice != 'B' and login_choice != 'C':
        print('Invalid choice')
        login_choice = input('Enter A or B: ').upper()

    else:
        if login_choice == 'A':
            return create_gossip()
        elif login_choice == 'B':
            return check_gossip()
        elif login_choice == 'C':
            return logged_out()


def create_gossip():
    print('What\'s happening?')
    new_post = input('>> ')
    with open('gossip.txt', 'a') as f:
        f.write(f'\n{username} posted at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: {new_post}')
    print('Your post has been published!')
    print('What would you like to do? \nA. View Posts \nB. Logout')
    new_choice = input('>> ').upper()
    while new_choice != 'A' and new_choice != 'B':
        print('Please choose a valid option')
        new_choice = input('>> ')
    else:
        if new_choice == 'A':
            return check_gossip()
        elif new_choice == 'B':
            return logged_out()


def check_gossip():
    with open('gossip.txt', 'r') as new_file:
        all_posts = new_file.read()
        print(all_posts)

    print('What would you like to do? A. Create New Post \nB. Logout')
    new_choice = input('>> ').upper()
    while new_choice != 'A' and new_choice != 'B':
        print('Please choose a valid option')
        new_choice = input('>> ')
    else:
        if new_choice == 'A':
            return create_gossip()
        elif new_choice == 'B':
            return logged_out()


def create_anon_post():
    print('What\'s happening?')
    while True:
        anon_post = input('>> ')
        with open('posts.txt', 'a') as file:
            file.write(f'\nanonymous posted at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: {anon_post}')
        print('Your post has been published!')


# User logout function
def logged_out():
    print('You have been logged out!')
    print('\nWhat would you like to do? \nA. Sign Up \nB. Log in \nC. Post as anonymous \nD. Close App')
    new_user_choice = input('>> ').upper()
    choose = ['A', 'B', 'C', 'D']
    while new_user_choice not in choose:
        print('Invalid action')
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

