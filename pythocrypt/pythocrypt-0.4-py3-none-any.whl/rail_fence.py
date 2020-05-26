"""
Module for rail fence cipher.
In the rail fence cipher, the plain text is written downwards and diagonally on successive
"rails" of an imaginary fence, then moving up when the bottom rail is reached. When the top rail
is reached, the message is written downwards again until the whole plaintext is written out.
The message is then read off in rows.
"""


def encrypt(message: str, rails: int = 2, no_spaces: bool = True, uppercase: bool = True) -> str:
    """
    Function to encrypt with rail fence cipher.

    :param message: message to be encrypted
    :param rails: number of rails to be used
    :param no_spaces: remove whitespaces to difficult decryption
    :param uppercase: transform to uppercase to difficult decryption
    :return: encrypted message
    """

    if no_spaces:
        message_encrypted = message.replace(" ", "")
    if uppercase:
        message_encrypted = message_encrypted.upper()

    slices = _slice_rails(message_encrypted, rails)

    message_encrypted = "".join(slices)
    return message_encrypted


def _slice_rails(message, rails):
    slices = [[] for i in range(rails)]

    slice_index = 0
    step = 1

    for letter in message:
        slices[slice_index].append(letter)

        if slice_index >= (rails-1) or (slice_index + step) <= -1:
            step = step * (-1)

        slice_index = slice_index + step

    slices = [''.join(s) for s in slices]
    return slices


def decrypt(message: str, rail: int) -> str:
    """
    This function decodes encrypted message in rail fence way.

    :param message: message to be decoded
    :param rail: number of rails used to encrypt message
    :return: message decrypted
    """

    rails = [[] for _ in range(rail)]

    slice_index = 0
    letter_counter = 0

    cycle_units = _cycle_units(rail)
    full_cycles = len(message) // cycle_units
    remaining_letters = len(message) % cycle_units
    total_remaining_letters = remaining_letters
    j = 0

    while j < len(message):

        rails[slice_index].append(message[j])
        letter_counter += 1

        if j == len(message) - 1:
            break

        if _is_end_of_edge_rail(slice_index,
                                letter_counter,
                                full_cycles) or _is_end_of_middle_row(letter_counter, full_cycles):

            if remaining_letters > 0:

                if not _is_edge_rail(slice_index, rails) \
                    and total_remaining_letters >= (cycle_units - slice_index + 1):
                    remaining_letters -= 2
                    rails[slice_index].append(message[j+1])
                    rails[slice_index].append(message[j+2])
                    j += 2
                else:
                    remaining_letters -= 1
                    j += 1
                    rails[slice_index].append(message[j])

            letter_counter = 0
            slice_index += 1

        j += 1

    message_decrypted = _rails_decryption(rails, len(message))
    return message_decrypted


def brute_force(message):
    """
    This function uses brute force rail fence to break decryption. It starts from 2 rows
    and keep rise until reach the length of the message.

    :param message: message to be decrypted
    :return: list of possibles messages decrypted
    """
    begin_rail = 2
    end_rail = len(message) - 2

    return [decrypt(message, i) for i in range(begin_rail, end_rail)]


def _is_edge_rail(index, rails):
    return index in (0, index == len(rails)-1)


def _rails_decryption(rails, message_len):

    slice_index = 0
    step = 1

    message = ""

    for _ in range(message_len):

        if len(rails[slice_index]) > 0:
            message += rails[slice_index].pop(0)

        if slice_index >= (len(rails) - 1) or (slice_index + step) <= -1:
            step = step * (-1)

        slice_index = slice_index + step

    return message


def _is_end_of_edge_rail(slice_index, counter, cycles):
    return slice_index == 0 and counter == cycles


def _is_end_of_middle_row(counter, cycles):
    return counter == cycles * 2


def _number_of_letters_in_rails(cycles, cycle_size):
    return cycles * cycle_size


def _cycle_units(rails):
    return (rails * 2) - 2


def _explode(message, piece_size):
    pieces = []
    counter = 0
    piece = ""
    for letter in message:
        piece += letter
        counter += 1
        if counter == piece_size:
            pieces.append(piece)
            piece = ""
            counter = 0

    if piece != "":
        pieces.append(piece)

    return pieces


def _put_on_rails(cycle, rails):

    rail_index = 0
    step = 1
    for letter in cycle:
        rails[rail_index] += letter

        if rail_index >= (len(rails) - 1) or (rail_index + step) <= -1:
            step = step * (-1)

        rail_index = rail_index + step
