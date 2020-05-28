import getpass
from termcolor import colored
from pusher import Pusher
import pysher
from dotenv import load_dotenv
import os
import json
import random
import string
import re

load_dotenv(dotenv_path='.env')

class gossip():
    pusher = None
    channel = None
    chatroom = None
    clientPusher = None
    user = None
    users=()
   
    chatrooms = ["Python", "Java", "C#", "C++", "Javascript", "New languages", "General"]

    ''' The entry point of the application'''
    def main(self):
        print("\n")     
        print(colored("        ---- DevGossip ----      ", "blue"))
        print(colored("*********************************", "blue"))
        print(colored("<< 1. Signup                 >>", "yellow"))
        print(colored("<< 2. Login                  >>", "yellow"))
        print(colored("<< 3. close App              >>", "yellow"))
        
        selection = input("Please choose a number from the options above: ")


        if selection == str(1):
            self.signup()
            self.main()
        elif selection == str(2):
            self.login()
            while True:
                self.logged()
        elif selection == str(3):
            self.closeApp()
        else:
            print("Please input '1' to signup; '2' to login or '3' to close the app")
            self.main()

    ''' This function handles signup to the system'''
    def signup(self):
        print("\n")
        print("Please pres Ctrl+c at anytime to cancel signup and go back to Welcome page")        
        try:
            while True:
                userName= input('Please choose a Username: ')
                if not userName.isalpha():
                    print("Your username must consist of letters only.")
                    continue
                else:
                    break
                
            while True:
                passWord= input('Please choose a password: ')
                break

            while True:
                email_add = input('Email Address: ')
                match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email_add)
                if match == None:
                    print('Invalid email address')
                    continue
                else:
                    break
                
            print("Your registration is complete. Please login")

            with open(f'userDetails.txt', 'a+') as users:
                for details in [userName, passWord, email_add]:
                    users.write(f"{details} ",)
                users.write('\n')
        
        except KeyboardInterrupt:
            print("Registration was cancelled.")
            self.main()


        

    ''' This function handles logon to the system'''

    def login(self):
        print("\n")
        print("Please pres Ctrl+c at anytime to cancel 'Login' and go back to Welcome page")        
        try:
            file = open("userDetails.txt")
            users = file.read().strip().split()
            username = input("Please enter your username: ")
            password = input("Please enter %s's Password:" % username)
            #while True:
            if username in users:
                if password in users:
                    self.user = username
                    #break
                else:
                    print(colored("Your password is incorrect", "red"))
                    self.login()
            else:
                print(colored("Your username is incorrect", "red"))
                self.login()

        except KeyboardInterrupt:
            print("Login was terminated")
            self.main()

    '''To close the app'''
    def closeApp(self):
        exit()

    
    def logged(self):
        print("\n")        
        print(colored("You're logged in   ", "blue"))
        print(colored("<< 1. Logout                        >>", "yellow"))
        print(colored("<< 2. Choose a room                 >>", "yellow"))
        print(colored("<< 3. Delete your account           >>", "yellow"))
        
        selection = input("Please choose a number from the options above: ")


        if selection == str(1):
            print("You are logged out")
            self.main()
        elif selection == str(2):
            self.selectChatroom()
            while True:
                self.getInput()
        elif selection == str(3):
            self.del_users()
        else:
            print("Please input '1' to Logout; '2' to Choose a room or '3' to delete your account")
            self.logged()

    #=======================================================================================

    ''' This function is used to select which chatroom you would like to connect to '''
    def selectChatroom(self):
        print("\n")
        print("Please pres Ctrl+c at anytime to exit the Room")        
        print(colored("Info! Available Rooms are %s" % str(self.chatrooms), "blue"))
        chatroom = input(colored("Please select a Room: ", "green")).capitalize()
        if chatroom in self.chatrooms:
            self.chatroom = chatroom
            self.initPusher()
        else:
            print(colored("No such Room in our list", "red"))
            self.selectChatroom()

   
    ''' This function initialises both the Http server Pusher as well as the clientPusher'''
    def initPusher(self):
        self.pusher = Pusher(app_id=os.getenv('PUSHER_APP_ID', None), key=os.getenv('PUSHER_APP_KEY', None), secret=os.getenv('PUSHER_APP_SECRET', None), cluster=os.getenv('PUSHER_APP_CLUSTER', None))
        self.clientPusher = pysher.Pusher(os.getenv('PUSHER_APP_KEY', None), os.getenv('PUSHER_APP_CLUSTER', None))
        self.clientPusher.connection.bind('pusher:connection_established', self.connectHandler)
        self.clientPusher.connect()
        
    ''' This function is called once pusher has succesfully established a connection'''
    def connectHandler(self, data):
        self.channel = self.clientPusher.subscribe(self.chatroom)
        self.channel.bind('newmessage', self.pusherCallback)
    
    ''' This function is called once pusher recieves a new event '''
    def pusherCallback(self, message):
        message = json.loads(message)
        if message['user'] != self.user:
            print(colored("{}: {}".format(message['user'], message['message']), "blue"))
            print(colored("{}: ".format(self.user), "green"))
    
    ''' This function is used to get the user's current message '''
    def getInput(self):
        try:
            message = input(colored("{}: ".format(self.user), "green"))
            self.pusher.trigger(self.chatroom, u'newmessage', {"user": self.user, "message": message})
        except KeyboardInterrupt:
            self.logged()
    
    #===========================================================================================================================

    def del_users(self):
        print("\n")
        print("Please pres Ctrl+c to terminate this process")   
        try:
            yn = input("Are you sure? Y/N: ").lower()
            if yn =='y':
                del_user = input("Please input your username: ")
                with open("userDetails.txt", "r+") as f:
                    d = f.readlines()
                    f.seek(0)
                    for line in d:
                        if del_user not in line:
                            f.write(line)
                    f.truncate()
                print("Your account has been deleted")
                self.main()
            elif yn == 'n':
                self.logged()
        except KeyboardInterrupt:
            self.logged()
            
if __name__ == "__main__":
    gossip().main()
