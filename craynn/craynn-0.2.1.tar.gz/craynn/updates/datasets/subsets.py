import numpy as np
import tensorflow as tf

from .meta import Dataset
from .variable import VariableDataset

__all__ = [
  'SlicedSubset',
  'IndexedSubset'
]

class SlicedSubset(VariableDataset):
  def __init__(self, dataset : Dataset, item : slice or int):
    item = tuple(slice(None, None, None) for _ in range(dataset.axis)) + (item,)

    super(SlicedSubset, self).__init__(*[
      d[item] for d in dataset._data()
    ], axis=dataset.axis)

class IndexedSubset(Dataset):
  def __init__(self, dataset : Dataset, indx):
    self.indx = tf.convert_to_tensor(indx)
    self.dataset = dataset

    super(IndexedSubset, self).__init__(self.dataset.axis, singular=dataset._singular)

  def _get_single(self, item):
    item = tuple(slice(None, None, None) for _ in range(self.axis)) + (item,)

    return self.dataset._get_single(self.indx[item])

  def _get_slice(self, item):
    item = tuple(slice(None, None, None) for _ in range(self.axis)) + (item,)

    indx = self.indx[item]

    return self.dataset._get_sparse(indx)

  def _get_sparse(self, item):
    indx = tf.gather(self.indx, indices=item)
    return self.dataset._get_sparse(indx)

  def get_subset(self, item):
    if isinstance(item, slice):
      return IndexedSubset(self.dataset, self.indx[item])
    else:
      indx = tf.gather(self.indx, item)
      return IndexedSubset(self.dataset, indx)

  def size(self):
    return tf.shape(self.indx)[0]

  def _data(self, batch_size=1):
    return self.dataset._get_sparse(self.indx)

  def shapes(self):
    size = self.size()
    return tuple(
      shape[:self.axis] + (size,) + shape[(self.axis + 1):]
      for shape in self.dataset.shapes()
    )