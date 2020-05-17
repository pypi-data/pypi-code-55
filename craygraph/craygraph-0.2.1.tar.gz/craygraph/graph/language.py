from collections import namedtuple

from ..meta import NodeModel

from .achain import achain as _achain
from .selector import SelectStatement, NothingStatement

__all__ = [
  'graph_lang', 'GraphLang'
]

GraphLang = namedtuple(
  'GraphLang', [
    'achain',
    'repeat',
    'for_each',
    'with_inputs',
    'select',
    'seek',
    'nothing'
  ]
)

def graph_lang(apply=None):
  class achain(NodeModel):
    def __init__(self, *definition):
      self.definition = definition

    def __call__(self, *incoming):
      return _achain(incoming, self.definition, apply=apply)

  def repeat(n):
    def repeated(*definition):
      return achain(definition * n)

    return repeated

  class for_each(NodeModel):
    def __init__(self, *definition):
      self.definition = definition

    def __call__(self, *incoming):
      return [
        _achain(input, self.definition, apply=apply)
        for input in incoming
      ]

  nothing = NothingStatement()

  select = SelectStatement(
    achain=achain,
    search_subgraph=False,
    replace=False
  )

  seek = SelectStatement(
    achain=achain,
    search_subgraph=True,
    replace=False
  )

  with_inputs = SelectStatement(
    achain=achain,
    search_subgraph=False,
    replace=True
  )

  return GraphLang(
    achain=achain,
    repeat=repeat,
    for_each=for_each,
    with_inputs=with_inputs,
    select=select,
    seek=seek,
    nothing=nothing
  )