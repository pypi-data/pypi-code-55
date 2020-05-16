
from src.abstract.fortune import FortuneAbstract
from src.fortune.fortune import Fortune
from src.fortune.indexer import Indexer
from src.fortune.config import Config

class Factory:

    @staticmethod
    def create(config_file: str = None) -> FortuneAbstract:
        config = Config(config_file)
        return Fortune(config, Indexer(Fortune.SEPARATOR))
