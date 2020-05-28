from termcolor import colored
from pusher import Pusher
import pysher
from dotenv import load_dotenv
import os
import json
import random
import string
import re

from devgossip import login, closeApp, logged, selectChatroom, initPusher, connectHandler, pusherCallback, getInput, del_users

load_dotenv(dotenv_path='.env')

class  gossip():
    pusher = None
    channel = None
    chatroom = None
    clientPusher = None
    user = None
    users=()
   
    chatrooms = ["Python", "Java", "C#", "C++", "Javascript", "New languages", "General"]
    print("Welcome to Devgossip")

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

if __name__ == "__main__":
    gossip().main()