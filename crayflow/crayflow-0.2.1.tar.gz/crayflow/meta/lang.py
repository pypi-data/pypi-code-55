from craygraph import graph_lang
from craygraph import NodeModel

from .meta import Cache, CachedComputation, GenericCachedComputation, NoCache

__all__ = [
  'achain', 'repeat', 'for_each',
  'nothing', 'with_inputs', 'select', 'seek'
]

def apply(f, *args, **kwargs):
  if isinstance(f, NodeModel):
    return f(*args, **kwargs)
  elif isinstance(f, Cache):
    return GenericCachedComputation(lambda *xs: xs, *args, cache=f)
  elif isinstance(f, CachedComputation):
    return f
  elif callable(f):
    return GenericCachedComputation(f, *args, cache=NoCache())
  else:
    raise TypeError(
      '%s is not understood: '
      'must be either an instance of Cache, a callable, or an instance of NodeModel.'
    )

lang = graph_lang(apply)
achain, repeat, for_each = lang.achain, lang.repeat, lang.for_each
nothing, with_inputs, select, seek = lang.nothing, lang.with_inputs, lang.select, lang.seek