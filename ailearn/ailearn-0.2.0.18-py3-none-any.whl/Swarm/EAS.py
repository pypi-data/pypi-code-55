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


# Evolutionary strategy
class ES:
    def __init__(self, func=None, param_len=1, size=50, x_min=-10., x_max=10., alpha=0.5):
        self.func = func  # The method of calculating adaptability coefficient
        self.param_len = param_len  # Number of parameters
        self.size = size  # How many elements are there
        self.alpha = alpha  # Elimination rate
        self.history = []  # Optimal value of each iteration
        assert np.floor(self.size * (1 - self.alpha)) > 1
        # Minimum value
        if type(x_min) != list:
            self.x_min = [x_min] * self.param_len
        else:
            assert len(x_min) == self.param_len
            self.x_min = x_min
        # Maximum value
        if type(x_max) != list:
            self.x_max = [x_max] * self.param_len
        else:
            assert len(x_max) == self.param_len
            self.x_max = x_max
        self.x = None  # position
        self.v = None  # velocity
        self.best_all_x = None  # Global optimal location
        self.best_all_score = None  # Global optimal score
        self.score = None  # score
        self._init_fit()

    def _init_fit(self):
        self.x = np.zeros([self.size, self.param_len])  # [number of particles, number of parameters]
        self.v = np.random.uniform(size=[self.size, self.param_len])
        self.score = np.zeros(self.size)
        for i in range(self.size):
            for j in range(self.param_len):
                self.x[i][j] = np.random.uniform(self.x_min[j], self.x_max[j])
        self.best_all_x = np.zeros(self.param_len)  # Global optimal location
        self.best_all_score = -np.inf  # Global optimal score

    def solve(self, epoch=50, verbose=False):
        self.history = []
        for _ in range(epoch):  # For each epoch
            self.score = np.zeros(self.size)
            # Calculation of fitness
            for i in range(self.size):  # For fish i
                self.score[i] = self.func(*self.x[i])
            # Update local optimal value and local optimal position
            if np.max(self.score) > self.best_all_score:
                self.best_all_score = np.max(self.score)
                self.best_all_x = self.x[np.argmax(self.score)]
            # Survival of the fittest
            for i in range(int(self.size * self.alpha)):
                idx = np.argmin(self.score)
                self.x = np.delete(self.x, idx, axis=0)
                self.v = np.delete(self.v, idx, axis=0)
                self.score = np.delete(self.score, idx, axis=0)
            # Reproduction
            x = np.zeros([self.size, self.param_len])
            v = np.zeros([self.size, self.param_len])
            for i in range(self.size):
                a, b = np.random.choice(self.x.shape[0], 2, False)
                mean = (self.x[a] + self.x[b]) / 2
                v[i] = np.abs(np.random.normal((self.v[a] + self.v[b]) / 2, 0.1))
                x[i] = np.clip(np.random.normal(mean, v[i]), self.x_min, self.x_max)
            self.x = x.copy()
            self.v = v.copy()
            if verbose:
                print('Number of iterations: %i.' % (_ + 1), 'Best fitness: %.4f' % self.best_all_score)
            self.history.append(self.best_all_score)
        self.history = np.array(self.history)
        return self.best_all_x
