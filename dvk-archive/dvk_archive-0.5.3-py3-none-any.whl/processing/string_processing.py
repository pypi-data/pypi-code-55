#!/usr/bin/env python3

"""Functions for processing plain text."""


def extend_int(input_int: int = 0, input_length: int = 0) -> str:
    """
    Return a string representation of a given int with a given length.

    If the lenght of int is to small, adds leading 0s.
    If values are invalid, returns a string of zeros of the specified length.

    Parameters:
        input_int (int): Int value to return as string.
        input_length (int): Lenth of the string to return.

    Returns:
        str: String value of input_int with the length of input_length
    """
    if input_length is None or input_length == 0:
        return "0"
    if input_int is None:
        return extend_int(0, input_length)
    return_str = str(input_int)
    if input_length < len(return_str):
        return extend_int(0, input_length)
    while len(return_str) < input_length:
        return_str = "0" + return_str
    return return_str


def get_extension(filename: str = None) -> str:
    """
    Return the extension of a given filename.

    Parameters:
        filename (str): Given filename

    Returns:
        str: Extension of filename ("" if there is no extension)
    """
    if filename is not None and "." in filename:
        start = filename.rfind(".")
        end = filename.rfind("?")
        if end == -1 or end < start:
            end = len(filename)
        extension = filename[filename.rfind("."):end]
        if len(extension) < 7:
            return extension
    return ""


def get_filename(filename: str = None) -> str:
    """
    Convert a given string to a string safe to use as a filename.

    Parameters:
        filename (str): Given string to convert

    Returns:
        str: String safe to use as a filename.
    """
    if filename is None:
        return "0"
    cleaned = []
    # REMOVE NON-LATIN AND NON-NUMERIC CHARACTERS
    for i in range(0, len(filename)):
        char = ord(filename[i])
        if ((char > 47 and char < 58)
                or (char > 64 and char < 91)
                or (char > 96 and char < 123)
                or char == 32):
            cleaned.append(filename[i])
        else:
            cleaned.append("-")
    # REMOVE SPACERS FROM START AND END OF FILENAME
    while len(cleaned) > 0 and (cleaned[0] == "-" or cleaned[0] == " "):
        del cleaned[0]
    while len(cleaned) > 0 and (cleaned[-1] == "-" or cleaned[-1] == " "):
        del cleaned[-1]
    # REMOVE DUPLICATE SPACERS
    index = 1
    while index < len(cleaned):
        if ((cleaned[index] == " " or cleaned[index] == "-")
                and cleaned[index] == cleaned[index - 1]):
            del cleaned[index]
        else:
            index = index + 1
    # REMOVE HANGING HYPHENS
    index = 1
    while index < (len(cleaned) - 1):
        if cleaned[index] == "-":
            delete = False
            if cleaned[index - 1] == " " and not cleaned[index + 1] == " ":
                delete = True
            if not cleaned[index - 1] == " " and cleaned[index + 1] == " ":
                delete = True
            if delete:
                del cleaned[index]
                index = index - 1
        index = index + 1
    # TRUNCATE LONG TITLE
    cleaned_str = "".join(cleaned)
    cleaned_str = truncate_string(cleaned_str, 90)
    # JOIN CLEANED LIST
    if cleaned_str == "":
        return "0"
    return cleaned_str


def truncate_string(input_str: str = None, length: int = 0) -> str:
    """
    Shortens a string to be at or below a given length.

    Parameters:
        input_str (str): String to shorten
        length (int): Maximum length of the returned string

    Returns:
        str: Truncated string
    """
    if input_str is None or length < 1:
        return ""
    if len(input_str) <= length:
        return input_str
    # GET INDEX TO REMOVE FROM
    chr_list = list(input_str)
    if " " in input_str:
        index = input_str.rfind(" ")
    elif "-" in input_str:
        index = input_str.rfind("-")
    else:
        index = int(len(input_str) / 2)
    # DELETE CHARACTERS
    if index < (len(chr_list) - index):
        index = index + 1
        while index < len(chr_list) and len(chr_list) > length:
            del chr_list[index]
    else:
        index = index - 1
        while index > -1 and len(chr_list) > length:
            del chr_list[index]
            index = index - 1
        if (chr_list[index] == chr_list[index + 1]
                and (chr_list[index] == " " or chr_list[index] == "-")):
            del chr_list[index]
    # IF STILL TOO LONG
    if len(chr_list) > length:
        chr_list = chr_list[0:length]
    # REMOVE SPACERS FROM START AND END OF FILENAME
    while len(chr_list) > 0 and (chr_list[0] == "-" or chr_list[0] == " "):
        del chr_list[0]
    while len(chr_list) > 0 and (chr_list[-1] == "-" or chr_list[-1] == " "):
        del chr_list[-1]
    return "".join(chr_list)
