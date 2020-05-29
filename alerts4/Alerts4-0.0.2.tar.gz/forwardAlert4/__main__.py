from .alerts import Notifications, Alerts, User
import configparser
import os

def main():
   
    if not os.path.exists("test.ini") or os.path.getsize("test.ini") == 0:
        config = configparser.ConfigParser()
        config["default"] = {}
        print("This is needed to be done only once")
        print("\tPlease note that this data can only be entered once. Please give care for accuracy")
        config["default"]["EMAIL_HOST_USER"] = input("Please input an email host address\n> ")
        config["default"]["EMAIL_HOST_PASSWORD"] = input("Password\n> ")
        config["default"]["twilio_phone"] = input("Twilio phone no\n> ")
        config["default"]["twilio_sid"] = input("Twilio SID no\n> ")
        config["default"]["twilio_token"] = input("Twilio Token\n> ")
        with open("test.ini", "w+") as cfg:
            config.write(cfg)

    p = User()

if __name__ == "__main__":
    main()
