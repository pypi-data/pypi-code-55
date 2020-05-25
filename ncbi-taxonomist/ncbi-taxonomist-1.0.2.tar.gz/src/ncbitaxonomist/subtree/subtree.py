"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Type
import ncbitaxonomist.model.taxon

class Subtree:
  """
  Implements subtree and collects children taxids in addition to taxa.
  """

  class Node:
    """
    Stores taxid and its children.
    """
    def __init__(self, taxid:int, parent_id:int=None):
      self.taxid = taxid
      self.parent_id = parent_id
      self.children = set()

  def __init__(self):
    self.taxa = {}
    self.nodes = {}

  def add_taxon(self, taxon:Type[ncbitaxonomist.model.taxon.Taxon]):
    """Adds taxa to subtree"""
    if taxon.taxon_id not in self.taxa:
      self.taxa[taxon.taxon_id] = taxon
    if taxon.taxon_id not in self.nodes:
      self.nodes[taxon.taxon_id] = Subtree.Node(taxon.taxon_id)
    if taxon.parent_id is not None and taxon.parent_id not in self.nodes:
      self.nodes[taxon.parent_id] = Subtree.Node(taxon.parent_id)
    self.nodes[taxon.taxon_id].parent_id = taxon.parent_id
    if taxon.parent_id is not None:
      self.nodes[taxon.parent_id].children.add(taxon.taxon_id)

  def isCollected(self, taxid:int)->bool:
    """Tests is taxa is collected. Should be replaces by meth:`has_taxon`."""
    return taxid in self.taxa

  def has_taxon(self, taxid:int):
    """Tests is taxa is collected. """
    return taxid in self.taxa

  def get_taxon(self, taxid:int):
    """Getter for a taxon."""
    return self.taxa[taxid]
