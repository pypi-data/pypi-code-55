__all__ = [
  'Node',
  'NodeModel',
  
  'propagate', 'dynamic_propagate',
  'reduce_graph', 'dynamic_reduce_graph',
  'graph_reducer', 'map_graph',
  'select_subgraph',

  'get_nodes',
  'get_inputs_nodes',
  'get_incoming', 'get_name',

  'model_selector',
  'modify_graph'
]

class Node(object):
  def __init__(self, *incoming, name=None, model=None):
    self._name = name
    self._incoming = incoming
    self._model = model

  def name(self):
    return self._name

  def set_incoming(self, *incoming):
    self._incoming = incoming

  def incoming(self):
    return self._incoming

  def __str__(self):
    name = self.name()
    if name is None:
      return self.__class__.__name__
    else:
      return name

  def __repr__(self):
    return str(self)

  def model(self):
    return self._model

def get_mutator(cls):
  """
  Returns class that allows to make some parameters of the corresponding model fixed or
  defaults redefined:

      model = node_model.with_fixed(x=1).with_defaults(y=2)

  is equivalent to:

      model = lambda *args, y=2, **kwargs: node_model(*args, x=1, y=y, **kwargs)
  """

  def __init__(self, fixed=None, defaults=None):
    self._fixed = fixed if fixed is not None else dict()
    self._defaults = defaults if defaults is not None else dict()

  def with_fixed(self, **kwargs):
    self._fixed.update(kwargs)
    return self

  def with_defaults(self, **kwargs):
    self._defaults.update(kwargs)
    return self

  def __str__(self):
    fixed_str = ', '.join(
      '%s=%s' % (k, v)
      for k, v in self._fixed.items()
    )

    defaults_str = ', '.join(
      '%s->%s' % (k, v)
      for k, v in self._defaults.items()
    )
    return '%s mutator(%s, %s)' % (
      cls.__name__,
      fixed_str,
      defaults_str
    )

  def __repr__(self):
    return str(self)

  def __call__(self, *args, **kwargs):
    for k in self._fixed:
      if k in kwargs:
        raise ValueError('attempting to redefine fixed argument')
      else:
        kwargs[k] = self._fixed[k]

    for k in self._defaults:
      kwargs[k] = kwargs.get(k, self._defaults[k])

    return cls(*args, **kwargs)

  from .func import signature_with_self
  __call__.__signature__ = signature_with_self(cls)

  return type(
    '%sMutator' % (cls.__name__, ),
    (object, ),
    dict(
      __init__ = __init__,
      __call__ = __call__,
      with_fixed = with_fixed,
      with_defaults = with_defaults,
      __str__ = __str__,
      __repr__ = __repr__
    )
  )

class MetaModel(type):
  """
  Meta-class for the NodeModel.
  Upon creation of a new NodeModel, a Mutator class is derived and assigned to the newly created class.
  """
  def __new__(mcs, name, bases, dct):
    cls = super().__new__(mcs, name, bases, dct)
    cls.mutator = get_mutator(cls)

    return cls

class NodeModel(object, metaclass=MetaModel):
  """
  Base class for (*Node) -> Node callables (a.k.a. node models).
  """

  def __call__(self, *args, **kwargs):
    raise NotImplementedError()

  @classmethod
  def with_fixed(cls, **kwargs):
    return cls.mutator(fixed=kwargs)

  @classmethod
  def with_defaults(cls, **kwargs):
    return cls.mutator(defaults=kwargs)

def get_incoming(node):
  incoming = getattr(node, 'incoming', tuple)
  if callable(incoming):
    return incoming()
  else:
    return incoming

def get_name(node):
  name = getattr(node, 'name', None)

  if callable(name):
    return name()
  else:
    return name

