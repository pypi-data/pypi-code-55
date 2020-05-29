import smtplib, ssl
import json
import string
import random
import os
from twilio.rest import Client
import time
from termcolor import colored
from pyfiglet import figlet_format
import configparser


class Alerts:
    with open("forwardAlert4/posts.json") as post:
        if os.path.getsize("forwardAlert4/posts.json") != 0:
            JOB_POSTS = json.load(post)     # To make sure posts from previous users are not overwritten
        else:
            JOB_POSTS = {}
            JOB_POSTS["alerts"] =[]    # If there are no posts, then this would instantiated

    def __init__(self, title, body, location, company, user):
        self._title = title
        self._body = body
        self._location = location
        self._company = company
        self._user = user
        self._store_alert()
    
    def _store_alert(self):
        user_alert = {}
        user_alert["title"] = self._title
        user_alert["body"] = self._body
        user_alert["user"] = self._user
        user_alert["company"] = self._company
        user_alert["location"] = self._location
        Alerts.JOB_POSTS["alerts"].append(user_alert)
        with open("forwardAlert4/posts.json", "w") as posts:
            json.dump(Alerts.JOB_POSTS, posts)
        print(colored("Alert noted, thank you", "red"))

    def get_alert(self):
        alerts = []
        print("\t\t\t\tFind an alert")
        keyword = input(colored("What is the keyword\n> ", "yellow")).lower()
        with open("forwardAlert4/posts.json", "r") as posts:
            posts = json.load(posts)
            for alert in posts["alerts"]:
                alert_values = " ".join(list(alert.values())).lower()
                if alert_values.find(keyword) != -1:
                    alerts.append(alert)
            if len(alerts) != 0: 
                for alert in alerts:                   
                    for key, values in alert.items():
                        print(f"\t\t{key}: {values}")
                        time.sleep(0.3)
                    print()
            else:
                print(colored("None exists", "red"))
    
    def get_last_post(self):
        with open("forwardAlert4/posts.json", "r") as posts:
            posts = json.load(posts)
            last_alert = posts["alerts"][-1]
            return last_alert


    def show_all_alerts(self):
        """"Display all fake job alerts"""
        if os.path.getsize("forwardAlert4/posts.json") == 0:
            print(colored("\t\t\tNothing here to see", "red"))
        else:
            with open("forwardAlert4/posts.json", "r") as posts:
                posts = json.load(posts)
                print("All Recent Posts")
                for alert in posts["alerts"]:
                    for key, value in alert.items():
                        print(f"\t\t{key}: {value}")
                    print()
                    time.sleep(0.5)
    

class Notifications:
    """"

    Gets all available email addresses and the phone numbers from the  registered users
    and sends all mails and sms respectively upon new post update

    """
    def __init__(self):
        """Initialises the Email host paramters and reciepients"""
        self._config = configparser.ConfigParser()
        self._recipients = []
        self._host = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
        self._port = os.environ.get("EMAIL_PORT", "587")
        self._config.read("test.ini")
        self._host_user = self._config["default"]["email_host_user"]
        self._host_pass = self._config["default"]["email_host_password"]
        self._phone = self._config["default"]["twilio_phone"]
        self._account_sid = self._config["default"]["twilio_sid"]
        self._twilio_token = self._config["default"]["twilio_token"]


    def get_numbers_or_emails(self, name):
        """A function to populate the recipient's list with either emails or phone numbers"""
        with open("forwardAlert4/users.json", "r") as users:
            users = json.load(users)
            for value in users["account"]:
                self._recipients.append(value[name]) # use either phone or email

    def send_email(self):
        """Send email to each registered user"""
        recent_alert = Alerts.get_last_post(self)
        self.get_numbers_or_emails("email")
        context = ssl.create_default_context()

        with smtplib.SMTP(self._host, self._port) as server:
            server.starttls(context=context)
            server.ehlo() 
            server.login(self._host_user, self._host_pass)
            message = f'''
            Hey,

            There is a new update on the fake job alerts
            NEW ALERTS
            {recent_alert["title"].upper()}
            {recent_alert["body"]}
            
            written by {recent_alert["user"]}

            '''            
            for email in self._recipients:
                server.sendmail(self._host_user , email, message)
        
    def send_sms(self):
        """Send sms to each registered user"""
        client = Client(self._account_sid, self._twilio_token)
        self.get_numbers_or_emails("phone")
        for phone in self._recipients:
            phone = "+234" + f"{phone}"
            client.messages.create(to=phone, from_=self._phone, body="Hey, there is a new alert, log in to see")


