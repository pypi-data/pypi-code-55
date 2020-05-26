import logging

from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet

from kaf_pas.kd.models.documents import Documents
from kaf_pas.kd.models.uploades import Uploades, UploadesManager

logger = logging.getLogger(__name__)


class Uploades_documentsQuerySet(AuditQuerySet):
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Uploades_documentsManager(AuditManager):

    def deleteFromRequest(self, request, removed=None, ):
        from isc_common.auth.models.user import User

        ids = request.GET.getlist('ids')
        user = User.objects.get(username=request.GET.get('ws_channel').split('_')[1])

        res = 0
        doc_cnt = 0
        lotsman_cnt = 0

        for i in range(0, len(ids), 2):
            id = ids[i]
            visibleMode = ids[i + 1]

            if visibleMode != "none":
                res += super().filter(id=id).soft_delete(visibleMode=visibleMode)
            else:
                res, _doc_cnt, _lotsman_cnt = UploadesManager.del_upload(
                    id=Uploades_documents.objects.get(id=id).upload.id,
                    document_id=id,
                    user=user,
                    doc_cnt=doc_cnt,
                    last_step=len(ids) / 2 == i,
                    lotsman_cnt=lotsman_cnt
                )
                doc_cnt += _doc_cnt
                lotsman_cnt += _lotsman_cnt
        return res

    @staticmethod
    def getRecord(record):
        document_view = record.document_view
        res = {
            'id': record.id,
            'document_id': record.document.id,
            'document__path_id': record.document.path.id,
            'document__attr_type_id': record.document.attr_type.id,
            'document__attr_type__code': record.document.attr_type.code,
            'document__attr_type__name': record.document.attr_type.name,
            'document__file_document': record.document.file_document,
            'document__file_size': record.document.file_size,
            'document__lastmodified': record.document.lastmodified,
            'document__file_modification_time': record.document.file_modification_time,
            'document__file_access_time': record.document.file_access_time,
            'document__file_change_time': record.document.file_change_time,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Uploades_documentsQuerySet(self.model, using=self._db)


class Uploades_documents(AuditModel):
    upload = ForeignKeyProtect(Uploades)
    document = ForeignKeyProtect(Documents)

    objects = Uploades_documentsManager()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        unique_together = (('upload', 'document'),)
