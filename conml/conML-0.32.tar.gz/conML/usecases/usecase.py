#  C O N S T R U C T I V I S T__ __
#   _____ ____   ____   /  |/  // /
#  / ___// __ \ / __ \ / /|_/ // /
# / /__ / /_/ // / / // /  / // /___
# \___/ \____//_/ /_//_/  /_//_____/
#  M A C H I N E   L E A R N I N G
#
#
# A Project by
# Thomas Schmid | UNIVERSITÄT LEIPZIG
# www.constructivist.ml
#
# Code Author: Dmitrij Denisenko
# Licence: MIT


from abc import abstractmethod, ABC


class Usecase(ABC):
    """Base class for all use cases.

    """
    def execute(self, request):
        """Execute the given requests.

        Args:
            request (namedtuple): Request with important parameters.

        Returns:
            Any

        """
        try:
            return self.process(request)

        except Exception as error:
            print(error.with_traceback())
            raise

    @abstractmethod
    def process(self, *args, **kwargs):
        """Every use case should implent their logic within this method. """
        raise NotImplementedError
