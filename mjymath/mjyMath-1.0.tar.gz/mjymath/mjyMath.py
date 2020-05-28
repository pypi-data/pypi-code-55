"""本方法用于计算阶乘"""
def mjyMath(n):
    """
    传入一个数字后，将计算该数字的阶乘
    :param n: 传入的数字
    :return: 返回计算结果
    """

    if n == 1:
        return 1
    else:
        return n * mjyMath(n - 1)