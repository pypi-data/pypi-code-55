# Copyright (C) Martin Singer <martin.singer@web.de>
#
# This file is part of PDF Chain.
#
# PDF Chain is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PDF Chain is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PDF Chain.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Martin Singer


'''
@brief PDF Chain string module.
@details
    This module contains classed with string constants
    or functions to process strings.
'''

import re

# import cli
import pdfchain.cli


def validate_page_selection_string(str_input):
    '''
    @brief   Validate page selection string from Concatenate File Filter entry.
    @details
        This functions normalizes and validates page selection strings.
        Before the validation the string becomes normalized.
        Normalization means the string becomes transformed
        to a unique PDFtk convented pattern.
        This is possible for PDFtk standardized strings
        and when the string equates a clear, comma separated pattern style.
        Mixing the styles is possible.

    @par Strings and Characters
        - `end`: indicates last page of document
        - `r`:   indicates reverse
        - `-`:   indicates connected pages
        - `,`:   indicates a separation of logical entities
        - ` `:   indicates a separation of logical

    @par Examples
        | Input String             | Output String   | Valid | Annotation                                            |
        | :----------------------- | :-------------- | :---- | :---------------------------------------------------- |
        | `1-end 2 1 r9`           | `1-end 2 1 r9`  | True  | clean PDFtk style                                     |
        | `1 - end, 2, 1, r9`      | `1-end 2 1 r9`  | True  | clean comma based style                               |
        | `end- 1 3 , r7 -31`      | `end-1 3 r7-31` | True  | tolerant to mixed separator styles                    |
        | `end-1, , 3  , r7  - 31` | `end-1 3 r7-31` | True  | tolerant to multiple comma and multiple spaces        |
        | `1-e n d, 4 - r 3`       | ``              | False | invalid spaces in indicator strings                   |
        | `38r`                    | ``              | False | indicator 'r' behind number is invalid                |
        | `1-end, 4, - 2`          | ``              | False | invalid comma separated sub entities _(is not `4-2`)_ |
        | `1 - en, a, x2`          | ``              | False | unknown strings and unknown characters                |
        | `1 - 4-1`                | ``              | False | double connections                                    |
        | `r r4, end end, r end`   | ``              | False | double indicator                                      |
        | `3r4, 9end, rend`        | ``              | False | missing separator or connector characters             |

    @par RegEx for PDFtk normalized string
        - from (required):
            - `^[1-9][0-9]*`
            - `^r[1-9][0-9]*`
            - `^end`
        - to (optional):
            - `-[1-9][0-9]*`
            - `-r[1-9][0-9]*`
            - `-end`

    @param[in]       The user file selection string
    @retval[0] True  When selection string is valid
    @retval[0] False When selection string is not valid
    @return[1]       Returns a PDFtk page selection command string, when file selection is interpretable and correct
    @retval[1] ""    Returns the input string, if the input string is empty or not interpretable
    '''
    REGEX = r"^((r?[1-9][0-9]*)|end)(-((r?[1-9][0-9]*)|end))?"
    valid = True
    str_output = ""

    # If string is empty, set default string
    if not str_input:
        str_base = "1-end"  #TODO: define this string as a constant
    else:
        str_base = str_input.lower()

    # Normalize string (create PDFtk command string)
    # (do not remove spaces as separators - just multiple spaces)
    arr_parts = str_base.split(',')
    for str_part in arr_parts:
        str_part = str_part.strip(',')             # strip leading and trailing commas from string
        str_part = str_part.strip(' ')             # strip leading and trailing spaces from string
        str_part = re.sub(r"\s+", r" ", str_part)  # remove multiple spaces
        str_part = str_part.replace(' -', '-')     # remove leading  spaces from hyphen
        str_part = str_part.replace('- ', '-')     # remove trailing spaces from hyphen
        str_output += ' ' + str_part

    # Validate normalized string
    arr_parts = str_output.split(None)
    for str_part in arr_parts:
        if re.fullmatch(REGEX, str_part) is None:
            valid = False
            #cli.debug_message("ERROR: Expression '{}'"
            #        " is no valid page selection pattern".format(str_part)) #DEBUG

    if valid == True:
        return valid, str_output
    else:
        return valid, str_input


