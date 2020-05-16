from .meta import typing

__all__ = [
  'boolean',
  'interval',
  'number',
  'either',
  'choice',
]

class boolean(object):
  def __call__(self, value):
    if value == 'False' or value == 'false' or value == 'off':
      return False
    elif value == 'True' or value == 'true' or value == 'on':
      return True
    else:
      raise ValueError("Boolean flag must be either 'True', 'true', 'on', 'False', 'false' or 'off'.")

  def __str__(self):
    return 'bool'

class interval_meta(type):
  def __getitem__(self, item):
    if not isinstance(item, slice):
      raise ValueError('interval value should be a slice')

    if item.step is not None:
      raise ValueError('interval step is not supported')

    return interval(item.start, item.stop)

class interval(object, metaclass=interval_meta):
  def __init__(self, start, stop, left=True, right=False, cast=None):
    xs = (start, stop)

    if not all(
      isinstance(x, (float, int, type(None)))
      for x in xs
    ):
      raise ValueError('values of interval must be a integers, floats or None, got %s.' % (xs, ))

    self.cast = cast

    self.left = left
    self.right = right

    self.start = start
    self.stop = stop

  def get_cast(self):
    xs = (self.start, self.stop)

    if not all(
      isinstance(x, (float, int, type(None)))
      for x in xs
    ):
      raise ValueError('values of interval must be a integers, floats or None, got %s.' % (xs,))

    if self.cast is None:
      if any(isinstance(x, float) for x in xs):
        return float
      elif all(x is None for x in xs):
        return float
      else:
        return int
    else:
      return self.cast

  def __call__(self, x):
    x = self.get_cast()(x)

    if self.start is not None:
      if not (self.start <= x and self.left or self.start < x and not self.left):
        raise ValueError('value (%s) is not in the interval [%s, %s).' % (x, self.start, self.stop))

    if self.stop is not None:
      if not (x <= self.stop and self.right or x < self.stop and not self.right):
        raise ValueError('value (%s) is not in the interval [%s, %s).' % (x, self.start, self.stop))

    return x

  def __str__(self):
    if self.get_cast() == int:
      if self.start is None:
        start = '-inf'
      else:
        start = '%d' %(self.start if self.left else self.start + 1, )

      if self.stop is None:
        stop = '+inf'
      else:
        stop = '%d' % (self.stop if self.right else self.stop - 1, )

      return '%s..%s' % (start, stop)
    else:
      left = '[' if self.left else '('
      right = ']' if self.right else ')'
      start = '-inf' if self.start is None else self.start
      stop = '+inf' if self.stop is None else self.stop
      return '%s%s, %s%s' % (left, start, stop, right)

  def __lt__(self, other):
    if self.stop is not None:
      raise ValueError('Interval already has upper bound.')

    self.stop = other
    self.right = False
    return self

  def __le__(self, other):
    if self.stop is not None:
      raise ValueError('Interval already has upper bound.')

    self.stop = other
    self.right = True
    return self

  def __gt__(self, other):
    if self.start is not None:
      raise ValueError('Interval already has lower bound.')

    self.start = other
    self.left = False
    return self

  def __ge__(self, other):
    if self.start is not None:
      raise ValueError('Interval already has lower bound.')

    self.start = other
    self.left = True
    return self

  def __and__(self, other):
    if self.start is not None and other.start is not None:
      raise ValueError('Trying to combine intervals with both having lower bounds defined')

    if self.stop is not None and other.stop is not None:
      raise ValueError('Trying to combine intervals with both having upper bounds defined')

    if self.cast != other.cast and self.cast is not None and other.cast is not None:
      raise ValueError('Incompatible types: %s vs %s.' % (self.cast, other.cast))

    start = self.start if self.start is not None else other.start
    left = self.left if self.start is not None else other.left

    stop = self.stop if self.stop is not None else other.stop
    right = self.right if self.stop is not None else other.right

    cast = self.cast if self.cast is not None else other.cast

    return interval(start, stop, cast=cast, left=left, right=right)

  def __bool__(self):
    return self

class IntervalConstructor(object):
  def __lt__(self, other):
    return interval(None, other, left=False, right=False)

  def __le__(self, other):
    return interval(None, other, left=False, right=True)

  def __gt__(self, other):
    return interval(other, None, left=False, right=False)

  def __ge__(self, other):
    return interval(other, None, left=True, right=False)

number = IntervalConstructor()


class either(object, metaclass=typing):
  def __init__(self, *types):
    noncallable = [
      t
      for t in types
      if not callable(t)
    ]

    if len(noncallable) > 0:
      raise ValueError(
        'either accepts only callable objects (including types, e.g., str, int, float...), '
        'got %s.' % (noncallable, )
      )

    self.types = types

  def __call__(self, value):
    for t in self.types:
      try:
        return t(value)
      except (ValueError, TypeError):
        pass

    raise ValueError('value %s is not of any of these types: %s.' % (value, self.types))

  def __str__(self):
    return ' or ' .join(
      getattr(t, '__name__', str(t))
      for t in self.types
    )

class choice(object, metaclass=typing):
  def __init__(self, *values, cast=None):
    self.values = set(values)

    if cast is None:
      types = tuple(set(type(x) for x in values))

      if len(types) > 1:
        raise ValueError('all values must be of the same type, got %s.' % (types, ))

      self.t = types[0]
    else:
      self.t = cast

  def __call__(self, value):
    value = self.t(value)

    if value in self.values:
      return value

    raise ValueError(
      'possible choices {%s}, got %s.' % (
        ', '.join(str(x) for x in self.values),
        value
      )
    )

  def __str__(self):
    return '{%s}' % (
      ', '.join(str(x) for x in self.values),
    )


