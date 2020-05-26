import logging

from bitfield import BitField
from django.db.models import PositiveIntegerField

from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_qty import Item_qtyManager
from kaf_pas.kd.models.document_attributes import Document_attributes

logger = logging.getLogger(__name__)


class Item_qty_viewQuerySet(AuditQuerySet):
    def delete(self):
        return super().delete()

    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Item_qty_viewManager(AuditManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
            'qty': record.qty,
            'lastmodified': record.lastmodified,
            "STMP_1_id": record.STMP_1.id if record.STMP_1 else None,
            "STMP_1__value_str": record.STMP_1.value_str if record.STMP_1 else None,
            "STMP_2_id": record.STMP_2.id if record.STMP_2 else None,
            "STMP_2__value_str": record.STMP_2.value_str if record.STMP_2 else None,
        }
        return res

    def get_queryset(self):
        return Item_qty_viewQuerySet(self.model, using=self._db)


class Item_qty_view(AuditModel):
    STMP_1 = ForeignKeyProtect(Document_attributes, verbose_name='Наименование изделия', related_name='STMP_1_qty_view', null=True, blank=True)
    STMP_2 = ForeignKeyProtect(Document_attributes, verbose_name='Обозначение изделия', related_name='STMP_2_qty_view', null=True, blank=True)
    child = ForeignKeyProtect(Item, related_name='Item_qty_view_child')
    parent = ForeignKeyProtect(Item, related_name='Item_qty_view_parent', blank=True, null=True)
    qty = PositiveIntegerField()
    props = Item_qtyManager.get_prop()

    objects = Item_qty_viewManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Количество элементов'
        managed = False
        db_table = 'ckk_item_qty_view'
