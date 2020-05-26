import logging

from django.core.management import BaseCommand
from django.db import transaction
from tqdm import tqdm

from isc_common.logger.Logger import Logger
from kaf_pas.kd.models.documents import Documents
from kaf_pas.kd.models.documents_ext import DocumentManagerExt
from kaf_pas.kd.models.spws import Spws

logger = logging.getLogger(__name__)
logger.__class__ = Logger


class Command(BaseCommand):
    help = "Test Make SPW"
    documentManagerExt = DocumentManagerExt(logger=logger)

    def handle(self, *args, **options):
        spws = [spws for spws in Spws.objects.filter(props=~Documents.props.beenItemed) if spws.file_document.lower().find('мусор') == -1]

        with transaction.atomic():
            pbar = tqdm(total=len(spws))
            for document in spws:
                self.documentManagerExt.make_spw(document=document)
                pbar.update()

            pbar.close()
