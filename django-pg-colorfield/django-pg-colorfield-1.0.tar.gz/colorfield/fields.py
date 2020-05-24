import json
import logging
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator

logger = logging.getLogger(__name__)


class ColorManager(models.Manager):
    def get_color(self, color):
        if type(color) == list:
            return color
        color = color.strip().lstrip('#')
        if color[0] == "[":
            return json.loads(color)
        if type(color[0]) == str:
            return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        raise Exception("Invalid data type of color.")

    def by_radius(self, *args, **kwargs):
        field = kwargs.pop("field")
        color = self.get_color(kwargs.pop("color"))
        radius = int(kwargs.pop("radius"))
        lower_str, upper_str = str(field)+"__{}__gte", str(field)+"__{}__lte"
        kwargs.update({lower_str.format(i): max(0, each-radius)
                       for i, each in enumerate(color)})
        kwargs.update({upper_str.format(i): min(255, each+radius)
                       for i, each in enumerate(color)})

        return super(ColorManager, self).filter(**kwargs)


class ColorField(ArrayField):

    def __init__(self, base_field=None, size=3, **kwargs):
        size = 3
        base_field = models.PositiveSmallIntegerField(
            validators=[MaxValueValidator(255), MinValueValidator(0)])
        super().__init__(base_field, size=size, **kwargs)

    @property
    def description(self):
        return 'Array of RGB Colors'
