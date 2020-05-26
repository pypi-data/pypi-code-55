# class FortuneCookie:

    # def __init__(self):
with open('../dataset/mymind.dat') as ds:
    lines = ds.readlines()
    myfortune = ""

    def creck():
        import random
        key = random.randint(0,len(lines))
        print(lines[key])
        return

# if __name__ == '__main__':
# cookie = FortuneCookie()
# cookie.creck()


creck()
