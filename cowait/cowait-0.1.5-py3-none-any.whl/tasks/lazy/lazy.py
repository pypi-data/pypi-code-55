"""
Example task: Does nothing for X seconds.

Inputs:
    duration (int): Number of seconds to sleep

Outputs:
    duration (int): Number of seconds slept
"""
import time

class Lazy(object):
    def run(self):
        print('sleeping...')
        duration = 5 # todo: options

        for i in range(0, int(duration)):
            print(i+1)
            time.sleep(1)

        print('done being lazy', flush=True)

        return {
            'duration': duration
        }