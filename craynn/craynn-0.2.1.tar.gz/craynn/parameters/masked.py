import tensorflow as tf

from .common import glorot_normal_init
from .meta import Parameter, parameter_model

__all__ = [
  'MaskedParameter', 'masked'
]

class MaskedParameter(Parameter):
  def __init__(self, shape, mask, w=glorot_normal_init(), properties=None, name=None):
    self.w = w(
      shape=shape,
      **properties,
      name=(name + '_w') if name is not None else None
    )

    self.mask = mask(
      shape=shape,
      mask=True,
      **properties,
      name=(name + '_mask') if name is not None else None
    )

    super(MaskedParameter, self).__init__(
      self.w, self.mask,
      shape=shape,
      properties=properties,
      name=name
    )

  def get_output_for(self, w, mask):
    return w * mask

  def get_output_shape_for(self, w_shape, mask_shape):
    assert w_shape == mask_shape
    return w_shape

masked = parameter_model(MaskedParameter)