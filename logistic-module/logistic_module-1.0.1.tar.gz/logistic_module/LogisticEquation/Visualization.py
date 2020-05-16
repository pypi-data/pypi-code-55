import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from .Logistic_and_vectorization import Logistic_equation

class Visualization:
    """
    This class allows to visualize two things : 

    - An animation representing some iterations of logistic map

    - The bifurcation diagram

    Besides, in this class we defined the global parameters :

    :param r0: Value of growth ratio of logistic map useful in animation
    :type r0: float

    :param n: Number of iterations to animate logistic map
    :type n: int

    :param p: Number of iterations to plot bifurcation diagram
    :type p: int

    :param ci: Initial point to calcul iteration of logistic map
    :type ci: float

    :param frames: Number of frames useful to animate the logistic map
    :type frames: int

    :param threshold: Thresold from which the diagram is drawn
    :type threshold: int
    """

    def __init__(self, r0=0.05, n=40, p=10000, ci=0.05, frames=82, threshold = 100):
        """Initialisation of class elements and plotting the x=y curve
        
        :param r: Subdivision of interval [2.5, 4] by 10 000 values
        :type r: numpy array

        :param x: Subdivision of interval [0, 1]
        :type x: numpy array

        :param y: Vector of antecedents of logistic map
        :type y: numpy array
        """
        self.frames = frames
        self.r0 = r0
        self.ci = ci
        self.p = p
        self.equation = Logistic_equation(n) 
        self.threshold = threshold
        self.fig, ax = plt.subplots()
        self.line, = ax.plot([], [],color='r')
        self.courbe, = ax.plot([], [], color='b')
        self.r = np.linspace(2.5, 4.0, p)
        self.x = np.linspace(0,1)
        self.y = 1e-5*np.ones(self.p)

        ax.plot([0, 1], [0, 1], 'black', lw=2)

    def __init(self):
        """Initialisation of curve and line for animation"""
        self.line.set_data([], [])
        self.courbe.set_data([],[])
        return self.line

    def __animate(self, i):
        """Main of animation : 

            - Recuperation of data in function vectorization and plot this couples of (x, f(x)) with ci on initial condition and a r0 who evolve

            - Plot the curve defined by logistic map on the same frame
        """
        self.line.set_data(zip(*self.equation.vectorization(self.ci, self.r0+i*self.r0)))
        self.courbe.set_data(self.x, self.equation.logistic(self.r0+i*self.r0, self.x))
        return self.line

    def start_animation(self):
        """Visualization of animation

        :return: Animation with matplotlib showing evolution of logistic map
        :rtype: animation with matplotlib
        """
        plt.title("Animation of logistic map evolution")
        plt.legend(["y = x", "liaison between x=y and x=f(y)", "y = rx(1-x)"])
        animation.FuncAnimation(self.fig, self.__animate, init_func=self.__init,frames=self.frames, interval=self.equation.n)
        plt.show()
