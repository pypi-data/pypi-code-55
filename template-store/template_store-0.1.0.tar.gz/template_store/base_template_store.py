import abc


class BaseTemplateStore(abc.ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_template(self, template_name: str):
        pass
