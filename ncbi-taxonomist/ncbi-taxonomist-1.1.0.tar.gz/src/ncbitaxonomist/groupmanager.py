#!/usr/bin/env python3
"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""


from typing import Type


import ncbitaxonomist.utils
import ncbitaxonomist.parser.group
import ncbitaxonomist.model.taxon
import ncbitaxonomist.convert.taxadb

class GroupManager:
  """
  Class managing groups in a local database. It's responsible for adding and
  deleting groups or entries into groups.
  """

  def __init__(self, taxonomist):
    self.db = taxonomist.db

  def group(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload],
            names:Type[ncbitaxonomist.payload.name.NamePayload], args):

    if args.list:
      self.list_groups()
      return
    if args.add:
      self.add(taxids, names, args.add)
      return
    if args.rm:
      self.remove(taxids, names, args.rm)
      return
    if args.get is not None:
      if not args.get:
        args.get = None
      self.retrieve_groups(ncbitaxonomist.payload.name.NamePayload(args.get))
      return

  def add(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload],
          names:Type[ncbitaxonomist.payload.name.NamePayload], groupname:str):
    """Create a new group or add to existing group in a local database."""
    values = []
    if not taxids.has_data() and not names.has_data():
      gp = ncbitaxonomist.parser.group.GroupParser()
      values = gp.parse(groupname)
    else:
      if taxids.has_data():
        for i in taxids.as_list():
          values.append((taxids.pop(), groupname))
      if names.has_data():
        for i in self.db.get_taxa_by_name(
          names.as_list(), ncbitaxonomist.convert.taxadb.TaxaDbConverter(
            ncbitaxonomist.model.taxon.Taxon())):
          if not taxids.contains(i.taxid()):
            values.append((i.taxid(), groupname))
    self.db.add_group(values)

  def remove(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload],
             names:Type[ncbitaxonomist.payload.name.NamePayload], groupname:str):
    """Remove group or entries belonging to a specific group from a local
    database."""
    if not taxids.has_data() and not names.has_data() and groupname is not None:
      self.db.remove_group(groupname)
    else:
      self.db.remove_from_group(taxids.as_list(), names.as_list(), groupname)

  def move(self, srcgroup, targetgroup, taxids, names):
    """ Future plan to implement"""
    raise NotImplementedError("For future release")

  def retrieve_groups(self, names:Type[ncbitaxonomist.payload.name.NamePayload]):
    """Get all or given groups from local database"""
    if names.has_data():
      for i in names.as_list():
        self.retrieve_group(i)
    else:
      self.retrieve_group()

  def retrieve_group(self, groupname:str=None):
    """Get group from local database"""
    groups = {}
    prev = None
    for i in self.db.retrieve_group(groupname):
      if i['name'] not in groups:
        if groups:
          ncbitaxonomist.utils.json_stdout({'group:': prev,
                                            'taxa': groups[prev]})
        prev = i['name']
        groups[i['name']] = []
      groups[i['name']].append(i['taxon_id'])
    if groups:
      ncbitaxonomist.utils.json_stdout({'group:': prev, 'taxa': groups[prev]})

  def list_groups(self):
    """List group names in local database"""
    for i in self.db.retrieve_group_names():
      print(i['name'])
