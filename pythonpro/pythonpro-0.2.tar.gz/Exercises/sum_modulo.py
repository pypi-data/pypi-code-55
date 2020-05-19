"""
This program receive many integer and adds them
"""


def sum(*args):
    total = 0
    for n in args:
        total += n
    return total
