from django.db import models

# Create your models here.
class Icon(models.Model):
    name = models.CharField(max_length=30, blank=True)
    width = models.IntegerField(default=60)
    height = models.IntegerField(default=60)

    def __str__(self):
        return self.name
