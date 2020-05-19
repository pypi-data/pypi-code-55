# Copyright 2018 Zhao Xingyu & An Yuexuan. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import numpy as np


# Modified Particle swarm optimization algorithm
class ModifiedPSO:
    def __init__(self, func=None, param_len=1, size=50, w=0.9, c1=2., c2=2., x_min=-10., x_max=10., v_min=-0.5,
                 v_max=0.5, r1=None, r2=None):
        self.func = func  # The method of calculating fitness
        self.param_len = param_len  # Number of parameters
        self.size = size  # How many particles
        self.w = w  # Inertial coefficient
        self.c1 = c1  # Cognitive coefficient
        self.c2 = c2  # Social coefficient
        self.history = []  # Optimal value of each iteration
        # Minimum position
        if type(x_min) != list:
            self.x_min = [x_min] * self.param_len
        else:
            assert len(x_min) == self.param_len  # wrong number of parameters
            self.x_min = x_min
        # Maximum position
        if type(x_max) != list:
            self.x_max = [x_max] * self.param_len
        else:
            assert len(x_max) == self.param_len  # wrong number of parameters
            self.x_max = x_max
        # Minimum speed
        if type(v_min) != list:
            self.v_min = [v_min] * self.param_len
        else:
            assert len(v_min) == self.param_len  # wrong number of parameters
            self.v_min = v_min
        # Maximum speed
        if type(v_max) != list:
            self.v_max = [v_max] * self.param_len
        else:
            assert len(v_max) == self.param_len  # wrong number of parameters
            self.v_max = v_max
        self.r1 = r1  # Random number 1
        self.r2 = r2  # Random number 2
        self.x = None  # Position
        self.v = None  # Velocity
        self.best_all_x = None  # Global optimal location
        self.best_all_score = None  # Global optimal score
        self.best_each_x = None  # Local optimum position
        self.best_each_score = None  # Local optimal score
        self._init_fit()

    def _init_fit(self):
        self.x = np.zeros([self.size, self.param_len])  # [Number of particles, number of parameters]
        self.v = np.zeros([self.size, self.param_len])
        for i in range(self.size):
            for j in range(self.param_len):
                self.x[i][j] = np.random.uniform(self.x_min[j], self.x_max[j])
                self.v[i][j] = np.random.uniform(self.v_min[j], self.v_max[j])
        self.best_all_x = np.zeros(self.param_len)  # Global optimal location
        self.best_all_score = -np.inf  # Global optimal score
        self.best_each_x = self.x.copy()  # Local optimum position
        self.best_each_score = np.full(self.size, -np.inf)  # Local optimal score

    def solve(self, epoch=50, verbose=False):
        self.history = []
        r1 = self.r1
        r2 = self.r2
        for _ in range(epoch):  # For each epoch
            # Configure random variables
            if r1 is None:
                r1 = np.random.uniform(0, 1)
            if r2 is None:
                r2 = np.random.uniform(0, 1)
            # Calculation of fitness
            for i in range(self.size):  # For the ith particle
                fitness = self.func(*self.x[i])
                # Update local optimal value and local optimal position
                if fitness > self.best_each_score[i]:
                    self.best_each_score[i] = fitness
                    self.best_each_x[i] = self.x[i].copy()
                if fitness > self.best_all_score:
                    self.best_all_score = fitness
                    self.best_all_x = self.x[i].copy()
            # Update particle speed and position
            self.v = self.w * self.v + self.c1 * r1 * (self.best_each_x - self.x) + self.c2 * r2 * (
                    self.best_all_x - self.x)
            for j in range(self.param_len):
                self.v[:, j] = np.clip(self.v[:, j], self.v_min[j], self.v_max[j])
            self.x = self.x + self.v
            for j in range(self.param_len):
                self.x[:, j] = np.clip(self.x[:, j], self.x_min[j], self.x_max[j])
            if verbose:
                print('Number of iterations: %i.' % (_ + 1), 'Best fitness: %.4f' % self.best_all_score)
            self.history.append(self.best_all_score)
        self.history = np.array(self.history)
        return self.best_all_x
