"""
This program determines number of uppercase characters in a string
"""


def number_of_upper(n):
    count = 0
    for value in n:
        if value.isupper():
            count += 1
    return count


print(number_of_upper('Alfonso AreizA GUeRRa'))
