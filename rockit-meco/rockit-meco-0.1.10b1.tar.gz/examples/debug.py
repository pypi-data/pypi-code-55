#
#     This file is part of Rockit.
#
#     Rockit -- Rapid Optimal Control Kit
#     Copyright (C) 2019 MECO, KU Leuven. All rights reserved.
#
#     Rockit is free software; you can redistribute it and/or
#     modify it under the terms of the GNU Lesser General Public
#     License as published by the Free Software Foundation; either
#     version 3 of the License, or (at your option) any later version.
#
#     Rockit is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#     Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public
#     License along with CasADi; if not, write to the Free Software
#     Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
#

"""
A Hello World Example
===================

Some basic example on solving an Optimal Control Problem with Rockit.
"""

# Import the project
from rockit import *
from numpy import sin

#%%
# Problem specification
# ---------------------

# Start an optimal control environment with a time horizon of 10 seconds
#  (free time problems can be configured with `FreeTime(initial_guess)`)
ocp = Ocp(T=10)

# Define two scalar states (vectors and matrices also supported)
x1 = ocp.state()
x2 = ocp.state()

# Define one piecewise constant control input
#  (use `order=1` for piecewise linear)
u = ocp.control()

# Specify differential equations for states
#  (time dependency supported with `ocp.t`,
#   DAEs also supported with `ocp.algebraic` and `add_alg`)
ocp.set_der(x1, (1 - x2**2) * x1 - x2 + u)
ocp.set_der(x2, x1)

# Lagrange objective term
ocp.add_objective(ocp.integral(x1**2 + x2**2 + u**2))
# Mayer objective term
ocp.add_objective(ocp.at_tf(x1**2))

# Path constraints
#  (must be valid on the whole time domain running from `t0` to `tf=t0+T`,
#   grid options available such as `grid='inf'`)
ocp.subject_to(x1 >= -0.25)
ocp.subject_to(-1 <= (u <= 1 ))

# Boundary constraints
ocp.subject_to(ocp.at_t0(x1) == 0)
ocp.subject_to(ocp.at_t0(x2) == 1)

ocp.subject_to(sin(x1)>=2)

#%%
# Solving the problem
# -------------------

# Pick an NLP solver backend
#  (CasADi `nlpsol` plugin):
ocp.solver('ipopt')

# Pick a solution method
#  N -- number of control intervals
#  M -- number of integration steps per control interval
method = MultipleShooting(N=10, M=2, intg='rk')
#method = DirectCollocation(N=10, M=2)
ocp.method(method)

# Solve
try:
    sol = ocp.solve()
except:
    pass

#ocp.show_infeasibilities(1e-4)
