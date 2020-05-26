import pandas as pd
import random



class FortuneCookie:

    def __init__(self):


        url = 'https://raw.githubusercontent.com/rafaelstojoao/fortcookie/master/dataset/mymind.csv'
        data = pd.read_csv(url, error_bad_lines=False)
        self.lines = str(data).split(',')
        self.myfortune = ""

    def creck(self):
        key = random.randint(0,len(self.lines))
        print(self.lines[key])
        return

if __name__ == '__main__':
    cookie = FortuneCookie()
    cookie.creck()


# creck()
