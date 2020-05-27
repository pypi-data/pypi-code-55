"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sqlite3
from typing import Tuple, Type


import ncbitaxonomist.db.table.basetable


class NameTable(ncbitaxonomist.db.table.basetable.BaseTable):
  """Implements the name table in a taxonomist database."""

  def __init__(self, database:str):
    super().__init__('names', database=database)

  def create(self, connection:Type[sqlite3.Connection]) -> __qualname__:
    stmt = """CREATE TABLE IF NOT EXISTS {}
              (id           INTEGER PRIMARY KEY,
                taxon_id     INT,
                name         TEXT,
                type         TEXT NULL,
                FOREIGN KEY (taxon_id) REFERENCES taxa(taxon_id) ON DELETE CASCADE,
                UNIQUE(taxon_id, name))""".format(self.name)
    connection.cursor().execute(stmt)
    stmt = """CREATE TRIGGER IF NOT EXISTS delete_names DELETE ON names
              BEGIN DELETE FROM names WHERE taxon_id=old.taxon_id; END;"""
    connection.cursor().execute(stmt)
    self.create_index(connection)
    return self

  def create_index(self, connection:Type[sqlite3.Connection]):
    stmt = """CREATE UNIQUE INDEX IF NOT EXISTS {0} ON names (taxon_id, name)""".format(self.idx)
    connection.cursor().execute(stmt)

  def get_rows(self, connection:Type[sqlite3.Connection])->Type[sqlite3.Cursor]:
    return connection.cursor().execute("SELECT taxon_id, name, type FROM {0}".format(self.name))

  def insert(self, connection:Type[sqlite3.Connection], values:Tuple[int, str, str]):
    stmt = """INSERT OR IGNORE INTO {0} (taxon_id, name, type) VALUES (?,?,?)""".format(self.name)
    connection.cursor().executemany(stmt, values)
    connection.commit()

  def name_to_taxid(self, connection:Type[sqlite3.Connection], name)->Type[sqlite3.Cursor]:
    stmt = """SELECT name, taxon_id FROM names WHERE name=?"""
    return connection.cursor().execute(stmt, (name,))
