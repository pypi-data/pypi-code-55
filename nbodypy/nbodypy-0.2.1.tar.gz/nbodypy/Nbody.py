#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import matplotlib
from scipy.integrate import odeint
from scipy.optimize import fsolve
import nbodypy.dynamics
import json

# function to convert string tab description json to numpy.ndarray
def json2arr(str):
    """
    Convert a string of json structure to a numpy.array
    Args:
         str: string
             describing a list (from a json file)
    :rtype: numpy.array
    :return: the numpy.array of the json structure

    :Example:

    >>> string = "[1,2,3]"
    >>> Array = json2arr(string)

    """
    return eval("numpy.array("+str+",dtype=float)")

class Nbody(object):
    tol = 1e-10
    def __init__(self, N=2, mass=None,init=None,dim=4,rotating=None,jsonFile=None,zdzInit=None):
        """
        Constructor

        :param N: int The number of bodies. default 2.
        :param mass: numpy.array of masses of the bodies.
                     default None that implies each body has a mass equal to one.
        :param init: numpy.array of initial conditions (ex: [x1, y1, dx1, dy1,x2,y2,dx2,dy2...] in dimension 4 (2D)).
                     default None, the bodies are on a circle.
        :param dim: number of dimension (space and velocity). default 4 (planar motion)
        :param rotating: rotation matrix (dim/2 times dim/2) for the frame. Default None (no rotation)
        :param jsonFile: name of the json file to construct the object. default none.
        """
        if(isinstance(jsonFile,str)):
            json_data = open(jsonFile).read()
            data = json.loads(json_data)
            # size of the system
            self._N = int(data["N"])
            # size of the system dynamics for each body
            self._dim = int(data["dim"])
            # the mass initialized to one
            if(not data.has_key("mass")):
                self.mass = numpy.ones(self._N)
            else:
                self.mass = json2arr(data["mass"])
            # the position velocity initialization
            if(not data.has_key("init")): # initialization for N-gon
                self.z = numpy.ones(self._N*self._dim)
                for i in range(self._N):
                    #print i*self._dim
                    deg = 2.0*numpy.pi/self._N
                    #print i*deg
                    self.z[(i*self._dim)+0] = numpy.cos(i*deg)
                    self.z[(i*self._dim)+1] = numpy.sin(i*deg)
                    self.z[(i*self._dim)+2] = -numpy.sin(i*deg)
                    self.z[(i*self._dim)+3] = numpy.cos(i*deg)
            else:
                self.z = json2arr(data["init"])
            # the state and the linearized state around the solution
            if(not data.has_key("zdzInit")): #
                self.zdz = numpy.ones(2*self._N*self._dim)
            else:
                self.zdz = json2arr(data["zdzInit"])
            # matrix of rotating coordinates
            if(not data.has_key("rotating")):
                self.rotating = None
            else:
                self.rotating = json2arr(data["rotating"])

        else: # we consider the other argumets

            # size of the system
            self._N = N
            # size of the system dynamics for each body
            self._dim = dim
            # the mass initialized to one
            if(not isinstance(mass,numpy.ndarray)):
                self.mass = numpy.ones(N)
            else:
                self.mass = mass.copy()
                # the position velocity initialization
            if(not isinstance(init, numpy.ndarray)): # initialization for N-gon
                self.z = numpy.ones(self._N*self._dim)
                for i in range(self._N):
                    #print i*self._dim
                    deg = 2.0*numpy.pi/self._N
                    #print i*deg
                    self.z[(i*self._dim)+0] = numpy.cos(i*deg)
                    self.z[(i*self._dim)+1] = numpy.sin(i*deg)
                    self.z[(i*self._dim)+2] = -numpy.sin(i*deg)
                    self.z[(i*self._dim)+3] = numpy.cos(i*deg)
            else:
                self.z = init.copy()
            # zdz initialization
            if(not isinstance(zdzInit, numpy.ndarray)):
                self.zdz = numpy.ones(2*self._N*self._dim)
            else:
                self.zdz = zdzInit.copy()
            # matrix of rotating coordinates
            if(not isinstance(rotating,numpy.ndarray)):
                self.rotating = None
            else:
                self.rotating = rotating.copy()

    def get_N(self):
        """
        Get the number of bodies
        :return: (int) Return the size of the system
        """
        return self._N

    def get_dim(self):
        """
        Get the dimensions (position+velocity of one body)
        :return: (int) Return the size of the system dynamics for each body
        """
        return self._dim

    def get_z(self):
        """
        Get the position of one body

        :return: Return the current state (numpy.array of dimension N*dim)
        """
        return self.z

    def get_r(self,I):
        """
        Get the position of one body

        :param I: the number of the considered body (starting at 0)
        :return: Return the position of the Ith Body
        """
        return self.z[I*self._dim:(I*self._dim+self._dim/2)]
    def get_v(self,I):
        """
        Get the velocity of one body

        :param I: the number of the considered body (starting at 0)
        :return: Return the velocity of the Ith Body
        """
        return self.z[(I*self._dim+self._dim/2):(I*self._dim+self._dim)]

    def integrate(self,t,fileName=None):
        """
        Method to integrate a solution for a given N-body problem

        :param t: (numpy array) t of all the times for which we want to get a point
        :param fileName: (string) optional parameter to save the solution in a external file.
                         The first column of the file contains the time steps. The others contain
                         the value of the phase state of each body.
        :return: the integrate solution at each times in a numpy array of size of t
        """
        z0 = self.z.copy()
        sol = odeint(nbodypy.dynamics.system, z0, t, rtol = self.tol, atol = self.tol, args=(self.mass, self._N,self._dim,self.rotating))
        if(isinstance(fileName, str)): # if a name of file is given, save the sol into the file
            print(numpy.array([t]).shape, sol.shape)
            dat = numpy.hstack((numpy.array([t]).T,sol))
            print(dat.shape)
            numpy.savetxt(fileName, dat)
        return sol

    def Dintegrate(self,t,fileName=None,opt=True):
        """
        Method to integrate a solution for a given N-body problem and the linearized system around the solution

        :param t: (numpy array) t of all the times for which we want to get a point
        :param fileName: (string) optional parameter to save the solution in a external file.
                         The first column of the file contains the time steps. The others contain
                         the value of the phase state of each body.
        :return: the integrate solution at each times in a numpy array of size of t
        """
        zdz0 = self.zdz.copy()
        if(not opt):
            sol = odeint(nbodypy.dynamics.Dsystem, zdz0, t, rtol = self.tol, atol = self.tol, args=(self.mass, self._N,self._dim,self.rotating))
        else:
            sol = odeint(nbodypy.dynamics.DsystemOpt, zdz0, t, rtol = self.tol, atol = self.tol, args=(self.mass, self._N,self._dim,self.rotating))

        if(isinstance(fileName, str)): # if a name of file is given, save the sol into the file
            print(numpy.array([t]).shape, sol.shape)
            dat = numpy.hstack((numpy.array([t]).T,sol))
            print(dat.shape)
            numpy.savetxt(fileName, dat)
        return sol

    def move(self,t):
        """
        Move the state integrating self.z during the time t
        :param t: time (float) for integration
        :return: move the self.z to the point after integration during t
        """
        sol = odeint(system, self.z, [0.0,t], rtol = self.tol, atol = self.tol, args=(self.mass, self._N,self._dim,self.rotating))
        self.z = sol[-1,:].copy()

    def monodromy(self,t):
        """
        Compute the monodromy matrix starting à self.z position pour a periodic solution of period t. The computation is done integrating the linearized equation around the periodic solution.

        :param t: (float) time for integration. The period of the periodic solution
        :return: (numpy.array) the monodromy matrix. Dim (N*dim, N*dim)
        """
        # initialization
        M = numpy.zeros((self._N*self._dim,self._N*self._dim))
        # save the zdz value
        zdzSave = self.zdz.copy()
        T=[0.0,t/2.0,t]
        for i in range(self._N*self._dim):
            ei = numpy.zeros(self._N*self._dim)
            ei[i] = 1.0
            Init = numpy.hstack((self.z,ei))

            self.zdz = Init.copy()
            sol = self.Dintegrate(T)

            M[i,:] = sol[-1,self._N*self._dim:].copy()
        # restore the zdz value
        self.zdz = zdzSave.copy()
        return M

    def monodromyDF(self,t,dx=1e-09):
        """
        Compute the monodromy matrix starting à self.z position pour a periodic solution of period t. The computation is done by finite differences.

        :param t: (float) time for integration. The period of the periodic solution
        :return: (numpy.array) the monodromy matrix. Dim (N*dim, N*dim)
        """
            # initialization
        M = numpy.zeros((self._N*self._dim,self._N*self._dim))
        # save the z value
        zSave = self.z.copy()
        T=[0.0,t/2.0,t]
        Tm=[0.0,-t/2,-t]
        for i in range(self._N*self._dim):
            ei = numpy.zeros(self._N*self._dim)
            ei[i] = dx
            self.z = self.z+ei
            sol = self.integrate(T)
            self.z = zSave.copy()
            self.z = self.z-ei
            sol2 = self.integrate(Tm)
            self.z = zSave.copy()
            M[i,:] = (sol[-1,:] - sol2[-1,:])/(2.0*dx)
            # restore the zdz value

        return M

    def shoot(self,t,z0):
        T = [0.0, t]
        sol = odeint(system, z0, T, rtol = 1e-10, atol = 1e-10,args=(self.mass, self._N,self._dim))
        return numpy.hstack(sol[1,:])

    def shootFChoregraphy(self,z0):
        T = 2.0*numpy.pi/self._N
        sol = self.shoot(T,z0)
        #print "init = ", self.z
        #print "sol = ", sol
        zeros = numpy.empty(self._N*self._dim)
        zeros[0:(self._N-1)*self._dim] = sol[0:(self._N-1)*self._dim]-z0[self._dim:(self._N)*self._dim]
        zeros[(self._N-1)*self._dim:(self._N)*self._dim] = sol[(self._N-1)*self._dim:(self._N)*self._dim]-z0[0:self._dim]
        return zeros
    def shootChoregraphy(self):
        return fsolve(self.shootFChoregraphy, self.z,xtol=1.0e-06,full_output=True)
    def massHomotopy(self, Mass,epsinit = 1e-03, epsmin = 1e-12, epsmax = 0.1, itmax=100):
        print("-------------- Mass Homotopy --------------")
        # save the initial mass
        massinit = self.mass.copy()
        # save the initial z
        zinit = self.z.copy()
        # homotopy parameter
        lbd = 0.0
        # number of iteration
        it = 0
        # step
        eps = epsinit
        zold = self.z.copy()
        while(lbd < 1.0 and it < itmax):
            lbdold = lbd
            lbd = min(lbd + eps,1.0)
            it = it +1
            self.z = self.z + lbd*(self.z-zold)
            self.mass = (1.0-lbd)*massinit+lbd*Mass
            (z, infodict, ier, mesg) = self.shootChoregraphy()
            if(ier==1): # if the newton did converge
                zold = self.z.copy()
                self.z = z.copy()
                eps = min(1.1*eps,epsmax)
                print("Success Iteration:",it," output:", ier, mesg)
                print("eps = ", eps, ", lambda = ", lbd)
            else:
                lbd = lbdold
                eps = max(eps*0.75,epsmin)
                print("Fail Iteration:",it," output:", ier,mesg)
                print("eps = ", eps, ", lambda = ", lbd)
            print("---------------------------------------")
        if(it==itmax):
            print("Maximal number of iteration")
            #self.z = zinit.copy()
            #self.mass = massinit.copy()
        else:
            print("Mass Homotopy success")
