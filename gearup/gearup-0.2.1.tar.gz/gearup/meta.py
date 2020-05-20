import inspect

from .utils import indent_second

__all__ = [
  'typing',
  'gearup',
  'apply'
]

def get_types(signature):
  from .special import kwargs

  types = dict()

  for k in signature.parameters:
    parameter = signature.parameters[k]
    annotation = parameter.annotation

    if annotation == inspect.Parameter.empty:
      if parameter.default == inspect.Parameter.empty:
        annotation = None

      elif parameter.default is None:
        annotation = None

      else:
        annotation = type(parameter.default)

    if not callable(annotation) and annotation is not None:
      raise ValueError('Annotation %s is not understood, must be absent or a callable.' % (annotation,))

    elif annotation is None and parameter.kind == inspect.Parameter.VAR_KEYWORD:
      types[k] = kwargs()

    elif annotation is None:
      types[k] = None

    elif annotation == bool:
      from .common import boolean
      types[k] = boolean()

    else:
      types[k] = annotation

  return types

def bind(signature, types, *args, **kwargs):
  bound = signature.bind(*args, **kwargs)

  ### applying defaults for *args and **kwargs
  ### as they always have implicit defaults
  ### and their presence is required for functionality of config.
  var_keyword = [
    p for p in signature.parameters
    if signature.parameters[p].kind == inspect.Parameter.VAR_POSITIONAL
  ]

  for p in var_keyword:
    if p not in bound.arguments:
      bound.arguments[p] = tuple()

  var_keyword = [
    p for p in signature.parameters
    if signature.parameters[p].kind == inspect.Parameter.VAR_KEYWORD
  ]

  for p in var_keyword:
    if p not in bound.arguments:
      bound.arguments[p] = dict()

  for arg in bound.arguments:
    cast = types.get(arg, None)
    value = bound.arguments[arg]

    if cast is None:
      pass

    elif type(arg) != str:
      ### already converted
      continue

    else:
      try:
        bound.arguments[arg] = cast(value)
      except (ValueError, TypeError) as e:
        raise e

  bound.apply_defaults()
  return bound.args, bound.kwargs


def apply(f, *args, **kwargs):
  if callable(f):
    signature = inspect.signature(f)
  else:
    signature = f

  types = get_types(signature)
  args, kwargs = bind(signature, types, *args, **kwargs)
  return f(*args, **kwargs)


class cli_function(object):
  def __init__(self, f):
    self._f = f
    self._signature = inspect.signature(f)
    self._types = get_types(self._signature)

  def signature(self):
    if self._signature.return_annotation == inspect.Parameter.empty:
      return_annotation = ''
    else:
      _return = self._signature.return_annotation
      return_annotation = ' -> %s' % (getattr(_return, '__name__', str(_return)), )

    types = list()
    for k, v in self._types.items():
      if v is None:
        types.append(k)
      else:
        types.append(
          '%s: %s' % (k, getattr(v, '__name__', str(v)))
        )

    return '(%s)%s' % (', '.join(types), return_annotation)

  def help(self):
    doc = getattr(self._f, '__doc__', None)
    doc = '%s\n' % (doc, ) if doc is not None else ''

    return '%s%s' % (doc, self.signature())

  def short_help(self):
    doc = getattr(self._f, '__doc__', None)
    if doc is None:
      return self.signature()
    else:
      lines = [
        line
        for line in doc.split('\n')
        if len(line) > 0
      ]

      if len(lines) > 0:
        return '%s %s' % (self.signature(), lines[0])
      else:
        return self.signature()


  def __call__(self, arguments=None):
    if arguments is None:
      import sys
      arguments = sys.argv[1:]

    if len(arguments) == 1:
      if arguments[0] == '--help' or arguments[0] == '-h':
        print(self.help())
        return

    args = list()
    kwargs = dict()

    for arg in arguments:
      if '=' in arg:
        key, value = arg.split('=', 1)
        kwargs[key] = value
      else:
        args.append(arg)

    args, kwargs = bind(self._signature, self._types, *args, **kwargs)
    return self._f(*args, **kwargs)

class cli_commands(object):
  def __init__(self, commands):
    self._commands = commands

  def signature(self):
    return '\n'.join(
      '%s -> %s' % (k, indent_second(v.short_help(), len(k) + 4))
      for k, v in self._commands.items()
    )

  def help(self):
    return '%s:\n%s' % (
      'Available commands',
      self.signature()
    )

  def short_help(self):
    return self.signature()

  def __call__(self, arguments=None):
    if arguments is None:
      import sys
      arguments = sys.argv[1:]

    if len(arguments) == 0:
      raise ValueError('please, specify command. %s' % (self.help(), ))

    if len(arguments) == 1:
      if arguments[0] == '--help' or arguments[0] == '-h':
        print(self.help())
        return

    command = arguments[0]
    if command not in self._commands:
      raise ValueError('invalid command %s. %s' % (command, self.help(), ))

    return self._commands[command](arguments[1:])

def gearup(*args, **kwargs):
  if len(kwargs) == 0 and len(args) == 0:
    return lambda *args, **kwargs: None

  if len(kwargs) == 0 and len(args) == 1:
    return cli_function(args[0])

  commands = dict()

  for arg in args:
    if hasattr(arg, '__name__') and callable(arg):
      name = arg.__name__
      if name in commands:
        raise ValueError('duplicated command names (%s)' % (name, ))
      else:
        commands[name] = cli_function(arg)

    else:
      raise ValueError('non-keyword arguments must be callables and have `__name__` attribute (like all functions).')

  for k, v in kwargs.items():
    if k in commands:
      raise ValueError('duplicated command names (%s)' % (k, ))

    if isinstance(v, (list, tuple)):
      commands[k] = gearup(*v)
    elif isinstance(v, (dict, )):
      commands[k] = gearup(**v)
    elif callable(v):
      commands[k] = cli_function(v)
    else:
      raise ValueError('command (%s) is not understood, must be either a callable, a tuple/list or a dict.')


  return cli_commands(commands)


class typing(type):
  def __getitem__(cls, item):
    if isinstance(item, tuple):
      return cls(*item)
    else:
      return cls(item)