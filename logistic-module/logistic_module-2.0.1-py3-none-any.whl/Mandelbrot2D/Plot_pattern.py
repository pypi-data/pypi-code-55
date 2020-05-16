import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from memory_profiler import profile

from logistic_module.Mandelbrot2D.Mandelbrot2D import Mandelbrot_2D

@profile
def plot_patterns(x):
    """Plot the pattern you have chosen from the list (this choice is made with x). Possible plots: Elephant valleys, Triple spiral valleys and mini-Mandelbrots. All of these plots are obtained thanks to several zooms on sparse matrix
    
    :param x: a character string from the list given
    :type x: string 

    :return: a plot of a boolean matrix
    :rtype: object
    """
    if x=="mini mandelbrot":
        Z_2=Mandelbrot_2D(500,500,600,-0.718,-0.714,0.213,0.217)
        fig = plt.figure()
        fig.suptitle("Minis mandelbrot set")
        im = plt.imshow(Z_2.Mandelbrotset, cmap='binary')
        plt.colorbar()
        plt.show()
        return im
    if x=="Elephant valley":
        Z_5=Mandelbrot_2D(500,500,600,0.26185,0.26196,0.002515,0.002573)
        fig = plt.figure()
        fig.suptitle("Elephant valleys")
        im = plt.imshow(Z_5.Mandelbrotset, cmap='binary')
        plt.colorbar()
        plt.show()
        return im
    if x=="Triple spiral valley":
        Z=Mandelbrot_2D(500,500,600,-0.069,-0.0669,0.6478,0.6490)
        fig = plt.figure()
        fig.suptitle("Triple spiral valley")
        im = plt.imshow(Z.Mandelbrotset, cmap='binary')
        plt.colorbar()
        plt.show()
        return im
    if x!="mini mandelbrot" and x!="Elephant valley" and x!="Triple spiral valley":
        return "It seems like you did not chose one of the patterns of the list...Restart the function if you want to plot a characteristic pattern"
   
