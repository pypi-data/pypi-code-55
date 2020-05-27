from .Animal import Animals


class Cats(Animals):
    def speak(self):
        print('cat miao miao')

if __name__ == '__main__':
    cat = Cats()
    cat.speak()
    cat.eat()