def propagate(f, nodes, substitutes=None, incoming=get_incoming):
  """
  For each node in the graph computes:

      r(node) = f(node, [r(x) for x in incoming(node)])

  Graph is defined as `nodes` and all their dependencies.
  This function caches results `r(node)`, thus, `f`.

  NB: if substitutes are specified not all nodes might be evaluated, also not all nodes might
    be present in the result.

  :param f: operator to propagate, a function of type `(Node, List[A]) -> A`;
  :param nodes: a list of nodes, output nodes of the graph `f` is to be propagated through;
  :param substitutes: a dictionary `Node -> A`, overrides results of `r(node)`,
    None is the same as an emtpy dictionary;
  :param incoming: operator `Node -> List[Node]`, returns list of incoming nodes (dependencies);
  :return: dictionary `Node -> A`.
  """
  if substitutes is not None:
    known_results = substitutes.copy()
  else:
    known_results = dict()

  stack = list()
  stack.extend(nodes)

  while len(stack) > 0:
    current_node = stack.pop()

    if current_node in known_results:
      continue

    incoming_nodes = incoming(current_node)

    unknown_dependencies = [
      nodes
      for nodes in incoming_nodes
      if nodes not in known_results
    ]

    if len(unknown_dependencies) == 0:
      args = tuple(known_results[node] for node in incoming_nodes)
      known_results[current_node] = f(current_node, args)

    else:
      stack.append(current_node)
      stack.extend(unknown_dependencies)

  return known_results

def reduce_graph(f, nodes, substitutes=None, incoming=get_incoming):
  """
    The same as `propagate` but returns results only for `nodes`:

        r(node) = f(node, [r(x) for x in incoming(node)])

    :param f: operator to propagate, a function of type `(Node, List[A]) -> A`;
    :param nodes: a list of nodes or a node --- output nodes of the graph `f` is to be propagated through;
    :param substitutes: a dictionary `Node -> A`, overrides results of r(node),
      None is the same as an emtpy dictionary;
    :param incoming: operator `Node -> List[Node]`, returns list of incoming nodes (dependencies);
    :return: list of results (if `nodes` is a collection of nodes), or
      just result for the `nodes` (in case `nodes` is a single node)
    """

  if isinstance(nodes, (tuple, list)):
    result = propagate(f, nodes, substitutes=substitutes, incoming=incoming)
    return tuple(
      result[node]
      for node in nodes
    )

  else:
    result = propagate(f, (nodes, ), substitutes=substitutes, incoming=incoming)
    return result[nodes]


def dynamic_propagate(f, nodes, substitutes=None, incoming=None):
  """
  Similar to `propagate` but allows to dynamically compute incoming nodes and pass results of `incoming(node)` to `f`.
  For each node in the graph computes:

      r(node) = f(node, [r(x) for x in incoming_nodes], q(node))
      where:
        incoming_nodes, intermediate_result = incoming(node)

  Graph is defined as `nodes` and all their dependencies.
  This function caches results `r(node)`, thus, `f`.

  Note, that unlike `propagate`, operator `f` receives 3 arguments:
  - node;
  - incoming nodes (dependencies) that *need to be computed*;
  - value returned by `incoming`.

  This is useful for implementing cached dataflows, when dependencies depend on results of cache retrieval:

      def incoming(node):
        try:
          return list(), load_cache(node)
        except:
          return node.incoming(), None

      def operator(node, inputs, cached):
        if cached is not None:
          return cached
        else:
          <perform computations>

  NB: if substitutes are specified not all nodes might be evaluated, also not all nodes might
    be present in the result.

  :param f: operator to propagate, a function of type `(Node, List[A], B) -> A`;
  :param nodes: a list of nodes, output nodes of the graph `f` is to be propagated through;
  :param substitutes: a dictionary `Node -> A`, overrides results of `r(node)`,
    None is the same as an emtpy dictionary;
  :param incoming: operator `Node -> (List[Node], B)`, returns list of incoming nodes (dependencies)
    and some intermediate results (e.g. cached results),
    if None --- defaults to `lambda node: (get_incoming(node), None)`;
  :return: dictionary `Node -> A`.
  """
  if incoming is None:
    incoming = lambda node: (get_incoming(node), None)

  known_results = dict() if substitutes is None else dict(substitutes.items())
  graph = dict()
  intermediate_result = dict()

  stack = list()
  stack.extend(nodes)

  while len(stack) > 0:
    current_node = stack.pop()

    if current_node in known_results:
      continue

    if current_node not in graph:
      graph[current_node], intermediate_result[current_node] = incoming(current_node)

    incoming_nodes, intermediate = graph[current_node], intermediate_result[current_node]

    unknown_dependencies = [
      nodes
      for nodes in incoming_nodes
      if nodes not in known_results
    ]

    if len(unknown_dependencies) == 0:
      args = tuple(known_results[node] for node in incoming_nodes)
      known_results[current_node] = f(current_node, args, intermediate)

    else:
      intermediate_result[current_node] = intermediate
      stack.append(current_node)
      stack.extend(unknown_dependencies)

  return known_results

