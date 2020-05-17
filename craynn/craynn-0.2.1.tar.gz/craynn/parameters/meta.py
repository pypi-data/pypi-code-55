import tensorflow as tf
from craygraph import bind, get_nodes, Node

from .parameter_utils import combine_properties

__all__ = [
  'Parameter', 'ParameterModel',

  'ConstantParameter', 'constant_parameter',
  'FreeParameter', 'free_parameter', 'as_free_parameter',

  'UnboundParameter', 'unbound_parameter',
  'BoundParameter', 'bound_parameter',

  'parameter_model',

  'check_properties',
  'get_parameters', 'get_all_parameters',
  'get_variables', 'get_all_variables',

  'ParameterCloneMachine', 'shared_parameter'
]

class Parameter(Node):
  def __init__(self, *incoming, variables=(), shape=(), properties=None, name=None):
    self._shape = shape

    if properties is None:
      self._properties = dict()
    else:
      self._properties = properties

    self._variables = variables
  
    super(Parameter, self).__init__(*incoming, name=name)

  def properties(self, item=None):
    if item is None:
      return self._properties
    else:
      return self._properties.get(item, False)

  def get_output_for(self, *incoming, **modes):
    raise NotImplementedError()

  def __call__(self, **modes):
    from ..layers import get_output

    incoming = get_output(self.incoming())
    return self.get_output_for(*incoming, **modes)

  def get_output_shape_for(self, *input_shapes):
    return self._shape

  def shape(self):
    return self._shape

  def variables(self):
    """
    Returns variables held by the parameter. A variable is held by a parameter if it is owned by the parmeter.
    Must not include variables of the dependencies.

    A variable shared between multiple parameters must be owned by only one of the parameters.
    See `shared`

    :return: list of `tf.Variable`
    """
    return self._variables

  def reset(self):
    for param in self.incoming():
      getattr(param, 'reset', lambda: None)()

  def __str__(self):
    name = self.__class__.__name__ if self._name is None else self._name
    shape = 'x'.join([ '%d' % (s, ) for s in self.shape() ])
    props = [('shape', shape)] + list(self._properties.items())

    return '%s (%s)' % (
      name,
      ', '.join([ '%s=%s' % (k, v) for k, v in props ])
    )

  def __repr__(self):
    return str(self)


class ConstantParameter(Parameter):
  def __init__(self, value, properties=None, name=None):
    dtype = tf.dtypes.as_dtype(getattr(value, 'dtype', tf.float32))
    self._value = tf.convert_to_tensor(value, dtype=dtype, name=name)

    super(ConstantParameter, self).__init__(shape=value.shape, properties=properties, name=name)

  def __call__(self):
    return self._value

  def get_output_for(self,):
    return self._value

  def reset(self):
    pass


def constant_parameter(value, dtype=tf.float32, name=None, **properties):
  def constructor(shape, **additional_properties):
    import numpy as np

    try:
      dtype_ = dtype.as_numpy_dtype
    except AttributeError:
      dtype_ = dtype

    if not isinstance(value, np.ndarray):
      v = np.array(value, dtype=dtype_)
    else:
      v = value

    v = np.broadcast_to(v, shape)
    props = combine_properties(properties, additional_properties)

    return ConstantParameter(v, properties=props, name=name)

  return constructor


class FreeParameter(Parameter):
  ### everything for pickle
  def __init__(self, initializer, initializer_arguments, properties=None, name=None):
    properties = dict() if properties is None else properties


    self._initializer = initializer
    self._initializer_arguments = initializer_arguments

    self.initial = initializer(**initializer_arguments)
    self._value = tf.Variable(
      initial_value=self.initial,
      name=name,
      dtype=self.initial.dtype,
      trainable=properties.get('trainable', False)
    )

    super(FreeParameter, self).__init__(
      shape=initializer_arguments['shape'],
      properties=properties,
      name=name,
      variables=(self._value, )
    )

  def get_output_for(self):
    return self._value

  def reset(self):
    return self._value.assign(
      self._initializer(**self._initializer_arguments)
    )

free_parameter = FreeParameter


class ParameterModel(object):
  def __init__(self, user_defined_properties, external_name=None):
    self._user_defined_properties = user_defined_properties
    self._external_name = external_name

  def user_defined_properties(self):
    return self._user_defined_properties

  def __call__(self, shape, name=None, **additional_properties):
    raise NotImplementedError

def _parameter_model(clazz, f, default_properties=None):
  from inspect import signature, Signature, Parameter as FParameter

  default_properties = dict() if default_properties is None else default_properties

  original_signature = signature(clazz)

  assert any(
    param.name == 'shape'
    for param in original_signature.parameters.values()
  ), 'Decorated function or class must have a "shape" argument.'

  accepted_kwargs = tuple(
    p
    for p in original_signature.parameters
  )

  def __init__(self, name=None, **kwargs):
    user_defined_properties = dict([
      (k, v) for k, v in kwargs.items()
      if k not in accepted_kwargs
    ])

    self.constructor_kwargs = dict([
      (k, v) for k, v in kwargs.items()
      if k in accepted_kwargs
    ])

    ParameterModel.__init__(self, user_defined_properties, external_name=name)

  new_signature = Signature(
    parameters=[
       FParameter('self', kind=FParameter.POSITIONAL_ONLY)
     ] + [
      param
      for param in original_signature.parameters.values()
      if param.name != 'shape'
     ] + (
      []
      if 'name' in accepted_kwargs else
      [FParameter('name', kind=FParameter.POSITIONAL_OR_KEYWORD, default=None, annotation=str)]
    ),
    return_annotation=original_signature.return_annotation
  )

  __init__.__signature__ = new_signature
  __init__.__doc__ = clazz.__doc__

  def __call__(self, shape, name=None, **additional_properties):
    if self._external_name is not None:
      name = self._external_name

    constructor_kwargs = self.constructor_kwargs.copy()

    if 'name' in accepted_kwargs:
      constructor_kwargs['name'] = name

    properties = combine_properties(additional_properties, default_properties)
    properties = combine_properties(self._user_defined_properties, properties)

    constructor_kwargs['shape'] = shape
    constructor_kwargs['properties'] = properties

    return f(constructor_kwargs)

  return type(
    clazz.__name__,
    (ParameterModel,),
    dict(
      __init__=__init__,
      __call__=__call__
    )
  )

