import sys
import json
import time
import queue
import random  # @UnusedImport
import traceback
import urllib.request
import logging.config
import logging.handlers


__all__ = 'QueueProxyHandler', 'BatchJsonHandler'


class QueueProxyHandler(logging.handlers.QueueHandler):
  '''
  Queue handler which creates its own ``QueueListener`` to
  proxy log records via provided ``queue`` to ``target`` handler.
  '''

  _listener = None
  '''Queue listener.'''

  _prefix = None
  '''Global logger name prefix.'''

  _closeJoinTimeout = None
  '''Timeout to join the queue before closing target handler.'''


  def __init__(
      self, queue, target = logging.handlers.HTTPHandler, prefix = '',
      closeJoinTimeout = 30, **kwargs):

    self._prefix = prefix
    self._closeJoinTimeout = closeJoinTimeout

    # user-supplied factory is not converted by default
    if isinstance(queue, logging.config.ConvertingDict):
      queue = queue.configurator.configure_custom(queue)

    super().__init__(queue)
    self._listener = logging.handlers.QueueListener(queue, target(**kwargs))
    self._listener.start()

  def close(self):
    '''
    Call ``logging.Handler.close``, stop the listener thread and explicitly
    close the queue listener's target handler (in case they are buffering).

    ``logging.handlers.QueueListener.stop`` tries to enqueue the poison pill
    which will fail if the queue is full. In such case this method will try
    to read one record from the queue and handle it with
    ``logging.Handler.handleError`` and then try to stop again.
    '''

    # This just removes the handler from global handler list
    super().close()

    markdone = getattr(self.queue, 'task_done', str)
    while True:
      try:
        self._listener.stop()
      except queue.Full:
        try:
          record = self.queue.get_nowait()
        except queue.Empty:
          break
        else:
          self.handleError(record)
          markdone()
      else:
        # QueueListener does not call "task_done" for the poison pill.
        markdone()
        break

    # Queue.join does not support timeout
    finish = time.time() + self._closeJoinTimeout
    while time.time() < finish:
      if self.queue.unfinished_tasks:
        time.sleep(0.1)
      else:
        break
    else:
      print('Timed out waiting for the queue to be consumed', file = sys.stderr)

    for h in self._listener.handlers:
      h.close()

  def prepare(self, record):
    record = super().prepare(record)
    origname = record.name

    if self._prefix:
      record.name = '{}.{}'.format(self._prefix, record.name)

    if hasattr(record, 'suffix'):
      record.name = '{}.{}'.format(record.name, record.suffix)
      del record.suffix

    if record.name != origname:
      record.origname = origname

    return record