def dynamic_reduce_graph(f, nodes, substitutes=None, incoming=None):
  """
    The same as `reduce_graph` but for `dymanic_propagate`

        r(node) = f(node, [r(x) for x in incoming(node)])

    :param f: operator to propagate, a function of type `(Node, List[A], B) -> A`;
    :param nodes: a list of nodes, output nodes of the graph `f` is to be propagated through;
    :param substitutes: a dictionary `Node -> A`, overrides results of `r(node)`,
      None is the same as an emtpy dictionary;
    :param incoming: operator `Node -> (List[Node], B)`, returns list of incoming nodes (dependencies)
      and some intermediate results (e.g. cached results),
      if None --- defaults to `lambda node: (get_incoming(node), None)`;
    :return: list with values of `r(node)` for each `node` in `nodes`,
      or just `r(node)` in case if `nodes` is a single node.
    """

  if isinstance(nodes, (tuple, list)):
    result = dynamic_propagate(f, nodes, substitutes=substitutes, incoming=incoming)
    return tuple(
      result[node]
      for node in nodes
    )

  else:
    result = dynamic_propagate(f, (nodes, ), substitutes=substitutes, incoming=incoming)
    return result[nodes]

def map_graph(f, nodes):
  """
  A wrapper over `propagate` for functions that does not depend on incoming values.
    Results are topologically ordered.

  :param f: `Node -> value`
  :param nodes: final nodes of the dataflow on which to compute `f`.
  :return: topologically ordered outputs.
  """

  if not isinstance(nodes, (list, tuple)):
    nodes = [nodes]

  return list(
    propagate(
      f=lambda node, *args: f(node),
      nodes=nodes,
      substitutes=dict()
    ).values()
  )

def graph_reducer(operator, strict=False):
  """
    Wraps operator into `propagate`-operator.

  :param operator: `Node` -> function
  :param strict: if `False` use `apply_with_kwargs` wrapper on `operator` which filters key word arguments before passing
    them into the propagated function; otherwise, passes `**kwargs` directly to the propagated function.
  :return: a getter, function `(list of nodes, substitution dictionary=None, **kwargs) -> value`
    that computes the operator output for `nodes`.
  """
  def getter(nodes_or_node, substitutes=None, **kwargs):
    from ..meta import apply_with_kwargs

    if not isinstance(nodes_or_node, (list, tuple)):
      nodes = [nodes_or_node]
    else:
      nodes = nodes_or_node

    if substitutes is None:
      substitutes = dict()

    if strict:
      wrapped_operator = lambda node, args: operator(node)(*args, **kwargs)
    else:
      wrapped_operator = lambda node, args: apply_with_kwargs(operator(node), *args, **kwargs)

    results = propagate(wrapped_operator, nodes, substitutes)

    if isinstance(nodes_or_node, Node):
      return results[nodes_or_node]
    else:
      return [results[node] for node in nodes_or_node]

  return getter

