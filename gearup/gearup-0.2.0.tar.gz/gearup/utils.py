__all__ = [
  'indent',
  'indent_second'
]

def indent(string, n=2):
  tokens = string.split('\n')
  ind = ' ' * n

  return '\n'.join(
    '%s%s' % (ind, token)
    for token in tokens
  )

def indent_second(string, n=2):
  tokens = string.split('\n')
  sep = '\n%s' % (' ' * n, )

  return sep.join(tokens)