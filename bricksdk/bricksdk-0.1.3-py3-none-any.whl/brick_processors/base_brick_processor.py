import abc


class BaseBrickProcessor(abc.ABC):
    """
    In the main() of every brick, a brick factory object is created.
    That object requires a Brick processor object which should be implemented using this interface.
    """

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def process(self, *args, **kwargs):
        pass
