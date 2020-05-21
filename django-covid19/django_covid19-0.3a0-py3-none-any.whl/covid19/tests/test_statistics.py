import json
from django.urls import reverse
from django.test import TestCase, Client

from ..models import Statistics

TEST_DATA = {
    "globalStatistics": {
        "currentConfirmedCount": 2720207,
        "curedCount": 1802983,
        "confirmedCount": 4845417,
        "seriousCount": 0,
        "suspectedCount": 0,
        "deadCount": 322227,
        "currentConfirmedIncr": 0,
        "curedIncr": 0,
        "confirmedIncr": 0,
        "suspectedIncr": 0,
        "deadIncr": 0
    },
    "domesticStatistics": {
        "currentConfirmedCount": 145,
        "curedCount": 79715,
        "confirmedCount": 84505,
        "seriousCount": 368,
        "suspectedCount": 1708,
        "deadCount": 4645,
        "currentConfirmedIncr": -2,
        "curedIncr": 7,
        "confirmedIncr": 5,
        "suspectedIncr": 1,
        "deadIncr": 0
    },
    "internationalStatistics": {
        "currentConfirmedCount": 2720062,
        "curedCount": 1723268,
        "confirmedCount": 4760912,
        "seriousCount": 0,
        "suspectedCount": 4,
        "deadCount": 317582,
        "currentConfirmedIncr": 0,
        "curedIncr": 0,
        "confirmedIncr": 0,
        "suspectedIncr": 0,
        "deadIncr": 0
    }
}

class StatisticsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        instance = Statistics()
        for key, value in TEST_DATA.items():
            value = json.dumps(value)
            setattr(instance, key, value)
        instance.save()

    def test_latest(self):
        response = self.client.get('/api/statistics/latest')
        self.assertEqual(response.status_code, 200)

        # response_content = json.loads(response.content)
        # user_url = response_content["url"]

        # response = self.client.get(user_url)
        # response_content = json.loads(response.content)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual("tom", response_content["username"])
        # self.assertEqual("tom@example.com", response_content["email"])