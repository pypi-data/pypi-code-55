import unittest

from koala_formatter.formatters.db.orcale_formatter import OracleFormatter

#                       schema1
#           table1                    table2
#            //                         \\
#         column1                      column2

resources = [{'schema_name': 'schema1',
              'table_name': 'table1',
              'column_name': 'column1',
              'data_type': 'number',
              'column_description': 'test_column'},
             {'schema_name': 'schema1',
              'table_name': 'table2',
              'column_name': 'column2',
              'data_type': 'date',
              'column_description': 'test_column'}
             ]

collections = [{'schema_name': 'schema1',
                'table_name': 'table1',
                'table_description': 'test_table',
                'team_name': 'test_team1'},
               {'schema_name': 'schema1',
                'table_name': 'table2',
                'table_description': 'test_table',
                'team_name': 'test_team2'}
               ]


expected_resource_nodes = [{'prop': {'id': 'schema1.table1.column1',
                                     'schema_name': 'schema1',
                                     'table_name': 'table1',
                                     'column_name': 'column1',
                                     'data_type': 'number',
                                     'column_description': 'test_column',
                                     'type': 'db_table_column'
                                     }
                            },
                           {'prop': {'id': 'schema1.table2.column2',
                                     'schema_name': 'schema1',
                                     'table_name': 'table2',
                                     'column_name': 'column2',
                                     'data_type': 'date',
                                     'column_description': 'test_column',
                                     'type': 'db_table_column'
                                     }
                            }
                           ]

expected_collection_nodes = [{'prop': {'id': 'schema1.table1',
                                       'schema_name': 'schema1',
                                       'table_name': 'table1',
                                       'table_description': 'test_table',
                                       'team_name': 'test_team1',
                                       'type': 'db_table'}},
                             {'prop': {'id': 'schema1.table2',
                                       'schema_name': 'schema1',
                                       'table_name': 'table2',
                                       'table_description': 'test_table',
                                       'team_name': 'test_team2',
                                       'type': 'db_table'}}]

expected_edges = [{'n1': 'schema1.table1',
                   'n2': 'schema1.table1.column1',
                   'prop': {'edge_description': 'contains'}
                   },
                  {'n1': 'schema1.table1.column1',
                   'n2': 'schema1.table1',
                   'prop': {'edge_description': 'belongs to'}
                   },
                  {'n1': 'schema1.table2',
                   'n2': 'schema1.table2.column2',
                   'prop': {'edge_description': 'contains'}
                   },
                  {'n1': 'schema1.table2.column2',
                   'n2': 'schema1.table2',
                   'prop': {'edge_description': 'belongs to'}
                   }
                  ]


class TestOracleFormatter(unittest.TestCase):
    def test_create_nodes(self):
        formatter = OracleFormatter()
        collections_nodes, resources_nodes, edges = formatter.create_nodes(collections, resources)
        self.assertEqual(expected_resource_nodes, resources_nodes)
        self.assertEqual(expected_collection_nodes, collections_nodes)
        self.assertEqual(expected_edges, edges)

