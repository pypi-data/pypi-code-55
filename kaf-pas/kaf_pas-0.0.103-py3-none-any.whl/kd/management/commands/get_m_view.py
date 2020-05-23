import logging

from django.core.management import BaseCommand

from kaf_pas.kd.models.documents import DocumentManager

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Тестирование get_m_view"

    def handle(self, *args, **options):
        logger.info(self.help)

        DocumentManager.get_m_view()
