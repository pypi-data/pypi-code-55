'''
Going to stop thinking about this now. No evidence that anyone cares about these
problems: could not find any clear evidence that people think about feature
selection for time series. And don't need to bother looking to know that people
don't care about channel selection for computer vision.

I could show this off as a Granger causality technique. But not very many people
care about that problem. I would be competing with cMLP/cLSTM, just using a
different sparsification mechanism. And those experiments were low stakes.

The point is, I'm done with this.
'''
import torch
import torch.nn as nn
from . import ConcreteMask


class ConcreteMaskConv1d(nn.Module):
    '''
    Input layer that selects channels for Conv1ds by learning a k-hot mask.

    Input is size (N, C_in, L_in).

    Args:
      input_size: number of inputs.
      k: number of features to be selected.
      temperature: temperature for Concrete samples.
      append: whether to append the mask to the input on forward pass.
    '''
    def forward(self, x, return_mask=False):
        # Sample mask.
        m = self.sample(sample_shape=(x.shape[0], 1))
        m = m.permute(0, 2, 1)

        # One sample per timepoint in each example. Problem: might want to
        # sample from different inputs periodically.
        # m = self.sample(sample_shape=(x.shape[0], x.shape[2]))
        # m = m.permute(0, 2, 1)

        # Apply mask.
        x = x * m

        # Post processing.
        if self.append:
            x = torch.cat((x, m.repeat(1, 1, x.shape[2])), dim=1)

        if return_mask:
            return x, m
        else:
            return x


class ConcreteMaskConv2d(nn.Module):
    '''
    Input layer that selects channels for Conv2ds by learning a k-hot mask.

    Input is size (N, C_in, H_in, W_in).

    Args:
      input_size: number of inputs.
      k: number of features to be selected.
      temperature: temperature for Concrete samples.
      append: whether to append the mask to the input on forward pass.
    '''
    def forward(self, x, return_mask=False):
        # Sample mask.
        m = self.sample(sample_shape=(x.shape[0], 1, 1))
        m = m.permute(0, 3, 1, 2)

        # One sample per timepoint in each example. Problem: might want to
        # sample from different inputs periodically.
        # m = self.sample(sample_shape=(x.shape[0], x.shape[2], x.shape[3]))
        # m = m.permute(0, 3, 1, 2)

        # Apply mask.
        x = x * m

        # Post processing.
        if self.append:
            x = torch.cat((x, m.repeat(1, 1, x.shape[2], x.shape[3])), dim=1)

        if return_mask:
            return x, m
        else:
            return x


class ConcreteMaskRNN(ConcreteMask):
    '''
    Input layer that selects features for RNNs by learning a k-hot mask.

    Input is size (L_in, N, input_size).

    Args:
      input_size: number of inputs.
      k: number of features to be selected.
      temperature: temperature for Concrete samples.
      append: whether to append the mask to the input on forward pass.
    '''
    def forward(self, x, return_mask=False):
        # Sample mask.
        m = self.sample(sample_shape=(1, x.shape[1]))

        # One sample per timepoint in each example. Problem: with RNN, might
        # want to sample from different inputs periodically.
        # m = self.sample(sample_shape=(x.shape[0], x.shape[1]))

        # Apply mask.
        x = x * m

        # Post processing.
        if self.append:
            x = torch.cat((x, m.repeat(x.shape[0], 1, 1)), dim=-1)

        if return_mask:
            return x, m
        else:
            return x
