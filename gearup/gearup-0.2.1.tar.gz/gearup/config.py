from .meta import typing

__all__ = [
  'config'
]

class config(object, metaclass=typing):
  def __init__(self, *args, **kwargs):
    self._types = {
      arg : None
      for arg in args
    }

    for k, v in kwargs.items():
      if isinstance(v, dict):
        v = config(**v)
      elif isinstance(v, (tuple, list)):
        v = config(*v)
      elif callable(v):
        pass
      elif v is None:
        pass
      else:
        raise ValueError('Type (%s) of the configuration value is not understood!' % (v, ))

      if k in self._types:
        raise ValueError('Duplication of configuration options: %s' % (k, ))

      self._types[k] = v

  def empty(self):
    return {
      k : t.empty()
      for k, t in self._types.items()
      if isinstance(t, config)
    }

  def __call__(self, arguments):
    if not isinstance(arguments, dict):
      raise ValueError('Only dictionaries are accepted, got %s.' % (arguments,))

    parsed = dict()

    for key, value in arguments.items():
      path = key.split('.', maxsplit=1)

      if len(path) == 1:
        if key in parsed:
          raise ValueError('Conflicting values for argument %s: %s vs %s.' % (key, parsed[key], value))

        parsed[key] = value
      else:
        base, rest = path[0], path[1]
        if base not in parsed:
          parsed[base] = dict()

        parsed[base][rest] = value

    for key in parsed:
      if key not in self._types:
        raise ValueError(
          '%s is not a valid configuration option (valid options: %s)' % (
            key,
            ', '.join(self._types.keys())
          )
        )

      if self._types[key] is None:
        continue

      parsed[key] = self._types[key](parsed[key])

    for k, t in self._types.items():
      if k in parsed:
        continue

      if t is None:
        continue

      raise ValueError('configuration %s is not provided.' % (k, ))

    return parsed

  def __str__(self):
    return 'config(%s)' % (
      ', '.join([
        '%s: %s' % (k, v) if v is not None else k
        for k, v in self._types.items()
      ]),
    )