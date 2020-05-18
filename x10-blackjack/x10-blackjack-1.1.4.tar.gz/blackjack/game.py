#!/usr/bin/env python3
"""
Sub-module defining the game's rules/logic and the game-loop's behaviours.
"""

# Python standard library imports
import time
import typing

# Non-standard library python package imports
import click
import tabulate

# Imports of module(s) internal to this project/package
from blackjack.game_objects import CardDeck
from blackjack.utils import (
    get_new_shuffled_deck,
    pick_from_top_of_deck,
    stringify_card_deck,
)


def main_loop(
    **kwargs,
) -> None:
    """
    Outer main loop which accommodates re-playability.

    Without having to re-start the program as a whole.
    """
    while True:
        game_loop(
            shuffled_deck=get_new_shuffled_deck(**kwargs),
            **kwargs,
        )
        if kwargs['autoplay']:
            click.echo(
                '`--auto-play` flag set, continuing until interrupt (e.g. CTRL+C)...\n',
                err=True,
            )
            time.sleep(1)
            continue
        if not click.confirm('\nDo you want to continue?', default=True):
            # User doesn't want to continue playing =)
            break


def sum_points_in_hand(
    hand: CardDeck,
) -> int:
    return sum(
        [
            card.points
            for card
            in hand
        ]
    )


def ascertain_winner(   # noqa: C901
    your_points: int,
    your_nickname: str,
    opponents_points: int,
    opponents_nickname: str,
) -> str:
    you_win = f"{your_nickname} won!"
    opponent_wins = f"{opponents_nickname} won!"

    if your_points == opponents_points:
        # This is only possible on first draw
        #   Where each player must both pick one Ace each,
        #   in addition to a card worth 10 points.
        return f"Tie - both got {your_points}."
    elif your_points == 21:
        return you_win
    elif opponents_points == 21:
        return opponent_wins

    # Now we know that nobody 'won' by getting 21
    #   Time to rule out losers, those who got more than 21
    if opponents_points > 21:
        return you_win
    elif your_points > 21:
        return opponent_wins

    # Now we're sure nobody got more than 21 points,
    #   time to ascertain winner
    if your_points < opponents_points:
        # Ref. below comment, this if-should always be true
        # with current implementation of rules
        # (AKA opponent always knowing your score and trying to beat it)
        return opponent_wins

    # This is impossible, for as long as opponent
    # _always_ draws cards while you're winning,
    # and _both_ of you are under or at 21 points...
    #   Thus code coverage pragma...
    return you_win  # pragma: no cover


def inner_game_loop_sequential_draws(    # noqa: C901
    input_deck: CardDeck,
    player_draw_limit: int,
    *,
    verbosity_level: int = 0,
) -> typing.Tuple[CardDeck, CardDeck]:
    """
    This function simulates the actual game.

    First the player draws up to (but not including) the specified draw limit.

    Then, the opponent draws cards either until the player is beat, or accumulated points are above 21.
    (The opponent doesn't draw cards when player has overextended - e.g. has more than 21 points accumulated).
    """
    # Initial draw, hard-coded to two cards each
    your_cards, input_deck = pick_from_top_of_deck(
        deck_to_pick_from=input_deck,
        amount=2,
    )
    opponents_cards, input_deck = pick_from_top_of_deck(
        deck_to_pick_from=input_deck,
        amount=2,
    )

    if (
        sum_points_in_hand(opponents_cards) == 21
        or sum_points_in_hand(your_cards) == 21
    ):
        # Game was won right of off the bat, first round
        return your_cards, opponents_cards

    # `list(your_cards)` - so as to use .extend() in while-loop
    your_cards, your_rounds = list(your_cards), 1
    while sum_points_in_hand(your_cards) < player_draw_limit:
        your_new_cards, input_deck = pick_from_top_of_deck(
            deck_to_pick_from=input_deck,
            amount=1,
        )
        if verbosity_level >= 3:
            click.echo(f"\nYou now picked; {your_new_cards}")
        your_cards.extend(your_new_cards)
        your_rounds += 1
    your_current_points = sum_points_in_hand(your_cards)
    if verbosity_level >= 2:
        click.echo(f"Your hand is now; {your_cards}")

    if your_current_points > 21:
        return your_cards, opponents_cards

    # Again, ensure `opponents_cards` is an extensible sequence (list)
    opponents_cards, opponents_rounds = list(opponents_cards), 1
    while (
        sum_points_in_hand(opponents_cards) <= your_current_points
        and sum_points_in_hand(opponents_cards) < 21
    ):
        # Your opponent doesn't draw points when
        #   she/he already beats your accumulated points
        # Or when you've already overextended yourself
        opponents_new_cards, input_deck = pick_from_top_of_deck(
            deck_to_pick_from=input_deck,
            amount=1,
        )
        if verbosity_level >= 3:
            click.echo(f"\nOpponent now picked; {opponents_new_cards}")
        opponents_cards.extend(opponents_new_cards)
        opponents_rounds += 1
    if verbosity_level >= 2:
        click.echo(f"Opponents hand is now; {opponents_cards}")
        click.echo(
            f"{len(input_deck)} remaining after "
            f"{max(your_rounds, opponents_rounds)} round(s)"
        )
    if verbosity_level >= 3:
        click.echo(f"\nDeck now remains with; {input_deck}")

    return your_cards, opponents_cards


def game_loop(
    nickname: str,
    shuffled_deck: CardDeck,
    *,
    no_internet: bool = False,
    opponents_nickname: str = 'Magnus',
    verbosity_level: int = 0,
    player_draw_limit: int = 17,
    **kwargs,
):
    """
        Inner game loop, a winner is declared per loop/invocation of this function.
    """

    your_cards, opponents_cards = inner_game_loop_sequential_draws(
        input_deck=shuffled_deck,
        player_draw_limit=player_draw_limit,
    )
    if verbosity_level >= 1:
        total_game_rounds = -1  # Firs round both draw two cards
        total_game_rounds += max(len(your_cards), len(opponents_cards))
        click.echo(f"Game is over after {total_game_rounds}", err=True)

    your_game_result = dict(
        Player=nickname.title(),
        Points=sum_points_in_hand(your_cards),
        Hand=stringify_card_deck(your_cards),
    )
    opponents_game_result = dict(
        Player=opponents_nickname.title(),
        Points=sum_points_in_hand(opponents_cards),
        Hand=stringify_card_deck(opponents_cards),
    )
    tabulated_output_string = tabulate.tabulate(
        (your_game_result, opponents_game_result),
        headers='keys',
    )
    click.echo(
        ascertain_winner(
            your_points=your_game_result['Points'],
            your_nickname=your_game_result['Player'],
            opponents_points=opponents_game_result['Points'],
            opponents_nickname=opponents_game_result['Player'],
        )
    )
    click.echo(tabulated_output_string)
