"""
This program receive a number and verify if it is prime or not
"""


def number_is_prime(n):
    numbers = list(range(2, n))
    for v in numbers:
        if (n/v).is_integer() is False:
            point = 'Es un numero primo'
        else:
            point = 'No es primo'
            break
    return point


print('Digite un Número')
x = input()
print(number_is_prime(int(x)))
