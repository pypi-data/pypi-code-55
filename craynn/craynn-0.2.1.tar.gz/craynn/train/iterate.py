import numpy as np

__all__ = [
  'iterate'
]

def make_buffer(step_results, batch_dim):
  shapes = [
    getattr(res, 'shape', tuple())
    for res in step_results
  ]
  return [
    np.zeros(shape=batch_dim + shape)
    for shape in shapes
  ]

def iterate(step, n_iterations, n_epoches=None, progress=None):
  ### not proud, but each microsecond counts
  assert n_iterations > 0

  if n_epoches is None:
    if progress is not None:
      pbar = progress(total=n_iterations)
      pbar_inc = pbar.update
      pbar_close = pbar.close
    else:
      pbar_inc = lambda: None
      pbar_close = lambda: None

    step_results = step()
    pbar_inc()

    if isinstance(step_results, tuple):
      results = make_buffer(step_results, (n_iterations, ))
      n_results = len(results)

      for k in range(n_results):
        results[k][0] = step_results[k]

      for j in range(1, n_iterations):
        step_results = step()
        pbar_inc()

        for k in range(n_results):
          results[k][j] = step_results[k]

      pbar_close()
      return results
    else:
      results, = make_buffer((step_results, ), (n_iterations,))
      results[0] = step_results

      for j in range(1, n_iterations):
        results[j] = step()
        pbar_inc()

      pbar_close()
      return results
  else:
    assert n_epoches > 0

    if progress is not None:
      pbar = progress(total=n_epoches)
      pbar_inc = pbar.update
      pbar_close = pbar.close

      pbar_secondary = progress(total=n_iterations, leave=False)
      pbar_inc_secondary = pbar_secondary.update
      pbar_close_secondary = pbar_secondary.close
      pbar_reset_secondary = pbar_secondary.reset
    else:
      pbar_inc = lambda : None
      pbar_close = lambda : None
      pbar_inc_secondary = lambda : None
      pbar_close_secondary = lambda : None
      pbar_reset_secondary = lambda : None

    step_results = step()
    pbar_inc_secondary()

    if isinstance(step_results, tuple):
      results = make_buffer(step_results, (n_epoches, n_iterations))
      n_results = len(results)

      for k in range(n_results):
        results[k][0, 0] = step_results[k]

      for j in range(1, n_iterations):
        step_results = step()
        pbar_inc_secondary()
        for k in range(n_results):
          results[k][0, j] = step_results[k]
      pbar_inc()

      for i in range(1, n_epoches):
        pbar_reset_secondary()
        for j in range(n_iterations):
          step_results = step()
          pbar_inc_secondary()
          for k in range(n_results):
            results[k][i, j] = step_results[k]
        pbar_inc()

      pbar_close_secondary()
      pbar_close()
      return results
    else:
      results, = make_buffer((step_results,), (n_epoches, n_iterations))
      results[0, 0] = step_results

      pbar_reset_secondary()
      for j in range(1, n_iterations):
        results[0, j] = step()
        pbar_inc_secondary()
      pbar_inc()

      for i in range(1, n_epoches):
        pbar_reset_secondary()
        for j in range(n_iterations):
          results[i, j] = step()
          pbar_inc_secondary()
        pbar_inc()

      pbar_close_secondary()
      pbar_close()
      return results