class User:
    """A user class to simulate the user"""
    with open("forwardAlert4/users.json") as user:
        if os.path.getsize("forwardAlert4/users.json") != 0:
            USER_DETAILS = json.load(user)     # To make sure user details are not overwritten
        else:
            USER_DETAILS = {}
            USER_DETAILS["account"] =[]

    def __init__(self):
        """Initialize the staff details to none. Useful for session"""
        self._username = None
        self._password = None 
        self._logged_in = False
        print(colored(figlet_format("ALERTS FORUM", font="slant"), "green"))
        print(colored("\t\t\t\tWelcome to Forward4-Alerts", "yellow"))
        self._start()

    def _start(self):
        """Start the simulation"""
        print( colored("""
        1. Register
        2. Log in 
        3. Close App
        """, "blue"))
        response = ""
        while response == "" or response > 3:
            try:
                response = int(input("\n> "))
            except:
                print("Value should be a number")
        else:
            if response == 1:
                self._register_user()
            elif response == 2:
                self.log_in_user()
            else:
                self.close_app()
   
    def _register_user(self):
        print(""" Create a new account""")
        details = {}
        details["first_name"] = input(colored("First name\n> ", "yellow"))
        details["last_name"] = input(colored("Last name\n> ", "yellow"))
        details["username"] = input(colored("Choose a username\n> ", "yellow"))
        details["email"] = input(colored("Email Address\n> ", "yellow"))
        try:
            details["phone"] = int(input(colored("Phone\n> ", "yellow")))
        except:
            print("Wrong value, please enter phone number")
            details["phone"] = int(input(colored("Phone\n> ", "yellow")))
        details["password"]  = self._password_generator(details["first_name"], details["last_name"])
        User.USER_DETAILS["account"].append(details)

        try:
            with open("forwardAlert4/users.json", "w") as customer:
                json.dump(User.USER_DETAILS, customer)
            print("Account creation was successful, Please log in")
            self.log_in_user()
        except:
            print("Something went wrong, try again")
            self._register_user()

    def _password_generator(self, first_name, last_name):
        """Generates passord for each user upon registration"""
        all_string = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase
        rand = "".join(random.choice(all_string) for i in range(5))
        password =  first_name[:4] + rand + last_name[-3:]
        print(colored(f"""
        This is your generated password. Do well to copy
        {password}
        """, "red"))

        return password

    def log_in_user(self):
        """Authenticate and logs in the user """
        print("\tPlease log in to your account")
        tries = 3
        print("Please input the correct details")
        if os.path.getsize("forwardAlert4/users.json") == 0:
            print(colored("No user exists, please create an account", "red"))
            self._register_user()
            
        else:
            while not self._logged_in and tries > 0:
                print(f"Note: you have {colored(tries, 'red')} tries")
                username = input(colored("What is your username ", "yellow")).lower()
                password = input(colored("Please input your password ", "yellow"))
                with open("forwardAlert4/users.json", "r") as user_account:
                    staff = json.load(user_account)
                    for user in staff["account"]:
                        if username == user["username"].lower() and password == user["password"]:
                            self._username = username
                            self._password = password
                            self._logged_in = True
                            print("Login successful")
                            break
                        else:
                            self._logged_in = False
                    if not self._logged_in:
                        print("Wrong details")
                tries -=  1
            else:
                if tries == 0 and not self._logged_in:
                    print("\t\tPlease create a new account as you can't access this")
                    self._start()
                else:                
                    self._create_session(action="logged in")
                    self._show_account_settings()

    def _show_account_settings(self):
        """ Actions to be perform on the account"""
        print(colored(f"""\t\t\t\t Welcome, {self._username}
        1. Create a new post
        2. Search alerts
        3. Show all alerts
        4. Logout
        """, "blue"))
        response = ""
        while response == "" or response > 4:
            try:
                response = int(input("\n> "))
            except:
                print("Value should be a number between 1 and 4")
        else:
            if response == 1:
                self._create_post()
            elif response == 2:
                self.get_posts()
            elif response == 3:
                self.display_all_posts()
            else:  
                self.logout()

    def display_all_posts(self):
        Alerts.show_all_alerts(self)
        print("What else do you want to do? ")
        self._show_account_settings()

    def logout(self):
        """Logs out user and deletes session files"""
        os.remove(f"forwardAlert4/{self._username}.txt")
        self._username, self._password, self._logged_in = None, None, False
        self._start()

    def get_posts(self):
        """"Search out instances of a particualar post"""
        Alerts.get_alert(self)
        self._show_account_settings()

       
    def _create_session(self, action=None):
        """This creates a session as the staff performs an action"""
        with open(f"forwardAlert4/{self._username}.txt", "a") as session:
            session.write(f"{self._username} {action} \n")

    def _create_post(self):
        """"Create a new alert and trigger the email module"""
        print("\t\t\t\tPost an alert")
        title = input(colored("Subject\n> ", "yellow"))
        body = input(colored("Message\n> ", "yellow"))
        location = input(colored("Location\n> ", "yellow"))
        company = input(colored("Company's Details\n> ", "yellow"))
        Alerts(title=title, body=body, location=location, company=company, user=self._username)
        try:
            p = Notifications()
            p.send_sms()
            p.send_email()
        except Exception as e :
            print(f"Error sending alerts {e}")
        self._show_account_settings()
        
    def close_app(self):
        """Close app"""
        print("Bye, bye. Come back next time")
        return 0


