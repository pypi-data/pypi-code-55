import logging

from bitfield import BitField
from django.conf import settings
from django.db import transaction
from isc_common.bit import TurnBitOn
from isc_common.common import blinkString
from isc_common.common.mat_views import refresh_mat_view
from isc_common.datetime import DateTimeToStr
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from isc_common.number import DelProps
from isc_common.progress import managed_progress, ProgressDroped

from kaf_pas.kd.models.pathes import Pathes
from kaf_pas.production.models import progress_deleted

logger = logging.getLogger(__name__)


class UploadesQuerySet(AuditQuerySet):
    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class UploadesManager(AuditManager):

    @staticmethod
    def props():
        return BitField(flags=(
            ('confirmed', 'Подтверждено'),
        ), default=0, db_index=True)

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'lastmodified': record.lastmodified,
            'path_id': record.path.id,
            'absolute_path': record.path.absolute_path,
            'editing': record.editing,
            'deliting': record.deliting,
            'props': record.props,
            'confirmed': record.props.confirmed,
        }
        return DelProps(res)

    def get_queryset(self):
        return UploadesQuerySet(self.model, using=self._db)

    @staticmethod
    def del_upload(id, user, doc_cnt=0, lotsman_cnt=0, document_id=None, last_step=False):
        from isc_common.models.deleted_progresses import Deleted_progresses
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.ckk.models.item import ItemManager
        from kaf_pas.ckk.models.item_document import Item_document
        from kaf_pas.ckk.models.item_image_refs import Item_image_refs
        from kaf_pas.kd.models.document_attr_cross import Document_attr_cross
        from kaf_pas.kd.models.documents import Documents
        from kaf_pas.kd.models.documents_history import Documents_history
        from kaf_pas.kd.models.documents_thumb import Documents_thumb
        from kaf_pas.kd.models.documents_thumb10 import Documents_thumb10
        from kaf_pas.kd.models.lotsman_document_attr_cross import Lotsman_document_attr_cross
        from kaf_pas.kd.models.lotsman_documents_hierarcy import Lotsman_documents_hierarcy
        from kaf_pas.kd.models.lotsman_documents_hierarcy_files import Lotsman_documents_hierarcy_files
        from kaf_pas.kd.models.lotsman_documents_hierarcy_refs import Lotsman_documents_hierarcy_refs
        from kaf_pas.kd.models.uploades_documents import Uploades_documents
        from kaf_pas.kd.models.uploades_log import Uploades_log

        if settings.LOCKS.locked(f'UploadesManager.del_upload_{id}'):
            return

        settings.LOCKS.acquire(f'UploadesManager.del_upload_{id}')

        if document_id == None:
            for upload_document in Uploades_documents.objects.filter(upload_id=id):
                lotsman_cnt += Lotsman_documents_hierarcy.objects.filter(document=upload_document.document).count()
        else:
            lotsman_cnt = Lotsman_documents_hierarcy.objects.filter(document_id=document_id).count()

        upload = Uploades.objects.get(id=id)

        if document_id != None:
            upload_document = Uploades_documents.objects.get(id=document_id)

        qty = Uploades_documents.objects.filter(upload_id=id).count() + lotsman_cnt if document_id == None else 1 + lotsman_cnt
        with managed_progress(
                qty=qty,
                id=f'Remove_upload_{id}',
                user=user,
                message=f'Удаление закачки: {upload.path.drived_absolute_path} от {DateTimeToStr(upload.lastmodified)}' if document_id == None else f'Удаление документа: {upload_document.document.file_document}',
                title='Выполнено',
                props=TurnBitOn(0, 0)
        ) as progress:
            try:
                res = 0
                with transaction.atomic():
                    continue_cnt = 0

                    if document_id == None:
                        upload_query = Uploades_documents.objects.select_for_update().filter(upload_id=id)
                    else:
                        upload_query = Uploades_documents.objects.select_for_update().filter(id=document_id)

                    for upload_document in upload_query:

                        _continue = False
                        for item in Item.objects.filter(document=upload_document.document):
                            if ItemManager.delete_recursive(item_id=item.id, delete_lines=True, user=user, props=0, document=upload_document.document, show_progress=True) == 2:
                                _continue = True
                                continue_cnt += 1
                                break
                            else:
                                item.delete()

                        if _continue:
                            continue

                        deleted = Document_attr_cross.objects.filter(document=upload_document.document).delete()
                        # logger.debug(f'deleted: {deleted}')

                        for documents_history in Documents_history.objects.filter(new_document=upload_document.document):
                            documents_history.old_document.props |= Documents.props.relevant
                            documents_history.old_document.save()
                            deleted = documents_history.delete()
                            # logger.debug(f'deleted: {deleted}')

                        for thumb in Documents_thumb.objects.filter(document=upload_document.document):
                            Item_image_refs.objects.filter(thumb=thumb).delete()
                            deleted = thumb.delete()
                            # logger.debug(f'deleted: {deleted}')

                        for thumb10 in Documents_thumb10.objects.filter(document=upload_document.document):
                            Item_image_refs.objects.filter(thumb10=thumb10).delete()
                            deleted = thumb10.delete()
                            # logger.debug(f'deleted: {deleted}')

                        for lotsman_document in Lotsman_documents_hierarcy.objects.filter(document=upload_document.document):

                            for item in Item.objects.filter(lotsman_document=lotsman_document):
                                if ItemManager.delete_recursive(item_id=item.id, delete_lines=True, user=user, props=0, document=lotsman_document, show_progress=True) == 2:
                                    _continue = True
                                    continue_cnt += 1
                                    break
                                else:
                                    Item_document.objects.filter(item=item).delete()
                                    item.delete()

                            if _continue:
                                break

                            deleted = Lotsman_document_attr_cross.objects.filter(document=lotsman_document).delete()
                            # logger.debug(f'deleted: {deleted}')
                            deleted = Lotsman_document_attr_cross.objects.filter(parent_document=lotsman_document).delete()
                            # logger.debug(f'deleted: {deleted}')
                            deleted = Lotsman_documents_hierarcy_refs.objects.filter(child=lotsman_document).delete()
                            # logger.debug(f'deleted: {deleted}')
                            deleted = Lotsman_documents_hierarcy_refs.objects.filter(parent=lotsman_document).delete()
                            # logger.debug(f'deleted: {deleted}')

                            for thumb in Documents_thumb.objects.filter(lotsman_document=lotsman_document):
                                Item_image_refs.objects.filter(thumb=thumb).delete()
                                deleted = thumb.delete()
                                # logger.debug(f'deleted: {deleted}')

                            for thumb10 in Documents_thumb10.objects.filter(lotsman_document=lotsman_document):
                                Item_image_refs.objects.filter(thumb10=thumb10).delete()
                                deleted = thumb10.delete()
                                # logger.debug(f'deleted: {deleted}')

                            Lotsman_documents_hierarcy_files.objects.filter(lotsman_document=lotsman_document).delete()
                            deleted = lotsman_document.delete()
                            # logger.debug(f'deleted: {deleted}')
                            lotsman_cnt += 1
                            if progress.step() != 0:
                                raise ProgressDroped(progress_deleted)

                        if _continue:
                            continue

                        # logger.debug(f'deleted: {deleted}')
                        Uploades_documents.objects.filter(document=upload_document.document).delete()
                        Item_document.objects.filter(document=upload_document.document).delete()
                        Documents.objects.filter(id=upload_document.document.id).delete()

                        doc_cnt += 1
                        # logger.debug('Done.')
                        if progress.step() != 0:
                            raise ProgressDroped(progress_deleted)

                    if continue_cnt == 0:
                        deleted = Uploades_log.objects.filter(upload_id=id).delete()
                        # logger.debug(f'deleted: {deleted}')
                        if document_id == None:
                            res += Uploades.objects.filter(id=id).delete()[0]

                if doc_cnt > 0 and last_step:
                    progress.setContentsLabel(blinkString(text='Обновление представления "kd_documents_mview"', color='blue'))
                    refresh_mat_view('kd_documents_mview')

                if lotsman_cnt > 0 and last_step:
                    progress.setContentsLabel(blinkString(text='Обновление представления "kd_lotsman_documents_hierarcy_mview"', color='blue'))
                    refresh_mat_view('kd_lotsman_documents_hierarcy_mview')

                settings.LOCKS.release(f'UploadesManager.del_upload_{id}')
                return res, doc_cnt, lotsman_cnt
            except ProgressDroped as ex:
                Deleted_progresses.objects.filter(id_progress=progress.id, user=progress.user).delete()
                settings.LOCKS.release(f'UploadesManager.del_upload_{id}')
                raise ex

            except Exception as ex:
                settings.LOCKS.release(f'UploadesManager.del_upload_{id}')
                raise ex

    def deleteFromRequest(self, request):
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
                    id=id,
                    user=user,
                    doc_cnt=doc_cnt,
                    last_step=len(ids) / 2 == i,
                    lotsman_cnt=lotsman_cnt
                )
                doc_cnt += _doc_cnt
                lotsman_cnt += _lotsman_cnt
        return res

    def confirmationFromRequest(self, request):
        from isc_common.http.DSRequest import DSRequest

        request = DSRequest(request=request)
        data = request.get_data()
        user = request.user

        res = self.change_confirm(data=data, user=user)

        return dict(res=res)

    def change_confirm(self, data, user, kind='confirm'):
        from kaf_pas.kd.models.uploades_documents import Uploades_documents
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.kd.models.lotsman_documents_hierarcy import Lotsman_documents_hierarcy

        res = 0

        if isinstance(data.get('ids'), list):
            with managed_progress(
                    id=f'confirm_{user.id}' if kind == 'confirm' else f'unconfirm_{user.id}',
                    qty=0,
                    user=user,
                    message='Подсчет товарных позиций',
                    props=TurnBitOn(0, 0)
            ) as progress:
                try:
                    with transaction.atomic():
                        for upload in Uploades.objects.select_for_update().filter(id__in=data.get('ids')):
                            for uploades_document in Uploades_documents.objects.filter(upload=upload):
                                res += Item.objects.filter(document=uploades_document.document).count()

                                for lotsman_documents_hierarcy in Lotsman_documents_hierarcy.objects.filter(document=uploades_document.document):
                                    res += Item.objects.filter(lotsman_document=lotsman_documents_hierarcy).count()

                            if res == 0:
                                raise Exception(f'Товарных позиций не найдено.')

                            progress.setQty(qty=res)
                            if kind == 'confirm':
                                progress.setContentsLabel(content=blinkString(f'Подтверждение закачки {upload.path.drived_absolute_path} от {DateTimeToStr(upload.lastmodified, hours=3)}', blink=False, bold=True))
                            else:
                                progress.setContentsLabel(content=blinkString(f'Отмена Подтверждения закачки {upload.path.drived_absolute_path} от {DateTimeToStr(upload.lastmodified, hours=3)}', blink=False, bold=True))
                            for uploades_document in Uploades_documents.objects.filter(upload=upload):
                                for item in Item.objects.filter(document=uploades_document.document):
                                    if kind == 'confirm':
                                        item.props |= Item.props.confirmed
                                    else:
                                        item.props &= ~Item.props.confirmed
                                    item.save()
                                    if progress.step() != 0:
                                        raise ProgressDroped

                                for lotsman_documents_hierarcy in Lotsman_documents_hierarcy.objects.filter(document=uploades_document.document):
                                    for item in Item.objects.filter(lotsman_document=lotsman_documents_hierarcy):
                                        if kind == 'confirm':
                                            item.props |= Item.props.confirmed
                                        else:
                                            item.props &= ~Item.props.confirmed
                                        item.save()
                                        if progress.step() != 0:
                                            raise ProgressDroped

                            if kind == 'confirm':
                                upload.props |= Uploades.props.confirmed
                            else:
                                upload.props &= ~Uploades.props.confirmed
                            upload.save()
                        progress.sendMessage(type='refresh_uploads_grid')
                except ProgressDroped as ex:
                    from isc_common.models.deleted_progresses import Deleted_progresses
                    Deleted_progresses.objects.filter(id_progress=progress.id, user=progress.user).delete()
                    raise ex

        return res

    def unConfirmationFromRequest(self, request):
        from isc_common.http.DSRequest import DSRequest

        request = DSRequest(request=request)
        data = request.get_data()
        user = request.user

        res = self.change_confirm(data=data, user=user, kind='unconfirm')

        return dict(res=res)


class Uploades(AuditModel):
    path = ForeignKeyProtect(Pathes)

    props = UploadesManager.props()

    objects = UploadesManager()

    def __str__(self):
        return f"{self.id}, path: [{self.path}]"

    class Meta:
        verbose_name = 'Загрузки внешних данных'
