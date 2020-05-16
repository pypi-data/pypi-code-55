from torch.optim.lr_scheduler import _LRScheduler
import math


class LinearCosine(_LRScheduler):
    def __init__(self, optimizer, T_lin, T_max, eta_min=0, last_epoch=-1):
        self.T_lin = T_lin
        self.T_max = T_max
        self.eta_min = eta_min
        super().__init__(optimizer, last_epoch)

    def get_lr(self):
        if self.last_epoch < self.T_lin:
            return [self.eta_min + (base_lr - self.eta_min)*self.last_epoch / self.T_lin
                    for base_lr, group in
                    zip(self.base_lrs, self.optimizer.param_groups)]
        return [(1 + math.cos(math.pi * (self.last_epoch-self.T_lin+1) / (self.T_max-self.T_lin+1))) /
                (1 + math.cos(math.pi * ((self.last_epoch-self.T_lin+1) - 1) / (self.T_max-self.T_lin+1))) *
                (group['lr'] - self.eta_min) + self.eta_min
                for group in self.optimizer.param_groups]
