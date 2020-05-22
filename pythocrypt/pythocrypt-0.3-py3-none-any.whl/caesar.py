"""
Module for Caesar cipher algorithms
"""


def encrypt(message: str, shift: int = 3, key: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
    """
    This function requires a string that will be encrypted in caesar's shift way.

    :param message: str. Message to be encrypted

    :param shift: int. Shift to be used

    :param key: str. Key for encryption

    :return: message encrypted: str
    """

    encrypted = ""
    for letter in message:
        letter_index = key.find(letter.upper())
        if letter_index != -1:
            letter_encrypted = key[(letter_index + shift) % len(key)]
            encrypted += letter_encrypted if letter.isupper() else letter_encrypted.lower()
        else:
            encrypted += letter

    return encrypted


def decrypt(message: str, shift: int = 3, key: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
    """
    This function decodes encrypted message in caesar's shift way.

    :param message: str. Message to be decrypted

    :param shift: int. Shift to be used

    :param key: str. Key used for decryption

    :return: message decrypted: str
    """

    decrypted = ""
    for letter in message:
        letter_index = key.find(letter.upper())
        if letter_index != -1:
            letter_decrypted = key[(letter_index - shift) % len(key)]
            decrypted += letter_decrypted if letter.isupper() else letter_decrypted.lower()
        else:
            decrypted += letter

    return decrypted


def brute_force_decryption(message: str,
                           initial_shift: int = 1,
                           final_shift: int = 25,
                           key: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    """
    This function returns all shifts decryption between 1 and 25.

    :param message: message to be decrypted

    :param initial_shift: Initial attempt shift

    :param final_shift: Final attempt shift

    :param key: key used for decryption

    :return: list of decrypted messages
    """
    return [decrypt(message, i, key) for i in range(initial_shift, final_shift)]
