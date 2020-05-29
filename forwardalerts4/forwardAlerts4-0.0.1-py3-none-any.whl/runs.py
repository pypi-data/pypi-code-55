from alerts import Notifications, Alerts, User
import configparser
import os



if __name__ == "__main__":
    if not os.path.exists("test.ini") or os.path.getsize("test.ini") == 0:
        config = configparser.ConfigParser()
        config["default"] = {}
        print("This is needed to be done only once")
        config["default"]["EMAIL_HOST_USER"] = input("Please input an email host address\n> ")
        config["default"]["EMAIL_HOST_PASSWORD"] = input("Password\n> ")
        config["default"]["twilio_phone"] = input("Twilio phone no\n> ")
        config["default"]["twilio_sid"] = input("Twilio SID no\n> ")
        config["default"]["twilio_token"] = input("Twilio Token\n> ")
        with open("test.ini", "w+") as cfg:
            config.write(cfg)

    p = User()
