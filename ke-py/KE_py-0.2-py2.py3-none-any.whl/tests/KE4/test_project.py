from __future__ import with_statement, print_function
import os
import unittest
from datetime import datetime
from KE import KE, KE3, KE4


class ProjectV4TestCase(unittest.TestCase):

    def setUp(self):
        self._client = KE('10.1.3.63', port=7171, username='ADMIN', password='KYLIN', version=4)

    def test_project_properties(self):
        project = self._client.projects(name='learn_kylin')
        self.assertEqual(project.name, 'learn_kylin')

    def test_project_jobs(self):
        project = self._client.projects(name='learn_kylin')
        jobs = project.jobs()
        print(jobs)

        jobs_last_week = project.jobs(time_filter=1)
        print(jobs_last_week)

        jobs_today = project.jobs(time_filter=0)
        print(jobs_today)

    def test_project_models(self):
        project = self._client.projects(name='learn_kylin')
        models = project.models()
        self.assertIn('kylin_sales_cube', [m.name for m in models])

