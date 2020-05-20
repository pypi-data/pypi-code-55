# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 15:33:14 2017
"""
from __future__ import absolute_import, division, print_function
import numpy as np
import random
from sklearn.cluster import KMeans
import time
from numpy.linalg import pinv
from scipy.stats import rankdata



## input: XX = matrice des distances,
## K = nb de cluster, S = nb points support

class BC_clustering_batch():




    def __init__(self, XS, L, K=3, init='k-means++', Tmax=5):
        """ cree
        :param XS:
        :type name : int
        :param L: distance euclidienne
        :type L : int
        :param K:
        :param init: le nombre K clusters
        :param Tmax: la dimension maximal
        """


        self.K = K
        self.L = L
        self.X = np.array(XS).shape[0]
        self.S = np.array(XS).shape[1]
        self.XS = XS ** 2
        self.SS = self.XS[self.L, :]

        start = time.time()

        self.Ax = self.BCProj()
        self.KS = self.Ax[np.random.choice(self.Ax.shape[0], self.K, replace=False), :]
        self.Cl = self.Assign()
        self.train(Tmax)

        end = time.time()
        self.time = (end - start)

    def train(self, Tmax):
        """
        :type
        :param Tmax:
        :return:
        """
        for i in range(Tmax):
            self.KS = self.Update()
            self.Cl = self.Assign()

    def Assign(self):

        Dist = self.distXK()
        return np.argmin(Dist, axis=1)

    def Update(self):
        KS = self.KS
        for k in np.unique(self.Cl):
            KS[k, :] = np.mean(self.Ax[self.Cl == k, :], axis=0)
        return KS

    def BCProj(self):
        if self.XS.ndim == 1:
            self.XS = np.array([self.XS])
        Ax = []
        ## COMPUTE M
        self.SS[0, :]
        Mg = np.tile(self.SS[0, :], (self.S - 1, 1))
        Md = self.SS[1:, :]
        M = np.vstack((Mg - Md, np.ones(self.S)))
        Mi = pinv(M)
        for x in self.XS:
            ## COMPUTE D
            D = np.append(x[0] - x[1:], 1)
            Ax.append(np.dot(Mi, D))
        return np.array(Ax)

    def distXK(self):
        if self.Ax.ndim == 1:
            self.Ax = np.array([self.Ax])
        Dxk = np.zeros((self.X, self.K))
        for i in range(len(self.Ax)):
            for j in range(len(self.KS)):
                a = self.Ax[i] - self.KS[j]
                Dxk[i, j] = -1 / 2 * np.dot(np.dot(a.T, self.SS), a)
        return Dxk


class BC_clustering_stoch(BC_clustering_batch):
    def __init__(self, XS, L, K=2, Tmax=5, alpha=0.1):
        self.K = K
        self.L = L
        self.X = np.array(XS).shape[0]
        self.S = np.array(XS).shape[1]
        self.XS = XS ** 2
        self.SS = self.XS[self.L, :]

        start = time.time()

        self.Ax = self.BCProj()
        self.KS = self.Ax[np.random.choice(self.Ax.shape[0], self.K, replace=False), :]
        self.Cl = np.zeros(self.X, dtype=int)
        self.train(Tmax, alpha)
        for x in range(self.X):
            self.Cl[x] = self.Assign(x)

        end = time.time()
        self.time = (end - start)

    def train(self, Tmax, alpha):
        for i in range(Tmax):
            for j in range(self.X):
                x = random.choice(range(self.X))
                self.Cl[x] = self.Assign(x)
                self.KS = self.Update(x, alpha)

    def Assign(self, x):
        Dist = self.distXK(x)
        return np.argmin(Dist)

    def Update(self, x, alpha):
        KS = self.KS
        w = self.Cl[x]
        KS[w, :] = (1 - alpha) * KS[w, :] + alpha * self.Ax[x, :]
        return KS

    def distXK(self, x):
        Dxk = []
        for j in range(self.K):
            a = self.Ax[x] - self.KS[j]
            Dxk.append(-1 / 2 * np.dot(np.dot(a.T, self.SS), a))
        return np.array(Dxk)

    def BCProj(self):
        if self.XS.ndim == 1:
            self.XS = np.array([self.XS])
        Ax = []
        ## COMPUTE M
        Mg = np.tile(self.SS[0, :], (self.S - 1, 1))
        Md = self.SS[1:, :]
        M = np.vstack((Mg - Md, np.ones(self.S)))
        Mi = pinv(M)
        for x in self.XS:
            ## COMPUTE D
            D = np.append(x[0] - x[1:], 1)
            Ax.append(np.dot(Mi, D))
        return np.array(Ax)
