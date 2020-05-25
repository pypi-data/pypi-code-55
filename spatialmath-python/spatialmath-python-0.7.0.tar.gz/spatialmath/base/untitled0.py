#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 20:14:35 2020

@author: corkep
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import spatialmath.base as tr
import numpy as np

fig = plt.figure()


ax = fig.add_subplot(111, projection='3d')

dims = [0, 3]
if len(dims) == 2:
    dims = dims * 3
ax.set_xlim(dims[0:2])
ax.set_ylim(dims[2:4])
ax.set_zlim(dims[4:6])


h = ax.text3D(0.5, 0.5, 0.5, "boo", color='black')
print(type(h))

x2, y2, _ = proj3d.proj_transform(0, 0, 0, ax.get_proj())

q = ax.quiver(0, 0, 0, 1, 1, 1)


# p = np.vstack( [q._segments3d.reshape(6,3).T, np.ones((1,6))])

# p = tr.transl(1, 1,0) @ p
# print(p)
# print(q._segments3d)
# print((p[0:3,:].T).reshape(3,2,3))
# p = (p[0:3,:].T).reshape(3,2,3)
# q.set_segments(p)


# h.set_position((x2, y2))

# plt.show()
