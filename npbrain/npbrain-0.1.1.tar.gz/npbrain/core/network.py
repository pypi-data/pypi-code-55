import time

import numpy as np

from npbrain import profile
from npbrain.core.monitor import SpikeMonitor, StateMonitor
from npbrain.core.neuron import Neurons
from npbrain.core.synapse import Synapses
from npbrain.utils.helper import Dict

__all__ = [
    'Network'
]


class Network(object):
    def __init__(self, *args, **kwargs):

        # store and neurons and synapses
        self.neurons = []
        self.synapses = []
        self.state_monitors = []
        self.spike_monitors = []

        # store all objects
        self._objsets = Dict()
        self.objects = []

        # record the current step
        self.current_t = 0.

        # add objects
        self.add(*args, **kwargs)

    def _add_obj(self, obj):
        if isinstance(obj, Neurons):
            self.neurons.append(obj)
        elif isinstance(obj, Synapses):
            self.synapses.append(obj)
        elif isinstance(obj, StateMonitor):
            self.state_monitors.append(obj)
        elif isinstance(obj, SpikeMonitor):
            self.spike_monitors.append(obj)
        else:
            raise ValueError('Unknown object type: {}'.format(type(obj)))
        self.objects.append(obj)

    def add(self, *args, **kwargs):
        """Add object (neurons or synapses or monitor) to the network.

        Parameters
        ----------
        args :
        kwargs :

        Returns
        -------

        """
        for obj in args:
            self._add_obj(obj)
        for name, obj in kwargs.items():
            self._add_obj(obj)
            self._objsets.unique_add(name, obj)
            if name in ['neurons', 'synapses', 'state_monitors',
                        'spike_monitors', '_objsets', 'objects',
                        'current_t', 'add', 'run', 'run_time']:
                raise ValueError('Invalid name: ', name)
            setattr(self, name, obj)

    def run(self, duration, report=False, inputs=(), receiver=()):
        """Run the network.

        Parameters
        ----------
        duration :
        report :
        inputs :
        receiver :

        Returns
        -------

        """
        # -----------------
        # initialization
        # -----------------

        # time
        ts = np.arange(self.current_t, self.current_t + duration, profile.get_dt())
        run_length = len(ts)

        # initialize the neurons
        for mon in self.state_monitors:
            mon.init_state(run_length)
        for mon in self.spike_monitors:
            mon.init_state(run_length)

        # -------------------------
        # assign external inputs
        # -------------------------

        # format
        if not isinstance(inputs, (list, tuple)):
            inputs = [inputs]
        if not isinstance(receiver, (list, tuple)):
            receiver = [receiver]
        temp = []
        for rec in receiver:
            if isinstance(rec, Neurons):
                temp.append(rec)
            elif isinstance(rec, str):
                temp.append(self._objsets[rec])
            else:
                raise ValueError('Unknown object: ', rec)
        receiver = temp

        # classification
        iterable_inputs, iterable_rec = [], []
        fixed_inputs, fixed_rec = [], []
        for Iext, obj in zip(inputs, receiver):
            assert obj in self.objects
            if isinstance(Iext, (int, float)):
                Iext = np.ones(obj.num) * Iext
                fixed_inputs.append(Iext)
                fixed_rec.append(obj)
                continue
            size = np.shape(Iext)[0]
            if size != run_length:
                if size == 1:
                    Iext = np.ones(obj.num) * Iext
                elif size == obj.num:
                    pass
                else:
                    raise ValueError('Wrong size of inputs for', obj)
                fixed_inputs.append(Iext)
                fixed_rec.append(obj)
            else:
                assert np.size(Iext[0]) == 1 or np.size(Iext[0]) == obj.num
                iterable_inputs.append(Iext)
                iterable_rec.append(inputs)

        # ---------
        # run
        # ---------

        if report:
            report_gap = int(run_length / 10)
            t0 = time.time()

        for run_idx in range(run_length):
            t = ts[run_idx]

            # inputs
            for inputs, receiver in zip(iterable_inputs, iterable_rec):
                receiver.state[-1] = inputs[run_idx]
            for inputs, receiver in zip(fixed_inputs, fixed_rec):
                receiver.state[-1] = inputs

            # neurons
            for neu in self.neurons:
                neu.update_state(neu.state, t)
                for psyn in neu.post_synapses:
                    neu.output_spike(psyn.state, neu.state)

            # synapses
            for syn in self.synapses:
                syn.update_state(syn.state, syn.conn_mat, t)
                syn.output_synapse(syn.post.state, syn.state)

            # neurons
            for mon in self.state_monitors:
                mon.update_state(mon.obj.state, mon.vars_idx, mon.state, run_idx)
            for mon in self.spike_monitors:
                mon.update_state(mon.obj.state, mon.index, mon.time, t)

            if report and ((run_idx + 1) % report_gap == 0):
                percent = (run_idx + 1) / run_length * 100
                print('Run {:.1f}% using {:.3f} s.'.format(percent, time.time() - t0))
        if report:
            print('Done. ')

        # Finally
        self.current_t += duration

    @property
    def run_time(self):
        """Get the time points of the network.

        Returns
        -------
        times : numpy.ndarray
            The running time-steps of the network.
        """
        return np.arange(0, self.current_t, profile.get_dt())


