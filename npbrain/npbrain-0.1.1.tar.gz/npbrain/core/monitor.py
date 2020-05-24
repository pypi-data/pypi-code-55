import numpy as np

from npbrain import profile
from npbrain.core.neuron import Neurons
from npbrain.core.synapse import Synapses
from npbrain.utils import helper

if profile.get_backend().startswith('numba'):
    from numba import typed, types
    from numba.core.dispatcher import Dispatcher

__all__ = [
    'Monitor',
    'SpikeMonitor',
    'StateMonitor'
]


class Monitor(object):
    def __init__(self, obj):
        self.obj = obj

        if profile.get_backend().startswith('numba'):
            if not isinstance(self.update_state, Dispatcher):
                self.update_state = helper.jit_function(self.update_state)

    def init_state(self, *args, **kwargs):
        raise NotImplementedError()


class SpikeMonitor(Monitor):
    def __init__(self, obj, ):
        self.vars = ['index', 'time']
        self.vars_idx = [-3, -3]
        super(SpikeMonitor, self).__init__(obj)

        assert isinstance(obj, Neurons)

        self.index = []
        self.time = []

    def init_state(self, length):
        self.index = []
        self.time = []
        if profile.get_backend().startswith('numba'):
            self.index = typed.List.empty_list(types.int64)
            self.time = typed.List.empty_list(types.float64)

    @staticmethod
    def update_state(obj_state, mon_index, mon_time, t):
        spike_idx = np.where(obj_state[-3] > 0)[0]
        for idx in spike_idx:
            mon_index.append(idx)
            mon_time.append(t)


class StateMonitor(Monitor):
    def __init__(self, obj, vars, vars_idx):
        # variables and variable indexes
        if isinstance(vars, str):
            vars = [vars]
            vars_idx = [vars_idx]
        vars = tuple(vars)
        vars_idx = tuple(vars_idx)
        self.vars = vars
        self.vars_idx = vars_idx

        # fake initialization
        for k in self.vars:
            setattr(self, k, np.zeros((1, 1)))
        self.state = []

        # function of update state
        def record_neu_state(obj_state, vars_idx, mon_states, i):
            var_len = len(vars_idx)
            for j in range(var_len):
                index = vars_idx[j]
                v = obj_state[index]
                mon_states[j][i] = v

        def record_syn_state(obj_state, vars_idx, mon_states, i):
            var_len = len(vars_idx)
            for j in range(var_len):
                index = vars_idx[j]
                v = obj_state[index[0]][index[1]]
                mon_states[j][i] = v

        if isinstance(obj, Neurons):
            self.update_state = record_neu_state
        elif isinstance(obj, Synapses):
            self.update_state = record_syn_state
        else:
            raise ValueError('Unknown type.')

        # super class initialization
        super(StateMonitor, self).__init__(obj)

    def init_state(self, length):
        assert isinstance(length, int)

        mon_states = []
        for i, k in enumerate(self.vars):
            index = self.vars_idx[i]
            if isinstance(self.obj, Synapses):
                v = self.obj.state
                for idx in index: v = v[idx]
            else: v = self.obj.state[index]
            shape = (length, ) + v.shape
            state = np.zeros(shape)
            setattr(self, k, state)
            mon_states.append(state)
        self.state = tuple(mon_states)


