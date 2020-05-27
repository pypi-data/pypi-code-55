
print("this can be cool")
'''
test-pypi access token
pypi-AgENdGVzdC5weXBpLm9yZwIkMzAzNmYxYjgtNmQ5MS00MzBlLTg0NDYtMGM3MzVhMzg3YzkxAAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiC67Ik1md3HMQ8Bx0zVBEs0Ay8YGLbvUSTh5STB5dlLLg
'''


class User:
    def __init__(self, username, name):
        self.username = username
        self.name = name

    def greet(self):
        print(f"Yo what the fuck @{self.username}, {self.name}")


bro1 = User('onebro', 'one')
bro2 = User('twobro', 'two')

bro1.greet()
bro2.greet()
