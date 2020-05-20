"""
Matchmaking environment.
https://github.com/openai/gym/blob/master/gym/core.py
https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
"""

import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import pandas as pd


class MatchMakingEnv(gym.Env):
    """
    Description:
        Match Making Env.

    Observation:
        Type: Discrete(N)
        Num	Observation                 Min         Max
        0	Cart Position             -4.8            4.8
        1	Cart Velocity             -Inf            Inf

    Actions:
        Type: Discrete(N)
        Num	Action
        0	Choose Player 0
        1	Choose Player 1
        ...

    Reward:
        Reward is 1 for every step taken, including the termination step

    Starting State:
        All observations are assigned a uniform random value in [-0.05..0.05]

    Episode Termination:
        Pole Angle is more than 12 degrees
        Cart Position is more than 2.4 (center of the cart reaches the edge of the display)
        Episode length is greater than 200
        Solved Requirements
        Considered solved when the average reward is greater than or equal to 195.0 over 100 consecutive trials.
    """

    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 50,
    }

    n_players = 100
    team_size = 2
    one_hot = True

    reward_table_1v1 = [
        [0, 1, -1, -1],
        [1, 0, -1, -1],
        [-1, -1, 0, 1],
        [-1, -1, 1, 0]
    ]

    reward_table_2v2 = [
        [0, 0.5, -1, -1, 0.5, -1, -1, -1, -1, -1],
        [0.5, 0, -1, -1, 0.5, -1, -1, -1, -1, -1],
        [-1, -1, 0, 0.5, -1, 0.5, 1, -1, -1, -1],
        [-1, -1, 0.5, 0, -1, 1, 0.5, -1, -1, -1],
        [0.5, 0.5, -1, -1, 0, -1, -1, -1, -1, -1],
        [-1, -1, 0.5, 1, -1, 0, 0.5, -1, -1, -1],
        [-1, -1, 1, 0.5, -1, 0.5, 0, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, 0, 0.5, 0.5],
        [-1, -1, -1, -1, -1, -1, -1, 0.5, 0, 0.5],
        [-1, -1, -1, -1, -1, -1, -1, 0.5, 0.5, 0],
    ]

    def __init__(self, config):

        self.x = None  # (batch_size, player_num, input_dim)

        #         self.n_players = n_players  # number of candidate players
        #         self.team_size = team_size  # number of players per team
        #         self.one_hot = one_hot  # one hot encoding for team players

        #         self.action_space = list(range(0, self.n_players))
        #         self.observation_space = None

        self.action_space = spaces.Discrete(self.n_players)
        self.observation_space = spaces.Box(-10000.0, 10000.0, shape=(self.team_size * 2 * self.n_players,))

        self.reward_range = (-float('inf'), float('inf'))

        # self.reward_table = np.array(self.reward_table_1v1).astype(float)
        self.reward_table = pd.DataFrame(data=self.reward_table_2v2,
                                         index=['11', '12', '13', '14', '22', '23', '24', '33', '34', '44', ],
                                         columns=['11', '12', '13', '14', '22', '23', '24', '33', '34', '44', ])

        self.state = None
        self.steps_done = 0
        self.steps_beyond_done = None

        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _reward_1v1(self, state, action, next_state):
        # n_chosed = (next_state == 0).sum()
        team_done = self.steps_done % (self.team_size * 2) == 0
        team_done = bool(team_done)
        if not team_done:
            reward = 0.0
        else:
            # state_team = np.nonzero(self.state_team)[0]
            assert len(self.state_team) == self.team_size * 2
            assert self.steps_done % (self.team_size * 2) == 0
            x = self.x[self.state_team]
            reward = self.reward_table[x[0], x[1]]
            # print(self.state_team, x, reward)
            self.state_team[:] = -1
        return reward

    def _reward_2v2(self, state, action, next_state):
        # n_chosed = (next_state == 0).sum()
        team_done = self.steps_done % (self.team_size * 2) == 0
        team_done = bool(team_done)
        if not team_done:
            reward = 0.0
        else:
            # state_team = np.nonzero(self.state_team)[0]
            assert len(self.state_team) == self.team_size * 2
            assert self.steps_done % (self.team_size * 2) == 0
            x = self.x[self.state_team] + 1
            x = [str(v) for v in x]
            reward = self.reward_table.loc[''.join(sorted([x[0], x[2]])), ''.join(sorted([x[1], x[3]]))]
            # print(self.state_team, x, ''.join(sorted([x[0], x[2]])), ''.join(sorted([x[1], x[3]])), reward)
            self.state_team[:] = -1
        return reward

    def step(self, action):
        assert action in self.action_space, "%r (%s) invalid" % (action, type(action))
        state = self.state
        next_state = state.copy()
        next_state[action] = 0
        self.steps_done += 1

        n = self.steps_done % (self.team_size * 2)
        #         if n == 1:
        #             self.state_team[:] = 0
        self.state_team[n - 1] = action
        state_team = self.state_team.copy()

        # r = self._reward_1v1(state, action, next_state)
        r = self._reward_2v2(state, action, next_state)

        self.state = next_state

        done = self.steps_done >= self.n_players
        # done = next_state.sum() >= self.n_players
        done = bool(done)

        if not done:
            reward = r
        elif self.steps_beyond_done is None:
            # episode just end!
            self.steps_beyond_done = 0
            reward = r
        else:
            if self.steps_beyond_done == 0:
                logger.warn("You are calling 'step()' even though this environment has already returned done = True. "
                            "You should always call 'reset()' once you receive 'done = True' "
                            "-- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0

        if self.one_hot:
            n = self.team_size * 2 - 1
            state_team = np.zeros(n * self.n_players).reshape(-1, self.n_players)
            p = self.state_team[self.state_team > -1]
            # print(self.state_team, p)
            state_team[range(len(p)), p] = 1
            state_team = state_team.reshape(-1).astype(int)
            return np.concatenate([self.state, state_team]), reward, done, {}

        # return (np.array(self.state), np.array(self.state_team)), reward, done, {}
        return np.concatenate([self.state, self.state_team]), reward, done, {}

    def reset(self):
        self.state = np.array([1] * self.n_players, dtype=int)
        self.state_team = np.array([-1] * self.team_size * 2, dtype=int)
        # self.x = np.random.randint(low=0, high=4, size=(self.n_players,))
        self.x = np.array([0, 1, 2, 3] * 25)
        # self.state = np.random.uniform(low=-0.05, high=0.05, size=(4,))
        self.steps_done = 0
        self.steps_beyond_done = None

        if self.one_hot:
            n = self.team_size * 2 - 1
            state_team = np.zeros(n * self.n_players).reshape(-1, self.n_players)
            p = self.state_team[self.state_team > -1]
            # print(self.state_team, p)
            state_team[range(len(p)), p] = 1
            state_team = state_team.reshape(-1).astype(int)
            return np.concatenate([self.state, state_team])

        # return np.array(self.state), np.array(self.state_team)
        return np.concatenate([self.state, self.state_team])

    def render(self, mode='human'):
        return None

    def close(self):
        return None


if __name__ == '__main__':

    env = MatchMakingEnv(None)

    state = env.reset()
    n_players = env.n_players
    print("Matching pool: \n", state)
    print("Player feture: \n", env.x)
    print("Reward table: \n", env.reward_table)

    # import itertools
    # actions = list(itertools.permutations(range(1, n_players + 1), 1))
    actions = np.random.permutation(range(0, n_players))
    print("Test actions: \n", actions)

    for i in range(n_players):
        env.render()
        # action = np.random.randint(low=1, high=8 + 1)  # this takes random actions
        action = actions[i]
        next_state, reward, done, info = env.step(action)
        # print("step %d:" % i, state[0].shape, state[1].shape, next_state[0].shape, next_state[1].shape)
        print("step %d:" % i,
              state[:n_players], state[n_players:],
              action,
              next_state[:n_players], next_state[n_players:],
              reward,
              done)
        # print("State transition: ", state, action, next_state, reward, done, '\n')
        state = next_state
        if done:
            state = env.reset()
    env.close()
