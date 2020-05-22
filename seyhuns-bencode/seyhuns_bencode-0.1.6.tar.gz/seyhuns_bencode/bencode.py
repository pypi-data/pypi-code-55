import enum
import logging
import requests

from seyhuns_bencode.exceptions import InputError


logger = logging.getLogger(__name__)


class States(enum.Enum):
    """List of states during decoding."""
    WAIT_DICT_OPEN = enum.auto()    # Next state should be initiating a dict
    WAIT_DICT_VALUE = enum.auto()   # Next state should be the dict value
    WAIT_DICT_KEY = enum.auto()     # Next state should be the dict key
    # Next state can be closing the dictionary, or it can be a new value.
    WAIT_DICT_CLOSE = enum.auto()
    # Next state can be closing the list, or it can be a new value to list.
    WAIT_LIST_CLOSE = enum.auto()
    # Next state should be a list value, because empty lists are not allowed.
    WAIT_LIST_VALUE = enum.auto()


class BencodeParser:
    """Bencoder decoder.

    Attributes:
        state_stack: [States] -- Stack for keeping order of states.
        output_list: [bytes]  -- Keep the list of bytes that will be returned
                                 after joined.
    """

    state_stack: [States]

    output_list: [bytes]

    def __init__(self, url: str) -> None:
        """Initialize BencodeDecoder.

        Initialized BencodeDecoder with:
            - ``self.state_stack`` having ``WAIT_DICT_OPEN``. The outermost
              object is always a dict.
            - ``self.encoded_str``` which is the content of the url.
            - ``output_list`` empty list, for keeping the final json.

        Args:
            url (str): URL of the file containing the seyhuns_bencode string.

        Raises:
            requests.exceptions.RequestException: If seyhuns_bencode string can't be
                fetched from url, this exception is raised.
        """
        response = requests.get(url)
        response.raise_for_status()
        self.state_stack = [States.WAIT_DICT_OPEN]
        self.encoded_str = response.content
        self.output_list = []

    def __call__(self) -> bytes:
        """Decode the seyhuns_bencode string.

        Returns:
            [bytes]: Return the decoded seyhuns_bencode string.

        Raises:
            - InputError: This error is raised if the seyhuns_bencode string is broken.
        """
        i = 0
        while i < len(self.encoded_str):
            if not self.state_stack:
                logger.debug("Invalid JSON, outermost object is not a dict.")
                raise InputError(i, self.encoded_str[:i])

            elif self.state_stack[-1] == States.WAIT_DICT_OPEN:
                # Initial state, we need to start with a dict for a valid json.
                self.state_stack.pop()
                string, i = self.parse_init_dictionary(i)
                self.output_list.append(string)

            elif self.state_stack[-1] == States.WAIT_DICT_KEY:
                # A new dict is initiated, we need at least one key.
                self.state_stack.pop()
                string, i = self.parse_byte_string(i)
                self.output_list.append(b'%s' % string)

            elif self.state_stack[-1] == States.WAIT_LIST_VALUE:
                # Because empty lists are not allowed
                # we have to expect a new value.
                self.state_stack.pop()
                value, i = self.parse_value(i)
                self.output_list.append(b'%s' % value)

            elif self.state_stack[-1] == States.WAIT_DICT_VALUE:
                # We have the key already in the output,
                # we need the value also.
                self.state_stack.pop()
                value, i = self.parse_value(i)
                self.output_list.append(b':%s' % value)

            elif self.state_stack[-1] == States.WAIT_LIST_CLOSE:
                # We can either close the list or add a new value.
                if self.encoded_str[i] == b'e'[0]:
                    self.state_stack.pop()
                    string, i = self.parse_end_list(i)
                    self.output_list.append(string)
                else:
                    string, i = self.parse_value(i)
                    self.output_list.append(b',%s' % string)

            elif self.state_stack[-1] == States.WAIT_DICT_CLOSE:
                # We can either close the dict, or add a new key pair.
                if self.encoded_str[i] == b'e'[0]:
                    self.state_stack.pop()
                    string, i = self.parse_end_dictionary(i)
                    self.output_list.append(string)

                elif self.encoded_str[i] in b'0123456789':
                    string, i = self.parse_byte_string(i)
                    self.output_list.append(b',%s' % string)
                    self.state_stack.append(States.WAIT_DICT_VALUE)

                else:
                    logger.debug("Failed while waiting dict key.")
                    raise InputError(i, self.encoded_str[:i])

        return b''.join(self.output_list)

    def parse_value(self, i: int) -> (bytes, int):
        """Parse the next token, starting from index ``i``.
        Returns:
            (value, i): -- Return a tuple holding the new value, and the new
                           index ``i``.

        Raises:
            - InputError: Raises because of unidentified pattern.
        """
        if self.encoded_str[i] in b'0123456789':
            value, i = self.parse_byte_string(i)
        elif self.encoded_str[i] == b'i'[0]:
            value, i = self.parse_integer(i)
        elif self.encoded_str[i] == b'd'[0]:
            value, i = self.parse_init_dictionary(i)
        elif self.encoded_str[i] == b'l'[0]:
            value, i = self.parse_list(i)
        else:
            logger.debug("Unidentified pattern.")
            raise InputError(i, self.encoded_str[:i])
        return value, i

    def parse_list(self, i: int) -> (bytes, int):
        """Parse list as the next value.

        Returns:
            (value, i): -- Return a tuple holding the new list, and the new
                           index ``i``.

        Raises:
            - InputError: Raises because next value is not list.
        """
        if self.encoded_str[i] != b'l'[0]:
            raise InputError(i, self.encoded_str[:i])
        self.state_stack.extend([
            States.WAIT_LIST_CLOSE,
            States.WAIT_LIST_VALUE,
        ])
        i += 1  # Skip `l`
        return b'[', i

    def parse_integer(self, i: int) -> (bytes, int):
        """Parse integer as the next value.

        Returns:
            (value, i): -- Return a tuple holding the new list, and the new
                           index ``i``.

        Raises:
            - InputError: Raises because next value is not list.
        """
        try:
            if self.encoded_str[i] != b'i'[0]:
                raise InputError(i, self.encoded_str[:i])
            i += 1  # Skip `i`
            j = i
            if self.encoded_str[i] not in b'-123456789':
                raise InputError(i, self.encoded_str[:i])
            if self.encoded_str[i] == b'-'[0]:
                if self.encoded_str[i + 1] not in b'123456789':
                    # -0 is not allowed.
                    raise InputError(i, self.encoded_str[:i])
                else:
                    j += 1
            while self.encoded_str[j] != b'e'[0]:
                if self.encoded_str[j] not in b'0123456789':
                    # Invalid character in integer
                    raise InputError(i, self.encoded_str[:i])
                j += 1
        except IndexError as exception:
            raise InputError(i, self.encoded_str[:i]) from exception
        integer = self.encoded_str[i:j]
        j += 1  # Skip e
        return integer, j

    def parse_end_list(self, i: int) -> (bytes, int):
        """Parse list closing bracket as the next value.

        Returns:
            (value, i): -- Return a tuple holding the list closing bracket,
                           and the new index ``i``.

        Raises:
            - InputError: Raises because next value is not list closing
                          bracket.
        """
        if self.encoded_str[i] != b'e'[0]:
            raise InputError(i, self.encoded_str[:i])
        else:
            return b']', i + 1

    def parse_end_dictionary(self, i: int) -> (bytes, int):
        """Parse dict closing bracket as the next value.

        Returns:
            (value, i): -- Return a tuple holding the dict closing bracket,
                           and the new index ``i``.

        Raises:
            - InputError: Raises because next value is not dict closing
                          bracket.
        """
        if self.encoded_str[i] != b'e'[0]:
            raise InputError(i, self.encoded_str[:1])
        else:
            return b'}', i + 1

    def parse_init_dictionary(self, i: int) -> (bytes, int):
        """Parse dict opening bracket as the next value.

        Returns:
            (value, i): -- Return a tuple holding the dict opening bracket, and
                           the new index ``i``.

        Raises:
            - InputError: Raises because next value is not dict opening
                          bracket.
        """
        if self.encoded_str[i] != b'd'[0]:
            raise InputError(i, self.encoded_str[:1])
        else:
            self.state_stack.extend([
                States.WAIT_DICT_CLOSE,
                States.WAIT_DICT_VALUE,
                States.WAIT_DICT_KEY,
            ])
            return b'{', i + 1

    def parse_byte_string(self, i: int) -> (bytes, int):
        """Parse string as the next value.

        Returns:
            (value, i): -- Return a tuple holding the string, and the new index
                           ``i``.

        Raises:
            - InputError: Raises because next value is not a valid string.
        """
        try:
            if self.encoded_str[i] not in b'0123456789' or (
                    self.encoded_str[
                        i
                    ] == b'0'[0] and self.encoded_str[i + 1] != b':'[0]
            ):
                raise InputError(i, self.encoded_str[:1])
            j = i
            while self.encoded_str[j] in b'0123456789':
                j += 1
        except IndexError as exception:
            raise InputError(i, self.encoded_str[:1]) from exception
        byte_string_length = int(self.encoded_str[i: j])
        if self.encoded_str[j] != b':'[0]:
            raise InputError(i, self.encoded_str[:1])
        j += 1  # Skip the colon
        # Check if we have enough characters for including inside the string
        if j + byte_string_length >= len(self.encoded_str):
            raise InputError(i, self.encoded_str[:1])
        byte_string = self.encoded_str[j:j + byte_string_length]
        j += byte_string_length
        return b'"%s"' % byte_string, j
