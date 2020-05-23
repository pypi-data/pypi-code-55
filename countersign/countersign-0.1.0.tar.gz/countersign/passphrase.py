import enum
import itertools
import random
from typing import Sequence, Generator, Optional

from countersign.core import StringGenerator
from countersign.password import PasswordGenerator


class DigitPlacementStrategy(enum.Enum):
    BEFORE = 'before'
    AFTER = 'after'
    BEFORE_AND_AFTER = 'before_and_after'
    IN_BETWEEN = 'in_between'
    AROUND = 'around'


class OneTimePasswordGenerator(PasswordGenerator):
    """
    Special password generator that generates a single password every call to generate.
    """

    def __init__(self, characters: Sequence[chr], length: int, unique: bool):
        super().__init__(characters, length, unique)
        self._cached = super().generate()

    def generate(self) -> str:
        return self._cached


class DigitGenerationStrategy:
    """
    Object containing various details about how digits are generated and placed throughout a generated passphrase
    """

    def __init__(self,
                 digit_count: int,
                 placement: Optional[DigitPlacementStrategy] = None,
                 unique: bool = True,
                 digits: Optional[Sequence[int]] = None):
        """
        Initializes a new digit generation strategy with the given details

        :param digits: The digits allowed to be used when generating a passphrase
        :param digit_count: The number of digits to be used in the generated 'digit group'
        :param unique: If all generated 'digit groups' should be unique
        :param placement: Where should generated digit groups be placed throughout the passphrase
        """

        if digits is None:
            digits = range(10)
        string_digits = [str(digit) for digit in digits]

        if placement is None:
            placement = DigitPlacementStrategy.AFTER

        self.digits = string_digits
        self.digit_count = digit_count
        self.unique = unique
        self.placement = placement

    def to_digit_generator(self) -> Generator[str, None, None]:
        """
        Factory method for creating a generator based on instance variables

        :return: The digit generator created from this strategy instance
        """
        if self.unique:
            return next(PasswordGenerator(self.digits, self.digit_count, False))
        else:
            return next(OneTimePasswordGenerator(self.digits, self.digit_count, False))


class PassPhraseGenerator(StringGenerator):
    """
    Generates strings that resemble passphrases. Passphrases are like password except they consist of more structured
    patterns. Consult the below example for a preview regarding what is possible with passphrase generators.

    - TestWord123
    - 123TestWord
    - Test123Word
    - 123Another456Test789Word012
    """

    def __init__(self, words: Sequence[str], word_count: int, digit_strategy: Optional[DigitGenerationStrategy] = None):
        """
        Initializes a new passphrase generator instance

        :param words: The word pool that will be used when generating a passphrase.
        :param word_count: The number of words the passphrase will consist of.
        :param digit_strategy: Strategy that will be used for placing digits throughout the passphrase
        """
        self.words = words
        self.word_count = word_count
        self.digit_strategy = digit_strategy

    def generate(self) -> str:
        """
        :return: The generated passphrase
        """
        selected_words = random.choices(self.words, k=self.word_count)
        if self.digit_strategy is None:
            return ''.join(selected_words)

        digits = self.digit_strategy.to_digit_generator()
        placement_strategy = self.digit_strategy.placement

        def digit_wrap(text: str) -> str:
            return next(digits) + text + next(digits)

        def digit_weave(words: Sequence[str]) -> Sequence[str]:
            zipped_values = zip(words, itertools.islice(digits, self.word_count))

            # Zip function returns iterable of tuples representing the zipped elements.
            # The values should be flattened.
            flattened_values = [value for zipped_value in zipped_values for value in zipped_value]

            # The last element is not wanted. The function should interweave digits in between, not
            # add digits to the beginning or end.
            return flattened_values[:-1]

        if placement_strategy is DigitPlacementStrategy.BEFORE:
            return next(digits) + ''.join(selected_words)
        elif placement_strategy is DigitPlacementStrategy.AFTER:
            return ''.join(selected_words) + next(digits)
        elif placement_strategy is DigitPlacementStrategy.BEFORE_AND_AFTER:
            return digit_wrap(''.join(selected_words))
        elif placement_strategy is DigitPlacementStrategy.IN_BETWEEN:
            digit_weaved_words = digit_weave(selected_words)
            return ''.join(digit_weaved_words)
        elif placement_strategy is DigitPlacementStrategy.AROUND:
            digit_weaved_words = digit_weave(selected_words)
            return digit_wrap(''.join(digit_weaved_words))


def passphrase(words: Sequence[str],
               word_count: int = 3,
               digit_strategy: Optional[DigitGenerationStrategy] = None) -> str:
    """
    :param words:
    :param word_count:
    :param digit_strategy:
    :return:
    """
    return PassPhraseGenerator(words=words, word_count=word_count, digit_strategy=digit_strategy).generate()


def passphrases(words: Sequence[str],
                word_count: int = 3,
                digit_strategy: Optional[DigitGenerationStrategy] = None) -> Generator[str, None, None]:
    """
    :param words:
    :param word_count:
    :param digit_strategy:
    :return:
    """
    return next(PassPhraseGenerator(words=words, word_count=word_count, digit_strategy=digit_strategy))
