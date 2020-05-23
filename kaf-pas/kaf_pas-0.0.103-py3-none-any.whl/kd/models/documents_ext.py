import logging
import os

from django.db import transaction, IntegrityError
from isc_common import setAttr
from isc_common.common.functions import delete_dbl_spaces

from kaf_pas.kd.models.document_attributes_view import Document_attributes_view

logger = logging.getLogger(__name__)


class DocumentManagerExt:

    def __init__(self, logger):
        self.logger = logger

    def rec_image_cwd(self, item_id, STMP_2):
        from kaf_pas.ckk.models.item_image_refs import Item_image_refs
        from kaf_pas.ckk.models.item import Item
        for item_image in Item_image_refs.objects.select_related('item').filter(
                item__props__in=[~Item.props.relevant & Item.props.from_cdw, ~Item.props.relevant & Item.props.from_pdf],
                item__STMP_2__value_str__delete_dbl_spaces=STMP_2):
            _, created = Item_image_refs.objects.get_or_create(
                item_id=item_id,
                thumb_id=item_image.thumb_id,
                thumb10_id=item_image.thumb10_id
            )

    def link_image_to_item(self, item):
        from kaf_pas.ckk.models.item_image_refs import Item_image_refs
        from kaf_pas.kd.models.documents_thumb import Documents_thumb
        from kaf_pas.kd.models.documents_thumb10 import Documents_thumb10

        document = item.document
        if document != None:
            for document_thumb in Documents_thumb.objects.filter(document=document):
                Item_image_refs.objects.get_or_create(item=item, thumb=document_thumb)

            for document_thumb10 in Documents_thumb10.objects.filter(document=document):
                Item_image_refs.objects.get_or_create(item=item, thumb10=document_thumb10)

    def link_image_to_lotsman_item(self, lotsman_document, item):
        from kaf_pas.ckk.models.item_image_refs import Item_image_refs
        from kaf_pas.kd.models.documents_thumb import Documents_thumb
        from kaf_pas.kd.models.documents_thumb10 import Documents_thumb10

        if lotsman_document != None:
            for document_thumb in Documents_thumb.objects.filter(lotsman_document_id=lotsman_document.id):
                Item_image_refs.objects.get_or_create(item=item, thumb=document_thumb)

            for document_thumb10 in Documents_thumb10.objects.filter(lotsman_document_id=lotsman_document.id):
                Item_image_refs.objects.get_or_create(item=item, thumb10=document_thumb10)

    def make_spw(self, document):
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.kd.models.documents import Documents
        from kaf_pas.system.models.contants import Contants
        from kaf_pas.ckk.models.item import ItemManager
        from kaf_pas.kd.models.spw_attrs import Spw_attrsQuerySet
        from kaf_pas.kd.models.document_attributes import Document_attributes
        from kaf_pas.kd.models.document_attr_cross import Document_attr_cross
        from kaf_pas.ckk.models.item_line import Item_line
        from kaf_pas.ckk.models.item_document import Item_document

        top_level = Contants.objects.get(code='audo_top_level')

        with transaction.atomic():
            if document.file_document.lower().find('мусор') == -1:

                try:
                    STMP_1 = Document_attributes_view.objects.get(document=document, attr_type__code='STMP_1')
                except Document_attributes_view.DoesNotExist:
                    STMP_1 = None
                except Document_attributes_view.MultipleObjectsReturned:
                    STMP_1 = Document_attributes_view.objects.filter(document=document, attr_type__code='STMP_1')[0]

                try:
                    STMP_2 = Document_attributes_view.objects.get(document=document, attr_type__code='STMP_2')
                except Document_attributes_view.DoesNotExist:
                    STMP_2 = None
                except Document_attributes_view.MultipleObjectsReturned:
                    STMP_2 = Document_attributes_view.objects.filter(document=document, attr_type__code='STMP_2')[0]

                if STMP_1 != None or STMP_2 != None:
                    props = Item.props.relevant | Item.props.from_spw

                    if STMP_1 == None:
                        item_query = Item.objects.filter(
                            STMP_2__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_2.value_str),
                            props=props
                        )
                    elif STMP_2 == None:
                        item_query = Item.objects.filter(
                            STMP_1__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_1.value_str),
                            props=props
                        )
                    else:
                        item_query = Item.objects.filter(
                            STMP_1__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_1.value_str),
                            STMP_2__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_2.value_str),
                            props=props
                        )

                    parent_count = 0
                    for item in item_query:
                        parent_count = Item_refs.objects.filter(parent=item).count()
                        if parent_count > 0:
                            break

                    version = 0
                    if parent_count > 0:
                        version = ItemManager.get_verstion(STMP_1=STMP_1, STMP_2=STMP_2, props=Item.props.from_spw)

                    while True:
                        try:
                            parent = Item.objects.create(
                                STMP_1_id=STMP_1.id if STMP_1 else None,
                                STMP_2_id=STMP_2.id if STMP_2 else None,
                                props=props,
                                document=document,
                                version=version
                            )
                            break
                        except IntegrityError:
                            version += 1

                    Item_refs.objects.create(parent_id=int(top_level.value), child=parent)
                    self.link_image_to_item(parent)

                    if STMP_2 != None:
                        self.rec_image_cwd(parent.id, delete_dbl_spaces(STMP_2.value_str))

                    query_spw = Document_attributes_view.objects.filter(document=document).order_by(*['position_in_document'])
                    specification = Spw_attrsQuerySet.make_specification(queryResult=query_spw)

                    SPC_CLM_MARK_old = None
                    for line_specification in specification:
                        SPC_CLM_NAME = delete_dbl_spaces(line_specification.get('SPC_CLM_NAME'))
                        SPC_CLM_NAME_ID = line_specification.get('SPC_CLM_NAME_ID')

                        SPC_CLM_MARK = delete_dbl_spaces(line_specification.get('SPC_CLM_MARK'))
                        SPC_CLM_MARK_ID = line_specification.get('SPC_CLM_MARK_ID')

                        if SPC_CLM_NAME_ID != None or SPC_CLM_MARK_ID != None:
                            if isinstance(SPC_CLM_MARK, str) and SPC_CLM_MARK.startswith('-') and isinstance(SPC_CLM_MARK_ID, int):
                                _SPC_CLM_MARK = f'{SPC_CLM_MARK_old}{SPC_CLM_MARK}'
                                for document_attribute in Document_attributes.objects.filter(id=SPC_CLM_MARK_ID):
                                    try:
                                        _document_attribute = Document_attributes.objects.get(
                                            attr_type=document_attribute.attr_type,
                                            value_str=_SPC_CLM_MARK
                                        )

                                        try:
                                            document_attr_cross = Document_attr_cross.objects.filter(
                                                attribute=document_attribute,
                                                document=document)[0]
                                            setAttr(line_specification, 'SPC_CLM_MARK_ID', _document_attribute.id)
                                        except IndexError:
                                            Document_attr_cross.objects.create(
                                                attribute=_document_attribute,
                                                document=document
                                            )
                                        setAttr(line_specification, 'SPC_CLM_MARK_ID', _document_attribute.id)
                                    except Document_attributes.DoesNotExist:
                                        document_attribute.value_str = _SPC_CLM_MARK
                                        document_attribute.save()

                            elif isinstance(SPC_CLM_MARK, str):
                                SPC_CLM_MARK_old = SPC_CLM_MARK

                            try:
                                if SPC_CLM_MARK == None:
                                    child = Item.objects.filter(
                                        STMP_1__value_str__delete_dbl_spaces=SPC_CLM_NAME,
                                        props=Item.props.relevant
                                    )[0]
                                elif SPC_CLM_NAME == None:
                                    child = Item.objects.filter(
                                        STMP_2__value_str__delete_dbl_spaces=SPC_CLM_MARK,
                                        props=Item.props.relevant
                                    )[0]
                                else:
                                    child = Item.objects.filter(
                                        STMP_1__value_str__delete_dbl_spaces=SPC_CLM_NAME,
                                        STMP_2__value_str__delete_dbl_spaces=SPC_CLM_MARK,
                                        props=Item.props.relevant
                                    )[0]

                                Item_document.objects.get_or_create(item=child, document=document)

                            except IndexError:
                                d = dict(
                                    STMP_1_id=SPC_CLM_NAME_ID,
                                    STMP_2_id=SPC_CLM_MARK_ID,
                                    props=Item.props.relevant | Item.props.from_spw | Item.props.for_line,
                                )
                                logger.debug(f'd: {d}')
                                child, created = Item.objects.get_or_create(**d, defaults=dict(document=document))

                                if not created:
                                    Item_document.objects.get_or_create(item=child, document=document)
                                    logger.debug(f'Not Created: {child}')
                                else:
                                    logger.debug(f'Created: {child}')

                            if parent.id != child.id:
                                Item_refs.objects.get_or_create(parent=parent, child=child)

                                defaults = dict(
                                    parent=parent,
                                    child=child,
                                    SPC_CLM_FORMAT_id=line_specification.get('SPC_CLM_FORMAT_ID'),
                                    SPC_CLM_ZONE_id=line_specification.get('SPC_CLM_ZONE_ID'),
                                    SPC_CLM_POS_id=line_specification.get('SPC_CLM_POS_ID'),
                                    SPC_CLM_MARK_id=line_specification.get('SPC_CLM_MARK_ID'),
                                    SPC_CLM_NAME_id=line_specification.get('SPC_CLM_NAME_ID'),
                                    SPC_CLM_COUNT_id=line_specification.get('SPC_CLM_COUNT_ID'),
                                    SPC_CLM_NOTE_id=line_specification.get('SPC_CLM_NOTE_ID'),
                                    SPC_CLM_MASSA_id=line_specification.get('SPC_CLM_MASSA_ID'),
                                    SPC_CLM_MATERIAL_id=line_specification.get('SPC_CLM_MATERIAL_ID'),
                                    SPC_CLM_USER_id=line_specification.get('SPC_CLM_USER_ID'),
                                    SPC_CLM_KOD_id=line_specification.get('SPC_CLM_KOD_ID'),
                                    SPC_CLM_FACTORY_id=line_specification.get('SPC_CLM_FACTORY_ID'),

                                    section=line_specification.get('section'),
                                    subsection=line_specification.get('subsection'),
                                )

                                item_line, _ = Item_line.objects.get_or_create(parent=parent, child=child, defaults=defaults)
                                # print(f'Create Item_line: {item_line}')

                else:
                    pass

            document.props |= Documents.props.beenItemed
            document.save()

    def make_cdw(self, document):
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.kd.models.documents import Documents
        from kaf_pas.system.models.contants import Contants
        from kaf_pas.ckk.models.item import ItemManager

        top_level = Contants.objects.get(code='audo_top_level')

        with transaction.atomic():
            if document.file_document.lower().find('мусор') == -1:

                try:
                    STMP_1 = Document_attributes_view.objects.get(document=document, attr_type__code='STMP_1')
                except Document_attributes_view.DoesNotExist:
                    STMP_1 = None
                except Document_attributes_view.MultipleObjectsReturned:
                    STMP_1 = Document_attributes_view.objects.filter(document=document, attr_type__code='STMP_1')[0]

                try:
                    STMP_2 = Document_attributes_view.objects.get(document=document, attr_type__code='STMP_2')
                except Document_attributes_view.DoesNotExist:
                    STMP_2 = None
                except Document_attributes_view.MultipleObjectsReturned:
                    STMP_2 = Document_attributes_view.objects.filter(document=document, attr_type__code='STMP_2')[0]

                if STMP_1 != None or STMP_2 != None:
                    cnt = Item.objects.filter(
                        STMP_1__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_1.value_str) if STMP_1 else None,
                        STMP_2__value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_2.value_str) if STMP_2 else None,
                        props=Item.props.relevant | Item.props.from_cdw,
                    ).count()

                    version = 0
                    if cnt != 0:
                        version = ItemManager.get_verstion(STMP_1=STMP_1, STMP_2=STMP_2, props=Item.props.relevant | Item.props.from_cdw)

                    while True:
                        try:
                            item = Item.objects.create(
                                STMP_1_id=STMP_1.id if STMP_1 else None,
                                STMP_2_id=STMP_2.id if STMP_2 else None,
                                props=Item.props.relevant | Item.props.from_cdw,
                                document=document,
                                version=version
                            )
                            break
                        except IntegrityError:
                            version += 1

                    Item_refs.objects.get_or_create(parent_id=int(top_level.value), child=item)
                    self.link_image_to_item(item)

                else:
                    pass

                document.props |= Documents.props.beenItemed
                document.save()

    def make_pdf(self, document, STMP_1_type, STMP_2_type):
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.ckk.models.item import ItemManager
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.kd.models.document_attributes import Document_attributes
        from kaf_pas.kd.models.documents import Documents
        from kaf_pas.system.models.contants import Contants

        top_level = Contants.objects.get(code='audo_top_level')

        with transaction.atomic():
            if document.file_document.lower().find('мусор') == -1:
                full_path = document.file_document
                _, file_name = os.path.split(full_path)
                file_name_part = file_name.split(' - ')
                if len(file_name_part) == 2:

                    STMP_1, ext = os.path.splitext(file_name_part[1])
                    STMP_2 = file_name_part[0]
                else:
                    STMP_1 = file_name.strip().replace('.pdf', '').replace('.PDF', '')
                    STMP_2 = STMP_1

                try:
                    STMP_1_attr, _ = Document_attributes.objects.get_or_create(value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_1), attr_type=STMP_1_type)
                except Document_attributes.MultipleObjectsReturned:
                    STMP_1_attr = Document_attributes.objects.filter(value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_1), attr_type=STMP_1_type)[0]

                try:
                    STMP_2_attr, _ = Document_attributes.objects.get_or_create(value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_2), attr_type=STMP_2_type)
                except Document_attributes.MultipleObjectsReturned:
                    STMP_2_attr = Document_attributes.objects.filter(value_str__delete_dbl_spaces=delete_dbl_spaces(STMP_2), attr_type=STMP_2_type)[0]

                cnt = Item.objects.filter(
                    STMP_1__value_str__delete_dbl_spaces=STMP_1,
                    STMP_2__value_str__delete_dbl_spaces=STMP_2,
                    props=Item.props.relevant | Item.props.from_pdf,
                ).count()

                version = 0
                if cnt != 0:
                    version = ItemManager.get_verstion(STMP_1=STMP_1_attr, STMP_2=STMP_2_attr, props=Item.props.from_pdf)

                while True:
                    try:
                        item = Item.objects.create(
                            STMP_1=STMP_1_attr,
                            STMP_2=STMP_2_attr,
                            props=Item.props.relevant | Item.props.from_pdf,
                            document=document,
                            version=version
                        )
                        break
                    except IntegrityError:
                        version += 1

                Item_refs.objects.get_or_create(parent_id=int(top_level.value), child=item)
                self.link_image_to_item(item)

            document.props |= Documents.props.beenItemed
            document.save()
