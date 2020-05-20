# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time

class Optimizer:
    """Base class for all optimization methods."""

    def __init__(self):
        """Initialization"""

        self.dimensions = None
        self.evaluation_function = None
        
        self.objectives = 1
        self.objective_weights = None
        self.objective_labels = None
        self.constraints = 0
        self.constraint_labels = None
        
        self.lb = None
        self.ub = None
        self.verbose = None
        self.report = {}
        
    def init(self):
        
        assert not isinstance(self.objectives, np.unsignedinteger), "optimizer.objectives should be positive integer"
        assert self.objectives > 0, "An optimizer.objectives should be positive integer"
        
        assert not isinstance(self.constraints, np.unsignedinteger), "optimizer.constraints should be unsigned integer"
        
        if self.objective_weights is None:
            self.objective_weights = np.ones(self.objectives) / self.objectives   
        else:
            assert len(self.objective_weights) == self.objectives, "optimizer.objective_weights list should contain number of elements equal to optimizer.objectives"
        
        if self.objective_labels is None:
            self.objective_labels = [f'o_{o}' for o in range(self.objectives)]   
        else:
            assert len(self.objective_labels) == self.objectives, "optimizer.objective_labels list should contain number of strings equal to optimizer.objectives"
            
        if self.constraint_labels is None:
            self.constraint_labels = [f'c_{c}' for c in range(self.constraints)]   
        else:
            assert len(self.constraint_labels) == self.constraints, "optimizer.constraint_labels list should contain number of strings equal to optimizer.constraints"
            
        self.ET = None
    
    def log(self, msg):
        print('    ' + msg)
        
    def tic(self):
        self._time1 = time.time()

    def toc(self, msg='', silent=False):

        s = time.time() - self._time1
        
        if not silent:        
            if s < 1:
                self.log('{}Elapsed time: {:.3f} miliseconds.'.format('' if msg == '' else msg + '. ', s*1e3))
            else:
                self.log('{}Elapsed time: {:.3f} seconds.'.format('' if msg == '' else msg + '. ', s))
            
        return s

