import logging

from django.core.management import BaseCommand

from isc_common.common.functions import delete_dbl_spaces
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_view import Item_view
from kaf_pas.kd.models.documents_ext import DocumentManagerExt

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Тестирование"

    def handle(self, *args, **options):
        logger.info(self.help)

        print(delete_dbl_spaces('К4310М-243-1.10.20.660           СБ'))
