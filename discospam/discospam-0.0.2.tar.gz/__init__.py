import requests

def Spam(webhook, message, pfpurl, username, amount=1):
    payload = {
        'content': message,
        'username': username,
    }

    for i in range(amount):
        requests.post(webhook, json=payload)

def Delete(webhook):
    requests.delete(webhook)