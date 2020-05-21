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


# Firefly algorithm
class FA:
    def __init__(self, func=None, param_len=1, size=50, x_min=-10., x_max=10., beta=2, alpha=0.5, gamma=0.9):
        self.func = func  # The method of calculating adaptability coefficient
        self.param_len = param_len  # Number of parameters
        self.size = size  # How many fireflies are there
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
        self.alpha = alpha  # step
        self.beta = beta  # Maximum attraction
        self.gamma = gamma  # Light intensity absorption coefficient
        self.x = None  # location
        self.score = None  # Score per firefly
        self.best_all_x = None  # Global optimal location
        self.best_all_score = None  # Global optimal score
        self._init_fit()

    def _init_fit(self):
        self.x = np.zeros([self.size, self.param_len])  # [Number of fireflies, number of parameters]
        self.score = np.zeros(self.size)
        for i in range(self.size):
            for j in range(self.param_len):
                self.x[i][j] = np.random.uniform(self.x_min[j], self.x_max[j])
            self.score[i] = self.func(*self.x[i])
        self.best_all_score = np.max(self.score)  # Global optimal score
        self.best_all_x = self.x[np.argmax(self.score)]  # Global optimal location

    def solve(self, epoch=50, verbose=False):
        self.history = []
        for _ in range(epoch):  # For each epoch
            # Calculate distance
            distance = np.zeros([self.size, self.size])
            for i in range(self.size):
                for j in range(self.size - 1, i, -1):
                    distance[i][j] = np.linalg.norm(self.x[i] - self.x[j], 2)
                    distance[j][i] = distance[i][j]
            for i in range(self.size):  # For the ith firefly
                # For the brightest fireflies, do random motion
                if np.argmax(self.score) == i:
                    self.x[i] += self.alpha * np.random.uniform(-0.5, 0.5)
                    self.x[i] = np.clip(self.x[i], self.x_min, self.x_max)
                    self.score[i] = self.func(*self.x[i])
                    # Update local optimal value and local optimal position
                    if self.score[i] > self.best_all_score:
                        self.best_all_score = self.score[i]
                        self.best_all_x = self.x[i].copy()
                    continue
                lightness = np.zeros(self.size)
                # Find the Firefly with the highest relative brightness
                for j in range(self.size):
                    if j == i:
                        lightness[j] = -np.inf
                    else:
                        lightness[j] = self.score[j] * np.exp(-self.gamma * distance[i][j])
                idx = np.argmax(lightness)
                # Update firefly location
                self.x[i] += self.beta * np.exp(-self.gamma * np.square(distance[i][idx])) * (
                        self.x[idx] - self.x[i]) + self.alpha * np.random.uniform(-0.5, 0.5)
                self.score[i] = self.func(*self.x[i])
                self.x[i] = np.clip(self.x[i], self.x_min, self.x_max)
                # Update local optimal value and local optimal position
                if self.score[i] > self.best_all_score:
                    self.best_all_score = self.score[i]
                    self.best_all_x = self.x[i].copy()
            if verbose:
                print('Number of iterations: %i. The optimal parameters:' % (_ + 1), self.best_all_x,
                      'Best fitness: %.4f' % self.best_all_score)
            self.history.append(self.best_all_score)
        self.history = np.array(self.history)
        return self.best_all_x
