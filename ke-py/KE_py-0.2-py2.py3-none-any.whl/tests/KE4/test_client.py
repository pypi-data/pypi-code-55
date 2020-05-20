# coding=u8
import unittest
from KE import KE, KE3, KE4
from KE.v4.job import Job
from KE.exceptions import ResourceUnavailable


class ClientV4TestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self._client = KE('10.1.3.63', port=7171, username='ADMIN', password='KYLIN', version=4)
        print(self._client)

    def test_debug(self):
        client = KE('10.1.3.63', port=7171, username='ADMIN', password='KYLIN', version=4, debug=True)
        client.models(project='learn_kylin')

    def test_projects(self):
        projects = self._client.projects()
        print(projects)
        print(len(projects))

    def test_fetch_json(self):
        client = KE('device2', username='admin', password='wrongpassword', version=4)
        with self.assertRaises(ResourceUnavailable):
            client.fetch_json('/projects/')

        json_obj = self._client.fetch_json('/projects/')
        self.assertIsInstance(json_obj, dict)

    def test_jobs(self):
        jobs = self._client.jobs()
        job = jobs[0]
        print(job)
        self.assertIsInstance(job, Job)

        project_jobs = self._client.jobs(project='learn_kylin')
        job = project_jobs[0]
        self.assertEqual(job.project_name, 'learn_kylin')

    def test_models(self):
        models = self._client.models(name="kylin_sales_cube", project='learn_kylin')
        print(models)

    def test_users(self):
        users = self._client.users()
        print(users)


