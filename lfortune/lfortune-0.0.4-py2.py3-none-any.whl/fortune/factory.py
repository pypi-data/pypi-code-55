
from src.lfortune.abstract import FortuneAbstract
from src.lfortune.fortune import Fortune
from src.lfortune.fortune.indexer import Indexer
from src.lfortune.fortune import Config

class Factory:

    @staticmethod
    def create(config_file: str = None) -> FortuneAbstract:
        config = Config(config_file)
        return Fortune(config, Indexer(Fortune.SEPARATOR))
