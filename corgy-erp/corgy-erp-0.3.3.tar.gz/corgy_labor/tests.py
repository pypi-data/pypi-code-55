from django.test import TestCase
import datetime
from . import models as labor_models
from corgy_mdm import models as mdm_models
from django.contrib.auth import models as auth_models
from django.utils import timezone

# Create your tests here.

class EmploymentModelTestCase(TestCase):
    """
    Unit tests of master data for employment.
    """

    def setUp(self):
        business_form = mdm_models.BusinessFormModel.objects.create(
            name='my-business-form'
        )

        organization = mdm_models.OrganizationModel.objects.create(
            name='test-org',
            business_form = business_form,
        )  # type:mdm_models.OrganizationModel
        self.organizationId = organization.pk

        permanent_address = mdm_models.Address()
        permanent_address.save()

        person = mdm_models.PersonModel.objects.create(
            name='test-person',
            birthdate=timezone.datetime(year=2020, month=1, day=2),
            name_of_mother='name of mother',
            permanent_address=permanent_address,
        )  # type: mdm_models.PersonModel
        self.personId = person.pk

    def test_create(self):
        """Test creation of default and minimal necessery data of employment master data model."""
        employment = labor_models.EmploymentModel.objects.create(
            person = mdm_models.PersonModel.objects.get(pk=self.personId),
            organization = mdm_models.OrganizationModel.objects.get(pk=self.organizationId),
        ) # type: mdm_models.EmploymentModel

        # self.assertIsNotNone(employment.pk)
