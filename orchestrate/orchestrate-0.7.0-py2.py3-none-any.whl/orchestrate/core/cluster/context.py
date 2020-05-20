import six

from orchestrate.core.cluster.errors import PleaseDisconnectError


class DisconnectOnException(object):
  def __init__(self, cluster_name, services):
    self._cluster_name = cluster_name
    self._services = services

  def __enter__(self):
    pass

  def __exit__(self, t, exc, tb):
    if exc is not None:
      try:
        self._services.cluster_service.disconnect(cluster_name=self._cluster_name, disconnect_all=False)
        return False
      except Exception as disconnect_exception:
        # NOTE(patrick): Preserve as much of the stack trace as we can.
        # Ideally we would conclude with the "Please disconnect" message, but in Python 2
        # that is arduous to do without losing the stack trace.
        # So, prefer to show a useful stack trace, but if we have the ability to chain exceptions,
        # then we can conclude with the PleaseDisconnectError
        if six.PY3:
          try:
            six.raise_from(disconnect_exception, exc)
          except Exception as chained_raise:
            six.raise_from(PleaseDisconnectError(self._cluster_name), chained_raise)
        raise
