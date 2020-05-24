import numpy as np

from npbrain import profile
from npbrain.utils import helper

__all__ = [
    'judge_spike',
    'output_spike',
    'initial_neu_state',
    'format_geometry',
    'format_refractory',
    'Neurons',
]


if profile.get_backend() == 'numpy':
    def judge_spike(neu_state, Vth, t):
        below_threshold = neu_state[0] < Vth
        above_threshold = np.logical_not(below_threshold)
        spike_st = np.logical_and(above_threshold, np.logical_not(neu_state[-3]))
        spike_idx = np.where(spike_st)[0]
        neu_state[-3] = spike_st
        neu_state[-2, spike_idx] = t
        return spike_idx
else:
    from numba.core.dispatcher import Dispatcher

    def judge_spike(neu_state, Vth, t):
        below_threshold = neu_state[0] < Vth
        above_threshold = np.logical_not(below_threshold)
        spike_st = np.logical_and(above_threshold, np.logical_not(neu_state[-3]))
        spike_idx = np.where(spike_st)[0]
        neu_state[-3] = spike_st
        for i in spike_idx:
            neu_state[-2, i] = t
        return spike_idx

    judge_spike = helper.jit_function(judge_spike)


def output_spike(syn_state, neu_state):
    syn_state[0][0, :] = neu_state[-3]


def initial_neu_state(num_var, num_neuron):
    """
    For each state:

    -----------   [[..........],
    variables      [..........],
    -----------    [..........],
    refractory     [..........],
    spike_state    [..........],
    spike_time     [..........],
    inputs         [..........]]

    Parameters
    ----------
    num_var :
    num_neuron :

    Returns
    -------

    """
    state = np.zeros((num_var + 4, num_neuron))
    state[-2] = -np.inf
    return state


def format_geometry(geometry):
    """

    Parameters
    ----------
    geometry :

    Returns
    -------

    """
    # define network geometry
    if isinstance(geometry, (int, float)):
        geometry = (1, int(geometry), 1)
    elif isinstance(geometry, tuple):
        # a tuple is given, can be 1 .. N dimensional
        width = int(geometry[0])
        height = int(geometry[1]) if len(geometry) >= 2 else 1
        depth = int(geometry[2]) if len(geometry) >= 3 else 1
        geometry = (width, height, depth)
    else:
        raise ValueError()
    num = int(np.prod(geometry))
    return num, geometry


def format_refractory(ref=None):
    """

    Parameters
    ----------
    ref :

    Returns
    -------

    """
    if ref is None:
        tau_ref = 0
    elif isinstance(ref, (int, float)):
        if ref > 0:
            tau_ref = float(ref)
        elif ref == 0:
            tau_ref = 0
        else:
            raise ValueError
    elif isinstance(ref, np.ndarray):
        assert np.alltrue(ref >= 0)
        tau_ref = ref
    else:
        raise ValueError()
    return tau_ref


class Neurons(object):
    def __init__(self, **kwargs):
        if 'kwargs' in kwargs:
            kwargs.pop('kwargs')

        assert 'update_state' in kwargs

        # set key and value
        for k, v in kwargs.items():
            setattr(self, k, v)

        if 'dt' not in kwargs:
            self.dt = profile.get_dt()

        # format functions
        if 'output_spike' not in kwargs:
            self.output_spike = output_spike

        if profile.get_backend().startswith('numba'):
            if not isinstance(self.update_state, Dispatcher):
                self.update_state = helper.jit_function(self.update_state)
            if not isinstance(self.output_spike, Dispatcher):
                self.output_spike = helper.jit_function(self.output_spike)

        # define external connections
        self.inputs = None
        self.pre_synapses = []
        self.post_synapses = []
        self.pre_groups = []
        self.post_groups = []

