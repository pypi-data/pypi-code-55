"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sqlite3
from typing import Iterable, Tuple, Type

import ncbitaxonomist.db.table.basetable

class TaxaTable(ncbitaxonomist.db.table.basetable.BaseTable):
  """Implements taxa table for local taxonomy database."""

  def __init__(self, database:str):
    super().__init__(name='taxa', database=database)

  def create(self, connection:Type[sqlite3.Connection])->__qualname__:
    stmt = """CREATE TABLE IF NOT EXISTS taxa
              (id           INTEGER PRIMARY KEY,
               taxon_id     INT NOT NULL,
               rank         TEXT NULL,
               parent_id    INT NULL,
               UNIQUE(taxon_id))"""
    connection.cursor().execute(stmt)
    self.create_index(connection)
    return self

  def create_index(self, connection:Type[sqlite3.Connection])->None:
    stmt = """CREATE UNIQUE INDEX IF NOT EXISTS {0} ON taxa (taxon_id)""".format(self.idx)
    connection.cursor().execute(stmt)

  def insert(self, connection:Type[sqlite3.Connection], taxavalues:Iterable[Tuple[int,str,int]])->None:
    stmt = """INSERT INTO taxa (taxon_id, rank, parent_id) VALUES (?,?,?)
              ON CONFLICT (taxon_id) WHERE parent_id is NULL
              DO UPDATE SET parent_id=excluded.parent_id,rank=excluded.rank"""
    connection.cursor().executemany(stmt, taxavalues)
    connection.commit()

  def insert_taxids(self, connection:Type[sqlite3.Connection], taxids:Iterable[int])->None:
    stmt = """INSERT OR IGNORE INTO taxa (taxon_id) VALUES (?)"""
    connection.cursor().executemany(stmt, taxids)
    connection.commit()

  def get_taxids(self, connection:Type[sqlite3.Connection])->Type[sqlite3.Cursor]:
    return connection.cursor().execute("""SELECT taxon_id FROM taxa""")

  def get_rows(self, connection:Type[sqlite3.Connection])->Type[sqlite3.Cursor]:
    return connection.cursor().execute("SELECT taxon_id, rank, name, parent_id FROM taxa")

  def get_lineage(self, connection:Type[sqlite3.Connection], taxid:int, name_table:str)->Type[sqlite3.Cursor]:
    """Recursive construction of lineage from given taxid to highest parent."""
    stmt = """WITH RECURSIVE parent(taxon_id) AS
      (SELECT taxon_id FROM taxa WHERE taxon_id=?  -- initial lookup
       UNION ALL                                   -- start recursion
       SELECT t.parent_id FROM taxa t, parent      -- subquery
       WHERE  t.taxon_id=parent.taxon_id)
      SELECT t.taxon_id, t.rank, t.parent_id, n.name, n.type FROM taxa t -- select recursion result
      JOIN parent p ON t.taxon_id=p.taxon_id
      JOIN {0} n ON t.taxon_id=n.taxon_id""".format(name_table)
    return connection.cursor().execute(stmt, (taxid,))

  def get_subtree(self, connection:Type[sqlite3.Connection], taxid:int)->Type[sqlite3.Cursor]:
    """Depth first search of taxon ids to find the subtree of taxid"""
    stmt = """WITH RECURSIVE subtree(taxon_id, depth, rank) AS
      (SELECT ti.taxon_id, 0, ti.rank FROM taxa ti WHERE ti.taxon_id=? -- initial lookup
       UNION ALL                                                      -- start recursion
       SELECT tq.taxon_id, st.depth+1, tq.rank FROM taxa tq            -- subquery
       JOIN subtree st ON tq.parent_id=st.taxon_id
       ORDER BY 2 DESC)                                               -- do dfs
       SELECT rst.taxon_id, rst.rank, t.parent_id, n.name, n.type FROM subtree rst -- select recursed results
       JOIN names n on rst.taxon_id=n.taxon_id
       JOIN taxa t on t.taxon_id=rst.taxon_id"""
    return connection.cursor().execute(stmt, (taxid,))
