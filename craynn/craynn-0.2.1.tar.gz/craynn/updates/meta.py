import tensorflow as tf

__all__ = [
  'Stateful', 'stateful', 'as_stateful'
]

def _populate(obj, property, value):
  setattr(obj, '_' + property, value)
  setattr(obj, property, lambda : getattr(obj, '_' + property))

class Stateful(object):
  def __init__(self, state=None, updates=None, observables=None):
    self._state = state if state is not None else []
    self._updates = updates if updates is not None else tf.no_op()

    if observables is not None:
      for k, v in observables.items():
        _populate(self, k, v)

    self._observables = observables if observables is not None else dict()

    self._reset_op = tf.group([
      var.initializer
      for var in self._state
    ])

  def updates(self):
    return self._updates

  def reset(self):
    return self._reset_op

  def observables(self):
    return self._observables

stateful = Stateful

def as_stateful(f):
  import inspect

  def new_init(self, state=None, updates=None, observables=None):
    Stateful.__init__(self, state, updates, observables)

  clazz = type(f.__name__, (Stateful, ), dict(
    __init__ = new_init
  ))

  def wrapper(*args, **kwargs):
    g = f(*args, **kwargs)

    def new_g(*args, **kwargs):
      result = g(*args, **kwargs)

      if isinstance(result, Stateful):
        return result
      else:
        state, updates, observables = result
        return clazz(state, updates, observables)

    new_g.__signature__ = inspect.signature(g)

    return new_g

  wrapper.__signature__ = inspect.signature(f)
  return wrapper
