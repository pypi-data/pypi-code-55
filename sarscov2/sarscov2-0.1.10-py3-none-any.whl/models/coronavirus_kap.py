from django.conf import settings
from django.db import models
from edc_crf.crf_status_model_mixin import CrfStatusModelMixin
from edc_model import models as edc_models
from edc_model.models import HistoricalRecords
from edc_model.validators import datetime_not_future
from edc_protocol.validators import datetime_not_before_study_start
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from ..choices import COLLECTION_METHOD_CHOICES
from ..constants import IN_PERSON
from ..model_mixins import CoronaKapModelMixin, CoronaKapDiseaseModelMixin


class CoronaKapManager(models.Manager):

    use_in_migrations = True

    def get_by_natural_key(self, screening_identifier):
        return self.get(screening_identifier=screening_identifier)


class CoronavirusKap(
    CoronaKapDiseaseModelMixin,
    CoronaKapModelMixin,
    CrfStatusModelMixin,
    SiteModelMixin,
    edc_models.BaseUuidModel,
):

    subject_identifier = models.CharField(
        max_length=50, unique=True, verbose_name="Subject identifier", null=True,
    )

    screening_identifier = models.CharField(
        max_length=50, unique=True, verbose_name="Screening identifier", null=True,
    )

    collection_method = models.CharField(
        verbose_name="How was this information collected?",
        max_length=25,
        choices=COLLECTION_METHOD_CHOICES,
        default=IN_PERSON,
    )

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[datetime_not_before_study_start, datetime_not_future],
        default=get_utcnow,
        help_text=(
            "If reporting today, use today's date/time, otherwise use "
            "the date/time this information was reported."
        ),
    )

    protocol = models.CharField(max_length=50, default=settings.APP_NAME,)

    on_site = CurrentSiteManager()

    objects = CoronaKapManager()

    history = HistoricalRecords()

    def __str__(self):
        return self.screening_identifier

    class Meta:
        verbose_name = "Coronavirus KAP"
        verbose_name_plural = "Coronavirus KAP"
