"""
File contains methods for document variable injection
"""
import re


def injector(document: str, params: dict, encapsulation: tuple = ("{{", "}}")):
    """
    Argument(s):
    - document      (str)   the document loaded as a string
    - params        (dict)  key,value == match,replacement
    - encapsulation (tuple)   variable encapsulation ('leftisde', 'rightside')

    Returns the provided document with injected parameters
    """

    # Compile regex pattern
    LEFT_SIDE, RIGHT_SIDE = encapsulation
    statement = r"(LEFT_SIDE.[a-z]{2,12}.[a-z]{2,12}.RIGHT_SIDE)".replace(
        "LEFT_SIDE", LEFT_SIDE
    ).replace("RIGHT_SIDE", RIGHT_SIDE)

    regex = re.compile(statement)

    # Inner method
    def inner(match):
        key: str = match.group().strip("}}").strip("{{")

        if key in params.keys():
            print(f"Variable substituted: '{key}' => '{params[key]}'")
            return params[key]

        return match.group()

    # Run substitution
    re.sub(pattern=regex, repl=inner, string=document)