def create_handle_from_number(number):
    '''
    @brief   Create a handle from an integer number.
    @details
        A handle is a letter or a letter string, representing a document path.
        It is used to assign various options to a document
        in the concatenate command.
        In this function a decimal number (base 10) becomes converted
        to a letter number (base 26), returned as string.
        - A 'A' is equivalent to a '0'
        - A 'Z' is equivalent to a '25'
        Leading 'A's are not visible as well leading '0's are not.

    @param[in] number The document number (id)
    @return           A string with a handle
    '''
    BASE = 26
    handle = ""

    # Convert number from base 10 [0 to 9] to base 26 [A to Z]
    while number >= BASE:
        handle += chr(ord('A') + number % BASE)
        number //= BASE

    handle += chr(ord('A') + number % BASE)
    return handle


def count_pages_of_document(path):
    '''
    @brief   Count the amount of pages of a PDF document.
    @details
        The document specified in the transferred path is opened
        and a memory buffer is read in binary. In this buffer,
        the respective number of four significant patterns is counted
        and calculated. This result is the page number of the document.
    @see <https://docs.python.org/3/library/stdtypes.html#bytes-and-bytearray-operations>

    @param[in] path The path to the document file
    @retval    0    The number of pages cannot be determined
    @return         The number of pages determined
    '''
    TYPE_PAGE_A = b'/Type/Page'
    TYPE_PAGE_B = b'/Type /Page'
    TYPE_PAGE_C = b'/Type/Pages'
    TYPE_PAGE_D = b'/Type /Pages'

    num_pages = 0

    try:
        with open(path, mode='rb') as source_file:
            file_content = source_file.read()
            readable = True

            count_A = file_content.count(TYPE_PAGE_A)
            count_B = file_content.count(TYPE_PAGE_B)
            count_C = file_content.count(TYPE_PAGE_C)
            count_D = file_content.count(TYPE_PAGE_D)

            num_pages = count_A + count_B - count_C - count_D
    except IOError as io_error:
        if io_error.errno == errno.ENOENT:
            cli.msg("ERROR: file '{}' does not exist!".format(path))
        elif io_error.errno == errno.EACCES:
            cli.msg("ERROR: file '{}' cannot be read!".format(path))
        else:
            cli.msg("ERROR: Unknown error in function 'count_pages_of_document()'")
            #TODO: maybe rise exception

    return num_pages


def calculate_digits_of_number_for_base(base, number):
    '''
    @brief   Calculates the number of digits of a decimal number to another base.
    @details
        This function is needed in the burst section, when the number of digits
        for the different bases must be calculated automatically.
        It calculates the number of digits that this number needs for another base.
    @warning
        Does not work correct for negative numbers and bases!
    @note
        This function uses the `__floordiv__` operator `//`,
        for a "classic division" with truncated decimal places.
        `number //= base` equals `number = int(number / base)`

    @param[in] base   The base to which the number of digits is to be calculated
    @param[in] number The decimal number
    @retval    0      The number of digits cannot be determined
    @return           The number of digits determined
    '''
    digits = 0

    while number > 0:
        number //= base
        digits += 1

    return digits


def quote_and_escape_string(string):
    '''
    @brief Quote and escape strings for the command line.
    @details
        This function is used to prepare strings like filenames
        and passwords for the command line.
    @note About quoting
        Inside a single quoted string is the single quote character `'`
        the only character which has to be handled.
        But there is no escape character which works inside a single quoted string.
        Therefore a single quoted string must be ended, the single quote escaped
        and the rest of the string restarts quoted again.

    @param[in] string The string to quote
    return            The quoted and escaped string
    '''
    return "'" + string.replace(r"'", r"'\''") + "'"
