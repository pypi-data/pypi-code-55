from CodePackage import Animal


class Cat(Animal.Animal):
    def speak(self):
        print('cat miao miao')

if __name__ == '__main__':
    cat = Cat()
    cat.speak()