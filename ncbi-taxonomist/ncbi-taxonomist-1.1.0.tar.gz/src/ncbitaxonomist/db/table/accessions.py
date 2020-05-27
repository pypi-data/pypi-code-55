"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sqlite3
from typing import Iterable, Tuple, Type


from ncbitaxonomist.db.table import basetable

class AccessionTable(basetable.BaseTable):

  def __init__(self, database):
    super().__init__('accessions', database=database)

  def create(self, connection:Type[sqlite3.Connection])->__qualname__:
    stmt = """CREATE TABLE IF NOT EXISTS accessions
              (id        INTEGER PRIMARY KEY,
               accession TEXT NOT NULL,
               db        TEXT NOT NULL,
               type      TEXT NULL,
               uid       INT NOT NULL,
               taxon_id  INT NOT NULL,
               FOREIGN KEY (taxon_id) REFERENCES taxa(taxon_id) ON DELETE CASCADE,
               UNIQUE(accession, uid))"""
    connection.cursor().execute(stmt)
    stmt = """CREATE TRIGGER IF NOT EXISTS delete_uids DELETE ON accessions
              BEGIN DELETE FROM accessions WHERE uid=old.uid; END;"""
    connection.cursor().execute(stmt)
    self.create_index(connection)
    return self

  def create_index(self, connection:Type[sqlite3.Connection])->None:
    stmt = """CREATE UNIQUE INDEX IF NOT EXISTS {0} ON
              accessions (accession, uid)""".format(self.idx)
    connection.cursor().execute(stmt)

  def get_rows(self, connection:Type[sqlite3.Connection])->Type[sqlite3.Cursor]:
    return connection.cursor().execute("SELECT accession, db, taxon_id FROM accessions")

  def insert(self, connection:Type[sqlite3.Connection], values:Iterable[Tuple[str,str,str,int,int]])->None:
    stmt = """INSERT OR IGNORE INTO accessions
              (accession, type, db, uid, taxon_id) VALUES (?,?,?,?,?)"""
    connection.cursor().executemany(stmt, values)
    connection.commit()
