from .general import *

def linear_regression(X, Y): 
    x_prime = []
    y_prime = []
    
    for i in range(len(Y)):
        if (Y[i] / 1) == (Y[i]):
            x_prime.append(X[i])
            y_prime.append(Y[i])
            
    mean_x = mean(x_prime)
    mean_y = mean(x_prime)
    n = len(x_prime)
    numer = 0
    denom = 0
    for i in range(n):
        numer += (x_prime[i] - mean_x) * (y_prime[i] - mean_y)
        denom += (x_prime[i] - mean_x) ** 2.0
    m = numer / denom
    c = mean_y - (m * mean_x)
    return m, c
