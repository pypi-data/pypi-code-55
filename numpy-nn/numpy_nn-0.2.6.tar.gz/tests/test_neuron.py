import numpy as np
from numpy_nn import Neuron
from numpy_nn.losses import MAE

def test_neuron_forward_operation():
    x = np.array([[1,1,1,1]])

    # create single neuron
    neuron = Neuron(4, 2)

    result = neuron.forward(x)
    print(result)
    assert result.shape == (1, 2)