def select_subgraph(predicate, nodes, single=False):
  results = []

  if not isinstance(nodes, (list, tuple)):
    stack = [nodes]
  else:
    stack = list(nodes)

  visited = set()

  while len(stack) > 0:
    current = stack.pop()
    if current in visited:
      continue

    if predicate(current):
      if single:
        return current
      else:
        results.append(current)

    incoming = get_incoming(current)
    stack.extend(incoming)

  if single:
    return None
  else:
    return results

def modify_graph(f, node_or_nodes):
  """
  This function dynamically changes graph with outputs `nodes` by propagating operator `f`
  from outputs to the inputs. Operator `f` receives a node and must output a tuple `(node replacement, subgraph)`,
  where:
    - node_replacement: must be either:
      - None: to remove current node from the graph;
      - a `Node` instance: to replace current node with, the instance will be copied and have incoming overridden;
      - a node model: *Node -> Node, a replacement for the current node.
    - subgraph: list of nodes for further propagation. Must be a subset of the incoming nodes of the original node.

  This function allows, for example, to prune graph.

  *Note*: this function might make shallow copies of the nodes and override `incoming` value.
    Inappropriate operator may result in an invalid graph. For example, removing second convolution from
    `conv(8) -> conv(16) -> conv(32)` will leave the last convolution with a mismatched kernel.

  *Note*: inputs node are never copied.
  """

  import copy

  visited = dict()

  if isinstance(node_or_nodes, (list, tuple)):
    nodes = node_or_nodes
  else:
    nodes = [node_or_nodes]

  stack = [node for node in nodes]

  while len(stack) > 0:
    current = stack.pop()
    if current in visited:
      continue

    replacement, subgraph = f(current)
    visited[current] = (replacement, subgraph)
    stack.extend(subgraph)

  graph = dict()
  stack = [node for node in nodes]

  while len(stack) > 0:
    current = stack.pop()

    if current in graph:
      continue

    replacement, subgraph = visited[current]
    unknown = [n for sg in subgraph for n in sg if n not in graph]

    if len(unknown) > 0:
      stack.append(current)
      stack.extend(unknown)
    else:
      incoming = [n for sg in subgraph for n in sg]

      if replacement is None:
        graph[current] = incoming

      elif isinstance(replacement, Node):
        new_replacement = copy(replacement)
        new_replacement.set_incoming(incoming)
        graph[current] = [new_replacement]

      elif callable(replacement):
        new_replacement = replacement(*incoming)
        graph[current] = [new_replacement]

  if isinstance(node_or_nodes, (list, tuple)):
    return [n for node in node_or_nodes for n in graph[node]]
  else:
    if len(graph[node_or_nodes]) == 1:
      return graph[node_or_nodes][0]
    else:
      return graph[node_or_nodes]

get_nodes = lambda nodes: map_graph(lambda node: node, nodes)

get_inputs_nodes = lambda nodes: [
  node
  for node in get_nodes(nodes)
  if len(get_incoming(node)) == 0
]

def get_subgraph(nodes, origins):
  if isinstance(nodes, Node):
    nodes = [nodes]

  return [
    node

    for node, is_origin in propagate(
      lambda node, *args, **kwargs: False,
      nodes, substitutes=dict([
        (origin, True) for origin in origins
      ])
    ).items()

    if not is_origin
  ]

def model_selector(criterion):
  def selector(models):
    from inspect import signature
    assert len(models) > 0
    models_signatures = [
      signature(model) for model in models
      if model is not None
    ]

    if len(set(models_signatures)) != 1:
      pretty_signatures = '\n  '.join([ str(signature) for signature in set(models_signatures)])
      raise ValueError('All models must have the same signature, got:%s' % pretty_signatures)

    common_signature = models_signatures[0]

    bound_criterion = criterion(models)

    def common_model(*args, **kwargs):
      common_signature.bind(*args, **kwargs)

      def model(incoming):
        selected_model = bound_criterion(incoming)
        if selected_model is None:
          raise ValueError('Invalid incoming node!')

        node = selected_model(*args, **kwargs)(incoming)
        return node

      return model

    common_model.__signature__ = common_signature
    return common_model

  return selector