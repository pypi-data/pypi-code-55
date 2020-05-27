#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
The N-body class dynamical system
================

:Example:

>>> import nbodypy.dynamics

This is a subtitle
-------------------

"""

import nbodypy
import numpy



# the N-body system
def system(z,t,m,N,dim,rotating):
    """
    The vector field for the Nbody problem
    coordinates are organized as (r1,v1,r2,v2,..,rN,vN)
    where r is the position in R^n where n=dim/2
    and v the velocity in R^n

    :param N: (int) number of bodies
    :param dim: (int) dimension of the phase space for one body
    :param z: (numpy array) state at which we want to compute the vector field. Dimension : dim*N
    :param t: (float) time at which we want to compute the vector field. Here the vector field is time independant
    :param rotating: (numpy array) rotation matrix for the frame. dimension dim/2 times dim/2
    :return: (numpy array) dz/dt the value of the vector field at state z (dimension N*dim)
    """
    dzdt = numpy.zeros(N*dim)
    for i in range(N):
        #print "Point i", i, z[(i*dim+2):(i*dim+dim)]
        qi = z[(i*dim):(i*dim+int(dim/2))]
        vi = z[(i*dim+int(dim/2)):(i*dim+dim)]
        dzdt[i*dim:(i*dim+int(dim/2))] = vi # dr/dt=v
        for j in range(N):
            qj = z[(j*dim):(j*dim+int(dim/2))]
            vj = z[(j*dim+int(dim/2)):(j*dim+dim)]
            if(i!=j):
                rij = numpy.linalg.norm(qj-qi)
                dzdt[(i*dim+int(dim/2)):(i*dim+dim)] = dzdt[(i*dim+int(dim/2)):(i*dim+dim)]+ (m[j]*(qj-qi))/numpy.power(rij,3.0)
            # if rotating frame
        if(isinstance(rotating,numpy.ndarray)):
            dzdt[(i*dim+int(dim/2)):(i*dim+dim)] = dzdt[(i*dim+int(dim/2)):(i*dim+dim)]-2.0*numpy.dot(rotating,vi)-numpy.dot(rotating,numpy.dot(rotating,qi))
    return dzdt



# the N-body system resolvant equation
def Dsystem(zdz,t,m,N,dim,rotating):
    """
    The vector field for the Nbody problem
    coordinates are organized as (r1,v1,r2,v2,..,rN,vN) and (dr1,dv1,dr2,dv2,..,drN,dvN)
    where r is the position in R^n where n=dim/2
    v the velocity in R^n and dr and dv are the variation position and velocity

    :param N: (int) number of bodies
    :param dim: (int) dimension of the phase space for one body
    :param zdz: (numpy array) state at which we want to compute the vector field. Dimenstion 2*dim*N
    :param t: (float) time at which we want to compute the vector field. Here the vector field is time independant
    :param rotating: (numpy array) rotation matrix for the frame. dimension dim/2 times dim/2
    :return: (numpy array) dz/dt the value of the vector field at state z (dimension N*dim)
    """

    # compute the dynamics
    # position and velocity
    z = zdz[0:N*dim].copy()
    dzdt = system(z,t,m,N,dim,rotating)

    # some constant parts
    n = int(dim/2)
    nZero = numpy.zeros((n,n),dtype=float)
    nId = numpy.eye(n,dtype=float)

    zdzdt = numpy.zeros(2*N*dim)
    zdzdt[0:N*dim] = dzdt.copy()

    # the dynamical matrix
    A = numpy.zeros((dim*N, dim*N))

    for i in range(N):
        qi = z[(i*dim):(i*dim+int(dim/2))]
        vi = z[(i*dim+int(dim/2)):(i*dim+dim)]
        for j in range(N):
            qj = z[(j*dim):(j*dim+int(dim/2))]
            vj = z[(j*dim+int(dim/2)):(j*dim+dim)]
            elA = numpy.zeros((dim,dim))
            # dfi_1/dq_j = 0
            if(i==j):
                elA[0:n,n:2*n] = nId.copy() # dfi_1/dvi
                for k in range(N):
                    if(k!=i):
                        qk = z[(k*dim):(k*dim+int(dim/2))]
                        rik = numpy.linalg.norm(qk-qi)
                        # dfi_2/dqi
                        elA[n:2*n,0:n] = elA[n:2*n,0:n]-m[k]/numpy.power(rik,3.0)*nId+3.0*m[k]/numpy.power(rik,5.0)*(numpy.dot(numpy.array([qk-qi]).T,numpy.array([qk-qi])))
                if(isinstance(rotating,numpy.ndarray)):
                    elA[n:2*n,n:2*n] = -2*rotating # dfi_2/dvi
                    elA[n:2*n,0:n] = elA[n:2*n,0:n]-numpy.dot(rotating,rotating) #dfi_2/dqi

            else: #j!=i
                rij = numpy.linalg.norm(qj-qi)
                #dfi_2/dqj
                elA[n:2*n,0:n] = m[j]/numpy.power(rij,3.0)*nId-3.0*m[j]/numpy.power(rij,5.0)*(numpy.dot(numpy.array([qj-qi]).T,numpy.array([qj-qi])))
            A[i*dim:(i+1)*dim,j*dim:(j+1)*dim]=elA.copy()

    ## Validation with finite differences
    # dx = 1e-09
    # Adf = numpy.zeros((dim*N,dim*N))
    # dzdt0 = system(z,t,m,N,dim,rotating)
    # for i in range(dim*N):
    #     dzi = z.copy()
    #     dzi[i] = dzi[i]+dx
    #     dzim = z.copy()
    #     dzim[i] = dzim[i]-dx
    #     dzdti = system(dzi,t,m,N,dim,rotating)
    #     dzdtim = system(dzim,t,m,N,dim,rotating)
    #     Adf[i,:] = (dzdti-dzdtim)/(2.0*dx)
    # print ""
    # print "A=",A
    # print "Adf=", Adf.T
    # print "norm Adf-A = ", numpy.linalg.norm(Adf-A)
    # print "norm Adf.T-A = ", numpy.linalg.norm(Adf.T-A)

    zdzdt[N*dim:2*N*dim]=numpy.dot(A,zdz[N*dim:2*N*dim])
    return zdzdt


# the N-body system resolvant equation
def DsystemOpt(zdz,t,m,N,dim,rotating):
    """
    The vector field for the Nbody problem
    coordinates are organized as (r1,v1,r2,v2,..,rN,vN) and (dr1,dv1,dr2,dv2,..,drN,dvN)
    where r is the position in R^n where n=dim/2
    v the velocity in R^n and dr and dv are the variation position and velocity

    :param N: (int) number of bodies
    :param dim: (int) dimension of the phase space for one body
    :param zdz: (numpy array) state at which we want to compute the vector field. Dimenstion 2*dim*N
    :param t: (float) time at which we want to compute the vector field. Here the vector field is time independant
    :param rotating: (numpy array) rotation matrix for the frame. dimension dim/2 times dim/2
    :return: (numpy array) dz/dt the value of the vector field at state z (dimension N*dim)
    """

    # compute the dynamics
    # position and velocity
    z = zdz[0:N*dim].copy()
    dzdt = system(z,t,m,N,dim,rotating)

    # some constant parts
    n = int(dim/2)
    nZero = numpy.zeros((n,n),dtype=float)
    nId = numpy.eye(n,dtype=float)

    zdzdt = numpy.zeros(2*N*dim)
    zdzdt[0:N*dim] = dzdt.copy()

    # the dynamical matrix
    A = numpy.zeros((dim*N, dim*N))

    for i in range(N):
        qi = z[(i*dim):(i*dim+int(dim/2))]
        vi = z[(i*dim+int(dim/2)):(i*dim+dim)]
        dqi = zdz[dim*N+(i*dim):dim*N+(i*dim+int(dim/2))]
        dvi = zdz[dim*N+(i*dim+int(dim/2)):dim*N+(i*dim+dim)]
        # n first lines equal : dfi_1/dvi = Id, and dfi_1/d(qj,vj) = 0
        zdzdt[dim*N+i*dim:dim*N+(i*dim+int(dim/2))] = dvi
        # n second lines dfi_2/d(qj,vj)*zdz
        for j in range(N):
            qj = z[(j*dim):(j*dim+int(dim/2))]
            vj = z[(j*dim+int(dim/2)):(j*dim+dim)]
            dqj = zdz[dim*N+(j*dim):dim*N+(j*dim+int(dim/2))]
            dvj = zdz[dim*N+(j*dim+int(dim/2)):dim*N+(j*dim+dim)]

            elA = numpy.zeros((n,n))
            # dfi_1/dq_j = 0
            if(i==j):
                #elA[0:n,n:2*n] = nId.copy() # dfi_1/dvi
                for k in range(N):
                    if(k!=i):
                        qk = z[(k*dim):(k*dim+int(dim/2))]
                        rik = numpy.linalg.norm(qk-qi)
                        # dfi_2/dqi
                        elA[:,:] = elA[:,:]-m[k]/numpy.power(rik,3.0)*nId+3.0*m[k]/numpy.power(rik,5.0)*(numpy.dot(numpy.array([qk-qi]).T,numpy.array([qk-qi])))
                zdzdt[dim*N+(i*dim+int(dim/2)):dim*N+(i+1)*dim]=zdzdt[dim*N+(i*dim+int(dim/2)):dim*N+(i+1)*dim]+numpy.dot(elA,dqi)
                if(isinstance(rotating,numpy.ndarray)):
                    zdzdt[dim*N+(i*dim+int(dim/2)):dim*N+(i+1)*dim]=zdzdt[dim*N+(i*dim+int(dim/2)):dim*N+(i+1)*dim]-numpy.dot(numpy.dot(rotating,rotating),dqi)-2.0*numpy.dot(rotating,dvi)
            else: #j!=i
                rij = numpy.linalg.norm(qj-qi)
                #dfi_2/dqj
                zdzdt[dim*N+(i*dim+int(dim/2)):dim*N+(i+1)*dim]=zdzdt[dim*N+(i*dim+int(dim/2)):dim*N+(i+1)*dim] + numpy.dot(m[j]/numpy.power(rij,3.0)*nId-3.0*m[j]/numpy.power(rij,5.0)*(numpy.dot(numpy.array([qj-qi]).T,numpy.array([qj-qi]))),dqj)


    ## Validation with finite differences
    # dx = 1e-09
    # Adf = numpy.zeros((dim*N,dim*N))
    # dzdt0 = system(z,t,m,N,dim,rotating)
    # for i in range(dim*N):
    #     dzi = z.copy()
    #     dzi[i] = dzi[i]+dx
    #     dzim = z.copy()
    #     dzim[i] = dzim[i]-dx
    #     dzdti = system(dzi,t,m,N,dim,rotating)
    #     dzdtim = system(dzim,t,m,N,dim,rotating)
    #     Adf[i,:] = (dzdti-dzdtim)/(2.0*dx)
    # print ""
    # print "A=",A
    # print "Adf=", Adf.T
    # print "norm Adf-A = ", numpy.linalg.norm(Adf-A)
    # print "norm Adf.T-A = ", numpy.linalg.norm(Adf.T-A)


    return zdzdt


# the RCTBP system Cross
def systemRCTBPCross(z,t,mu,P1,P2):
    """
    The vector field for the RCTBP in Cross coordinates
    coordinates (r,v) in R^6
    where r is the position in R^3
    and v the velocity in R^3

    :param z: (numpy array) state at which we want to compute the vector field. Dimension : 6
    :param t: (float) time at which we want to compute the vector field. Here the vector field is time independant
    :param mu: (float) parameter of the considered RCTBP
    """

    # primary coordinates
    #xP1 = system.P1#numpy.array([-mu,0.0,0.0,0.0,0.0,0.0])
    #xP2 = system.P2#numpy.array([1.0-mu,0.0,0.0,0.0,0.0,0.0])
    r13 = numpy.linalg.norm(z[0:3]-P1[0:3])
    r23 = numpy.linalg.norm(z[0:3]-P2[0:3])
    dzdt = numpy.zeros(6)


    # velocity
    dzdt[0] = z[3]
    dzdt[1] = z[4]
    dzdt[2] = z[5]
    # acceleration
    dzdt[3] = z[0]+2.0*z[4]-(1.0-mu)*(z[0]-P1[0])/numpy.power(r13,3.0)-mu*(z[0]-P2[0])/numpy.power(r23,3.0)
    dzdt[4] = z[1]-2.0*z[3]-(1.0-mu)*(z[1])/numpy.power(r13,3.0)-mu*(z[1])/numpy.power(r23,3.0)
    dzdt[5] = -(1.0-mu)*(z[2])/numpy.power(r13,3.0)-mu*(z[2])/numpy.power(r23,3.0)
    return dzdt


# the RCTBP system Richardson aroud L1
def systemRCTBPRichardsonL1(z,t,mu,P1,P2,d):
    """
    The vector field for the RCTBP in Richardson centered in L1
    coordinates (r,v) in R^6
    where r is the position in R^3
    and v the velocity in R^3

    :param z: (numpy array) state at which we want to compute the vector field. Dimension : 6
    :param t: (float) time at which we want to compute the vector field. Here the vector field is time independant
    :param mu: (float) parameter of the considered RCTBP
    :param d: (float) self.DL1 szebehely value
    """
    #print("integrate Richardson L1")
    #print(P1[0], (d-1.0)/d)
    #print(P2[0], 1.0)
    r13 = numpy.linalg.norm(z[0:3]-P1[0:3])
    r23 = numpy.linalg.norm(z[0:3]-P2[0:3])
    dzdt = numpy.zeros(6)
    correction = (1.0-mu)/d-1.0

    # velocity
    dzdt[0] = z[3]
    dzdt[1] = z[4]
    dzdt[2] = z[5]
    # acceleration
    dzdt[3] = z[0]+2.0*z[4]+correction-1.0/(d**3)*((1.0-mu)*(z[0]-P1[0])/numpy.power(r13,3.0)+mu*(z[0]-P2[0])/numpy.power(r23,3.0))
    dzdt[4] = z[1]-2.0*z[3]-1.0/(d**3)*((1.0-mu)*(z[1])/numpy.power(r13,3.0)+mu*(z[1])/numpy.power(r23,3.0))
    dzdt[5] = -1.0/(d**3)*((1.0-mu)*(z[2])/numpy.power(r13,3.0)+mu*(z[2])/numpy.power(r23,3.0))
    return dzdt

# the RCTBP system Richardson aroud L2
def systemRCTBPRichardsonL2(z,t,mu,P1,P2,d):
    """
    The vector field for the RCTBP in Richardson centered in L2
    coordinates (r,v) in R^6
    where r is the position in R^3
    and v the velocity in R^3

    :param z: (numpy array) state at which we want to compute the vector field. Dimension : 6
    :param t: (float) time at which we want to compute the vector field. Here the vector field is time independant
    :param mu: (float) parameter of the considered RCTBP
    :param d: (float) self.DL2 szebehely value
    """

    r13 = numpy.linalg.norm(z[0:3]-P1[0:3])
    r23 = numpy.linalg.norm(z[0:3]-P2[0:3])
    dzdt = numpy.zeros(6)
    correction = (1.0-mu)/d+1.0

    # velocity
    dzdt[0] = z[3]
    dzdt[1] = z[4]
    dzdt[2] = z[5]
    # acceleration
    dzdt[3] = z[0]+2.0*z[4]+correction-1.0/(d**3)*((1.0-mu)*(z[0]-P1[0])/numpy.power(r13,3.0)+mu*(z[0]-P2[0])/numpy.power(r23,3.0))
    dzdt[4] = z[2]-2.0*z[3]-1.0/(d**3)*((1.0-mu)*(z[1])/numpy.power(r13,3.0)+mu*(z[1])/numpy.power(r23,3.0))
    dzdt[5] = -1.0/(d**3)*((1.0-mu)*(z[2])/numpy.power(r13,3.0)+mu*(z[2])/numpy.power(r23,3.0))
    return dzdt
