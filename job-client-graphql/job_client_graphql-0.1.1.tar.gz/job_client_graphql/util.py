
import string
import random


class Util:
    """
    """

    def __init__(self):
        """
        """
        pass

    @staticmethod
    def random_uuid(size=6,
                    chars=None):
        """
        """
        if not chars:
            chars = string.ascii_letters + string.digits

        return ''.join(random.choice(chars) for _ in range(size))
