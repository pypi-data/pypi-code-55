import math

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torchvision.utils

def dist_show(data, figsize=(5,5), title=None,
              xlabel='$q_{ij}$', ylabel='Counts', 
              xlim=None, ylim=None, bins=None,
              stat=True, save_path=None):
    
    if stat :
        print("- Stats")
        print("Max : %f"%np.max(data))
        print("Min : %f"%np.min(data))
        print("Mean : %f"%np.mean(data))
        print("Median : %f"%np.median(data))
    
    xsize, ysize = figsize
    fig = plt.figure(figsize=(xsize, ysize))
    
    sns.distplot(data, kde=False, bins=bins)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    if xlim is not None :
        plt.xlim(xlim)
    if ylim is not None :
        plt.ylim(ylim)    

    plt.title(title)
        
    plt.tight_layout()
    if save_path is not None :
        plt.savefig(save_path)
        print("Figure Saved!")
        
    plt.show()
    plt.clf()
    
def weight_show(model, ncols=2, figsize=(5,5), 
                title=None, filter=lambda x:True,
                xlabel='$q_{ij}$', ylabel='Counts',
                xlim=None, ylim=None, bins=None,
                stat=True, save_path=None) :
    
    if not isinstance(model, nn.Module) :
        raise ValueError(reduction + " is not valid")

    if ncols == 0 :
        
        params = []
        
        for name, param in model.named_parameters():
            if param.requires_grad and filter(name) :
                params.append(param.view(-1).cpu().detach())        
        
        data = torch.cat(params).view(-1).numpy()
        dist_show(data, figsize, title,
                  xlabel, ylabel,
                  xlim, ylim, bins,
                  stat, save_path)
    else :
        xsize, ysize = figsize
        
        subplots_num = 0
        for name, param in model.named_parameters():
            if param.requires_grad and filter(name) :
                subplots_num += 1

        nrows = math.ceil(subplots_num/ncols)
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols,
                                 figsize=(ncols*xsize, nrows*ysize))

        i = 0
        for name, param in model.named_parameters():
            if param.requires_grad and filter(name) :
                if ncols == 1:
                    ax = axes[i//ncols]
                else :
                    ax = axes[i//ncols, i%ncols]
                data = param.view(-1).cpu().detach().numpy()
                sns.distplot(data, kde=False, ax=ax, bins=bins)
                ax.set_ylabel(ylabel)
                ax.set_xlabel(xlabel)
                
                ax.set_xlim(xlim)
                ax.set_ylim(ylim)    
                
                ax.set_title(name)
                i += 1

        plt.tight_layout()
        if save_path is not None :
            plt.savefig(save_path)
            print("Figure Saved!")
        plt.show()
        plt.clf()
    
def logit_show(model, loader, figsize=(5,5),
               title=None, xlabel='$q_{ij}$', ylabel='Counts',
               xlim=None, ylim=None, bins=None,
               stat=True, save_path=None) :
    
    device = next(model.parameters()).device
    
    if not isinstance(model, nn.Module) :
        raise ValueError(reduction + " is not valid")

    logits = []

    for images, _ in loader :
        images = images.to(device)
        logit = model(images).cpu().detach()
        logits.append(logit.view(-1))        

    data = torch.cat(logits).view(-1).numpy()
    dist_show(data, figsize, title,
              xlabel, ylabel,
              xlim, ylim, bins,
              stat, save_path)
    
def grad_show(model, loader, figsize=(5,5),
              title=None, xlabel='$q_{ij}$', ylabel='Counts',
              xlim=None, ylim=None, bins=None,
              stat=True, save_path=None) :
    
    device = next(model.parameters()).device
    
    if not isinstance(model, nn.Module) :
        raise ValueError(reduction + " is not valid")

    grads = []
    
    loss = nn.CrossEntropyLoss()

    for images, labels in loader :
        images = images.to(device)
        labels = labels.to(device)
        
        images.requires_grad = True
        outputs = model(images)
        cost = loss(outputs, labels).to(device)
        
        grad = torch.autograd.grad(cost, images, 
                                   retain_graph=False, create_graph=False)[0]
        grad = grad.cpu().detach()
        grads.append(grad.view(-1))        

    data = torch.cat(grads).view(-1).numpy()
    dist_show(data, figsize, title,
              xlabel, ylabel,
              xlim, ylim, bins,
              stat, save_path)
    
def im_show(tensor, title="", figsize=(5,15), ncols=8, normalize=False, range=None,
           scale_each=False, padding=2, pad_value=0, save_path=None) :
    
    # tensor (Tensor or list) – 4D mini-batch Tensor of shape (B x C x H x W) or a list of images all of the same size.
    # nrow (python:int, optional) – Number of images displayed in each row of the grid. The final grid size is (B / nrow, nrow). Default: 8.
    # padding (python:int, optional) – amount of padding. Default: 2.
    # normalize (bool, optional) – If True, shift the image to the range (0, 1), by the min and max values specified by range. Default: False.
    # range (tuple, optional) – tuple (min, max) where min and max are numbers, then these numbers are used to normalize the image. By default, min and max are computed from the tensor.
    # scale_each (bool, optional) – If True, scale each image in the batch of images separately rather than the (min, max) over all images. Default: False.
    # pad_value (python:float, optional) – Value for the padded pixels. Default: 0.

    img = torchvision.utils.make_grid(tensor, ncols, padding, normalize, range, scale_each, pad_value)
    npimg = img.numpy()
    fig = plt.figure(figsize = figsize)
    plt.imshow(np.transpose(npimg,(1,2,0)))
    plt.title(title)
    plt.axis('off')
    plt.show()
    
    if save_path is not None :
        plt.savefig(save_path)
    
    plt.clf()