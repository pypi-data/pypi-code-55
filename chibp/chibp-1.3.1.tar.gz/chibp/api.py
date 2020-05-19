import requests
import urllib.parse

def get(email, key):
    if isinstance(email, str):
        return requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(email)}",
            headers={"hibp-api-key": key}  
        ).text
    
    if isinstance(email, list):
        result = {}
        for e in email:
            r = requests.get(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(e)}",
                headers={"hibp-api-key": key}  
            )
            result[e] = r.text
        return result
    
def get_full(email, key):
    if isinstance(email, str):
        return requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(email)}?truncateResponse=false",
             headers={"hibp-api-key": key}
        ).text

    if isinstance(email, list):
        result = {}
        for e in email:
            r = requests.get(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(e)}?truncateResponse=false",
                headers={"hibp-api-key": key}
            )
            result[e] = r.text
        return result

def get_breaches(key):
    return requests.get(
        f"https://haveibeenpwned.com/api/v3/breaches",
        headers={"hibp-api-key": key}
    ).text

def get_breach(site, key):
    return requests.get(
        f"https://haveibeenpwned.com/api/v3/breach/{site}",
        headers={"hibp-api-key": key}
    ).text

def get_pastes(email, key):
    return requests.get(
        f"https://haveibeenpwned.com/api/v3/pasteaccount/{urllib.parse.quote(email)}",
        headers={"hibp-api-key": key}
    ).text