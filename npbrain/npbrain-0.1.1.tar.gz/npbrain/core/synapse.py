from math import ceil
from typing import Union

import numpy as np

from npbrain import profile
from npbrain.utils import connection
from npbrain.utils import helper

__all__ = [
    'record_conductance',
    'initial_syn_state',
    'format_connection',
    'Synapses',
    'CondSynapses',
]


def record_conductance(state, g, delay_len):
    state[1][:delay_len - 1] = state[1][1: delay_len]
    state[1][0, :] = g


if profile.get_backend().startswith('numba'):
    from numba.core.dispatcher import Dispatcher

    record_conductance = helper.jit_function(record_conductance)


def format_connection(conn, num_pre, num_post, weights):
    if isinstance(conn, str):
        conn_name = conn
        i, j = connection.get_conn_by_name(conn_name, num_pre, num_post)
    elif isinstance(conn, dict):
        if 'method' in conn:
            conn_name = conn.pop('method')
            conn_pars = conn
            if callable(conn_name):
                i, j = conn_name(**conn_pars)
            else:
                i, j = connection.get_conn_by_name(conn_name, num_pre, num_post, **conn_pars)
        else:
            i, j = conn.pop('i'), conn.pop('j')
    elif callable(conn):
        i, j = conn(num_pre, num_post)
    else:
        raise ValueError()

    conn_mat = np.zeros((num_pre, num_post))
    conn_mat[i, j] = 1.
    conn_mat *= weights
    return conn_mat


def initial_syn_state(delay: Union[int, float],
                      dt: float,
                      num_pre: int,
                      num_post: int,
                      pre_shape_num: int = 0,
                      post_shape_num: int = 0,
                      conn_shape_num: int = 0):
    """
    For each state:

    -----------   [[..........],
    delays         [..........],
    -----------    [..........],
    variables      [..........],
    -----------    [..........]]

    :param delay:
    :type delay:
    :param post_shape_num:
    :type post_shape_num:
    :param num_post:
    :type num_post:
    :param dt:
    :type dt:
    :return:
    :rtype:
    """

    # state = []
    # if profile.get_backend().startswith('numba'):
    #     state = typed.List()

    # state with (pre_num, ) shape #
    ################################
    # The state is:
    # pre_spike   [[..........],
    # -----------  [..........],
    # other vars   [..........],
    # -----------  [..........]]
    pre_shape_state = np.zeros((1 + pre_shape_num, num_pre))

    # state with (post_num, ) shape #
    #################################
    # The state is:
    # ----------- [[..........],
    # delays       [..........],
    # -----------  [..........],
    # other vars   [..........],
    # -----------  [..........]]
    if delay is None: delay_len = 1
    elif isinstance(delay, (int, float)):
        delay_len = int(ceil(delay / dt)) + 1
    else: raise ValueError()
    post_shape_state = np.zeros((delay_len + post_shape_num, num_post))

    # state with (pre_num, post_num) shape #
    ########################################
    # The state is:
    # ----------- [[[..........],
    # conn mat      [..........]
    # -----------   [..........]],
    # -----------  [[..........]],
    # other vars   [[..........]],
    # -----------  [[..........]]]
    conn_shape_state = np.zeros((1 + conn_shape_num, num_pre, num_post))

    state = (pre_shape_state, post_shape_state, conn_shape_state)

    return state, delay_len


class Synapses(object):
    def __init__(self, **kwargs):
        assert 'update_state' in kwargs

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.pre.post_groups.append(self.post)
        self.post.pre_groups.append(self.pre)
        self.post.pre_synapses.append(self)
        self.pre.post_synapses.append(self)

        if 'output_synapse' not in kwargs:
            def f(neu_state, syn_state):
                neu_state[-1] += syn_state[1][0]
            self.output_synapse = f

        if profile.get_backend().startswith('numba'):
            if not isinstance(self.update_state, Dispatcher):
                self.update_state = helper.jit_function(self.update_state)
            if not isinstance(self.output_synapse, Dispatcher):
                self.output_synapse = helper.jit_function(self.output_synapse)


class CondSynapses(Synapses):
    def __init__(self, **kwargs):
        assert 'update_state' in kwargs

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.pre.post_groups.append(self.post)
        self.post.pre_groups.append(self.pre)
        self.post.pre_synapses.append(self)
        self.pre.post_synapses.append(self)

        if 'output_synapse' not in kwargs:
            E = self.E

            def f(neu_state, syn_state):
                syn_val = -syn_state[1][0] * (neu_state[0] - E)
                neu_state[-1] += syn_val

            self.output_synapse = f

        if profile.get_backend().startswith('numba'):
            if not isinstance(self.update_state, Dispatcher):
                self.update_state = helper.jit_function(self.update_state)
            if not isinstance(self.output_synapse, Dispatcher):
                self.output_synapse = helper.jit_function(self.output_synapse)
