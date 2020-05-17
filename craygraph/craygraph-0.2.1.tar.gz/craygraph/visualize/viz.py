from ..meta import propagate, get_incoming, get_name

### With a little shame stolen from nolearn
### heavily modified afterwards

"""
Copyright (c) 2012-2015 Daniel Nouri

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__all__ = [
  'draw_to_file',
  'draw_to_notebook',
  'get_info'
]

default_display_properties = dict(
  __style__ = 'filled',
  __color__ = 'black',
  __fillcolor__ = 'white',
  __shape__ = 'box',
  _name_ = lambda node: get_name(node) if get_name(node) is not None else node.__class__.__name__.lower()
)

def make_graphviz_table(props, ports):
  port_row = '<TR>%s</TR>' % (
    ''.join(
      '<TD PORT="%s" BORDER="1">%s</TD>' % (port, port)
      for port in ports
    )
  )

  return \
    '<<TABLE CELLSPACING="0" CELLPADDING="5" BORDER="0">' \
    '%s' \
    '<TR><TD COLSPAN="%d">%s</TD></TR>' \
    '</TABLE>>' % (
      port_row, len(ports),'<BR/>'.join(props)
    )

def get_info(node, incoming, display_properties):
  """
  Applies `display_properties` to `node` and converts it to graphviz node attributes.

  If `display_properties` is a callable, simply returns `display_properties(node, incoming)`.
  In this case, `display_properties` must return a dictionary with graphviz node attributes, e.g.:

      def my_display_properties(node, incoming):
        return dict(
          style='filled',
          color='purple',
          label='node %s is the best' % (node.name, )
        )

  Alternatively, `display_properties` should be a dictionary with keys corresponding to attribute names and value
  that are either:
  - strings (treated as a constant);
  - functions: Node -> string

  If attribute name starts and ends with `__` (double underscore) it is treated as node attribute, e.g.:

      display_properties = dict( __color__ = 'black', ... )

  produces:

      some_node [color='black', ...]

  All other attributes form node's label:
  - if attribute name starts with `_` (single underscore), value is added to nodes label as is;
  - otherwise, attribute is appended to label as `<attribute name> : <attribute value>`.
  For example:

      display_properties = dict( _name_ = lambda node: node.name, kernel = lambda node: str(node.kernel_size) )

  might produce:

      some_node [..., label='My Node\nkernel: 3x3']

  :param node: node to pull attributes from;
  :param incoming: None or a list/tuple of names for incoming node;
    if not None, shape of graphviz node is changed to `record` adding corresponding ports;
  :param display_properties: see above;
  :return: dictionary with graphviz node attributes.
  """
  if callable(display_properties):
    return display_properties(node, incoming)

  node_props = dict()

  if isinstance(display_properties, dict):
    for prop_name, prop in display_properties.items():
      if prop is None:
        pass

      elif callable(prop):
        result = prop(node)
        if result is not None:
          node_props[prop_name] = result

      elif isinstance(prop, str):
        node_props[prop_name] = prop

      else:
        raise ValueError(
          'Display property %s [%s] is not understood: must be either:'
           'callable: (Node, Nodeinfo) -> value;'
           'string: attribute name;'
           '(string, default value): attribute name and its default value.' % (prop_name, prop)
        )

  else:
    raise ValueError(
      'Display properties must be either a callable or a attribute dictionary.'
    )

  display_props = dict()
  label_props = []
  for k in node_props:
    if k.startswith('__') and k.endswith('__'):
      display_props[k[2:-2]] = node_props[k]
    elif k.startswith('_') and k.endswith('_'):
      label_props.append(str(node_props[k]))
    else:
      label_props.append('%s: %s' % (k, node_props[k]))

  if incoming is not None:
    display_props['label'] = make_graphviz_table(label_props, incoming)
    display_props['margin'] = 0
  else:
    display_props['label'] = '\n'.join(label_props)

  return display_props

try:
  from pydotplus import Subgraph
  class Ordering(Subgraph):
    def __init__(self, graph_name=''):
      super(Ordering, self).__init__(graph_name=graph_name, rank='same')

      ### dirty hack to erase `subgraph ...`
      self.obj_dict['show_keyword'] = False
      self.obj_dict['type'] = ''
      self.obj_dict['name'] = ''
except ImportError:
  Ordering = None

def make_ordered_cluster(nodes, name):
  import pydotplus as pd
  cluster = Ordering(graph_name=name)

  for node in nodes:
    cluster.add_node(node)

  ### force ordering of the nodes
  for node1, node2 in zip(nodes[:-1], nodes[1:]):
    cluster.add_edge(pd.Edge(node1, node2, style='invis'))

  return cluster

default_selector = lambda node, args: get_incoming(node)

def make_graph(
  outputs, inputs=None,
  display_properties=None, vertical=True,
  selector=default_selector
):
  if display_properties is None:
    display_properties = default_display_properties

  if inputs is None:
    inputs = tuple()

  import pydotplus as pydot

  rankdir = 'TB' if vertical else 'LR'
  dot_graph = pydot.Dot(
    'network',
    graph_type='digraph',
    rank='source',
    rankdir=rankdir,
    nodesep=0.4,
    bgcolor='transparent',
    splines='polyline'
  )

  display_graph = propagate(
    selector,
    outputs,
    substitutes=dict(
      (input_node, tuple())
      for input_node in inputs
    )
  )

  display_graph = {
    node : incoming
    for node, incoming in display_graph.items()
    if incoming is not None
  }

  node_naming = dict()
  dot_nodes = dict()

  for node, incoming in display_graph.items():
    if isinstance(incoming, dict):
      incoming = {
        port : node
        for port, node in incoming.items()
        if node in display_graph
      }
    else:
      incoming = tuple(
        node
        for node in incoming
        if node in display_graph
      )

    node_naming[node] = 'node%d' % (len(node_naming), )

    dot_nodes[node] = pydot.Node(
      name=node_naming[node],
      **get_info(
        node,
        incoming=incoming if isinstance(incoming, dict) else None,
        display_properties=display_properties)
    )
    dot_graph.add_node(dot_nodes[node])

    if isinstance(incoming, dict):
      for port, incoming_node in incoming.items():
        dot_graph.add_edge(pydot.Edge(
          node_naming[incoming_node],
          '%s:%s' % (node_naming[node], port)
        ))
    else:
      for incoming_node in incoming:
        dot_graph.add_edge(pydot.Edge(
          node_naming[incoming_node],
          '%s' % (node_naming[node], )
        ))

  dot_graph.add_subgraph(make_ordered_cluster(
    tuple(dot_nodes[node] for node in inputs),
    'inputs'
  ))

  return dot_graph


def get_image(graph, inputs=None, display_properties=None, vertical=True, format='png', selector=default_selector):
  import pydotplus as pydot
  from ..meta import Node

  if display_properties is None:
    display_properties = default_display_properties

  try:
    if isinstance(graph, Node):
      outputs = (graph,)

    elif isinstance(graph, (list, tuple)) and all(isinstance(node, Node) for node in graph):
        outputs = graph

    elif hasattr(graph, 'outputs'):
      outputs = getattr(graph, 'outputs')()

      if inputs is None and hasattr(graph, 'inputs'):
        inputs = getattr(graph, 'inputs')()

      return get_image(
        outputs, inputs,
        display_properties=display_properties, vertical=True,
        format='png', selector=selector
      )

    else:
      raise Exception(
        '`outputs` must be a node, a tuple/list of nodes '
        'or a object with `outputs` method that is a node or a tuple/list of nodes.'
      )

    if inputs is None:
      pass

    elif isinstance(inputs, Node):
      inputs = (inputs,)

    elif isinstance(inputs, (list, tuple)) and all(isinstance(node, Node) for node in inputs):
      pass

    elif isinstance(inputs, dict) and all(isinstance(node, Node) for node in inputs.values()):
      inputs = list(inputs.values())

    else:
      raise Exception(
        '`inputs` must be None, a node, a tuple/list of nodes '
        'or a object with `inputs` attribute that is a node or a tuple/list/dict of nodes.'
      )

    return make_graph(
      outputs, inputs=inputs,
      display_properties=display_properties,
      vertical=vertical,
      selector=selector
    ).create(format=format)

  except pydot.InvocationException:
    import traceback
    tb = traceback.format_exc()

    import warnings
    warnings.warn(tb)

def draw_to_file(path, outputs, inputs=None, vertical=True, selector=default_selector, **display_properties):
  display_props = default_display_properties.copy()
  display_props.update(display_properties)

  png = get_image(
    outputs, inputs=inputs,
    display_properties=display_props,
    vertical=vertical,
    selector=selector
  )

  with open(path, 'wb') as f:
    f.write(png)


def draw_to_notebook(nodes, inputs=None, vertical=True, selector=default_selector, **display_properties):
  from IPython.display import Image

  display_props = default_display_properties.copy()
  display_props.update(display_properties)

  png = get_image(
    nodes, inputs=inputs,
    display_properties=display_props,
    vertical=vertical,
    selector=selector
  )

  return Image(png)