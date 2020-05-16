class Logistic_equation:
    """This class contains two functions : 

        - One to calculate an iteration of logistic map 

        - One to vectorize the result of n iterations of logistic map in couples of (x, f (x))
    """

    def __init__(self, n):
        """Initialisation of class

        :param n: Number of iterations 
        :type n: int"""
        self.n = n

    def logistic(self, r, x):
        """Calculates an iteration of logistic map

        :param r: Growth coefficient in logistic map
        :type r: float

        :param x: Value of research point
        :type x: float

        :return: Result of the calcul with r and x
        :rtype: float
        """
        return r * x * (1 - x)

    def vectorization(self, x0, r):
        """Returns a vector of size n, composed by couples of points. The couples of points maked by respectively 
        the valeur of x and the result of a logistic map iteration with this x.

        :param x0: Initial coordinate
        :type x0: float

        :param r: Growth coefficient in logistic map
        :type r: float

        :return: Vector of size n composed by the couples of points (x, f(x)) where f(x) is an iteration of logistic map.
        :rtype: list"""

        coord = [(x0,0)]
        i = 0
        while i < self.n:
            y0 = self.logistic(r, x0)
            coord.append((x0,y0))        
            coord.append((y0,y0))
            x0 = y0
            i += 1
        return coord
