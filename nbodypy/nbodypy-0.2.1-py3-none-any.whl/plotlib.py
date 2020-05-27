#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
The N-body class plotlib
================

:Example:

>>> import nbodypy.plotlib

This is a subtitle
-------------------

"""

import nbodypy
import numpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors

import os, sys

def get_cmap(N):
    '''
    Returns a function that maps each index in 0, 1, self... N-1 to a distinct
    RGB color.
    :param N: Number of bodies
    :return: a matplotlib.cm color map of size N'''
    color_norm  = colors.Normalize(vmin=0, vmax=N)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv')
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color


class Nbodyplot:
    '''
    Class to plot pictures for the nbodypy class
    '''
    def __init__(self, fig=1):
        """
        Constructor
        :param fig: (int) number of the matplotlib figure we consider (default =1)
        """
        self.grid = True
        self.fig = fig
        self.points = True
        self.nbrFig = 0
        #
    def textTeX(self, normal=False):
        '''
        Personalize the font for the legend
        :param normal: (boolean) to use TeX or the classical way of matlplotlib (default Fasle for TeX)
        '''
        plt.rc('text', usetex=not normal)
        plt.rc('font', family='serif')
    def plotSol2D(self,nbody,t,mode='show',name='trajectory',boundingbox = None,orbit=None):
        """
        Plot trajectory in the (x,y)-plane

        :param nbody: Nbody Class Instance
        :param t: (numpy.array) array of times of integration to plot the solution
        :param mode: (str)  to chose if window show or print in a
                     'pdf' or 'png' file (default 'show')
        :param name: (str)  name of the file if png or pdf file is
                     generated (default 'trajectory')
        :param boundingbox: (list)  of the form [xmin xmax ymin ymax] (default None)
        """
        if(isinstance(orbit,numpy.ndarray)):
            sol=orbit
        else:
            sol = nbody.integrate(t)
        fig = plt.figure(self.nbrFig,figsize=(14,14))
        self.nbrFig = self.nbrFig +1
        ax = fig.add_subplot(111)
        cmap = get_cmap(nbody._N)
        for i in range(nbody._N):
            ax.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+1], color=cmap(i))
            if(self.points==True):
                ax.plot(sol[-1,i*nbody._dim], sol[-1,i*nbody._dim+1],'o',color=cmap(i))
        if(self.grid):
            ax.grid()
        ax.set_aspect('equal')
        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')
        if(isinstance(boundingbox, list)):
            ax.set_xlim(boundingbox[0:2])
            ax.set_ylim(boundingbox[2:4])
        if(mode=='show'):
            plt.show()
        if(mode!='show'):
            fig.savefig(name+"."+mode,format=mode)
            plt.close()



    def plotSol3D(self,nbody,t,mode='show',name='trajectory',projection=True,orbit=None):
        """
        Plot trajectory in the (x,y)-plane, (y,z)-plane, (x-z)-plane and 3D view

        :param nbody: Nbody Class Instance
        :param t: (numpy.array) time of integration to plot the solution
        :param mode: (str)  to chose if window show or print in a
                     'pdf' or 'png' file (default 'show')
        :param name: (str)  name of the file if png or pdf file is
                     generated (default 'trajectory')
        :param projection: (boolean) to choose if we want 2D projections
                           (on (x,y)-plane, (y,z) plane and (x,z)-plane,
                           default) or to choose a 3D visualization
        """
        if(isinstance(orbit,numpy.ndarray)):
            sol=orbit
        else:
            sol = nbody.integrate(t)
        fig = plt.figure(self.nbrFig,figsize=(14,14))
        self.nbrFig = self.nbrFig +1
        if(projection):
            ax = fig.add_subplot(221, projection='3d')
        else:
            ax = fig.add_subplot(111, projection='3d')
        cmap = get_cmap(nbody._N)
        for i in range(nbody._N):
            ax.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+1], sol[:,i*nbody._dim+2], color=cmap(i))
            if(self.points==True):
                ax.scatter(sol[-1,i*nbody._dim], sol[-1,i*nbody._dim+1], sol[-1,i*nbody._dim+2], marker='.',color=cmap(i))
        if(self.grid):
            ax.grid()
        ax.set_aspect('equal')
        ax.title.set_text('3D view')
        if(projection):
            axXY = fig.add_subplot(222)
            axYZ = fig.add_subplot(223)
            axXZ = fig.add_subplot(224)
            for i in range(nbody._N):
                axXY.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+1], color=cmap(i))
                axYZ.plot(sol[:,i*nbody._dim+1], sol[:,i*nbody._dim+2], color=cmap(i))
                axXZ.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+2], color=cmap(i))
                if(self.points==True):
                    axXY.plot(sol[-1,i*nbody._dim], sol[-1,i*nbody._dim+1],marker='o',color=cmap(i))
                    axYZ.plot(sol[-1,i*nbody._dim+1], sol[-1,i*nbody._dim+2],marker='o',color=cmap(i))
                    axXZ.plot(sol[-1,i*nbody._dim], sol[-1,i*nbody._dim+2],marker='o',color=cmap(i))
            if(self.grid):
                axXY.grid()
                axYZ.grid()
                axXZ.grid()
            axXY.set_xlabel('$x$')
            axXY.set_ylabel('$y$')
            axYZ.set_xlabel('$y$')
            axYZ.set_ylabel('$z$')
            axXZ.set_xlabel('$x$')
            axXZ.set_ylabel('$z$')
        if(mode=='show'):
            plt.show()
        if(mode!='show'):
            fig.savefig(name+"."+mode,format=mode)
            plt.close()

    def plotManifolds(self,RCTBP,whichManifold='all',mode='show',name='trajectory',projection=True):
        """
        Plot set of trajectories defining the manifolds of a periodic orbit in
        the RCTBP problem

        :param RCTBP: RCTPB Class Instance
        :param mode: (str)  to chose if window show or print in a
                    'pdf' or 'png' file (default 'show')
        :param name: (str)  name of the file if png or pdf file is
                    generated (default 'trajectory')
        :param projection: (boolean) to choose if we want 2D projections
                        (on (x,y)-plane, (y,z) plane and (x,z)-plane,
                        default) or to choose a 3D visualization
        """
        if(not isinstance(RCTBP.manifoldRightStable,list)): # if manifolds are not generated
            exit
        else:
            fig = plt.figure(self.nbrFig,figsize=(14,14))
            self.nbrFig = self.nbrFig +1
        if(projection):
            ax = fig.add_subplot(221, projection='3d')
        else:
            ax = fig.add_subplot(111, projection='3d')
        for i in range(RCTBP.periodicOrbitPointNbr):
            if(whichManifold=='all'):
                ax.plot(RCTBP.manifoldRightStable[i][:,0], RCTBP.manifoldRightStable[i][:,1], RCTBP.manifoldRightStable[i][:,2], color='r')
                ax.plot(RCTBP.manifoldRightUnstable[i][:,0], RCTBP.manifoldRightUnstable[i][:,1], RCTBP.manifoldRightUnstable[i][:,2], color='g')
                ax.plot(RCTBP.manifoldLeftUnstable[i][:,0], RCTBP.manifoldLeftUnstable[i][:,1], RCTBP.manifoldLeftUnstable[i][:,2], color='b')
                ax.plot(RCTBP.manifoldLeftStable[i][:,0], RCTBP.manifoldLeftStable[i][:,1], RCTBP.manifoldLeftStable[i][:,2], color='y')
                if(self.points==True):
                    ax.scatter(RCTBP.manifoldRightStable[i][:,0], RCTBP.manifoldRightStable[i][:,1], RCTBP.manifoldRightStable[i][:,2], color='r', marker='.')
        if(self.grid):
            ax.grid()
            ax.set_aspect('equal')
            ax.title.set_text('3D view')
        if(projection):
            axXY = fig.add_subplot(222)
            axYZ = fig.add_subplot(223)
            axXZ = fig.add_subplot(224)
            for i in range(nbody._N):
                axXY.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+1], color=cmap(i))
                axYZ.plot(sol[:,i*nbody._dim+1], sol[:,i*nbody._dim+2], color=cmap(i))
                axXZ.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+2], color=cmap(i))
                if(self.points==True):
                    axXY.plot(sol[-1,i*nbody._dim], sol[-1,i*nbody._dim+1],marker='o',color=cmap(i))
                    axYZ.plot(sol[-1,i*nbody._dim+1], sol[-1,i*nbody._dim+2],marker='o',color=cmap(i))
                    axXZ.plot(sol[-1,i*nbody._dim], sol[-1,i*nbody._dim+2],marker='o',color=cmap(i))
            if(self.grid):
                axXY.grid()
                axYZ.grid()
                axXZ.grid()
                axXY.set_xlabel('$x$')
                axXY.set_ylabel('$y$')
                axYZ.set_xlabel('$y$')
                axYZ.set_ylabel('$z$')
                axXZ.set_xlabel('$x$')
                axXZ.set_ylabel('$z$')
        if(mode=='show'):
            plt.show()
        if(mode!='show'):
            fig.savefig(name+"."+mode,format=mode)
            plt.close()


    def plotSol4D(self,nbody,t,mode='show',name='trajectory',projection='3d'):
        """
        Plot a four dimensional solution

        :param nbody: Nbody Class Instance
        :param t: (float) time of integration to plot the solution (numpy.array)
        :param mode: (str)  to chose if window show or print in a 'pdf' or 'png' file (default 'show')
        :param name: (str)  name of the file if png or pdf file is generated (default 'trajectory')
        :param projection: (string) to choose, '3d' (default) : trajectories in the (x1,x2,x3)-plane, (x1,x2,x4)-plane, (x1,x3,x4)-plane, (x2,x3,x4)-plane,'2d': trajectories in the (x1,x2)-plane, (x1,x3)-plane, (x1,x4)-plane, (x2,x3)-plane, (x2,x4)-plane, (x3,x4)-plane
        """
        sol = nbody.integrate(t)
        if(projection=='3d'):
            fig = plt.figure(self.nbrFig,figsize=(14,14))
            self.nbrFig = self.nbrFig+1
            ax1 = fig.add_subplot(221, projection='3d')
            ax2 = fig.add_subplot(222, projection='3d')
            ax3 = fig.add_subplot(223, projection='3d')
            ax4 = fig.add_subplot(224, projection='3d')
            cmap = get_cmap(nbody._N)
            for i in range(nbody._N):
                ax1.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+1], sol[:,i*nbody._dim+2], color=cmap(i))
                ax2.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+1], sol[:,i*nbody._dim+3], color=cmap(i))
                ax3.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+2], sol[:,i*nbody._dim+3], color=cmap(i))
                ax4.plot(sol[:,i*nbody._dim+1], sol[:,i*nbody._dim+2], sol[:,i*nbody._dim+3], color=cmap(i))
                if(self.points==True):
                    ax1.scatter(sol[-1,i*nbody._dim], sol[-1,i*nbody._dim+1], sol[-1,i*nbody._dim+2], marker='.',color=cmap(i))
                    ax2.scatter(sol[-1,i*nbody._dim], sol[-1,i*nbody._dim+1], sol[-1,i*nbody._dim+3], marker='.',color=cmap(i))
                    ax3.scatter(sol[-1,i*nbody._dim], sol[-1,i*nbody._dim+3], sol[-1,i*nbody._dim+3], marker='.',color=cmap(i))
                    ax4.scatter(sol[-1,i*nbody._dim+1], sol[-1,i*nbody._dim+2], sol[-1,i*nbody._dim+3], marker='.',color=cmap(i))
            if(self.grid):
                ax1.grid()
                ax2.grid()
                ax3.grid()
                ax4.grid()
                #ax.set_aspect('equal')
            ax1.title.set_text('$(x_1,x_2,x_3)$')
            ax2.title.set_text('$(x_1,x_2,x_4)$')
            ax3.title.set_text('$(x_1,x_3,x_4)$')
            ax4.title.set_text('$(x_2,x_3,x_4)$')
        elif(projection=='2d'):
            fig = plt.figure(self.nbrFig,figsize=(16,10))
            self.nbrFig = self.nbrFig+1
            ax1 = fig.add_subplot(231)
            ax2 = fig.add_subplot(232)
            ax3 = fig.add_subplot(233)
            ax4 = fig.add_subplot(234)
            ax5 = fig.add_subplot(235)
            ax6 = fig.add_subplot(236)
            cmap = get_cmap(nbody._N)
            for i in range(nbody._N):
                ax1.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+1],  color=cmap(i))
                ax2.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+2],  color=cmap(i))
                ax3.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+3],  color=cmap(i))
                ax4.plot(sol[:,i*nbody._dim+1], sol[:,i*nbody._dim+2],  color=cmap(i))
                ax5.plot(sol[:,i*nbody._dim+1], sol[:,i*nbody._dim+3],  color=cmap(i))
                ax6.plot(sol[:,i*nbody._dim+2], sol[:,i*nbody._dim+3],  color=cmap(i))
                if(self.points==True):
                    ax1.plot(sol[-1,i*nbody._dim], sol[-1,i*nbody._dim+1], 'o', color=cmap(i))
                    ax2.plot(sol[-1,i*nbody._dim], sol[-1,i*nbody._dim+2], 'o', color=cmap(i))
                    ax3.plot(sol[-1,i*nbody._dim], sol[-1,i*nbody._dim+3], 'o', color=cmap(i))
                    ax4.plot(sol[-1,i*nbody._dim+1], sol[-1,i*nbody._dim+2],'o', color=cmap(i))
                    ax5.plot(sol[-1,i*nbody._dim+1], sol[-1,i*nbody._dim+3],'o', color=cmap(i))
                    ax6.plot(sol[-1,i*nbody._dim+2], sol[-1,i*nbody._dim+3],'o', color=cmap(i))
            if(self.grid):
                ax1.grid()
                ax2.grid()
                ax3.grid()
                ax4.grid()
                #ax.set_aspect('equal')
            ax1.set_xlabel('$x_1$')
            ax1.set_ylabel('$x_2$')
            ax2.set_xlabel('$x_1$')
            ax2.set_ylabel('$x_3$')
            ax3.set_xlabel('$x_1$')
            ax3.set_ylabel('$x_4$')
            ax4.set_xlabel('$x_2$')
            ax4.set_ylabel('$x_3$')
            ax5.set_xlabel('$x_2$')
            ax5.set_ylabel('$x_4$')
            ax6.set_xlabel('$x_3$')
            ax6.set_ylabel('$x_4$')
        if(mode=='show'):
            plt.show()
        if(mode!='show'):
            fig.savefig(name+"."+mode,format=mode)
            plt.close()

    def imageMovie2D(self,nbody,sol, I, prevIt = 0,boundingbox=None):
        """
        Function to create a image of the plot of a 2D solution to create a film

        :param nbody: Nbody Class Instance
        :param sol: (numpy.array) output of nbodypy.integrate() function
        :param I: (int) current, the range in the sol array
        :param prevIt: (int)  the previous range in the sol array, depending on the rate and the size of sol
        :param boundingbox: (list)  of the form [xmin xmax ymin ymax] (default None)
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cmap = get_cmap(nbody._N)
        for i in range(nbody._N):
            for j in range(I-prevIt, I):
                if(j>=0):
                    alphaV = (float(j-I+prevIt))/(float(prevIt))
                    ax.plot(sol[j,i*nbody._dim], sol[j,i*nbody._dim+1],
                            marker='o',
                            fillstyle='full',
                            markeredgewidth=0.0,
                            color=cmap(i),alpha = (alphaV*alphaV*alphaV))
            #ax.plot(sol[:,i*nbody._dim], sol[:,i*nbody._dim+1], color=cmap(i))
            ax.plot(sol[I,i*nbody._dim], sol[I,i*nbody._dim+1],'o',color=cmap(i))
            if(self.grid):
                ax.grid()
            ax.set_aspect('equal')
            if(isinstance(boundingbox, list)):
                ax.set_xlim(boundingbox[0:2])
                ax.set_ylim(boundingbox[2:4])





    def CreateMovie2D(self, nbody, time, numberOfFrames, prevTime=0.0, fps=24,name="trajectory",keep=False,mode="png",boundingbox=None):
        """
        Function to create a movie of the plot of a 2D solution. The fuction produce a set of pictures that may be collected to build a video with avconv software.

        :param nbody: Nbody Class Instance
        :param time: (float) total time of integration
        :param numberOfFrames: (int) number of Frames for the total video
        :param prevTime: (float) to get a trace of the past of each body (defaults 0.0)
        :param fps: (int) frame per second (default 24)
        :param keep: (boolean) to keep the different generated images (default False)
        :param mode: (str) to choose the format of each generated image (default 'png'), if mode='png' a mp4 movie is created
        :param boundingbox: (list)  of the form [xmin xmax ymin ymax] (default None)
        """
        os.system("mkdir movie"+name) # create the directory
        os.system("rm movie"+name+"/*") # clean the directory
        ttab = numpy.linspace(0.0, time, numberOfFrames)
        sol = nbody.integrate(ttab)
        prevItV = int((prevTime/time)*numberOfFrames)
        for i in range(numberOfFrames):
            self.imageMovie2D(nbody,sol,i,prevIt=prevItV,boundingbox=boundingbox)
            fname = name+'_%05d'%i
            fname = "movie"+name+"/"+fname+"."+mode
            plt.savefig(fname)
            plt.clf()
        if(mode=="png"):
            os.system("rm movie"+name+".mp4")
            os.system("avconv -r "+str(fps)+" -i movie"+name+"/"+name+"_%05d.png movie"+name+".mp4")
        if(keep==False):
            os.system("rm movie"+name+"/"+name+"_*."+mode)
            os.system("rm -r movie"+name)
