from abc import ABC, abstractmethod


class StringGenerator(ABC):
    """
    Instance capable of generating strings of different shapes and sizes
    """

    def __next__(self):
        while True:
            yield self.generate()

    def __iter__(self):
        return self

    @abstractmethod
    def generate(self) -> str:
        """
        Generates some string

        :return: The generated string
        """
