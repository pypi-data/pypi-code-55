from django.db import models


class Country(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    iso3 = models.CharField(max_length=3, null=True)
    iso2 = models.CharField(max_length=2, null=True)
    phone_code = models.CharField(max_length=15, null=True)
    currency = models.CharField(max_length=3, null=True)

    class Meta:
        permissions = (
            ('list_country', 'Can list countries'),
        )


class State(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='states')
    name = models.CharField(max_length=200)
    state_code = models.CharField(max_length=3, null=True)

    class Meta:
        permissions = (
            ('list_state', 'Can list states'),
        )


class City(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT, related_name='cities')
    name = models.CharField(max_length=200)

    class Meta:
        permissions = (
            ('list_city', 'Can list cities'),
        )
