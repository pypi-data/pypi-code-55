# -*- coding: utf-8 -*-

import numpy as np
from .optimizer import Optimizer, CandidateState, OptimizationResults 
import copy
from scipy.interpolate import interp1d # need this for akb_model


class Particle(CandidateState):
    """PSO Particle class"""
    
    def __init__(self, optimizer: Optimizer):
        CandidateState.__init__(self, optimizer)
        #super(Particle, self).__init__(optimizer) # ugly version of the above
        
        self.V = np.zeros([optimizer.dimensions]) * np.nan

class PSO(Optimizer):
    """Particle Swarm Optimization class"""

    def __init__(self):
        """Initialization"""
        Optimizer.__init__(self)
        #super(PSO, self).__init__() # ugly version of the above

        self.X0 = None
        self.method = 'Vanilla'
        self.swarm_size = None
        self.iterations = None
        self.params = {}

    def init_params(self):

        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.method == 'Vanilla':
            mandatory_params = 'inertia cognitive_rate social_rate'.split()
            optional_params = 'akb_model akb_fun_start akb_fun_stop'.split()
        elif self.method == 'TVAC':
            mandatory_params = 'inertia'.split()
            optional_params = 'akb_model akb_fun_start akb_fun_stop'.split()

        # print(defined_params, mandatory_params, optional_params)

        for param in mandatory_params:
            # if param not in defined_params:
            #    print('Error: Missing parameter (%s)' % param)
            assert param in defined_params, f'Error: Missing parameter {param}'

        for param in defined_params:
            if param not in mandatory_params and param not in optional_params:
                print(f'Warning: Excessive parameter {param}')

        """ Anakatabatic Inertia a.k.a. Polynomial PFIDI """
        if self.params['inertia'] == 'anakatabatic':
            assert ('akb_fun_start' in defined_params \
                    and 'akb_fun_stop' in defined_params) \
                    or 'akb_model' in defined_params, \
                    'Error: anakatabatic inertia requires either akb_model parameter or akb_fun_start and akb_fun_stop parameters'
                    
            if 'akb_model' in defined_params:
                
                if self.params['akb_model'] == 'languid':
                    def akb_fun_languid(Th):
                        w = (0.72 + 0.05) * np.ones_like(Th)
                        for i, th in enumerate(Th):
                            if th < 4*np.pi/4: 
                                w[i] = 0
                        return w
                    self.params['akb_fun_start'] = akb_fun_languid
                    self.params['akb_fun_stop'] = akb_fun_languid                
                else:   # w-list-based named akb_models                
                    if self.params['akb_model'] == 'fish':
                        w_start = [1.4, 0.4, 0.8, 0.7, -1.5]
                        w_stop = [-0.7, 0.4, 0.0, -0.1, 1.8]
                        splinetype = 'cubic'
                        if self.method != 'TVAC':
                            print('Warning: akb_model \'fish\' was designed for TVAC PSO')                    
                    if self.params['akb_model'] == 'nosedive':
                        w_start = [-0.5, 2.0, -1.3, -0.6, -1.9]
                        w_stop = [2.0, 2.0, 1.9, -0.3, -2.0]
                        splinetype = 'linear'
                        if self.method != 'Vanilla':
                            print('Warning: akb_model \'nosedive\' was designed for Vanilla PSO')                    
                    # code shared for all w-list-based named akb_models
                    Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
                    self.params['akb_fun_start'] = \
                                        interp1d(Th, w_start, kind=splinetype)
                    self.params['akb_fun_stop'] = \
                                        interp1d(Th, w_stop, kind=splinetype)              
                
        
    def init(self):
        
        super(PSO, self).init()
        
        # Bounds for position and velocity
        self.lb = np.array(self.lb)
        self.ub = np.array(self.ub)
        self.v_max = 0.2 * (self.ub - self.lb)

        # Generate a swarm
        self.cS = np.array([Particle(self) for c in range(self.swarm_size)], dtype=Particle)
        
        # Prepare arrays
        self.dF = np.empty([self.swarm_size]) * np.nan

        # Generate initial positions
        for p in range(self.swarm_size):
            
            # Random position
            self.cS[p].X = np.random.uniform(self.lb, self.ub)
            
            # Using specified particles initial positions
            if self.X0 is not None:
                if p < np.shape(self.X0)[0]:
                    self.cS[p].X = self.X0[p]
                    
            # Generate velocity
            #self.V[p, :] = np.random.uniform(-self.v_max, self.v_max)
            self.cS[p].V = np.random.uniform(-self.v_max, self.v_max)
                        
            # Evaluate
            self.cS[p].evaluate()
            
            # No fitness change at the start
            self.dF[p] = 0.0
            
        # Use initial particles as best ones
        self.cB = np.array([cP.copy() for cP in self.cS], dtype=CandidateState)
        
        # Update the overall best
        #self.p_best = np.argmin([cP.f for cP in self.cB])
        self.p_best = np.argmin(self.cB)
            
        # Update history
        self.results = OptimizationResults(self)
        self.results.cHistory = [self.cB[self.p_best].copy()]
        
        self.BI = np.zeros(self.swarm_size, dtype=int)
        self.TOPO = np.zeros([self.swarm_size, self.swarm_size], dtype=np.bool)

        self.reinitialize_topology()
        self.find_neighbourhood_best()
        
        self.ET = np.zeros([self.iterations])
        
    def reinitialize_topology(self, k=3):
        self.TOPO[:, :] = False
        for p in range(self.swarm_size):
            links = np.random.randint(self.swarm_size, size=k)
            self.TOPO[p, links] = True
            self.TOPO[p, p] = True

    def find_neighbourhood_best(self):
        for p in range(self.swarm_size):
            links = np.where(self.TOPO[p, :])[0]
            #best = np.argmin(self.BF[links])
            p_best = np.argmin(self.cB[links])
            p_best = links[p_best]
            self.BI[p] = p_best

    def run(self):
        self.init_params()
        self.init()

        if self.verbose:
            if self.params['inertia'] == 'anakatabatic':
                self.report['theta'] = np.empty([self.swarm_size,
                                                 self.iterations])

        if 'inertia' in self.params.keys():
            w = self.params['inertia']
        if 'cognitive_rate' in self.params.keys():
            c1 = self.params['cognitive_rate']
        if 'cognitive_rate' in self.params.keys():
            c2 = self.params['social_rate']

        for i in range(self.iterations):
            R1 = np.random.uniform(0, 1, [self.swarm_size, self.dimensions])
            R2 = np.random.uniform(0, 1, [self.swarm_size, self.dimensions])

            """ LDIW """
            if self.params['inertia'] == 'LDIW':
                w = 1.0 - (1.0 - 0.4) * i / self.iterations

            """ TVAC """
            if self.method == 'TVAC':
                c1 = 2.5 - (2.5 - 0.5) * i / self.iterations
                c2 = 0.5 + (2.5 - 0.5) * i / self.iterations

            """ Anakatabatic Inertia """
            if self.params['inertia'] == 'anakatabatic':

                theta = np.arctan2(self.dF, np.min(self.dF))
                theta[theta < 0] = theta[theta < 0] + 2 * np.pi  # 3rd quadrant
                # fix for atan2(0,0)=0
                theta0 = theta < 1e-300
                theta[theta0] = np.pi / 4 + \
                    np.random.rand(np.sum(theta0)) * np.pi
                w_start = self.params['akb_fun_start'](theta)
                w_stop = self.params['akb_fun_stop'](theta)
                #print(w_start)
                w = w_start * (1 - i / self.iterations) \
                    + w_stop * (i / self.iterations)

                if self.verbose:
                    self.report['theta'][:, i] = theta
            
            w = w * np.ones(self.swarm_size) # ensure w is a vector
            
            # Calculate new velocity and new position
            
            for p, cP in enumerate(self.cS):

                self.cS[p].V = w[p] * self.cS[p].V + \
                               c1 * R1[p, :] * (self.cB[p].X - self.cS[p].X) + \
                               c2 * R2[p, :] * (self.cB[self.BI[p]].X - self.cS[p].X)
                        
                self.cS[p].X = self.cS[p].X + self.cS[p].V  
                
                # Correct position to the bounds
                cP.X = np.clip(cP.X, self.lb, self.ub)
#                ilb = cP.X < self.lb
#                cP.X[ilb] = self.lb[ilb]
#                iub = cP.X > self.ub
#                cP.X[iub] = self.ub[iub]         

            # Evaluate swarm
            for p, cP in enumerate(self.cS):
                
                # Get old fitness
                f_old = cP.f
                
                # Evaluate particle
                cP.evaluate()
                
                # Calculate dF
                self.dF[p] = f_old - cP.f
                
            for p, cP in enumerate(self.cS):
                # Update personal best
                if cP <= self.cB[p]:
                    self.cB[p] = cP.copy()  
            
            # Update the overall best
            self.p_best = np.argmin(self.cB)
                        
            # Update history
            self.results.cHistory.append(self.cB[self.p_best].copy())

            # Update swarm topology
            if np.min(self.dF) <= 0.0:
                self.reinitialize_topology()
                
            # Find best particles in neighbourhood 
            self.find_neighbourhood_best()

            if self.verbose:
                print(i, self.cB[self.p_best].f)

        return self.cB[self.p_best]
    
