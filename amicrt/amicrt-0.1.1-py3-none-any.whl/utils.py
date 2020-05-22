import numpy as np

def monteCarloEntropy(model, x, y):
    out = 0
    yHatProbs = model.predict_proba(x)

    numToRemove = 0
    for i in range(len(y)):
        p_y_x = yHatProbs[i, y[i]]
        if p_y_x == 0:
            numToRemove += 1
        else:
            out -= np.log(p_y_x)

    # warning: this can result in error if numToRemove = len(y)
    return out / (len(y) - numToRemove)


def binaryLoss(model, x, y):
    """
    assumes model has a .predict() method
    """
    return (model.predict(x) == y).mean()


def ltgteq(a, b, operation):
    if operation == '>':
        return a > b
    if operation == '<':
        return a < b
    if operation == '==':
        return a == b
    if operation == '>=':
        return a >= b
    if operation == '<=':
        return a <= b
