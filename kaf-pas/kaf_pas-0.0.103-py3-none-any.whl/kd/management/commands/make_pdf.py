import logging

from django.core.management import BaseCommand
from django.db import transaction
from tqdm import tqdm

from isc_common.logger.Logger import Logger
from kaf_pas.ckk.models.attr_type import Attr_type
from kaf_pas.kd.models.documents import Documents
from kaf_pas.kd.models.documents_ext import DocumentManagerExt
from kaf_pas.kd.models.pdfs import Pdfs

logger = logging.getLogger(__name__)
logger.__class__ = Logger


class Command(BaseCommand):
    help = "Test Make PDF"
    documentManagerExt = DocumentManagerExt(logger=logger)

    def handle(self, *args, **options):
        pdfs = [pdfs for pdfs in Pdfs.objects.filter(props=~Documents.props.beenItemed) if pdfs.file_document.lower().find('мусор') == -1]

        with transaction.atomic():
            STMP_1_type = Attr_type.objects.get(code='STMP_1')
            STMP_2_type = Attr_type.objects.get(code='STMP_2')

            pbar = tqdm(total=len(pdfs))
            for document in pdfs:
                self.documentManagerExt.make_pdf(document=document, STMP_1_type=STMP_1_type, STMP_2_type=STMP_2_type)
                pbar.update()
            pbar.close()
