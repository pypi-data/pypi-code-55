import tensorflow as tf
import collections

from .meta import Dataset

class VariableDataset(Dataset):
  def __init__(self, *variables, axis=0, singular=True):
    self.variables = variables

    super(VariableDataset, self).__init__(axis=axis, singular=singular)

  def _get_single(self, item):
    item = tuple(
      slice(None, None, None)
      for _ in range(self.axis)
    ) + (item, )

    return tuple(
      var[item]
      for var in self.variables
    )

  def _get_slice(self, item):
    item = tuple(
      slice(None, None, None)
      for _ in range(self.axis)
    ) + (item, )

    return tuple(
      var[item]
      for var in self.variables
    )

  def _get_sparse(self, item):
    return tuple(
      tf.gather(var, item, axis=self.axis)
      for var in self.variables
    )

  def size(self):
    return tf.shape(self.variables[0])[self.axis]

  @tf.function
  def assign(self, *data):
    return [
      var.assign(value)
      for var, value in zip(self.variables, data)
    ]

  def _data(self, batch_size=1):
    return self.variables

  def shapes(self):
    return tuple(
      var.shape
      for var in self.variables
    )

def empty_dataset(*shapes, dtypes=tf.float32, batch_axis=0, singular=True):
  assert len(shapes) > 0

  if isinstance(dtypes, str) or isinstance(dtypes, tf.dtypes.DType):
    dtypes = [dtypes for _ in shapes]

  shapes = [
    shape_or_array.shape if hasattr(shape_or_array, 'shape') else tuple(shape_or_array)
    for shape_or_array in shapes
  ]

  general_shapes = [
    shape[:batch_axis] + (None, ) + shape[(batch_axis + 1):]
    for shape in shapes
  ]

  if not isinstance(dtypes, collections.Iterable) or isinstance(dtypes, str):
    default_dtype = dtypes
    dtypes = []

    for shape_or_array in shapes:
      if hasattr(shape_or_array, 'dtype'):
        dtypes.append(shape_or_array.dtype)
      else:
        dtypes.append(default_dtype)

  variables = [
    tf.Variable(
      initial_value=tf.zeros(shape, dtype=dtype),
      dtype=dtype,
      validate_shape=False,
      shape=general_shape,
    ) for shape, general_shape, dtype in zip(shapes, general_shapes, dtypes)
  ]

  return VariableDataset(*variables, axis=batch_axis, singular=singular)

def variable_dataset(*data, batch_axis=0, singular=True):
  dataset = empty_dataset(
    *(d.shape for d in data),
    dtypes=tuple(str(d.dtype) for d in data),
    batch_axis=batch_axis,
    singular=singular
  )
  dataset.assign(*data)
  return dataset