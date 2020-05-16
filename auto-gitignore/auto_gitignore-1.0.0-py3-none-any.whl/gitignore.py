"""
Using the https://www.gitignore.io/ API to get templates for a gitignore file
"""
import logging
import os

import requests
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator

logging.basicConfig(level=logging.WARNING,
                    format="%(asctime)s — %(levelname)s — Line:%(lineno)d — %(message)s")


def main():
    """
    Using the https://www.gitignore.io/ API to get templates for a gitignore file
    """
    # request to get all possible templates
    r = requests.get("https://www.gitignore.io/api/list?format=lines")
    # check for connection errors
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error:\n{err}")
        quit()

    templates = [line for line in r.text.splitlines()]
    logging.debug(templates)

    # setting the input completer to the list of templates from the API
    input_completer = WordCompleter(templates)
    # prompting the user for template input and setting them as parameter for next API call
    parameter = prompt("Enter all templates with a space in between: ",
                       completer=input_completer,
                       complete_while_typing=True
                       ).split()
    logging.info(parameter)

    # Check if list is empty
    if not parameter:
        print("Please enter at least one template!")
        quit()
    # Test if all parameters are in the templates list (taking care of invalid input here)
    for param in parameter:
        if param not in templates:
            print(f"Invalid Input: {param} not a valid template")
            quit()

    # actual request with parameters
    r = requests.get(f"https://www.gitignore.io/api/{','.join(parameter)}")
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error:\n{err}")
        quit()

    # setting up a validator
    validator = Validator.from_callable(
        validate, error_message="Please choose: a, w or q", move_cursor_to_end=True
    )

    # mode for writing the .gitignore file
    mode = "w"

    # check if a .gitignore file already exists
    if os.path.isfile(".gitignore"):
        print("A .gitignore file already exists in this location. Do you want to...\n"
              "...overwrite? Type w\n"
              "...append? Type a\n"
              "...quit? Type q")

        mode = prompt("Answer: ", validator=validator)
        if mode == "q":
            print("No changes were made.")
            quit()

    # write returned text into .gitignore file in the dir from which script was run
    with open(".gitignore", mode=mode) as f:
        f.write(r.text)

    # Success
    if mode == "a":
        print("Successfully updated .gitignore file")
    else:
        print("Successfully created .gitignore file")


def validate(text):
    """validate user input, if .gitignore already exists"""
    INPUT_LIST = ["w", "a", "q"]
    return text in INPUT_LIST


if __name__ == "__main__":
    main()
