from tests.test_segmentation.unet_seg_dataset import UnetSegDataset as Dataset
from tests.test_segmentation.model.unet.unet_model import UNet
from gcam import gcam
import torch
import os
from torch.utils.data import DataLoader
import gc
import time


class Tmp():

    def __init__(self):
        self.DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.dataset = Dataset(device=self.DEVICE)
        current_path = os.path.dirname(os.path.abspath(__file__))
        CECKPOINT_PATH = os.path.join(current_path, 'model/CHECKPOINT.pth')
        self.model = UNet(n_channels=3, n_classes=1)
        self.model.load_state_dict(torch.load(CECKPOINT_PATH, map_location=self.DEVICE))
        self.model.to(device=self.DEVICE)
        self.model.eval()

    def test_gbp_hook(self):
        model = gcam.inject(self.model, output_dir="results/unet_seg/gbp", backend="gbp",
                     postprocessor="sigmoid", evaluate=False, save_scores=True, save_maps=False, save_pickle=False, metric="wioa", label=lambda x: 0.5 < x, channels=1)
        model.eval()
        data_loader = DataLoader(self.dataset, batch_size=1, shuffle=False)
        # TODO: Memory leak finden (Oder nur beim testen?)
        start_time = time.time()
        for i, batch in enumerate(data_loader):
            #output = model(batch["img"], mask=batch["gt"])
            output = model(batch["img"])

        #model.dump()
        gc.collect()
        torch.cuda.empty_cache()
        end_time = time.time()
        print("Time elapsed: ", end_time - start_time)

        # if os.path.isdir("results"):
        #     shutil.rmtree("results")

    def test_gcam_hook(self):
        layer = 'full'
        metric = 'wioa'
        model = gcam.inject(self.model, output_dir="results/unet_seg/gcam_" + metric, backend="gcam", layer=layer, replace=False,
                                postprocessor="sigmoid", evaluate=True, save_scores=True, save_maps=False, save_pickle=False, metric=metric, label=lambda x: 0.5 < x, channels=1)
        model.eval()
        data_loader = DataLoader(self.dataset, batch_size=1, shuffle=False)
        # TODO: Memory leak finden (Oder nur beim testen?)
        model.test_run(next(iter(data_loader))["img"])
        start_time = time.time()
        for i, batch in enumerate(data_loader):
            output = model(batch["img"], mask=batch["gt"])

        model.dump()
        end_time = time.time()
        print("Time elapsed: ", end_time - start_time)
        gc.collect()
        torch.cuda.empty_cache()

        # if os.path.isdir("results"):
        #     shutil.rmtree("results")

    def test_ggcam_hook(self):
        layer = 'full'
        metric = 'wioa'
        model = gcam.inject(self.model, output_dir="results/unet_seg/ggcam_" + metric, backend="ggcam", layer=layer,
                                postprocessor="sigmoid", evaluate=True, save_scores=True, save_maps=False, save_pickle=False, metric=metric, label=lambda x: 0.5 < x, channels=1)
        model.eval()
        data_loader = DataLoader(self.dataset, batch_size=1, shuffle=False)
        # TODO: Memory leak finden (Oder nur beim testen?)
        model.test_run(next(iter(data_loader))["img"])
        start_time = time.time()
        for i, batch in enumerate(data_loader):
            output = model(batch["img"], mask=batch["gt"])

        model.dump()
        end_time = time.time()
        print("Time elapsed: ", end_time - start_time)
        gc.collect()
        torch.cuda.empty_cache()

        # if os.path.isdir("results"):
        #     shutil.rmtree("results")

    def test_gcampp_hook(self):
        layer = 'auto'
        metric = 'wioa'
        model = gcam.inject(self.model, output_dir="results/unet_seg/gcampp_" + metric, backend="gcampp", layer=layer,
                     postprocessor="sigmoid", evaluate=True, save_scores=True, save_maps=False, save_pickle=False, metric=metric, label=lambda x: 0.5 < x, channels=1)
        model.eval()
        data_loader = DataLoader(self.dataset, batch_size=1, shuffle=False)
        # TODO: Memory leak finden (Oder nur beim testen?)
        model.test_run(next(iter(data_loader))["img"])
        start_time = time.time()
        for i, batch in enumerate(data_loader):
            output = model(batch["img"], mask=batch["gt"])

        model.dump()
        end_time = time.time()
        print("Time elapsed: ", end_time - start_time)
        gc.collect()
        torch.cuda.empty_cache()

        # if os.path.isdir("results"):
        #     shutil.rmtree("results")

if __name__ == '__main__':
    test = Tmp()
    #test.test_gbp_hook()
    #test.test_gcam_hook()
    #test.test_ggcam_hook()
    test.test_gcampp_hook()