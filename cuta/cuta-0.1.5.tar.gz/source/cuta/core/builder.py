
import abc


class Builder(metaclass=abc.ABCMeta):
    """
    Builder

    This is the base class for all application builders. It is
    an abstract class and cannot be directly instatiated. Specific
    build implmentations should inherit from this class and implement
    the abstract properties and methods.
    """

    def build(self, app):
        """
        """
        pass


class AWSLambdaBuilder(Builder):
    """
    AWS Lambda Builder

    A builder used to create a
    """

