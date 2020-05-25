from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone
import datetime
from django.utils.translation import ugettext_lazy as _
from corgy_mdm import models as mdm_models
# Create your models here.

class ActivityModel(models.Model):

    class Meta:
        verbose_name = _('activity')

    name = models.CharField(
        max_length=100,
        default='work'
    )

class WorksheetModel(models.Model):

    class Meta:
        verbose_name = _('worksheet')

    owner = models.ForeignKey(
        to=mdm_models.PersonModel,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.owner)

    def daily_entries(self, timestamp: datetime.datetime):
        return self.entries.filter(
            worksheet = self,
            timestamp__year = timestamp.year,
            timestamp__month = timestamp.month,
            timestamp__day = timestamp.day
        )

    def daily_summary(self, timestamp: timezone.datetime):
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
