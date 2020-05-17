__all__ = [
  'achain',
]

def flatten(l):
  if isinstance(l, list):
    return [ flatten(x) for x in l ]
  else:
    return l

def achain(incoming, definition, apply=None):
  if apply is None:
    apply = lambda f, *args, **kwargs: f(*args, **kwargs)

  graph = incoming

  if not isinstance(graph, (tuple, list)):
    graph = [graph]

  if not hasattr(definition, '__iter__'):
    try:
      graph = apply(definition, *graph)
    except Exception as e:
      raise Exception('An error occurred while try to apply %s to %s' % (definition, graph)) from e

  elif isinstance(definition, list):
    results = []
    for op in definition:
      try:
        result = achain(graph, op, apply=apply)
      except Exception as e:
        raise Exception('An error occurred while try to apply %s to %s' % (op, graph)) from e

      if isinstance(result, (tuple, list)):
        results.extend(result)
      else:
        results.append(result)

    graph = results

  elif isinstance(definition, tuple):
    for op in definition:
      try:
        graph = achain(graph, op, apply=apply)
      except Exception as e:
        raise Exception('An error occurred while try to apply %s to %s' % (op, graph)) from e

  else:
    raise ValueError('Unknown chain definition: %s' % (definition, ))

  return graph