"""
A module that contains common methods for ciphers works
"""

import sys
from random import choice


def load(file):
    """
    Open a text file and return a list of lowercase string.
    Can throw Exceptions:
        - IOError if filename not found
    :param file: text file name ( and path, if needed)
    :return: A list of all words in a text file in lower case
    """

    try:
        with open(file) as in_file:
            loaded_text = in_file.read().strip().split('\n')
            loaded_text = [x.lower() for x in loaded_text]
            return loaded_text
    except IOError as exception:
        print("{}\n Error opening file {}".format(exception, file))
        sys.exit(1)


s_nouns = ["A dude", "My mom", "The king", "Some guy", "A cat with rabies",
           "A sloth", "Your homie", "This cool guy my gardener met yesterday", "Superman"]

s_verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures",
           "spies on", "retards", "meows on", "flees from", "tries to automate", "explodes"]

infinitives = ["to make a pie", "for no apparent reason", "because the sky is green",
               "for a disease", "to be able to make toast explode",
               "to know more about archeology"]


def create_simple_sentence(should_include_first_noun: bool = False) -> str:
    """
    Makes a random senctence from the different parts of speech. Uses a SINGULAR subject
    :param should_include_first_noun
    :return: sentence
    """
    possibles = [True, False]
    should_be_singular = choice(possibles)

    sentence = f"{choice(s_nouns).capitalize()} " if should_include_first_noun else ""

    if should_be_singular:
        sentence += f"{choice(s_verbs)} {choice(s_nouns)}"
    else:
        sentence += f"{choice(infinitives)}"

    return sentence

