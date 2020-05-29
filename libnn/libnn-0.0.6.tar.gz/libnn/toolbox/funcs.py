import numpy as np
import pandas as pd

class Functions(object):
    def __init__(self):
        pass
    
    @staticmethod
    def init_nn(net, *args):
        return net(*args)

    @staticmethod
    def save_csv(**kwargs):
        # load params: {
        pred_val = kwargs["pred_val"]
        true_val = kwargs["true_val"]
        path = kwargs["net_params_path"]
        run_mode = kwargs["run_mode"]
        # }

        # covert pred_val, true_val to 1d array, which can be compared in dataframe.
        # {
        if isinstance(pred_val, list):
            pred_val = np.array(pred_val)
        if isinstance(true_val, list):
            true_val = np.array(true_val)
        if pred_val.ndim > 1:
            pred_val = pred_val.ravel()
        if true_val.ndim > 1:
            true_val = true_val.ravel()
        # }
        
        # save to dataframe:{
        df = pd.DataFrame(list(zip(pred_val, true_val)), columns = ["pred", "ys"])
        # print(mean_squared_error(df["ys"].values, df["pred"].values))
        # print(median_absolute_error(df["ys"].values, df["pred"].values))
        # print(r2_score(df["ys"].values, df["pred"].values))
        if run_mode == "t2":
            filename = path.stem.split("_net_params")[0] + "_test.csv"
        elif run_mode == "a":
            filename = path.stem.split("_net_params")[0] + ".csv"
        else:
            filename = path.stem.split("_net_params")[0] + f"_{run_mode}.csv"
        df.to_csv(path.parent.joinpath(filename).as_posix())
        # }