import tensorflow as tf

from ..networks import Network
from ..objectives import Objective
from ..updates import Dataset

from .iterate import iterate

__all__ = [
  'TrainingProcedure'
]

class TrainingProcedure(object):
  def __init__(self,
   network : Network, loss : Objective, optimizer,
   dataset : Dataset, validation_dataset : Dataset = None, batch_size=4,
   metrics=(), progress=None
  ):
    self.network = network
    self.loss = loss
    self.optimizer = optimizer(
      target=loss,
      variables=network.variables(trainable=True)
    )

    self.dataset = dataset
    self.metrics = metrics

    if validation_dataset is None:
      self.validation_dataset = dataset
    else:
      self.validation_dataset = validation_dataset

    self.epoch = 0
    self.metrics = list()
    self.batch_size = batch_size
    self.iterations_per_epoch = len(self.dataset) // batch_size

    self.progress = progress

    @tf.function
    def step():
      args = self.dataset.batch(batch_size)
      X, y = args[:-1], args[-1]
      with self.optimizer:
        predictions = self.network(*X)
        if not isinstance(predictions, tuple):
          predictions = (predictions, )

        return self.optimizer.step(*predictions, y)

    self._step = step

  def reset(self):
    self.optimizer.reset()
    self.network.reset()
    self.metrics = list()

  def epoch(self):
    return iterate(self._step, self.iterations_per_epoch, progress=self.progress)