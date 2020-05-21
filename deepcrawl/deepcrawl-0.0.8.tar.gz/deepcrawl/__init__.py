from .accounts.connection import AccountConnection
from .crawls.connection import CrawlConnection
from .downloads.connection import DownloadConnection
from .projects.connection import ProjectConnection
from .reports.connection import ReportConnection


class DeepCrawlConnection(AccountConnection, ProjectConnection, CrawlConnection, ReportConnection, DownloadConnection):
    __instance = None

    def __init__(self, id_user, key_pass, auth_type_user=False):
        super(DeepCrawlConnection, self).__init__(id_user, key_pass, auth_type_user)

        DeepCrawlConnection.__instance = self

    @staticmethod
    def get_instance():
        return DeepCrawlConnection.__instance
