from django.test import TestCase
import datetime
# Create your tests here.
from corgy_worksheet import models as corgy_worksheet_models
from django.contrib.auth import models as auth_models

class WorksheetModelTestCase(TestCase):

    def setUp(self):
        user = auth_models.User.objects.create_superuser(
            username='user',
            password='qwe123',
            email='user@gmail.com'
        )
        worksheet1 = corgy_worksheet_models.WorksheetModel.objects.create(owner=user)
        worksheet2 = corgy_worksheet_models.WorksheetModel.objects.create(owner=user)
        entry1_day1 = corgy_worksheet_models.WorksheetEntryModel.objects.create(
            worksheet = worksheet1,
            timestamp = datetime.datetime(year=2020, month=10, day=1),
            duration = datetime.timedelta(minutes=1)
        )
        entry1_day2 = corgy_worksheet_models.WorksheetEntryModel.objects.create(
            worksheet=worksheet1,
            timestamp=datetime.datetime(year=2020, month=10, day=1),
            duration=datetime.timedelta(minutes=10)
        )
        entry2_day2 = corgy_worksheet_models.WorksheetEntryModel.objects.create(
            worksheet=worksheet2,
            timestamp=datetime.datetime(year=2020, month=10, day=2),
            duration=datetime.timedelta(minutes=2)
        )

        self.worksheet1_id = worksheet1.pk
        self.worksheet2_id = worksheet2.pk

    def test_daily_summary(self):
        """Animals that can speak are correctly identified"""
        worksheet1 = corgy_worksheet_models.WorksheetModel.objects.get(pk=self.worksheet1_id) #type: corgy_worksheet_models.WorksheetModel
        worksheet2 = corgy_worksheet_models.WorksheetModel.objects.get(pk=self.worksheet2_id)
        self.assertEqual(worksheet1.daily_summary(datetime.datetime(year=2020, month=10, day=1)), datetime.timedelta(minutes=11))
        #self.assertEqual(worksheet1.daily_summary(datetime.datetime(year=2020, month=10, day=2)), datetime.timedelta(minutes=2))
        pass


class WorksheetEntryModelTestCase(TestCase):

    def setUp(self):
        user = auth_models.User.objects.create_superuser(
            username='user',
            password='qwe123',
            email='user@gmail.com'
        )
        worksheet = corgy_worksheet_models.WorksheetModel.objects.create(owner=user)
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
