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
                print ('{}\r'.format(now.strftime('%Y-%m-%d %H:%M:%S')), end='')
                sys.stdout.flush()
                time.sleep(1)
                now = dt.datetime.now()

if __name__ == '__main__':
    util = Util.wait(dt.datetime.now()+dt.timedelta(seconds=20))