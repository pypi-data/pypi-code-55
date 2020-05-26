from .general import *

def linear_regression(X, Y): 
    x_prime = []
    y_prime = []
    
    for i in range(len(Y)):
        if (str(type(Y[i])) in num_types) and not math.isnan(Y[i]):
            x_prime.append(X[i])
            y_prime.append(Y[i])
            
    mean_x = mean(x_prime)
    mean_y = mean(y_prime)
    n = len(x_prime)
    numer = 0
    denom = 0
    for i in range(n):
        numer += (x_prime[i] - mean_x) * (y_prime[i] - mean_y)
        denom += (x_prime[i] - mean_x) ** 2.0
    m = numer / denom
    b = mean_y - (m * mean_x)

    return m, b

def mean_squares_error(x, y, m, b):
    elements = []

    for i in range(len(x)):
        if (str(type(x[i])) in num_types) and not math.isnan(x[i]) and (str(type(y[i])) in num_types) and not math.isnan(y[i]):
            lr_val = m * x[i] + b
            diff = y[i] - lr_val
            elements.append(diff * diff)
        
    return mean(elements)