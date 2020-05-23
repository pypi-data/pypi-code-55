import logging

from django.core.management import BaseCommand
from django.db import transaction
from isc_common.logger.Logger import Logger

from kaf_pas.kd.models.documents_ext import DocumentManagerExt
from kaf_pas.kd.models.lotsman_documents_hierarcy_ext import Lotsman_documents_hierarcyManagerExt
from kaf_pas.kd.models.lotsman_documents_hierarcy_view import Lotsman_documents_hierarcy_view

logger = logging.getLogger(__name__)
logger.__class__ = Logger


class Command(BaseCommand):
    help = "Test Make Lotsman"
    documentManagerExt = DocumentManagerExt(logger=logger)

    def handle(self, *args, **options):
        self.lotsman_documents_hierarcyManagerExt = Lotsman_documents_hierarcyManagerExt(
            documentManagerExt=self.documentManagerExt,
            user=2,
            logger=logger
        )

        with transaction.atomic():
            lotsman_documents_hierarcy_view = Lotsman_documents_hierarcy_view.objects.get(id=100937)
            self.lotsman_documents_hierarcyManagerExt.make_items(
                lotsman_documents_hierarcy_view_record=lotsman_documents_hierarcy_view
            )
