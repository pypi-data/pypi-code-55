"""
Given a number, is calculated it is reduced to zero by certain logic. In addition the steps
are counted until reaching zero
Input: num = 14
Output: 6
Explanation:
Step 1) 14 es par; divide by 2 and obtain 7.
Step 2) 7 es impar; subtract 1 and obtain 6.
Step 3) 6 es par; divide by 2 and obtain 3.
Step 4) 3 es impar; subtract 1 and obtain 2.
Step 5) 2 es par; divide by 2 and obtain 1.
Step 6) 1 es impar; subtract 1 and obtain 0."""


def numberOfSteps(num):
    """
    :type num: int
    :rtype: int
    """
    count = 1
    while num != 0:
        if num % 2 == 0:
            print(f'Step {count}. {int(num)} es par; dividido por 2 se obtiene el {int(num/2)}.')
            num = num/2
            count += 1
        else:
            print(f'Step {count}. {int(num)} es impar; menos 1 se obtiene el {int(num - 1)}.')
            num = num - 1
            count += 1
    return


print('↓ Digita un Número Positivo ↓')
num = input()
numberOfSteps(int(num))
