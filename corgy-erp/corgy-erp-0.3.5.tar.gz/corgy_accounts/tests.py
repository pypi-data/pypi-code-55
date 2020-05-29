from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from corgy_accounts import models as corgy_accounts_models

class AccountModelTestCase(TestCase):
    def setUp(self):
        corgy_accounts_models.AccountModel.objects.create()
        corgy_accounts_models.AccountModel.objects.create()

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        # lion = Animal.objects.get(name="lion")
        # cat = Animal.objects.get(name="cat")
        # self.assertEqual(lion.speak(), 'The lion says "roar"')
        # self.assertEqual(cat.speak(), 'The cat says "meow"')
        pass