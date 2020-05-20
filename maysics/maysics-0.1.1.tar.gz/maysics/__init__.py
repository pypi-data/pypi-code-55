'''
本库用于科学计算和快速建模

maysics主要包括六个模块：

1、algorithm 储存了几种模拟方法，用于简易模拟；
2、constant 储存了部分常数；
3、models 储存了几种常用的数学物理定律、方程、模型以便快速构建数理模型；
4、model_selection 用于评估和选择模型；
5、operator 储存了部分常见的算符算子，辅助数学运算；
6、transformation 储存了常用的坐标转换及其他数学变换。


This package is used for calculating and fast modeling.

maysics includes six modules:

1. "algorithm" stores several simulation methods for simple simulation;
2. "constant" contents some usual constants;
3. "models" stores several commonly used laws, equations and models of mathematical physics for fast modeling;
4. "model_selection" used for estimating and selecting model;
5. "calculate" stores some common operators to assist in mathematical operations;
6. "transformation" stores common coordinate transformations and other mathematical transformations.

maysics-|- __init__
        |- algorithm -------|- GA
        |                   |- MC
        |                   |- SA
        |
        |- constant --------|- LP
        |
        |- model_selection -|- Error
        |                   |- Estimate
        |                   |- Search
        |                   |- Sense
        |
        |- models ----------|- ED
        |                   |- Fouriers_law
        |                   |- Leslie
        |                   |- Logistic
        |                   |- MVD_law
        |                   |- Plancks_law
        |
        |- operator --------|- Del
        |                   |- Dif
        |                   |- H
        |                   |- Laplace
        |
        |- transformation --|- Cylinder
        |                   |- Lorentz
        |                   |- Polar
        |                   |- Sphere
'''

import numpy as np


def arr(f):
    '''
    将矢量函数的输出形式统一为ndarray
    
    返回值：更改输出格式后的函数
    
    
    transform the output of vector function as ndarray
    
    return: function after changing the output format
    '''
    def obj(x):
        func = f(x)
        try:
            return np.array(func)
        except:
            return func
    return obj


def add(*arg):
    '''
    实现函数与同型函数、函数与数之间的加法
    要求作用函数若输出列表，必须是ndarray格式
    
    返回值：相加后的新函数
    
    
    addition between function and function or function and number
    if output of the function is list, it requires ndarray
    
    return: new function after addition
    '''
    def obj(x):
        list = []
        for i in range(len(arg)):
            if type(arg[i]).__name__ == 'function':
                list.append(arg[i](x))
            else:
                list.append(arg[i])
        return sum(list)
    return obj


def mul(*arg):
    '''
    实现函数与同型函数、函数与数之间的乘法
    要求作用函数若输出列表，必须是ndarray格式
    
    返回值：相乘后的新函数
    
    
    multiplication between function and function or function and number
    if output of the function is list, it requires ndarray
    
    return: new function after multiplication
    '''
    def obj(x):
        result = 1
        for i in range(len(arg)):
            if type(arg[i]).__name__ == 'function':
                result *= arg[i](x)
            else:
                result *= arg[i]
        return result
    return obj


def sub(minuend, subtrahend):
    '''
    实现函数与同型函数、函数与数之间的减法
    要求作用函数若输出列表，必须是ndarray格式
    minuend：被减数
    subtrahend：减数
    
    返回值：相乘后的新函数
    
    
    subtraction between function and function or function and number
    if output of the function is list, it requires ndarray
    minuend: minuend
    subtrahend: subtrahend
    
    return: new function after subtraction
    '''
    def obj(x):
        if type(minuend).__name__ == 'function':
            result_of_minuend = minuend(x)
        else:
            result_of_minuend = minuend
        if type(subtrahend).__name__ == 'function':
            result_of_subtrahend = subtrahend(x)
        else:
            result_of_subtrahend = subtrahend
        
        result = result_of_minuend - result_of_subtrahend
        return result
    return obj


