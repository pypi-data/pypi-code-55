# importing requests package,click, login, user_login and json
from greet import login, user_login

import click
import requests
import json
import os


@click.command()
def get_started():
    """
    Worried? Here's some help!
    """
    login()
    session_details = open('user_session.txt', 'w')
    # opentdb api for the random trivia questions
    api_url = "https://opentdb.com/api.php?amount=50"
    response = requests.get(api_url)
    # fetching the data in json format using the click command
    click.echo(response.json())
    click.echo('\n')
    click.echo('-' * 100)
    session_details.close()
    os.remove('user_session.txt')
    # Handling endpoint errors
    try:
        response.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % exc)


if __name__ == '__main__':
    get_started()
