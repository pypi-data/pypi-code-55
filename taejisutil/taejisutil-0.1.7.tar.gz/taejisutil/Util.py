import sys
import time
import datetime as dt

class Util:
    @classmethod
    def wait(self, until, withTimerDisplay=True):
        print ('wait task until '+until.strftime('%Y-%m-%d %H:%M:%S'+' :'))
        if withTimerDisplay == True:
            now = dt.datetime.now()
            while until > now:
                Util.prompt(now.strftime('%Y-%m-%d %H:%M:%S'))
                time.sleep(1)
                now = dt.datetime.now()
    
    @classmethod
    def prompt(self, message):
        print ('{}\r'.format(message), end='')
        sys.stdout.flush()

if __name__ == '__main__':
    util = Util.wait(dt.datetime.now()+dt.timedelta(seconds=20))