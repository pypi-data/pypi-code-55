from django.db import models
from django.db import connections
import sense_core as sd


class BaseModel0(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True

    @classmethod
    def find_map_by_ids(cls, ids):
        items = list(cls.objects.filter(id__in=ids))
        return {x.id: x for x in items}

    @classmethod
    def find_by_ids(cls, ids):
        map = cls.find_map_by_ids(ids)
        result = []
        for id in ids:
            if id in map:
                result.append(map[id])
        return result

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.filter(pk=id).first()

    @classmethod
    def find_many(cls, **kwargs):
        return cls.objects.filter(**kwargs).all()

    @classmethod
    def find_one_by(cls, **kwargs):
        return cls.objects.filter(**kwargs).first()


class BaseModel(BaseModel0):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


@sd.try_catch_exception
def close_model_connection():
    connections.close_all()
    sd.log_info("close_all connections")
