def placeholder():
    pass

p = placeholder

def _is_placeholder(val):
    return val is placeholder

class _placeholders_memo():
  def __init__(self, args):
    self.args = args
    self.len = len(tuple(v for v in args if not _is_placeholder(v)))
