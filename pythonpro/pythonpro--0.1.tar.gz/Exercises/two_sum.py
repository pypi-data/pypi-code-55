"""
Given a list and a target, this program calculate all the combinations possible of summatory
between two numbers up to the target.
Ex:
Input :  6
Output: [1,5]
        [2,4]
"""


def sumfrominput(numbers, target):
    resultTemp = []
    result = []
    for i, v in enumerate(numbers):
        for j, p in enumerate(numbers):
            if j > i:
                if int(v) + int(p) == target:
                    resultTemp = [v, p]
                    result.append(resultTemp)
    return result


numbers = list(range(1, 101))
target = int(input('Digit a number target : '))
totalNumbers = sumfrominput(numbers, target)
for i, v in enumerate(totalNumbers):
    print(totalNumbers[i])
