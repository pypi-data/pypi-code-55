from .meta import typing

class kwargs(object, metaclass=typing):
  def __init__(self, t):
    self.t = t

  def __call__(self, value):
    if not isinstance(value, dict):
      raise ValueError('kwargs[%s] type only accepts dictionaries, got %s.' % (self.t, value))

    return {
      k : self.t(v)
      for k, v in value.items()
    }

  def __str__(self):
    return '**%s' % (getattr(self.t, '__name__', str(self.t)))

class args(object, metaclass=typing):
  def __init__(self, t):
    self.t = t

  def __call__(self, value):
    if not isinstance(value, tuple):
      raise ValueError('args[%s] type only accepts tuples, got %s.' % (self.t, value))

    return tuple(
      self.t(v)
      for v in value
    )

  def __str__(self):
    return '*%s' % (getattr(self.t, '__name__', str(self.t)))