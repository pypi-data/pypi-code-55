from .Animal import Animals
import numpy

class Cats(Animals):
    def speak(self):
        print('cat miao miao')

if __name__ == '__main__':
    cat = Cats()
    cat.speak()
    cat.eat()