import mock
import pytest
from pytest_mock import mocker
from python_notes.test.source import manager

'''
https://medium.com/@bfortuner/python-unit-testing-with-pytest-and-mock-197499c4623c
https://packaging.python.org/tutorials/packaging-projects/
'''

def test_update_jobs_fleet_capacity(mocker):
  mocker.patch.object(manager, 'sub_method')
  manager.sub_method.return_value = 120
  result = manager.method_under_test()
  manager.sub_method.assert_called_with('somestring', 1, 120)
  assert result == 121