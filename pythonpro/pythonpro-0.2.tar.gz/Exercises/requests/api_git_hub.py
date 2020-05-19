"""
This program gets a photo of a username in github using requests library.
"""

import requests


def get_avatar(usuario):
    """
    get a avatar of a user in github
    :param usuario: str with username
    :return: str with link of the photo.
    """
    url = f'https://api.github.com/users/{usuario}'
    response = requests.get(url)
    return response.json()['avatar_url']


if __name__ == '__main__':
    username = input('Digite su username in github : ')
    print(get_avatar(username))
