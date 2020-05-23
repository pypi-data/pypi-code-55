import random
import string
from typing import Sequence, Generator

from countersign.core import StringGenerator


class PasswordGenerator(StringGenerator):
    """

    """

    def __init__(self, characters: Sequence[chr], length: int, unique: bool):
        self.characters = characters
        self.length = length
        self._random_function = None
        self.unique = unique

    def generate(self) -> str:
        """
        :return: The generated password
        """
        random_sequence = self._random_function(self.characters, k=self.length)
        return ''.join(random_sequence)

    @property
    def unique(self):
        return self._unique

    @unique.setter
    def unique(self, is_unique):
        if is_unique and len(self.characters) < self.length:
            raise ValueError(
                'Impossible to build password of all unique characters when the specified length is '
                'larger than the number of characters specified. Provide a larger collection of characters.')

        self._unique = is_unique
        self._random_function = random.sample if is_unique else random.choices


def password(characters: Sequence[chr] = string.printable,
             length: int = 8,
             unique: bool = False) -> str:
    """
    :param characters: The character pool that will be used when generating the password
    :param length: The total length of the password to be generated
    :param unique: Whether the password should consist of unique given characters
    :return: The randomly generated password
    """
    return PasswordGenerator(characters=characters, length=length, unique=unique).generate()


def passwords(characters: Sequence[chr] = string.printable,
              length: int = 8,
              unique: bool = False) -> Generator[str, None, None]:
    """
    :param characters: The character pool that will be used when generating the password
    :param length: The total length of the password to be generated
    :param unique: Whether the password should consist of unique given characters
    :return: Generator capable of generating 'count' number of passwords
    """
    return next(PasswordGenerator(characters=characters, length=length, unique=unique))
