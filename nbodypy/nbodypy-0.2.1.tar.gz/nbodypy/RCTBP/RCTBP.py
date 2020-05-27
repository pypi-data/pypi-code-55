#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
The Restricted circular three body problem class
================

:Example:

>>> import nbodypy.RCTBP

This is a subtitle
-------------------

"""

import nbodypy
import numpy
import matplotlib
from scipy.integrate import ode,odeint,solve_ivp
from scipy.optimize import fsolve,root
import json


class RCTBP(object):
    tol = 1e-10
    def __init__(self,M1=1.989e6,M2=5.972,Distance=149597870e3,init=None,dim=6,coord = "Cross"):
        """
        Constructor

        :param mu: (float) parameter of the Three Body problem we consider. Default value 1.215e-02 for Earth-Moon system
        """
        self.M1 = M1
        self.M2 = M2
        self.Distance = Distance
        # mu initialization
        self._mu = M2/(M1+M2)
        # dimension initialization
        self._dim = dim
        self._N = 1
        # the position velocity initialization
        if(not isinstance(init, numpy.ndarray)): # initialization for N-gon
            self.z = numpy.ones(self._dim)
        else:
            self.z = init.copy()

        # some points
        self.P1 = numpy.array([-self._mu,0.0,0.0,0.0,0.0,0.0]) # in P1 coordinates
        self.P2 = numpy.array([1-self._mu,0.0,0.0,0.0,0.0,0.0]) # in P2 coordinates

        # Szebehely values
        self._rh = numpy.power(self._mu/3.0,1.0/3.0)
        self._gamma1 = self._rh*(1.0-1.0/3.0*self._rh-1.0/9.0*numpy.power(self._rh,2.0)-23.0/81.0*numpy.power(self._rh,3.0)+151.0/243.0*numpy.power(self._rh,4.0)-1.0/9.0*numpy.power(self._rh,5.0))
        self._gamma2 = self._rh*(1.0+1.0/3.0*self._rh-1.0/9.0*numpy.power(self._rh,2.0)-31.0/81.0*numpy.power(self._rh,3.0)-119.0/243.0*numpy.power(self._rh,4.0)-1.0/9.0*numpy.power(self._rh,5.0))
        self._v = numpy.power(self._mu/(3.0*(1.0-self._mu)),1.0/3.0)
        self.DL1 = self._v*(1.0-1.0/3.0*self._v-1.0/9.0*numpy.power(self._v,2.0)-23.0/81.0*numpy.power(self._v,3.0)+151.0/243.0*numpy.power(self._v,4.0)-1.0/9.0*numpy.power(self._v,5.0))
        self.DL2 = self._v*(1.0+1.0/3.0*self._v-1.0/9.0*numpy.power(self._v,2.0)-31.0/81.0*numpy.power(self._v,3.0)-119.0/243.0*numpy.power(self._v,4.0)-1.0/9.0*numpy.power(self._v,5.0))

        self.L1 = numpy.array([1-self._mu-self._gamma1,0.0,0.0,0.0,0.0,0.0]) # in P1 coordinates
        self.L2 = numpy.array([1-self._mu+self._gamma2,0.0,0.0,0.0,0.0,0.0]) # in P1 coordinates
        # coordinate system
        self._D1 = numpy.linalg.norm(self.P2-self.L1) # in P1 coordinates
        self._D2 = numpy.linalg.norm(self.P2-self.L2) # in P1 coordinates

        self._coordinates = "Cross"
        if(coord=="RichardsonL1"):
            self.CrossToRichardsonL1()
        if(coord=="RichardsonL2"):
            self.CrossToRichardsonL2()
        self._coordinates = coord



    def _CrossToRichardsonL1(self,x):

        xout = numpy.zeros(self._dim)
        xout[0] = (x[0]+self.DL1-(1.0-self._mu))/self.DL1
        xout[1] = x[1]/self.DL1
        xout[2] = x[2]/self.DL1
        xout[3] = x[3]/self.DL1
        xout[4] = x[4]/self.DL1
        xout[5] = x[5]/self.DL1
        return xout

    def CrossToRichardsonL1(self):
        """
        Change every intern points from Cross P1 centered coordinates to Richardson L1 centered coordinates
        """
        if(self._coordinates == "Cross"):
            self.P1 = self._CrossToRichardsonL1(self.P1)
            self.P2 = self._CrossToRichardsonL1(self.P2)
            self.L1 = self._CrossToRichardsonL1(self.L1)
            self.L2 = self._CrossToRichardsonL1(self.L2)
            self.z = self._CrossToRichardsonL1(self.z)
            if( hasattr(self, 'periodicOrbit')):
                self.periodicOrbit = self._CrossToRichardsonL1(self.periodicOrbit)

            self._coordinates = "RichardsonL1"

    def _CrossToRichardsonL2(self,x):

        xout = numpy.zeros(self._dim)
        xout[0] = (x[0]-self.DL2-(1.0-self._mu))/self.DL2
        xout[1] = x[1]/self.DL2
        xout[2] = x[2]/self.DL2
        xout[3] = x[3]/self.DL2
        xout[4] = x[4]/self.DL2
        xout[5] = x[5]/self.DL2
        return xout

    def CrossToRichardsonL2(self):
        """
        Change every intern points from Cross P1 centered coordinates to Richardson L2 centered coordinates
        """
        if(self._coordinates == "Cross"):
            self.P1 = self._CrossToRichardsonL2(self.P1)
            self.P2 = self._CrossToRichardsonL2(self.P2)
            self.L1 = self._CrossToRichardsonL2(self.L1)
            self.L2 = self._CrossToRichardsonL2(self.L2)
            self.z = self._CrossToRichardsonL2(self.z)
            if( hasattr(self, 'periodicOrbit')):
                self.periodicOrbit = self._CrossToRichardsonL2(self.periodicOrbit)
            self._coordinates = "RichardsonL2"

    def _RichardsonToCross(self,x):
        if(self._coordinates == "RichardsonL1"):
            #print("L1")
            di = self.DL1
            pm = -1.0
        elif(self._coordinates == "RichardsonL2"):
            #print("L2")
            di = self.DL2
            pm = 1.0
        else:
            print("Error Richardson to Cross")

        xout = numpy.zeros(self._dim)
        xout[0] = di*x[0]+pm*di+(1.0-self._mu)
        xout[1] = x[1]*di
        xout[2] = x[2]*di
        xout[3] = x[3]*di
        xout[4] = x[4]*di
        xout[5] = x[5]*di
        return xout

    def RichardsonToCross(self):
        """
        Change every intern points from Richardson (L1 or L2) coordinates to Cross P1 centered coordinates
        """
        self.P1 = self._RichardsonToCross(self.P1)
        self.P2 = self._RichardsonToCross(self.P2)
        self.L1 = self._RichardsonToCross(self.L1)
        self.L2 = self._RichardsonToCross(self.L2)
        self.z = self._RichardsonToCross(self.z)
        if(hasattr(self, 'periodicOrbit')):
            self.periodicOrbit = self._RichardsonToCross(self.periodicOrbit)

        self._coordinates = "Cross"

    def RichardsonL1toL2(self):
        """
        Change every intern points from Richardson L1 to Richardson L2 centered coordinates
        """
        if(self._coordinates == "RichardsonL1"):
            self.RichardsonToCross()
            self.CrossToRichardsonL2()
            self._coordinates = "RichardsonL2"
    def RichardsonL2toL1(self):
        """
        Change every intern points from Richardson L1 to Richardson L2 centered coordinates
        """
        if(self._coordinates == "RichardsonL2"):
            self.RichardsonToCross()
            self.CrossToRichardsonL1()
            self._coordinates = "RichardsonL1"


    def computeEnergy(self,z=None):
        """
        Compute the energy of a point given in Richardson coordinates.
        But the energy is compute in Cross Coordinates (call of _RichardsonToCross)
        """
        if(isinstance(z,numpy.ndarray)):
            state = z.copy()
        else:
            state = self.z.copy()

        if(self._coordinates == "RichardsonL1" or self._coordinates == "RichardsonL2"):
            xCross = self._RichardsonToCross(state)
        else:
            xCross = state

        x1 = -self._mu
        x2 = 1.0 -self._mu

        r1 = numpy.sqrt((xCross[0]-x1)**2+xCross[1]**2+xCross[2]**2)
        r2 = numpy.sqrt((xCross[0]-x2)**2+xCross[1]**2+xCross[2]**2)

        U = -1.0/2.0*(xCross[0]**2+xCross[1]**2)-(1.0-self._mu)/r1-0.5*self._mu*(1.0-self._mu)
        energyOut = 0.5*(xCross[3]**2+xCross[4]**2+xCross[5]**2)+U
        return energyOut

    def get_coordsys(self):
        """
        Get the name of the coordinate system
        :return: (string) Return the name of the coordinate system ("Cross","RichardsonL1" or "RichardsonL2")
        """
        return self._coordinates

    def get_dim(self):
        """
        Get the dimensions (position+velocity of the body)
        :return: (int) Return the size of the system dynamics
        """
        return self._dim

    def get_z(self):
        """
        Get the position of the body

        :return: Return the current state (numpy.array of dimension dim)
        """
        return self.z


    def get_r(self):
        """
        Get the position of the body

        :return: Return the position of the Body
        """
        return self.z[0:(self._dim/2)]
    def get_mu(self):
        """
        Get the mu parameter

        :return: Return the mu parameter
        """
        return self._mu


    def get_v(self):
        """
        Get the velocity of the body

        :return: Return the velocity of the Body
        """
        return self.z[self._dim/2:]


    def integrate(self,t,zinit=None,fileName=None):
        """
        Method to integrate a solution for the RCTBP problem

        :param t: (numpy array) t of all the times for which we want to get a point
        :param fileName: (string) optional parameter to save the solution in a external file.
                        The first column of the file contains the time steps. The others contain
                        the value of the phase state of each body.
        :return: the integrate solution at each times in a numpy array of size of t
        """
        if(isinstance(zinit,numpy.ndarray)):
            z0 = zinit
        else:
            z0 = self.z.copy()
        if(self.get_coordsys()=="Cross"):
            fun=lambda tp, z: nbodypy.dynamics.systemRCTBPCross(z,tp,self._mu,self.P1,self.P2)
            print("time :", t)
            sol = solve_ivp(fun,[t[0],t[-1]],z0,method="Radau",t_eval=t)#, rtol = self.tol, atol = self.tol)
        if(self.get_coordsys()=="RichardsonL1"):
            fun=lambda tp, z: nbodypy.dynamics.systemRCTBPRichardsonL1(z,tp,self._mu,self.P1,self.P2,self.DL1)
            #print("time :", t)
            sol = solve_ivp(fun,[t[0],t[-1]],z0,method="Radau",t_eval=t)#, rtol = self.tol, atol = self.tol)

        if(self.get_coordsys()=="RichardsonL2"):
            fun=lambda tp, z: nbodypy.dynamics.systemRCTBPRichardsonL2(z,tp,self._mu,self.P1,self.P2,self.DL2)
            #print("time :", t)
            sol = solve_ivp(fun,[t[0],t[-1]],z0,method="Radau",t_eval=t)#, rtol = self.tol, atol = self.tol)
        if(isinstance(fileName, str)): # if a name of file is given, save the sol into the file
            print(numpy.array([t]).shape, sol.shape)
            dat = numpy.hstack((numpy.array([t]).T,sol))
            print(dat.shape)
            numpy.savetxt(fileName, dat)
        return sol

    def _computeCn(self,k):

        #  the integer k of c_k

        if(self.Li==2):
            c = 1.0/(numpy.power(self._gammaL,3.0))*((numpy.power(-1.0,k))*self._mu+(numpy.power(-1.0,k))*(1.0-self._mu)*(numpy.power(self._gammaL,(k+1)))/(numpy.power(1.0+self._gammaL,(k+1))))
        else:
            c = 1.0/(numpy.power(self._gammaL,3.0))*((numpy.power(1.0,k))*self._mu+(numpy.power(-1.0,k))*(1.0-self._mu)*(numpy.power(self._gammaL,(k+1)))/(numpy.power(1.0-self._gammaL,(k+1))));
        return c

    def _computeRichardConst(self):
        """
        Compute the constants introduced by Richardson
        """

        if(self.Li==1):
            self._gammaL = self.DL1
        else:
            self._gammaL = self.DL2
        self._c2 = self._computeCn(2)
        self._c3 = self._computeCn(3)
        self._c4 = self._computeCn(4)

        if(self._c2>1):
            self._lambda=numpy.sqrt(2.0-self._c2+numpy.sqrt(self._c2)*numpy.sqrt(9.0*self._c2-8.0))/numpy.sqrt(2.0);
            self._omegap=numpy.sqrt(-(self._c2-2.0-numpy.sqrt(self._c2)*numpy.sqrt(9.0*self._c2-8.0)))/numpy.sqrt(2.0);
        else:
            print("self._lambda definition problem: self._c2<1 : ")

        self._k = 2.0*self._lambda/((self._lambda**2)+1.0-self._c2)

        self._d1 = 3.0*(self._lambda**2)/self._k*(self._k*(6*(self._lambda**2)-1.0)-2.0*self._lambda)
        self._d2 = 8.0*(self._lambda**2)/self._k*(self._k*(11*(self._lambda**2)-1.0)-2.0*self._lambda)

        self._a21 = 3.0*self._c3*((self._k**2)-2.0)/(4.0*(1.0+2.0*self._c2));
        self._a22 = 3.0*self._c3/(4.0*(1.0+2.0*self._c2));
        self._a23 = -3.0*self._c3*self._lambda/(4.0*self._k*self._d1)*(3.0*(self._k**3)*self._lambda-6.0*self._k*(self._k-self._lambda)+4.0);
        self._a24 = -3.0*self._c3*self._lambda/(4.0*self._k*self._d1)*(2.0+3.0*self._k*self._lambda);

        self._b21 = -3.0*self._c3*self._lambda/(2.0*self._d1)*(3.0*self._k*self._lambda-4.0);
        self._b22 = 3.0*self._c3*self._lambda/self._d1;

        self._d21 = -self._c3/(2.0*(self._lambda**2));

        self._a31 = -9.0*self._lambda/(4.0*self._d2)*(4.0*self._c3*(self._k*self._a23-self._b21)+self._k*self._c4*(4.0+(self._k**2)))+ \
                    (9.0*(self._lambda**2)+1.0-self._c2)/(2.0*self._d2)*(3.0*self._c3*(2.0*self._a23-self._k*self._b21)+self._c4*(2.0+3.0*(self._k**2)));
        self._a32 = -1.0/self._d2*(9.0*self._lambda/4.0*(4.0*self._c3*(self._k*self._a24-self._b22)+self._k*self._c4)+3.0/2.0*(9.0*(self._lambda**2)+\
                    1.0-self._c2)*(self._c3*(self._k*self._b22+self._d21-2.0*self._a24)-self._c4));

        self._b31 = 3.0/(8.0*self._d2)*(8.0*self._lambda*(3.0*self._c3*(self._k*self._b21-2.0*self._a23)-self._c4*(2.0+3.0*(self._k**2)))+\
                    (9.0*(self._lambda**2)+1.0+2.0*self._c2)*(4.0*self._c3*(self._k*self._a23-self._b21)+self._k*self._c4*(4.0+(self._k**2))));
        self._b32 = (9.0*self._lambda*(self._c3*(self._k*self._b22+self._d21-2.0*self._a24)-self._c4)+3.0/8.0*(9.0*(self._lambda**2)+\
                    1.0+2.0*self._c2)*(4.0*self._c3*(self._k*self._a24-self._b22)+self._k*self._c4))/self._d2;

        self._d31 = 3.0/(64.0*(self._lambda**2))*(4.0*self._c3*self._a24+self._c4);
        self._d32 = 3.0/(64.0*(self._lambda**2))*(4.0*self._c3*(self._a23-self._d21)+self._c4*(4.0+(self._k**2)));

        self._a1 = -3.0/2.0*self._c3*(2.0*self._a21+self._a23+5*self._d21)-3.0/8.0*self._c4*(12.0-(self._k**2));
        self._a2 = 3.0/2.0*self._c3*(self._a24-2.0*self._a22)+9.0/8.0*self._c4;

        self._s1 = (3.0/2.0*self._c3*(2.0*self._a21*((self._k**2)-2.0)-self._a23*((self._k**2)+2.0)-2.0*self._k*self._b21)-\
                    3.0/8.0*self._c4*(3.0*(self._k**4)-8.0*(self._k**2)+8.0))/(2.0*self._lambda*(self._lambda*(1+(self._k**2))-2.0*self._k));
        self._s2 = (3.0/2.0*self._c3*(2.0*self._a22*((self._k**2)-2.0)-self._a24*((self._k**2)+2.0)-2.0*self._k*self._b22+5*self._d21)+\
                    3.0/8.0*self._c4*(12.0-(self._k**2)))/(2.0*self._lambda*(self._lambda*(1.0+(self._k**2))-2.0*self._k));

        self._l1 = self._a1+2.0*(self._lambda**2)*self._s1;
        self._l2 = self._a2+2.0*(self._lambda**2)*self._s2;



    def initRichardson(self,Li=1,Azkm=300e3):
        """
        Compute a point of an analytical approximation
        of a Halo orbit and its associated period

        :param Li: (int) 1 for L1, 2 for L2
        """

        if(self._coordinates == "Cross"):
            if(Li==1):
                self.CrossToRichardsonL1()
            elif(Li==2):
                self.CrossToRichardsonL2()

            print("Warning : coordinates system changed to Richardson corresponding to the Li point")


        self.Li = Li

        self._computeRichardConst()

        t=0.0
        _type=1

        if(Li==1):
            DLi = self._gamma1*self.Distance
        else:
            DLi = self._gamma2*self.Distance

        delta = (self._omegap**2)-self._c2;
        # in normalized system
        Az=Azkm/DLi;

        Ax=numpy.sqrt((-self._l2*Az*Az-delta)/self._l1);

        Ay=self._k*Ax;
        w = (1 + self._s1*Ax*Ax + self._s2*Az*Az );

        X = numpy.zeros(6)

        X[0]= self._a21*Ax*Ax + self._a22*Az*Az - Ax*numpy.cos(t) + (self._a23*Ax*Ax-self._a24*Az*Az)*numpy.cos(2*t) + (self._a31*Ax*Ax*Ax-self._a32*Ax*Az*Az)*numpy.cos(3*t)

        X[1]=self._k*Ax*numpy.sin(t)+(self._b21*Ax*Ax-self._b22*Az*Az)*numpy.sin(2*t)+(self._b31*Ax*Ax*Ax-self._b32*Ax*Az*Az)*numpy.sin(3*t);

        dn=2-_type;
        X[2]= dn*Az*numpy.cos(t) + dn*self._d21*Ax*Az*(numpy.cos(2*t)-3)+ dn*(self._d32*Az*Ax*Ax-self._d31*Az*Az*Az)*numpy.cos(3*t);

        coef = self._omegap*w;
        yy = self._k*Ax + 2.0*(self._b21*Ax*Ax-self._b22*Az*Az) + 3*(self._b31*Ax*Ax*Ax- self._b32*Ax*Az*Az);
        X[3] = 0;
        X[4] = coef*yy;
        X[5] = 0;
        periodeOrb = 2.0*numpy.pi/(self._omegap*w);
        return X, periodeOrb

    #def initArchambeau(self):

    def _shootFunctionEnergy(self,z,energy):
        """
        Shooting function to find a periodic orbit with a fixed energy
        Az. Starting with a  period t_x and a state \f$(x,0,z,0, \dot y, 0)\f$
        we want to reach a point of the form: \f$(x_1,0,z_1,0, \dot y_1, 0)\f$
        at time 0.5*period matching a fixed energy. Hence we right that
        as the shooting function  for the library HYBRD.

        In richardson coordinates

        :param z: ! Shooting unknown : (X,Z,\dot Y, 0.5*period)
        """

        #print("coucou2")
        if(self._coordinates == "Cross"):
            print("ERROR, shoot periodic orbit should be in Richardson coordinates")
            exit()

        t0 = 0.0
        tf = z[3]
        #print(tf)
        state = numpy.zeros(6)
        state[0] = z[0]
        state[2] = z[1]
        state[4] = z[2]
        sol = self.integrate([t0,tf],zinit=state)

        output = numpy.zeros(4)
        output[0] =  sol.y[:,1][1]
        output[1] =  sol.y[:,1][3]
        output[2] =  sol.y[:,1][5]
        Cenergy = self.computeEnergy(z=state)
        output[3] = Cenergy-energy
        return output

    def _shootPeriodicEnergy(self,zi,energy):
        """
        Solves (try) the single shooting using 'hybrd'
        and 'zi' as initial guess for the shooting unknowns

        :param zi:      Initial guess (x0, z0, \dot y0, t)

        Returns
        -------
        sol : OptimizeResult
        The solution represented as a ``OptimizeResult`` object.
        Important attributes are: ``x`` the solution array, ``success`` a
        Boolean flag indicating if the algorithm exited successfully and
        ``message`` which describes the cause of the termination. See
        `OptimizeResult` for a description of other attributes.
        """
        #print("coucou")
        sol = root(self._shootFunctionEnergy, zi, method='hybr',args=(energy))
        return sol

    def continuationPeriodicOrbit(self,init,period,energy,stepNbr=100,Li=1,family=False):
        """
        Define periodic orbit around the libration point from an initial point
        using continuation method on the energy parameter

        :param init: initial guess (x0, y0, z0, \dot x0,\dot y0,\dot z0 )
        :param period: initial guess for the period of the periodic orbit
        :param energy: ojbective energy for the output periodic orbit
        :param pointNbr: (default 100) nbr of point for the period orbit
        :param Li: point aroud which the periodic orbit is computed


        Returns
        -------
        self.periodicOrbit : initial condition of periodic orbits
        self.periodicTime : numpy.ndarray period of the obtain periodic orbit
        """
        eps = 1e-10
        energyInit = self.computeEnergy(z=init)
        delta = 1.0/stepNbr
        gap = energy-energyInit
        #
        maxEchec = 10
        # counter of steps
        it = 0
        # current energy
        Cenergy = energyInit+delta*gap

        if(self._coordinates == "Cross"):
            boolCross = True
            if(Li==1):
                self.CrossToRichardsonL1()
                Init = self._CrossToRichardsonL1(init)
            elif(Li==2):
                self.CrossToRichardsonL2()
                Init = self._CrossToRichardsonL2(init)
        else:
            boolCross = False
            Init = init.copy()
        # building of init vector
        Zinit = [Init[0], Init[2], Init[4], 0.5*period]

        if(family): #TODO
            self.periodicTime = []
            self.periodicOrbit = []
        while(abs(Cenergy-energy)>eps and it < 10*stepNbr ):
            print(it,delta,Cenergy)
            it+=1
            sol = self._shootPeriodicEnergy(Zinit,Cenergy)
            if(sol.success == True):
                print(sol.x)
                Zinit = sol.x.copy()
                Cenergy = Cenergy+numpy.sign(gap)*min(abs(delta*gap),abs(energy-Cenergy))
                delta=1.2*delta
                if(family): #TODO
                    first = numpy.array([Zinit[0],0.0,Zinit[1],0.0,Zinit[2],0.0])
                    time = 2.0*Zinit[3]
                    self.periodicTime.append(time.copy())
                    self.periodicOrbit.append(first.copy())

            else: # echec
                Cenergy = Cenergy - delta*gap
                delta = 0.5*delta
                Cenergy = Cenergy + delta*gap
        if(it == 10*stepNbr):
            print("fail")
        else:
            if(not family):
                first = numpy.array([Zinit[0],0.0,Zinit[1],0.0,Zinit[2],0.0])
                time = 2.0*Zinit[3]
                self.periodicTime = time
                if(boolCross):
                    self.periodicOrbit = self._RichardsonToCross(first.copy())
                else:
                    self.periodicOrbit = first.copy()
        if(boolCross):
            self.RichardsonToCross()

    def _unitVect(self, vect):
        """
        Normalize a vector
        """
        return vect/numpy.norm(vect)

    def monodromy(self, point, period,eps= 1e-10):
        """
        Compute the monodromy matrix associated to a point of a
        periodic orbit.

        :param point: point of a periodic orbit in R^6
        :type point: numpy.ndarray
        :param period: (real) period of the periodic orbit

        """

        # pertubed points
        Yp = numpy.zeros(self._dim)
        Ym = numpy.zeros(self._dim)
        Ypi = numpy.zeros(self._dim)
        Ymi = numpy.zeros(self._dim)
        matrix = numpy.zeros((self._dim,self._dim))
        for j in range(self._dim):
            for k in range(self._dim):
                if(j==k):
                    Yp[k] = point[k] + eps
                    Ym[k] = point[k] - eps
                else:
                    Yp[k] = point[k]
                    Ym[k] = point[k]
            solP = self.integrate([0.0, period],zinit = Yp)
            solM = self.integrate([0.0, period],zinit = Ym)
            for l in range(self._dim):
                matrix[j,l] = (solP.y[l,-1]-solM.y[l,-1])/(2.0*eps)
        return matrix

    def manifoldVect(self, point, period, eps=1e-10):
        """
        Compute the eigenvalues, and keep the eigenvectors
        corresponding to the one >>1 and the one <<1. This will give us
        a linear approximation of the stable and unstable manifolds.
        """

        M = self.monodromy(point,period, eps=eps)
        (w,v) = numpy.linalg.eig(M)
        # we test which value correspond to instable and instable eigen value
        for i in range(self._dim):
            if(numpy.real(w[i])<0.1):
                iI = i
            if(numpy.real(w[i])>2.0):
                iS = i

        #  getting the eigenvectors
        Vi = numpy.real(v[:,iI])/numpy.linalg.norm(v[:,iI])
        Vs = numpy.real(v[:,iS])/numpy.linalg.norm(v[:,iS])

        # we want vectors oriented to right x>0
        if (Vi[0]<0.0) :
            Vi = -Vi
        if (Vs[0]<0.0) :
            Vs = -Vs

        return Vi, Vs

    def manifoldPertubPoints(self, periodicOrbit=None,period=None,epsMani=1e-03,epsDiff=1e-10):
        """
        Compute a set of perturbed points from a the set of the points
        of the periodic orbit. For each, we perturbed along the stable and
        unstable eigenvectors of the monodromy matrix. We get four set of perturbed
        points, stable left and right, and unstable left and right.
        """

        if(isinstance(periodicOrbit,numpy.ndarray) and isinstance(period, float)):
            orbit = periodicOrbit
            time = period
        else:
            orbit = self.periodicOrbit
            time = self.periodicTime[-1]

        N = orbit.shape[0]
        self.stableLeftPoints = numpy.zeros((N,6))
        self.stableRightPoints = numpy.zeros((N,6))
        self.unstableLeftPoints = numpy.zeros((N,6))
        self.unstableRightPoints = numpy.zeros((N,6))
        for i in range(N):
            (Vi,Vs) = self.manifoldVect(orbit[i,:], time,eps=epsDiff)
            print("------------\n",Vi,Vs,"-----------\n")
            self.stableLeftPoints[i,:] = orbit[i,:] - epsMani*Vs
            self.stableRightPoints[i,:] = orbit[i,:] + epsMani*Vs
            self.unstableLeftPoints[i,:] = orbit[i,:] - epsMani*Vi
            self.unstableRightPoints[i,:] = orbit[i,:] + epsMani*Vi

    def buildManifolds(self,manifoldsTime,periodicOrbit=None,period=None,epsMani=1e-03,epsDiff=1e-10,pointNbr=100):
        """
        Propagate the four manifolds from the set of perturbed points
        during a given time. Each trajectory is discretized with a given
        number of points.
        """

        if(isinstance(periodicOrbit,numpy.ndarray) and isinstance(period, float)):
            orbit = periodicOrbit
            time = period
        else:
            orbit = self.periodicOrbit
            time = self.periodicTime[-1]


        self.manifoldPertubPoints(periodicOrbit=orbit,period=time,epsMani=epsMani,epsDiff=epsDiff)

        self.manifoldRightStable = []
        self.manifoldRightUnstable = []
        self.manifoldLeftStable = []
        self.manifoldLeftUnstable = []

        self.manifoldsTime = manifoldsTime
        N = orbit.shape[0]

        for i in range(N):
            timeArray = numpy.linspace(0.0,manifoldsTime,pointNbr)
            sol = self.integrate(-timeArray,zinit=self.stableRightPoints[i,:])
            self.manifoldRightStable.append(sol.y.T)
            sol = self.integrate(-timeArray,zinit=self.stableLeftPoints[i,:])
            self.manifoldLeftStable.append(sol.y.T)
            sol = self.integrate(timeArray,zinit=self.unstableRightPoints[i,:])
            self.manifoldRightUnstable.append(sol.y.T)
            sol = self.integrate(timeArray,zinit=self.unstableLeftPoints[i,:])
            self.manifoldLeftUnstable.append(sol.y.T)
