# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Mon May 18 15:18:03 2020

# @author: corkep
# """

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import matplotlib.colors as colors


# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('../../../MATLAB/robot/data/meshes/UNIMATE/puma560/link1.stl')
tri = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)
# tri.set_color(colors.rgb2hex([0.9,0.6,0.]))
# tri.set_edgecolor('k')
axes.add_collection3d(tri)

# Auto scale to the mesh size
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

ls = LightSource(azdeg=0, altdeg=65)

# Show the plot to the screen
pyplot.show()


# import numpy as np
# from mayavi import mlab
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.colors import LightSource

# ## Test data: Matlab `peaks()`
# x, y = np.mgrid[-3:3:150j,-3:3:150j]
# z =  3*(1 - x)**2 * np.exp(-x**2 - (y + 1)**2) \
#    - 10*(x/5 - x**3 - y**5)*np.exp(-x**2 - y**2) \
#    - 1./3*np.exp(-(x + 1)**2 - y**2) 

# ## Mayavi
# surf = mlab.surf(x, y, z, colormap='RdYlBu', warp_scale='auto')
# # Change the visualization parameters.
# surf.actor.property.interpolation = 'phong'
# surf.actor.property.specular = 0.1
# surf.actor.property.specular_power = 5



# ## Matplotlib
# fig = plt.figure()
# ax = fig.gca(projection='3d')

# # Create light source object.
# ls = LightSource(azdeg=0, altdeg=65)
# # Shade data, creating an rgb array.
# rgb = ls.shade(z, plt.cm.RdYlBu)
# surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, linewidth=0,
#                        antialiased=False, facecolors=rgb)
# plt.show()
# mlab.show()

