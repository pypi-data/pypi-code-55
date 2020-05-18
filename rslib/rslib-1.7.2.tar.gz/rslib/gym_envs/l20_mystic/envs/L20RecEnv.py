import gym
from gym.utils import seeding

from rslib.algo.atrank import ATRankforRL3
from rslib.core.FeatureUtil import FeatureUtil
from rslib.gym_envs.l20_mystic.envs.L20RecEnvSrc import L20RecEnvSrc
from rslib.gym_envs.l20_mystic.envs.L20RecSim import L20RecSim
from rslib.gym_envs.l20_mystic.envs.L20controllerObs import controllerObs


class L20RecEnv(gym.Env):
    """
    This gym implements a simple recommendation environment for reinforcement learning.
    """

    def __init__(self,
                 statefile, actionfile, modelfile, config,
                 batch_size=None, one_step=False, reward_sqr=False, use_rslib_model=False, config_for_rslib_model=None, use_rule=True, reward_type='ctr'):

        obs_size = 256
        if batch_size:
            self.batch_size = batch_size
            self.batch = True
        else:
            self.batch_size = 1
            self.batch = False
        self.one_step = one_step
        self.reward_sqr = reward_sqr
        self.use_rslib_model = use_rslib_model
        self.use_rule = use_rule
        config['is_serving'] = 1
        model, sess = ATRankforRL3.get_model(config, return_session=True)
        self.src = L20RecEnvSrc(config, statefile, actionfile, batch_size=self.batch_size, reward_type=reward_type)
        self.sim = L20RecSim(self.src, model, modelfile, sess, steps=9, batch_size=self.batch_size, reward_sqr=self.reward_sqr, use_rule=self.use_rule)
        self.controllerobs = controllerObs(config, model, modelfile, sess, self.src, batch_size=self.batch_size, one_step=self.one_step, use_rule=self.use_rule)
        self.action_space = gym.spaces.Discrete(config['class_num'])
        self.observation_space = gym.spaces.Box(-10000.0, 10000.0, shape=(obs_size,))
        if use_rslib_model:
            self.FeatureUtil = FeatureUtil(config_for_rslib_model)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        self.stepp += 1

        action = action if self.batch else [action]
        new_rawstate, reward, done, info = self.sim._step(self.cur_rawstate, action, self.info)
        self.cur_rawstate = new_rawstate
        self.info = info
        # observation用于RL学习，每步都变
        if self.use_rslib_model:
            return self.FeatureUtil.feature_extraction(data=self.cur_rawstate, predict=True), reward, done, info

        observation = self.controllerobs.get_obs(new_rawstate, self.info, self.stepp)

        if self.batch:
            return observation, reward, done, info
        else:
            return observation[0], reward[0], done[0], info

    def reset(self, reset_user=True):
        self.stepp = 0
        self.sim.reset()
        self.info = self.sim.get_init_info()

        if reset_user:
            self.user = self.sim.recEnvSrc.get_random_user()
        self.cur_rawstate = self.sim.recEnvSrc.get_user_rawstate(self.user)

        if self.use_rslib_model:
            return self.FeatureUtil.feature_extraction(data=self.cur_rawstate, predict=True)

        observation = self.controllerobs.get_obs(self.cur_rawstate, self.info, self.stepp)
        if self.batch:
            return observation
        else:
            return observation[0]
