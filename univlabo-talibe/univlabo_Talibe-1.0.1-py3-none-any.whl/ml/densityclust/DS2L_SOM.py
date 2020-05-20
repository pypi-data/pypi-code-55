# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:20:39 2020

@author: guenael
"""

from scipy.stats import rankdata
import numpy as np

class Rel_den_clust():
    
    def __init__(self, sim, sigma = 1):
        self.sim = np.array(sim)
        self.nbprot = int(self.sim.shape[1])
        self.sigma = sigma       
        self.makegraph() 
        self.protden()
        self.clustering()
        self.refine()
        self.dataclust = self.clust[np.argmin(sim, axis=1)]
        self.dataclustref = self.clustref[np.argmin(sim, axis=1)]

   
    def makegraph(self):
        self.graph = np.zeros((self.nbprot, self.nbprot))
        g = np.unique(np.argsort(self.sim, axis=1)[:,0:2], axis=0)
        for i in g: 
            self.graph[i[0],i[1]] = 1
            self.graph[i[1],i[0]] = 1
    
    def protden(self):
        self.den = np.exp(-np.square(self.sim)/(2*self.sigma**2)).mean(0)
        self.den = self.den / max(self.den)
        
    def maxden(self):
        self.clust = np.zeros(self.nbprot)
        self.maxdenclust = {}
        cur_clust = 1
        for p in range(self.nbprot):
            den = self.den[p]
            den_vois =  self.den[self.graph[p]==1]
            if len(den_vois)==0:
                self.clust[p]= -1
            elif den >= max(den_vois):
                self.clust[p]= cur_clust
                self.maxdenclust[cur_clust]=den
                cur_clust += 1
    
    def clustering(self):
        self.maxden()       
        clust_tmp = self.clust.copy()+1
        while (clust_tmp != self.clust).any():
            clust_tmp = self.clust.copy()
            for p in range(self.nbprot):
                den_vois =  self.den*self.graph[p]
                if not np.all(den_vois==0):
                    indmax = np.argmax(den_vois)
                    if self.clust[indmax]>0:
                        self.clust[p] = self.clust[indmax]
        
    def refine(self):
        self.clustref = np.array(self.clust,dtype=np.int)
        for i in range(self.nbprot):
            Ci = self.clustref[i]
            if Ci > -1:
                maxdeni = self.maxdenclust[Ci]
                for j in range(i+1,self.nbprot):
                    Cj = self.clustref[j]
                    if Cj > -1:
                        maxdenj = self.maxdenclust[Cj]
                        if self.graph[i,j]:
                            seuil = 1/(1/maxdeni+1/maxdenj)
                            if self.den[i] >= seuil and self.den[j] >= seuil:
                                self.clustref[self.clustref==self.clustref[j]] = self.clustref[i]
                                self.maxdenclust[self.clustref[i]]=max([maxdeni, maxdenj])
        self.clustref = rankdata(self.clustref, method='dense')        