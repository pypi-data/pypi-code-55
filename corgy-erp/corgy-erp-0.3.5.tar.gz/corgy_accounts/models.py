from django.db import models

# Create your models here.

class AccountModel(models.Model):
    pass

class AccountPropertyModel(models.Model):

    name = models.TextField(
        max_length=100
    )

    value = models.TextField(
        max_length=100
    )
    account = models.ForeignKey(
        default=None,
        null=True,
        blank=True,
        to=AccountModel,
        on_delete=models.CASCADE,
    )


