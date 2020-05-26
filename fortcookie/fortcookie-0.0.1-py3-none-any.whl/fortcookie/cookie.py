class FortuneCookie:

    def __init__(self):
        with open('../dataset/mymind.dat') as ds:
            self.lines = ds.readlines()
        self.myfortune = ""

    def creck(self):
        import random
        key = random.randint(0,len(self.lines))
        print(self.lines[key])
        return

if __name__ == '__main__':
    cookie = FortuneCookie()
    cookie.creck()

