# Copyright 2020 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from unittest.mock import patch
import copy
import numpy as np
import sympy

import cirq


class MockGet:

    def __init__(self, json):
        self.counter = 0
        self.json = json

    def raise_for_status(self):
        pass

    @property
    def text(self):
        self.counter += 1
        if self.counter > 1:
            return self.json


def _make_sampler() -> cirq.pasqal.PasqalSampler:

    sampler = cirq.pasqal.PasqalSampler(remote_host='http://00.00.00/',
                                        access_token='N/A')
    return sampler


def test_pasqal_circuit_init():
    qs = cirq.pasqal.ThreeDGridQubit.square(3)
    ex_circuit = cirq.Circuit()
    ex_circuit.append([[cirq.CZ(qs[i], qs[i + 1]),
                        cirq.X(qs[i + 1])] for i in range(len(qs) - 1)])
    device = cirq.pasqal.PasqalDevice(control_radius=3, qubits=qs)
    test_circuit = cirq.Circuit(device=device)
    test_circuit.append([[cirq.CZ(qs[i], qs[i + 1]),
                          cirq.X(qs[i + 1])] for i in range(len(qs) - 1)])

    for moment1, moment2 in zip(test_circuit, ex_circuit):
        assert moment1 == moment2


@patch('cirq.pasqal.pasqal_sampler.requests.get')
@patch('cirq.pasqal.pasqal_sampler.requests.post')
def test_run_sweep(mock_post, mock_get):
    """
    Encodes a random binary number in the qubits, sweeps between odd and even
    without noise and checks if the results match.
    """

    qs = [
        cirq.pasqal.ThreeDGridQubit(i, j, 0) for i in range(3) for j in range(3)
    ]

    par = sympy.Symbol('par')
    sweep = cirq.Linspace(key='par', start=0.0, stop=1.0, length=2)

    num = np.random.randint(0, 2**9)
    binary = bin(num)[2:].zfill(9)

    device = cirq.pasqal.PasqalDevice(control_radius=1, qubits=qs)
    ex_circuit = cirq.Circuit(device=device)

    for i, b in enumerate(binary[:-1]):
        if b == '1':
            ex_circuit.append(cirq.X(qs[-i - 1]))
    ex_circuit.append([cirq.measure(q) for q in qs])

    ex_circuit_odd = copy.deepcopy(ex_circuit)
    ex_circuit_odd.append(cirq.X(qs[0]))

    xpow = cirq.XPowGate(exponent=par)
    ex_circuit.append([xpow(qs[0])])

    mock_get.return_value = MockGet(cirq.to_json(ex_circuit_odd))
    sampler = _make_sampler()
    data = sampler.run_sweep(program=ex_circuit, params=sweep, repetitions=1)

    submitted_json = mock_post.call_args[1]['data']
    assert cirq.read_json(json_text=submitted_json) == ex_circuit_odd
    assert mock_post.call_count == 2
    assert data[1] == ex_circuit_odd
