def login():
    login_page = input('Please enter 1 or 2 to continue. 1. login 2. Close App : ')
    if login_page == "1":
        user_login()
    elif login_page == "2":
        exit()
    else:
        print("Invalid request")
        login()  # calling back the login page to show the options


def user_login():
    print("Hello there! I'm Tri_Vail, your general knowledge buddy "
          "for quiz and interview! You can always count on me")
    user_name = input(" What's your name?: ")
    print("It's nice meeting you", user_name, " I will give you a result shortly")
    print('-' * 100)
