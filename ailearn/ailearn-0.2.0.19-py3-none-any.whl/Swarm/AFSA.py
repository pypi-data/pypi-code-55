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


# Artificial fish swarm algorithm
class AFSA:
    def __init__(self, func=None, param_len=1, size=50, x_min=-10., x_max=10., visual=1., step=0.5, delta=1,
                 try_number=5):
        self.func = func  # The method of calculating adaptability coefficient
        self.param_len = param_len  # Number of parameters
        self.size = size  # How many fishes
        self.history = []  # Optimal value of each iteration
        # 最小位移
        if type(x_min) != list:
            self.x_min = [x_min] * self.param_len
        else:
            assert len(x_min) == self.param_len  # wrong number of parameters
            self.x_min = x_min
        # 最大位移
        if type(x_max) != list:
            self.x_max = [x_max] * self.param_len
        else:
            assert len(x_max) == self.param_len  # wrong number of parameters
            self.x_max = x_max
        self.visual = visual  # field of vision of fish
        self.step = step  # Step length of fish
        self.delta = delta  # Crowding factor
        self.try_number = try_number  # Number of foraging attempts
        self.x = None  # position
        self.score = None  # Score per fish
        self.best_all_x = None  # Global optimal location
        self.best_all_score = None  # Global optimal score
        self._init_fit()

    def _init_fit(self):
        self.x = np.zeros([self.size, self.param_len])  # [number of fish, number of parameters]
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
            for i in range(self.size):  # For fish i
                # Check for fish around
                fishes = []
                fish_idx = []
                fish_num = 0
                for j in range(self.size):  # Search for how many fish are nearby
                    if np.sum(np.square(self.x[i] - self.x[j])) < self.visual:
                        fish_num += 1
                        fishes.append(self.x[j])
                        fish_idx.append(j)
                if fish_num > 1:  # If there are fish around
                    fishes = np.array(fishes)
                    # Clustering behavior
                    centre = np.mean(fishes, 0)
                    if self.func(*centre) / fish_num > self.delta * self.score[i]:
                        self.x[i] += (centre - self.x[i]) / (np.sum(
                            np.square(centre - self.x[i])) + 10e-8) * self.step * np.random.rand()
                        self.x[i] = np.clip(self.x[i], self.x_min, self.x_max)
                        self.score[i] = self.func(*self.x[i])
                        # Update local optimal value and local optimal position
                        if self.score[i] > self.best_all_score:
                            self.best_all_score = self.score[i]
                            self.best_all_x = self.x[i].copy()
                        continue
                    # Tail chasing behavior
                    best_index = fish_idx[np.argmax(self.score[fish_idx])]
                    if self.score[best_index] / fish_num > self.delta * self.score[i]:
                        self.x[i] += (self.x[best_index] - self.x[i]) / np.sum(
                            np.square(self.x[best_index] - self.x[i])) * self.step * np.random.rand()
                        self.x[i] = np.clip(self.x[i], self.x_min, self.x_max)
                        self.score[i] = self.func(*self.x[i])
                        # Update local optimal value and local optimal position
                        if self.score[i] > self.best_all_score:
                            self.best_all_score = self.score[i]
                            self.best_all_x = self.x[i].copy()
                        continue
                # Foraging behavior
                find = False
                x = None
                for j in range(self.try_number):
                    x = self.x[i] + self.visual * np.random.uniform(-1, 1, self.param_len)
                    x = np.clip(x, self.x_min, self.x_max)
                    if self.func(*x) > self.score[i]:
                        find = True
                    break
                if find is True:
                    self.x[i] += (x - self.x[i]) / np.sum(np.square(x - self.x[i])) * self.step * np.random.rand()
                else:
                    self.x[i] += self.visual * np.random.uniform(-1, 1)
                self.x[i] = np.clip(self.x[i], self.x_min, self.x_max)
                self.score[i] = self.func(*self.x[i])
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
