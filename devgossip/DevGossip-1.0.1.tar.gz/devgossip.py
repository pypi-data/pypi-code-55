import time

ts = time.gmtime()



print("WELCOME TO STARTNG DISCUSSION PLATFORM")
print("*" * 38)


def register_user():
    choice = str(input('Are you a New user?: ')).lower()
    if choice == 'yes':
        capture_user()
    elif choice == 'no':
        user_login()
    else:
        print('Invalid Option. Please type yes or no')
        register_user()


def capture_user():
    print('Please fill details to create your user profile')
    staff_name = str(input('Enter your full name: '))
    email = str(input('Enter your email: '))
    username = str(input('Enter your username: ')).lower()
    password = str(input('Enter Password of 8 characters: '))
    if len(password) != 8:
        print('Password must be 8 characters')
        password = str(input('Enter a maximum of 8 characters: '))
    user_info = open('user_details.txt', 'a')
    user_info.write('\n'+ username + ',' + password + ',' + email + ',' + staff_name)
    user_info.close()
    user_login()


def user_login():
    print('Please put in your login details')
    username = str(input('username: ')).lower()
    password = str(input('password: '))
    with open('user_details.txt', 'r') as file:
        content = file.read()
        if username in content and password in content:
            print('Login Successful')
            session_choice()
        else:
            print('Login Details Incorrect')
            user_login()


def log_out():
    print('Do you want to exit? Yes or No')
    logout = str(input('>>: ')).lower()
    if logout == 'yes':
        print('App Closed. Thank you')
    elif logout == 'no':
        session_choice()
    else:
        print('Invalid Choice. Please choose Yes or No')
        log_out()


def session_choice():
    choice = int(input('Please select an option:\n1.Start a Discussion \n2.Comment on a Discussion \n3.Exit App\n:>>> '))
    if choice == 1:
        start_disc()
    elif choice == 2:
        comment_disc()
    elif choice ==3:
        log_out()


def start_disc():
    username = str(input('Enter your username: ')).lower()
    date = time.strftime('%x %X', ts)
    my_discuss = str(input('write here>:  ')).lower()
    with open('discussion_board.txt','a+') as start_chat:
        start_chat.write('\n'+ username + '___' + date + '___' + my_discuss)
    with open('discussion_board.txt', 'r') as file:
        display_chat = file.read()
        print(display_chat)
        another_discuss = str(input('Do you want to start another discussion? Yes or No: ')).lower()
        if another_discuss == 'yes':
            start_disc()
        elif another_discuss == 'no':
            log_out()
        else:
            print('Invalid Choice. Please choose Yes or No')
            log_out()


def comment_disc():
    with open('discussion_board.txt', 'r+') as file:
        disc_list = file.read()
        print(disc_list)
        print('Choose the discussion you want to comment on')
        post_username = str(input('post username: ')).lower()
        post_date = str(input('date of post: '))
        with open('discussion_board.txt', 'r') as f:
            comment_line = f.read()
            if post_username in comment_line and post_date in comment_line:
                username = str(input('Enter your username: ')).lower()
                date = time.strftime('%x %X', ts)
                my_comment = str(input('write your comment here>: ')).lower()
                with open('discussion_board.txt', 'a+') as comment_chat:
                    comment_chat.write('\n comment on post by___' + post_username + '___' + post_date+':')
                    comment_chat.write('\n___________' + username + '___' + date + '___' + my_comment)
                with open('discussion_board.txt', 'r') as cf:
                    display_chat = cf.read()
                    print(display_chat)
                    another_comment = str(input('Do you want to make another comment? Yes or No: ')).lower()
                    if another_comment == 'yes':
                        comment_disc()
                    elif another_comment == 'no':
                        session_choice()
                    else:
                        print('Invalid Choice. Please choose Yes or No')
                        log_out()

register_user()