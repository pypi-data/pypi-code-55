import requests

def generate():
    # Requests data from page

    url = "https://icanhazdadjoke.com"
    headers = {'Accept': 'text/plain'}

    joke = requests.get(url, headers=headers)

    return joke.text