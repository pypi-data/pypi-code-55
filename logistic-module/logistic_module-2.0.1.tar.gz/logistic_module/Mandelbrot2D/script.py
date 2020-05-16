from logistic_module.Mandelbrot2D.Mandelbrot2D import Mandelbrot_2D
from logistic_module.Mandelbrot2D.Mandelbrot2DAnimation import animate
from logistic_module.Mandelbrot2D.Plot_pattern import plot_patterns
from logistic_module.Mandelbrot2D.Inside_Mandelbrotset import Inside_the_set

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import tracemalloc

from numba import int64
from numba import float64
from numba import jitclass
from numba import jit 
import time

start = time.time()
tracemalloc.start()
Z = Mandelbrot_2D(hauteur=500, largeur=500, max_iteration=100,
                  xmin=-2, xmax=0.5, ymin=-1.25, ymax=1.25)
fig = plt.figure()
fig.suptitle("Mandelbrot set")
im = plt.imshow(Z.Mandelbrotset, cmap='magma')
plt.colorbar()
plt.show()
current, peak= tracemalloc.get_traced_memory()
print( f"Current memory usage is : {current/10**6}MB")
tracemalloc.stop()
end=time.time()
print("Time spent to print the Mandelbrotset:  {0:.5f} s.".format(end - start))


start_1=time.time()
fig = plt.figure()
fig.suptitle("Mandelbrot fractal")
Z_1 = Mandelbrot_2D(500, 500, 50, -2, 0.5, -1.25, 1.25)
im = plt.imshow(Z_1.Mandelbrotset, cmap='binary')
anim = animation.FuncAnimation(fig, animate, frames=np.arange(15), interval=400, blit=False)
plt.show()
end_1=time.time()
print("Time spent to animate the zoom on the Mandelbrotset:  {0:.5f} s.".format(end_1 - start_1))

start_2=time.time()
x=input("Do you want to save each frame of the animation in a folder ? This will slow the animation. Answer 'yes' or 'no' without quotes :")
Inside_the_set(x)
end_2=time.time()
print("Time spent to animate the zoom inside the Mandelbrotset:  {0:.5f} s.".format(end_2 - start_2))

start_3=time.time()
x=input('Which one do you want to plot ("Elephant valley", "Triple spiral valley" or "mini mandelbrot". Write the answer without quotes)?')
plot_patterns(x)
end_3=time.time()
print("Time spent to plot a characteristic pattern:  {0:.5f} s.".format(end_3 - start_3))

