from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from address.models import AddressField
from phonenumber_field.modelfields import PhoneNumberField
import uuid

# Create your models here.
# class TaggingMixin(object):
#     tag = models.ForeignKey(Tag)
#
#     class Meta:
#         abstract = True



class BankAccountModelMixin(models.Model):

    class Meta:
        abstract = True

    bank_account_number = models.CharField(
        verbose_name=_('bank account number'),
        help_text=_('Please provide bank account number as a form of xxxxxxxx-xxxxxxxx-xxxxxxxx'),
        max_length=24
    )

class MasterDataModel(models.Model):

    class Meta:
        abstract = True

    prime_number = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('prime number'),
        help_text=_('prime number is unique code for any master data')
    )

    name = models.CharField(
        verbose_name=_('name'),
        help_text=_('Humanized name of master data'),
        max_length=100,
        blank=False,
        null=False,
        default=None
    )

NAME_PREFIX_CHOICES = [
    ('junior', _('Junior')),
    ('senior', _('Senior')),
    ('doctor', _('Doctor')),
    ('professor', _('Professor')),
    ('widow', _('Widow')),
]

class PersonRegistratNameMixin(models.Model):

    class Meta:
        abstract = True

    name_prefix = models.CharField(
        max_length=10,
        choices=NAME_PREFIX_CHOICES,
        default=None,
        blank=True,
        null=True
    )

    first_name = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    middle_name = models.CharField(
        max_length=100,
        default=None,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    name_suffix = models.CharField(
        max_length=10,
        default=None,
        blank=True,
        null=True
    )

    @property
    def full_name(self):
        return "{prefix} {first} {middle} {last} {suffix}".format(
            prefix=str(self.name_prefix),
            suffix=str(self.name_suffix),
            first=str(self.first_name),
            middle=str(self.middle_name),
            last=str(self.last_name)
        ).title()

class PersonBirthDataMixin(models.Model):

    class Meta:
        abstract = True

    birthdate = models.DateField(
        blank=False,
        null=False
    )

    birthplace = models.CharField(
        max_length=200,
        blank=False,
        null=False
    )

    name_of_mother = models.CharField(
        max_length=200,
        default=None,
        blank=False,
        null=False
    )


gender_female = 'female'
gender_male = 'male'
gender_choices = [
    (gender_female, 'Female'),
    (gender_male, 'Male'),
]

class TaxationModelMixin(models.Model):

    class Meta:
        abstract = True

    tax_number = models.CharField(
        max_length=100
    )


class NationalityModelMixin(models.Model):
    class Meta:
        abstract = True

    primary = models.CharField(
        verbose_name=_('nationality'),
        max_length=100
    )

    inland_resident = models.BooleanField(
        verbose_name=_('has inland residence'),
        help_text=_('Has inland address.')
    )


class PersonModel(PersonBirthDataMixin, PersonRegistratNameMixin, NationalityModelMixin, TaxationModelMixin, MasterDataModel):

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')

    gender = models.CharField(
        choices=gender_choices,
        max_length=10,
        default=None,
        blank=True,
        null=True
    )

    permanent_address = AddressField(
        verbose_name=_('permanent address'),
        help_text=_('Permanent address, desc.'),
        related_name='permanent_residents',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    temporary_address = AddressField(
        verbose_name=_('temporary address'),
        help_text=_('temporary address, desc.'),
        related_name='termorary_residents',
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE
    )

    phone_number = PhoneNumberField(
        verbose_name=_('phone number'),
        help_text=_('Phone number, desc.'),
        blank=False,
        null=False,
    )

    email = models.EmailField(
        verbose_name=_('email'),
        help_text=_('Primary email address')
    )

    def __str__(self):
        return str(self.full_name)

class OrganizationModel(MasterDataModel):

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')

    registration_number = models.CharField(
        max_length=500,
        blank=False,
        null=False
    )

class EmploymentModel(MasterDataModel):

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    person = models.ForeignKey(
        to=PersonModel,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    organization = models.ForeignKey(
        to=OrganizationModel,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    begin = models.DateTimeField(
        default=timezone.now,
        blank=False,
        null=False
    )

    end = models.DateTimeField(
        default=None,
        blank = True,
        null = True,
    )