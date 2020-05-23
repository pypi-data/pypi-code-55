import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from torchsummary import summary
import torchvision

classes = ('plane', 'car', 'bird', 'cat',
            'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

def model_summary(model):
    """Displays the Summary of the Architecture - All the methods used and the parameters used"""
    summary(model, input_size=(3, 32, 32))

#To Display random pictures
def unnorm(img, mean= (0.4914, 0.4822, 0.4465), std= (0.2023, 0.1994, 0.2010)):
        for t, m, s in zip(img, mean, std):
            t.mul_(s).add_(m)
            # The normalize code -> t.sub_(m).div_(s)
        return img

def _imshow(img):
    img = unnorm(img)      # unnormalize
    npimg = img.numpy()
    #print(npimg.shape)
    #print(np.transpose(npimg, (1, 2, 0)).shape)
    plt.figure()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))

def display(train_loader, n= 64,):

    # get some random training images
    dataiter = iter(train_loader)
    images, labels = dataiter.next()
    for i in range(0,n,int(np.sqrt(n))):
        #print('the incoming image is ',images[i: i+int(np.sqrt(n))].shape)
        _imshow(torchvision.utils.make_grid(images[i: i+int(np.sqrt(n))]))
        # print labels
        plt.title(' '.join('%7s' % classes[j] for j in labels[i: i+int(np.sqrt(n))]), loc= 'left')