"""
Given a list with repeated numbers, it returns to list without repeated numbers
"""


def uniqueElements(numbers):
    numbers.sort()
    numbersUnique = []
    num_anterior = numbers[0]
    for num in numbers[1::]:
        if not num_anterior == num:
            numbersUnique.append(num_anterior)
            num_anterior = num
    numbersUnique.append(num_anterior)
    return numbersUnique


numbers = [10, 1, 6, 2, 4, 3, 3, 3, 4, 4, 5, 6]
print(uniqueElements(numbers))


def unique_list(list):
    x = []
    for a in list:
        if a not in x:  # en los IF también se puede usar el 'in'
            x.append(a)
    return x


print(unique_list([1, 2, 3, 3, 3, 3, 4, 5]))
