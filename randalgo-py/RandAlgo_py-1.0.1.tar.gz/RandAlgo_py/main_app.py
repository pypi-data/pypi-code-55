from user_registration import register_user
from user_login import login_user
from fetchequestions import give_user_question
from messages import message_log

message4 = 'invalid response, respond with 1, 2, or 3'
message7 = 'Welcome to RandAlgo console, looking for Algorithm questions? we got you'
message8 = 'Please login'
message1 = 'login successful'
message2 = 'login unsuccessful, please check username and password then 1try again'


def main_app():
    '''This function calls and integrate everyother function in the CLI to enable users run them
    '''
    message_log(message7)
    while True:
        try:
            user_action = eval(input('1 Register\n2 Login\n3 Quit App\n')) # user_action is the variable that collects the useraction
        except NameError:
            message_log(message4)
            continue
        except ValueError:
            message_log(message4)
            continue
        except SyntaxError:
            message_log(message4)
            continue
        if user_action == 1:
            register_user()
            message_log(message8)
            if login_user():
                message_log(message1)
                give_user_question()
            else:
                message_log(message2)
                continue
        elif user_action == 2:
            if login_user():
                message_log(message1)
                give_user_question()
            else:
                message_log(message2)
                continue
        elif user_action == 3:
            break
        else:
            message_log(message4)
            continue

