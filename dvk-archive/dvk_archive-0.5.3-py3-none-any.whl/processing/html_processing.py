#!/usr/bin/env python3

"""Functions for processing HTML formatted text."""


def add_escapes(input_str: str = None) -> str:
    """
    Replace uncommon characters in a given string with HTML escape characters.

    Parameters:
        input_str (str): String in which to replace uncommon characters.

    Returns:
        str: String containing replacement HTML escape characters
    """
    if input_str is None:
        return ""
    char_index = 0
    output_str = ""
    while char_index < len(input_str):
        char_value = ord(input_str[char_index])
        if ((char_value > 47 and char_value < 58)
                or (char_value > 64 and char_value < 91)
                or (char_value > 96 and char_value < 123)
                or char_value == ord(" ")):
            output_str = output_str + input_str[char_index]
        else:
            output_str = output_str + "&#" + str(char_value) + ";"
        char_index = char_index + 1
    return output_str


def add_escapes_to_html(input_str: str = None) -> str:
    """
    Replace uncommon characters in a HTML string with HTML escape characters.

    Maintainins HTML formatting and tags.

    Parameters:
        input_str (str): Given HTML formatted string

    Returns:
        str: HTML string with replacement escape characters
    """
    if input_str is None:
        return ""
    char_index = 0
    output_str = ""
    while(char_index < len(input_str)):
        char_value = ord(input_str[char_index])
        if char_value == ord("\"") or char_value == ord("'"):
            end = input_str.find("\"", char_index + 1) + 1
            if end == 0:
                end = input_str.find("'", char_index + 1) + 1
            if end == 0:
                end = len(input_str)
            output_str = output_str + input_str[char_index:end]
            char_index = end - 1
        elif char_value > 31 and char_value < 127:
            output_str = output_str + input_str[char_index]
        else:
            output_str = output_str + "&#" + str(char_value) + ";"
        char_index = char_index + 1
    return output_str


def escape_to_char(escape: str = None) -> str:
    """
    Return a single character string from a given HTML escape character.

    Parameters:
        escape (str): Given HTML escape character

    Returns:
        str: Single character string representation of given escape character
    """
    if (escape is None
            or len(escape) < 3
            or not escape[0] == "&"
            or not escape[-1] == ";"):
        return ""
    mid = escape[1:-1]
    if mid == "quot":
        return "\""
    if mid == "apos":
        return "'"
    if mid == "amp":
        return "&"
    if mid == "lt":
        return "<"
    if mid == "gt":
        return ">"
    if mid == "nbsp":
        return " "
    if mid[0] == "#":
        try:
            out_char = chr(int(mid[1:len(mid)]))
            return out_char
        except ValueError:
            return ""
    return ""


def replace_escapes(input_str: str = None) -> str:
    """
    Replace HTML escape characters in a given string with unicode characters.

    Parameters:
        input_str (str): String from which to remove escape characters

    Returns:
        str: String with replaced escape characters
    """
    if input_str is None:
        return ""
    output_str = input_str
    start = output_str.find("&")
    while not start == -1:
        end = output_str.find(";", start)
        if not end == -1:
            end = end + 1
            replaced = output_str[0:start]
            replaced = replaced + escape_to_char(output_str[start:end])
            if end < len(output_str):
                replaced = replaced + output_str[end:len(output_str)]
            output_str = replaced
            start = output_str.find("&", start)
        else:
            start = -1
    return output_str
