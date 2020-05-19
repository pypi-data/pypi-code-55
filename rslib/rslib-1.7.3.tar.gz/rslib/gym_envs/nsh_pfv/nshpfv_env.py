import gym
from gym import error, spaces, utils
from gym.utils import seeding
from collections import Counter
import tensorflow as tf
# from tensorflow import keras
import numpy as np
import json
from numpy import random
import requests
import pandas as pd
import logging
from rslib.core.FeatureUtil import FeatureUtil
from numpy import random
import numpy as np
from rslib.gym_envs.RecEnvSrc import RecEnvSrc
from rslib.gym_envs.RecSim import RecSim


class NSHpfvEnvSrc(object):

    def __init__(self, statefile, batch_size=1):
        self.batch_size = batch_size
        self.state_dict = {}
        self.fs = open(statefile, 'r')
        self.rawstate_cache(self.fs, 1)

    def rawstate_cache(self, f, num):
        for i in range(num):
            tmp = f.readline()
            role_id = str(i)
            self.state_dict[role_id] = tmp

    def get_user_rawstate(self, role_id):
        if self.batch_size:
            rawstate = [self.state_dict[str(role)] for role in role_id]
        else:
            rawstate = self.state_dict[str(role_id)]
        return rawstate

    def get_user_state(self, role_id):
        rawstate = self.get_user_rawstate(str(role_id))
        feature = self.rawstate_to_state(rawstate)
        return feature

    def get_random_user(self):
        return list(random.choice(list(self.state_dict.keys()), self.batch_size)) if self.batch_size else random.choice(list(self.state_dict.keys()))

    def get_random_user_rawstate(self):
        rawstate = self.get_user_rawstate(self.get_random_user())
        return rawstate

    def get_random_user_state(self):
        rawstate = self.get_random_user_rawstate()
        feature = self.rawstate_to_state([rawstate])
        return feature

    def rawstate_to_state(self, rawstates):
        L=[]
        for state in rawstates:
            state = state.strip()
            assert self.is_json(state)
            json_line = json.loads(state)
            tmp = json_line["message"].split("=")[1].replace("'", '"')
            param = json.loads(tmp)
            team = [np.sum([list(param[team][player].values())[:5] for player in param[team] if player!='wait_time'],-2) for team in param if team!='conf']
            team = [[x[0]/1/3, x[1]/2/3, x[2]/10000/3, x[3]/10/3, x[4]/100/3] for x in team]
            feats = np.concatenate((np.min(team,-2),np.average(team,-2),np.max(team,-2)))
            L.append(feats)
        return L

    def get_new_user_rawstate(self, rawstate, info):
        assert type(rawstate) == type('')
        return rawstate

    def get_new_user_state(self, rawstate, info):
        new_rawstate = self.get_new_user_rawstate(rawstate, info)
        feature = self.rawstate_to_state([new_rawstate])
        return feature

    def is_json(self, json_str):
        try:
            json.loads(json_str)
        except ValueError:
            return False
        return True

    def reset(self):
        self.state_dict = {}
        self.fs.seek(0, 0)
        self.rawstate_cache(self.fs, 1)


