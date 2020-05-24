import numpy as np

from npbrain.core.neuron import *
from npbrain.profile import get_dt
from npbrain.profile import get_backend
from npbrain.utils import helper
from npbrain.core import sde_generator


__all__ = [
    'LIF'
]


def LIF(geometry, init='reset', method='euler', **kwargs):
    num, geometry = format_geometry(geometry)
    dt = kwargs.pop('dt', get_dt())
    tau = kwargs.pop('tau', 10.)
    ref = kwargs.pop('ref', 1.)
    V_reset = kwargs.pop('V_reset', 0.)
    Vth = kwargs.pop('Vth', 10.)
    noise = kwargs.pop('noise', 0.)
    f = lambda V, t, Isyn: (-V + V_reset + Isyn) / tau
    if get_backend().startswith('numba'):
        f = helper.jit_lambda(f)
    g = noise / tau
    int_f = sde_generator(f, g, dt, method)
    helper.check_params(kwargs)

    # init state
    state = initial_neu_state(1, num)
    if init == 'zero':
        pass
    if init == 'reset':
        state[0] = V_reset
    if init == 'random':
        state[0] = np.random.uniform(size=(num, ))

    def update_state(state_, t):
        neu_nin_ref = (t - state_[-2]) > ref
        neu_in_ref_ = np.logical_not(neu_nin_ref)
        state_[-4] = neu_in_ref_
        V_old = state_[0]
        V_new = int_f(state_[0], t, state_[-1], )
        V_new = V_new * neu_nin_ref + V_old * neu_in_ref_
        state_[0] = V_new
        spike_idx = judge_spike(state_, Vth, t)
        # state_[0] = state_[0] * np.logical_not(state_[-3]) + \
        #             V_reset * state_[-3]
        for i in spike_idx:
            state_[0, i] = V_reset

    return Neurons(**locals())


