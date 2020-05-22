import numpy as np
import sympy as sym
sym.init_printing()

def matrix_operations(first_matrix, second_matrix, matrix_operation = 'Multiplication'):
    '''
    Performs a specified arithmetic operation on two given matrices
    
    Parameters
    ----------
    first_matrix: 2D array
        A two dimensional array with elements of the second matrix
        
    second_matrix: 2D array
        A two dimensional array with elements of the first matrix
        
    matrix_operation: string, optional
        Arithmetic operation to be applied
        Valid values include: Addition, Subtraction, Multiplication, Division
    
    Examples
    --------
    >> A = np.array([[5/2, 3, 5, 1], [-8, 7/6, 5, 6], [4/5, 2, -9, 5]])
    >> B = np.array([[8, 4, 7/3, -2], [5/8, -5, 3, 9], [1, 8, 2, 6/5]])
    >> matrix_operations(A, B, 'Multiplication')
    '''
    
    A = first_matrix
    
    B = second_matrix
    
    if matrix_operation not in ['Addition', 'Subtraction', 'Multiplication', 'Division']:
        raise ValueError(matrix_operation + " is an invalid value for the argument matrix operation. Valid values are: 'Addition', 'Subtraction', 'Multiplication', 'Division'")
    
    # -------------------------------------------------------------------------
    # addition
    # -------------------------------------------------------------------------
    
    if matrix_operation == 'Addition':
        
        Results = A + B
        
    # -------------------------------------------------------------------------
    # subtraction
    # -------------------------------------------------------------------------
    
    if matrix_operation == 'Subtraction':
        
        Results = A - B
        
    # -------------------------------------------------------------------------
    # multiplication
    # -------------------------------------------------------------------------
    
    if matrix_operation == 'Multiplication':
        
        Results = A * B
        
    # -------------------------------------------------------------------------
    # Division
    # -------------------------------------------------------------------------
    
    if matrix_operation == 'Division':
        
        Results = A / B
        
    return sym.Matrix(Results)