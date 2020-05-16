from django.db import models
from django.utils import timezone
# Create your models here.
# class TaggingMixin(object):
#     tag = models.ForeignKey(Tag)
#
#     class Meta:
#         abstract = True

class PersonRegistratNameMixin(object):

    class Meta:
        abstract = True

    name_prefix = models.CharField(
        max_length=10,
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
            prefix=self.name_prefix,
            suffix=self.name_suffix,
            first=self.first_name,
            middle=self.middle_name,
            last=self.last_name
        )

class PersonBirthDataMixin(object):

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

class TaxationModel(models.Model):
    tax_number = models.CharField(
        max_length=100
    )

class PersonModel(models.Model, PersonBirthDataMixin, PersonRegistratNameMixin):

    gender = models.CharField(
        choices=gender_choices,
        max_length=10,
        default=None,
        blank=True,
        null=True
    )

class OrganizationModel(models.Model):

    name = models.CharField(
        max_length=500,
        blank=False,
        null=False
    )

    registration_number = models.CharField(
        max_length=500,
        blank=False,
        null=False
    )

class EmploymentModel(models.Model):

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