class BatchJsonHandler(logging.handlers.BufferingHandler):
  '''
  This class is a batch processing buffering handler.

  It should provide better throughput for verbose logging
  applications.

  The record buffer flush conditions (any flushes) are:

    * buffer at the capacity
    * encountered logging record with given or higher level
    * first record in buffer is older than given timeout
    * handler closing (e.g. on application shutdown)

  Possible failure/data-loss scenarios are worth noting. Given
  that this class' instance is supposed to be used as a target for
  ``QueueProxyHandler``, thus it works in a separate thread, there
  are a few questions of what happens when:

    1. all flush request attempts failed

       The handler writes the JSON lines into ``stderr``, like
       ``logging.Handler.handleError``. The buffer is always
       cleared in ``flush``.

    2. a flush request attempt takes too long

       The queue listener is blocked and cannot read from the queue.

    3. the application logs into corresponding queue handler to fast

       The queue's ``maxsize`` should be set according to the
       application's logging patterns. When the queue is full,
       the excess record will be written by
       ``logging.Handler.handleError`` into ``stderr``.

    4. the application shuts down when the buffer is being flushed

       The application may have much delayed graceful (SIGTERM, SIGINT)
       shutdown, with the worst case of
       ``requestTimeout * attempts + max(delay) * (attempts - 1)`` per
       buffer.

    5. the application shuts down when the queue is full

       Handled by ``QueueProxyHandler.close``.

  '''

  capacity = None
  '''Capacity of the buffer. Set by the superclass.'''

  buffer = None
  '''Record buffer. Set by the superclass.'''

  flushLevel = None
  '''Flush the buffer once encounter a record with this or higher level.'''

  flushTimeout = None
  '''Flush the buffer if the first record in the buffer was created
  longer than given number of seconds (on emission of the next record).'''

  url = None
  '''URL to POST the JSON batches to.'''

  urlopener = None
  '''``urllib`` opener that combines authentication and TLS handlers.'''

  requestTimeout = None
  '''POST request timeout. 30 seconds by default.'''

  requestAttemptLimit = None
  '''POST request (re)try attempt limit. 4 by default.'''

  requestAttemptDelayFn = None
  '''POST request (re)try attempt delay function. Default function
  is an exponential back-off with jitter that saturates at 10 seconds.'''


  def __init__(
      self, capacity, host, url, *,
      flushLevel = logging.ERROR,
      flushTimeout = 60,
      credentials = None,
      secure = False,
      context = None,
      requestTimeout = 30,
      requestAttemptLimit = 4,
      requestAttemptDelayFn = lambda i: min(2 ** i * random.uniform(1, 1.5), 10)):
    super().__init__(capacity)

    self.flushLevel = logging._checkLevel(flushLevel)
    self.flushTimeout = flushTimeout

    self.url = 'http{secure}://{host}{path}'.format(
      secure = 's' if secure else '', host = host, path = url)

    self.requestTimeout = requestTimeout
    self.requestAttemptLimit = requestAttemptLimit
    self.requestAttemptDelayFn = requestAttemptDelayFn

    handlers = []
    if credentials:
      pwdmgr = urllib.request.HTTPPasswordMgrWithPriorAuth()
      pwdmgr.add_password(None, self.url, credentials[0], credentials[1])
      pwdmgr.update_authenticated(self.url, True)  # send credentials right away
      auth = urllib.request.HTTPBasicAuthHandler(pwdmgr)
      handlers.append(auth)
    if secure and context:
      https = urllib.request.HTTPSHandler(context = context)
      handlers.append(https)
    self.urlopener = urllib.request.build_opener(*handlers)

  def shouldFlush(self, record):
    return (
      len(self.buffer) >= self.capacity
      or record.levelno >= self.flushLevel
      or len(self.buffer) >= 1 and self.buffer[0].created + self.flushTimeout < time.time())

  def send(self, lines):
    request = urllib.request.Request(
      self.url, data = lines.encode(), headers = {'Content-Type': 'application/x-ndjson'})
    for i in range(self.requestAttemptLimit):
      try:
        return self.urlopener.open(request)
      except urllib.request.URLError:
        if i + 1 < self.requestAttemptLimit:
          delay = self.requestAttemptDelayFn(i)
          print('Batch-flush error, retrying in {:.2f}s'.format(delay), file = sys.stderr)
          print(traceback.format_exc(), file = sys.stderr)
          time.sleep(delay)
        else:
          raise

  def serialiseBuffer(self):
    return '\n'.join(json.dumps(r.__dict__, default = str) for r in self.buffer)

  def flush(self):
    '''
    Flush current record buffer.

    This method must not raise because it's called from
    ``logging.Handler.emit``  which handles exceptions
    via ``logging.Handler.handleError``.
    '''

    if not self.buffer:
      return

    bufferJsonLines = None
    self.acquire()
    try:
      bufferJsonLines = self.serialiseBuffer()
      self.send(bufferJsonLines)
    except Exception:
      print('Batch-flush error, flushing buffer into stderr', file = sys.stderr)
      print(traceback.format_exc(), file = sys.stderr)
      print(bufferJsonLines, file = sys.stderr)

      self.buffer.clear()
    else:
      self.buffer.clear()
    finally:
      self.release()