class CandidateState:
    """Candidate solution for optimization problem"""
    
    
    def __init__(self, optimizer: Optimizer):
        self._optimizer = optimizer
        self.X = np.zeros(optimizer.dimensions)
        self.O = np.zeros(optimizer.objectives) * np.nan
        self.C = np.zeros(optimizer.constraints) * np.nan
        self.f = np.nan
                    
        # Evaluation
        if self._optimizer.objectives == 1 and self._optimizer.constraints == 0:
            self.evaluate = self._eval_fast
        else:
            self.evaluate = self._eval_full
        
        # Comparison operators
        if self._optimizer.objectives == 1 and self._optimizer.constraints == 0:
            self._eq_fn = CandidateState._eq_fast
            self._lt_fn = CandidateState._lt_fast 
            #self.__gt__ = self._gt_fast
        else:
            self._eq_fn = CandidateState._eq_full
            self._lt_fn = CandidateState._lt_full 
            #self.__gt__ = self._gt_full
        
        
    def copy(self):
        
        cP = CandidateState(self._optimizer)        
        # Real copy for ndarrays
        cP.X = np.copy(self.X)
        cP.O = np.copy(self.O)
        cP.C = np.copy(self.C)
        cP.f = self.f
        return cP
    
    def __str__(self): 
        nch = np.max([np.size(self.X), np.size(self.O), np.size(self.C)]) 
        nch = np.min([8, nch])
        #print(nch)
        s = '-' * (12 * nch + nch + 20)
        
        for i in range(int(np.ceil(np.size(self.X)/nch))):
            if i == 0:
                s += '\n' + 'X: '.rjust(20)
            else:
                s += '\n' + ' ' * 20
            s += ' '.join([f'{x:12.5e}' for x in self.X[i*nch:(i+1)*nch]])
        
        """
        s += '\n' + 'Objectives: '.rjust(20) + ' '.join([f'{o:12.5e}' for o in self.O]) + \
             '\n' + 'Constraints: '.rjust(20) + ' '.join([f'{c:12.5e}' for c in self.C]) + \
        """
        alllbl = self._optimizer.objective_labels + self._optimizer.constraint_labels
        lblchr = np.max([len(lbl) for lbl in alllbl]) + 3
        for o, olbl in zip(self.O, self._optimizer.objective_labels):
            s += '\n' + f'{olbl}: '.rjust(lblchr) + f'{o:12.5e}' 
        for c, clbl in zip(self.C, self._optimizer.constraint_labels):
            s += '\n' + f'{clbl}: '.rjust(lblchr) + f'{c:12.5e}' 
        s += '\n' + 'Fitness: '.rjust(lblchr) + f'{self.f:12.5e}' + \
             '\n' + '-' * (12 * nch + nch + 20)
        return s
    
    # Equality operator
    def __eq__(self, other): 
        return self._eq_fn(self, other) 
    
    @staticmethod
    def _eq_fast(a, b): 
        return a.f == b.f

    @staticmethod
    def _eq_full(a, b):
        return np.sum(np.abs(a.X - b.X)) + np.sum(np.abs(a.O - b.O)) + np.sum(np.abs(a.C - b.C)) == 0.0

    # Inequality operator
    def __ne__(self, other):
        return self.f != other.f
        #return not self.__eq__(other)
    
    # Less-then operator
    def __lt__(self, other):
        return self._lt_fn(self, other)    
    
    @staticmethod
    def _lt_fast(a, b): 
        #print('_lt_fast')
        return a.f < b.f   
    
    @staticmethod     
    def _lt_full(a, b):  
        #print("_lt_full")               
        if np.sum(a.C > 0) == 0 and np.sum(b.C > 0) == 0: 
            # Both are feasible
            # Better candidate is the one with smaller fitness
            return a.f < b.f
        
        elif np.sum(a.C > 0) == np.sum(b.C > 0): 
            # Both are unfeasible and break same number of constraints
            # Better candidate is the one with smaller sum of constraint values
            return np.sum(a.C) < np.sum(b.C)
        
        else:
            # The number of unsatisfied constraints is not the same
            # Better candidate is the one which breaks fewer constraints
            return np.sum(a.C > 0) < np.sum(b.C > 0)
       
    
    def __gt__(self, other):
        #print('__gt__')
        #return self.f > other.f
        return not (self._lt_fn(self, other) or self._eq_fn(self, other))
    """
    def _gt_fast(self, other):
        return self.f > other.f
    def _gt_full(self, other): 
        return not (self.__eq__(other) or self.__lt__(other))
    """    
    
    def __le__(self, other):
        #print('__le__')
        #return self.f <= other.f
        return self._lt_fn(self, other) or self.__eq__(other)
    
    def __ge__(self, other):
        #print('__ge__')
        #return self.f >= other.f
        return self.__gt__(other) or self.__eq__(other)
    
    
    def set_X(self, X: np.ndarray):
        assert np.size(self.X) == np.size(X), 'Unexpected size of optimization vector X'
        self.X = X
        
    def _eval_full(self):
        
        #print('_eval_full')
        #print(self.X.shape)
        
        oc = self._optimizer.evaluation_function(self.X)
        #print(oc)

        for io in range(self._optimizer.objectives):
            self.O[io] = oc[io]
        
        self.f = np.dot(self.O, self._optimizer.objective_weights)
        
        for ic in range(self._optimizer.constraints):
            self.C[ic] = oc[self._optimizer.objectives + ic]

        #print('_eval_full', self.X[:5], self.f)
        
    def _eval_fast(self):
        
        f = self._optimizer.evaluation_function(self.X)
        self.f = f
        self.O[0] = f 
        #print('_eval_fast', self.f, type(self.f))
        #input(' >> Press return to continue.')

class OptimizationRecord(CandidateState):
    
    def __init__(self, optimizer: Optimizer):
        super(OptimizationRecord, self).__init__(optimizer)        
        self.evaluation = None

class OptimizationResults:
    """Data holder for optimization results."""
    
    def __init__(self, optimizer: Optimizer):
        
        self.optimizer = optimizer
        self.cHistory = []
        
    def plot_convergence(self, axes=None):
        
        if axes is None:
            fig = plt.figure(constrained_layout=True)
            spec = gridspec.GridSpec(ncols=1, nrows=2, figure=fig)
            axo = fig.add_subplot(spec[0])
            axc = fig.add_subplot(spec[1], sharex=axo)
        else:
            axo, axc = axes
        
        for io in range(self.optimizer.objectives):
            O = np.array([cB.O[io] for cB in self.cHistory])
            axo.plot(np.arange(np.size(O)), O, label=self.optimizer.objective_labels[io], lw=1)
            
        F = np.array([cB.f for cB in self.cHistory])
        axo.plot(np.arange(np.size(F)), F, label='f', lw=2, ls='-', c='b')
         
        axo.legend()
        
        for ic in range(self.optimizer.constraints):
            C = np.array([cB.C[ic] for cB in self.cHistory])
            I = np.arange(np.size(C))
            axc.plot(I, C, label=self.optimizer.constraint_labels[io], lw=1)
            
            I = I[C > 0]
            C = C[C > 0]
            
            nc = np.sum(C>0)
            axc.plot(I[:nc], C[:nc], c='r', ls='-', lw=2)
            if nc == 1:
                axc.plot(I[:nc], C[:nc],'ro')
                
            
        axc.legend()
        
        axo.set_ylabel('Objectives')
        axc.set_xlabel('Iterations')
        axc.set_ylabel('Constraints')
        #ax.set_yscale('log')
        
        