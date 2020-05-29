from messages import message_log

message1 = 'login succesful'
message2 = 'login not successful please try again'


def collect_user_details():
    '''
    input:
        user details
    output:

    '''
    global username
    global password
    username = input('Username:\n')
    password = input('Password\n')
    return username, password


def user_reg_details(file):
    '''
    this functions is been called whenever an id confirmation is to take place e.g login checks
    input:
        the csv file to be read
    output:
        variable containing user details
    '''
    user_details1 = [line.strip() for line in open(file, 'r')]
    user_details2 = [m.split(' ') for m in user_details1]
    for i in user_details2:
        if len(i) == 3:
            user_details2.remove(i)
        elif i == ['']:
            user_details2.remove(i)
        else:
            continue
    user_details_dictionary = dict(user_details2)
    d = user_details_dictionary  # d is a variable used to store user details in a clean dictionary
    return d


def login_user():
    '''This feature collects user details and check if details are valid before proceeding further.
    input:
        username and password of user
    output:
        validation
    '''
    collect_user_details()
    d = user_reg_details('UserRegister.txt')
    if (password == d['password']) and (username == d['username']):
        return True
    else:
        return False

