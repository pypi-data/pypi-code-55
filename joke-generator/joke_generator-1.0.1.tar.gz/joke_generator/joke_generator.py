import requests

def generate():
    # Requests data from page

    url = "https://icanhazdadjoke.com"
    headers = {'Accept': 'application/json'}

    r = requests.get(url, headers=headers)
    json_string = r.json()

    if json_string["status"] == 200:
        return json_string["joke"]
    else:
        raise ValueError("An error occured.")