from datetime import datetime


def print_logg(msg):
    print(str(datetime.now().time().replace(microsecond=0)) + 5*' ' + msg)
