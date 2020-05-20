# IMPLEMENTATION OF A USER SYSTEM WITH LOGIN/REGISTER
# WARNING!!! THIS FEATURE IS DEPRECATED AND IS NOT USED IN THE FINAL APPLICATION.


import hashlib


class UserBase:

    def __init__(self):
        self.passwd_base = "data/users.txt"
        self.info_base = "data/user_info.txt"

    def register_user(self):
        login = input("Create a username: ")
        passwd = hashlib.sha3_256(input("Password: ").encode()).hexdigest()

        with open(self.passwd_base, mode="a") as f:
            f.write(f"{login},{passwd}\n")

    def login_user(self):
        with open(self.passwd_base, mode="r") as f:
            user_info = set(map(lambda x: tuple(x.rstrip().split(",")), f.readlines()))
            user_info = {login: passwd for login, passwd in user_info}

        login = input("Login (your username): ")
        passwd = hashlib.sha3_256(input("Password: ").encode()).hexdigest()

        if login in user_info.keys():
            if passwd == user_info[login]:
                print("Logged in!")
                return True
            else:
                print("Wrong password.")
        else:
            print("This username doesn't exist.")
        return False


if __name__ == '__main__':
    choice = input("Login or register?\n")
    if choice == "login":
        login_user()
    elif choice == "register":
        register_user()
    else:
        print("No such choice.")
