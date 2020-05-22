import numpy as np
import sympy as sym
sym.init_printing()

def matrix_multiplication(first_matrix, second_matrix):
    '''
    Returns the product of two matrices
    
    Parameters
    ----------
    first_matrix: 2D array
        A two dimensional array with elements of the second matrix
        
    second_matrix: 2D array
        A two dimensional array with elements of the first matrix
      
    Examples
    --------
    >> A = np.array([[5/2, 3, 5, 1], [-8, 7/6, 5, 6], [4/5, 2, -9, 5]])
    >> B = np.array([[8, 4, 7/3, -2], [5/8, -5, 3, 9], [1, 8, 2, 6/5]]).T
    >> matrix_operations(A, B)
    '''
    
    A = first_matrix
    
    B = second_matrix
    
    Results = np.dot(A,B)
        
    return sym.Matrix(Results)