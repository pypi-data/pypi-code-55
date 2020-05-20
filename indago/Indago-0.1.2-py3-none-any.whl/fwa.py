# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 13:43:18 2018

@author: Stefan
"""

# -*- coding: utf-8 -*-

import numpy as np
from .optimizer import Optimizer, CandidateState, OptimizationResults
import random


class FWA(Optimizer):
    """Firework Algorithm class"""

    def __init__(self):
        """Initialization"""
        super(FWA, self).__init__()

        self.X = None
        self.X0 = None
        self.cX = None
        self.method = 'Vanilla'
        self.params = {}

    def init_params(self):

        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.method == 'Vanilla':
            mandatory_params = 'n m1 m2'.split()
            optional_params = ''.split()
        elif self.method == 'rank':
            mandatory_params = 'n m1 m2'.split()
            optional_params = ''.split()
        else:
            assert False, f'Uknonwn method! {self.method}'
            
        for param in mandatory_params:
            # if param not in defined_params:
            #     print('Error: Missing parameter (%s)' % param)
            assert param in defined_params, 'Error: Missing parameter (%s)' % param

        for param in defined_params:
            if param not in mandatory_params and param not in optional_params:
                print('Warning: Excessive parameter (%s)' % param)

    def init(self):
        
        super(FWA, self).init()
        self.cX = np.array([CandidateState(self) for p in range(self.params['n'])], dtype=CandidateState)
        
        # Generate initial positions
        for p in range(self.params['n']):
            
            # Random position
            self.cX[p].X = np.random.uniform(self.lb, self.ub, self.dimensions)
            
            # Using specified initial positions
            if not self.X0 is None:
                if p < np.shape(self.X0)[0]:
                    self.cX[p].X = self.X0[p]
                    
            # Evaluate
            self.cX[p].evaluate()

        self.cX = np.sort(self.cX)
        
        # Initialize the results
        self.results = OptimizationResults(self)
        self.results.cHistory = [np.min(self.cX).copy()]
        
        
        
    """
    Firework Algorithm
    """

    def run(self):
        """
        :param n: number of fireworks
        :param function: test function
        :param lb: lower limits for plot axes
        :param ub: upper limits for plot axes
        :param dimension: space dimension
        :param iteration: the number of iterations
        :param m1: parameter controlling the number of normal sparks
    (default value is 7)
        :param m2: parameter controlling the number of Gaussian sparks
    (default value is 7)
        :param eps: constant used to avoid division by zero (default value is 0.001)
        :param amp: amplitude of normal explosion (default value is 2)
        :param a: parameter controlling the lower bound for number of normal sparks
    (default value is 0.3)
        :param b: parameter controlling the upper bound for number of normal sparks,
     b must be greater than a (b is set to 3 by default)
        """

        self.init_params()
        self.init()
        
        n = self.params['n']

        #print('init sort:', np.sort([p.f for p in self.cX]))
        
            
        for i in range(self.iterations):

            explosion_sparks = self.explosion()
                        
            mutation_sparks = self.gaussian_mutation()

            #self.__mapping_rule(sparks, self.lb, self.ub, self.dimensions)
            for cS in (explosion_sparks + mutation_sparks):
                
                ilb = cS.X < self.lb
                cS.X[ilb] = self.lb[ilb]
                iub = cS.X > self.ub
                cS.X[iub] = self.ub[iub]
                
                cS.evaluate()
                
                self.cX = np.append(self.cX, [cS])
                
            #self.__selection(sparks, self.params['n'], self.evaluation_function)
            
            #print('evaluated sparks:', np.array([p.f for p in self.cX]))
            #p_sorted = np.argsort(self.cX)[:n]
            #self.cX = self.cX[p_sorted]
            self.cX = np.sort(self.cX)[:n]
                
            #print('sorted sparks:', ' '.join([f'{p.f:.12f}' for p in self.cX]))
            #print('sorted sparks:', len(self.cX))
            #input(' >> Press return to continue.')
        
            #print(self.cX.shape)
            #print(cS)
            
            #print(self.cX)

            #p_sorted = np.argsort(self.cX)[:n]
            
            # for p in range(self.swarm_size):
            #     self.F[p] = self.objective(self.X[p,:])

            #if np.min(self.cX) <= self.cB:
            #    self.cB = np.min(self.cX).copy()

            # Update history
            self.results.cHistory.append(np.min(self.cX).copy())
            
            #print(i, np.min(self.cX).f, len(explosion_sparks) + len(mutation_sparks) )
            #print(i, np.max(self.cX).O, np.max(self.cX).C, len(sparks))
            
            
            #sort = np.argsort(self.cX)
            #self.cX = self.cX[sort]
            #print(self.cX[0].O, self.cX[0].C)
        
        return np.min(self.cX)
        # self.best = Gbest
        # self._set_Gbest(Gbest)

    def explosion(self):
        eps=0.001
        amp=10
        a=0.01
        b=10
        F = np.array([cP.f for cP in self.cX])
        fmin = np.min(F)
        fmax = np.max(F)
        
        explosion_sparks = []
        for p in range(self.params['n']):
               
            cFw = self.cX[p].copy()
            #print(cFw.X)
            
            if self.method == 'Vanilla':
                # Number of sparks
                n1 = self.params['m1'] * (fmax - cFw.f + eps) / \
                    np.sum(fmax - F + eps)
                
                n1 = self.min_max_round(n1, self.params['m1'] * a, self.params['m2'] * b)
                
                # Amplitude
                A = amp * (cFw.f - fmin + eps) / \
                    (np.sum(F - fmin) + eps)
                #print('n1:', n1, 'A:', A)
                #print(f'{p} >>> f:{self.cX[p].f:.5f} Ac:{A}')

                for j in range(n1):
                    #cFw.X += np.random.uniform(-A, A) * np.random.randint(0, 1, cFw.X.size)
                    for k in range(self.dimensions):
                        if (random.choice([True, False])):
                            #print(f'{j},{k}: {cFw.X[k]} ==> ', end='')
                            cFw.X[k] += random.uniform(-A, A)
                            #print(f'{cFw.X[k]}')
                    #print(cFw.X)
                    explosion_sparks.append(cFw.copy())
                
            if self.method == 'rank':
                
                # Number of sparks
                vn1 = self.params['m1'] * (fmax - cFw.f + eps) / \
                    np.sum(fmax - F + eps)
                
                vn1 = self.min_max_round(vn1, self.params['m1'] * a, self.params['m2'] * b)
                
                n1 = self.params['m1'] * (self.params['n'] - p)**1 / np.sum(np.arange(self.params['n']+1)**1)
                n1 = random.choice([int(np.floor(n1)), int(np.ceil(n1))])
                #print(self.cX[p].f, vn1, n1)
                
                # Amplitude
                Ac = amp * (cFw.f - fmin + eps) / \
                    (np.sum(F - fmin) + eps)
                    
                #print('n1:', n1, 'A:', A)
                XX = np.array([cP.X for cP in self.cX])
                #print(XX.shape)
                
                # Uniform
                dev = np.std(XX, 0)
                avg_scale = np.average(np.sqrt(np.arange(self.params['n']) + 1))
                scale = np.sqrt(p + 1) / avg_scale
                
                #avg_scale = np.average(np.arange(self.params['n']) + 1)
                #scale = (p + 1) / avg_scale
                
                
                A = np.sqrt(12) / 2 * dev * scale
                A *= 1.5
                
                #print(f'{p} >>> {self.cX[p].f:.5f}, {self.cX[p].O}, {self.cX[p].C}')
                #print(f'      {n1}, {vn1}')
                #print(f'{p} >>> f:{self.cX[p].f:.5f} n1:{n1}, Ac:{Ac:.5f}, A:{np.average(A):.5f}, scale:{scale:.5f} avg.dev:{np.average(dev):.5f}')
                #print(A)
                #input(' > Press return to continue.')
                  
                
                #cS = cFw.copy()
                for j in range(n1):
                    cFw.X = cFw.X + np.random.uniform(-A, A) * np.random.randint(0, 1, A.size)
                    
                    for k in range(self.dimensions):
                        if (random.choice([True, False])):
                            # Uniform
                            cFw.X[k] += np.random.uniform(-A[k], A[k])
                            # Normal
                            # cFw.X[k] += random.normal(-A[k], A[k])
                    
                    #print(cS.X)
                    explosion_sparks.append(cFw.copy())  

        #print('expl sparks:', len(explosion_sparks))
        #input(' > Press return to continue.')
        return explosion_sparks
    
    """
    def __explosion_operator(self, sparks, fw, function,
                             dimension, m, eps, amp, Ymin, Ymax, a, b):
        
        sparks_num = self.__round(m * (Ymax - function(fw) + eps) /
                                  (sum([Ymax - function(fwk) for fwk in self.X]) + eps), m, a, b)
        print(sparks_num)

        amplitude = amp * (function(fw) - Ymax + eps) / \
            (sum([function(fwk) - Ymax for fwk in self.X]) + eps)

        for j in range(int(sparks_num)):
            sparks.append(np.array(fw))
            for k in range(dimension):
                if (random.choice([True, False])):
                    sparks[-1][k] += random.uniform(-amplitude, amplitude)
    """
    
    def gaussian_mutation(self):
        
        mutation_sparks = []
        for j in range(self.params['m2']):
            cFw = self.cX[np.random.randint(self.params['n'])].copy()
            g = np.random.normal(1, 1)
            for k in range(self.dimensions):
                if(random.choice([True, False])):
                    cFw.X[k] *= g
            mutation_sparks.append(cFw)

        #print('mut sparks:', np.sort([p.f for p in mutation_sparks]))
        #print('mut sparks:', len(mutation_sparks))
        return mutation_sparks
            
    def __mapping_rule(self, sparks, lb, ub, dimension):
        for i in range(len(sparks)):
            for j in range(dimension):
                if(sparks[i].X[j] > ub[j] or sparks[i].X[j] < lb[j]):
                    sparks[i].X[j] = lb[j] + \
                        (sparks[i].X[j] - lb[j]) % (ub[j] - lb[j])

    def __selection(self, sparks, n, function):
        
        for cS in sparks:
            cS.evaluate()
            #print(self.cX.shape)
            #print(cS)
            self.cX = np.append(self.cX, [cS])
            
            #print(self.cX)

        #p_sorted = np.argsort(self.cX)[:n]
        #self.cX = self.cX[p_sorted]
        #self.cX = np.sort(self.cX)#[:n]
        
        # self.X = sorted(np.concatenate((self.X, sparks)), key=function)[:n]

        #print('selection:', self.F[0], self.F[-1], len(sparks))

    def min_max_round(self, s, smin, smax):
        return int(np.round(np.min([np.max([s, smin]), smax])))

    def __round(self, s, m, a, b):
        if (s < a * m):
            return round(a * m)
        elif (s > b * m):
            return round(b * m)
        else:
            return round(s)