def divi(dividend, divisor):
    '''
    实现函数与同型函数、函数与数之间的减法
    要求作用函数若输出列表，必须是ndarray格式
    
    参数
    ----
    dividend：被除数
    divisor：除数
    
    返回值：相乘后的新函数
    
    
    Parameters
    ----------
    division between function and function or function and number
    if output of the function is list, it requires ndarray
    dividend: dividend
    divisor: divisor
    
    return: new function after division
    '''
    def obj(x):
        if type(dividend).__name__ == 'function':
            result_of_dividend = dividend(x)
        else:
            result_of_dividend = dividend
        if type(divisor).__name__ == 'function':
            result_of_divisor = divisor(x)
        else:
            result_of_divisor = divisor
        result = result_of_dividend - result_of_divisor
        return result
    return obj


def shuffle(*arg):
    '''
    以相同方法打乱多个序列或打乱一个序列
    
    返回值：一个ndarray
    
    
    shuffle multiple sequences in the same way or shuffle a sequences
    
    return: a ndarray
    '''
    state = np.random.get_state()
    a_new_list = []
    for li in arg:
        np.random.set_state(state)
        np.random.shuffle(li)
        a_new_list.append(li)
    return np.array(a_new_list)


def r(*arg):
    '''
    相关系数
    
    返回值：各数组之间的相关系数矩阵
    
    
    correlation coefficient
    
    return: matrix of correlation coefficient
    '''
    arg = np.array(arg, dtype=float)
    if len(arg.shape) != 2:
        raise Exception("Input list should be 1 dimension.")
    
    cov_mat = np.cov(arg)
    var_mat = np.diagonal(cov_mat)**0.5
    
    for i in range(cov_mat.shape[0]):
        cov_mat[i] /= var_mat[i]
        cov_mat[:, i] /= var_mat[i]
    
    return cov_mat


def data_split(data, targets, train_size=None, test_size=None, shuffle=True, random_state=None):
    '''
    分离数据
    
    参数
    ----
    data：数据
    targets：指标
    train_size：浮点数类型，可选，训练集占总数据量的比，取值范围为(0, 1]，默认为0.75
    test_size：浮点数类型，可选，测试集占总数据量的比，取值范围为[0, 1)，当train_size被定义时，该参数无效
    shuffle：布尔类型，可选，True表示打乱数据，False表示不打乱数据，默认为True
    random_state：整型，可选，随机种子
    
    
    split the data
    
    Parameters
    ----------
    data: data
    targets: targets
    train_size: float, callable, ratio of training set to total data, value range is (0, 1], default=0.75
    test_size: float, callable, ratio of test set to total data, value range is [0, 1)
    shuffle: bool, callable, 'True' will shuffle the data, 'False' will not, default = True
    random_state: int, callable, random seed
    '''
    if not (train_size or test_size):
        train_size = 0.75
    elif test_size:
        train_size = 1 - test_size
    
    if train_size <= 0 or train_size > 1:
        raise Exception("'train_size' should be in (0, 1], 'test_size' should be in [0, 1)")
    
    if shuffle:
        np.random.seed(random_state)
        
        state = np.random.get_state()
        np.random.shuffle(data)
        np.random.set_state(state)
        np.random.shuffle(targets)
        
    num_of_data = len(data)
    train_data = data[:int(num_of_data * train_size)]
    train_target = targets[:int(num_of_data * train_size)]
    validation_data = data[int(num_of_data * train_size):]
    validation_target = targets[int(num_of_data * train_size):]
    
    return train_data, train_target, validation_data, validation_target


def kfold(data, targets, n, k=5):
    '''
    参数
    ----
    data：数据
    targets：指标
    n：整型，表示将第n折作为验证集，从0开始
    k：整型，可选，k折验证的折叠数，默认k=5
    
    返回值：训练集和验证集的元组
    
    
    Parameters
    ----------
    data: data
    targets: targets
    n: int, take the nth part as validation set, starting from 0
    k: int, callable, the number of k-fold, default = 5
    
    return: the tuple of training set and validation set
    '''
    num_validation_samples = len(data) // k
    
    validation_data = data[num_validation_samples * n:
                           num_validation_samples * (n + 1)]
    validation_targets = targets[num_validation_samples * n:
                                 num_validation_samples * (n + 1)]
    
    train_data = np.concatenate([data[: num_validation_samples * n],
                                 data[num_validation_samples * (n + 1):]])
    train_targets = np.concatenate([targets[: num_validation_samples * n],
                                    targets[num_validation_samples * (n + 1):]])
    
    return train_data, train_targets, validation_data, validation_targets