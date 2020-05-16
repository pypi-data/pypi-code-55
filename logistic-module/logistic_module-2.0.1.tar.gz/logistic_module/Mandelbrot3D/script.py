"""Modelize an interactive representation of the Mandelbrot set in 3D and compute the time spent to do it.  
   Animate the rotation of the later representation to show the linf between the Mandelbrot set and the bifurcation diagram.  
   Please enter integers values for n and M.   
   Use the Mand_3D class from Mandelbrot3D and plotly.  
   
   ..seealso:: plotly.graph_projects for figure reference and Mand_3D documentation.  
   ..warning:: The modelization may take some time depending of each computer.  
   ..note:: The decrease of the n and/or M parameters can speed up the processus.  
   """

import warnings
import time
import plotly
from logistic_module.Mandelbrot3D.Mandelbrot3D import Mand_3D
from logistic_module.Mandelbrot3D.Mandelbrot3D_anim import animation

warnings.filterwarnings("ignore")

n,M = Mand_3D.init_param()
L = 1.4
dx = -0.6
dy = 0.0


start_total = time.time()
fig = Mand_3D(n,M,L,dx,dy)

start = time.time()
plotly.offline.plot(fig.interact(), filename='Mandelbrot3D_interactive.html')
end = time.time()
print("Time spent to modelize the Mandelbrot set in 3D:  {0:.5f} s.".format(end - start))



anim = animation(fig)

start2 = time.time()
plotly.offline.plot(anim, filename='Mandelbrot3D_animation.html')
end2 = time.time()
print("Time spent to animate the Mandelbrot set in 3D:  {0:.5f} s.".format(end2 - start2))

end_total = time.time()
print("Total time spent to modelize and animate the Mandelbrot set in 3D:  {0:.5f} s.".format(end_total - start_total))
