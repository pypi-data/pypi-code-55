import pickle
import numpy as np
from sklearn.model_selection import KFold, train_test_split
from pysy.toolbox.utils import Yaml, create_all_parents

class Splitter():
    """
    random_split for single train/test
    kfold_split for cross validation
    """
    def __init__(self):
        pass

    def __call__(
            self, 
            workspace, data_folder = "data", cv = False, 
            test_scale = 0.3, n_splits = 3,
            ext = "pkl", shuffle = True
        ):
        np.random.seed(0)
        self.random_state = 42 # for randomly split
        self.workspace = workspace
        # dataset supposed to be under dir "workspace/data/":    
        files_to_split = self.workspace.joinpath(data_folder).glob(f"*.{ext}")
        if cv:
            print("k-fold spliting...")
        else:
            print("random spliting...")
        for count, p in enumerate(files_to_split):
            self.filename = p.stem
            # load dataset: {
            with open(p.as_posix(), 'rb') as f:
                ds = pickle.load(f)
            Xs = ds["Xs"]
            ys = ds["ys"]
            # }
            if cv:
                self.kfold_split(Xs, ys, n_splits, shuffle)
            else:
                self.random_split(Xs, ys, test_scale)
            print(f"{str(count).zfill(3)}, {self.filename} splitted...")

    def random_split(self, Xs, ys, test_scale):
        # state static randomly split each dataset into train and test: {
        X_train, X_test, y_train, y_test = train_test_split(
            Xs, ys, test_size = test_scale, 
            random_state = self.random_state
            )
        # }
        # save splited train/test sets: {
            # save dir: "workspace/train_test"
        trainset = {"Xs": X_train, "ys": y_train}
        testset = {"Xs": X_test, "ys": y_test}
        save_folder = self.workspace.joinpath("train_test")
        create_all_parents(save_folder, flag = "d")
        with open(save_folder.joinpath(f"{self.filename}_train.pkl"), "wb") as f:
            pickle.dump(trainset, f)
        with open(save_folder.joinpath(f"{self.filename}_test.pkl"), "wb") as f:
            pickle.dump(testset, f)
        # }

    def kfold_split(self, Xs, ys, n_splits, shuffle):
        # state static kfold split for cross validation: {
        kf = KFold(
            n_splits = n_splits, 
            shuffle = shuffle, 
            random_state = self.random_state
        )
        # }

        # save splited train/test sets: {
            # save dir: "workspace/cross_val"
        for count, (train_index, test_index) in enumerate(kf.split(Xs)):
            print(f"CV{str(count).zfill(3)} TRAIN indices: {train_index}, TEST indices: {test_index}")
            X_train, X_test = Xs[train_index], Xs[test_index]
            y_train, y_test = ys[train_index], ys[test_index]
            trainset = {"Xs": X_train, "ys": y_train}
            testset = {"Xs": X_test, "ys": y_test}
            save_folder = self.workspace.joinpath("cross_val")
            create_all_parents(save_folder, flag = "d")
            with open(save_folder.joinpath(f"{self.filename}_cv_{str(count).zfill(3)}_train.pkl"), "wb") as f:
                pickle.dump(trainset, f)
            with open(save_folder.joinpath(f"{self.filename}_cv_{str(count).zfill(3)}_test.pkl"), "wb") as f:
                pickle.dump(testset, f)
        # }