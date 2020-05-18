#!/usr/bin/env python3
"""
Sub-module containing miscellaneous utilities, which don't have a more fitting file within which to call "home".
"""

# Python standard library imports
import itertools
import random
import typing

# Non-standard library python package imports
import click
import requests

# Imports of module(s) internal to this project/package
from blackjack import game_objects


def greeting(
    who_you_want_to_greet: str = None,
) -> str:
    who_you_want_to_greet = who_you_want_to_greet.strip()
    if (
        not isinstance(who_you_want_to_greet, str)
        or not(who_you_want_to_greet)
        or any(
            # If any of these remain in string
            # after strip()-ing the string...
            char in who_you_want_to_greet
            for char in ('\r', '\n')
        )
    ):
        who_you_want_to_greet = 'you'
    return f"Welcome to a game of blackjack, {who_you_want_to_greet}!"


def stringify_card_deck(deck_to_print: game_objects.CardDeck) -> str:
    return ",".join(
        [
            str(card)
            for card in deck_to_print
        ]
    )


def get_new_shuffled_deck(
    *,
    no_internet: bool = False,
    verbosity_level: int = 0,
    shuffle_url: str = 'http://nav-deckofcards.herokuapp.com/shuffle',
    **kwargs,
) -> game_objects.CardDeck:
    if no_internet:
        shuffled_deck: game_objects.CardDeck = [
            game_objects.Card(
                value=v,
                suit=s,
            )
            for s, v
            in itertools.product(
                [s for s in game_objects.CardSuit],
                [v for v in game_objects.CardValue],
            )
        ]
        random.shuffle(shuffled_deck)
    else:
        if verbosity_level >= 1:
            click.echo(
                f"\tFetching shuffled deck of cards from '{shuffle_url}'...",
                err=True,
            )
        shuffled_cards_data = requests.get(shuffle_url).json()
        shuffled_deck: game_objects.CardDeck = [
            game_objects.Card.from_json(json_card_data)
            for json_card_data
            in shuffled_cards_data
        ]
    if verbosity_level >= 2:
        click.echo(
            '\tHere are the cards in deck to be used (in order);\n\t[',
            err=True,
        )
        for card in shuffled_deck:
            click.echo(f"\t\t{str(card)},", err=True)
        click.echo('\t]', err=True)
    if verbosity_level >= 1:
        click.echo(f"{len(shuffled_deck)} cards in deck!")
    return list(shuffled_deck)


def pick_from_top_of_deck(
    amount: int,
    deck_to_pick_from: game_objects.CardDeck,
) -> typing.Tuple[
    game_objects.CardDeck,
    game_objects.CardDeck,
]:
    type_err_msg = (
        f"`amount` must be a natural number greater than zero, not '{amount}'"
    )
    if type(amount) is not int:
        raise TypeError(type_err_msg)
    elif amount < 1:
        raise ValueError(type_err_msg)

    if len(deck_to_pick_from) == 0:
        raise ValueError(
            '`deck_to_pick_from` must contain one or more `Card`s.'
        )

    return (
        deck_to_pick_from[:amount],
        deck_to_pick_from[amount:],
    )
