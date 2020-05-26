import getpass
import rubus.http as http
import requests


def create_user(config):
    user = {}
    user['username'] = input('Enter a username for the new user: ')
    user['email'] = input('Enter an email for the new user: ')
    user['password'] = getpass.getpass('Enter a password for the new user: ')
    answer = input('Do you want this user to be an administrator? [y/N] ')
    user['role'] = 'administrator' if answer == 'y' or answer == 'Y' else 'user'
    answer = input('Do you want to set an expiration date for the user? [Y/n] ')
    if answer not in ['n', 'N']:
        user['expiration'] = input('Enter an expiration date [YYYY-MM-DD]: ')

    r = requests.post(config.baseURL + '/admin/user', headers=config.headers,
                      json=user)

    if r.status_code == 201:
        return http.handle_response(r.json())
    
    print("\nError: ", r.json()['error'])


def delete_user(config, user_id):
    r = requests.delete(config.baseURL + '/admin/user/' + user_id,
                      headers=config.headers)

    if r.status_code == 204:
        return print('\nUser successfully deleted')
    
    print("\nError: ", r.json()['error'])


def list_user(config):
    r = requests.get(config.baseURL + '/admin/user', headers=config.headers)
    
    if r.status_code == 200:
        return http.handle_response(r.json())
    
    print("\nError: ", r.json()['error'])


def update_user_exp(config, user_id):
    exp = input('Enter a new expiration [YYYY-MM-DD]: ')
    params = {'expiration': exp}

    r = requests.post(config.baseURL + '/admin/user/' + user_id, params=params,
                      headers=config.headers)

    if r.status_code == 200:
        return http.handle_response(r.json())

    print("\nError: ", r.json()['error'])


def add_device(config):
    hostname = input('Enter the device\'s hostname: ')
    port = input('Enter the device\'s port: ')

    params = {'hostname': hostname, 'port': port}
    r = requests.post(config.baseURL + '/admin/device',
                      params=params, headers=config.headers)
    
    if r.status_code == 201:
        return http.handle_response(r.json())

    print("\nError: ", r.json()['error'])


def delete_device(config):
    hostname = input('Enter the device\'s hostname: ')
    device_id = input('Enter the device\'s id: ')

    params = {'hostname': hostname, 'deviceId': device_id}
    r = requests.delete(config.baseURL + '/admin/device',
                        params=params, headers=config.headers)

    if r.status_code == 204:
        return print('\nDevice has been deleted.')

    print("\nError: ", r.json()['error'])
