from datetime import datetime, timedelta
import time

class Butt:
    def __init__(self, butt_date):
        self.butt_date = butt_date

    def checkIt(self):
        butt_date = self.butt_date
        now = datetime.now()
        butt_age = now - butt_date
        print(f"This butt's been around for {butt_age.days} days")
        if butt_age.days > 300:
            print("It's too much dude, just throw it")
        elif butt_age.days > 90:
            print("I don't know man, doesn't seem right")
        else:
            print("give me a puff.")

butt_please = Butt(datetime(1983, 1, 12))
butt_please.checkIt()