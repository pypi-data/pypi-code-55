import numpy as np
from numpy_nn.activations import Sigmoid

def test_sigmoid():
    a = np.array([-20, -1, 0, 1, 20])
    sigmoid = Sigmoid()
    b = sigmoid(a)
    assert b.shape == a.shape