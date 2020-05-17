import tensorflow as tf

__all__ = [
  'sliced_seq',
  'xmap'
]

def sliced_seq(size, batch_size=None):
  if batch_size is not None:
    n_batches = size // batch_size + (1 if size % batch_size != 0 else 0)

    for i in range(n_batches):
      yield slice(i * batch_size, min((i + 1) * batch_size, size))
  else:
    for s in range(size):
      yield s

def xmap(f, indexed_seq, axis=0):
  results = None
  singular = False

  for _, batch in indexed_seq:
    batch_results = f(*batch)

    if not isinstance(batch_results, (tuple, list)):
      batch_results = (batch_results, )
      singular = True

    if results is None:
      results = tuple([] for _ in batch_results)

    for r, br in zip(results, batch_results):
      r.append(br)

  results = tuple(
    tf.concat(r, axis=axis)
    for r in results
  )

  if len(results) == 1 and singular:
    return results[0]
  else:
    return results
