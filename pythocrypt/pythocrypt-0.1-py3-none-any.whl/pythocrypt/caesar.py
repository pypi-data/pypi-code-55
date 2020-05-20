"""
Caesar cipher for module
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
