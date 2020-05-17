from inspect import signature, Signature, Parameter
from .meta import NodeModel

__all__ = [
  'derive', 'model_from',

  'carry', 'bind',
  'CarringExpression',
]

def get_var_arguments(sign : Signature):
  var_arguments = [
    name for name, param in sign.parameters.items()
    if param.kind == Parameter.VAR_POSITIONAL
  ]

  if len(var_arguments) == 0:
    return None
  else:
    return var_arguments[0]

def bind(sign : Signature, kwargs):
  positionals = list()
  keywords = dict()

  positional = True

  for k, p in sign.parameters.items():
    if k not in kwargs:
      positional = False
      continue

    v = kwargs.pop(k)

    if positional and (p.kind == Parameter.POSITIONAL_ONLY or p.kind == Parameter.POSITIONAL_OR_KEYWORD):
      positionals.append(v)

    elif p.kind == Parameter.VAR_POSITIONAL:
      positionals.extend(v)

    elif p.kind == Parameter.VAR_KEYWORD:
      keywords.update(v)
      positional = False

    else:
      keywords[k] = v
      positional = False

  for k, v in kwargs.items():
    keywords[k] = v

  return positionals, keywords

class From(object):
  def __init__(self, what, base_class):
    self.what = what
    self.base_class = base_class
    self._defaults = dict()

  def with_defaults(self, **kwargs):
    self._defaults.update(kwargs)

  def with_fixed(self, **kwargs):
    return _derive_from(self.what, self.base_class, kwargs, self._defaults)

class Deriver(object):
  def __init__(self, what):
    self.what = what

  def based_on(self, base_class):
    return From(self.what, base_class)

derive = Deriver

def _derive_from(name, base_class, fixed, defaults):
  common = set(fixed.keys()) & set(defaults.keys())
  if len(common) > 0:
    raise ValueError('can not fix value and set default value of the same parameter [%s]' % (', '.join(common)))

  original_signature = signature(base_class.__init__)
  new_parameters = list()
  for pname, param in original_signature.parameters.items():
    if pname in fixed:
      continue

    if pname in defaults:
      param = param.replace(default=defaults[pname])

    new_parameters.append(param)

  new_signature = Signature(
    new_parameters,
    return_annotation=original_signature.return_annotation
  )

  def new_init(self, *args, **kwargs):
    arguments = new_signature.bind(self, *args, **kwargs)
    arguments.apply_defaults()

    updated_kwargs = arguments.arguments.copy()
    updated_kwargs.update(fixed)

    args, kwargs = bind(original_signature, updated_kwargs)

    base_class.__init__(*args, **kwargs)


  new_init.__signature__ = new_signature

  return type(name, (base_class, ), {
    '__init__' : new_init
  })

