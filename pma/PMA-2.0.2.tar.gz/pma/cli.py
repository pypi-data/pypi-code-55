"""
MIT License

Copyright (c) 2018-2020 Nihaal Sangha (Orangutan)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import click

from pma import ALL_PLCS, User, __version__
from pma.exceptions import InvalidLogin


def _status(text: str, newline: bool = False):
    m = "\r" + text + "\033[K"
    click.echo(m, nl=newline)


@click.group()
@click.version_option(__version__, prog_name='PMA')
def cli():
    pass


@cli.command()
@click.confirmation_option(help='Are you sure you want to farm points?')
@click.option(
    '--goal', default=-1, help='The goal score. If not given, it will continue until it stops gaining points.'
)
@click.argument('school_id', required=True, type=str)
@click.argument('username', required=True, type=str)
@click.argument('password', required=True, type=str)
def farm(goal, school_id: str, username: str, password: str):
    """Farms points using the school-id, username and password to login."""
    try:
        user = User.login(username, password, school_id)
    except InvalidLogin:
        _status('Invalid login credentials. Make sure you are a PiXL member.', newline=True)
        raise click.Abort()

    last_score = next(l for l in user.get_leaderboard() if l.username == username).score

    if last_score >= goal != -1:
        _status('Goal reached ({}).'.format(goal), newline=True)
        raise click.Abort()

    length_all_plcs = len(ALL_PLCS)
    length_longest_question = len(sorted(ALL_PLCS, reverse=True, key=lambda i: len(i['question']))[0]['question'])
    padding_max = max(len(str(last_score)) + 1, 5)

    removed_questions = []
    completed = 0
    while True:
        for question in ALL_PLCS:
            if len(removed_questions) == length_all_plcs:
                _status('\nGained maximum points for the week.', newline=True)
                raise click.Abort()

            if question['question'] in removed_questions:
                continue

            user.send_score(1, question['question'])
            completed += 1
            current_score = next(l for l in user.get_leaderboard() if l.username == username).score
            if current_score == last_score:
                removed_questions.append(question['question'])

            _status(
                "Last question: {:{}} "
                "Removed questions: {:{}}/{} "
                "Current score: {:{}} "
                "Completed: {:{}}".format(
                    question['question'],
                    length_longest_question,
                    len(removed_questions),
                    len(str(length_all_plcs)),
                    length_all_plcs,
                    current_score,
                    padding_max if goal == -1 else len(str(goal)),
                    completed,
                    padding_max if goal == -1 else len(str(goal - current_score + completed)),
                )
            )

            last_score = current_score
            if last_score >= goal != -1:
                _status('\nGoal reached ({}).'.format(goal), newline=True)
                raise click.Abort()
