
def collect_user_details():
    '''
    this function collects and returns details of the user
    input:
        user response to first prompt when they install app
    output:
        user_registration file after details are been entered
    '''
    global first_name
    first_name = input('Firstname:\n')
    global last_name
    last_name = input('Lastname:\n')
    global e_mail
    e_mail = input('E-mail:\n')
    global username
    username = input('Username:\n')
    global password
    password = input('password:\n')
    return first_name, last_name, e_mail, username, password


def create_user_details_file(first_name, last_name, e_mail, username, password):
    '''This function creates a file in the local machine of the user, onceuser finishes registration
input:
    user details like name, username, and password
output:
    csv file containing user details
'''
    global file1
    with open('UserRegister.txt', 'w') as file1:
        '''the file UserRegister.txt is the csv file that will be created on users local machine to
        hold user details in case for login purposes'''
        file1.write(f'''fullname {first_name}
last {last_name}
e-mail {e_mail}
username {username}
password {password}
        ''')
    file1.close()
    return file1


def register_user():
    '''this file collaborates the above functions and register users successfully
'''
    collect_user_details()
    create_user_details_file(first_name, last_name, e_mail, username, password)
    return file1


