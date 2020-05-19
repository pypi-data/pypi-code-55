"""
Exercise #31 of https://www.w3resource.com/python-exercises/python-conditional-statements-and-loop-exercises.php
Write a Python program to calculate a dog's age in dog's years.
Note: For the first two years, a dog year is equal to 10.5 human years. After that, each dog year equals 4 human years.
Expected Output:
    Input a dog's age in human years: 15
    The dog's age in dog's years is 73
>>> calc_dog_age(15)
73
"""


def calc_dog_age(age):
    if age <= 0:
        return 'Age must be positive'
        exit()
    elif age <= 2:
        return age * 10.5
    else:
        return 21+(age-2)*4


if __name__ == '__main__':
    age = int(input("Input a dog's age in human years : "))
    print(calc_dog_age(age))
