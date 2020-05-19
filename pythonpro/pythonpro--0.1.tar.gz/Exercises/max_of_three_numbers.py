"""
Highest number of a tuple
"""


def max_of_3_numbers_op1(args):
    num_anterior = args[0]
    for valor in args:
        if valor > num_anterior:
            maxnumber = valor
            num_anterior = valor

    return maxnumber


def max_of_3_numbers_op2(args):
    return max(args)


tpl = (1, 5, 4, 10, 7, 22)
print(max_of_3_numbers_op1(tpl))
print(max_of_3_numbers_op2(tpl))
