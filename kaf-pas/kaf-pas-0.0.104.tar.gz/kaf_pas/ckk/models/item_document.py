import logging

from django.db.models import UniqueConstraint, Q
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditManager, AuditQuerySet, AuditModel

from kaf_pas.ckk.models.item import Item
from kaf_pas.kd.models.documents import Documents
from kaf_pas.kd.models.lotsman_documents_hierarcy import Lotsman_documents_hierarcy

logger = logging.getLogger(__name__)


class Item_documentQuerySet(AuditQuerySet):
    def delete(self):
        return super().delete()

    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Item_documentManager(AuditManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Item_documentQuerySet(self.model, using=self._db)


class Item_document(AuditModel):
    item = ForeignKeyProtect(Item)
    document = ForeignKeyProtect(Documents, verbose_name='Документ', null=True, blank=True)
    lotsman_document = ForeignKeyProtect(Lotsman_documents_hierarcy, verbose_name='Документ из Лоцмана', null=True, blank=True)

    objects = Item_documentManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс-таблица'
        constraints = [
            UniqueConstraint(fields=['item'], condition=Q(document=None) & Q(lotsman_document=None), name='Item_document_unique_constraint_0'),
            UniqueConstraint(fields=['document', 'item'], condition=Q(lotsman_document=None), name='Item_document_unique_constraint_1'),
            UniqueConstraint(fields=['item', 'lotsman_document'], condition=Q(document=None), name='Item_document_unique_constraint_2'),
            UniqueConstraint(fields=['document', 'item', 'lotsman_document'], name='Item_document_unique_constraint_3'),
        ]
