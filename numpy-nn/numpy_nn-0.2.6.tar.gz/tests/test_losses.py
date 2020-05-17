from numpy_nn.losses import MAE
import numpy as np

def test_mae_basic1():
    y_pred = np.array([[1,2],[3,4]])
    y = np.array([[2,3],[4,5]])
    mae = MAE()
    true_list = mae(y,y_pred)
    assert list(true_list) == [True, True]