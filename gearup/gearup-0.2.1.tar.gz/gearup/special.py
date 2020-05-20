from .meta import typing

__all__ = [
  'kwargs',
  'seq'
]

def parse_str_config(arguments, cast=None):
  if not isinstance(arguments, dict):
    raise ValueError('Only dictionaries are accepted, got %s.' % (arguments, ))

  result = dict()

  for key, value in arguments.items():
    path = key.split('.')
    current = result

    for k in path[:-1]:
      if k not in current:
        current[k] = dict()

      current = current[k]

    k = path[-1]
    if k in current:
      raise ValueError('Conflicting values for argument %s [%s vs %s]' % (key, value, current[k]))
    else:
      if cast is not None:
        current[k] = cast(value)
      else:
        current[k] = value

  return result


class kwargs(object, metaclass=typing):
  def __call__(self, arguments):
    return parse_str_config(arguments)

  def __str__(self):
    return '**kwargs'