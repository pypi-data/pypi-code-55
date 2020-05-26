import rubus.http as http
import requests


def list(config):
    r = requests.get(config.baseURL + '/device', headers=config.headers)
    if r.status_code == 200:
        return http.handle_response(r.json())

    print("\nError: ", r.json()['error'])


def get(config, device_id):
    r = requests.get(config.baseURL + '/device/' + device_id, headers=config.headers)
    if r.status_code == 200:
        return http.handle_response(r.json())

    print("\nError: ", r.json()['error'])


def acquire(config, device_id):
    r = requests.post(config.baseURL + '/device/' + device_id + '/acquire',
                      headers=config.headers)
    if r.status_code == 200:
        return http.handle_response(r.json())

    print("\nError: ", r.json()['error'])


def release(config, device_id):
    r = requests.post(config.baseURL + '/device/' + device_id + '/release',
                      headers=config.headers)
    if r.status_code == 200:
        return http.handle_response(r.json())
    print("\nError: ", r.json()['error'])


def deploy(config, device_id):
    r = requests.post(config.baseURL + '/device/' + device_id + '/deploy',
                      headers=config.headers)
    if r.status_code == 204:
        return print('Device deployed.')

    print("\nError: ", r.json()['error'])


def on(config, device_id):
    r = requests.post(config.baseURL + '/device/' + device_id +
                      '/on', headers=config.headers)
    if r.status_code == 204:
        click.echo('Device is on.')

    print("\nError: ", r.json()['error'])


def off(config, device_id):
    r = requests.post(config.baseURL + '/device/' + device_id +
                      '/off', headers=config.headers)
    if r.status_code == 204:
        print('Device is off.')

    print("\nError: ", r.json()['error'])

