import numpy as np

from npbrain import profile
from npbrain.core.synapse import *
from npbrain.utils import helper

__all__ = [
    'NormalSynapses',
]


def NormalSynapses(pre, post, weights, conn, **kwargs):
    num_pre = pre.num
    num_post = post.num
    dt = kwargs.pop('dt', profile.get_dt())
    delay = kwargs.pop('delay', None)

    conn_mat = format_connection(conn, num_pre, num_post, weights)
    state, delay_len = initial_syn_state(delay, dt, num_pre, num_post,
                                         0, 0, 0)
    state[2][0, :] = conn_mat
    helper.check_params(kwargs)

    def update_state(state_, mat, t):
        spike = state_[0][0]
        g = np.dot(spike, mat)
        record_conductance(state_, g, delay_len)

    def output_synapse(neu_state, syn_state):
        # neu_nin_ref = np.where(neu_state[-4] < 1.)[0]
        # for i in neu_nin_ref:
        #     neu_state[0, i] += syn_state[0, i]
        neu_state[0] += (syn_state[1][0] * (neu_state[-4] < 1.))

    return Synapses(**locals())

