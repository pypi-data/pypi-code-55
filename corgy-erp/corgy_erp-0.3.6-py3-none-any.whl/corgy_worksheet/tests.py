from django.test import TestCase
import datetime
from corgy_worksheet import models as corgy_worksheet_models
from corgy_mdm import models as mdm_models
from django.utils import timezone

# Create your tests here.

class WorksheetModelTestCase(TestCase):

    def setUp(self):
        permanent_address = mdm_models.Address()
        permanent_address.save()
        person = mdm_models.PersonModel.objects.create(
            name='test-person',
            birthdate=timezone.datetime(year=2020, month=1, day=2),
            name_of_mother='name of mother',
            permanent_address=permanent_address,
        )  # type: mdm_models.PersonModel
        worksheet1 = corgy_worksheet_models.WorksheetModel.objects.create(owner=person)
        worksheet2 = corgy_worksheet_models.WorksheetModel.objects.create(owner=person)
        entry1_day1 = corgy_worksheet_models.WorksheetEntryModel.objects.create(
            worksheet = worksheet1,
            timestamp = timezone.datetime(year=2020, month=10, day=1),
            duration = timezone.timedelta(minutes=1)
        )
        entry1_day2 = corgy_worksheet_models.WorksheetEntryModel.objects.create(
            worksheet=worksheet1,
            timestamp=timezone.datetime(year=2020, month=10, day=1),
            duration=timezone.timedelta(minutes=10)
        )
        entry2_day2 = corgy_worksheet_models.WorksheetEntryModel.objects.create(
            worksheet=worksheet2,
            timestamp=timezone.datetime(year=2020, month=10, day=2),
            duration=timezone.timedelta(minutes=2)
        )

        self.worksheet1_id = worksheet1.pk
        self.worksheet2_id = worksheet2.pk

    def test_daily_summary(self):
        """Animals that can speak are correctly identified"""
        worksheet1 = corgy_worksheet_models.WorksheetModel.objects.get(pk=self.worksheet1_id) #type: corgy_worksheet_models.WorksheetModel
        worksheet2 = corgy_worksheet_models.WorksheetModel.objects.get(pk=self.worksheet2_id)
        self.assertEqual(worksheet1.daily_summary(timezone.datetime(year=2020, month=10, day=1)), timezone.timedelta(minutes=11))
        pass


class WorksheetEntryModelTestCase(TestCase):

    def setUp(self):
        permanent_address = mdm_models.Address()
        permanent_address.save()
        person = mdm_models.PersonModel.objects.create(
            name='test-person',
            birthdate=timezone.datetime(year=2020, month=1, day=2),
            name_of_mother='name of mother',
            permanent_address=permanent_address,
        )  # type: mdm_models.PersonModel
        worksheet = corgy_worksheet_models.WorksheetModel.objects.create(owner=person)
        entry_day1_1 = corgy_worksheet_models.WorksheetEntryModel.objects.create(worksheet=worksheet)
        entry_day2_1 = corgy_worksheet_models.WorksheetEntryModel.objects.create(worksheet=worksheet)
        entry_day2_2 = corgy_worksheet_models.WorksheetEntryModel.objects.create(worksheet=worksheet)

    def test_create(self):
        """Animals that can speak are correctly identified"""
        # lion = Animal.objects.get(name="lion")
        # cat = Animal.objects.get(name="cat")
        # self.assertEqual(lion.speak(), 'The lion says "roar"')
        # self.assertEqual(cat.speak(), 'The cat says "meow"')
        pass
