import numpy as np
import matplotlib.pyplot as plt

from .Logistic_and_vectorization import Logistic_equation

class Visualization_bifurcation:
    """This class allows to visualize the bifurcation diagram, wuit the global parameters :

    :param p: Number of iterations to plot bifurcation diagram
    :type p: int

    :param n: Number of iterations to animate logistic map
    :type n: int

    :param threshold: Thresold from which the diagram is drawn
    :type threshold: int
    """

    def __init__(self, p=10000, n=40, threshold = 100):
        """Initialisation of class elements

        :param r: Subdivision of interval [2.5, 4] by p values
        :type r: numpy array
        
        :param y: Matrix p*p with 1e-5 values
        :type y: numpy array
        """
        self.p = p
        self.equation = Logistic_equation(n) 
        self.r = np.linspace(2.5, 4.0, self.p)
        self.threshold = threshold
        self.y = 1e-5*np.ones(self.p)


    def bifurcation_diagram(self):
        """Visualization of bifurcation diagram

        :return: Plot showing bifurcation diagram
        :rtype: plot with matplotlib
        """

        for i in range(self.p):
            self.y = self.equation.logistic(self.r, self.y)
            if i >= (self.p - self.threshold):
                plt.plot(self.r, self.y, alpha=.25)
        
        plt.xlim(2.5, 4)
        plt.title("Bifurcation diagram")

        plt.show()