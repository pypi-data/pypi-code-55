from .myModel import MyModel


class MyModelLR(MyModel):
    """ Model with LRScheduler. """

    def __init__(self, net, device=None, track=None):
        super().__init__(net, device)
        self.track = track

    def scheduler_step(self, epoch, metrics):
        if self.track and self.track != "epoch":
            # keep track of a metric
            print(metrics[self.track])
            self.scheduler.step(metrics[self.track])
        elif self.track and self.track == "epoch":
            # change based on the epoch
            self.scheduler.step(epoch)
        else:
            self.scheduler.step()