class NSHpfvEnv(gym.Env):
    """
    This gym implements a simple recommendation environment for reinforcement learning.
    """

    def __init__(self, statefile = 'test_data/pfv.log', config = {}):
        self.batch_size = config.get('batch_size',1)
        self.src = NSHpfvEnvSrc(statefile, self.batch_size)
        # self.action_space = spaces.Discrete(config['class_num'])
        self.action_space = spaces.Box(-1.0,
                                       1.0,
                                       shape=(9,),
                                       # dtype=np.float32
                                       )
        self.observation_space = spaces.Box(-100.0,
                                            100.0,
                                            shape=(15,),
                                            # dtype=np.float32
                                            )
        # self.info = self.sim.get_init_info()
        self.cur_rawstate = None
        self.cur_obs = None
        self.user = None
        self.url = 'http://nsh-matchmaking-pfv-cupai-rl-52-2335.apps.danlu.netease.com/'
        self.reset()

    def is_json(self, json_str):
        try:
            json.loads(json_str)
        except ValueError:
            return False
        return True

    def _rewardshape(self, x):
        return 1-5*x if x <= 0.15 else 0


    def _step(self, rawstates, myconfs):
        rewards=[]
        for state, myconf in zip(rawstates, myconfs):
            state = state.strip()
            assert self.is_json(state)
            json_line = json.loads(state)
            tmp = json_line["message"].split("=")[1].replace("'", '"')
            param = json.loads(tmp)
            param['conf'] = myconf
            result = requests.post(self.url + 'match', json=param).json()
            reward = np.sum([self._rewardshape(float(player['result'][1])) for player in result])
            rewards.append(reward)

        return [[]]*self.batch_size, rewards, [True]*self.batch_size, [{}]*self.batch_size

    def action2param(self, actions):
        cupai_conf_list = ['sort_waitpriority'
                            , 'sort_suwencnt'
                            , 'sort_teamlen'
                            , 'sort_zongping'
                            , 'team_zongpingadjust_1'
                            , 'team_zongpingadjust_2'
                            , 'team_zongpingadjust_3'
                            , 'team_zongpingadjust_4'
                            , 'lianbai_zongpingadjust']
        return [dict(zip(cupai_conf_list, action)) for action in actions]


    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    # def step(self, action):
    #     self.stepp += 1
    #     assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
    #     new_rawstate, reward, done, info = self.sim._step(self.cur_rawstate, action, self.info)
    #     self.cur_rawstate = new_rawstate
    #     self.info = info
    #     # observation用于RL学习，每步都变
    #
    #     observation = self.controllerobs.get_obs(new_rawstate, info,self.stepp)
    #     return observation, reward, done, info

    #一步走完
    def step(self, actions):
        self.stepp += 1
        assert self.action_space.contains(actions[0]), "%r (%s) invalid" % (actions[0], type(actions[0]))
        myconfs = self.action2param(actions)
        observations, rewards, dones, infos = self._step(self.cur_rawstate, myconfs)
        # self.cur_rawstate = new_rawstate
        # self.info = info
        # observation用于RL学习，每步都变

        # observation = self.controllerobs.get_obs(new_rawstate, info,self.stepp)
        return observations, rewards, dones, infos


    def reset(self):
        self.stepp=0
        self.src.reset()
        self.info = {}
        self.user = self.src.get_random_user()
        self.cur_rawstate = self.src.get_user_rawstate(self.user)
        self.cur_obs = self.src.rawstate_to_state(self.cur_rawstate)
        return self.cur_obs


if __name__ == '__main__':
    import sys

    sys.path.append("test_data")

    env = NSHpfvEnv('test_data/pfv.log', {})
    observations, rewards, dones, infos = env.step([[0.1]*9])

    import gym
    from gym.envs.registration import register
    from rslib.gym_envs.l20_mystic.Policy_gradient_softmax.RL_brain import PolicyGradient

    mykwargs = {'statefile': 'test_data/pfv.log',
                'config': {'batch_size':1}}

    register(
        id='NSHpfv-v0',
        entry_point='nshpfv_env:NSHpfvEnv',
        # timestep_limit=9,
        reward_threshold=1000.0,
        nondeterministic=False,
        kwargs=mykwargs
    )
    env = gym.make('NSHpfv-v0')
    RL = PolicyGradient(
        n_actions=env.action_space.shape[0],
        n_features=env.observation_space.shape[0],
        learning_rate=0.001,
        reward_decay=0.995,
        # output_graph=True,
    )
    for i_episode in range(1000):
        observation = env.reset()[0]
        while True:
            # if RENDER: env.render()
            action = RL.choose_action(observation)
            observation_, reward, done, info = env.step(action)  # reward = -1 in all cases
            RL.store_transition(observation[0], action[0], reward[0])
            if done:
                # calculate running reward
                ep_rs_sum = sum(RL.ep_rs)
                if 'running_reward' not in globals():
                    running_reward = ep_rs_sum
                else:
                    running_reward = running_reward * 0.99 + ep_rs_sum * 0.01
                print("episode:", i_episode, "  reward:", int(running_reward))
                print(info)
                print(ep_rs_sum)
                vt = RL.learn()  # train
                break
            observation = observation_

