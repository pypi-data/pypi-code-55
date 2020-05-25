from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from address.models import AddressField, Address
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
        verbose_name=_('prime number'),
        default=uuid.uuid4,
        editable=False,
        help_text=_('prime number is unique code for any master data')
    )

    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
        blank=False,
        null=False,
        default=None,
        help_text=_('Humanized name of master data'),
    )

    def __str__(self) -> str:
        return self.name

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
        verbose_name=_('name prefix'),
        max_length=10,
        choices=NAME_PREFIX_CHOICES,
        default=None,
        blank=True,
        null=True
    )

    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=100,
        blank=False,
        null=False
    )

    middle_name = models.CharField(
        verbose_name=_('middle name'),
        max_length=100,
        default=None,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=100,
        blank=False,
        null=False
    )

    name_suffix = models.CharField(
        verbose_name=_('name suffix'),
        max_length=10,
        default=None,
        blank=True,
        null=True
    )

    @property
    def full_name(self):
        return "{prefix} {first} {middle} {last} {suffix}".format(
            prefix=str(self.name_prefix) if self.name_prefix is not None else '',
            suffix=str(self.name_suffix) if self.name_suffix is not None else '',
            first=str(self.first_name) if self.first_name is not None else '',
            middle=str(self.middle_name) if self.middle_name is not None else '',
            last=str(self.last_name if self.last_name is not None else '')
        ).title()

class PersonBirthDataMixin(models.Model):

    class Meta:
        abstract = True

    birthdate = models.DateField(
        verbose_name=_('birth date'),
        blank=False,
        null=False,
    )

    birthplace = models.CharField(
        verbose_name=_('birth place'),
        max_length=200,
        blank=False,
        null=False
    )

    name_of_mother = models.CharField(
        verbose_name=_('name of mother'),
        max_length=200,
        default=None,
        blank=False,
        null=False
    )


gender_female = 'female'
gender_male = 'male'
gender_choices = [
    (gender_female, _('Female')),
    (gender_male, _('Male')),
]

class TaxationModelMixin(models.Model):

    class Meta:
        abstract = True

    tax_number = models.CharField(
        verbose_name=_('tax number'),
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
        help_text=_('Has inland address.'),
        blank=False,
        null=False,
        default=True
    )


class SubAccount(BankAccountModelMixin):

    class Meta:
        verbose_name = _('sub account')


class DependenceQualityModel(MasterDataModel):

    class Meta:
        abstract = False
        verbose_name = _('dependence quality')
        verbose_name_plural = _('dependence qualities')

class DependenceLegitimacyModel(MasterDataModel):

    class Meta:
        abstract = False
        verbose_name = _('dependence legitimacy')
        verbose_name_plural = _('dependence legitimacies')

class LegalTypeModel(MasterDataModel):
    pass

class IntervalMixin(models.Model):

    class Meta:
        abstract = True

    begin = models.DateTimeField(
        verbose_name=_('begin'),
        default=timezone.now,
        blank=False,
        null=False
    )

    end = models.DateTimeField(
        verbose_name=_('end'),
        default=None,
        blank = True,
        null = True,
    )


class DependentModelMixin(models.Model):

    class Meta:
        abstract = True

    quality = models.ForeignKey(
        to=DependenceQualityModel,
        on_delete=models.CASCADE,
    )
    legitimacy = models.ForeignKey(
        to=DependenceLegitimacyModel,
        on_delete=models.CASCADE,
    )

class LegalModelMixin(models.Model):

    class Meta:
        abstract = True

class RecreationalCardModelMixin(models.Model):

    class Meta:
        abstract = True

    accomodation_subaccount = models.ForeignKey(
        verbose_name=_('accomodation subaccount'),
        to=SubAccount,
        related_name='accomodations',
        on_delete=models.CASCADE,
    )

    hospitality_subaccount = models.ForeignKey(
        verbose_name=_('hospitality subaccount'),
        to=SubAccount,
        related_name='hospitalities',
        on_delete=models.CASCADE,
    )

    leisure_subaccount = models.ForeignKey(
        verbose_name=_('leisure subaccount'),
        to=SubAccount,
        related_name='leisures',
        on_delete=models.CASCADE,
    )



class PersonModelManager(models.Manager):
    pass

class PersonModel(PersonBirthDataMixin, PersonRegistratNameMixin, NationalityModelMixin, TaxationModelMixin, MasterDataModel):

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')

    objects = PersonModelManager

    gender = models.CharField(
        verbose_name=_('gender'),
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

class BusinessFormModel(MasterDataModel):

    class Meta:
        verbose_name = _('business form')
        verbose_name_plural = _('business forms')


class OrganizationModel(MasterDataModel):

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')

    registration_number = models.CharField(
        verbose_name=_('registration_number'),
        max_length=500,
        blank=False,
        null=False
    )

    business_form = models.ForeignKey(
        verbose_name=_('business_form'),
        to=BusinessFormModel,
        related_name='organizations',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