def parameter_model(clazz, **default_properties):
  from inspect import signature, Parameter as FParameter
  original_signature = signature(clazz)

  assert any([
    param.name == 'properties' and param.name != FParameter.VAR_KEYWORD
    for param in original_signature.parameters.values()
  ]), 'Decorated function or class must have a non-variable argument "properties".'

  assert not any([
    param.kind == FParameter.VAR_KEYWORD
    for param in original_signature.parameters.values()
  ]), 'Decorated function can not have variable keyword arguments as they are translated to properties.'

  def constructor(arguments):
    clazz_args, clazz_kwargs = bind(original_signature, arguments)
    return clazz(*clazz_args, **clazz_kwargs)

  return _parameter_model(clazz, constructor, default_properties=default_properties)

def as_free_parameter(f, name=None, **default_properties):
  if name is None:
    clazz_name = '%s_init' % (
      f.__name__[1:]
      if f.__name__.startswith('_') else
      f.__name__
    )
  else:
    clazz_name = name

  clazz = type(clazz_name, (FreeParameter, ), dict())

  def constructor(arguments):
    properties = arguments.pop('properties')
    parameter_name = arguments.pop('name')

    return clazz(
      initializer=f, initializer_arguments=arguments,
      name=parameter_name, properties=properties
    )

  return _parameter_model(f, constructor, default_properties=default_properties)

class UnboundParameter(Parameter):
  def __init__(self, shape, dtype='float32', properties=None, name=None):
    super(UnboundParameter, self).__init__(shape, properties, name)
    self.dtype = dtype

  def get_output_for(self, ):
    raise NotImplementedError('Unbound parameters are meant to be substituted.')

  def __str__(self):
    return '%s: %s' % (
      self.__class__.__name__ if self.name is None else self.name,
      str(self._shape)
    )

unbound_parameter = parameter_model(UnboundParameter, unbound=True)

class BoundParameter(Parameter):
  def __init__(self, incoming, shape, properties=None, name=None):
    super(BoundParameter, self).__init__(incoming, shape=shape, properties=properties, name=name)

  def get_output_for(self, incoming):
    return incoming

bound_parameter = parameter_model(BoundParameter)


def check_properties(**properties):
  effective_properties = tuple(
    (k, v)
    for k, v in properties.items()
    if v is not None
  )

  def predicate(param):
    props = getattr(param, 'properties', dict)()

    return all([
      (props.get(k, False) == v)
      for k, v in effective_properties
    ])

  return predicate

def get_all_parameters(layer, **properties):
  """
  Get parameters that satisfy all `properties`.
  A parameter satisfies a property `prop = value` if:
    - value is None;
    - the parameter has property `prop` and its value equals to `value` or
    - the parameter lacks property `prop` and `value = False`.

  Note, that `prop = None` matches all parameters, this is done to
  place commonly used properties to default arguments and enable autocomplete for them.

  :param layer: an instance of Layer, a list or a tuple of layers.
  :param properties: properties to select by.
  """
  check_props = check_properties(**properties)

  return [
    node
    for node in get_nodes(layer)
    if isinstance(node, Parameter) and check_props(node)
  ]

def get_parameters(layer, **properties):
  parameters = getattr(layer, 'parameters', tuple)()

  if len(parameters) == 0:
    return parameters
  else:
    return get_all_parameters(parameters, **properties)

def get_all_variables(layer, **properties):
  """
    Return all variables from parameters that satisfy `properties`.
    Note that variables themselves do not have properties, but parameters have.

    Note, that this function assumes empty property dict if a node does not have `properties` attribute, thus,
    layers that have variables also might be included in the output, e.g., if no filters are to apply.

    :param layer: an instance of Layer, a list or a tuple of layers.
    :param properties: properties to select parameters by.
    """
  check = check_properties(**properties)

  return tuple(
    var

    for node in get_nodes(layer)
    if check(node)

    for var in getattr(node, 'variables', tuple)()
  )

def get_variables(layer, **properties):
  return tuple(
    var
    for parameter in get_parameters(layer, **properties)
    for var in getattr(parameter, 'variables', tuple)()
  )


class ParameterCloneMachine(object):
  def __init__(self, parameter_constructor):
    self.parameter_constructor = parameter_constructor
    self.parameter = None
    self._shape = None

  def __call__(self, shape, name=None, **additional_properties):
    if self.parameter is None:
      self.parameter = self.parameter_constructor(shape, name, **additional_properties)
      self._shape = shape
      return self.parameter

    else:
      assert shape == self._shape, 'Can not clone parameter for different shape.'
      return self.parameter

shared_parameter = ParameterCloneMachine