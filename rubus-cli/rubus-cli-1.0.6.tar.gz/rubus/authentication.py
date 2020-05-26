import getpass
import rubus.http as http

import click
import requests


def login(baseURL: str):
    username = input("Username: ")
    password = getpass.getpass('Password: ')
    payload = {'username': username, 'password': password}
    r = requests.get(baseURL + '/login', params=payload)
    if r.status_code == 200:
        token = r.json()['token']
        return print(f'''You are logged in!

In order to perform any other command, set your session key to the
`RUBUS_SESSION` environment variable. ex:

$ export RUBUS_SESSION={token}

        ''')

    print("\nError: ", r.json()['error'])


def info(config):
    r = requests.get(config.baseURL + '/user/me', headers=config.headers)
    if r.status_code == 200:
        return http.handle_response(r.json())
    
    print("\nError: ", r.json()['error'])


def update(config):
    user = {}

    answer = input('Do you want to update your username? [y/N] ')
    if answer == 'y' or answer == 'Y':
        user['username'] = input('Enter a new Username: ')

    answer = input('Do you want to update your email? [y/N] ')
    if answer == 'y' or answer == 'Y':
        user['email'] = input('Enter a new Email: ')

    answer = input('Do you want to update your password? [y/N] ')
    if answer == 'y' or answer == 'Y':
        user['password'] = getpass.getpass('Enter a new Password: ')

    r = requests.put(config.baseURL + '/user/me',
                     headers=config.headers, json=user)

    if r.status_code == 200:
        return http.handle_response(r.json())
    
    print("\nError: ", r.json()['error'])
