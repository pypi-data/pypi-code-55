#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_atws
----------------------------------

Tests for `atws` module.
"""

import os
import sys
import logging
import unittest
from contextlib import contextmanager
import atws
import suds

logger = logging.getLogger(__name__)
query_test_output=u'<?xml version="1.0" ?>\n<queryxml>\n\t<entity>Ticket</entity>\n\t<query>\n\t\t<field>\n\t\t\tStatus\n\t\t\t<expression op="NotEqual">5</expression>\n\t\t</field>\n\t\t<condition>\n\t\t\t<condition operator="OR">\n\t\t\t\t<field>\n\t\t\t\t\tIssueType\n\t\t\t\t\t<expression op="GreaterThan">345</expression>\n\t\t\t\t</field>\n\t\t\t</condition>\n\t\t</condition>\n\t</query>\n</queryxml>\n'


class UnConnectedTest(unittest.TestCase): pass

class ConnectedTest(UnConnectedTest):
    
    def setUp(self):
        url = os.environ.get('AUTOTASK_URL', None) # save the wsdl lookups
        self.api = atws.connect(username=os.environ['AUTOTASK_USERNAME'],
                                password=os.environ['AUTOTASK_PASSWORD'],
                                url=url)


class TestUnitTestATWS(UnConnectedTest):

    def test_000_zone_lookup_failure(self):
        try:
            _ = atws.connect(username='failed@toresolve.com',
                              password='notright')
        except ValueError as e:
            assert 'failed@toresolve.com failed to resolve to a zone' in str(e) 

class TestUnitTestQuery(UnConnectedTest):
    
    def test_001_query_building_output(self):
        query = atws.Query('Ticket')
        query.WHERE('Status', query.NotEqual, 5)
        query.open_bracket()
        query.OR('IssueType', query.GreaterThan, 345)
        query_output = query.pretty_print()
        assert repr(query_test_output) == repr(query_output)
        
class TestIntegratedGetMethods(ConnectedTest):
    def test_001_get_entity_info(self):
        infos = self.api.getEntityInfo()
        self.assertGreater(len(infos), 0, 'There have to be some '
                           'entities with info returned!')

class TestIntegratedQueryCursorFeatures(ConnectedTest):
    def test_011_next_method(self):
        complete = self.api.picklist['Ticket']['Status']['Complete']
        query = atws.Query('Ticket')
        query.WHERE('Status', query.Equals, complete)
        tickets = self.api.query(query)
        ticket = tickets.next()
        self.assertEqual(ticket.Status, complete, 'It may not be related to '
                         'the query cursor next failing if this does not pass '
                         'as it could be the lookup values')
        
        ticket2 = next(tickets)
        self.assertEqual(ticket2.Status, complete, 'It is unlikely related to '
                         'the query cursor next failing if this does not pass '
                         'as the failure will probably be an exception on the '
                         'next call')
        
        i=0
        for ticket in tickets:
            i+=1
            self.assertEqual(ticket.Status, complete)
            if i>2:
                break
               
        
class TestIntegratedPicklist(ConnectedTest):
    
    def test_001_field_picklist_status_lookup(self):
        field_picklist = self.api.picklist['Ticket']['Status']
        complete = field_picklist['Complete']
        self.assertEqual(complete, 5, 'lookup for complete did not match 5')

    def test_002_field_picklist_status_reverse_lookup(self):
        field_picklist = self.api.picklist['Ticket']['Status']
        complete = field_picklist['Complete']
        self.assertEqual('Complete', field_picklist.reverse_lookup(complete))
        
    def test_011_parent_child_subissuetype_lookup(self):
        with self.assertRaises(KeyError, 
                         msg='Access|Password reset == 157 and is active.'
                         'This test should only pass if parent or child is NOT'
                         ' active'):

            child_fieldpicklist = self.api.picklist['Ticket']['SubIssueType']
            parent_child = child_fieldpicklist['Workstation SW']
            
            _ = parent_child['Autotask']
    
    def test_012_parent_child_subissuetype_lookup(self):
        child_fieldpicklist = self.api.picklist['Ticket']['SubIssueType']
        parent_child = child_fieldpicklist['Printing & Scanning']
        lookup_value = parent_child['Consumable']
        self.assertEqual(lookup_value, 393, 'The value for '
                         'Printing & Scanning|Consumable is either not 393 or '
                         'parent/child is NOT active')
        
    def test_022_entity_to_picklist_match_check(self):
        complete = self.api.picklist['Ticket']['Status']['Complete']
        ticket_query = atws.Query('Ticket')
        ticket_query.WHERE('Status', ticket_query.Equals, complete)
        ticket = self.api.query(ticket_query).fetch_one()
        self.assertEqual(ticket.Status, complete, 'ticket status is not '
                         'mapping to the same value as a lookup that a query '
                         'for that status does - issue #77')
        
if __name__ == '__main__':
    sys.exit(unittest.main())
