from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone
import datetime

# Create your models here.

class ActivityModel(models.Model):
    name = models.CharField(
        max_length=100,
        default='work'
    )

class WorksheetModel(models.Model):
    owner = models.ForeignKey(
        to=auth_models.User,
        on_delete=models.CASCADE
    )

    def daily_entries(self, timestamp: datetime.datetime):
        return self.entries.filter(
            worksheet = self,
            timestamp__year = timestamp.year,
            timestamp__month = timestamp.month,
            timestamp__day = timestamp.day
        )

    def daily_summary(self, timestamp: datetime.datetime):
        return self.entries.aggregate(daily_work = models.Sum('duration'))['daily_work'] #type:

class WorksheetEntryModel(models.Model):
    worksheet = models.ForeignKey(
        to=WorksheetModel,
        related_name='entries',
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        blank=False,
        null=False
    )
    duration = models.DurationField(
        default=datetime.timedelta()
    )
    note = models.CharField(
        max_length=100,
        default=None,
        blank=True,
        null=True
    )
    activity = models.ForeignKey(
        to = ActivityModel,
        related_name='logged_entries',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )
