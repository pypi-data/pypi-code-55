import argparse
import warnings
from pathlib import Path

import numpy as np
import torch
from pysy.toolbox.utils import Yaml, create_all_parents
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, utils

try:
    from libnn import *
    from .toolbox import *
    from .networks import *
except:
    from .toolbox import *
    from .networks import *


class Trainer():
    def __init__(
        self, 
        net, device, EPOCH, BATCH_SIZE, 
        NUM_WORKERS, lr, decay,
        early_stop_epoch, mean_loss_threshold, std_loss_threshold
        ):
        # params setting: {
            # num_classes: NN prediction dim
            # EPOCH: times of dataset iteration
            # BATCH_SIZE: size of data loader batch
            # NUM_WORKERS: workers number for loading dataset
            # lr: learning rate
            # decay: learning decay rate 
            # device: cpu/cuda
        self.net = net
        self.device = device
        self.EPOCH = EPOCH
        self.BATCH_SIZE = BATCH_SIZE
        self.NUM_WORKERS = NUM_WORKERS
        self.lr = lr
        self.decay = decay
        self.early_stop_epoch = early_stop_epoch
        self.mean_loss_threshold = mean_loss_threshold
        self.std_loss_threshold =  std_loss_threshold
        # }

    def train(self, train_path):
        # define dataset, dataloader, loss function and initial net: {
        dataset = Loader(
            file_path = train_path.as_posix(),
            transform = transforms.Compose([ToTensor()])
        )

        dataloader = DataLoader(
            dataset, 
            batch_size = self.BATCH_SIZE, 
            shuffle = True, 
            num_workers = self.NUM_WORKERS
        )
        loss_F = torch.nn.MSELoss()
        # net = ResNet18(num_classes = num_classes).to(device)
        net = self.net.to(self.device)
        # }

        # epach training: {
            # variable learning rate, and optimizer
            # optimizer: Adam
        for epoch in range(self.EPOCH):
            optimizer = torch.optim.Adam(net.parameters(), lr = self.lr)
            # decay the learning rate every self.EPOCH/4 epoches
            # for a better local minimum
            if self.EPOCH > 4:
                if epoch % (self.EPOCH // 4) == 0 and epoch != 0:
                    self.lr *= self.decay   
            losses = []
            # # print epoch count
            # print(f'Epoch: {epoch + 1}')

            # training each batch: {
            for step, data in enumerate(dataloader, 0):
                # load a batch, assign Xs, ys to device (cpu/cuda): {
                Xs, ys = data # print(Xs.shape)
                Xs, ys = Xs.to(self.device), ys.to(self.device)
                # }
                # apply net and calculate loss: {
                preds = net(Xs)
                loss = loss_F(preds, ys)
                # }
                # clean optimizer grad and backpropagate for next step: {
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                # }
                losses.append(loss.item())
                # print loss of each 10 batches: 
                if step % 10 == 0:
                    # sys.stdout.write(f"step {step} loss: {np.round(loss.item(), 4)}\r")
                    print(f"step {step} loss: {np.round(loss.item(), 4)}\r")
            # }            
            print(f"Epoch: {epoch}, loss: {np.round(np.mean(losses), 4)}, std: {np.round(np.std(losses), 4)}")
            # Early stopping:
            if epoch >= self.early_stop_epoch \
                and np.mean(losses) < self.mean_loss_threshold \
                and np.std(losses) < self.std_loss_threshold:
                break
        # }
        return net        

    def test(self, net_params_path, test_path, callback, run_mode = "t2"):
        net = self.net
        net.load_state_dict(torch.load(net_params_path))
        net.eval()
        if self.device.type == "cuda":
            net.cuda()
        pred_val = []
        true_val = []
        # define dataset, dataloader: {
        dataset = Loader(
            file_path = test_path.as_posix(),
            transform = transforms.Compose([ToTensor()])
        )

        dataloader = DataLoader(
            dataset, 
            batch_size = self.BATCH_SIZE,
            shuffle = False, 
            num_workers = self.NUM_WORKERS
        )
        # }

        # testing each batch: {
        for _, data in enumerate(dataloader, 0):
            # load a batch, assign Xs, ys to device (cpu/cuda): {
            Xs, ys = data
            # # use 80% data to prevent cuda out of memory
            # Xs = Xs[0: np.int(0.8 * Xs.shape[0]), :, :, :]
            # ys = ys[0: np.int(0.8 * ys.shape[0])]
            Xs, ys = Xs.to(self.device), ys.to(self.device)
            # }
            pred = net(Xs)
            pred_val.extend(pred.data.cpu().numpy())
            true_val.extend(ys.cpu().numpy())
        # }
        # call the post proc function, like Postproc.save_csv:
        callback(pred_val = pred_val, true_val = true_val, net_params_path = net_params_path, run_mode = run_mode)

def run(run_mode, config_file):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cfg = Yaml(config_file).load()

    workspace = cfg["directories"]["workspace"]
    workspace = Path(workspace)

    net = neuralnets[cfg["neural_network"]["name"]]
    # nn params must be in order
    # parse param dict into list
    net_params = [list(val.values())[0] for val in cfg["neural_network"]["params"]]
    net = Functions.init_nn(net, *net_params)

    runtime_params = [net, device] + [list(val.values())[0] for val in cfg["runtime"]]
    trainer = Trainer(*runtime_params)

    if run_mode == "t2":
        print("Enter train & test mode...")    
        split_params = cfg["split_params"]
        splitter = Splitter()
        splitter(workspace, **split_params)
        if split_params["cv"] == True:
            training_folder = workspace.joinpath("cross_val")
        else:
            training_folder = workspace.joinpath("train_test")

        train_test_paths = zip(
            training_folder.glob(r"*train.pkl"),
            training_folder.glob(r"*test.pkl")
        )

        for count, (train_path, test_path) in enumerate(train_test_paths):
            name = train_path.stem.split("_train")[0]
            # init model save paths: {
            # # cannot load model directly which is an error of package pickle
            # save_model = data_folder.joinpath(f"{name_}net.pth") 
            net_params_path = training_folder.joinpath(f"{name}_net_params.pth")
            # }
            print("training...")
            print("-" * 40)
            net = trainer.train(train_path)
            # torch.save(net, save_model)
            torch.save(net.state_dict(), net_params_path)
            print(f"{train_path.stem} is trained...")

            print("testing...")
            print("-" * 40)
            trainer.test(net_params_path, test_path, Functions.save_csv)
            print(f"{test_path.stem} is tested...")

    else:
        print("Enter model application mode...")
        print("-" * 40)        
        paths = zip(
            workspace.joinpath(cfg["application"]["model_folder"]).glob(r"*.pkl"),
            workspace.joinpath(cfg["application"]["model_folder"]).glob(r"*.pth")
        )
        for data_path, model_path in paths:
            trainer.test(model_path, data_path, Functions.save_csv, run_mode = "a")
            print(f"apply model to {data_path.stem}...")  

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    parse = argparse.ArgumentParser()
    parse.add_argument("action", type = str, help = "run type, train and test (t2) or application (a)")
    parse.add_argument("--config", type = str, help = "position of yaml config file.", default = "run_config.yaml")
    args = parse.parse_args()
    config_file = args.config
    run_mode = args.action
    run(run_mode, config_file)
    # # example:
    # python dispatch.py t2 --c=run_config.yaml