def carry(original, fixed, defaults, carried, base_constructor_class=NodeModel, inject_model=None):
  original_signature = signature(original)
  original_parameters = list(original_signature.parameters.values())

  assert all(c in original_signature.parameters for c in carried)

  has_kwargs = any(p.kind == Parameter.VAR_KEYWORD for p in original_signature.parameters.values())

  if not has_kwargs and inject_model is not None:
    if inject_model not in original_signature.parameters:
      raise Exception('There is no arguments for model injection!')

  existing_defaults = {
    k : v
    for k, v in defaults.items()
    if k in original_signature.parameters
  }

  kwargs_defaults = {
    k : v
    for k, v in defaults.items()
    if k not in original_signature.parameters
  }

  if len(kwargs_defaults) > 0 and not has_kwargs:
    bad_args = ','.join([str(k) for k in kwargs_defaults])
    raise Exception(
      'Attempting to provide default value for arguments ({bad_args}) not present in function signature. '
      'Consider adding {bad_args} to function arguments or adding **kwargs.'.format(
        bad_args=bad_args
      )
    )

  constructor_parameters = list()

  ### last argument might be **kwargs
  if len(original_parameters) > 0 and original_parameters[-1].kind != Parameter.VAR_KEYWORD:
    non_kwargs_original = original_parameters
  else:
    non_kwargs_original = original_parameters[:-1]

  for p in non_kwargs_original:
    if p.name in carried:
      continue

    elif p.name in fixed:
      continue

    elif p.name == inject_model:
      continue

    elif p.name in existing_defaults:
      constructor_parameters.append(
        p.replace(default=existing_defaults[p.name])
      )
    else:
      constructor_parameters.append(p)

  for k, v in kwargs_defaults.items():
    constructor_parameters.append(
      Parameter(name=k, kind=Parameter.KEYWORD_ONLY, default=v)
    )

  if len(original_parameters) > 0 and original_parameters[-1].kind == Parameter.VAR_KEYWORD:
    constructor_parameters.append(original_parameters[-1])

  if original_signature.return_annotation == Parameter.empty:
    constructor_return = Parameter.empty
  else:
    constructor_return = '(%s) -> %s' % (
      ', '.join(carried),
      original_signature.return_annotation
    )

  var_positional = False
  pretty_constructor_parameters = list()
  for p in constructor_parameters:
    if var_positional:
      new_p = p
    elif p.kind == Parameter.VAR_POSITIONAL:
      var_positional = True
      new_p = p
    elif p.kind == Parameter.KEYWORD_ONLY:
      new_p = p.replace(kind=Parameter.POSITIONAL_OR_KEYWORD)
    else:
      new_p = p

    pretty_constructor_parameters.append(new_p)


  constructor_signature = Signature(
    parameters=pretty_constructor_parameters,
    return_annotation=constructor_return
  )

  apparent_constructor_signature = Signature(
    parameters=[Parameter('self', Parameter.POSITIONAL_ONLY)] + pretty_constructor_parameters,
    return_annotation=constructor_return
  )

  model_signature = Signature(
    parameters=[
      original_signature.parameters[p]
      for p in original_signature.parameters
      if p in carried
    ],
    return_annotation=original_signature.return_annotation
  )

  apparent_model_signature = Signature(
    parameters=[Parameter('self', Parameter.POSITIONAL_ONLY)] + [
      original_signature.parameters[p]
      for p in original_signature.parameters
      if p in carried
    ],
    return_annotation=original_signature.return_annotation
  )

  def __init__(self, *args, **kwargs):
    self.constructor_arguments = constructor_signature.bind(*args, **kwargs)
    self.constructor_arguments.apply_defaults()
    self.fixed_arguments = fixed
    self.original = original

    base_constructor_class.__init__(self)

  __init__.__signature__ = apparent_constructor_signature

  def __call__(self, *args, **kwargs):
    model_arguments = model_signature.bind(*args, **kwargs)
    model_arguments.apply_defaults()

    params = model_arguments.arguments.copy()

    params.update(self.constructor_arguments.arguments)
    params.update(self.fixed_arguments)

    if inject_model is not None:
      if inject_model in params:
        raise Exception('Argument for model injection (%s) is already specified!' % (inject_model, ))

      params[inject_model] = self

    args, kwargs = bind(original_signature, params)
    return self.original(*args, **kwargs)

  __call__.__signature__ = apparent_model_signature

  def __str__(self, ):
    name = getattr(original, '__name__', 'Model')
    return '%s(%s) -> (%s) -> %s' % (
      name,
      ', '.join('%s=%s' % (k, v) for k, v in self.fixed_arguments.items()),
      constructor_signature,
      model_signature
    )

  original_name = getattr(original, '__name__', 'node')
  if len(original_name) == 0:
    clazz_name = 'NodeModel'
  else:
    clazz_name = '%s%sModel' % (original_name[0].upper(), original_name[1:])


  model_clazz = type(
    clazz_name,
    (base_constructor_class, ),
    dict(
      __init__=__init__,
      __str__=__str__,
      __call__=__call__,
    )
  )

  return model_clazz

class CarringExpression(object):
  """
  Allows nice syntax for `carry` method:
  carry(<function>, ['param1', 'param2']).with_fixed(param1=value1).with_defaults(param3=value3)()
  """
  def __init__(self, original, fixed=None, defaults=None, carried=None, base_constructor_class=NodeModel):
    self.original = original

    self.fixed = dict() if fixed is None else fixed
    self.defaults = dict() if defaults is None else defaults
    self.carried = dict() if carried is None else carried
    self.base_constructor_class = base_constructor_class

  def __call__(self, inject_model=None):
    return carry(
      self.original,
      self.fixed, self.defaults, self.carried,
      base_constructor_class=self.base_constructor_class,
      inject_model=inject_model
    )

  def with_defaults(self, **kwargs):
    self.defaults.update(kwargs)
    return self

  def with_fixed(self, **kwargs):
    self.fixed.update(kwargs)
    return self

def model_from(clazz, carried=('incoming', ), base_constructor_class=NodeModel):
  return CarringExpression(clazz, carried=carried, base_constructor_class=base_constructor_class)