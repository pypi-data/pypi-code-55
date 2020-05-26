"""
This null cipher uses every nth letter after a punctuation mark to encode message
"""

from string import punctuation
from pythocrypt.common.utils import load, create_simple_sentence
from random import choice

import pkg_resources


def encrypt(message: str, shift: int = 3) -> str:
    """
    Encryption involves taking a text and be pay attention to position of the
    punctuation so that after each sign, after counting a number of letters
    (eg 3 letters) a letter from the hidden message is found.

    :param message: message to be encrypted
    :param shift: letter count after punctuation mark
    :return: message decrypted
    """

    path = './common/english_words.txt'  # always use slash
    filepath = pkg_resources.resource_filename(__name__, path)
    english_words = load(filepath)

    message = message.replace(" ", "")

    message_encrypted = f"{create_simple_sentence(True)}."

    for letter in message:
        available_words = list(filter(lambda word: len(word) >= shift and word[shift-1] == letter, english_words))
        word_picked = choice(available_words)
        message_encrypted += f" {word_picked.capitalize()} {create_simple_sentence()}."

    return message_encrypted


def decrypt(message: str, shift: int = 3) -> str:
    """
    Decryption requires to know of the shift N used. To find the plain text it
    is necessary to browse the text in search of the signs of punctuation.
    After each one, count a number of characters (N) to find a new letter of the plaintext.

    :param message: message to be decrypted
    :param shift: letter count after punctuation mark
    :return: message decrypted
    """

    message_decrypted = ""

    counter = 0
    should_count = False

    for letter in message:

        if should_count and not letter.isspace() and letter not in punctuation:
            counter += 1

        if letter in punctuation:
            should_count = True

        if counter == shift:
            message_decrypted += letter
            counter = 0
            should_count = False

    return message_decrypted
